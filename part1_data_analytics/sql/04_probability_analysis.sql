/* 
* This SQL query verifies the probablity of congestion,
* clear weathre, congestion and clear weather.
*/
SELECT
    COUNT(*) AS "Total Records",

    SUM(CASE
        WHEN traffic_volume > 5500 THEN 1
        ELSE 0
    END) AS "Congestion Records",

    SUM(CASE
        WHEN weather_main = 'Clear' THEN 1
        ELSE 0
    END) AS "Clear Weather Records",

    SUM(CASE
        WHEN traffic_volume > 5500
         AND weather_main = 'Clear' THEN 1
        ELSE 0
    END) AS "Congestion And Clear Weather Records"

FROM traffic;


/*
* Conditional Probability task
*/
SELECT
    SUM(CASE WHEN traffic_volume > 5500
        THEN 1 ELSE 0 END) AS "Congestion Records",

    SUM(CASE WHEN traffic_volume > 5500
        AND weather_main = 'Clear'
        THEN 1 ELSE 0 END) AS "Clear And Congestion",

    SUM(CASE WHEN traffic_volume > 5500
        AND temp > 292
        THEN 1 ELSE 0 END) AS "High Temperature And Congestion",

    SUM(CASE WHEN temp > 292
        THEN 1 ELSE 0 END) AS "High Temperature Records"
FROM traffic;



/*
* Count the number of records for clear weather.
*/

SELECT COUNT(*) AS "Clear Weather Records"
FROM traffic
WHERE weather_main = 'Clear';


/*
* Odds ration
*/

SELECT
    weather_main AS "Weather",
    SUM(CASE WHEN traffic_volume > 5500
        THEN 1 ELSE 0 END) AS "Congestion",
    SUM(CASE WHEN traffic_volume <= 5500
        THEN 1 ELSE 0 END) AS "No Congestion"
FROM traffic
WHERE weather_main IN ('Clear', 'Clouds')
GROUP BY weather_main;