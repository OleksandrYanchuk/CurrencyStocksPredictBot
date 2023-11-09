import schedule
import time
import subprocess


def run_my_script():
    subprocess.run(["python", "predict_bot.py"])


schedule.every().day.at("22:16").do(run_my_script)


# Main loop to check the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
