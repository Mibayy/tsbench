-- Migration 0003_invoices
CREATE TABLE IF NOT EXISTS invoices (id SERIAL PRIMARY KEY, name TEXT NOT NULL);
