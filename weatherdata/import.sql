CREATE TABLE IF NOT EXISTS weathercrash.weatherdata (
	uid VARCHAR(10) PRIMARY KEY,
    timestamp BIGINT,
    aesch_bl_temp_avg DECIMAL(5,2),
    aesch_bl_precipitation_intensity DECIMAL(5,2),
    amburnex_temp_avg DECIMAL(5,2),
    amburnex_precipitation_intensity DECIMAL(5,2),
    anieres_temp_avg DECIMAL(5,2),
    anieres_precipitation_intensity DECIMAL(5,2),
    antagnes_temp_avg DECIMAL(5,2),
    antagnes_precipitation_intensity DECIMAL(5,2),
    arth_temp_avg DECIMAL(5,2),
    arth_precipitation_intensity DECIMAL(5,2),
    aubonne_temp_avg DECIMAL(5,2),
    aubonne_precipitation_intensity DECIMAL(5,2),
    baar_temp_avg DECIMAL(5,2),
    baar_precipitation_intensity DECIMAL(5,2),
    bad_ragaz_temp_avg DECIMAL(5,2),
    bad_ragaz_precipitation_intensity DECIMAL(5,2),
    begnins_temp_avg DECIMAL(5,2),
    begnins_precipitation_intensity DECIMAL(5,2),
    berg_temp_avg DECIMAL(5,2),
    berg_precipitation_intensity DECIMAL(5,2),
    berneck_feuerbrand_temp_avg DECIMAL(5,2),
    berneck_feuerbrand_precipitation_intensity DECIMAL(5,2),
    berneck_indermaur_temp_avg DECIMAL(5,2),
    berneck_indermaur_precipitation_intensity DECIMAL(5,2),
    bernex_temp_avg DECIMAL(5,2),
    bernex_precipitation_intensity DECIMAL(5,2),
    bex_temp_avg DECIMAL(5,2),
    bex_precipitation_intensity DECIMAL(5,2)
) ENGINE=InnoDB;

SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'weatherdata/wetterdaten_mysql.csv'
INTO TABLE weather_data
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(uid, timestamp, aesch_bl_temp_avg, aesch_bl_precipitation_intensity, amburnex_temp_avg, amburnex_precipitation_intensity, anieres_temp_avg, anieres_precipitation_intensity, antagnes_temp_avg, antagnes_precipitation_intensity, arth_temp_avg, arth_precipitation_intensity, aubonne_temp_avg, aubonne_precipitation_intensity, baar_temp_avg, baar_precipitation_intensity, bad_ragaz_temp_avg, bad_ragaz_precipitation_intensity, begnins_temp_avg, begnins_precipitation_intensity, berg_temp_avg, berg_precipitation_intensity, berneck_feuerbrand_temp_avg, berneck_feuerbrand_precipitation_intensity, berneck_indermaur_temp_avg, berneck_indermaur_precipitation_intensity, bernex_temp_avg, bernex_precipitation_intensity, bex_temp_avg, bex_precipitation_intensity)