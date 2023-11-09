import schedule
import time
import subprocess


def run_my_script():
    subprocess.run(
        [
            "python",
            "data_cleaner.py",
        ]
    )


# Розклад
schedule.every().day.at("16:50").do(run_my_script)

# Головний цикл для перевірки розкладу
while True:
    schedule.run_pending()
    time.sleep(1)
