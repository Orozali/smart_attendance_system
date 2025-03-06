import schedule
import time
def job():
    print("Running scheduled task...")

# Schedule the task
schedule.every().day.at("13:13").do(job)  # Runs every day at 12:00 PM

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
