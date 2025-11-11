USE weathercrash;

DROP TABLE IF EXISTS population;

CREATE TABLE IF NOT EXISTS population (
    uid INT NOT NULL AUTO_INCREMENT,
    year INT,
    canton_code VARCHAR(2),
    population_start INT,
    population_end INT,
    PRIMARY KEY (uid)
) ENGINE=InnoDB;

SET GLOBAL local_infile = 1;  -- Enable loading local flies

LOAD DATA LOCAL INFILE './population/population.csv'
INTO TABLE population
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(year, @canton_code, population_start, population_end)
SET canton_code = UPPER(@canton_code);

SET GLOBAL local_infile = 0;  -- Disable loading local flies
