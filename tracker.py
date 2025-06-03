import json
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from logger import log_to_file
from pytz import timezone

scheduler = BackgroundScheduler(timezone=timezone("Asia/Kolkata"))
scheduler.start()
IST = timezone("Asia/Kolkata")
TRACKER_FILE = "message_tracker.json"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_reminder(phone_number):
    data = read_tracker()
    log_to_file(f"Reminder triggered for {phone_number})")
    for entry in data:
        if entry["phone_number"] == phone_number and not entry["replied"]:
            try:
                twilio_client.messages.create(
                    to=phone_number,
                    from_=TWILIO_WHATSAPP_NUMBER,
                    content_sid ="HXe92f39f5e46b95efedea0ffca6b25cfc",
                    content_variables=json.dumps({
                                                    "1": "Chithambarash",
                                                    "2": "10th June",
                                                    "3": "5pm"
                                                })  
                )
                log_to_file(f"Reminder sent to {phone_number}")
            except Exception as e:
                log_to_file(f"Failed to send reminder to {phone_number}: {e}")
            break

def read_tracker():
    """Reads the message tracking JSON file. Returns a list of records."""
    if not os.path.exists(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_tracker(data):
    """Overwrites the tracker file with updated data."""
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_message_record(sid, phone_number):
    """Adds a new message entry to the tracker."""
    data = read_tracker()
    data.append({
        "sid": sid,
        "phone_number": phone_number,
        "timestamp": datetime.utcnow().isoformat(),
        "replied": False,
        "reminder_sent": False
    })
    write_tracker(data)

def schedule_reminder(phone_number):
    now = datetime.now(IST)
    run_time = now + timedelta(hours=24)
    log_to_file(f"Now (IST): {now.isoformat()}")
    log_to_file(f"Scheduled run_time (IST): {run_time.isoformat()}")
    log_to_file(f"Calling schedule_reminder for {phone_number}")
    if run_time < datetime.now(IST):
        log_to_file(f"Error: Scheduled run_time {run_time} is in the past!")

    job_id = f"reminder_{phone_number}_{run_time.isoformat()}"

    scheduler.add_job(
        func=send_reminder,
        trigger="date",
        run_date=run_time,
        args=[phone_number],
        id=job_id,
        replace_existing=True
    )
    log_to_file(f"Scheduled reminder job for {phone_number} at {run_time}")

def mark_as_replied(phone_number):
    """Marks the latest message to this number as replied if within 24 hours."""
    data = read_tracker()
    updated = False

    for entry in reversed(data):
        if entry["phone_number"] == phone_number and not entry["replied"]:
            sent_time = datetime.fromisoformat(entry["timestamp"])
            if datetime.utcnow() - sent_time <= timedelta(hours=24):
                entry["replied"] = True
                updated = True
                break

    if updated:
        write_tracker(data)