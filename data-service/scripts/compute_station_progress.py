"""
compute_station_progress.py
    - Populate station_progress table with
    - values from station_metadata and line_shapes

usage:
    python compute_station_progress.py
"""
import sys
import os
import psycopg2


def main():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "mtr"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    SQL_TABLE = """
    CREATE TABLE IF NOT EXISTS station_progress (
        line_code       TEXT    NOT NULL,
        station_code    TEXT    NOT NULL,
        direction       TEXT    NOT NULL,
        stop_number     INTEGER NOT NULL,
        progress        FLOAT   NOT NULL,
        dist_from_prev  FLOAT,
        PRIMARY KEY     (line_code, station_code, direction)
    );
    """

    INSERT_SQL = """
    INSERT INTO station_progress (line_code, station_code, direction, stop_number, progress, dist_from_prev)
    WITH cte AS (
      SELECT
          sm.line_code,
          sm.station_code,
          sm.direction,
          ST_LineLocatePoint(ls.geom, ST_SetSRID(ST_MakePoint(sm.lon, sm.lat), 4326)) AS progress,
          ls.total_length
      FROM station_metadata sm
      JOIN line_shapes ls
        ON sm.line_code = ls.line_code AND sm.direction = ls.direction
    )
    SELECT
      line_code,
      station_code,
      direction,
      ROW_NUMBER() OVER w AS stop_number,
      progress,
      (total_length/1000.0) * (progress - LAG(progress, 1) OVER w) AS dist_from_prev
    FROM cte
    WINDOW w AS (PARTITION BY line_code, direction ORDER BY progress)
    """

    UPDATE_SQL = """
    -- Scale station progress for each line_code + direction
    WITH minmax AS (
      SELECT
        line_code,
        direction,
        MIN(progress) AS min_prog,
        MAX(progress) AS max_prog
      FROM station_progress
      GROUP BY line_code, direction
    )
    UPDATE station_progress sp
    SET progress = (sp.progress - mm.min_prog) / NULLIF(mm.max_prog - mm.min_prog, 0)
    FROM minmax mm
    WHERE
      sp.line_code = mm.line_code
      AND sp.direction = mm.direction;
    """

    with conn, conn.cursor() as cur:
        cur.execute(SQL_TABLE)
        cur.execute(INSERT_SQL)
        # cur.execute(UPDATE_SQL)

if __name__ == "__main__":
    main()