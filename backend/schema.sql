CREATE TABLE IF NOT EXISTS job_applications(
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    date_applied TEXT NOT NULL,
    platform TEXT,
    link TEXT,
    pay_type TEXT NOT NULL CHECK(pay_type IN('Contract', 'Hourly', 'Salaried', 'Internship')),
    pay_amount REAL NOT NULL,
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'Applied',
    last_heard_from TEXT
);

CREATE TABLE IF NOT EXISTS interview_rounds(
    id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    round_date TEXT NOT NULL,
    round_label TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (application_id) REFERENCES job_applications(id)
);

CREATE TABLE IF NOT EXISTS job_application_log(
    id INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL,
    log_date TEXT NOT NULL,
    log_time TEXT NOT NULL,
    event TEXT NOT NULL,
    FOREIGN KEY (application_id) REFERENCES job_applications(id)
);