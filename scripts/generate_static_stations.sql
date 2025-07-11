SELECT jsonb_pretty(jsonb_build_object(
	'type', 'FeatureCollection',
	'features', jsonb_agg(jsonb_build_object(
		'type', 'Feature',
		'geometry', jsonb_build_object(
			'type', 'Point',
			'coordinates', jsonb_build_array(lon, lat) -- GeoJSON gives coords in (lon, lat)
		),
		'properties', jsonb_build_object(
			'station_code', station_code,
			'station_name', station_name,
			'direction', direction
		)
	))
))
FROM station_metadata;