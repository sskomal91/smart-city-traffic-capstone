# Smart City Traffic Capstone

This is my work for the smart city traffic capstone project. I used SQL, Excel and Power BI to check the Metro Interstate Traffic Volume data. I wanted to undertsand when traffic is busy and whether temperature and weather have any link with traffic.

So far I have added Part 1. 
## Files I have added

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

## How to check my work

1. Open `sql/traffic.db` in DB Browser for SQLite. Open each SQL file in the Execute SQL tab and run the statements. The queries use the table name `traffic`.
2. Open `statistics/Traffic_Statistics.xlsx` in Excel to view the statistics and formulas. The workbook uses population standard deviation and population variance.
3. Open `powerbi/MetroTrafficVolumeAnalysis.pbix` in Power BI Desktop. 
4. The output document has my calculations, explnations and screenshots. The `insights_report.pdf` is a short report about what I found and how it could help the city team.

The probability SQL file gives the counts. I used these counts to calculate the probabilites in the output documnt. 






## What I found

- There are 48204 records, but only 40575 different recorded hours. Some hours appear more than once.
- Average traffic volume is 3259.82. Median traffic volume is 3380.
- The temperature and traffic correlation is 0.1303. This is a weak positive link, so temperature alone does not explain traffic very well.
- For this project I counted traffic above 5500 as congestion. With this rule, 14.73% of records have congestion.
- In 2017, the highest hourly average is at 4 pm, about 5798. The lowest is at 3 am, about 382.
- Clouds has the highest average traffic at 3618.45. Squall has the lowest at 2061.75. The difference between the displayed averages is 1556.70.
- I also tested all three filters togther. Hours 8 to 11, Clear weather and Low traffic gave 907 dif    ferent hours, average traffic of 3491.64 and average temperatur of 6.28 degrees Celsius.

## Things to keep in mind

- I kept all the original records. The averages, yearly totals and probabilities use these records. Only the hours card counts each recorded hour once.
- Some years have missing data. The 2012 data starts in October, and the 2015 data in the daily chart starts in June. So a yearly increase or decrease may partly come from the amount of data availble.
- My holiday query only shows the records with holiday labels. These are midnight readings, not averages for the whole day. There is no labelled New Years Day record for 2015. The 2017 record with t hat label is dated 2 January.
- I found 10 temperature readings of 0 Kelvin, which becomes -273.15 degrees Celsius. I hid these in the second scatter plot. They are still included in the temperature card and correlation.
- I used the congestion rule given for this project, which is traffic volume above 5500.
- These calculations show a link between weather and congestion, but do not prove that weather causes changes in traffic.
- I tested the three slicers on the KPI page. The charts on the other pages show the other tasks seperately, with their saved date filters.

## Dataset

I used the Metro Interstate Traffic Volume dataset given The original CSV has 9 columns. In Power BI I have added Hur, Temperature in Celsius, Traffic Category and Date.
