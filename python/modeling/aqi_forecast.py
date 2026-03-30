import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
# =========================
# LOAD DATA
# =========================
df = pd.read_csv("E:/AQI project/data/processed/delhi_aqi_timeseries.csv")

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df.set_index('date', inplace=True)

# =========================
# FEATURE ENGINEERING
# =========================

# Lag features
for lag in [1,2,3,5,7,10,14,21,30]:
    df[f'lag_{lag}'] = df['aqi'].shift(lag)

# Rolling features
df['rolling_mean_3'] = df['aqi'].rolling(3).mean()
df['rolling_mean_7'] = df['aqi'].rolling(7).mean()
df['rolling_mean_14'] = df['aqi'].rolling(14).mean()

df['rolling_std_7'] = df['aqi'].rolling(7).std()

# Trend feature
df['trend'] = df['aqi'] - df['lag_1']

# Time features
df['month'] = df.index.month
df['day_of_week'] = df.index.dayofweek

df.dropna(inplace=True)

# =========================
# TRAIN TEST SPLIT
# =========================
train = df[df.index.year < 2024]
test = df[df.index.year == 2024]

X_train = train.drop(columns=['aqi'])
y_train = train['aqi']

X_test = test.drop(columns=['aqi'])
y_test = test['aqi']

# =========================
# MODEL
# =========================
model = XGBRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =========================
# PREDICTIONS
# =========================
predictions = model.predict(X_test)

# =========================
# EVALUATION
# =========================
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
accuracy = 100 - mape

print("\nXGBoost Results")
print("MAE:", round(mae,2))
print("RMSE:", round(rmse,2))
print("MAPE:", round(mape,2))
print("Accuracy:", round(accuracy,2), "%")

# =========================
# TOLERANCE ACCURACY
# =========================
print("\nTolerance-Based Accuracy")

for tol in [10, 15, 20, 30]:
    correct = np.abs(y_test - predictions) <= tol
    acc = correct.mean() * 100
    print(f"Accuracy within ±{tol}: {round(acc,2)}%")

# =========================
# SAVE RESULTS
# =========================
result_df = pd.DataFrame({
    "date": y_test.index,
    "actual_aqi": y_test.values,
    "predicted_aqi": predictions
})

result_df.to_csv("E:/AQI project/data/processed/delhi_xgb_predictions.csv", index=False)

print("\nPredictions saved")

# =========================
# SAVE PLOT
# =========================
plt.figure(figsize=(12,6))

plt.plot(y_test.index, y_test, label="Actual AQI", color="green")
plt.plot(y_test.index, predictions, label="Predicted AQI", color="red")

plt.title("XGBoost AQI Prediction")
plt.xlabel("Date")
plt.ylabel("AQI")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("E:/AQI project/docs/aqi_prediction.png")
plt.close()

print("Plot saved")

# =========================
# STORE RESULTS IN MYSQL
# =========================
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aakrisht",   
    database="aqi_db"
)

cursor = conn.cursor()

# Optional: clear old data (clean table each run)
cursor.execute("DELETE FROM aqi_predictions")

for i in range(len(y_test)):
    cursor.execute("""
        INSERT INTO aqi_predictions (date, actual_aqi, predicted_aqi)
        VALUES (%s, %s, %s)
    """, (
        str(y_test.index[i].date()),
        float(y_test.values[i]),
        float(predictions[i])
    ))

conn.commit()

cursor.close()
conn.close()

print("Data stored in MySQL successfully")