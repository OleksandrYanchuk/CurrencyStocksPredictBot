import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from labels import currency, stock_tickers, currency_tickers

currency_data = []
stock_data = []
stock_data_week = []
stock_data_month = []
start_data = datetime.today()
end_week = start_data - timedelta(days=7)
end_month = start_data - timedelta(days=30)

for idx, pair in enumerate(currency):
    ticker = currency_tickers[idx]
    data = yf.download(ticker, period="1d")
    data.insert(0, "Data", datetime.today().date())  # Додайте 'Data' на початок
    # Додаємо стовпець 'Currency' з назвою валютної пари
    data["Currency"] = pair
    currency_data.append(data)

for ticker in stock_tickers:
    data = yf.download(ticker, period="1d")
    data.insert(0, "Data", datetime.today().date())  # Додайте 'Data' на початок
    # Додаємо стовпець 'Stock' з назвою акції
    data["Stock"] = ticker
    stock_data.append(data)

for ticker in stock_tickers:
    data = yf.download(ticker, start=end_week, end=start_data)
    data["Stock"] = ticker
    stock_data_week.append(data)

for ticker in stock_tickers:
    data = yf.download(ticker, start=end_month, end=start_data)
    data["Stock"] = ticker
    stock_data_month.append(data)

# Об'єднуємо всі дані в один DataFrame
combined_data_currency = pd.concat(currency_data)
combined_data_stock = pd.concat(stock_data)
combined_data_stock_week = pd.concat(stock_data_week)
combined_data_stock_month = pd.concat(stock_data_month)

# Збережіть дані за акції та валютні пари за сьогодні
combined_data_currency.to_csv(
    f"combined_data_currency_{datetime.today().date()}.csv", index=False
)
combined_data_stock.to_csv(
    f"combined_data_stock_{datetime.today().date()}.csv", index=False
)
combined_data_stock_week.to_csv(
    f"combined_data_stock_week_{datetime.today().date()}.csv", index=False
)
combined_data_stock_month.to_csv(
    f"combined_data_stock_month_{datetime.today().date()}.csv", index=False
)
