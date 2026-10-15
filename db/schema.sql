-- Day 4 schema. Run with: python scripts/init_db.py
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS leads (
    lead_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL DEFAULT 'Valued Prospect',
    phone           TEXT CHECK (phone IS NULL OR length(phone) = 10),
    location        TEXT,
    location_source TEXT,
    title           TEXT,
    question        TEXT,
    posted_date     TEXT,
    thread_url      TEXT NOT NULL UNIQUE,
    source_url      TEXT,
    scraped_at      TEXT,
    score           INTEGER CHECK (score IS NULL OR (score BETWEEN 0 AND 100)),
    loaded_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id     INTEGER NOT NULL REFERENCES leads(lead_id),
    sales_tag   TEXT,
    notes       TEXT,
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_leads_location ON leads(location);