
# Task 3: Visualise Traffic Patterns


import logging
from pathlib import Path

import matplotlib

# Save charts without opening a window 
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from pipeline import configure_logging
from feature_engineering import validate_features

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


#Load and check the saved feature data.

def load_feature_data(file_path):
    data = pd.read_csv(
        file_path,
        keep_default_na=False,
        parse_dates=["date_time"]
    )

    validate_features(data)

    logger.info(
        "Chart data has loaded. There are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )

    return data


# Save each chart

def save_chart(chart, filename):
    chart_path = BASE_DIR / "charts" / filename
    chart_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        chart.tight_layout()
        chart.savefig(chart_path, dpi=150)

        logger.info(
            "Chart is saved to %s.",
            chart_path.relative_to(BASE_DIR).as_posix()
        )
    finally:
        plt.close(chart)


# Create a chart of average recorded traffic by hour.
def chart_traffic_by_hour(data):
    hourly_traffic = (
        data.groupby("hour")["traffic_volume"]
        .mean()
        .reindex(range(24))
    )

    chart, ax = plt.subplots(figsize=(10, 5))

    ax.bar(hourly_traffic.index, hourly_traffic.values)
    ax.set_title("Average Traffic Volume by Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Traffic Volume")
    ax.set_xticks(range(24))

    # Save the chart.
    save_chart(chart, "traffic_by_hour.png")

    return hourly_traffic


# Compare average traffic on weekdays and weekends.
def chart_weekday_weekend(data):
    weekend_traffic = (
        data.groupby("is_weekend")["traffic_volume"]
        .mean()
        .reindex([0, 1])
    )
    weekend_traffic.index = ["Weekday", "Weekend"]

    chart, ax = plt.subplots(figsize=(7, 5))

    ax.bar(weekend_traffic.index, weekend_traffic.values)
    ax.set_title("Average Traffic Volume on Weekdays and Weekends")
    ax.set_xlabel("Day Type")
    ax.set_ylabel("Average Traffic Volume")

    save_chart(chart, "weekday_weekend_traffic.png")

    return weekend_traffic


# Compare weather averages and keep record counts for interpretation.
def chart_traffic_by_weather(data):
    weather_summary = (
        data.groupby("weather_main")["traffic_volume"]
        .agg(average_traffic="mean", records="size")
        .sort_values("average_traffic")
    )

    chart, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        weather_summary.index,
        weather_summary["average_traffic"]
    )
    ax.set_title("Average Traffic Volume by Weather Category")
    ax.set_xlabel("Average Traffic Volume")
    ax.set_ylabel("Weather Category")

    save_chart(chart, "traffic_by_weather.png")

    return weather_summary


#Load the feature data and create all three charts.
def run_visualizations():
    input_path = BASE_DIR / "data" / "traffic_features.csv"
    data = load_feature_data(input_path)

    # Each chart function saves its output and logs the path.
    hourly_traffic = chart_traffic_by_hour(data)
    weekend_traffic = chart_weekday_weekend(data)
    weather_summary = chart_traffic_by_weather(data)

    logger.info("All three traffic charts have saved.")

    # Return the summaries for use.
    return {
        "hourly_traffic": hourly_traffic,
        "weekend_traffic": weekend_traffic,
        "weather_summary": weather_summary
    }


# Configure loggin
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create Traffic Charts."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Include detailed DEBUG messages."
    )
    args = parser.parse_args()

    try:
        configure_logging(debug=args.debug)
        logger.info("Traffic visualisation has started.")

        run_visualizations()

        logger.info("Traffic visualisation has completed successfully.")
        return 0

    except (
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
        KeyError,
        pd.errors.ParserError
    ):
        logger.error(
            "Traffic visualisation could not be completed.",
            exc_info=True
        )
        return 1




if __name__ == "__main__":
    raise SystemExit(main())
