/* Compare the total yearly traffic volume for
* year 2012-2017. Use group by clause and between 
* operator for range of years
*/
SELECT
    strftime('%Y', date_time) AS year,
    SUM(traffic_volume) AS total_traffic_volume
FROM traffic
WHERE strftime('%Y', date_time) BETWEEN '2012' AND '2017'
GROUP BY strftime('%Y', date_time)
ORDER BY year;


/*
* i. Identify years with increases or decreases. 
* ii.Calculate the change between years where appropriate. 
*/
WITH yearly_totals AS (
    SELECT
        strftime('%Y', date_time) AS year,
        strftime('%Y', date_time, '-1 year') AS previous_year,
        SUM(traffic_volume) AS total_traffic_volume
    FROM traffic
    WHERE strftime('%Y', date_time) BETWEEN '2012' AND '2017'
    GROUP BY strftime('%Y', date_time),
             strftime('%Y', date_time, '-1 year')
)
SELECT
    current.year AS "Year",
    current.total_traffic_volume AS "Total Traffic Volume",
    current.total_traffic_volume
        - previous.total_traffic_volume AS "Traffic Volume Change",
    ROUND(
        100.0 * (
            current.total_traffic_volume
            - previous.total_traffic_volume
        ) / previous.total_traffic_volume,
        2
    ) AS "Traffic Volume Change %"
FROM yearly_totals AS current
LEFT JOIN yearly_totals AS previous
    ON current.previous_year = previous.year
ORDER BY current.year;