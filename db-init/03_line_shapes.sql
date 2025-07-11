-- Install PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS line_shapes;

-- Create table line_shapes
CREATE TABLE IF NOT EXISTS line_shapes(
    line_code       TEXT,
    direction       TEXT, 
    geom            GEOMETRY(LINESTRING, 4326),
    total_length    FLOAT,
    kmph            FLOAT,
    PRIMARY KEY (line_code, direction)
);

-- Insert values (mainly train speed)
INSERT INTO line_shapes (line_code, direction, geom, total_length, kmph)
VALUES
    ('ISL', 'UP', NULL, 0, 33),
    ('ISL', 'DOWN', NULL, 0, 33),
    ('TWL', 'UP', NULL, 0, 33),
    ('TWL', 'DOWN', NULL, 0, 33)
ON CONFLICT (line_code, direction) DO NOTHING;