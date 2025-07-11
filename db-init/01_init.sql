-- Enable extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Raw snapshots straight from API
CREATE TABLE IF NOT EXISTS train_eta_raw (
    line_code       TEXT,
    station_code    TEXT,
    destination     TEXT,
    platform        TEXT,
    direction       TEXT,
    eta             TIMESTAMPTZ,
    polled_at       TIMESTAMPTZ DEFAULT NOW()
);

-- Create hypertable
SELECT create_hypertable('train_eta_raw', 'polled_at', if_not_exists => TRUE);

-- Index to speed up "latest per station" queries
CREATE INDEX IF NOT EXISTS train_eta_station_ts_idx
    ON train_eta_raw (line_code, station_code, polled_at DESC);