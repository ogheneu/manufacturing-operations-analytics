import pandas as pd


# ============================================
# LOAD RAW PRODUCTION DATA
# ============================================

production = pd.read_csv("data/raw/production_raw.csv")

print(production.head())
df = production.copy()
print("Raw production data loaded successfully.")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["product_id"] = (
    df["product_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["machine_id"] = (
    df["machine_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["line_id"] = (
    df["line_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["shift_id"] = (
    df["shift_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["operator_id"] = (
    df["operator_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

print("\nMISSING VALUES BEFORE CLEANING")

print(df.isnull().sum())
df["operator_id"] = df["operator_id"].fillna("UNKNOWN")
print("\nMISSING VALUES AFTER OPERATOR CLEANING")

print(df["operator_id"].isnull().sum())

duplicate_ids = df["production_id"].duplicated().sum()

print("\nDUPLICATE PRODUCTION IDs:")
print(duplicate_ids)

df = df.drop_duplicates(
    subset="production_id",
    keep="first"
)
print("\nDUPLICATE PRODUCTION IDs AFTER CLEANING:")

print(df["production_id"].duplicated().sum())

df["calculated_total"] = (
    df["good_units"] + df["defective_units"]
)
invalid_units = df[
    df["calculated_total"] != df["units_produced"]
]

print("\nINVALID PRODUCTION QUANTITIES:")
print(len(invalid_units))
df = df.drop(columns=["calculated_total"])
invalid_defects = df[
    df["defective_units"] > df["units_produced"]
]

print("\nRECORDS WHERE DEFECTS EXCEED TOTAL PRODUCTION:")
print(len(invalid_defects))

invalid_good_units = df[
    df["good_units"] > df["units_produced"]
]

print("\nRECORDS WHERE GOOD UNITS EXCEED TOTAL PRODUCTION:")
print(len(invalid_good_units))

negative_downtime = df[
    df["downtime_minutes"] < 0
]

print("\nNEGATIVE DOWNTIME RECORDS:")
print(len(negative_downtime))

negative_planned = df[
    df["planned_minutes"] < 0
]

print("\nNEGATIVE PLANNED TIME RECORDS:")
print(len(negative_planned))

df["operating_minutes"] = (
    df["planned_minutes"] - df["downtime_minutes"]
).clip(lower=0)

df["defect_rate"] = (
    df["defective_units"] /
    df["units_produced"]
)

df["quality_rate"] = (
    df["good_units"] /
    df["units_produced"]
)

df["throughput_per_hour"] = (
    df["good_units"] /
    (df["operating_minutes"] / 60)
)

print("\nCLEANED DATA")
print(df.head())
print("\nCLEANED DATA SHAPE")
print(df.shape)
print("\nFINAL MISSING VALUES")
print(df.isnull().sum())

df.to_csv(
    "data/processed/production_clean.csv",
    index=False
)
print("\nCleaned production dataset saved successfully.")