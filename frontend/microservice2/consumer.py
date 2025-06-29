from confluent_kafka import Consumer
import json
import smtplib
from email.message import EmailMessage

# --- Kafka Consumer Setup ---
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'form-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['form-submissions'])

print("👂 Listening for messages on 'form-submissions'...")

# --- Email Configuration ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'harikabhavani.hb@gmail.com'
SENDER_PASSWORD = 'alzeogtmbrackrrj'  # ✅ use actual Gmail app password here

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("❌ Error:", msg.error())
        continue

    try:
        data = json.loads(msg.value().decode('utf-8'))
        print("📨 Received message:")
        print("🧾 Raw message data:", data)

        for k, v in data.items():
            print(f"  {k}: {v}")

        # --- Compose Email ---
        email_msg = EmailMessage()
        email_msg['Subject'] = f"Form Submission: {data.get('subject', 'No Subject')}"
        email_msg['From'] = SENDER_EMAIL
        email_msg['To'] = data.get('email', SENDER_EMAIL)  # fallback to sender if missing

        content = f"""
You received a new submission:

Name: {data.get('first_name', '')} {data.get('last_name', '')}
Email: {data.get('email', '')}
Subject: {data.get('subject', '')}
Message: {data.get('message', '')}
Attachment: {data.get('attachment_name', 'N/A')} ({data.get('attachment_type', '')})
"""
        email_msg.set_content(content)

        print("📧 Preparing to send email...")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(email_msg)

        print("✅ Email sent successfully.")

    except BaseException as e:
        print("❌ Failed to send email:", e)
