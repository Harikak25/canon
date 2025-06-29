# CANON – Customer Alert & Notification Orchestration Network

CANON is a microservice system to collect customer contact form submissions, route them via Kafka, store them in PostgreSQL, and send email notifications to customers and internal teams.

----------------------------------------

PROJECT STRUCTURE:

FS_Project/
├── frontend/            # React frontend
├── microservice1/       # FastAPI form ingestion + Kafka producer
├── microservice2/       # Kafka consumer + email sender
├── db/                  # SQL migration scripts
├── canon-infra/         # Terraform configs
└── README.md

----------------------------------------

PREREQUISITES:

- Node.js >= 18
- Python >= 3.9
- PostgreSQL client (e.g. psql)
- Confluent Cloud account
- Azure account + CLI installed
- Terraform installed
- Git

----------------------------------------

STEPS TO REPRODUCE LOCALLY & IN CLOUD:

----------------------------------------
STEP 1 - CLONE THE REPO

git clone https://github.com/Harikak25/canon.git
cd canon

----------------------------------------
STEP 2 - TERRAFORM (DB + KEY VAULT)

cd canon-infra
terraform init
terraform apply

After terraform runs, note:
- Postgres FQDN
- Admin username
- Key Vault name

----------------------------------------
STEP 3 - CREATE DATABASE

Connect:

psql "postgresql://<admin_user>:<password>@<fqdn>:5432/postgres?sslmode=require"

Create DB:

CREATE DATABASE canon_db;

Switch DB:

\c canon_db

----------------------------------------
STEP 4 - RUN SQL TABLES

Put this SQL in a file:

db/create_tables.sql

----------------------------------------

CREATE TABLE IF NOT EXISTS form_submissions (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    urgent BOOLEAN NOT NULL DEFAULT FALSE,
    attachment_name TEXT,
    attachment_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    last_error_message TEXT
);

CREATE TABLE IF NOT EXISTS internal_team_emails (
    id SERIAL PRIMARY KEY,
    team_member_name TEXT NOT NULL,
    team_member_email TEXT NOT NULL
);

----------------------------------------

Run it:

psql "postgresql://<admin_user>:<password>@<fqdn>:5432/canon_db?sslmode=require" -f db/create_tables.sql

----------------------------------------
STEP 5 - SEED INTERNAL TEAM EMAILS

psql "postgresql://<admin_user>:<password>@<fqdn>:5432/canon_db?sslmode=require"

INSERT INTO internal_team_emails (team_member_name, team_member_email)
VALUES ('Nalanda', 'sainalanda0523@gmail.com');

----------------------------------------
STEP 6 - FRONTEND

cd frontend
npm install
npm start

----------------------------------------
STEP 7 - FASTAPI MICROSERVICE 1

cd ../microservice1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

----------------------------------------
STEP 8 - FASTAPI MICROSERVICE 2

cd ../microservice2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py

----------------------------------------
ENV FILES

frontend/.env → no secrets required

microservice1/.env:

DB_URL=postgresql://canonuser:<password>@<fqdn>:5432/canon_db
KAFKA_BOOTSTRAP_SERVERS=<bootstrap-servers>
KAFKA_API_KEY=<api-key>
KAFKA_API_SECRET=<api-secret>
TOPIC_NAME=form-submissions

microservice2/.env:

DB_URL=postgresql://canonuser:<password>@<fqdn>:5432/canon_db
KAFKA_BOOTSTRAP_SERVERS=<bootstrap-servers>
KAFKA_API_KEY=<api-key>
KAFKA_API_SECRET=<api-secret>
TOPIC_NAME=form-submissions
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=<your-email>
SENDER_PASSWORD=<your-app-password>

----------------------------------------
AZURE STATIC WEB APP (OPTIONAL)

az staticwebapp create \
  --name canon-frontend \
  --resource-group canon-rg \
  --source ./frontend \
  --location eastasia \
  --branch master \
  --token <your-github-token>

Then push code to your repo:

cd frontend
git add .
git commit -m "Deploy frontend to Azure Static Web App"
git push origin master

----------------------------------------
