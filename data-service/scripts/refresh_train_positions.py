"""
refresh_train_positions.py
    - Rerun and refresh the current_train_positions materialized view

usage:
    python refresh_train_positions.py
"""

import os
import time
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "timescaledb"),
    port=os.getenv("DB_PORT", 5432),
    dbname=os.getenv("POSTGRES_DB", "mtr"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres")
)

cur = conn.cursor()

print("Starting refresh loop...")

while True:
    try:
        with open("/scripts/compute_current_positions.sql", "r") as f:
            query = f.read()
        cur.execute(query)
        conn.commit()
        
        print("Refreshed train positions.")
    
    except Exception as e:
        print(f"Error refreshing: {e}")
        conn.rollback()
    
    time.sleep(10)