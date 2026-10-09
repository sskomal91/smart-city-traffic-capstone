/*
* This query analyzes temperature 
* around holidays.
*/

SELECT DISTINCT
    strftime('%Y', date_time) AS "Year",
    holiday AS "Holiday",
    date_time AS "Date and Time",
    ROUND(temp - 273.15, 2) AS "Temperature °C",
    traffic_volume AS "Traffic Volume"
FROM traffic
WHERE holiday IN ('New Years Day', 'Labor Day')
  AND strftime('%Y', date_time) BETWEEN '2015' AND '2017'
ORDER BY holiday, date_time;