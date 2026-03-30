import pandas as pd
import mysql.connector

# -------- 1. Load Raw CSV --------
df = pd.read_csv("E:/AQI project/data/raw/city_day.csv")

# -------- 2. Date Parsing --------
df['Datetime'] = pd.to_datetime(df['Datetime'])

# -------- 3. Rename Columns --------
df = df.rename(columns={
    'City': 'city',
    'Datetime': 'date',
    'PM2.5': 'pm25',
    'PM10': 'pm10',
    'NO': 'no',
    'NO2': 'no2',
    'NOx': 'nox',
    'NH3': 'nh3',
    'CO': 'co',
    'SO2': 'so2',
    'O3': 'o3',
    'AQI': 'aqi',
    'AQI_Bucket': 'aqi_bucket'
})

# -------- 4. Drop Intentionally Excluded Columns --------
df = df.drop(columns=['Benzene', 'Toluene', 'Xylene'], errors='ignore')

# -------- 5. Connect to MySQL --------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aakrisht",
    database="urban_aqi"
)

cursor = conn.cursor()

# -------- 6. Insert Query --------
insert_query = """
INSERT IGNORE INTO city_daily_aqi
(city, date, pm25, pm10, no, no2, nox, nh3, co, so2, o3, aqi, aqi_bucket)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# -------- 7. Load Data --------
for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()
conn.close()

print("✅ City-level daily AQI data loaded successfully")
