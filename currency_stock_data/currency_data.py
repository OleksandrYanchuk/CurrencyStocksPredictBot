import json
import os
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import joblib

print(os.getcwd())

currency_data = pd.read_csv(
    f"currency_stock_data/combined_data_currency_{datetime.today().date()}.csv",
    skiprows=[0],  # Пропустити перший рядок (назви стовпців)
    names=[
        "Data",
        "Open_Currency",
        "High_Currency",
        "Low_Currency",
        "Close_Currency",
        "Adj Close_Currency",
        "Volume",
        "Currency_Currency",
    ],
    dtype={
        "Open_Currency": float,
        "High_Currency": float,
        "Low_Currency": float,
        "Close_Currency": float,
        "Adj Close_Currency": float,
        "Volume": int,
    },
)

currency_data["Data"] = pd.to_datetime(currency_data["Data"])
currency_data["Date"] = currency_data["Data"].apply(lambda x: x.timestamp())


label_encoder = LabelEncoder()
currency_data["Currency_Currency_encoded"] = label_encoder.fit_transform(
    currency_data["Currency_Currency"]
)

selected_columns = [
    "Date",
    "Open_Currency",
    "High_Currency",
    "Low_Currency",
    "Close_Currency",
    "Adj Close_Currency",
    "Currency_Currency_encoded",
]

current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, "..", "models", "model_currency_pairs.pkl")

model = joblib.load(file_path)


# Визначте унікальні валютні пари
unique_currency_pairs = currency_data["Currency_Currency"].unique()

# Проведіть передбачення для кожної валютної пари
predictions_by_currency_pair = {}
for currency_pair in unique_currency_pairs:
    data_subset = currency_data[currency_data["Currency_Currency"] == currency_pair]
    X = data_subset[selected_columns]
    predictions = model.predict(X)
    predictions_by_currency_pair[currency_pair] = predictions

# Результати передбачення збережені в словнику "predictions_by_currency_pair"
for currency_pair, predictions in predictions_by_currency_pair.items():
    

for currency_pair, predictions in predictions_by_currency_pair.items():
    predictions_by_currency_pair[currency_pair] = predictions.tolist()

# Збережіть словник у JSON файл
file_name = f"currency_stock_data/currency_predictions_{datetime.today().date()}.json"
with open(file_name, "w") as json_file:
    json.dump(predictions_by_currency_pair, json_file)
