# Smart City Traffic Part 3 Final Capstone Report

## Purpose and main findings

I developed an intelligent mobility solution using the Metro Interstate Traffic Volume dataset and the preparation workflow from Part 2. This report covers the methodology and findings across all seven Part 3 tasks. The solution predicts traffic volume, classifies a documented accident-risk proxy, explores traffic patterns, recommends travel times and demonstrates experiment tracking, deployment and monitoring.

Random Forest achieved a held-out traffic-volume MAE of 250.84 vehicles per hour and R-squared of 0.9448. The neural network achieved MAE of 256.94 and R-squared of 0.9455. I used the saved Random Forest for the recommendation engine and deployment simulation. Its lower test MAE supports this choice, although it does not establish that it will perform best in every future period. The results also show weaker performance in some conditions and limited severe-weather coverage.

The dataset represents one corridor and historical observations. Recommendations compare supplied travel times; they do not provide alternative routes, live traffic or journey times. No real accident dataset was supplied or sourced. The classification target is a constructed proxy and cannot validate actual accident likelihood.

## Data preparation and evaluation design

The original dataset contained 48204 records. The Part 2 preparation workflow corrected text formatting, checked types and missing values, and removed 17 exact duplicate rows, leaving 48187 records. Different weather records can share an hourly timestamp, so I retained these records and kept each timestamp entirely within one split.

For supervised modelling, I treated ten nonpositive temperature readings and one exceptionally large rain reading above 9000 as missing. Monthly medians fitted on the training data supplied these values. Preparation settings and fitted transformations were saved with the models so that later prediction used the same process.

I split unique timestamps chronologically into training, validation and test periods rather than randomly mixing future and past observations. The resulting row counts were 35873 for training, 7370 for validation and 4944 for testing. Training ended on 2 August 2017 at 23:00. Validation ran from 3 August 2017 at 00:00 to 14 April 2018 at 15:00. Testing ran from 14 April 2018 at 16:00 to 30 September 2018 at 23:00.

The common feature set included temperature, rain, snow, cloud cover, hour, day of week, month, weekend and holiday flags, cyclical sine and cosine encodings for hour and day of week, and rain, snow and low-visibility indicators. Weather categories were one-hot encoded. The 17 input features became 27 transformed features. Scaling and encoding were fitted on training data. Validation supported model comparison; the held-out test period provided the final evaluation.

## Task 1 Supervised Machine Learning Models

### Methodology

I compared Linear Regression with Random Forest for traffic-volume regression and Logistic Regression with Random Forest for classification. Both problems used the common engineered feature set. The Random Forest regressor used 100 trees, maximum depth 20, minimum leaf size 2 and random seed 42. Saved preparation settings and model files support repeatable inference.

The accident-risk proxy combined congestion and weather. Training traffic-volume quartiles defined Low, Medium, High and Severe congestion. High or Severe congestion together with severe or low-visibility weather produced the positive class. The thresholds were fitted on training data and then applied to validation and test data. This avoids fitting the label thresholds on the future test period.

### Regression findings

| Model | Validation MAE | Validation R-squared |
| --- | --- | --- |
| Linear Regression | 826.19 | 0.7158 |
| Random Forest | 317.57 | 0.9256 |

Random Forest substantially improved validation MAE and R-squared over the linear baseline. Its held-out test MAE was 250.84 and R-squared was 0.9448. The improvement suggests that nonlinear relationships between time, weather and traffic matter for this dataset. It does not show that these features cause traffic changes.

### Classification findings

| Model and period | Accuracy | Precision | Recall | F1 | ROC AUC |
| --- | --- | --- | --- | --- | --- |
| Logistic Regression validation | 0.9507 | 0.7645 | 0.9842 | 0.8605 | 0.9895 |
| Random Forest validation | 0.9769 | 0.9047 | 0.9508 | 0.9272 | 0.9932 |
| Random Forest test | 0.9875 | 0.9091 | 0.9664 | 0.9369 | 0.9982 |

Random Forest had the stronger validation F1 score and precision, while Logistic Regression had higher recall. The positive class contained 476 test records. Weather inputs also helped define the target, so these strong scores mainly demonstrate reproduction of the proxy rule. They are not evidence of accurate prediction of observed accidents or injuries.

## Task 2 Unsupervised Machine Learning

### K means clustering

I clustered historical traffic conditions using scaled hour sine and cosine, weather severity and traffic volume. I compared two to six clusters using silhouette scores with a reproducible sample of 3000 records and selected five clusters, which had the highest tested score of approximately 0.3704. This was an exploratory analysis of the full cleaned historical dataset, separate from supervised test evaluation.

| Cluster | Records | Mean traffic volume | Most common hour | Most common weather |
| --- | --- | --- | --- | --- |
| 0 | 8043 | 1079.69 | 04:00 | Mist |
| 1 | 12787 | 5080.17 | 14:00 | Clouds |
| 2 | 9624 | 3189.59 | 18:00 | Clouds |
| 3 | 9039 | 4924.87 | 09:00 | Rain |
| 4 | 8694 | 944.87 | 00:00 | Clear |

Clusters 0 and 4 represented lower-volume conditions, with different weather patterns. Cluster 1 represented busy conditions with low encoded weather severity. Cluster 3 combined high volume with more severe weather, while cluster 2 represented more moderate traffic. The most common hour describes each group and does not mean every record occurred at that hour. Cluster assignments describe similarity under the chosen features and severity encoding, rather than fixed operational traffic classes.

### Association rules

I discretised time of day, weekday type, weather and congestion. Congestion quartiles for this exploratory analysis came from the full cleaned dataset. I mined context combinations leading to congestion categories with minimum support 0.01, confidence 0.60 and lift above 1. Thirty-eight rules met these criteria.

The highest-lift rule was Weekend, Night and Mist leading to Low congestion. It applied to 558 antecedent records, of which 511 had Low congestion. Confidence was approximately 91.58 percent, support 1.06 percent and lift 3.663. Low congestion was therefore more frequent within this context than its overall frequency. The rule describes historical association and does not establish that mist reduces traffic.

## Task 3 Deep Learning with Explainability

### Neural network

I trained a neural network with hidden layers of 64 and 32 units using ReLU activation and a linear output. Inputs used the same fitted feature preparation as the Random Forest, and the target was standardised using training statistics. Training used Adam with learning rate 0.001, batch size 256 and a maximum of 100 epochs. Early stopping monitored validation loss with patience 10 and restored the best weights. Training finished after 37 epochs, with the best epoch at 27.

| Model | Validation MAE | Validation R-squared | Test MAE | Test R-squared |
| --- | --- | --- | --- | --- |
| Random Forest | 317.57 | 0.9256 | 250.84 | 0.9448 |
| Neural Network | 316.44 | 0.9307 | 256.94 | 0.9455 |

The neural network slightly improved validation results and held-out R-squared, while Random Forest had lower held-out MAE. The small differences do not support an unconditional claim that one model is superior. Both were retained for comparison and later group error analysis.

### Explainability

I used Tree SHAP on the comparable Random Forest trained for the same traffic-volume problem. This provides an explanation of the Random Forest, not a direct explanation of the neural network. I selected 200 held-out records with a fixed random seed and checked that the base value plus contributions reconstructed predictions.

Hour cosine had the largest mean absolute contribution, approximately 1438.38 vehicles per hour, followed by hour at 447.40, hour sine at 204.08 and day of week at 180.97. These findings show that time patterns strongly influenced this model. Related time features can share explanatory importance, and SHAP contributions are not causal effects.

For an example at 15:00 on 18 April 2018, actual traffic volume was 5835 and the prediction was 5801.59. The SHAP base value was 3244.99 and contributions summed to 2556.60. The saved global chart, local waterfall and contribution tables show both overall and individual prediction explanations.

## Task 4 Apply an Advanced AI Technique

I selected MLflow because experiment tracking connects model comparison with the later deployment simulation. I recorded the existing Random Forest and neural network evaluations in the Smart City Traffic Regression experiment, using a local SQLite tracking database and artifact folders.

The two completed runs recorded parameters, validation and test MAE and R-squared, model version v1, and relevant model, preparation and evaluation artifacts. The neural network run also retained training evidence. I verified the recorded metrics and artifact inventory against the saved results. These runs document existing evaluations; they do not represent additional model training.

MLflow adds traceability by keeping model settings, results and artifacts together. It supports review and reproduction of the selected model. This implementation uses local tracking and copied artifacts rather than a managed model registry or an automated promotion process. Artifact copies increase storage, and relative artifact locations require the documented working directory when using the local tracking interface.

## Task 5 Build a Traffic Recommendation System

I built a reusable recommendation module that validates candidate travel records, applies the saved preparation workflow and predicts traffic volume with the saved Random Forest. Inputs include date and time, weather measurements, weather category and holiday status. Calendar and cyclical features are derived from the supplied timestamp.

The engine ranks candidate hours by predicted traffic volume, using time to resolve ties, and generates a plain-language recommendation. It preserves the relationship between each candidate and its prediction. Validation checks covered shuffled input order, duplicate timestamps, unknown weather and invalid cloud cover.

For five supplied clear-weather weekday candidates on 7 May 2018, the predictions were:

| Candidate hour | Predicted vehicles per hour |
| --- | --- |
| 06:00 | 5692.33 |
| 07:00 | 5475.10 |
| 08:00 | 5871.44 |
| 09:00 | 4956.37 |
| 10:00 | 4204.31 |

The engine recommended 10:00 among these supplied choices. Its predicted volume was approximately 1667 vehicles per hour below the highest-volume candidate at 08:00. This example demonstrates timing advice for one corridor. It does not guarantee a shorter journey or account for current incidents, and the candidate weather values must come from the caller.

## Task 6 MLOps and Deployment Simulation

### Versioning and deployment

The deployment manifest records the selected model version, artifact locations, SHA-256 hashes and evaluation metrics. The MLflow comparison retains the two evaluated model families and their v1 results. No second trained release or automatic retraining process was created.

I implemented a FastAPI application with GET /health and POST /predict. The prediction endpoint validates records, applies the reusable preparation function and returns model version, units, timestamps and predicted traffic volumes in input order. Model and preparation hashes are verified when the saved application is loaded.

Tests checked the saved application against notebook inference, using exact comparisons for metadata and timestamps and a tight numerical tolerance for predictions. Both health and valid prediction requests returned HTTP 200. Invalid inputs were rejected with HTTP 422. Live local HTTP tests and browser tests confirmed the running application, including rejection of cloud cover above 100.

### Monitoring and alerting

The monitoring function compares batch means for temperature, rain, cloud cover and hour with training scaler statistics. A batch requires at least 100 records. An absolute mean shift greater than one training standard deviation triggers ALERT; otherwise the selected checks return PASS. This is a Python function in the saved application rather than an HTTP endpoint.

A synthetic batch of 240 reference-like records returned PASS. A temperature-shifted batch of 240 records, with temperature increased by two training standard deviations, returned ALERT. A five-record batch was rejected with the expected minimum-size error. These checks demonstrate monitoring behaviour, rather than prove that the threshold is suitable for operations.

Mean checks can miss changes in variance, tails or other relationships. PASS does not guarantee accurate predictions. Monitoring prediction accuracy requires observed traffic volumes. Operational use would require threshold calibration, investigation of alerts and validation before replacing models.

## Task 7 Responsible and Sustainable AI

### Coverage and uneven errors

I analysed the saved 4944 held-out predictions without retraining either model. I checked timestamp and actual-volume alignment before attaching weather labels. This avoided a timestamp-only join that could duplicate records sharing an hour.

Random Forest MAE ranged from 97.14 at night to 330.02 in the morning. Neural network MAE ranged from 116.40 at night to 324.96 in the morning. Different traffic levels affect the interpretation of absolute error, so these differences alone do not establish unfairness.

| Model | Weekday MAE | Weekend MAE |
| --- | --- | --- |
| Random Forest | 222.63 | 320.35 |
| Neural Network | 234.90 | 311.25 |

Both models had higher weekend MAE despite lower average weekend volume. This warrants investigation, but the analysis does not identify a cause. Weekdays contained 3517 records and weekends 1427.

Snow had the highest observed weather-group MAE: 1125.13 for Random Forest and 1164.69 for the neural network. Both overpredicted by approximately 1053 vehicles per hour on average, but only 47 snow records supported this result. Fog had 112 records and MAE of 444.55 and 435.23 respectively. Smoke had only two records and squall had none in the test period.

Groups below 100 records were flagged as limited evidence. This is a reporting rule, not a statistical guarantee. The April to September test period does not cover a complete annual weather cycle. Repeated hourly timestamps also mean that records are not all independent. The single-corridor dataset has no demographic attributes, so these comparisons cannot establish demographic fairness.

### Proxy risks and governance

The accident-risk proxy is based on selected congestion and weather conditions rather than observed accidents. Strong classification results must not be presented as validated accident prediction. It should not be used to declare journeys safe, impose penalties or guide emergency decisions.

Recommendations should support human judgement alongside current road conditions, incidents and official information. Model versions, preparation settings, metrics and hashes should be retained. Proposed replacement models require validation and group error review. Monitoring alerts should prompt investigation of data quality, seasonal changes and performance rather than automatic retraining. More representative severe-weather data and evaluation across additional corridors and periods are needed before wider use.

### Sustainability

I reused saved models for recommendation and deployment. Early stopping limited neural network training to 37 epochs rather than the maximum 100. Energy and emissions were not measured, so resource savings cannot be quantified and neither model is claimed to be greener.

MLflow copies improve traceability while increasing storage. Retention policies should preserve required evidence and archive obsolete versions. Future comparisons should measure training time, inference latency, memory use and, where feasible, energy consumption. The separate responsible and sustainable AI report provides the bias, fairness, governance and sustainability discussion with supporting group result files.

## Conclusion and supporting evidence

The project connects data preparation, supervised and unsupervised analysis, deep learning, explainability, tracking, recommendation and deployment in a local historical-data simulation. Random Forest provided the lower held-out MAE and was reused for timing recommendations and the API. Monitoring and input validation demonstrated expected behaviour, while group analysis identified weaker conditions and gaps in test coverage.

The next operational steps are to obtain representative observations across additional periods and corridors, evaluate severe-weather performance, calibrate monitoring thresholds and review predictions with human oversight. Actual accident prediction would require an appropriate accident dataset and a separately validated target.

The seven notebooks in notebooks contain the task workflows. Saved models and preparation artifacts are in models; MLflow tracking is in mlflow; the recommendation module is in recommendation_system; and the application, manifest and examples are in deployment. Results contains model comparisons, SHAP contributions, validation checks, recommendation outputs and group error tables. The execution output document records screenshots and verification evidence, while the separate responsible and sustainable AI report is in reports. Python logging records task milestones and noteworthy events.
