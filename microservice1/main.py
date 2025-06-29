from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from confluent_kafka import Producer
from dotenv import load_dotenv

import psycopg2
import os
import json
import datetime

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("TOPIC_NAME")

# Connect to PostgreSQL (once, at app startup)
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Kafka producer
producer = Producer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET")
})

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def handle_submission(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    urgent: bool = Form(False),
    attachment: UploadFile = File(None)
):
    # Prepare data dictionary
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "subject": subject,
        "message": message,
        "urgent": urgent,
        "attachment_name": attachment.filename if attachment else None,
        "attachment_type": attachment.content_type if attachment else None
    }

    # Insert into DB
    insert_query = """
        INSERT INTO form_submissions
        (first_name, last_name, email, subject, message, urgent, attachment_name, attachment_type, created_at, email_status, last_error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        first_name,
        last_name,
        email,
        subject,
        message,
        urgent,
        data["attachment_name"],
        data["attachment_type"],
        datetime.datetime.utcnow(),
        'PENDING',
        None
    ))
    conn.commit()

    # Produce message to Kafka
    producer.produce(TOPIC_NAME, json.dumps(data).encode('utf-8'))
    producer.flush()

    return JSONResponse(
        status_code=200,
        content={"status": "success", "detail": "Form submitted successfully!"}
    )


@app.get("/")
def read_root():
    return {"message": "Backend is running"}
