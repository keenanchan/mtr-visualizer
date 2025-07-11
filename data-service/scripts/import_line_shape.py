"""
import_line_shape.py - Import line geoJSON file into line_shapes table

usage:
    python import_line_shape.py cleaned_line_file.geojson
requirements:
    pip install shapely geojson psycopg2-binary
"""

import sys
import os
import json
import psycopg2
from pathlib import Path
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer

def main(inp):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "mtr"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    with open(inp, "r") as f:
        data = json.load(f)
    
    INSERT_SQL = """
    INSERT INTO line_shapes (line_code, direction, geom, total_length)
    VALUES (%s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326), %s)
    ON CONFLICT (line_code, direction) DO UPDATE
        SET geom = EXCLUDED.geom,
            total_length = EXCLUDED.total_length;
    """

    # transforms WGS84 to projected CRS (HK 1980 Grid System)
    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:2326",
        always_xy=True
    )

    with conn, conn.cursor() as cur:
        for feature in data['features']:
            geom = shape(feature['geometry'])
            line_code = feature['properties']['line_code']
            direction = feature['properties']['direction']

            if geom.geom_type != "LineString":
                raise ValueError("Expected a LineString geometry.")
            
            total_length = transform(transformer.transform, geom).length

            cur.execute(INSERT_SQL, (line_code, direction, geom.wkt, total_length))

    line_name = data['features'][0]['properties']['line_name']
    print(f"Upserted {len(data['features'])} LineStrings for {line_name} into line_shapes table.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python import_line_shape.py <input.geojson>")
    
    main(Path(sys.argv[1]))