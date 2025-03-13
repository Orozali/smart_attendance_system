from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

scheduler = BackgroundScheduler()

LESSON_TIMES = ["08:00", "08:55", "09:50", "10:45", "11:40", "12:35", "13:30", "14:25", "15:20", "16:15"]

def capture_faces(lesson_time):
    print(f"Capturing faces at {lesson_time} - {datetime.now()}")

def start_schedulers():
    for lesson_time in LESSON_TIMES:
        start_hour, start_minute = map(int, lesson_time.split(":"))
        
        # Adjust minute and hour correctly
        if start_minute < 10:
            adjusted_hour = start_hour - 1  # Move to previous hour
            adjusted_minute = (start_minute - 10) % 60  # Convert to valid minute value
        else:
            adjusted_hour = start_hour
            adjusted_minute = start_minute - 10

        # Schedule jobs only from Monday to Friday (day_of_week=0-4)
        scheduler.add_job(
            capture_faces,
            CronTrigger(hour=adjusted_hour, minute=adjusted_minute, day_of_week="0-4"),  # Monday-Friday only
            args=[lesson_time],
            id=f"capture_{lesson_time.replace(':', '')}"  # Unique ID
        )

    scheduler.start()
    print("All cron jobs started (Monday to Friday)")

if not scheduler.running:
    start_schedulers()
