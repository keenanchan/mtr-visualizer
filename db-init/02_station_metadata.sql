-- Install PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create table for station metadata (e.g. location)
CREATE TABLE IF NOT EXISTS station_metadata (
    line_code       TEXT NOT NULL,
    station_code    TEXT NOT NULL,
    direction       TEXT NOT NULL,
    station_name    TEXT NOT NULL,
    lat             FLOAT NOT NULL,
    lon             FLOAT NOT NULL,
    geom            GEOMETRY(POINT, 4326),
    PRIMARY KEY     (line_code, station_code, direction)
);

-- Index on line_code for faster filtering
CREATE INDEX idx_station_metadata_line_code ON station_metadata (line_code);

-- Insert values
INSERT INTO station_metadata (line_code, station_code, direction, station_name, lat, lon, geom)
VALUES
    ('ISL', 'KET', 'UP', 'Kennedy Town',       22.2815, 114.1289, ST_SetSRID(ST_MakePoint(22.2815, 114.1289), 4326)),
    ('ISL', 'HKU', 'UP', 'HKU',                22.2844, 114.1351, ST_SetSRID(ST_MakePoint(22.2844, 114.1351), 4326)),
    ('ISL', 'SYP', 'UP', 'Sai Ying Pun',       22.2860, 114.1426, ST_SetSRID(ST_MakePoint(22.2860, 114.1426), 4326)),
    ('ISL', 'SHW', 'UP', 'Sheung Wan',         22.2870, 114.1516, ST_SetSRID(ST_MakePoint(22.2870, 114.1516), 4326)),
    ('ISL', 'CEN', 'UP', 'Central',            22.2819, 114.1582, ST_SetSRID(ST_MakePoint(22.2819, 114.1582), 4326)),
    ('ISL', 'ADM', 'UP', 'Admiralty',          22.2795, 114.1646, ST_SetSRID(ST_MakePoint(22.2795, 114.1646), 4326)),
    ('ISL', 'WAC', 'UP', 'Wan Chai',           22.2778, 114.1732, ST_SetSRID(ST_MakePoint(22.2778, 114.1732), 4326)),
    ('ISL', 'CAB', 'UP', 'Causeway Bay',       22.2808, 114.1850, ST_SetSRID(ST_MakePoint(22.2808, 114.1850), 4326)),
    ('ISL', 'TIH', 'UP', 'Tin Hau',            22.2828, 114.1917, ST_SetSRID(ST_MakePoint(22.2828, 114.1917), 4326)),
    ('ISL', 'FOH', 'UP', 'Fortress Hill',      22.2884, 114.1937, ST_SetSRID(ST_MakePoint(22.2884, 114.1937), 4326)),
    ('ISL', 'NOP', 'UP', 'North Point',        22.2914, 114.2007, ST_SetSRID(ST_MakePoint(22.2914, 114.2007), 4326)),
    ('ISL', 'QUB', 'UP', 'Quarry Bay',         22.2882, 114.2099, ST_SetSRID(ST_MakePoint(22.2882, 114.2099), 4326)),
    ('ISL', 'TAK', 'UP', 'Tai Koo',            22.2851, 114.2166, ST_SetSRID(ST_MakePoint(22.2851, 114.2166), 4326)),
    ('ISL', 'SWH', 'UP', 'Sai Wan Ho',         22.2825, 114.2220, ST_SetSRID(ST_MakePoint(22.2825, 114.2220), 4326)),
    ('ISL', 'SKW', 'UP', 'Shau Kei Wan',       22.2795, 114.2289, ST_SetSRID(ST_MakePoint(22.2795, 114.2289), 4326)),
    ('ISL', 'HFC', 'UP', 'Heng Fa Chuen',      22.2772, 114.2400, ST_SetSRID(ST_MakePoint(22.2772, 114.2400), 4326)),
    ('ISL', 'CHW', 'UP', 'Chai Wan',           22.2650, 114.2374, ST_SetSRID(ST_MakePoint(22.2650, 114.2374), 4326)),
    ('TWL', 'CEN', 'UP', 'Central',            22.2819, 114.1582, ST_SetSRID(ST_MakePoint(22.2819, 114.1582), 4326)),
    ('TWL', 'ADM', 'UP', 'Admiralty',          22.2795, 114.1646, ST_SetSRID(ST_MakePoint(22.2795, 114.1646), 4326)),
    ('TWL', 'TST', 'UP', 'Tsim Sha Tsui',      22.2981, 114.1722, ST_SetSRID(ST_MakePoint(22.2981, 114.1722), 4326)),
    ('TWL', 'JOR', 'UP', 'Jordan',             22.3051, 114.1715, ST_SetSRID(ST_MakePoint(22.3051, 114.1715), 4326)),
    ('TWL', 'YMT', 'UP', 'Yau Ma Tei',         22.3132, 114.1707, ST_SetSRID(ST_MakePoint(22.3132, 114.1707), 4326)),
    ('TWL', 'MOK', 'UP', 'Mong Kok',           22.3195, 114.1694, ST_SetSRID(ST_MakePoint(22.3195, 114.1694), 4326)),
    ('TWL', 'PRE', 'UP', 'Prince Edward',      22.3255, 114.1684, ST_SetSRID(ST_MakePoint(22.3255, 114.1684), 4326)),
    ('TWL', 'SSP', 'UP', 'Sham Shui Po',       22.3313, 114.1622, ST_SetSRID(ST_MakePoint(22.3313, 114.1622), 4326)),
    ('TWL', 'CSW', 'UP', 'Cheung Sha Wan',     22.3362, 114.1561, ST_SetSRID(ST_MakePoint(22.3362, 114.1561), 4326)),
    ('TWL', 'LCK', 'UP', 'Lai Chi Kok',        22.3375, 114.1480, ST_SetSRID(ST_MakePoint(22.3375, 114.1480), 4326)),
    ('TWL', 'MEF', 'UP', 'Mei Foo',            22.3378, 114.1379, ST_SetSRID(ST_MakePoint(22.3378, 114.1379), 4326)),
    ('TWL', 'LAK', 'UP', 'Lai King',           22.3489, 114.1262, ST_SetSRID(ST_MakePoint(22.3489, 114.1262), 4326)),
    ('TWL', 'KWF', 'UP', 'Kwai Fong',          22.3571, 114.1279, ST_SetSRID(ST_MakePoint(22.3571, 114.1279), 4326)),
    ('TWL', 'KWH', 'UP', 'Kwai Hing',          22.3635, 114.1313, ST_SetSRID(ST_MakePoint(22.3635, 114.1313), 4326)),
    ('TWL', 'TWH', 'UP', 'Tai Wo Hau',         22.3712, 114.1251, ST_SetSRID(ST_MakePoint(22.3712, 114.1251), 4326)),
    ('TWL', 'TSW', 'UP', 'Tsuen Wan',          22.3739, 114.1176, ST_SetSRID(ST_MakePoint(22.3739, 114.1176), 4326)),
    ('KTL', 'WHA', 'UP', 'Whampoa',            22.3055, 114.1895, ST_SetSRID(ST_MakePoint(22.3055, 114.1895), 4326)),
    ('KTL', 'HOM', 'UP', 'Ho Man Tin',         22.3100, 114.1827, ST_SetSRID(ST_MakePoint(22.3100, 114.1827), 4326)),
    ('KTL', 'YMT', 'UP', 'Yau Ma Tei',         22.3132, 114.1707, ST_SetSRID(ST_MakePoint(22.3132, 114.1707), 4326)),
    ('KTL', 'MOK', 'UP', 'Mong Kok',           22.3195, 114.1694, ST_SetSRID(ST_MakePoint(22.3195, 114.1694), 4326)),
    ('KTL', 'PRE', 'UP', 'Prince Edward',      22.3255, 114.1684, ST_SetSRID(ST_MakePoint(22.3255, 114.1684), 4326)),
    ('KTL', 'SKM', 'UP', 'Shek Kip Mei',       22.3328, 114.1690, ST_SetSRID(ST_MakePoint(22.3328, 114.1690), 4326)),
    ('KTL', 'KOT', 'UP', 'Kowloon Tong',       22.3376, 114.1760, ST_SetSRID(ST_MakePoint(22.3376, 114.1760), 4326)),
    ('KTL', 'LOF', 'UP', 'Lok Fu',             22.3387, 114.1870, ST_SetSRID(ST_MakePoint(22.3387, 114.1870), 4326)),
    ('KTL', 'WTS', 'UP', 'Wong Tai Sin',       22.3418, 114.1939, ST_SetSRID(ST_MakePoint(22.3418, 114.1939), 4326)),
    ('KTL', 'DIH', 'UP', 'Diamond Hill',       22.3402, 114.2017, ST_SetSRID(ST_MakePoint(22.3402, 114.2017), 4326)),
    ('KTL', 'CHH', 'UP', 'Choi Hung',          22.3352, 114.2090, ST_SetSRID(ST_MakePoint(22.3352, 114.2090), 4326)),
    ('KTL', 'KOB', 'UP', 'Kowloon Bay',        22.3236, 114.2138, ST_SetSRID(ST_MakePoint(22.3236, 114.2138), 4326)),
    ('KTL', 'NTK', 'UP', 'Ngau Tau Kok',       22.3160, 114.2191, ST_SetSRID(ST_MakePoint(22.3160, 114.2191), 4326)),
    ('KTL', 'KWT', 'UP', 'Kwun Tong',          22.3124, 114.2264, ST_SetSRID(ST_MakePoint(22.3124, 114.2264), 4326)),
    ('KTL', 'LAT', 'UP', 'Lam Tin',            22.3071, 114.2327, ST_SetSRID(ST_MakePoint(22.3071, 114.2327), 4326)),
    ('KTL', 'YAT', 'UP', 'Yau Tong',           22.2986, 114.2371, ST_SetSRID(ST_MakePoint(22.2986, 114.2371), 4326)),
    ('KTL', 'TIK', 'UP', 'Tiu Keng Leng',      22.3049, 114.2528, ST_SetSRID(ST_MakePoint(22.3049, 114.2528), 4326)),
    ('ISL', 'KET', 'DOWN', 'Kennedy Town',     22.2815, 114.1289, ST_SetSRID(ST_MakePoint(22.2815, 114.1289), 4326)),
    ('ISL', 'HKU', 'DOWN', 'HKU',              22.2844, 114.1351, ST_SetSRID(ST_MakePoint(22.2844, 114.1351), 4326)),
    ('ISL', 'SYP', 'DOWN', 'Sai Ying Pun',     22.2860, 114.1426, ST_SetSRID(ST_MakePoint(22.2860, 114.1426), 4326)),
    ('ISL', 'SHW', 'DOWN', 'Sheung Wan',       22.2870, 114.1516, ST_SetSRID(ST_MakePoint(22.2870, 114.1516), 4326)),
    ('ISL', 'CEN', 'DOWN', 'Central',          22.2819, 114.1582, ST_SetSRID(ST_MakePoint(22.2819, 114.1582), 4326)),
    ('ISL', 'ADM', 'DOWN', 'Admiralty',        22.2795, 114.1646, ST_SetSRID(ST_MakePoint(22.2795, 114.1646), 4326)),
    ('ISL', 'WAC', 'DOWN', 'Wan Chai',         22.2778, 114.1732, ST_SetSRID(ST_MakePoint(22.2778, 114.1732), 4326)),
    ('ISL', 'CAB', 'DOWN', 'Causeway Bay',     22.2808, 114.1850, ST_SetSRID(ST_MakePoint(22.2808, 114.1850), 4326)),
    ('ISL', 'TIH', 'DOWN', 'Tin Hau',          22.2828, 114.1917, ST_SetSRID(ST_MakePoint(22.2828, 114.1917), 4326)),
    ('ISL', 'FOH', 'DOWN', 'Fortress Hill',    22.2884, 114.1937, ST_SetSRID(ST_MakePoint(22.2884, 114.1937), 4326)),
    ('ISL', 'NOP', 'DOWN', 'North Point',      22.2914, 114.2007, ST_SetSRID(ST_MakePoint(22.2914, 114.2007), 4326)),
    ('ISL', 'QUB', 'DOWN', 'Quarry Bay',       22.2882, 114.2099, ST_SetSRID(ST_MakePoint(22.2882, 114.2099), 4326)),
    ('ISL', 'TAK', 'DOWN', 'Tai Koo',          22.2851, 114.2166, ST_SetSRID(ST_MakePoint(22.2851, 114.2166), 4326)),
    ('ISL', 'SWH', 'DOWN', 'Sai Wan Ho',       22.2825, 114.2220, ST_SetSRID(ST_MakePoint(22.2825, 114.2220), 4326)),
    ('ISL', 'SKW', 'DOWN', 'Shau Kei Wan',     22.2795, 114.2289, ST_SetSRID(ST_MakePoint(22.2795, 114.2289), 4326)),
    ('ISL', 'HFC', 'DOWN', 'Heng Fa Chuen',    22.2772, 114.2400, ST_SetSRID(ST_MakePoint(22.2772, 114.2400), 4326)),
    ('ISL', 'CHW', 'DOWN', 'Chai Wan',         22.2650, 114.2374, ST_SetSRID(ST_MakePoint(22.2650, 114.2374), 4326)),
    ('TWL', 'CEN', 'DOWN', 'Central',          22.2819, 114.1582, ST_SetSRID(ST_MakePoint(22.2819, 114.1582), 4326)),
    ('TWL', 'ADM', 'DOWN', 'Admiralty',        22.2795, 114.1646, ST_SetSRID(ST_MakePoint(22.2795, 114.1646), 4326)),
    ('TWL', 'TST', 'DOWN', 'Tsim Sha Tsui',    22.2981, 114.1722, ST_SetSRID(ST_MakePoint(22.2981, 114.1722), 4326)),
    ('TWL', 'JOR', 'DOWN', 'Jordan',           22.3051, 114.1715, ST_SetSRID(ST_MakePoint(22.3051, 114.1715), 4326)),
    ('TWL', 'YMT', 'DOWN', 'Yau Ma Tei',       22.3132, 114.1707, ST_SetSRID(ST_MakePoint(22.3132, 114.1707), 4326)),
    ('TWL', 'MOK', 'DOWN', 'Mong Kok',         22.3195, 114.1694, ST_SetSRID(ST_MakePoint(22.3195, 114.1694), 4326)),
    ('TWL', 'PRE', 'DOWN', 'Prince Edward',    22.3255, 114.1684, ST_SetSRID(ST_MakePoint(22.3255, 114.1684), 4326)),
    ('TWL', 'SSP', 'DOWN', 'Sham Shui Po',     22.3313, 114.1622, ST_SetSRID(ST_MakePoint(22.3313, 114.1622), 4326)),
    ('TWL', 'CSW', 'DOWN', 'Cheung Sha Wan',   22.3362, 114.1561, ST_SetSRID(ST_MakePoint(22.3362, 114.1561), 4326)),
    ('TWL', 'LCK', 'DOWN', 'Lai Chi Kok',      22.3375, 114.1480, ST_SetSRID(ST_MakePoint(22.3375, 114.1480), 4326)),
    ('TWL', 'MEF', 'DOWN', 'Mei Foo',          22.3378, 114.1379, ST_SetSRID(ST_MakePoint(22.3378, 114.1379), 4326)),
    ('TWL', 'LAK', 'DOWN', 'Lai King',         22.3489, 114.1262, ST_SetSRID(ST_MakePoint(22.3489, 114.1262), 4326)),
    ('TWL', 'KWF', 'DOWN', 'Kwai Fong',        22.3571, 114.1279, ST_SetSRID(ST_MakePoint(22.3571, 114.1279), 4326)),
    ('TWL', 'KWH', 'DOWN', 'Kwai Hing',        22.3635, 114.1313, ST_SetSRID(ST_MakePoint(22.3635, 114.1313), 4326)),
    ('TWL', 'TWH', 'DOWN', 'Tai Wo Hau',       22.3712, 114.1251, ST_SetSRID(ST_MakePoint(22.3712, 114.1251), 4326)),
    ('TWL', 'TSW', 'DOWN', 'Tsuen Wan',        22.3739, 114.1176, ST_SetSRID(ST_MakePoint(22.3739, 114.1176), 4326)),
    ('KTL', 'WHA', 'DOWN', 'Whampoa',          22.3055, 114.1895, ST_SetSRID(ST_MakePoint(22.3055, 114.1895), 4326)),
    ('KTL', 'HOM', 'DOWN', 'Ho Man Tin',       22.3100, 114.1827, ST_SetSRID(ST_MakePoint(22.3100, 114.1827), 4326)),
    ('KTL', 'YMT', 'DOWN', 'Yau Ma Tei',       22.3132, 114.1707, ST_SetSRID(ST_MakePoint(22.3132, 114.1707), 4326)),
    ('KTL', 'MOK', 'DOWN', 'Mong Kok',         22.3195, 114.1694, ST_SetSRID(ST_MakePoint(22.3195, 114.1694), 4326)),
    ('KTL', 'PRE', 'DOWN', 'Prince Edward',    22.3255, 114.1684, ST_SetSRID(ST_MakePoint(22.3255, 114.1684), 4326)),
    ('KTL', 'SKM', 'DOWN', 'Shek Kip Mei',     22.3328, 114.1690, ST_SetSRID(ST_MakePoint(22.3328, 114.1690), 4326)),
    ('KTL', 'KOT', 'DOWN', 'Kowloon Tong',     22.3376, 114.1760, ST_SetSRID(ST_MakePoint(22.3376, 114.1760), 4326)),
    ('KTL', 'LOF', 'DOWN', 'Lok Fu',           22.3387, 114.1870, ST_SetSRID(ST_MakePoint(22.3387, 114.1870), 4326)),
    ('KTL', 'WTS', 'DOWN', 'Wong Tai Sin',     22.3418, 114.1939, ST_SetSRID(ST_MakePoint(22.3418, 114.1939), 4326)),
    ('KTL', 'DIH', 'DOWN', 'Diamond Hill',     22.3402, 114.2017, ST_SetSRID(ST_MakePoint(22.3402, 114.2017), 4326)),
    ('KTL', 'CHH', 'DOWN', 'Choi Hung',        22.3352, 114.2090, ST_SetSRID(ST_MakePoint(22.3352, 114.2090), 4326)),
    ('KTL', 'KOB', 'DOWN', 'Kowloon Bay',      22.3236, 114.2138, ST_SetSRID(ST_MakePoint(22.3236, 114.2138), 4326)),
    ('KTL', 'NTK', 'DOWN', 'Ngau Tau Kok',     22.3160, 114.2191, ST_SetSRID(ST_MakePoint(22.3160, 114.2191), 4326)),
    ('KTL', 'KWT', 'DOWN', 'Kwun Tong',        22.3124, 114.2264, ST_SetSRID(ST_MakePoint(22.3124, 114.2264), 4326)),
    ('KTL', 'LAT', 'DOWN', 'Lam Tin',          22.3071, 114.2327, ST_SetSRID(ST_MakePoint(22.3071, 114.2327), 4326)),
    ('KTL', 'YAT', 'DOWN', 'Yau Tong',         22.2986, 114.2371, ST_SetSRID(ST_MakePoint(22.2986, 114.2371), 4326)),
    ('KTL', 'TIK', 'DOWN', 'Tiu Keng Leng',   22.3049, 114.2528, ST_SetSRID(ST_MakePoint(22.3049, 114.2528), 4326))
ON CONFLICT (line_code, station_code, direction) DO NOTHING;