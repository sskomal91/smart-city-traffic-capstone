"""Compare input feature means with the saved training reference."""
import json
import logging
from pathlib import Path
import pandas as pd
logger = logging.getLogger(__name__)
monitoring_config = json.loads((Path(__file__).parent / "monitoring_reference.json").read_text(encoding="utf-8"))

def monitor_feature_means(candidates, prepare_inputs):
    features = (
        prepare_inputs(
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
