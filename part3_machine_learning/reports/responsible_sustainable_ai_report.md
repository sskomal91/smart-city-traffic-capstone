# Responsible and Sustainable AI Report

## Scope

This analyss uses 4944 held-out test records from 14 April to 30 September 2018. It compares saved Random Forest and neural network regression predictions without retraining or tuning on the test set.

The dataset contains no demographic attributes.

## Time group performance

Random Forest MAE ranged from 97.14 veicles at night to 330.02 in the morning. Neural Network MAE ranged from 116.40 at night to 324.96 in the morning.

Traffic volume differs between time groups, so absolute error differences require context and do not alone establish unfairness.

## Weekday and weekend performance

Random Forest MAE was 222.63 on weekdays and 320.35 on wekends. Neural Network MAE was 234.90 on weekdays and 311.25 on weekends.

There were 3517 weekday and 1427 weekend records. Average actual volume was 3604.24 on weekdays and 2606.78 on weekends. Higher weekend error despite lower average volume warrants investigation.

## Weather performance and coverage

Snow MAE was 1125.13 for Random Forest and 1164.69 for the neural network. Both models overpredicted snow traffic by approximately 1053 vehicles on average. Only 47 test records supported these estimates.

Fog had 112 records, with MAE 444.55 for Random Foest and 435.23 for the neural network. Smoke had two records and squall had none.

The test period does not cover a complete annual weather cycle. Multiple records can share an hourly timestamp, so record counts do not represent independent observations.

## Classification proxy

HighRisk was constructed from traffic volume thresholds and selected weather conditions. It is not an observed accident or injury outcome. Weather inputs also help define the label, so strong classification scores demonstrate reproduction of the proxy rule rather than validated accident prediction ability.

The proxy must not be used to declare journeys safe, issue penalties or make emergency decisions.

## Human oversight and governance

Recommendations should support human judgement alongside current incidents, road conditions and oficial information.

Retain model versions, preparation settings, evaluation results and artifact hashes. Validate replacement models and review group errors before deployment.

Investigate monitoring ALERT results for data quality, seasonal changes and performance changes. Do not automatically retrain. PASS does not guarantee accurate predictions.

Colect more representative severe-weather data and assess performance across additional periods and corridors before wider use.

## Sustainability

Saved models were reused rather than retrained for recommendation and deployment. Early stopping completed neural network training after 37 epochs instead of the maximum 100.

Energy and emissions were not measured. Environmental savings cannot be quantified, and no claim is made that one model is greener.

MLflow artifact copies support reproducibility but increase storage. Define retention rules and archive obsolete versions while preserving required evidence.

Fuure comparisons should measure training time, inference latency, memory use and, where feasible, energy consumption.

## Supporting results

responsible_ai_time_group_errors.csv

responsible_ai_day_group_errors.csv

responsible_ai_weather_group_errors.csv

responsible_ai_weather_coverage.csv

These files are stored in the Part 3 results folder.
