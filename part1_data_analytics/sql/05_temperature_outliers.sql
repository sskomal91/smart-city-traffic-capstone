/*
* Find outliers
*/

SELECT COUNT(*) AS "Invalid Temperature Records"
FROM traffic
WHERE temp = 0;