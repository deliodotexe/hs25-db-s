import csv
from datetime import datetime
from pathlib import Path

# -------------------
# Config
# -------------------
DATE_COLUMN = "Datum"
DATE_FORMAT = "%d/%m/%Y"   # e.g. 31/12/2024
UID_PREFIX = "wt"

# -------------------
# Paths
# -------------------
local_dir = Path(__file__).absolute().parent
input_csv = local_dir / "Wetterdaten.csv"
output_csv = local_dir / "wetterdaten_mysql.csv"

if not input_csv.exists():
    raise FileNotFoundError(f"Input file not found: {input_csv}")

# -------------------
# Process CSV
# -------------------
with input_csv.open("r", newline="", encoding="utf-8") as infile, \
     output_csv.open("w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)

    if DATE_COLUMN not in reader.fieldnames:
        raise ValueError(f"Column '{DATE_COLUMN}' not found in CSV")

    # Build output header
    fieldnames = ["uid", "timestamp"] + [
        col for col in reader.fieldnames if col != DATE_COLUMN
    ]

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    uid_counter = 0
    total = 0
    converted = 0

    for row in reader:
        total += 1
        date_str = row.get(DATE_COLUMN, "").strip()

        try:
            dt = datetime.strptime(date_str, DATE_FORMAT)
            unix_ts = int(dt.timestamp())
        except Exception as e:
            print(f"Skipping row {total}: invalid date '{date_str}' ({e})")
            continue

        # Create UID
        uid = f"{UID_PREFIX}{uid_counter}"
        uid_counter += 1

        # Write row
        out_row = {
            "uid": uid,
            "timestamp": unix_ts,
        }

        for col in reader.fieldnames:
            if col != DATE_COLUMN:
                out_row[col] = row[col]

        writer.writerow(out_row)
        converted += 1

print("\nDone.")
print(f"Total rows processed: {total}")
print(f"Successfully converted: {converted}")
print(f"Output file: {output_csv}")
