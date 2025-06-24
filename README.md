# CANON – Customer Alert & Notification Orchestration Network

**CANON** is a lightweight microservice-based platform that captures "Contact Us" form submissions, processes them via Kafka, stores them in PostgreSQL, and sends real-time email notifications to customers. Built with FastAPI, Kafka, and React, CANON is ideal for businesses looking to streamline and scale customer communication workflows.

---

## 🔧 Key Features

- 📬 Frontend form built with **React**
- ⚙️ Backend powered by **FastAPI**
- 🧵 Asynchronous messaging using **Kafka**
- 🗃️ Persistent storage via **PostgreSQL**
- 🔐 Credential management via `.env` (KMS integration planned)
- 📧 Email notifications via **SMTP**
- 🧪 Local dev with `venv`, live-reloading, and Kafka CLI tools

---

## 📁 Project Structure

```
FS_Project/
├── frontend/         # React UI for form submission
├── microservice1/    # FastAPI producer service (form ingestion)
├── microservice2/    # Kafka consumer & email sender
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/fs-project.git
cd fs-project
```

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

### 3. Microservice 1 – FastAPI Producer

```bash
cd ../microservice1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

---

### 4. Microservice 2 – Kafka Consumer & Email Sender

```bash
cd ../microservice2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py
```

---

## 🔐 Environment Variables

Create a `.env` file in both `microservice1/` and `microservice2/` directories based on the `.env.example` templates.

### `microservice1/.env`

```env
DB_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=form-submissions
```

### `microservice2/.env`

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=form-submissions
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@email.com
SENDER_PASSWORD=your-app-password
```

> 🔒 *Never commit real secrets — use `.env` and `.gitignore` wisely.*

---

## 📬 Use Case

**CANON** is perfect for:
- Customer-facing "Contact Us" forms
- Automated intake and routing of inquiries
- Real-time notifications for support teams or customer replies
- Future CRM integration pipelines

