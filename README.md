Urban Air Quality Forecasting System

Overview
This project focuses on predicting Air Quality Index (AQI) using machine learning. It follows a complete pipeline starting from data preprocessing to model prediction and visualization. The goal is to build a practical system that can forecast AQI values and help in understanding pollution trends.
The project combines Python-based modeling, MySQL for storage, and Power BI for visualization.

Features:
AQI prediction using XGBoost regression
Time-series feature engineering (lag values, rolling averages, trends)
Model evaluation using MAE, RMSE, and accuracy
Storage of predictions in MySQL
Visualization using Power BI dashboard
Modular structure for different stages of the pipeline

Tech Stack:
Python
Pandas, NumPy, XGBoost, Scikit-learn, Matplotlib
MySQL
Power BI

Project Structure:
AQI Project/
│
├── python/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── modeling/
│   ├── evaluation/
│
├── sql/
│   └── aqi_predictions.sql
│
├── docs/
│   ├── aqi_prediction.png
│   └── feature_importance.png
│
├── power bi/
│   └── Delhi AQI Dashboard.pbix
│
├── requirements.txt
└── README.md

Workflow:
Raw Data → Preprocessing → Feature Engineering → Model Training → Predictions → MySQL → Power BI Dashboard

Model Performance:-
MAE: 9.06
RMSE: 11.58
Accuracy: 88.91%

Tolerance-based accuracy:
±15: 81.15%
±20: 92.35%
±30: 98.63%

Dashboard:-
The Power BI dashboard shows:

Actual vs predicted AQI
Monthly AQI trends
Error distribution
Filters for month-wise analysis

Database:-
MySQL is used to store predicted AQI values. This allows structured storage and makes it easier to connect with Power BI for visualization.

How to Run:-
Clone the repository:
git clone https://github.com/aakrisht-26/aqi-forecasting-project.git
cd aqi-forecasting-project

Create virtual environment:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the model:
python python/modeling/aqi_forecast.py


Future Work:
Try deep learning models like LSTM
Add real-time data using APIs
Deploy using Flask or FastAPI
Automate pipeline

Author:-
Aakrisht Yadav
B.Tech CSE (Data Science)
