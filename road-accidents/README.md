# Data

## RoadTrafficAccidentLocations

- Total features: 249735
- Valid accidents: 249730
- Dropped accidents: 5
- Unique accident types: 11
- Unique severity categories: 3
- Unique road types: 6

### accident_types.csv

- **uid**: Short code (e.g., "at0") for the accident type.
- **name_de**: German name.
- **name_fr**: French name.
- **name_it**: Italian name.
- **name_en**: English name.

### severity_categories.csv

- **uid**: Short code (e.g., "as3") for the severity category.
- **name_de**: German name.
- **name_fr**: French name.
- **name_it**: Italian name.
- **name_en**: English name.

### road_types.csv

- **uid**: Short code (e.g., "rt432") for the road type.
- **name_de**: German name.
- **name_fr**: French name.
- **name_it**: Italian name.
- **name_en**: English name.

### accidents.csv

- **accident_type_uid**: Foreign key to accident_types.uid.
- **severity_category_uid**: Foreign key to severity_categories.uid.
- **road_type_uid**: Foreign key to road_types.uid.
- **involving_pedestrian**: "true" if pedestrian involved, else "false".
- **involving_bicycle**: "true" if bicycle involved, else "false".
- **involving_motorcycle**: "true" if motorcycle involved, else "false".
- **longitude**: WGS84 longitude (decimal degrees).
- **latitude**: WGS84 latitude (decimal degrees).
- **swiss_e**: Swiss CHLV95 easting coordinate.
- **swiss_n**: Swiss CHLV95 northing coordinate.
- **canton_code**: Two-letter Swiss canton code (e.g., "GE").
- **municipality_code**: Four-digit Swiss municipality code (e.g., "6621").
- **timestamp**: Unix epoch seconds for the accident's estimated datetime
   (within the hour of the timestamp) (year/month/hour/weekday). Invalid
   entries dropped (5 in total)
