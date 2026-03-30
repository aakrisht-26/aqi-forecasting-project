import pandas as pd
import numpy as np
import mysql.connector
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =========================
# CONFIGURATION
# =========================
CITY = "Delhi"
FORECAST_DAYS = 30
MODEL_NAME = "ARIMA(5,0,0)"

DATA_PATH = "E:/AQI project/data/processed/delhi_aqi_timeseries.csv"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "aakrisht",   
    "database": "urban_aqi"
}

# =========================
# STEP 1: LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH, parse_dates=['date'])
df = df.set_index('date')
df = df.asfreq('D')

# =========================
# STEP 2: TRAIN–TEST SPLIT
# =========================
train_size = int(len(df) * 0.9)
train = df['aqi'][:train_size]
test = df['aqi'][train_size:]

# =========================
# STEP 3: TRAIN MODEL
# =========================
model = ARIMA(train, order=(5, 0, 0))
model_fit = model.fit()

# =========================
# STEP 4: EVALUATION
# =========================
predictions = model_fit.forecast(steps=len(test))

mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mean_squared_error(test, predictions))
accuracy = (1 - mae / test.mean()) * 100

# =========================
# STEP 5: FUTURE FORECAST
# =========================
future_forecast = model_fit.forecast(steps=FORECAST_DAYS)
future_dates = pd.date_range(
    start=df.index[-1] + pd.Timedelta(days=1),
    periods=FORECAST_DAYS,
    freq='D'
)

forecast_df = pd.DataFrame({
    "city": CITY,
    "forecast_date": future_dates,
    "predicted_aqi": future_forecast,
    "model": MODEL_NAME
})

# =========================
# STEP 6: CONNECT TO MYSQL
# =========================
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# =========================
# STEP 7: INSERT FORECASTS
# =========================
forecast_query = """
INSERT INTO aqi_forecasts (city, forecast_date, predicted_aqi, model)
VALUES (%s, %s, %s, %s)
"""

forecast_values = [
    (row.city, row.forecast_date.date(), float(row.predicted_aqi), row.model)
    for row in forecast_df.itertuples()
]

cursor.executemany(forecast_query, forecast_values)

# =========================
# STEP 8: INSERT METRICS
# =========================
metrics_query = """
INSERT INTO model_metrics (city, model, mae, rmse, accuracy)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.execute(metrics_query, (
    CITY,
    MODEL_NAME,
    float(mae),
    float(rmse),
    float(accuracy)
))

conn.commit()
cursor.close()
conn.close()

print("✅ Forecasts and model metrics successfully stored in MySQL")
print(f"MAE      : {mae:.2f}")
print(f"RMSE     : {rmse:.2f}")
print(f"Accuracy : {accuracy:.2f}%")
