import os
import json
import smtplib
import psycopg2
from email.message import EmailMessage
from dotenv import load_dotenv
from confluent_kafka import Consumer

# Load env vars
load_dotenv()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_API_KEY = os.getenv("KAFKA_API_KEY")
KAFKA_API_SECRET = os.getenv("KAFKA_API_SECRET")
TOPIC_NAME = os.getenv("TOPIC_NAME")

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Database configuration
DB_URL = os.getenv("DB_URL")

# Kafka Consumer config
consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': KAFKA_API_KEY,
    'sasl.password': KAFKA_API_SECRET,
    'group.id': 'form-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC_NAME])

print("👂 Listening for messages on:", TOPIC_NAME)

def update_submission_status(submission_id, status, error_message=None):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        UPDATE submissions
        SET processed_status = %s,
            last_error_message = %s
        WHERE id = %s
    """, (status, error_message, submission_id))
    conn.commit()
    cur.close()
    conn.close()

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue

    if msg.error():
        print("❌ Kafka error:", msg.error())
        continue

    msg_value = msg.value()
    if not msg_value:
        print("⚠️ Skipped empty message.")
        continue

    try:
        data = json.loads(msg_value.decode('utf-8'))
        print("📨 Received message:", data)

        # Compose confirmation email for customer
        email_msg = EmailMessage()
        email_msg['Subject'] = f"Confirmation: We received your message about '{data.get('subject', 'No Subject')}'"
        email_msg['From'] = SENDER_EMAIL
        email_msg['To'] = data.get('email', SENDER_EMAIL)

        body = f"""
Hi {data.get('first_name', '')},

Thanks for reaching out to us via CANON. We've received your message with the following details:

Name: {data.get('first_name', '')} {data.get('last_name', '')}
Email: {data.get('email', '')}
Urgent: {'Yes' if data.get('urgent') else 'No'}
Subject: {data.get('subject', '')}
Message: {data.get('message', '')}
Attachment: {data.get('attachment_name', 'N/A')} ({data.get('attachment_type', '')})

We’ll get back to you as soon as possible.

Best regards,
The CANON Team
"""
        email_msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(email_msg)

        print("✅ Confirmation email sent.")

        # Update DB as emailed
        submission_id = data.get('id')
        if submission_id:
            update_submission_status(submission_id, 'emailed', None)

    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", str(e))
        continue

    except Exception as e:
        print("❌ Failed to process message:", str(e))
        try:
            if 'data' in locals():
                submission_id = data.get('id')
                if submission_id:
                    update_submission_status(submission_id, 'failed', str(e))
        except Exception as nested:
            print("⚠️ Also failed updating DB:", str(nested))
        continue