from datetime import datetime
import csv
import time
import json
import os
from llm import generate_llm_message
from tracker import add_message_record, schedule_reminder

LOG_FILE = 'message_log.txt'

def send_campaign(client, llm_client, CSV_FILE, SENT_MESSAGES_FILE, TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'):
    results = []
    sent_messages = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('Name')
            phone_number = row.get('Phone Number')
            interest_areas = row.get('Interest Areas')
            if not name or not phone_number:
                status = "Missing data"
                continue
            to_whatsapp_number = f'whatsapp:{phone_number}'
            message_body = generate_llm_message(llm_client, name, interest_areas)
            # message_body = "Hi there"
            print(message_body)
            try:
                print(f"Sending message to {to_whatsapp_number} for {name}")
                message = client.messages.create(
                    body=message_body,
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=to_whatsapp_number
                )
                print(f"Message SID: {message.sid}")
                add_message_record(message.sid, phone_number)
                
                schedule_reminder(to_whatsapp_number)
                time.sleep(2)
                sent_messages.append({
                    "sid": message.sid,
                    "Name": name,
                    "Phone Number": phone_number
                })
            except Exception as e:
                print(f"Failed to send message to {name} ({phone_number}): {e}")
                status = f"Failed: {e}"
            
    with open(SENT_MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(sent_messages, f)

def read_logs():
    try:
        with open("message_log.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No logs yet."
