#!/usr/bin/env python
import os

import schedule
import time
import subprocess
from flask import Flask

app = Flask(__name__)

def run_my_script():
    subprocess.run(["python", "currency_stock_data/currency_stock_data.py"])
    subprocess.run(["python", "currency_stock_data/stock_data.py"])
    subprocess.run(["python", "currency_stock_data/currency_data.py"])
    subprocess.run(["python", "currency_stock_data/previous_day_data.py"])
    subprocess.run(["python", "currency_stock_data/stock_predict_analys_rate.py"])
    subprocess.run(["python", "currency_stock_data/currency_predict_analys_rate.py"])
    subprocess.run(["python", "data_cleaner.py"])
    subprocess.run(["python", "predict_bot.py"])

# Schedule the job
schedule.every().day.at("19:45").do(run_my_script)

# Main loop to check the schedule
def run_scheduled_job():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Use gunicorn to run the Flask app
if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    import multiprocessing

    # Number of worker processes
    workers = multiprocessing.cpu_count() * 2 + 1

    # Start the scheduled job in a separate thread
    import threading
    threading.Thread(target=run_scheduled_job).start()

    # Run the Flask app with gunicorn
    os.environ['MAGICK_NO_X11'] = '1'  # Set this if needed
    gunicorn_options = {
        'bind': '0.0.0.0:5000',  # Set the desired host and port
        'workers': workers,
        'worker_class': 'gevent',
    }
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(StandaloneApplication, self).__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key, value)

        def load(self):
            return self.application

    StandaloneApplication(app, gunicorn_options).run()
