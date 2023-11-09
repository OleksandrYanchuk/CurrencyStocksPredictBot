import glob
import json
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt


def analysis_function(previous_day_data, predicted_prices):
    # Обчисліть різні метрики для порівняння фактичних та передбачених цін
    rmse = sqrt(mean_squared_error(previous_day_data["Close"], predicted_prices))
    mae = mean_absolute_error(previous_day_data["Close"], predicted_prices)

    # Округліть кожен елемент списку передбачених цін
    predicted_prices = [round(price, 6) for price in predicted_prices]

    actual_change = [
        (round((actual * 100), 6) / round(open_price, 6)) - 100
        for actual, open_price in zip(
            previous_day_data["Close"], previous_day_data["Open"]
        )
    ]
    predict_change = [
        (round((predicted * 100), 6) / round(open_price, 6)) - 100
        for predicted, open_price in zip(predicted_prices, previous_day_data["Open"])
    ]

    actual_change = [round(change, 2) for change in actual_change]
    predict_change = [round(change, 2) for change in predict_change]

    return {
        "RMSE": rmse,
        "MAE": mae,
        "actual_change": actual_change,
        "predict_change": predict_change,
    }


# Отримайте список файлів з фактичними цінами закриття та передбаченнями
previous_day_data_files = glob.glob("currency_stock_data/previous_day_data_stock_*.csv")
prediction_files = glob.glob("currency_stock_data/stock_predictions_*.json")

# Отримайте список унікальних дат з назв файлів
dates_previous_day_data = [
    file.split("_")[-1].split(".")[0] for file in previous_day_data_files
]
dates_predictions = [file.split("_")[-1].split(".")[0] for file in prediction_files]

# Знайдіть спільні дати для аналізу
common_dates = set(dates_previous_day_data) & set(dates_predictions)

# Виконайте аналіз для кожної спільної дати
results = {}
for date in common_dates:
    # Отримайте файли з фактичними цінами закриття та передбаченнями для поточної дати
    previous_day_data_file = f"currency_stock_data/previous_day_data_stock_{date}.csv"
    prediction_file = f"currency_stock_data/stock_predictions_{date}.json"

    # Завантажте фактичні ціни закриття
    previous_day_data = pd.read_csv(previous_day_data_file)
    # Заванажте передбачення
    with open(prediction_file, "r") as json_file:
        predictions = json.load(json_file)

    # Виконайте аналіз для кожної акції окремо
    for stock, predicted_prices in predictions.items():
        # Виберіть дані для обраної акції
        stock_data = previous_day_data[previous_day_data["Stock"] == stock]

        # Виконайте аналіз для цієї акції
        analysis_result = analysis_function(stock_data, predicted_prices)

        if stock not in results:
            results[stock] = {}
        results[stock] = analysis_result

# Збережіть результати в JSON-файл
with open("currency_stock_data/stock_analysis_results.json", "w") as json_file:
    json.dump(results, json_file, indent=4)
print("Результати аналізу збережено у файлі 'stock_analysis_results.json'.")
