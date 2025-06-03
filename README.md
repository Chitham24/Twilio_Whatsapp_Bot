# Twilio WhatsApp Bot

A Flask and Streamlit-based automation tool that uses Twilio's WhatsApp API to send personalized messages, track user responses, and send follow-up reminders if users don’t respond within a specified time. It integrates LLMs for custom message generation and provides a lightweight scheduler using APScheduler.

---

## 📦 Tech Stack

- **Python**
- **Flask** – for webhook server and API endpoints  
- **Streamlit** – for simple frontend UI
- **Twilio WhatsApp API** – to send and track WhatsApp messages  
- **Gemini API** – for LLM-based message customization  
- **APScheduler** – for scheduling follow-up reminders  
- **Ngrok** – for tunneling Flask server during local development  

---

## ⚙️ How It Works

1. **Streamlit UI** is used to load a CSV of contacts (name, phone number, interest area).
2. For each contact:
   - An **LLM-generated personalized message** is created using Gemini API.
   - The message is **sent via Twilio's WhatsApp API**.
   - Message metadata is **logged to a JSON file**.
   - A **reminder job is scheduled** via APScheduler to follow up after 24 hours.
3. A **Flask server** handles:
   - Incoming WhatsApp messages (via `/incoming`) and logs them.
   - Status callbacks (via `/status_callback`) to track delivery, read status, and replies.
   - On receiving a reply, the reminder job is **canceled**.

---

## 📂 File Overview

### `main.py`
- The entry point for the Streamlit UI.
- Loads environment variables and contacts CSV.
- Sends messages using the Twilio API.

### `server.py`
- The Flask server handling Twilio webhooks:
  - `/incoming`: logs incoming user replies.
  - `/status_callback`: logs message delivery status.

### `tracker.py`
- Manages tracking of message states in a JSON file.
- Functions:
  - `add_message_record`: logs new outgoing messages.
  - `mark_as_replied`: updates JSON when a user replies.
  - `schedule_reminder`: sets up a follow-up reminder if no reply is received.
  - `send_reminder`: sends reminder message using Twilio's pre-approved template.

### `llm.py`
- Uses **Gemini API** to generate a customized campaign message.
- The message is tailored based on name and interest areas.
- Ensures that the message is concise (under 50 words) and contextually relevant.

---

## ✅ Optional Enhancements


- **Database Integration**: Replace JSON file with a relational database (e.g., PostgreSQL or SQLite) to:
  - Persist full chat history per lead
  - Enable efficient querying and analytics
- **Advanced Streamlit Dashboard**:
  - Visualize metrics like response rates, read status, and lead engagement
  - Add filters to view and search logs by status, date, or phone number
- **Media Support**:
  - Enable sending of images, PDFs, and other media via Twilio API
- **Robust Scheduling**:
  - Use background workers like Celery + Redis for reliable and scalable job scheduling
  - Improve handling of time zones, retries, and delivery failures
- **Containerization**:
  - Dockerize the app for easier deployment, scaling, and environment consistency
- **Enhanced Logging**:
  - Improve log format (e.g., JSON lines)
  - Integrate with logging dashboards (like ELK stack) for production use

---

