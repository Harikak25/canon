from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from confluent_kafka import Producer
import json

app = FastAPI()
producer = Producer({'bootstrap.servers': 'localhost:9092'})
TOPIC = 'form-submissions'


# Allow frontend (localhost:3000) to send requests here
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
    attachment: UploadFile = File(None)
):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "subject": subject,
        "message": message,
        "attachment_name": attachment.filename if attachment else None,
        "attachment_type": attachment.content_type if attachment else None
    }

    print("✅ Sending to Kafka:", data)
    producer.produce(TOPIC, json.dumps(data).encode('utf-8'))
    producer.flush()

    return JSONResponse(
        status_code=200,
        content={"status": "success", "detail": "Form sent to Kafka!"}
    )


@app.get("/")
def read_root():
    return {"message": "Backend is running"}
