"""Recommend travel windows using supplied candidate conditions."""

import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

PART3_DIR = Path(__file__).resolve().parent.parent

recommendation_model = joblib.load(
    PART3_DIR / "models" / "random_forest_regression_v1.joblib"
)

recommendation_config = joblib.load(
    PART3_DIR / "models" / "preparation_config_v1.joblib"
)

weather_encoder = (
    recommendation_model.named_steps["preprocessor"]
    .named_transformers_["weather"]
)

known_weather = set(weather_encoder.categories_[0])


def prepare_recommendation_inputs(candidates):
    prepared = candidates.copy()

    required_columns = [
        "date_time",
        "temp",
        "rain_1h",
        "snow_1h",
        "clouds_all",
        "weather_main",
        "is_holiday"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in prepared.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}."
        )

    if prepared.empty:
        raise ValueError("At least one candidate hour is required.")

    
    prepared["date_time"] = pd.to_datetime(
        prepared["date_time"],
        errors="coerce"
    )

    if prepared["date_time"].isna().any():
        raise ValueError("Candidate timestamps must be valid.")

    if prepared["date_time"].dt.tz is not None:
        raise ValueError(
            "Use local corridor timestamps without timezone offsets."
        )

    if not prepared["date_time"].eq(
        prepared["date_time"].dt.floor("h")
    ).all():
        raise ValueError("Candidate timestamps must be on the hour.")

    if prepared["date_time"].duplicated().any():
        raise ValueError("Candidate timestamps must be unique.")

    # Require explicit, finite measurements for this recommendation.
    numeric_columns = [
        "temp", "rain_1h", "snow_1h", "clouds_all", "is_holiday"
    ]

    
    for column in numeric_columns:
        prepared[column] = pd.to_numeric(
            prepared[column], errors="coerce"
        )

    if not np.isfinite(
        prepared[numeric_columns].to_numpy(dtype=float)
    ).all():
        raise ValueError("Numeric inputs must be finite numbers.")

    if not prepared["temp"].between(200, 330).all():
        raise ValueError(
            "Temperature must be between 200 and 330 Kelvin "
        )

    if not prepared["rain_1h"].between(0, 9000).all():
        raise ValueError("Rainfall must be between 0 and 9000 mm.")

    if (prepared["snow_1h"] < 0).any():
        raise ValueError("Snowfall must be non-negative.")

    if not prepared["clouds_all"].between(0, 100).all():
        raise ValueError("Cloud cover must be between 0 and 100.")

    if not prepared["is_holiday"].isin([0, 1]).all():
        raise ValueError("The holiday flag must be 0 or 1.")

    prepared["weather_main"] = (
        prepared["weather_main"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    if not prepared["weather_main"].isin(known_weather).all():
        raise ValueError(
            "Weather categories must match those used in training."
        )

    # Recreate time and weather features.
    prepared["hour"] = prepared["date_time"].dt.hour
    prepared["day_of_week"] = prepared["date_time"].dt.dayofweek
    prepared["month"] = prepared["date_time"].dt.month
    prepared["is_weekend"] = (
        prepared["day_of_week"] >= 5
    ).astype(int)

    hour_angle = 2 * np.pi * prepared["hour"] / 24
    weekday_angle = 2 * np.pi * prepared["day_of_week"] / 7

    prepared["hour_sin"] = np.sin(hour_angle)
    prepared["hour_cos"] = np.cos(hour_angle)
    prepared["weekday_sin"] = np.sin(weekday_angle)
    prepared["weekday_cos"] = np.cos(weekday_angle)


    
    prepared["has_rain"] = (
        prepared["rain_1h"] > 0
    ).astype(int)

    prepared["has_snow"] = (
        prepared["snow_1h"] > 0
    ).astype(int)

    prepared["is_low_visibility"] = (
        prepared["weather_main"].isin(
            recommendation_config["low_visibility_weather"]
        )
    ).astype(int)

    return prepared[
        recommendation_config["feature_columns"]
    ].copy()

def recommend_travel_window(candidates):
    try:
        model_inputs = prepare_recommendation_inputs(candidates)
        predictions = recommendation_model.predict(model_inputs)

        if not np.isfinite(predictions).all():
            raise ValueError("Model predictions must be finite.")

        
        ranked = candidates.copy()
        ranked["date_time"] = pd.to_datetime(ranked["date_time"])
        ranked["predicted_traffic_volume"] = predictions

        ranked = ranked.sort_values(
            ["predicted_traffic_volume", "date_time"],
            kind="stable"
        ).reset_index(drop=True)

        ranked.insert(0, "rank", np.arange(1, len(ranked) + 1))

        best = ranked.iloc[0]
        highest = ranked["predicted_traffic_volume"].max()
        difference = highest - best["predicted_traffic_volume"]

        message = (
            f"Among the {len(ranked)} supplied candidate hours, "
            f"{best['date_time']:%d %B %Y at %H:%M} has the "
            f"lowest predicted traffic volume, approximately "
            f"{best['predicted_traffic_volume']:.0f} vehicles "
            f"during that hour. "
            f"This is approximately {difference:.0f} fewer than "
            f"the highest-volume candidate. "
            "The comparison uses yje  supplied weather and holiday "
            "assumptions; it is not live traffic information or "
            "a journey-time estimate."
        )

        logger.info(
            "Ranked %s candidate hours and prepared a recommendation.",
            len(ranked)
        )

        return ranked, message


    except (ValueError, TypeError, KeyError):
        logger.error("Travel-window recommendation failed.")
        raise
