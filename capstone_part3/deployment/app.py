"""Local traffic prediction and feature monitoring simulation."""

import hashlib
import importlib.util
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
PART3_DIR = Path(__file__).resolve().parent.parent
deployment_dir = PART3_DIR / "deployment"

saved_manifest = json.loads(
    (deployment_dir / "deployment_manifest.json").read_text(
        encoding="utf-8"
    )
)
monitoring_config = json.loads(
    (deployment_dir / "monitoring_reference.json").read_text(
        encoding="utf-8"
    )
)

for file_key, hash_key in [
    ("model_file", "model_sha256"),
    ("preparation_file", "preparation_sha256")
]:
    artifact_path = PART3_DIR / saved_manifest[file_key]
    actual_hash = hashlib.sha256(
        artifact_path.read_bytes()
    ).hexdigest()
    if actual_hash != saved_manifest[hash_key]:
        raise ValueError("Deployment artifact hash mismatch.")

spec = importlib.util.spec_from_file_location(
    "deployment_recommender",
    PART3_DIR / "recommendation_system" / "recommender.py"
)
deployment_recommender = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment_recommender)
deployment_model = deployment_recommender.recommendation_model

app = FastAPI(
    title="Smart City Traffic Prediction",
    version="1.0"
)


class TrafficConditions(BaseModel):
    date_time: str
    temp: float = Field(ge=200, le=330, allow_inf_nan=False)
    rain_1h: float = Field(ge=0, le=9000, allow_inf_nan=False)
    snow_1h: float = Field(ge=0, allow_inf_nan=False)
    clouds_all: float = Field(ge=0, le=100, allow_inf_nan=False)
    weather_main: str
    is_holiday: int = Field(ge=0, le=1, strict=True)

class PredictionRequest(BaseModel):
    records: list[TrafficConditions] = Field(
        min_length=1,
        max_length=1000
    )

@app.get("/health")
def health():
    return {
        "status": "ready",
        "model_name": saved_manifest["model_name"],
        "model_version": saved_manifest["model_version"],
        "deployment_type": "local simulation"
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    inputs = pd.DataFrame([
        record.model_dump()
        for record in request.records
    ])

    try:
        features = (
            deployment_recommender.prepare_recommendation_inputs(
                inputs
            )
        )
    except (ValueError, TypeError, KeyError):
        logger.warning("Prediction request failed input validation.")
        raise HTTPException(
            status_code=422,
            detail=(
                "Check timestamps, weather categories and required "
                "traffic conditions."
            )
        ) from None

    try:
        predictions = deployment_model.predict(features)

        if not np.isfinite(predictions).all():
            raise ValueError("Non-finite model predictions.")

        records = [
            {
                "date_time": str(timestamp),
                "predicted_traffic_volume": float(prediction)
            }
            for timestamp, prediction in zip(
                pd.to_datetime(inputs["date_time"]),
                predictions
            )
        ]

        logger.info(
            "Completed prediction request for %s records.",
            len(records)
        )


        return {
            "model_version": saved_manifest["model_version"],
            "prediction_units": saved_manifest["prediction_units"],
            "predictions": records
        }

    except Exception:
        logger.error("Prediction request failed during model inference.")
        raise HTTPException(
            status_code=500,
            detail="Model inference failed."
        ) from None

def monitor_feature_means(candidates):
    features = (
        deployment_recommender.prepare_recommendation_inputs(
            candidates
        )
    )

    minimum_size = monitoring_config["minimum_batch_size"]
    if len(features) < minimum_size:
        raise ValueError(
            f"Monitoring requires at least {minimum_size} records."
        )

    threshold = monitoring_config["alert_threshold"]
    records = []

    for reference in monitoring_config["features"]:
        feature = reference["feature"]
        batch_mean = float(features[feature].mean())

        mean_shift = abs(
            batch_mean - reference["training_mean"]
        ) / reference["training_std"]

        records.append({
            "feature": feature,
            "training_mean": reference["training_mean"],
            "batch_mean": batch_mean,
            "standardised_mean_shift": mean_shift,
            "threshold": threshold,
            "status": "ALERT" if mean_shift > threshold else "PASS"
        })

    checks = pd.DataFrame(records)
    overall_status = (
        "ALERT"
        if checks["status"].eq("ALERT").any()
        else "PASS"
    )

    if overall_status == "ALERT":
        logger.warning(
            "Feature mean monitoring returned ALERT for %s records.",
            len(features)
        )
    else:
        logger.info(
            "Feature mean monitoring returned PASS for %s records.",
            len(features)
        )

    return checks, overall_status
