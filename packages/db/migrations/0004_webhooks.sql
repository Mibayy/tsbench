-- Migration 0004_webhooks
CREATE TABLE IF NOT EXISTS webhooks (id SERIAL PRIMARY KEY, name TEXT NOT NULL);
