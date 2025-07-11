#!/bin/bash
set -e

echo "Waiting until Postgres is ready..."

# Loop until the DB responds
until pg_isready -h timescaledb -p 5432 -U postgres; do
  echo "Postgres is not ready yet..."
  sleep 0.5
done

echo "Postgres is ready. Running extract_station_points.py..."

# Run python script populating station_metadata
for file in /geojson/raw/*; do
  python3 /scripts/extract_station_points.py "$file"
done

echo "Done extracting station points."
echo "Running flatten_mtr_line.py..."

# Run python script flattening MTR lines
for file in /geojson/raw/*; do
  filename=$(basename "$file")
  python3 /scripts/flatten_mtr_line.py "$file" /geojson/cleaned/"$filename"
done

echo "Done flattening MTR lines."
echo "Running import_line_shape.py..."

# Run python script importing flattened MTR lines
for file in /geojson/cleaned/*; do
  python3 /scripts/import_line_shape.py "$file"
done

echo "Done importing line shape."
echo "Computing station progress..."

# Run SQL script computing station progress
python3 /scripts/compute_station_progress.py

echo "Station progress computed."
echo "Entering into MV loop..."

# Enter materialized view loop
python3 /scripts/refresh_train_positions.py