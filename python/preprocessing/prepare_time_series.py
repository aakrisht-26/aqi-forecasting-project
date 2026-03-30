import pandas as pd
import mysql.connector

# =========================
# CONFIGURATION
# =========================
CITY = "Delhi"   # change if you want another city

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "aakrisht",  
    "database": "urban_aqi"
}

# =========================
# STEP 1: CONNECT TO MYSQL
# =========================
conn = mysql.connector.connect(**DB_CONFIG)

query = f"""
SELECT date, aqi
FROM city_daily_aqi
WHERE city = '{CITY}'
ORDER BY date;
"""

df = pd.read_sql(query, conn)
conn.close()

print(f"Loaded {len(df)} rows for city: {CITY}")

# =========================
# STEP 2: BASIC CLEANING
# =========================
df['date'] = pd.to_datetime(df['date'])

# Check missing values
missing_before = df['aqi'].isna().sum()
print("Missing AQI before cleaning:", missing_before)

# Forward fill missing AQI
df['aqi'] = df['aqi'].ffill()

# Drop any remaining NaNs (usually at start)
df = df.dropna()

missing_after = df['aqi'].isna().sum()
print("Missing AQI after cleaning:", missing_after)

# =========================
# STEP 3: SET TIME INDEX
# =========================
df = df.set_index('date')

print("\nTime series preview:")
print(df.head())

# =========================
# STEP 4: BASIC SANITY CHECKS
# =========================
print("\nTime range:")
print("Start:", df.index.min())
print("End  :", df.index.max())

print("\nAQI statistics:")
print(df['aqi'].describe())

# =========================
# STEP 5: SAVE CLEAN DATA (OPTIONAL BUT PROFESSIONAL)
# =========================
output_path = f"E:\AQI project\data\processed\{CITY.lower()}_aqi_timeseries.csv"
df.to_csv(output_path)

print(f"\nClean time series saved to: {output_path}")
print("✅ Preprocessing completed successfully")
