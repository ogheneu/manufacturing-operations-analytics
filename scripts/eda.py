import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load cleaned datasets

production = pd.read_csv("data/processed/production_clean.csv")
downtime = pd.read_csv("data/processed/downtime_clean.csv")
maintenance = pd.read_csv("data/processed/maintenance_clean.csv")

# Check dataset sizes

print("PRODUCTION SHAPE:")
print(production.shape)

print("\nDOWNTIME SHAPE:")
print(downtime.shape)

print("\nMAINTENANCE SHAPE:")
print(maintenance.shape)

# Production summary

total_units = production["units_produced"].sum()
total_good_units = production["good_units"].sum()
total_defective_units = production["defective_units"].sum()

defect_rate = (
    total_defective_units / total_units
) * 100

print("\nPRODUCTION SUMMARY")
print("------------------")
print(f"Total units produced: {total_units:,}")
print(f"Total good units: {total_good_units:,}")
print(f"Total defective units: {total_defective_units:,}")
print(f"Overall defect rate: {defect_rate:.2f}%")

# Downtime analysis

total_downtime = downtime["downtime_minutes"].sum()
average_downtime = downtime["downtime_minutes"].mean()

print("\nDOWNTIME SUMMARY")
print("----------------")
print(f"Total downtime: {total_downtime:,.1f} minutes")
print(f"Average downtime event: {average_downtime:.1f} minutes")

# Downtime by machine

downtime_by_machine = (
    downtime.groupby("machine_id")["downtime_minutes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOP 10 MACHINES BY DOWNTIME")
print("---------------------------")
print(downtime_by_machine.head(10))

# Downtime by reason

downtime_by_reason = (
    downtime.groupby("downtime_reason")["downtime_minutes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nDOWNTIME BY REASON")
print("------------------")
print(downtime_by_reason)

# Production by shift

production_by_shift = (
    production.groupby("shift_id")
    .agg(
        units_produced=("units_produced", "sum"),
        good_units=("good_units", "sum"),
        defective_units=("defective_units", "sum")
    )
)

production_by_shift["defect_rate"] = (
    production_by_shift["defective_units"]
    / production_by_shift["units_produced"]
) * 100

print("\nPRODUCTION BY SHIFT")
print("-------------------")
print(production_by_shift)

# Cycle time analysis

production["cycle_time_variance"] = (
    production["actual_cycle_seconds"]
    - production["ideal_cycle_seconds"]
)

average_ideal_cycle = production["ideal_cycle_seconds"].mean()
average_actual_cycle = production["actual_cycle_seconds"].mean()

print("\nCYCLE TIME SUMMARY")
print("------------------")
print(f"Average ideal cycle time: {average_ideal_cycle:.2f} seconds")
print(f"Average actual cycle time: {average_actual_cycle:.2f} seconds")
print(
    f"Average cycle time variance: "
    f"{production['cycle_time_variance'].mean():.2f} seconds"
)

# Average cycle time by machine

cycle_time_by_machine = (
    production.groupby("machine_id")
    .agg(
        ideal_cycle_time=("ideal_cycle_seconds", "mean"),
        actual_cycle_time=("actual_cycle_seconds", "mean")
    )
)

cycle_time_by_machine["variance"] = (
    cycle_time_by_machine["actual_cycle_time"]
    - cycle_time_by_machine["ideal_cycle_time"]
)

cycle_time_by_machine = cycle_time_by_machine.sort_values(
    "variance",
    ascending=False
)

print("\nMACHINES WITH HIGHEST CYCLE TIME VARIANCE")
print("-----------------------------------------")
print(cycle_time_by_machine.head(10))

# Save analysis results

downtime_by_machine.to_csv(
    "data/processed/downtime_by_machine.csv"
)

downtime_by_reason.to_csv(
    "data/processed/downtime_by_reason.csv"
)

production_by_shift.to_csv(
    "data/processed/production_by_shift.csv"
)

cycle_time_by_machine.to_csv(
    "data/processed/cycle_time_by_machine.csv"
)

print("\nEDA analysis completed successfully.")

