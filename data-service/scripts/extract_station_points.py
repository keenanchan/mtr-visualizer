"""
extract_station_points.py
    - Read a GeoJSON with Point features
    - Match each point to the closest reference station (<=300m)
    - Upsert a station_metadata table in TimescaleDB/PostGIS

usage:
    python extract_station_points.py island_line_raw.geojson

requirements:
    pip install shapely psycopg2-binary haversine
"""

import json
import sys
import os
from pathlib import Path
from shapely.geometry import shape, Point
from haversine import haversine, Unit
import psycopg2


REF_STATIONS = {
    'ISL': [
        ('KET', 'Kennedy Town', 22.2815, 114.1289),
        ('HKU', 'HKU', 22.2844, 114.1351),
        ('SYP', 'Sai Ying Pun', 22.2860, 114.1426),
        ('SHW', 'Sheung Wan', 22.2870, 114.1516),
        ('CEN', 'Central', 22.2819, 114.1582),
        ('ADM', 'Admiralty', 22.2795, 114.1646),
        ('WAC', 'Wan Chai', 22.2778, 114.1732),
        ('CAB', 'Causeway Bay', 22.2808, 114.1850),
        ('TIH', 'Tin Hau', 22.2828, 114.1917),
        ('FOH', 'Fortress Hill', 22.2884, 114.1937),
        ('NOP', 'North Point', 22.2914, 114.2007),
        ('QUB', 'Quarry Bay', 22.2882, 114.2099),
        ('TAK', 'Tai Koo', 22.2851, 114.2166),
        ('SWH', 'Sai Wan Ho', 22.2825, 114.2220),
        ('SKW', 'Shau Kei Wan', 22.2795, 114.2289),
        ('HFC', 'Heng Fa Chuen', 22.2772, 114.2400),
        ('CHW', 'Chai Wan', 22.2650, 114.2374)
    ],
    'TWL': [
        ('CEN', 'Central', 22.2819, 114.1582),
        ('ADM', 'Admiralty', 22.2795, 114.1646),
        ('TST', 'Tsim Sha Tsui', 22.2981, 114.1722),
        ('JOR', 'Jordan', 22.3051, 114.1715),
        ('YMT', 'Yau Ma Tei', 22.3132, 114.1707),
        ('MOK', 'Mong Kok', 22.3195, 114.1694),
        ('PRE', 'Prince Edward', 22.3255, 114.1684),
        ('SSP', 'Sham Shui Po', 22.3313, 114.1622),
        ('CSW', 'Cheung Sha Wan', 22.3362, 114.1561),
        ('LCK', 'Lai Chi Kok', 22.3375, 114.1480),
        ('MEF', 'Mei Foo', 22.3378, 114.1379),
        ('LAK', 'Lai King', 22.3489, 114.1262),
        ('KWF', 'Kwai Fong', 22.3571, 114.1279),
        ('KWH', 'Kwai Hing', 22.3635, 114.1313),
        ('TWH', 'Tai Wo Hau', 22.3712, 114.1251),
        ('TSW', 'Tsuen Wan', 22.3739, 114.1176)
    ]
}

# Max Haversine threshold (metres) to match a platform to a station
MAX_DIST_M = 300


def extract_direction(props, line_code):
    try:
        if line_code == "ISL": # TODO: refactor. This can lead to tech-debt
            return props["@relations"][0]["reltags"]["direction:official_ref:en"].upper()
        elif line_code == "TWL":
            if "northbound" in props["@relations"][0]["reltags"]["name:en"].lower():
                return "UP"
            elif "southbound" in props["@relations"][0]["reltags"]["name:en"].lower():
                return "DOWN"
            else:
                return None
    except (KeyError, IndexError, TypeError):
        return None
    
def extract_line_code(props):
    try:
        return props["@relations"][0]["reltags"]["ref"].upper()
    except (KeyError, IndexError, TypeError):
        return None

def match_to_station(pt: Point, l: str):
    """Return (station_code station_name) of nearest station within threshold."""
    lat, lon = pt.y, pt.x # GeoJSON stores in lon/lat order
    
    best_code, best_name, best_d = None, None, float("inf")
    for code, name, ref_lat, ref_lon in REF_STATIONS[l]:
        d = haversine((lat, lon), (ref_lat, ref_lon), unit=Unit.METERS)
        if d < best_d:
            best_code, best_name, best_d = code, name, d
    if best_d <= MAX_DIST_M:
        return best_code, best_name, best_d
    return None, None, None


def main(geojson_file: str):
    geojson_path = Path(geojson_file)
    if not geojson_path.exists():
        sys.exit(f"GeoJSON file not found: {geojson_file}")

    """Yield a shapely Point (lat, lon) for every Point feature in file."""
    with geojson_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    
    rows = []
    for feat in data.get("features", []):
        geom = shape(feat["geometry"])
        if geom.geom_type != "Point":
            continue # lon/lat order in GeoJSON
        # Else, proceed

        line = extract_line_code(feat.get("properties", {}))
        if not line: continue

        direction = extract_direction(feat.get("properties", {}), line)
        if direction not in ("UP", "DOWN"):
            continue

        scode, sname, dist = match_to_station(geom, line)
        if scode:
            rows.append((line, scode, direction, sname, geom.y, geom.x, geom.x, geom.y)) # lat, lon
        else:
            print(f"Unmatched point at ({geom.y:.5f}, {geom.x:.5f})")
    
    if not rows:
        sys.exit("No station points matched - aborting.")

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "mtr"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    DELETE_SQL = "DELETE FROM station_metadata WHERE line_code = %s AND station_code = %s AND direction = 'BOTH';"

    INSERT_SQL = """
    INSERT INTO station_metadata (line_code, station_code, direction, station_name, lat, lon, geom)
    VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    ON CONFLICT (line_code, station_code, direction) DO UPDATE
      SET lat = EXCLUDED.lat,
          lon = EXCLUDED.lon;
    """

    with conn, conn.cursor() as cur:
        # Step 1: delete 'BOTH' rows for any station getting new directional info
        # station_codes = {(lcode, scode) for lcode, scode, _, _, _, _, _, _ in rows}
        # for lcode, scode in station_codes:
            # cur.execute(DELETE_SQL, (lcode, scode,))

        # Step 2: Insert direction platform rows
        for row in rows:
            cur.execute(INSERT_SQL, row)
    
    print(f"Upserted {len(rows)} stations into station_metadata.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python extract_station_points.py <island_line.geojson>")
    main(sys.argv[1])