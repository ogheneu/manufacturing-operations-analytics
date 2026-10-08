import pandas as pd


# ============================================
# LOAD CLEAN DATA
# ============================================

production = pd.read_csv(
    "data/processed/production_clean.csv"
)

downtime = pd.read_csv(
    "data/processed/downtime_clean.csv"
)

maintenance = pd.read_csv(
    "data/processed/maintenance_clean.csv"
)


# ============================================
# PRODUCTION VALIDATION
# ============================================

print("=" * 50)
print("PRODUCTION DATA QUALITY REPORT")
print("=" * 50)

print(
    "Duplicate production IDs:",
    production["production_id"].duplicated().sum()
)

print(
    "Missing machine IDs:",
    production["machine_id"].isnull().sum()
)

print(
    "Missing product IDs:",
    production["product_id"].isnull().sum()
)

print(
    "Negative downtime:",
    (production["downtime_minutes"] < 0).sum()
)

print(
    "Negative production:",
    (production["units_produced"] < 0).sum()
)


# ============================================
# UNIT CONSISTENCY
# ============================================

unit_errors = (
    production["good_units"] +
    production["defective_units"]
) != production["units_produced"]

print(
    "Production quantity errors:",
    unit_errors.sum()
)


# ============================================
# DOWNTIME VALIDATION
# ============================================

print("\nDOWNTIME DATA")

print(
    "Duplicate downtime IDs:",
    downtime["downtime_id"].duplicated().sum()
)

print(
    "Negative downtime:",
    (downtime["downtime_minutes"] < 0).sum()
)


# ============================================
# MAINTENANCE VALIDATION
# ============================================

print("\nMAINTENANCE DATA")

print(
    "Duplicate maintenance IDs:",
    maintenance["maintenance_id"].duplicated().sum()
)

print(
    "Negative maintenance duration:",
    (
        maintenance["maintenance_duration_minutes"] < 0
    ).sum()
)

print(
    "Negative maintenance cost:",
    (
        maintenance["maintenance_cost"] < 0
    ).sum()
)


print("\nData validation completed.")