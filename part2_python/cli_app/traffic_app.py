
# Task 4: Build a Mini Traffic Analytics Application.
import argparse
import logging
from pathlib import Path

import pandas as pd

import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pipeline import (
    configure_logging,
    validate_schema,
    validate_cleaned_data
)
from feature_engineering import validate_features

logger = logging.getLogger(__name__)



# HAndle invalid command arguments
class TrafficArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(f"Invalid command arguments: {message}.")


#Load and check the processed data before answering a command.
def load_app_data():
    input_path = BASE_DIR / "data" / "traffic_features.csv"

    data = pd.read_csv(
        input_path,
        keep_default_na=False
    )

    validate_schema(data)

    #Invalid dates become missing values and fail validation.
    data["date_time"] = pd.to_datetime(
        data["date_time"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    validate_cleaned_data(data)
    validate_features(data)

    logger.info(
        "Application data has been loaded. There are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )

    return data


#Find traffic records for a specific date and time.
def query_datetime(data, date_time_text):
    from datetime import datetime


    try:
        requested_time = datetime.strptime(
            date_time_text,
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        raise ValueError(
            "Use a valid date and time in YYYY-MM-DD HH:MM:SS format."
        ) from None

    matching_rows = data.loc[
        data["date_time"] == requested_time,
        [
            "date_time",
            "traffic_volume",
            "traffic_category",
            "weather_main",
            "weather_description",
            "temp",
            "rain_1h",
            "snow_1h"
        ]
    ]


    if matching_rows.empty:
        print("No records were found for that date and time.")
    else:
        print(matching_rows.to_string(index=False))


# Identify records above the requested traffic-volume threshold.

def query_high_traffic(data, threshold):
    if threshold < 0:
        raise ValueError("The traffic threshold must be zero or greater.")

    matching_rows = data.loc[
        data["traffic_volume"] > threshold,
        [
            "date_time",
            "traffic_volume",
            "traffic_category",
            "weather_main"
        ]
    ].sort_values("traffic_volume", ascending=False)

    if matching_rows.empty:
        print("No records were found above that traffic threshold.")
    else:
        print(matching_rows.to_string(index=False))

#Compare average traffic volume on weekdays and weekends.
def compare_days(data):
    summary = (
        data.groupby("is_weekend")["traffic_volume"]
        .agg(average_traffic="mean", records="size")
        .reindex([0, 1])
    )

    summary.index = ["Weekday", "Weekend"]
    summary.index.name = "day_type"

    print(summary.round({"average_traffic": 2}).to_string())

#Defin the application's commands and arguments.

def build_parser():
    parser = TrafficArgumentParser(
        description="Query and compare traffic data."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Include detailed DEBUG messages."
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    date_command = commands.add_parser(
        "query",
        help="Find records for a specific date and time."
    )
    date_command.add_argument(
        "--datetime",
        required=True,
        help="Date and time in YYYY-MM-DD HH:MM:SS format."
    )

    traffic_command = commands.add_parser(
        "high-traffic",
        help="Find records above a traffic-volume threshold."
    )
    traffic_command.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="A traffic-volume threshold of zero or greater."
    )

    commands.add_parser(
        "compare-days",
        help="Compare average weekday and weekend traffic."
    )

    return parser

#Run the requested command and handle application errors.
def main():
    import sys

    try:
        configure_logging()
        logger.info(
            "Application is invoked with arguments %s.",
            sys.argv[1:]
        )

        parser = build_parser()
        args = parser.parse_args()

        if args.debug:
            configure_logging(debug=True)

        logger.info(
            "Command %s is invoked with arguments %s.",
            args.command,
            vars(args)
        )

        data = load_app_data()

        if args.command == "query":
            query_datetime(data, args.datetime)
        elif args.command == "high-traffic":
            query_high_traffic(data, args.threshold)
        elif args.command == "compare-days":
            compare_days(data)

        logger.info("Traffic application command has completed successfully.")
        return 0

    except (
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
        KeyError,
        pd.errors.ParserError
    ) as error:
        logger.error("Traffic application could not complete: %s.", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
