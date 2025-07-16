-- 1. Populate train_eta_progress staging table
TRUNCATE TABLE train_eta_progress;

INSERT INTO train_eta_progress (line_code, direction, station_code, destination, eta, polled_at, progress, stop_number, dist_from_prev, line_kmph)
SELECT
    r.line_code,
    r.direction,
    r.station_code,
    r.destination,
    r.eta,
    r.polled_at,
    sp.progress,
    sp.stop_number,
    sp.dist_from_prev,
    ls.kmph             AS line_kmph
FROM train_eta_raw r
JOIN station_progress sp
  ON (r.line_code, r.station_code, r.direction) = (sp.line_code, sp.station_code, sp.direction)
JOIN line_shapes ls
  ON (r.line_code, r.direction) = (ls.line_code, ls.direction)
WHERE r.polled_at > now() - interval '10 second' -- keep the table small for demo
      -- cull overly far ETAs (calc. dist > 2.0 * station_dist, after accounting for 45s dwell time)
  AND ls.kmph * 1/3600.0 * GREATEST(EXTRACT(EPOCH from r.eta - now()) - 45, 0.0) <= 1.6 * sp.dist_from_prev;

-- 2. Materialized view: current_train_positions
--  - Interpolates each train's current position along current line
--  - Produces lat/lon so Grafana can plot points
--  - Refresh with REFRESH MATERIALIZED VIEW CONCURRENTLY ...,

-- Drop first if exists
DROP MATERIALIZED VIEW IF EXISTS current_train_positions;

CREATE MATERIALIZED VIEW IF NOT EXISTS current_train_positions AS
WITH cte AS (
    SELECT
        t.line_code,
        t.direction,
        t.destination,
        t.station_code,
        s.station_code      AS prev_station_code,
        t.progress          AS prog_to,
        s.progress          AS prog_from,
        -- t.dist_from_prev,
        -- t.line_kmph,
        t.eta,
        t.polled_at,
        LEAST(1.0, GREATEST(0.0,
            1.0 - EXTRACT(EPOCH from t.eta - now()) / 
            (3600.0 * t.dist_from_prev / t.line_kmph)
        )) AS frac
    FROM train_eta_progress t
    JOIN station_progress s
      ON (t.line_code, t.stop_number - 1, t.direction) = (s.line_code, s.stop_number, s.direction)
)
SELECT
    c.line_code,
    c.direction,
    c.destination,
    c.prog_from + (c.prog_to - c.prog_from) * c.frac    AS progress_now,

    -- Real interpolated point on curved geometry
    ST_Y(point) AS lat,
    ST_X(point) AS lon
FROM cte c
JOIN line_shapes ls
  ON ls.line_code = c.line_code
  AND ls.direction = c.direction
CROSS JOIN LATERAL
    ST_LineInterpolatePoint(ls.geom, c.prog_from + (c.prog_to - c.prog_from) * c.frac) AS point
WITH NO DATA;

-- Index for quick Grafana queries
CREATE INDEX IF NOT EXISTS ON current_train_positions (line_code, direction);

REFRESH MATERIALIZED VIEW current_train_positions;