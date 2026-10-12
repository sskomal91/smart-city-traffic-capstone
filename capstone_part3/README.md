# Part 3 Machine Learning and AI

This part of my Smart City Traffic Capstone uses historical traffic and weather data to predict traffic volume, explore traffic patterns and recommend lower-traffic travel times. It also includes a neural network, model explanations, MLflow tracking, a local API and simulated monitoring.

No real accident dataset was supplied or sourced. I have used a documented accident-risk proxy based on congestion and severe or low-visibility weather. The classification results show how well the models reproduce this proxy, they do not measure the prediction of actual accidents.

## Project structure

| File or folder | Purpose |
| --- | --- |
| `notebooks/` | Seven task notebooks containing the development workflow and results |
| `models/` | Saved regression and classification models, clustering artifacts and preparation settings |
| `figures/` | Clustering, neural network training and SHAP figures |
| `mlflow/tracking.db` | Local MLflow experiment tracking database |
| `mlflow/artifacts/` | Model, preparation and evaluation artifacts copied into MLflow runs |
| `recommendation_system/recommender.py` | Reusable input preparation and travel-time recommendation functions |
| `recommendation_system/example_candidate_hours.csv` | Example candidate conditions for recommendations |
| `deployment/` | FastAPI application, deployment manifest, monitoring reference and example requests and responses |
| `results/` | Evaluation metrics, association rules, SHAP contributions, recommendations, validation checks and group error tables |
| `reports/part3_final_capstone_report.docx` | Final report covering methodology and findings across all seven tasks |
| `reports/part3_final_capstone_report.md` | Text version of the final report |
| `reports/responsible_sustainable_ai_report.docx` | Separate bias, fairness, governance and sustainability report |
| `reports/responsible_sustainable_ai_report.md` | Text version of the responsible and sustainable AI report |
| `Part3DEliverablesExecutionOutput.docx` | Execution screenshots and verification evidence |
| Task log files | Python logging output from the notebook workflows |

## Data and prerequisites

Keep the full repository when downloading this project. The Part 3 notebooks use the raw CSV at `part1_data_analytics/Metro_Interstate_Traffic_Volume.csv` and the cleaning functions in `capstone_part2/pipeline.py`. Downloading only the Part 3 folder is not enough to rerun the complete workflow.

Use a Python environment with NumPy, Pandas, Matplotlib, scikit-learn, Joblib, TensorFlow, SHAP, MLflow, FastAPI, Pydantic, Uvicorn, HTTPX and Jupyter Notebook. The saved scikit-learn models were created with scikit-learn 1.7.2, and the neural network used TensorFlow 2.21.0. Use compatible versions when loading these artifacts.

For an environment that needs these packages, the following command installs the main dependencies. This is a package list rather than a fully pinned environment specification.

```cmd
python -m pip install numpy pandas matplotlib scikit-learn==1.7.2 joblib tensorflow==2.21.0 shap mlflow fastapi pydantic uvicorn httpx notebook
```

Select the same Python environment as the notebook kernel and when starting the API. The supplied notebooks already contain saved outputs, so they can be reviewed without repeating model training.

## Run the notebooks

From the repository root, open Jupyter in the notebook folder:

```cmd
cd capstone_part3/notebooks
python -m notebook
```

Run each notebook from top to bottom in this order. The working directory must remain `capstone_part3/notebooks` because the notebooks derive the data and output locations from it.

| Order | Notebook | Main work |
| --- | --- | --- |
| 1 | `task1_supervised_learning.ipynb` | Chronological split, feature preparation, regression and proxy classification |
| 2 | `task2_unsupervised_learning.ipynb` | K-means clustering and association rules |
| 3 | `task3_deep_learning_explainability.ipynb` | Neural network comparison and SHAP explanations of Random Forest |
| 4 | `task4_advanced_ai.ipynb` | MLflow tracking of the saved model evaluations |
| 5 | `task5_traffic_recommendation_system.ipynb` | Candidate travel-time ranking and reusable recommendation module |
| 6 | `task6_mlops_deployment_simulation.ipynb` | Version manifest, API validation, saved application and monitoring |
| 7 | `task7_responsible_sustainable_ai.ipynb` | Held-out group errors, coverage analysis and responsible AI report |

Rerunning notebooks can replace saved models, results, figures and logs. Task 4 can add experiment runs. If models or preparation settings are regenerated, run the later tasks again so that recommendations, deployment hashes and group analysis match the regenerated artifacts.

Task 6 first checks the application with FastAPI TestClient. Its live HTTP check requires the API to be running in a separate terminal. Leave the API running when executing that section.

## Review MLflow tracking

From the repository root, enter the notebooks folder before starting the tracking interface:

```cmd
cd capstone_part3/notebooks
python -m mlflow ui --backend-store-uri sqlite:///../mlflow/tracking.db --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000` and select **Smart City Traffic Regression**. The saved runs record the Random Forest and neural network evaluations, parameters, version v1 and artifacts. They record existing evaluations rather than additional training. The database uses relative artifact locations, so use the working directory shown above.

## Test the recommendation engine

Task 5 demonstrates the complete example and validation checks. For a separate Python example, start Python from the repository root and run:

```python
import pandas as pd
from capstone_part3.recommendation_system.recommender import recommend_travel_window

candidates = pd.read_csv(
    "capstone_part3/recommendation_system/example_candidate_hours.csv"
)
ranked_candidates, recommendation = recommend_travel_window(candidates)
print(ranked_candidates)
print(recommendation)
```

The printed text is direct output for the user. The module uses Python logging for internal status messages. The engine ranks only the supplied candidate times. It uses temperature in kelvin, rain and snow in millimetres, cloud cover as a percentage and a holiday flag of 0 or 1.

## Start and test the API

In a separate terminal at the repository root, run:

```cmd
python -m uvicorn app:app --app-dir capstone_part3/deployment --host 127.0.0.1 --port 8000
```

Keep this terminal running while testing. Open `http://127.0.0.1:8000/docs` in a browser.

1. Expand **GET /health**, click **Try it out**, then **Execute**. A healthy application returns HTTP 200 and model version v1.
2. Expand **POST /predict**, click **Try it out**, and copy the JSON from `deployment/example_prediction_request.json` into the request box.
3. Click **Execute**. A valid request returns HTTP 200, the input timestamps and predicted traffic volume in vehicles per hour.
4. Change one record's `clouds_all` to 150 and execute again. HTTP 422 confirms that cloud cover above 100 is rejected.

Requests accept 1 to 1000 records. Each timestamp must be unique, on the hour and expressed as corridor local time without a timezone offset. Predictions preserve input order. Stop the server with Ctrl+C in its terminal.

Further API details are in `deployment/README.md`. The Task 6 notebook contains the saved application comparisons and live HTTP checks, and `results/deployment_live_http_checks.csv` records the live test results.

## Monitoring

`monitor_feature_means` in `deployment/app.py` is a Python function, not an HTTP endpoint. Task 6 demonstrates how to call it using a DataFrame with the prediction input columns.

Monitoring requires at least 100 records and compares temperature, rain, cloud cover and hour means with training statistics. An absolute shift above one training standard deviation triggers **ALERT**; otherwise the selected checks return **PASS**. A reference-like synthetic batch returned PASS and a temperature-shifted batch returned ALERT. A batch below the minimum size was rejected.

This threshold is for demonstration and requires calibration before operational use. Mean checks do not detect every distribution change. PASS does not guarantee accurate predictions, and accuracy monitoring needs observed traffic volumes.

## Main findings and limitations

Random Forest achieved test MAE of 250.84 vehicles per hour and R-squared of 0.9448. The neural network achieved MAE of 256.94 and R-squared of 0.9455. Random Forest was reused for recommendations and deployment. SHAP explains the comparable Random Forest rather than the neural network directly.

The test period contained 4944 records from April to September 2018. Weekend errors were higher than weekday errors for both models. Severe-weather coverage was limited: snow had 47 test records, smoke had two and squall had none. These results need further investigation and do not establish demographic fairness.

The classification proxy combines High or Severe congestion with severe or low-visibility weather. Its congestion thresholds were fitted on training data. Weather features also help define the proxy, so strong classification scores do not prove accident prediction ability.

This is a historical-data simulation for one corridor. It does not provide live traffic, alternative routes or journey times. Predictions and recommendations need human review before practical use. Energy and emissions were not measured, and no claim is made that one model is environmentally better than the other.

## Logging

The notebooks and reusable modules use Python's logging module. Task logs include `part3.log`, `part3_unsupervised_ml.log`, `part3_deep_learning.log`, `part3_smart_city_capstone_advanced_ai.log`, `part3_traffic_recommendation.log`, `part3_smart_city_traffic_mlops_deployment.log` and `part3_smart_city_traffic_responsible_ai.log`.

INFO records normal milestones. WARNING records noteworthy events such as dropped records or a monitoring alert.
