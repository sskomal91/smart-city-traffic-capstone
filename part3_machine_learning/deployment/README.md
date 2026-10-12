# Smart City Traffic Deployment Simulation

The application serves Random Forest regression v1 using the saved model
and preparation configuration. Artifact hashes are checked on import.

## Start the API

From the repository root, using the project Python environment:

```cmd
python -m uvicorn app:app --app-dir part3_machine_learning/deployment --host 127.0.0.1 --port 8000
```

Keep the terminal running. Stop the server with Ctrl+C.

## Endpoints

- GET /health returns readiness and model version.
- POST /predict accepts a JSON object containing a records list.
- Interactive API documentation: http://127.0.0.1:8000/docs

Use example_prediction_request.json as the example request body.
Each record requires date_time, temp, rain_1h, snow_1h, clouds_all,
weather_main and is_holiday.

Temperature is in kelvin, rain and snow are in millimetres, cloud cover
is a percentage, and is_holiday is an integer flag of 0 or 1.
Timestamps must be unique, on the hour and expressed as corridor local
time without a timezone offset. Requests accept 1 to 1000 records.

Predictions retain input order and report traffic volume in vehicles
per hour. Invalid inputs return HTTP 422.

## Monitoring

monitor_feature_means is a Python function in app.py. It is not an HTTP
endpoint. It accepts a candidate DataFrame with the same input columns.

Monitoring compares batch means for temperature, rain, cloud cover and
hour with statistics from the training preprocessing scaler. Batches
require at least 100 records.

An absolute mean shift above one training standard deviation triggers
ALERT. Otherwise, the selected checks return PASS. The threshold is for
demonstration and requires operational calibration.

Synthetic examples verified PASS and ALERT behavior. Mean checks do
not detect every distribution change or measure prediction accuracy.
Accuracy monitoring requires observed traffic volumes.

## Evidence

deployment_manifest.json records model version, hashes and evaluation metrics.
../monitoring/monitoring_reference.json records training statistics and monitoring settings.
Example API requests and responses are stored in this folder.
Verification tables are stored in the Part 3 results folder.

## Scope

This is a local simulation using a model trained on historical traffic
records. It does not provide live traffic information or journey times.
MLflow tracking from Task 4 retains the existing model evaluations;
this task does not retrain or register a new model.
