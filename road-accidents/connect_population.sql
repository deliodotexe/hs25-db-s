ALTER TABLE accidents
ADD COLUMN population_uid INT,
ADD FOREIGN KEY (population_uid) REFERENCES population(uid);


UPDATE accidents a
SET population_uid = (
    SELECT p.uid
    FROM population p
    WHERE p.canton_code = a.canton_code
    AND p.year = YEAR(FROM_UNIXTIME(a.timestamp))
);