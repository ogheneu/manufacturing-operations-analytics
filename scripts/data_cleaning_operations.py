import pandas as pd


# ============================================
# LOAD DATA
# ============================================

downtime = pd.read_csv(
    "data/raw/downtime_raw.csv"
)

maintenance = pd.read_csv(
    "data/raw/maintenance_raw.csv"
)


# ============================================
# CLEAN DOWNTIME DATA
# ============================================

downtime["date"] = pd.to_datetime(
    downtime["date"],
    errors="coerce"
)

downtime["machine_id"] = (
    downtime["machine_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

downtime["line_id"] = (
    downtime["line_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

downtime["shift_id"] = (
    downtime["shift_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

downtime["downtime_reason"] = (
    downtime["downtime_reason"]
    .astype("string")
    .str.strip()
)

downtime["downtime_minutes"] = (
    pd.to_numeric(
        downtime["downtime_minutes"],
        errors="coerce"
    )
)

downtime = downtime.drop_duplicates(
    subset="downtime_id"
)

downtime = downtime[
    downtime["downtime_minutes"] >= 0
]


# ============================================
# CLEAN MAINTENANCE DATA
# ============================================

maintenance["date"] = pd.to_datetime(
    maintenance["date"],
    errors="coerce"
)

maintenance["machine_id"] = (
    maintenance["machine_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

maintenance["maintenance_type"] = (
    maintenance["maintenance_type"]
    .astype("string")
    .str.strip()
)

maintenance["maintenance_duration_minutes"] = (
    pd.to_numeric(
        maintenance["maintenance_duration_minutes"],
        errors="coerce"
    )
)

maintenance["maintenance_cost"] = (
    pd.to_numeric(
        maintenance["maintenance_cost"],
        errors="coerce"
    )
)

maintenance = maintenance.drop_duplicates(
    subset="maintenance_id"
)

maintenance = maintenance[
    maintenance["maintenance_duration_minutes"] >= 0
]

maintenance = maintenance[
    maintenance["maintenance_cost"] >= 0
]


# ============================================
# SAVE CLEAN DATA
# ============================================

downtime.to_csv(
    "data/processed/downtime_clean.csv",
    index=False
)

maintenance.to_csv(
    "data/processed/maintenance_clean.csv",
    index=False
)


# ============================================
# REPORT
# ============================================

print("Downtime records:", len(downtime))

print("Maintenance records:", len(maintenance))

print("\nDowntime missing values:")
print(downtime.isnull().sum())

print("\nMaintenance missing values:")
print(maintenance.isnull().sum())

print("\nClean operational datasets saved successfully.")