#!/usr/bin/env python
import os

import schedule
import time
import subprocess


def run_my_script():
    subprocess.run(["python", "currency_stock_data/currency_stock_data.py"])
    subprocess.run(["python", "currency_stock_data/stock_data.py"])
    subprocess.run(["python", "currency_stock_data/currency_data.py"])
    subprocess.run(["python", "currency_stock_data/previous_day_data.py"])
    subprocess.run(["python", "currency_stock_data/stock_predict_analys_rate.py"])
    subprocess.run(["python", "currency_stock_data/currency_predict_analys_rate.py"])
    subprocess.run(["python", "data_cleaner.py"])
    subprocess.run(["python", "predict_bot.py"])


schedule.every().day.at("18:58").do(run_my_script)

# Головний цикл для перевірки розкладу
while True:
    schedule.run_pending()
    time.sleep(1)
