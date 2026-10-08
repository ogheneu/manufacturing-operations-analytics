import pandas as pd

# Load processed datasets

production = pd.read_csv(
    "data/processed/production_clean.csv"
)

downtime = pd.read_csv(
    "data/processed/downtime_clean.csv"
)

maintenance = pd.read_csv(
    "data/processed/maintenance_clean.csv"
)

machine_oee = pd.read_csv(
    "data/processed/machine_oee.csv"
)

machine_performance = pd.read_csv(
    "data/processed/machine_performance.csv"
)

# ---------------------------------------------------------
# MACHINE ID FIX
# ---------------------------------------------------------
# machine_performance.csv was saved with machine_id as
# the DataFrame index. When loaded with pandas, this
# appears as an "index" column.
#
# Convert the index values 0-11 back to M-001-M-012.
# ---------------------------------------------------------

if "machine_id" not in machine_performance.columns:

    if "index" in machine_performance.columns:

        machine_performance["machine_id"] = (
            machine_performance["index"]
            .astype(int)
            .apply(lambda x: f"M-{x + 1:03d}")
        )

        machine_performance = machine_performance.drop(
            columns=["index"]
        )

    else:
        machine_performance = machine_performance.reset_index()

        machine_performance["machine_id"] = (
            machine_performance.index
            .astype(int)
            .apply(lambda x: f"M-{x + 1:03d}")
        )


# ---------------------------------------------------------
# Executive KPI summary
# ---------------------------------------------------------

total_units = production["units_produced"].sum()

total_good_units = production["good_units"].sum()

total_defective_units = production[
    "defective_units"
].sum()

defect_rate = (
    total_defective_units
    / total_units
)

total_downtime = downtime[
    "downtime_minutes"
].sum()

average_ideal_cycle = production[
    "ideal_cycle_seconds"
].mean()

average_actual_cycle = production[
    "actual_cycle_seconds"
].mean()

average_cycle_variance = (
    average_actual_cycle
    - average_ideal_cycle
)

SHIFT_MINUTES = 480

planned_production_time = (
    len(production)
    * SHIFT_MINUTES
)

operating_time = (
    planned_production_time
    - total_downtime
)

availability = (
    operating_time
    / planned_production_time
)

ideal_production_time = (
    average_ideal_cycle
    * total_units
    / 60
)

performance = (
    ideal_production_time
    / operating_time
)

quality = (
    total_good_units
    / total_units
)

oee = (
    availability
    * performance
    * quality
)


# ---------------------------------------------------------
# Create KPI summary table
# ---------------------------------------------------------

kpi_summary = pd.DataFrame(
    {
        "KPI": [
            "Total Units Produced",
            "Good Units",
            "Defective Units",
            "Defect Rate (%)",
            "Total Downtime (minutes)",
            "Average Ideal Cycle Time (seconds)",
            "Average Actual Cycle Time (seconds)",
            "Average Cycle Time Variance (seconds)",
            "Availability (%)",
            "Performance (%)",
            "Quality (%)",
            "OEE (%)"
        ],
        "Value": [
            total_units,
            total_good_units,
            total_defective_units,
            defect_rate * 100,
            total_downtime,
            average_ideal_cycle,
            average_actual_cycle,
            average_cycle_variance,
            availability * 100,
            performance * 100,
            quality * 100,
            oee * 100
        ]
    }
)

print("\nEXECUTIVE KPI SUMMARY")
print("---------------------")

print(
    kpi_summary.to_string(index=False)
)


# ---------------------------------------------------------
# Machine dashboard dataset
# ---------------------------------------------------------

machine_dashboard = machine_performance[
    [
        "machine_id",
        "total_units",
        "downtime_minutes",
        "availability_pct",
        "performance_pct",
        "quality_pct",
        "oee_pct",
        "cycle_time_variance",
        "maintenance_events"
    ]
].copy()

machine_dashboard = (
    machine_dashboard
    .sort_values(
        "machine_id"
    )
    .reset_index(drop=True)
)

print("\nMACHINE DASHBOARD DATA")
print("----------------------")

print(
    machine_dashboard.sort_values(
        "oee_pct"
    )
)


# ---------------------------------------------------------
# Shift quality dashboard dataset
# ---------------------------------------------------------

shift_dashboard = (
    production.groupby("shift_id")
    .agg(
        total_units=("units_produced", "sum"),
        good_units=("good_units", "sum"),
        defective_units=("defective_units", "sum")
    )
)

shift_dashboard["defect_rate_pct"] = (
    shift_dashboard["defective_units"]
    / shift_dashboard["total_units"]
    * 100
)

shift_dashboard = (
    shift_dashboard
    .reset_index()
)

print("\nSHIFT QUALITY DASHBOARD DATA")
print("----------------------------")

print(shift_dashboard)


# ---------------------------------------------------------
# Downtime dashboard dataset
# ---------------------------------------------------------

downtime_dashboard = (
    downtime.groupby("downtime_reason")
    .agg(
        downtime_minutes=(
            "downtime_minutes",
            "sum"
        )
    )
    .reset_index()
)

downtime_dashboard[
    "downtime_pct"
] = (
    downtime_dashboard[
        "downtime_minutes"
    ]
    / downtime_dashboard[
        "downtime_minutes"
    ].sum()
    * 100
)

downtime_dashboard = (
    downtime_dashboard
    .sort_values(
        "downtime_minutes",
        ascending=False
    )
)

print("\nDOWNTIME DASHBOARD DATA")
print("-----------------------")

print(downtime_dashboard)


# ---------------------------------------------------------
# Maintenance dashboard dataset
# ---------------------------------------------------------

maintenance_dashboard = (
    maintenance.groupby("machine_id")
    .agg(
        maintenance_events=(
            "maintenance_id",
            "count"
        ),
        maintenance_downtime=(
            "maintenance_duration_minutes",
            "sum"
        )
    )
    .reset_index()
)

print("\nMAINTENANCE DASHBOARD DATA")
print("--------------------------")

print(maintenance_dashboard)


# ---------------------------------------------------------
# Machine priority dataset
# ---------------------------------------------------------

machine_priority = (
    machine_dashboard
    .sort_values(
        "oee_pct"
    )
    .head(5)
    .reset_index(drop=True)
)

print("\nTOP 5 MACHINES REQUIRING ATTENTION")
print("----------------------------------")

print(machine_priority)


# ---------------------------------------------------------
# Save dashboard datasets
# ---------------------------------------------------------

kpi_summary.to_csv(
    "data/processed/kpi_summary.csv",
    index=False
)

machine_dashboard.to_csv(
    "data/processed/machine_dashboard.csv",
    index=False
)

shift_dashboard.to_csv(
    "data/processed/shift_dashboard.csv",
    index=False
)

downtime_dashboard.to_csv(
    "data/processed/downtime_dashboard.csv",
    index=False
)

maintenance_dashboard.to_csv(
    "data/processed/maintenance_dashboard.csv",
    index=False
)

machine_priority.to_csv(
    "data/processed/machine_priority.csv",
    index=False
)

print(
    "\nDashboard datasets created successfully."
)
