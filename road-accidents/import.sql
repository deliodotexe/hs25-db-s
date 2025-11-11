-- Assume database 'weathercrash' selected.
USE weathercrash;

-- Create tables (if not exists)
CREATE TABLE IF NOT EXISTS accident_types (
    uid VARCHAR(10) PRIMARY KEY,
    name_de VARCHAR(255),
    name_fr VARCHAR(255),
    name_it VARCHAR(255),
    name_en VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS severity_categories (
    uid VARCHAR(10) PRIMARY KEY,
    name_de VARCHAR(255),
    name_fr VARCHAR(255),
    name_it VARCHAR(255),
    name_en VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS road_types (
    uid VARCHAR(10) PRIMARY KEY,
    name_de VARCHAR(255),
    name_fr VARCHAR(255),
    name_it VARCHAR(255),
    name_en VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS accidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    accident_type_uid VARCHAR(10),
    severity_category_uid VARCHAR(10),
    road_type_uid VARCHAR(10),
    involving_pedestrian BOOLEAN,
    involving_bicycle BOOLEAN,
    involving_motorcycle BOOLEAN,
    longitude DECIMAL(10,8),
    latitude DECIMAL(10,8),
    swiss_e VARCHAR(10),
    swiss_n VARCHAR(10),
    canton_code VARCHAR(2),
    municipality_code VARCHAR(4),
    timestamp BIGINT,
    FOREIGN KEY (accident_type_uid) REFERENCES accident_types(uid),
    FOREIGN KEY (severity_category_uid) REFERENCES severity_categories(uid),
    FOREIGN KEY (road_type_uid) REFERENCES road_types(uid),
    INDEX idx_timestamp (timestamp),
    INDEX idx_coords (longitude, latitude)
) ENGINE=InnoDB;

-- Load data (use LOCAL for client-side files)
SET GLOBAL local_infile = 1;  -- Enable loading local files

LOAD DATA LOCAL INFILE 'road-accidents/accident_types.csv'
INTO TABLE accident_types
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(uid, name_de, name_fr, name_it, name_en);

LOAD DATA LOCAL INFILE 'road-accidents/severity_categories.csv'
INTO TABLE severity_categories
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(uid, name_de, name_fr, name_it, name_en);

LOAD DATA LOCAL INFILE 'road-accidents/road_types.csv'
INTO TABLE road_types
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(uid, name_de, name_fr, name_it, name_en);

LOAD DATA LOCAL INFILE 'road-accidents/accidents.csv'
INTO TABLE accidents
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(accident_type_uid, severity_category_uid, road_type_uid, @ped, @bic, @mot, longitude, latitude, swiss_e, swiss_n, canton_code, municipality_code, @timestamp)
SET
    involving_pedestrian = (@ped = 'true'),
    involving_bicycle = (@bic = 'true'),
    involving_motorcycle = (@mot = 'true'),
    timestamp = NULLIF(@timestamp, '');

SET GLOBAL local_infile = 0;  -- Disable loading local flies
