import schedule
import time
import subprocess


def run_my_script():
    subprocess.run(
        [
            "python",
            "currency_stock_data.py",
        ]
    )
    subprocess.run(
        [
            "python",
            "stock_data.py",
        ]
    )
    subprocess.run(
        [
            "python",
            "currency_data.py",
        ]
    )
    subprocess.run(
        [
            "python",
            "previous_day_data.py",
        ]
    )
    subprocess.run(
        [
            "python",
            "stock_predict_analys_rate.py",
        ]
    )
    subprocess.run(
        [
            "python",
            "currency_predict_analys_rate.py",
        ]
    )


# Розклад
schedule.every().day.at("16:31").do(run_my_script)

# Головний цикл для перевірки розкладу
while True:
    schedule.run_pending()
    time.sleep(1)
