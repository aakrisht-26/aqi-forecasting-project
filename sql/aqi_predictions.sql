CREATE DATABASE aqi_db;
USE aqi_db;

CREATE TABLE aqi_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    actual_aqi FLOAT,
    predicted_aqi FLOAT
);

SELECT * FROM aqi_predictions LIMIT 10;

SELECT 
    AVG(ABS(actual_aqi - predicted_aqi)) AS MAE
FROM aqi_predictions;