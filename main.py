import os
from dotenv import load_dotenv, dotenv_values
import datetime
from twilio.rest import Client
import streamlit as st
from utils import send_campaign, read_logs
from google import genai

load_dotenv()

print("Loaded from .env:", dotenv_values())
print("Loaded from environment:", os.environ.get("TWILIO_ACCOUNT_SID"))

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886' 
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
llm_client = genai.Client(api_key=GEMINI_API_KEY)

print(TWILIO_ACCOUNT_SID)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
CSV_FILE = 'Leads_data.csv'
SENT_MESSAGES_FILE = 'sent_messages.json'

st.title("WhatsApp Campaign Sender")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    st.error("Twilio credentials are missing. Please check your .env file.")

if st.button("Send WhatsApp Campaign"):
    st.info("Sending messages...")
    send_campaign(client, llm_client, CSV_FILE, SENT_MESSAGES_FILE)
    st.success("Campaign completed.")
    

st.subheader("Live Message and Status Logs")

log_text = read_logs()
st.text_area("Log Output", log_text, height=300)

if st.button("Refresh Logs"):
    log_text = read_logs()
    
