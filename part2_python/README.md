# Part 2 – Python: Building a Reproducible Traffic Analytics Pipeline

This part of my project uses Python to clean the traffic dataset, create features, save charts and build a command-line application.

## Project structure

| File or folder | Purpose |
| --- | --- |
| pipeline.py | Loads, checks and cleans the raw data |
| feature_engineering.py | Creates time, weather, scaled and traffic-category features |
| visualizations.py | Creates and saves three traffic charts |
| traffic_app.py | Provides three commands to query the processed data |
| data/traffic_cleaned.csv | Cleaned dataset |
| data/traffic_features.csv | Dataset with engineered features |
| figures/ | Saved charts |
| pipeline.log | Logs from script execution and application tests |
| traffic_pipeline_development.ipynb | Notebook used to develop the scripts and explore results |
| Part2DeliverablesExecutionOutput.docx | Supporting explanations and execution screenshots |
| README.md | Project structure, run commands and logging information |
| Part2ShortReport.docx | Short report summarising the findings |

## Requirements

Use Python 3 with NumPy, Pandas and Matplotlib.

Install the packages if needed:
```bat
python -m pip install numpy pandas matplotlib
```

The raw dataset is stored in the repository at:
```text
part1_data_analytics/Metro_Interstate_Traffic_Volume.csv
```

Keep both the part1_data_analytics and part2_python folders when downloading the project. The pipeline uses the raw CSV from the Part 1 folder.

## Task 1: Data Pipeline Construction (with mandatory logging)

From the repository folder, enter the Part 2 folder:
```bat
cd part2_python
```

Run the cleaning pipeline:
```bat
python pipeline.py
```

The pipeline checks the required columns before cleaning. It standardises category text, converts dates and numerical values, handles missing or invalid values and removes exact duplicate rows.

Invalid temperatures and rainfall readings are replaced using the median of valid readings from the same calendar month across all years. Rainfall above 9000 mm is treated as invalid, following the assignment requirement.

The raw dataset has 48204 rows and 9 columns. After cleaning, the dataset has 48187 rows and 9 columns. The output is saved to data/traffic_cleaned.csv.

## Task 2: Feature Engineering (NumPy and Pandas)

Run:
```bat
python feature_engineering.py
```

The script adds hour, day of week, a weekend indicator and sine and cosine encodings of the hour. It also adds weather-category encoding, rain and snow indicators, and scaled temperature and rainfall values between 0 and 1.

Traffic categories use the cleaned dataset's 25th and 75th percentiles:

- Low: traffic volume at or below 1192.5.
- Medium: traffic volume above 1192.5 and at or below 4933.
- High: traffic volume above 4933.

These categories describe relative traffic volume in this dataset. They do not directly measure road congestion. Values tied at a threshold can change the category sizes.

The output has 48187 rows and 30 columns and is saved to data/traffic_features.csv.

## Task 3: Visualise Traffic Patterns

Run:
```bat
python visualizations.py
```

The script saves these charts:

- figures/traffic_by_hour.png
- figures/weekday_weekend_traffic.png
- figures/traffic_by_weather.png

Average recorded traffic is lowest at 03:00, about 371.09 vehicles, and highest at 16:00, about 5663.76 vehicles.

Average traffic is 3533.29 on weekdays and 2570.70 on weekends.

Clouds has the highest weather-category average at 3617.99. Squall has the lowest at 2061.75, but has only 4 records. Small weather groups should be interpreted carefully. The charts show associations and do not prove that weather causes traffic changes.

The averages use all cleaned records. Some timestamps have more than one weather record, so these are averages over records rather than averages over unique hours.

## Task 4: Build a Mini Traffic Analytics Application

Query a specific date and time:
```bat
python cli_app/traffic_app.py query --datetime "2012-10-02 09:00:00"
```

Find records with traffic volume above a chosen threshold:
```bat
python cli_app/traffic_app.py high-traffic --threshold 7000
```

Compare weekday and weekend traffic:
```bat
python cli_app/traffic_app.py compare-days
```

The high-traffic command uses the threshold supplied by the user. This threshold is separate from the percentile-based traffic_category feature.

View the available commands:
```bat
python cli_app/traffic_app.py --help
```

Invalid dates, missing arguments and invalid threshold arguments produce a clear ERROR message without a raw traceback.

Successful commands return exit code 0. Handled errors return exit code 1. In Windows Command Prompt, check the code immediately after a command:
```bat
echo %ERRORLEVEL%
```

## Task 5: GitHub and Reproducibility

The repository contains separate commits for pipeline construction, feature engineering, visualisation and the mini-application.

To reproduce the processing and charts, run the scripts in this order:
```bat
python pipeline.py

python feature_engineering.py

python visualizations.py

python cli_app/traffic_app.py compare-days
```

The scripts resolve their data paths relative to their own location. Running the processing scripts again replaces the generated CSV files and charts.

## Logging configuration

Each Python module uses `logging.getLogger(__name__)`.

Logging is configured when a script runs as the main program. Messages are written to both the console and part2_python/pipeline.log. The log file uses UTF-8 and appends messages across runs.

Each log entry contains:

- Timestamp
- Log level
- Module name
- Message

The logging levels mean:

- DEBUG: Intermediate calculations, such as monthly medians, scaling ranges and percentile thresholds.
- INFO: Normal events, such as loading data, completing a step, saving a chart or invoking an application command.
- WARNING: Recoverable data issues, including changed values, removed duplicates and imputed readings.
- ERROR: A problem that prevents a script or command from completing.

Normal runs use INFO level. Enable DEBUG logging with:
```bat
python pipeline.py --debug

python feature_engineering.py --debug

python visualizations.py --debug

python cli_app/traffic_app.py --debug compare-days
```
