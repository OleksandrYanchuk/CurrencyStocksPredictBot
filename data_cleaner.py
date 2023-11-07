import os
import datetime

directory = "currency_stock_data"
current_time = datetime.datetime.now()

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    if filename.endswith(".csv") or filename.endswith(".json"):
        file_creation_time = datetime.datetime.fromtimestamp(
            os.path.getctime(file_path)
        )
        days_difference = (current_time - file_creation_time).days

        if days_difference > 3:
            os.remove(file_path)
            print(f"Видалено файл: {filename}")
