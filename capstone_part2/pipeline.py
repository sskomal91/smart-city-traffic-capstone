

# Task 1: Load, check and clean the traffic data.


import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent

EXPECTED_COLUMNS = [
    "holiday",
    "temp",
    "rain_1h",
    "snow_1h",
    "clouds_all",
    "weather_main",
    "weather_description",
    "date_time",
    "traffic_volume"
]

category_columns = [
    "holiday",
    "weather_main",
    "weather_description"
]


# Set up logging for the main program start
def configure_logging(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(BASE_DIR / "pipeline.log", encoding="utf-8")
        ],
        force=True
    )


# Load the raw CSV and find out it's size.
def load_raw_data(file_path):
    data = pd.read_csv(file_path, keep_default_na=False)

    logger.info(
        "Raw CSV has loaded succesfully. There are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )

    return data


# Check required columns before cleaning the data.
def validate_schema(data):
    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}."
        )

    logger.info("Column check has passed. All required columns are present.")


# Make the category text consistent.


def standardise_categories(data):
    cleaned = data.copy()

    for column in category_columns:
        original = cleaned[column]
        standardised = original.astype("string").str.strip()

        if column == "weather_description":
            standardised = standardised.str.lower()
        else:
            standardised = standardised.str.title()

        changed_rows = int(
            original.ne(standardised).fillna(False).sum()
        )
        cleaned[column] = standardised

        if changed_rows > 0:
            logger.warning(
                "%s: changed %s rows to fix spaces and capital letters.",
                column,
                changed_rows
            )
        else:
            logger.info("%s: no text changes are required.", column)

    return cleaned


# Convert the dates and remove rows with missing or invalid dates.

def clean_datetime(data):
    cleaned = data.copy()

    cleaned["date_time"] = pd.to_datetime(
        cleaned["date_time"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    invalid_dates = cleaned["date_time"].isna()
    count = int(invalid_dates.sum())

    if count > 0:
        cleaned = cleaned.loc[~invalid_dates].copy()
        logger.warning(
            "Dropped %s rows because their dates were missing or invalid.",
            count
        )
    else:
        logger.info("Date check has passed. No missing or invalid dates.")

    logger.info("date_time is now in datetime format.")

    return cleaned


# Remove rows that match exactly across every column.

def remove_duplicates(data):
    count = int(data.duplicated().sum())
    cleaned = data.drop_duplicates().copy()

    if count > 0:
        logger.warning(
            "Dropped %s rows because all their values were duplicates.",
            count
        )
    else:
        logger.info("Duplicate check finished. No exact duplicates found.")

    logger.info(
        "After removing duplicates, there are %s rows and %s columns.",
        cleaned.shape[0],
        cleaned.shape[1]
    )

    return cleaned


# Convert the numerical columns into numbers.

def convert_numeric_columns(data):
    cleaned = data.copy()

    numeric_columns = [
        "temp",
        "rain_1h",
        "snow_1h",
        "clouds_all",
        "traffic_volume"
    ]

    for column in numeric_columns:
        original = cleaned[column]


        converted = pd.to_numeric(original, errors="coerce")

        invalid_count = int(
            (original.notna() & converted.isna()).sum()
        )

        cleaned[column] = converted

        if invalid_count > 0:
            logger.warning(
                "%s: changed %s unreadable values to missing values.",
                column,
                invalid_count
            )
        else:
            logger.info("%s: number conversion finished.", column)

    return cleaned


# Fix missing or impossible temperatures using monthly medians.

def fix_temperature(data):
    cleaned = data.copy()

    invalid = (
        cleaned["temp"].isna()
        | ~np.isfinite(cleaned["temp"])
        | (cleaned["temp"] <= 0)
    )

    months = cleaned["date_time"].dt.month

    # Use a separate median for each calendar month across all years.
    for month in sorted(months.unique()):
        month_rows = months == month
        rows_to_fix = month_rows & invalid
        count = int(rows_to_fix.sum())

        if count == 0:
            continue

        # Keep invalid readings out of the median calculation.
        monthly_median = cleaned.loc[
            month_rows & ~invalid, "temp"
        ].median()

        if pd.isna(monthly_median):
            raise ValueError(
                f"No valid temperature readings for month {month}."
            )

        logger.debug(
            "Month %s temperature median is %s Kelvin.",
            month,
            monthly_median
        )

        cleaned.loc[rows_to_fix, "temp"] = monthly_median

        logger.warning(
            "Fixed %s missing or invalid temperatures in month %s "
            "using the monthly median.",
            count,
            month
        )

    if not invalid.any():
        logger.info("Temperature check passed. No changes needed.")

    return cleaned


# Fix missing or invalid rainfall using monthly medias.

def fix_rainfall(data):
    cleaned = data.copy()

    #Use the rainfall limit given in the assignment.
    invalid = (
        cleaned["rain_1h"].isna()
        | ~np.isfinite(cleaned["rain_1h"])
        | (cleaned["rain_1h"] < 0)
        | (cleaned["rain_1h"] > 9000)
    )

    months = cleaned["date_time"].dt.month

    # Find a seprate median for each calendar month.
    for month in sorted(months.unique()):
        month_rows = months == month
        rows_to_fix = month_rows & invalid
        count = int(rows_to_fix.sum())

        if count == 0:
            continue

        # Exclude invalid readings from the median.
        monthly_median = cleaned.loc[
            month_rows & ~invalid, "rain_1h"
        ].median()

        if pd.isna(monthly_median):
            raise ValueError(
                f"No valid rainfall readings for month {month}."
            )

        logger.debug(
            "Month %s rainfall median is %s mm.",
            month,
            monthly_median
        )

        cleaned.loc[rows_to_fix, "rain_1h"] = monthly_median

        logger.warning(
            "Fixed %s missing or invalid rainfall readings in month %s "
            "using the monthly median.",
            count,
            month
        )

    if not invalid.any():
        logger.info("Rainfall check ic complrete. No changes required.")

    return cleaned


# Fill missing category text with an explicit label.

def fill_missing_categories(data):
    cleaned = data.copy()

    for column in category_columns:
        missing = (
            cleaned[column].isna()
            | cleaned[column].eq("").fillna(False)
        )
        count = int(missing.sum())

        if count > 0:
            cleaned.loc[missing, column] = "Unknown"

            logger.warning(
                "%s: filled %s missing values with Unknown.",
                column,
                count
            )
        else:
            logger.info("%s: no missing category values.", column)

    return cleaned


# Remove rows with invalid values in the remaining numerical fields.
def clean_other_numbers(data):
    cleaned = data.copy()

    invalid_checks = {
        "snow_1h": (
            ~np.isfinite(cleaned["snow_1h"])
            | (cleaned["snow_1h"] < 0)
        ),
        "clouds_all": (
            ~np.isfinite(cleaned["clouds_all"])
            | ~cleaned["clouds_all"].between(0, 100)
            | (cleaned["clouds_all"] % 1 != 0)
        ),
        "traffic_volume": (
            ~np.isfinite(cleaned["traffic_volume"])
            | (cleaned["traffic_volume"] < 0)
            | (cleaned["traffic_volume"] % 1 != 0)
        )
    }

    for column, invalid in invalid_checks.items():
        # Count only rows still present after previous checks.
        rows_to_drop = invalid.loc[cleaned.index]
        count = int(rows_to_drop.sum())

        if count > 0:
            cleaned = cleaned.loc[~rows_to_drop].copy()

            logger.warning(
                "Dropped %s rows because %s was missing or invalid.",
                count,
                column
            )
        else:
            logger.info("%s: no missing or invalid numbers.", column)

    return cleaned


# Stop the pipeline if cleaned data still has problems.
def validate_cleaned_data(data):

    if data.empty:
        raise ValueError("There are no rows remain after cleaning.")

    # Check for missing cells and blank text.
    for column in data.columns:
        missing = data[column].isna()

        if pd.api.types.is_object_dtype(data[column]) or \
                pd.api.types.is_string_dtype(data[column]):
            blank = data[column].astype("string").str.strip().eq("")
            missing = missing | blank.fillna(False)

        if missing.any():
            raise ValueError(f"Missing values remain in {column}.")

    # Check each numerical field against its allowed range.
    checks = {
        "temp": (
            np.isfinite(data["temp"])
            & (data["temp"] > 0)
        ),
        "rain_1h": (
            np.isfinite(data["rain_1h"])
            & data["rain_1h"].between(0, 9000)
        ),
        "snow_1h": (
            np.isfinite(data["snow_1h"])
            & (data["snow_1h"] >= 0)
        ),
        "clouds_all": (
            np.isfinite(data["clouds_all"])
            & data["clouds_all"].between(0, 100)
            & (data["clouds_all"] % 1 == 0)
        ),
        "traffic_volume": (
            np.isfinite(data["traffic_volume"])
            & (data["traffic_volume"] >= 0)
            & (data["traffic_volume"] % 1 == 0)
        )
    }

    for column, valid in checks.items():
        if not valid.all():
            raise ValueError(f"Invalid numbers remain in {column}.")

    if not pd.api.types.is_datetime64_any_dtype(data["date_time"]):
        raise ValueError("date_time is not in proper datetime format.")

    if data.duplicated().any():
        raise ValueError("Exact duplicate rows remain.")

    logger.info(
        "Cleaned data checks completed. There are %s rows and %s columns.",
        data.shape[0],
        data.shape[1]
    )


#Run the cleaning steps in order.

def run_pipeline():
    raw_path = (
        BASE_DIR.parent
        / "part1_data_analytics"
        / "Metro_Interstate_Traffic_Volume.csv"
    )
    output_path = BASE_DIR / "data" / "traffic_cleaned.csv"

    data = load_raw_data(raw_path)
    validate_schema(data)

    data = standardise_categories(data)
    data = clean_datetime(data)
    data = convert_numeric_columns(data)
    data = fill_missing_categories(data)
    data = clean_other_numbers(data)
    data = remove_duplicates(data)
    data = fix_temperature(data)
    data = fix_rainfall(data)

    # Imputation can create duplicates, so check again afterwards.
    data = remove_duplicates(data)
    validate_cleaned_data(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

    logger.info("Cleaned data saved to data/traffic_cleaned.csv.")

    return data


#Configure logging onl when the script is run directly.
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Clean traffic data.")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Include detailed DEBUG messages."
    )
    args = parser.parse_args()

    try:
        configure_logging(debug=args.debug)
        logger.info("Traffic pipeline started.")

        run_pipeline()

        logger.info("Traffic pipeline completed succesfully.")
        return 0

    except (OSError, UnicodeError, ValueError, TypeError,
            KeyError, pd.errors.ParserError):
        logger.error("Traffic pipeline could not completed.", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
