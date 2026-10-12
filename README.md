# Smart City Traffic Capstone

This is my work for the smart city traffic capstone project. I used SQL, Excel and Power BI to explore historical traffic, Python to build a reproducible analytics pipeline, and machine learning to predict traffic volume and recommend travel times.

The project covers **three connected parts** using the Metro Interstate Traffic Volume dataset for one corridor. The recommendation and deployment components are local simulations. They do not provide live traffic, alternative routes or journey times.

## Main results

| Part | Selected findings |
| --- | --- |
| Part 1 | **48,204 records**, **40,575 distinct recorded hours**, average traffic **3,259.82 vehicles per hour**, and temperature–traffic correlation **0.1303** |
| Part 2 | **48,187 cleaned records** after removing **17 exact duplicates**; the feature dataset has **30 columns** |
| Part 3 Random Forest | Held-out test MAE **250.84 vehicles per hour** and R-squared **0.9448** |
| Part 3 Neural Network | Held-out test MAE **256.94 vehicles per hour** and R-squared **0.9455** |

Part 1 statistics use the original records. Part 2 results use cleaned records. Part 3 model scores use a separate chronological held-out test period, so these figures describe different stages of the project.

## Project structure

```text
smart-city-traffic-capstone/
|-- part1_data_analytics/
|   |-- sql/
|   |-- statistics/
|   |-- powerbi/
|   |-- Metro_Interstate_Traffic_Volume.csv
|   |-- Part1DEliverablesExecutionOutput.docx
|   |-- Data Analytics Insights Report.docx
|   `-- insights_report.pdf
|-- part2_python/
|   |-- cli_app/traffic_app.py
|   |-- data/
|   |-- figures/
|   |-- pipeline.py
|   |-- feature_engineering.py
|   |-- visualizations.py
|   |-- traffic_pipeline_development.ipynb
|   |-- pipeline.log
|   |-- Part2DeliverablesExecutionOutput.docx
|   |-- Part2ShortReport.docx
|   `-- README.md
|-- part3_machine_learning/
|   |-- notebooks/
|   |-- models/
|   |-- figures/
|   |-- mlflow/
|   |-- deployment/
|   |-- recommendation_system/
|   |-- monitoring/
|   |-- results/
|   |-- reports/
|   |-- responsible_ai_report.pdf
|   |-- Part3DEliverablesExecutionOutput.docx
|   `-- README.md
|-- final_capstone_report.pdf
`-- README.md
```

Keep all three folders when downloading the project. Parts 2 and 3 use the raw CSV in the Part 1 folder. Part 3 also reuses cleaning functions from Part 2.

## Part 1 Data analytics

I have used SQLite to analyse yearly traffic and holiday temperatures, Excel to calculate descriptive statistics, and Power BI to explore daily, hourly, weather and temperature patterns. Probability calculations use congestion defined as traffic volume **above 5,500 vehicles**.

### Files and evidence

The following paths are relative to `part1_data_analytics/`.

| File or folder | Purpose |
| --- | --- |
| `Metro_Interstate_Traffic_Volume.csv` | Original dataset |
| `sql/traffic.db` | SQLite database containing the traffic table |
| `sql/01_verify_data.sql` | Record count and data preview |
| `sql/02_annual_traffic.sql` | Annual totals and changes for 2012–2017 |
| `sql/03_holiday_temperature.sql` | Holiday-labelled temperature observations |
| `sql/04_probability_analysis.sql` | Counts for probabilities and the odds ratio |
| `sql/05_temperature_outliers.sql` | Invalid temperature count |
| `statistics/Traffic_Statistics.xlsx` | Statistics, formulas and supporting data |
| `powerbi/MetroTrafficVolumeAnalysis.pbix` | Charts, KPI cards and slicers |

Read [the insights PDF](part1_data_analytics/insights_report.pdf) or [its Word version](part1_data_analytics/Data%20Analytics%20Insights%20Report.docx). Calculations and screenshots are in [the Part 1 execution output](part1_data_analytics/Part1DEliverablesExecutionOutput.docx).

### Findings and interpretation

- Mean traffic volume is **3,259.82** and median traffic volume is **3,380 vehicles per hour**. Population standard deviation is **1,986.84** and population variance is **3,947,533.43**. The range is **7,280 vehicles per hour**.
- The temperature–traffic correlation is **0.1303**, a weak positive association that does not establish causation.
- **14.73%** of records have traffic volume above **5,500**. The congestion odds ratio for Clear versus Clouds weather is **0.7354**.
- The recorded annual total fell **44.17%** from 2013 to 2014 and rose **20.12%** from 2016 to 2017. Unequal coverage and repeated timestamps limit comparisons of actual traffic growth.
- In 2017, the highest hourly average was at **16:00**, approximately **5,798 vehicles**; the lowest was at **03:00**, approximately **382**.
- Clouds had the highest weather-category average, **3,618.45**, and Squall the lowest, **2,061.75**. Their difference was **1,556.70 vehicles**. Small weather groups need careful interpretation.

### How to check Part 1

1. Open `sql/traffic.db` in DB Browser for SQLite and run the SQL files against the `traffic` table.
2. Open `statistics/Traffic_Statistics.xlsx` in Excel to inspect the formulas and results.
3. Open `powerbi/MetroTrafficVolumeAnalysis.pbix` in Power BI Desktop and check the charts, KPI cards and slicers.
4. Compare the outputs with the insights report and execution evidence.

All records were retained for Part 1. The hours card counts distinct timestamps, while averages and probabilities use records. Holiday queries describe midnight records labelled as holidays, not whole-day averages. There is no labelled New Year's Day observation for 2015; the 2017 observation with that label is dated **2 January**. The **10 zero-kelvin readings** were hidden in the second scatter plot but remain in the original-data temperature average and correlation.

## Part 2 Python analytics

The Python pipeline checks the schema, cleans categorical and numeric values, handles invalid readings, creates features, saves charts and supports command-line traffic queries.

### Files and evidence

The following paths are relative to `part2_python/`.

| File or folder | Purpose |
| --- | --- |
| `pipeline.py` | Loading, validation, cleaning and monthly median imputation |
| `feature_engineering.py` | Time, weather, scaled and traffic-category features |
| `visualizations.py` | Three saved Matplotlib charts |
| `cli_app/traffic_app.py` | Date queries, high-traffic queries and weekday/weekend comparison |
| `traffic_pipeline_development.ipynb` | Development workflow and saved outputs |
| `data/` | Cleaned data and engineered features |
| `figures/` | Saved traffic charts |
| `pipeline.log` | Sample execution and validation messages |

Read [the Part 2 README](part2_python/README.md), [short report](part2_python/Part2ShortReport.docx) and [execution output](part2_python/Part2DeliverablesExecutionOutput.docx).

### Findings and interpretation

Cleaning removed **17 exact duplicates**, replaced **10 invalid temperatures** and **one rainfall reading above 9,000 mm**, leaving **48,187 rows**. Replacements used valid monthly medians. The saved feature dataset contains **30 columns**.

Across cleaned records, average traffic was **3,533.29** on weekdays and **2,570.70** on weekends, a difference of **962.59 vehicles per hour**. The hourly average was lowest at **03:00**, **371.09**, and highest at **16:00**, **5,663.76**. These figures cover the full cleaned dataset, whereas the Part 1 hourly figures above describe 2017.

### How to check Part 2

1. Follow the environment setup and script order in the Part 2 README.
2. Review the notebook, scripts, saved data, charts and sample log.
3. Test the three CLI commands and invalid-input handling using the documented examples.
4. Compare outputs with the short report and execution evidence.

Some timestamps still have multiple weather records. Averages describe records rather than unique hours. Data gaps and small weather groups limit interpretation.

## Part 3 Machine learning and AI

The seven tasks cover supervised learning, clustering and association rules, a neural network with explainability, MLflow, travel-time recommendations, deployment and monitoring, and responsible and sustainable AI.

### Files and evidence

The following paths are relative to `part3_machine_learning/`.

| File or folder | Purpose |
| --- | --- |
| `notebooks/` | Seven task notebooks with saved results |
| `models/` | Saved models and preparation settings |
| `figures/` | Clustering, training and SHAP figures |
| `mlflow/` | Tracking database and run artifacts |
| `recommendation_system/` | Candidate-time ranking module and example inputs |
| `deployment/` | FastAPI application, model manifest and request examples |
| `monitoring/` | Feature mean monitoring module and training reference |
| `responsible_ai_report.pdf` | PDF of the responsible and sustainable AI report |
| `results/` | Model metrics, association rules, SHAP contributions, recommendations, group errors and validation checks |
| `reports/` | Final Part 3 report and responsible AI report in Word and Markdown |
| Task log files | Milestones, warnings and verification messages |

Read [the Part 3 README](part3_machine_learning/README.md), [final Part 3 report](part3_machine_learning/reports/part3_final_capstone_report.docx), [responsible and sustainable AI report](part3_machine_learning/reports/responsible_sustainable_ai_report.docx) and [execution output](part3_machine_learning/Part3DEliverablesExecutionOutput.docx).

### Findings and interpretation

The chronological held-out test period contained **4,944 records**. Random Forest achieved MAE **250.84** and R-squared **0.9448**; the neural network achieved MAE **256.94** and R-squared **0.9455**. Random Forest was reused for the recommendation engine and local API. SHAP explains the comparable Random Forest, not the neural network directly.

For five supplied candidate hours, **10:00** had the lowest predicted traffic volume. This ranks the supplied options and does not guarantee shorter journey times.

Monitoring requires at least **100 records**. A feature mean shift above **one training standard deviation** triggers ALERT. Synthetic batches demonstrated PASS and ALERT, and an undersized batch was rejected. The threshold requires operational calibration; PASS does not guarantee accurate predictions.

Both models had higher weekend MAE than weekday MAE. The test period had only **47 snow records**, **two smoke records** and **no squall records**, limiting severe-weather conclusions. Energy and emissions were not measured.

### How to check Part 3

1. Follow the Part 3 README for dependencies, working directories and notebook order.
2. Review the seven notebooks and saved result tables without repeating training.
3. Inspect the MLflow runs and the model-version comparison.
4. Test the recommendation module and API using the documented examples, including invalid inputs.
5. Review monitoring behaviour, group error analysis and supporting reports.

## Traffic categories and accident-risk proxy

The category rules differ by task and should not be treated as interchangeable.

| Stage | Rule and purpose |
| --- | --- |
| Part 1 | Fixed dashboard categories: Low below **4,500**, Medium from **4,500 to 5,500**, High above **5,500**. Probability analysis uses traffic above **5,500** as congestion. |
| Part 2 | Data-driven categories: Low at or below **1,192.5**, Medium above **1,192.5** and at or below **4,933**, High above **4,933**. These describe relative volume in the cleaned dataset. |
| Part 3 supervised learning | Training-derived quartiles define Low, Medium, High and Severe categories for the classification proxy. Thresholds are applied unchanged to validation and test data. |
| Part 3 association rules | Full cleaned-data quartiles define categories for exploratory historical pattern mining. |

No real accident dataset was supplied or sourced. The proxy marks High or Severe congestion together with severe or low-visibility weather as high risk. Weather inputs also help define the label, so strong classification scores measure reproduction of that rule, not actual accident prediction.

## Technologies used

- SQL and SQLite, including DB Browser for SQLite
- Microsoft Excel and Power BI
- Python, Jupyter Notebook, NumPy, Pandas and Matplotlib
- scikit-learn, Joblib and TensorFlow
- SHAP and MLflow
- FastAPI, Pydantic, Uvicorn and HTTPX
- Git and GitHub

## Running the project

Start with Part 1's analysis and raw data, then follow [the Part 2 run instructions](part2_python/README.md), followed by [the Part 3 run instructions](part3_machine_learning/README.md). Use the documented working directories. Rerunning workflows can replace generated data, models, figures and logs.

The scripts and reusable modules use Python logging. Part 2 writes console messages and `pipeline.log`; Part 3 retains task-specific logs. INFO records normal milestones, WARNING records recoverable issues, ERROR records failures, and DEBUG records troubleshooting details when enabled.

## Report scope and project limitations

The [combined final capstone report](final_capstone_report.pdf) brings together the methodology, findings and limitations from Parts 1, 2 and 3. It is available at the repository root.

The insights report covers Part 1, the short report covers Part 2, and the final Part 3 report covers all seven Part 3 tasks. The [responsible AI PDF](part3_machine_learning/responsible_ai_report.pdf) is available in the Part 3 folder. The individual reports and execution evidence provide supporting detail for each part.

This is a decision-support prototype using historical observations from one corridor. Data gaps, repeated timestamps, limited severe-weather coverage and the constructed accident-risk label restrict wider conclusions. Practical use would  require more representative data, validation across additional periods and roads, calibrated monitoring and human oversight.
