-- Install PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create table for absolute progress along Island Line
-- (We will have to refactor this to incorporate other lines)
DROP TABLE IF EXISTS station_progress;

CREATE TABLE station_progress(
    line_code       TEXT    NOT NULL,
    station_code    TEXT    NOT NULL,
    direction       TEXT    NOT NULL,
    stop_number     INTEGER NOT NULL,
    progress        FLOAT   NOT NULL,
    dist_from_prev  FLOAT, -- Distance from previous stop (in km)
    PRIMARY KEY     (line_code, station_code, direction)
);
