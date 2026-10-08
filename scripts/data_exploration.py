import pandas as pd

# Load the datasets

production = pd.read_csv("data/raw/production_raw.csv")
downtime = pd.read_csv("data/raw/downtime_raw.csv")
maintenance = pd.read_csv("data/raw/maintenance_raw.csv")
machines = pd.read_csv("data/raw/machines.csv")
products = pd.read_csv("data/raw/products.csv")
shifts = pd.read_csv("data/raw/shifts.csv")
operators = pd.read_csv("data/raw/operators.csv")


# Display the first five rows of each major dataset

print("PRODUCTION DATA")
print(production.head())

print("\nDOWNTIME DATA")
print(downtime.head())

print("\nMAINTENANCE DATA")
print(maintenance.head())

print("\nDATASET SHAPES")

print("Production:", production.shape)

print("Downtime:", downtime.shape)

print("Maintenance:", maintenance.shape)

print("\nPRODUCTION DATA TYPES")

print(production.info())
print("\nMISSING VALUES")

print(production.isnull().sum())
print("\nDUPLICATE ROWS")

print(production.duplicated().sum())
print("\nDUPLICATE PRODUCTION IDs")

print(production["production_id"].duplicated().sum())