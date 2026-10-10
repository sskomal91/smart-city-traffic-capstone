
# Task 2: Feature Engineering

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from pipeline import configure_logging, validate_cleaned_data

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


# Load and check the cleaned data before adding features.

def load_cleaned_data(file_path):
    data = pd.read_csv(
        file_path,
        keep_default_na=False
    )

    data["date_time"] = pd.to_datetime(
        data["date_time"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    validate_cleaned_data(data)

    logger.info(
        "Before feature engineering, there are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )

    return data


# Add the required time features.

def add_time_features(data):
    featured = data.copy()

    # Monday is 0 and Sunday is 6.
    featured["hour"] = featured["date_time"].dt.hour
    featured["day_of_week"] = featured["date_time"].dt.dayofweek

    # Use 1 for weekends and 0 for weekdays.
    featured["is_weekend"] = (
        featured["day_of_week"] >= 5
    ).astype(int)


    hour_angle = 2 * np.pi * featured["hour"] / 24
    featured["hour_sin"] = np.sin(hour_angle)
    featured["hour_cos"] = np.cos(hour_angle)

    logger.info("Time features and cyclical hour features were added.")

    return featured


# Encode weather categories 
#Add rain and snow indicators.
def add_weather_features(data):
    featured = data.copy()


    featured["has_rain"] = (featured["rain_1h"] > 0).astype(int)
    featured["has_snow"] = (featured["snow_1h"] > 0).astype(int)

    # Create one 0 or 1 column for each main weather category.
    weather_encoded = pd.get_dummies(
        featured["weather_main"],
        prefix="weather",
        dtype=int
    )

    featured = pd.concat(
        [featured, weather_encoded],
        axis=1
    )

    logger.info("Weather encoding, rain and snow features have been added.")

    return featured


# Scale temperature and rainfall to the range 0 to 1.

def add_scaled_features(data):
    featured = data.copy()

    for column in ["temp", "rain_1h"]:
        minimum = featured[column].min()
        maximum = featured[column].max()


        logger.debug(
            "%s scaling minimum is %s and maximum is %s.",
            column,
            minimum,
            maximum
        )

        # HAnle dividing by zero when all values are equal.
        if maximum == minimum:
            featured[f"{column}_scaled"] = 0.0
        else:
            featured[f"{column}_scaled"] = (
                (featured[column] - minimum)
                / (maximum - minimum)
            )

        logger.info("%s scaled feature have bee added.", column)

    return featured


#Create traffic categories using the cleaned data distribution.
def add_traffic_category(data):
    featured = data.copy()

    #Percentiles make the thresholds depend on the actual data.
    # The lowest quarter is Low and the highest quarter is High.
    #The middle half is Medium. Ties can change the group sizes.
    # These labels describe relative volume

    lower_threshold = featured["traffic_volume"].quantile(0.25)
    upper_threshold = featured["traffic_volume"].quantile(0.75)

    # Show calculated thresholds only in debug mode.
    logger.debug(
        "Traffic category thresholds are %s and %s vehicles.",
        lower_threshold,
        upper_threshold
    )

    # Check Low first, then Medium, and assign High to the rest.
    featured["traffic_category"] = np.select(
        [
            featured["traffic_volume"] <= lower_threshold,
            featured["traffic_volume"] <= upper_threshold
        ],
        ["Low", "Medium"],
        default="High"
    )

    logger.info("Data-driven traffic categories have been added.")

    return featured


#Check the generated features before saving them.
def validate_features(data):


    weather_columns = [
        column for column in data.columns
        if column.startswith("weather_")
        and column not in ["weather_main", "weather_description"]
    ]

    checks = {
        "unique_column_names": data.columns.is_unique,
        "no_missing_values": not data.isna().any().any(),
        "valid_hours": data["hour"].between(0, 23).all(),
        "valid_weekdays": data["day_of_week"].between(0, 6).all(),
        "correct_weekends": data["is_weekend"].eq(
            (data["day_of_week"] >= 5).astype(int)
        ).all(),
        "valid_hour_cycle": np.allclose(
            data["hour_sin"] ** 2 + data["hour_cos"] ** 2,
            1
        ),
        "valid_weather_encoding": (
            bool(weather_columns)
            and data[weather_columns].isin([0, 1]).all().all()
            and data[weather_columns].sum(axis=1).eq(1).all()
        ),
        "correct_rain_indicator": data["has_rain"].eq(
            (data["rain_1h"] > 0).astype(int)
        ).all(),
        "correct_snow_indicator": data["has_snow"].eq(
            (data["snow_1h"] > 0).astype(int)
        ).all(),
        "valid_scaled_values": (
            data["temp_scaled"].between(0, 1).all()
            and data["rain_1h_scaled"].between(0, 1).all()
        ),
        "valid_traffic_categories": data["traffic_category"].isin(
            ["Low", "Medium", "High"]
        ).all()
    }

    #Stop the script if any feature check fails.
    failed_checks = [
        name for name, passed in checks.items()
        if not passed
    ]

    if failed_checks:
        raise ValueError(
            f"Feature checks failed: {failed_checks}."
        )

    logger.info(
        "Feature checks have been  passed. After feature engineering, "
        "there are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )


# Run feature engineering using the cleaned CSV.
def run_feature_engineering():
    input_path = BASE_DIR / "data" / "traffic_cleaned.csv"
    output_path = BASE_DIR / "data" / "traffic_features.csv"

    data = load_cleaned_data(input_path)

    # Add each group of features in order.
    data = add_time_features(data)
    data = add_weather_features(data)
    data = add_scaled_features(data)
    data = add_traffic_category(data)

    # Save only after the feature validaion checks is complete.
    validate_features(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

    logger.info("Feature data has saved to data/traffic_features.csv.")

    return data





#Configure logging 

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create traffic features."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Include detailed DEBUG messages."
    )
    args = parser.parse_args()

    try:
        configure_logging(debug=args.debug)
        logger.info("Feature engineering has started.")

        run_feature_engineering()

        logger.info("Feature engineering has completed successfully.")
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
            "Feature engineering could not be completed.",
            exc_info=True
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
