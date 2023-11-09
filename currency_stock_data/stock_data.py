import json
import os


import joblib
import pandas as pd
from datetime import datetime, timedelta

from sklearn.preprocessing import LabelEncoder

stock_data = pd.read_csv(
    f"currency_stock_data/combined_data_stock_{datetime.today().date()}.csv",
    skiprows=[0],  # Пропустити перший рядок (назви стовпців)
    names=[
        "Data",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Stock",
    ],
    dtype={
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Adj Close": float,
        "Volume": int,
    },
)

stock_data_week = pd.read_csv(
    f"currency_stock_data/combined_data_stock_week_{datetime.today().date()}.csv",
    skiprows=[0],  # Пропустити перший рядок (назви стовпців)
    names=[
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Stock",
    ],
    dtype={
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Adj Close": float,
        "Volume": int,
    },
)

stock_data_month = pd.read_csv(
    f"currency_stock_data/combined_data_stock_month_{datetime.today().date()}.csv",
    skiprows=[0],  # Пропустити перший рядок (назви стовпців)
    names=[
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Stock",
    ],
    dtype={
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Adj Close": float,
        "Volume": int,
    },
)

grouped_week = stock_data_week.groupby("Stock")
average_data_week = grouped_week.mean().reset_index()

grouped_month = stock_data_month.groupby("Stock")
average_data_month = grouped_month.mean().reset_index()

average_data_month.insert(0, "Data", datetime.today().date())
average_data_week.insert(0, "Data", datetime.today().date())


stock_data["Data"] = pd.to_datetime(stock_data["Data"])
stock_data["Date"] = stock_data["Data"].apply(lambda x: x.timestamp())

average_data_week["Data"] = pd.to_datetime(average_data_week["Data"])
average_data_week["Date"] = average_data_week["Data"].apply(lambda x: x.timestamp())

average_data_month["Data"] = pd.to_datetime(average_data_month["Data"])
average_data_month["Date"] = average_data_month["Data"].apply(lambda x: x.timestamp())

label_encoder = LabelEncoder()
stock_data["Stock_encoded"] = label_encoder.fit_transform(stock_data["Stock"])
average_data_week["Stock_encoded"] = label_encoder.fit_transform(
    average_data_week["Stock"]
)
average_data_month["Stock_encoded"] = label_encoder.fit_transform(
    average_data_month["Stock"]
)

selected_columns = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Stock_encoded",
]


current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, "..", "models", "model_stock.pkl")

model = joblib.load(file_path)


# Визначте унікальні валютні пари
unique_stock = stock_data["Stock"].unique()
unique_stock_week = average_data_week["Stock"].unique()
unique_stock_month = average_data_month["Stock"].unique()

# Проведіть передбачення для кожної валютної пари
predictions_by_stock = {}
for stock in unique_stock:
    data_subset = stock_data[stock_data["Stock"] == stock]
    X = data_subset[selected_columns]
    predictions = model.predict(X)
    predictions_by_stock[stock] = predictions

predictions_by_stock_week = {}
for stock in unique_stock_week:
    data_subset = average_data_week[average_data_week["Stock"] == stock]
    X = data_subset[selected_columns]
    predictions = model.predict(X)
    predictions_by_stock_week[stock] = predictions

predictions_by_stock_month = {}
for stock in unique_stock_month:
    data_subset = average_data_month[average_data_month["Stock"] == stock]
    X = data_subset[selected_columns]
    predictions = model.predict(X)
    predictions_by_stock_month[stock] = predictions


for stock, predictions in predictions_by_stock.items():
    predictions_by_stock[stock] = predictions.tolist()

for stock, predictions in predictions_by_stock_week.items():
    predictions_by_stock_week[stock] = predictions.tolist()

for stock, predictions in predictions_by_stock_month.items():
    predictions_by_stock_month[stock] = predictions.tolist()

# Збережіть словник у JSON файл
file_name = f"currency_stock_data/stock_predictions_{datetime.today().date()}.json"
with open(file_name, "w") as json_file:
    json.dump(predictions_by_stock, json_file)


file_name = f"currency_stock_data/stock_predictions_week_{datetime.today().date()}.json"
with open(file_name, "w") as json_file:
    json.dump(predictions_by_stock_week, json_file)

file_name = (
    f"currency_stock_data/stock_predictions_month_{datetime.today().date()}.json"
)
with open(file_name, "w") as json_file:
    json.dump(predictions_by_stock_month, json_file)
