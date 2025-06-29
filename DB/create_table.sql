CREATE TABLE IF NOT EXISTS form_submissions (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    subject TEXT,
    message TEXT,
    attachment_name TEXT,
    attachment_type TEXT,
    urgent BOOLEAN DEFAULT false,
    processed BOOLEAN DEFAULT false,
    last_error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS internal_team_emails (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);