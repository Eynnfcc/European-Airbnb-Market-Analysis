from pathlib import Path
import pandas as pd

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

BRONZE_DIR = BASE_DIR / "bronze_data"
SILVER_DIR = BASE_DIR / "silver_data"

SILVER_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = SILVER_DIR / "airbnb_silver_master.csv"
NULL_REPORT_FILE = SILVER_DIR / "null_report.csv"

# --------------------------------------------------
# FIND BRONZE FILES
# --------------------------------------------------

csv_files = sorted(BRONZE_DIR.glob("*.csv"))

# Do not treat the manifest as Airbnb data
csv_files = [
    file for file in csv_files
    if file.name != "bronze_manifest.csv"
]

if not csv_files:
    raise FileNotFoundError(
        "No Bronze CSV files found. Run bronzelayer.py first."
    )

print("=" * 70)
print("SILVER LAYER - CLEANING AND MASTER DATASET")
print("=" * 70)

all_dataframes = []
null_reports = []

# --------------------------------------------------
# PROCESS EVERY CITY FILE
# --------------------------------------------------

for file in csv_files:

    print(f"\nProcessing: {file.name}")

    df = pd.read_csv(file)

    # --------------------------------------------------
    # 1. Remove accidental CSV index columns
    # --------------------------------------------------

    unwanted_columns = [
        col for col in df.columns
        if str(col).lower().startswith("unnamed")
    ]

    if unwanted_columns:
        df = df.drop(columns=unwanted_columns)

    # --------------------------------------------------
    # 2. Clean column names
    # --------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------
    # 3. Extract city and weekday/weekend from filename
    # --------------------------------------------------

    filename = file.stem.lower()

    if filename.endswith("_weekdays"):
        city = filename.replace("_weekdays", "")
        day_type = "Weekday"

    elif filename.endswith("_weekends"):
        city = filename.replace("_weekends", "")
        day_type = "Weekend"

    else:
        city = filename
        day_type = "Unknown"

    city = city.replace("_", " ").title()

    df["city"] = city
    df["day_type"] = day_type
    df["source_file"] = file.name

    # --------------------------------------------------
    # 4. Standardize room type
    # --------------------------------------------------

    if "room_type" in df.columns:
        df["room_type"] = (
            df["room_type"]
            .astype("string")
            .str.strip()
        )

    # --------------------------------------------------
    # 5. Standardize Boolean columns
    # --------------------------------------------------

    boolean_columns = [
        "room_shared",
        "room_private",
        "host_is_superhost",
    ]

    for column in boolean_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.lower()
                .map(
                    {
                        "true": True,
                        "false": False,
                        "1": True,
                        "0": False,
                    }
                )
            )

    # --------------------------------------------------
    # 6. Convert numerical columns
    # --------------------------------------------------

    numerical_columns = [
        "realsum",
        "person_capacity",
        "multi",
        "biz",
        "cleanliness_rating",
        "guest_satisfaction_overall",
        "bedrooms",
        "dist",
        "metro_dist",
        "attr_index",
        "attr_index_norm",
        "rest_index",
        "rest_index_norm",
        "lng",
        "lat",
    ]

    for column in numerical_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # --------------------------------------------------
    # 7. Detect missing values
    # --------------------------------------------------

    null_count = df.isnull().sum()

    for column, count in null_count.items():

        if count > 0:
            null_reports.append(
                {
                    "file": file.name,
                    "column": column,
                    "missing_values": int(count),
                }
            )

    # --------------------------------------------------
    # 8. Remove completely duplicated listings
    # --------------------------------------------------

    rows_before = len(df)

    df = df.drop_duplicates()

    rows_after = len(df)

    duplicates_removed = rows_before - rows_after

    print(f"City: {city}")
    print(f"Day type: {day_type}")
    print(f"Rows: {rows_after}")
    print(f"Duplicates removed: {duplicates_removed}")

    # --------------------------------------------------
    # 9. Remove records without a price
    # --------------------------------------------------

    if "realsum" in df.columns:

        missing_prices = df["realsum"].isna().sum()

        if missing_prices > 0:
            print(
                f"Removing {missing_prices} rows "
                "because price is missing."
            )

            df = df.dropna(subset=["realsum"])

    # --------------------------------------------------
    # 10. Remove impossible/non-positive prices
    # --------------------------------------------------

    if "realsum" in df.columns:

        invalid_prices = (df["realsum"] <= 0).sum()

        if invalid_prices > 0:
            print(
                f"Removing {invalid_prices} "
                "non-positive prices."
            )

            df = df[df["realsum"] > 0]

    # --------------------------------------------------
    # 11. Add useful derived feature
    # --------------------------------------------------

    if (
        "realsum" in df.columns
        and "person_capacity" in df.columns
    ):

        df["price_per_person"] = (
            df["realsum"]
            / df["person_capacity"].replace(0, pd.NA)
        )

    # Add dataframe to master list
    all_dataframes.append(df)

# --------------------------------------------------
# MERGE ALL CITIES
# --------------------------------------------------

master_df = pd.concat(
    all_dataframes,
    ignore_index=True,
    sort=False
)

# --------------------------------------------------
# ADD UNIQUE LISTING ID
# --------------------------------------------------

master_df.insert(
    0,
    "listing_id",
    range(1, len(master_df) + 1)
)

# --------------------------------------------------
# SAVE MASTER DATASET
# --------------------------------------------------

master_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# SAVE NULL REPORT
# --------------------------------------------------

if null_reports:

    null_report_df = pd.DataFrame(null_reports)

else:

    null_report_df = pd.DataFrame(
        columns=[
            "file",
            "column",
            "missing_values",
        ]
    )

null_report_df.to_csv(
    NULL_REPORT_FILE,
    index=False
)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("SILVER LAYER COMPLETE")
print("=" * 70)

print(f"\nTotal rows: {len(master_df):,}")
print(f"Total columns: {len(master_df.columns)}")

print("\nCities:")
print(master_df["city"].value_counts())

print("\nDay Types:")
print(master_df["day_type"].value_counts())

print("\nMissing values in final dataset:")
print(
    master_df
    .isnull()
    .sum()
    .sort_values(ascending=False)
)

print(f"\nMaster dataset saved to:")
print(OUTPUT_FILE)

print(f"\nNull report saved to:")
print(NULL_REPORT_FILE)