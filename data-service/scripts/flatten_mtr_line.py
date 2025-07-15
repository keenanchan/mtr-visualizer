"""
flatten_mtr_line.py - Merge all LineString / MultiLineString segments
                      of a route into one ordered LineString.

usage:
    python flatten_mtr_line.py input.geojson output.geojson
requirements:
    pip install shapely geojson
"""

import sys, json
from pathlib import Path
from shapely.geometry import (
    shape,
    LineString,
    mapping,
)
from shapely.ops import linemerge
from shapely import wkt
from math import hypot

GAP_THRESHOLD_METERS = 5000 # A jump of this length (5km) signifies a cut in the line. TODO: handling for Disneyland (2 stops)
DEG_TO_METERS = 111000 # 1 deg in meters


def flatten_to_linestring(geom):
    """
    Recursively collect coords from any geometry into a list
    of LineString coord tuples (ordered).
    """
    if geom.geom_type == "LineString":
        return [list(geom.coords)]
    if geom.geom_type == "MultiLineString":
        return [list(g.coords) for g in geom.geoms]
    if geom.geom_type == "GeometryCollection":
        coords = []
        for g in geom.geoms:
            coords.extend(flatten_to_linestring(g))
        return coords
    if geom.geom_type == "Point":
        print(f"Skipping Point geometry: {geom.wkt}")
        return []
    raise ValueError(f"Unsupported geometry type: {geom.geom_type}")


def split_by_gap(coords):
    jump_idx = None

    for i in range(1, len(coords)):
        # rough planar distance in degrees, ok for jump detection
        dx = coords[i][0] - coords[i-1][0]
        dy = coords[i][1] - coords[i-1][1]
        dist_deg = (dx*dx + dy*dy) ** 0.5

        # convert deg to m (1 deg ~ 111km)
        if dist_deg * DEG_TO_METERS > GAP_THRESHOLD_METERS:
            jump_idx = i
            break
    
    if jump_idx is None:
        sys.exit("Could not find a gap in loop. Adjust threshold?")
    
    down_coords = coords[:jump_idx]     # Direction DOWN.
    up_coords = coords[jump_idx:][::-1] # Direction UP.

    return LineString(down_coords), LineString(up_coords)


# TODO: this is nearly duplicated in extract_station_points.
# Consider moving into a utils.py file?
def extract_line_code(data):
    try:
        return data["features"][0]["properties"]["ref"].upper()
    except (KeyError, IndexError, TypeError):
        return None


def main(inp, outp):
    with open(inp, "r", encoding="utf-8") as f:
        data = json.load(f)

    line_code = extract_line_code(data)
    
    # Collect all coord seqs, preserving order
    segments = []
    for feat in data.get("features", []):
        geom = shape(feat["geometry"])
        segments.extend(flatten_to_linestring(geom))

    # Concat segments in original file order
    flat_coords = []
    for seg in segments:
        # Don't duplicate vertices between consecutive segments
        if flat_coords and flat_coords[-1] == seg[0]:
            flat_coords.extend(seg[1:])
        else:
            flat_coords.extend(seg)
    
    # At this point we have a full line.
    down, up = split_by_gap(flat_coords)

    lookup = {
        "ISL": "Island Line",
        "TWL": "Tsuen Wan Line",
        "KTL": "Kwun Tong Line"
    }

    # Wrap as a simple FeatureCollection to view/load easily
    # TODO: Refactor. Tech debt!!!
    cleaned_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "line_name": lookup[line_code],
                    "line_code": line_code,
                    "direction": "DOWN"},
                "geometry": mapping(down)
            },
            {
                "type": "Feature",
                "properties": {
                    "line_name": lookup[line_code],
                    "line_code": line_code,
                    "direction": "UP"},
                "geometry": mapping(up)
            },
        ]
    }

    with open(outp, "w", encoding="utf-8") as f:
        json.dump(cleaned_geojson, f, indent=2)
    print(f"Wrote cleaned LineStrings to {outp}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python flatten_mtr_line.py <input.geojson> <output.geojson>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))