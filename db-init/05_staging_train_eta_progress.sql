-- Create denormalized staging table train_eta_progress
-- adding station-level progress to train_eta
-- We only take the last minute to avoid bloat

CREATE TABLE train_eta_progress (
    id              BIGSERIAL   PRIMARY KEY,
    line_code       TEXT        NOT NULL,
    direction       TEXT        NOT NULL,
    station_code    TEXT        NOT NULL,
    destination     TEXT,
    eta             TIMESTAMPTZ NOT NULL,
    polled_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    progress        FLOAT,
    stop_number     INTEGER     NOT NULL,
    dist_from_prev  FLOAT,
    line_kmph       FLOAT
);