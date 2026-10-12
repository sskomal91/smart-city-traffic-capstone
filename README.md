# Smart City Traffic Capstone

This is my work for the smart city traffic capstone project. I used SQL, Excel and Power BI to explore the Metro Interstate Traffic Volume data, Python to build a reproducible analytics pipeline, and machine learning to predict traffic volume and recommend travel times.

The repository contains all three parts. The dataset describes historical traffic on one corridor. The recommendation and deployment components are local simulations and do not provide live traffic, alternative routes or journey times.

## Project structure

| Folder | Work included | Main documentation |
| --- | --- | --- |
| `part1_data_analytics/` | SQL analysis, Excel statistics and Power BI visuals | Execution output document and insights report |
| `capstone_part2/` | Data cleaning, feature engineering, charts and command-line queries | [Part 2 README](capstone_part2/README.md) and short report |
| `capstone_part3/` | Supervised and unsupervised learning, neural network, SHAP, MLflow, recommendations, API and monitoring | [Part 3 README](capstone_part3/README.md), final report and responsible AI report |

Keep all three folders when downloading the project. Parts 2 and 3 use the raw CSV in the Part 1 folder, and Part 3 also reuses the Part 2 cleaning functions.

## Part 2 Python analytics

The Python pipeline checks and cleans the data, creates time and weather features, saves charts and provides a command-line application for querying traffic conditions. The development notebook, scripts, saved data and execution logs are in `capstone_part2`.

Follow the [Part 2 run instructions](capstone_part2/README.md). The findings are in [the Part 2 short report](capstone_part2/Part2ShortReport.docx), with screenshots and verification in [the execution output](capstone_part2/Part2DeliverablesExecutionOutput.docx).

## Part 3 Machine learning and AI

The seven notebooks cover regression and classification, K-means and association rules, a neural network and SHAP, MLflow experiment tracking, travel-time recommendations, FastAPI deployment and monitoring, and responsible and sustainable AI. Saved models, results and supporting artifacts are included.

Follow the [Part 3 run instructions](capstone_part3/README.md) for the notebook order, dependencies, tracking interface and API tests. Read [the final Part 3 report](capstone_part3/reports/part3_final_capstone_report.docx) for methodology and findings across all seven tasks. The [responsible and sustainable AI report](capstone_part3/reports/responsible_sustainable_ai_report.docx) discusses bias, fairness, coverage, governance and resource trade-offs. [The Part 3 execution output](capstone_part3/Part3DEliverablesExecutionOutput.docx) contains supporting screenshots and checks.

No real accident dataset was supplied or sourced. Part 3 uses an accident-risk proxy combining congestion and severe or low-visibility weather. Classification scores measure reproduction of that proxy, not prediction of observed accidents. Traffic recommendations compare supplied candidate hours on the same corridor and need human review before practical use.

## Part 1 files

I have kept the Part 1 files in `part1_data_analytics`. The table below shows what each file is for.

| File or folder | What it contains |
| --- | --- |
| `Metro_Interstate_Traffic_Volume.csv` | Original data  |
| `sql/traffic.db` | SQLite database with the `traffic` table |
| `sql/01_verify_data.sql` | Record count and data preview |
| `sql/02_annual_traffic.sql` | Yearly totals and changes for 2012 to 2017 |
| `sql/03_holiday_temperature.sql` | Records labelled New Years Day and Labor Day for 2015 to 2017 |
| `sql/04_probability_analysis.sql` | Counts used for statisticscalculations |
| `sql/05_temperature_outliers.sql` | Count of invalid temperature readings |
| `statistics/Traffic_Statistics.xlsx` | Traffic statistics, formulas and traffic volume data |
| `powerbi/MetroTrafficVolumeAnalysis.pbix` | Charts, KPI cards and slicers |
| `Part1DEliverablesExecutionOutput.docx` | Task results, calculations, explanations and screenshots |
| `Data Analytics Insights Report.docx` | Insights report inb .docx |
| `insights_report.pdf` | Insights report |

## How to check Part 1

1. Open `sql/traffic.db` in DB Browser for SQLite. Open each SQL file in the Execute SQL tab and run the statements. The queries use the table name `traffic`.
2. Open `statistics/Traffic_Statistics.xlsx` in Excel to view the statistics and formulas. The workbook uses population standard deviation and population variance.
3. Open `powerbi/MetroTrafficVolumeAnalysis.pbix` in Power BI Desktop. 
4. The output document has my calculations, explnations and screenshots. The `insights_report.pdf` is a short report about what I found and how it could help the city team.

The probability SQL file gives the counts. I used these counts to calculate the probabilites in the output documnt. 






## Part 1 findings

- There are 48204 records, but only 40575 different recorded hours. Some hours appear more than once.
- Average traffic volume is 3259.82. Median traffic volume is 3380.
- The temperature and traffic correlation is 0.1303. This is a weak positive link, so temperature alone does not explain traffic very well.
- For this project I counted traffic above 5500 as congestion. With this rule, 14.73% of records have congestion.
- In 2017, the highest hourly average is at 4 pm, about 5798. The lowest is at 3 am, about 382.
- Clouds has the highest average traffic at 3618.45. Squall has the lowest at 2061.75. The difference between the displayed averages is 1556.70.
- I also tested all three filters togther. Hours 8 to 11, Clear weather and Low traffic gave 907 dif    ferent hours, average traffic of 3491.64 and average temperatur of 6.28 degrees Celsius.

## Part 1 limitations

- I kept all the original records. The averages, yearly totals and probabilities use these records. Only the hours card counts each recorded hour once.
- Some years have missing data. The 2012 data starts in October, and the 2015 data in the daily chart starts in June. So a yearly increase or decrease may partly come from the amount of data availble.
- My holiday query only shows the records with holiday labels. These are midnight readings, not averages for the whole day. There is no labelled New Years Day record for 2015. The 2017 record with t hat label is dated 2 January.
- I found 10 temperature readings of 0 Kelvin, which becomes -273.15 degrees Celsius. I hid these in the second scatter plot. They are still included in the temperature card and correlation.
- I used the congestion rule given for this project, which is traffic volume above 5500.
- These calculations show a link between weather and congestion, but do not prove that weather causes changes in traffic.
- I tested the three slicers on the KPI page. The charts on the other pages show the other tasks seperately, with their saved date filters.

## Part 1 dataset

I haveused the Metro Interstate Traffic Volume dataset given The original CSV has 9 columns. In Power BI I have added Hur, Temperature in Celsius, Traffic Category and Date.

## Part 2 files

The following paths are inside `capstone_part2`.

| File or folder | What it contains |
| --- | --- |
| `pipeline.py` | Data loading, validation and cleaning functions |
| `feature_engineering.py` | Time, weather, scaled and traffic-category features |
| `visualizations.py` | Code for creating the traffic charts |
| `traffic_app.py` | Command-line traffic queries |
| `traffic_pipeline_development.ipynb` | Development notebook and saved outputs |
| `data/` | Cleaned data and engineered features |
| `charts/` | Saved traffic charts |
| `pipeline.log` | Execution and validation messages |
| `Part2DeliverablesExecutionOutput.docx` | Task explanations and execution screenshots |
| `Part2ShortReport.docx` | Methodology, findings and limitations |
| `README.md` | Dependencies, commands and logging information |

## How to check Part 2

1. Read `capstone_part2/README.md` for the environment and run commands.
2. Review the development notebook and the cleaning, feature engineering and visualisation scripts.
3. Check the saved data in `data/`, the figures in `charts/` and the execution messages in `pipeline.log`.
4. Use the documented commands to test `traffic_app.py`.
5. Read the short report and execution output document for the findings and supporting evidence.

## Part 2 findings and limitations

Cleaning removed 17 exact duplicate records, leaving 48187 rows. Different records can still share an hourly timestamp. The pipeline creates repeatable features and charts, while the command-line application lets a user query the prepared data. The results describe historical observations from one corridor, with gaps in coverage, and do not establish that weather causes traffic changes.

## Part 3 files

The following paths are inside `capstone_part3`.

| File or folder | What it contains |
| --- | --- |
| `notebooks/task1_supervised_learning.ipynb` | Regression and proxy classification comparisons |
| `notebooks/task2_unsupervised_learning.ipynb` | K-means clusters and association rules |
| `notebooks/task3_deep_learning_explainability.ipynb` | Neural network training, model comparison and SHAP |
| `notebooks/task4_advanced_ai.ipynb` | MLflow experiment tracking |
| `notebooks/task5_traffic_recommendation_system.ipynb` | Travel-time recommendations and validation |
| `notebooks/task6_mlops_deployment_simulation.ipynb` | Versioning, API tests and monitoring simulation |
| `notebooks/task7_responsible_sustainable_ai.ipynb` | Group errors, coverage, bias and sustainability analysis |
| `models/` | Saved models and preparation settings |
| `figures/` | Clustering, training and explainability figures |
| `mlflow/` | Tracking database and saved run artifacts |
| `recommendation_system/` | Reusable recommendation module and example candidate hours |
| `deployment/` | API application, manifest, monitoring settings and request examples |
| `results/` | Evaluation tables, recommendations and verification checks |
| `reports/part3_final_capstone_report.docx` | Final methodology and findings across all seven tasks |
| `reports/responsible_sustainable_ai_report.docx` | Separate bias, fairness, governance and sustainability report |
| `Part3DEliverablesExecutionOutput.docx` | Execution screenshots and verification evidence |
| Task log files | Logged milestones and noteworthy events |
| `README.md` | Dependencies, notebook order, MLflow instructions and API tests |

## How to check Part 3

1. Read `capstone_part3/README.md` for dependencies and the correct working directories.
2. Review the seven notebooks in task order. Saved outputs can be inspected without repeating training.
3. Check the model comparisons, association rules, SHAP contributions and group errors in `results/`.
4. Follow the README to view the saved MLflow runs and test the recommendation engine.
5. Start the API from the repository root using the documented Uvicorn command. Use its interactive documentation to check health, valid predictions and rejection of invalid inputs.
6. Review the synthetic PASS and ALERT monitoring checks in Task 6.
7. Read the final report, responsible AI report and execution output document.

## Part 3 findings and limitations

Random Forest achieved held-out test MAE of 250.84 vehicles per hour and R-squared of 0.9448. The neural network achieved MAE of 256.94 and R-squared of 0.9455. The saved Random Forest was used for the recommendation engine and API. In the five-hour example, 10:00 had the lowest predicted traffic volume among the supplied candidates.

Both models had higher weekend MAE than weekday MAE. Snow had only 47 test records, smoke had two and squall had none. These coverage gaps limit the conclusions that can be drawn about severe weather. The accident-risk target is a proxy rather than observed accidents, SHAP explains the Random Forest, and monitoring checks selected feature means rather than every kind of drift. Energy and emissions were not measured. Human review and further evaluation are needed before operational use.
