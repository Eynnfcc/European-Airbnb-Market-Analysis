from pathlib import Path
import sqlite3
import pandas as pd

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

SILVER_FILE = (
    BASE_DIR
    / "silver_data"
    / "airbnb_silver_master.csv"
)

GOLD_DIR = BASE_DIR / "gold_data"
GOLD_DIR.mkdir(exist_ok=True)

DATABASE_FILE = GOLD_DIR / "airbnb_gold.db"

# --------------------------------------------------
# CHECK SILVER DATA
# --------------------------------------------------

if not SILVER_FILE.exists():
    raise FileNotFoundError(
        "Silver master dataset not found. "
        "Run silverlayer.py first."
    )

print("=" * 70)
print("GOLD LAYER - STAR SCHEMA")
print("=" * 70)

# --------------------------------------------------
# LOAD SILVER MASTER
# --------------------------------------------------

df = pd.read_csv(SILVER_FILE)

print(f"\nSilver rows loaded: {len(df):,}")

# --------------------------------------------------
# DIMENSION 1: CITY
# --------------------------------------------------

dim_city = (
    df[["city"]]
    .drop_duplicates()
    .sort_values("city")
    .reset_index(drop=True)
)

dim_city.insert(
    0,
    "city_id",
    range(1, len(dim_city) + 1)
)

# --------------------------------------------------
# DIMENSION 2: ROOM TYPE
# --------------------------------------------------

dim_room_type = (
    df[["room_type"]]
    .drop_duplicates()
    .sort_values("room_type")
    .reset_index(drop=True)
)

dim_room_type.insert(
    0,
    "room_type_id",
    range(1, len(dim_room_type) + 1)
)

# --------------------------------------------------
# DIMENSION 3: DAY TYPE
# --------------------------------------------------

dim_day_type = (
    df[["day_type"]]
    .drop_duplicates()
    .sort_values("day_type")
    .reset_index(drop=True)
)

dim_day_type.insert(
    0,
    "day_type_id",
    range(1, len(dim_day_type) + 1)
)

# --------------------------------------------------
# ADD DIMENSION KEYS TO FACT DATA
# --------------------------------------------------

fact_df = df.merge(
    dim_city,
    on="city",
    how="left"
)

fact_df = fact_df.merge(
    dim_room_type,
    on="room_type",
    how="left"
)

fact_df = fact_df.merge(
    dim_day_type,
    on="day_type",
    how="left"
)

# --------------------------------------------------
# FACT TABLE COLUMNS
# --------------------------------------------------

fact_columns = [
    "listing_id",
    "city_id",
    "room_type_id",
    "day_type_id",
    "realsum",
    "price_per_person",
    "person_capacity",
    "room_shared",
    "room_private",
    "host_is_superhost",
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

# Only select columns that actually exist
fact_columns = [
    col
    for col in fact_columns
    if col in fact_df.columns
]

fact_airbnb = fact_df[fact_columns].copy()

# --------------------------------------------------
# CREATE SQLITE DATABASE
# --------------------------------------------------

if DATABASE_FILE.exists():
    DATABASE_FILE.unlink()

connection = sqlite3.connect(DATABASE_FILE)

# --------------------------------------------------
# WRITE DIMENSION TABLES
# --------------------------------------------------

dim_city.to_sql(
    "dim_city",
    connection,
    if_exists="replace",
    index=False
)

dim_room_type.to_sql(
    "dim_room_type",
    connection,
    if_exists="replace",
    index=False
)

dim_day_type.to_sql(
    "dim_day_type",
    connection,
    if_exists="replace",
    index=False
)

# --------------------------------------------------
# WRITE FACT TABLE
# --------------------------------------------------

fact_airbnb.to_sql(
    "fact_airbnb",
    connection,
    if_exists="replace",
    index=False
)

# --------------------------------------------------
# CREATE SQL INDEXES
# --------------------------------------------------

cursor = connection.cursor()

cursor.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_city_id
    ON dim_city(city_id)
    """
)

cursor.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_room_type_id
    ON dim_room_type(room_type_id)
    """
)

cursor.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_day_type_id
    ON dim_day_type(day_type_id)
    """
)

cursor.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_listing_id
    ON fact_airbnb(listing_id)
    """
)

cursor.execute(
    """
    CREATE INDEX IF NOT EXISTS
    idx_fact_city
    ON fact_airbnb(city_id)
    """
)

cursor.execute(
    """
    CREATE INDEX IF NOT EXISTS
    idx_fact_room_type
    ON fact_airbnb(room_type_id)
    """
)

cursor.execute(
    """
    CREATE INDEX IF NOT EXISTS
    idx_fact_day_type
    ON fact_airbnb(day_type_id)
    """
)

connection.commit()

# --------------------------------------------------
# CREATE GOLD SUMMARY VIEWS
# --------------------------------------------------

cursor.execute(
    """
    CREATE VIEW IF NOT EXISTS vw_city_price_summary AS

    SELECT
        c.city,
        COUNT(*) AS total_listings,
        ROUND(AVG(f.realsum), 2) AS average_price,
        ROUND(MIN(f.realsum), 2) AS minimum_price,
        ROUND(MAX(f.realsum), 2) AS maximum_price,
        ROUND(
            AVG(f.guest_satisfaction_overall),
            2
        ) AS average_guest_satisfaction

    FROM fact_airbnb f

    JOIN dim_city c
        ON f.city_id = c.city_id

    GROUP BY c.city
    """
)

cursor.execute(
    """
    CREATE VIEW IF NOT EXISTS vw_room_type_summary AS

    SELECT
        r.room_type,
        COUNT(*) AS total_listings,
        ROUND(AVG(f.realsum), 2) AS average_price,
        ROUND(
            AVG(f.cleanliness_rating),
            2
        ) AS average_cleanliness,
        ROUND(
            AVG(f.guest_satisfaction_overall),
            2
        ) AS average_satisfaction

    FROM fact_airbnb f

    JOIN dim_room_type r
        ON f.room_type_id = r.room_type_id

    GROUP BY r.room_type
    """
)

connection.commit()

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\nDimension: City")
print(dim_city)

print("\nDimension: Room Type")
print(dim_room_type)

print("\nDimension: Day Type")
print(dim_day_type)

print("\nFact table:")
print(fact_airbnb.head())

print("\nFact table rows:", len(fact_airbnb))

# --------------------------------------------------
# TEST QUERY
# --------------------------------------------------

query = """
SELECT
    c.city,
    ROUND(AVG(f.realsum), 2) AS average_price,
    COUNT(*) AS listings
FROM fact_airbnb f
JOIN dim_city c
    ON f.city_id = c.city_id
GROUP BY c.city
ORDER BY average_price DESC
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nAverage Airbnb Price by City:")
print(result)

connection.close()

# --------------------------------------------------
# SAVE CSV COPIES FOR EASY INSPECTION
# --------------------------------------------------

dim_city.to_csv(
    GOLD_DIR / "dim_city.csv",
    index=False
)

dim_room_type.to_csv(
    GOLD_DIR / "dim_room_type.csv",
    index=False
)

dim_day_type.to_csv(
    GOLD_DIR / "dim_day_type.csv",
    index=False
)

fact_airbnb.to_csv(
    GOLD_DIR / "fact_airbnb.csv",
    index=False
)

print("\n" + "=" * 70)
print("GOLD LAYER COMPLETE")
print("=" * 70)

print(f"\nSQLite database:")
print(DATABASE_FILE)

print("\nGold CSV tables saved inside:")
print(GOLD_DIR)