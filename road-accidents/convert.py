import calendar
import csv
import json
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Load data
local_dir = Path(__file__).absolute().parent
accident_json = local_dir / "RoadTrafficAccidentLocations.json"
data = json.loads(accident_json.read_text())
features = data["features"]
total = len(features)

# Collect unique types
accident_types = defaultdict(lambda: {"de": "", "fr": "", "it": "", "en": ""})
severity_categories = defaultdict(lambda: {"de": "", "fr": "", "it": "", "en": ""})
road_types = defaultdict(lambda: {"de": "", "fr": "", "it": "", "en": ""})

# Weekday map
weekday_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

# Process features for types
for i, feature in enumerate(features):
    if i % 1000 == 0:
        sys.stdout.write(f"\rProcessed {i}/{total} features for types")
        sys.stdout.flush()
    props = feature["properties"]
    # Accident type
    at = props["AccidentType"]
    accident_types[at]["de"] = props.get("AccidentType_de", "")
    accident_types[at]["fr"] = props.get("AccidentType_fr", "")
    accident_types[at]["it"] = props.get("AccidentType_it", "")
    accident_types[at]["en"] = props.get("AccidentType_en", "")
    # Severity
    sc = props["AccidentSeverityCategory"]
    severity_categories[sc]["de"] = props.get("AccidentSeverityCategory_de", "")
    severity_categories[sc]["fr"] = props.get("AccidentSeverityCategory_fr", "")
    severity_categories[sc]["it"] = props.get("AccidentSeverityCategory_it", "")
    severity_categories[sc]["en"] = props.get("AccidentSeverityCategory_en", "")
    # Road type
    rt = props["RoadType"]
    road_types[rt]["de"] = props.get("RoadType_de", "")
    road_types[rt]["fr"] = props.get("RoadType_fr", "")
    road_types[rt]["it"] = props.get("RoadType_it", "")
    road_types[rt]["en"] = props.get("RoadType_en", "")

print()  # Newline after progress


# Write types CSVs
def write_type_csv(path: Path, types_dict: dict[str, str]):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["uid", "name_de", "name_fr", "name_it", "name_en"])
        for uid, names in sorted(types_dict.items()):
            writer.writerow([uid, names["de"], names["fr"], names["it"], names["en"]])


accidents_path = local_dir / "accidents.csv"
accident_types_path = local_dir / "accident_types.csv"
severity_categories_path = local_dir / "severity_categories.csv"
road_types_path = local_dir / "road_types.csv"
write_type_csv(accident_types_path, accident_types)
write_type_csv(severity_categories_path, severity_categories)
write_type_csv(road_types_path, road_types)

# Now main accidents CSV
dropped_count = 0
valid_count = 0
with accidents_path.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "accident_type_uid",
            "severity_category_uid",
            "road_type_uid",
            "involving_pedestrian",
            "involving_bicycle",
            "involving_motorcycle",
            "longitude",
            "latitude",
            "swiss_e",
            "swiss_n",
            "canton_code",
            "municipality_code",
            "timestamp",
        ]
    )
    for i, feature in enumerate(features):
        if i % 1000 == 0:
            sys.stdout.write(f"\rProcessed {i}/{total} features for main data")
            sys.stdout.flush()
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        longi, lati = coords[0], coords[1]
        swiss_e = props.get("AccidentLocation_CHLV95_E", "")
        swiss_n = props.get("AccidentLocation_CHLV95_N", "")
        canton = props.get("CantonCode", "")
        muni = props.get("MunicipalityCode", "")
        year_str = props.get("AccidentYear", "")
        month_str = props.get("AccidentMonth", "")
        weekday_en = props.get("AccidentWeekDay_en", "")
        hour_str = props.get("AccidentHour", "")

        # Check for issues
        issues = []
        try:
            year = int(year_str)
        except (ValueError, TypeError):
            year = None
            issues.append(f"Invalid year: {year_str}")
        try:
            month = int(month_str)
        except (ValueError, TypeError):
            month = None
            issues.append(f"Invalid month: {month_str}")
        if not hour_str or not hour_str.isdigit():
            hour = None
            issues.append(f"Invalid hour: {hour_str}")
        else:
            hour = int(hour_str)
        dow = weekday_map.get(weekday_en)
        if dow is None:
            issues.append(f"Invalid weekday: {weekday_en}")
        # Compute timestamp (epoch)
        if year is None or month is None or hour is None or dow is None:
            timestamp = ""
        else:
            try:
                days_in_month = calendar.monthrange(year, month)[1]
                date_found = None
                for day in range(1, days_in_month + 1):
                    if calendar.weekday(year, month, day) == dow:
                        date_found = datetime(year, month, day, hour, 0, 0)
                        break
                if date_found:
                    timestamp = str(int(date_found.timestamp()))
                else:
                    timestamp = ""
                    issues.append("No date found matching weekday")
            except ValueError as e:
                timestamp = ""
                issues.append(f"Date computation error: {e}")
        if issues:
            dropped_count += 1
            continue
        valid_count += 1
        writer.writerow(
            [
                props["AccidentType"],
                props["AccidentSeverityCategory"],
                props["RoadType"],
                props.get("AccidentInvolvingPedestrian", ""),
                props.get("AccidentInvolvingBicycle", ""),
                props.get("AccidentInvolvingMotorcycle", ""),
                longi,
                lati,
                swiss_e,
                swiss_n,
                canton,
                muni,
                timestamp,
            ]
        )

print(
    f"\nDone. Dropped {dropped_count} entries. CSVs: accident_types.csv, severity_categories.csv, road_types.csv, accidents.csv"
)

# Statistics
print("\nStatistics:")
print(f"Total features: {total}")
print(f"Valid accidents: {valid_count}")
print(f"Dropped accidents: {dropped_count}")
print(f"Unique accident types: {len(accident_types)}")
print(f"Unique severity categories: {len(severity_categories)}")
print(f"Unique road types: {len(road_types)}")
