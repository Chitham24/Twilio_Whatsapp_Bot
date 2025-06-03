from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from tracker import mark_as_replied
from logger import log_to_file
app = Flask(__name__)


@app.route('/incoming', methods=['POST'])
def incoming_message():
    sender = request.form.get('From')
    body = request.form.get('Body')
    # print(f"Received message from {sender}: {body}")
    mark_as_replied(sender)
    log_to_file(f"Received message from {sender}: {body}")

    resp = MessagingResponse()
    resp.message("Thank you for your message! We'll be in touch soon.")
    return str(resp)

@app.route('/status_callback', methods=['POST'])
def status_callback():
    message_sid = request.form.get('MessageSid')
    message_status = request.form.get('MessageStatus')
    to_number = request.form.get('To')
    log_to_file(f"Status update for {message_sid}: {message_status} (to {to_number})")
    # print(f"Status update for {message_sid}: {message_status} (to {to_number})")
    return ('', 204)

if __name__ == '__main__':
    app.run(port=5000)
