from pathlib import Path
import pandas as pd
import shutil

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
BRONZE_DIR = BASE_DIR / "bronze_data"

BRONZE_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# FIND CSV FILES
# --------------------------------------------------

csv_files = sorted(DATASET_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files were found inside: {DATASET_DIR}"
    )

print("=" * 70)
print("BRONZE LAYER - RAW DATA INGESTION")
print("=" * 70)

print(f"\nFound {len(csv_files)} CSV files.\n")

manifest = []

common_columns = None

# --------------------------------------------------
# LOAD EACH RAW FILE
# --------------------------------------------------

for file in csv_files:

    print("-" * 70)
    print(f"Processing: {file.name}")

    # Load raw data without cleaning
    df = pd.read_csv(file)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")
    print(f"Column names: {df.columns.tolist()}")

    # Determine common columns between all files
    current_columns = set(df.columns)

    if common_columns is None:
        common_columns = current_columns
    else:
        common_columns = common_columns.intersection(current_columns)

    # Copy original CSV unchanged into Bronze staging
    destination = BRONZE_DIR / file.name
    shutil.copy2(file, destination)

    manifest.append(
        {
            "file_name": file.name,
            "rows": df.shape[0],
            "columns": df.shape[1],
        }
    )

# --------------------------------------------------
# SAVE BRONZE MANIFEST
# --------------------------------------------------

manifest_df = pd.DataFrame(manifest)

manifest_path = BRONZE_DIR / "bronze_manifest.csv"
manifest_df.to_csv(manifest_path, index=False)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("BRONZE LAYER COMPLETE")
print("=" * 70)

print("\nCommon columns across all CSV files:")

for column in sorted(common_columns):
    print(f" - {column}")

print(f"\nRaw files stored in: {BRONZE_DIR}")
print(f"Manifest saved to: {manifest_path}")

print("\nNo cleaning was performed in the Bronze layer.")