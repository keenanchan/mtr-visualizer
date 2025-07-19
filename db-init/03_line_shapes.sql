-- Install PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS line_shapes;

-- Create table line_shapes
CREATE TABLE IF NOT EXISTS line_shapes(
    line_code       TEXT,
    line_name       TEXT,
    direction       TEXT, 
    geom            GEOMETRY(LINESTRING, 4326),
    total_length    FLOAT,
    kmph            FLOAT,
    PRIMARY KEY (line_code, direction)
);

-- Insert values (mainly train speed)
INSERT INTO line_shapes (line_code, line_name, direction, geom, total_length, kmph)
VALUES
    ('ISL', 'Island Line', 'UP', NULL, 0, 40),
    ('ISL', 'Island Line', 'DOWN', NULL, 0, 40),
    ('TWL', 'Tsuen Wan Line', 'UP', NULL, 0, 40),
    ('TWL', 'Tsuen Wan Line', 'DOWN', NULL, 0, 40),
    ('KTL', 'Kwun Tong Line', 'UP', NULL, 0, 40),
    ('KTL', 'Kwun Tong Line', 'DOWN', NULL, 0, 40)
ON CONFLICT (line_code, direction) DO NOTHING;