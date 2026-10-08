import pandas as pd

# Load cleaned datasets

production = pd.read_csv("data/processed/production_clean.csv")
downtime = pd.read_csv("data/processed/downtime_clean.csv")
maintenance = pd.read_csv(
    "data/processed/maintenance_clean.csv"
)

# Total production

total_units = production["units_produced"].sum()
total_good_units = production["good_units"].sum()

print("PRODUCTION TOTALS")
print("-----------------")
print(f"Total units produced: {total_units:,}")
print(f"Total good units: {total_good_units:,}")

# Quality

quality = total_good_units / total_units

print("\nQUALITY")
print("-------")
print(f"Quality: {quality:.4f}")
print(f"Quality percentage: {quality * 100:.2f}%")

# Planned production time

SHIFT_MINUTES = 480

number_of_records = len(production)

planned_production_time = (
    number_of_records * SHIFT_MINUTES
)

print("\nPLANNED PRODUCTION TIME")
print("-----------------------")
print(
    f"Planned production time: "
    f"{planned_production_time:,.0f} minutes"
)

# Total downtime

total_downtime = downtime["downtime_minutes"].sum()

print("\nDOWNTIME")
print("--------")
print(f"Total downtime: {total_downtime:,.1f} minutes")

# Operating time

operating_time = planned_production_time - total_downtime

print("\nOPERATING TIME")
print("--------------")
print(f"Operating time: {operating_time:,.1f} minutes")

# Availability

availability = operating_time / planned_production_time

print("\nAVAILABILITY")
print("------------")
print(f"Availability: {availability:.4f}")
print(f"Availability percentage: {availability * 100:.2f}%")

# Performance calculation

average_ideal_cycle_seconds = production["ideal_cycle_seconds"].mean()

ideal_production_time_seconds = (
    average_ideal_cycle_seconds * total_units
)

ideal_production_time_minutes = (
    ideal_production_time_seconds / 60
)

print("\nPERFORMANCE CALCULATION")
print("----------------------")
print(
    f"Average ideal cycle time: "
    f"{average_ideal_cycle_seconds:.2f} seconds"
)

print(
    f"Ideal production time: "
    f"{ideal_production_time_minutes:,.1f} minutes"
)

# Performance

performance = (
    ideal_production_time_minutes
    / operating_time
)

print(
    f"Performance: {performance:.4f}"
)

print(
    f"Performance percentage: "
    f"{performance * 100:.2f}%"
)

# Overall Equipment Effectiveness

oee = (
    availability
    * performance
    * quality
)

print("\nOVERALL EQUIPMENT EFFECTIVENESS (OEE)")
print("------------------------------------")
print(f"OEE: {oee:.4f}")
print(f"OEE percentage: {oee * 100:.2f}%")

# OEE by machine

machine_oee = (
    production.groupby("machine_id")
    .agg(
        total_units=("units_produced", "sum"),
        good_units=("good_units", "sum"),
        average_ideal_cycle_seconds=("ideal_cycle_seconds", "mean")
    )
)

machine_oee["quality"] = (
    machine_oee["good_units"]
    / machine_oee["total_units"]
)

# Downtime by machine

machine_downtime = (
    downtime.groupby("machine_id")["downtime_minutes"]
    .sum()
)

machine_oee["downtime_minutes"] = (
    machine_downtime
)

machine_oee["downtime_minutes"] = (
    machine_oee["downtime_minutes"].fillna(0)
)

# Planned production time by machine

machine_record_count = (
    production.groupby("machine_id")
    .size()
)

machine_oee["planned_time_minutes"] = (
    machine_record_count * SHIFT_MINUTES
)

# Machine availability

machine_oee["operating_time_minutes"] = (
    machine_oee["planned_time_minutes"]
    - machine_oee["downtime_minutes"]
)

machine_oee["availability"] = (
    machine_oee["operating_time_minutes"]
    / machine_oee["planned_time_minutes"]
)

# Machine performance

machine_oee["ideal_production_time_minutes"] = (
    machine_oee["average_ideal_cycle_seconds"]
    * machine_oee["total_units"]
    / 60
)

machine_oee["performance"] = (
    machine_oee["ideal_production_time_minutes"]
    / machine_oee["operating_time_minutes"]
)

# Machine OEE

machine_oee["oee"] = (
    machine_oee["availability"]
    * machine_oee["performance"]
    * machine_oee["quality"]
)
machine_oee["availability_pct"] = (
    machine_oee["availability"] * 100
)

machine_oee["performance_pct"] = (
    machine_oee["performance"] * 100
)

machine_oee["quality_pct"] = (
    machine_oee["quality"] * 100
)

machine_oee["oee_pct"] = (
    machine_oee["oee"] * 100
)

print("\nOEE BY MACHINE")
print("--------------")

print(
    machine_oee[
        [
            "total_units",
            "downtime_minutes",
            "availability_pct",
            "performance_pct",
            "quality_pct",
            "oee_pct"
        ]
    ]
    .sort_values("oee_pct")
)

print("\nBOTTOM 5 MACHINES BY OEE")
print("------------------------")

print(
    machine_oee[
        [
            "availability_pct",
            "performance_pct",
            "quality_pct",
            "oee_pct"
        ]
    ]
    .sort_values("oee_pct")
    .head(5)
)

# Save machine OEE results

machine_oee.to_csv(
    "data/processed/machine_oee.csv"
)

print("\nOEE calculation completed successfully.")

# Downtime analysis by machine

downtime_by_machine = (
    downtime.groupby("machine_id")["downtime_minutes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nDOWNTIME BY MACHINE")
print("-------------------")

print(downtime_by_machine)

# Downtime analysis by reason

downtime_by_reason = (
    downtime.groupby("downtime_reason")["downtime_minutes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nDOWNTIME BY REASON")
print("------------------")

print(downtime_by_reason)
# Downtime percentage by reason

downtime_reason_pct = (
    downtime_by_reason
    / downtime_by_reason.sum()
    * 100
)

print("\nDOWNTIME PERCENTAGE BY REASON")
print("-----------------------------")

print(
    downtime_reason_pct.round(2)
)

# Defect analysis by shift

shift_quality = (
    production.groupby("shift_id")
    .agg(
        total_units=("units_produced", "sum"),
        good_units=("good_units", "sum"),
        defective_units=("defective_units", "sum")
    )
)

shift_quality["defect_rate"] = (
    shift_quality["defective_units"]
    / shift_quality["total_units"]
)

shift_quality["defect_rate_pct"] = (
    shift_quality["defect_rate"] * 100
)

print("\nQUALITY BY SHIFT")
print("----------------")

print(
    shift_quality[
        [
            "total_units",
            "good_units",
            "defective_units",
            "defect_rate_pct"
        ]
    ]
)

# Cycle time analysis by machine

cycle_time_analysis = (
    production.groupby("machine_id")
    .agg(
        ideal_cycle_time=("ideal_cycle_seconds", "mean"),
        actual_cycle_time=("actual_cycle_seconds", "mean")
    )
)

cycle_time_analysis["cycle_time_variance"] = (
    cycle_time_analysis["actual_cycle_time"]
    - cycle_time_analysis["ideal_cycle_time"]
)

cycle_time_analysis = (
    cycle_time_analysis
    .sort_values(
        "cycle_time_variance",
        ascending=False
    )
)

print("\nCYCLE TIME VARIANCE BY MACHINE")
print("------------------------------")

print(cycle_time_analysis)

# Maintenance analysis by machine

maintenance_by_machine = (
    maintenance.groupby("machine_id")
    .agg(
        maintenance_events=("maintenance_id", "count"),
        maintenance_downtime=("maintenance_duration_minutes", "sum")
    )
    .sort_values(
        "maintenance_events",
        ascending=False
    )
)

print("\nMAINTENANCE BY MACHINE")
print("----------------------")

print(maintenance_by_machine)

# Combined machine performance analysis

machine_performance = machine_oee[
    [
        "total_units",
        "downtime_minutes",
        "availability_pct",
        "performance_pct",
        "quality_pct",
        "oee_pct"
    ]
].copy()

machine_performance = machine_performance.join(
    cycle_time_analysis[
        ["cycle_time_variance"]
    ]
)

machine_performance = machine_performance.join(
    maintenance_by_machine[
        ["maintenance_events"]
    ]
)

print("\nCOMBINED MACHINE PERFORMANCE")
print("----------------------------")

print(
    machine_performance
    .sort_values("oee_pct")
)
# Identify machines requiring attention

priority_machines = (
    machine_performance
    .sort_values("oee_pct")
    .head(5)
)

print("\nMACHINES REQUIRING ATTENTION")
print("----------------------------")

print(priority_machines)

# Save analysis results

downtime_by_machine.to_csv(
    "data/processed/downtime_by_machine.csv"
)

downtime_by_reason.to_csv(
    "data/processed/downtime_by_reason.csv"
)

shift_quality.to_csv(
    "data/processed/quality_by_shift.csv"
)

cycle_time_analysis.to_csv(
    "data/processed/cycle_time_analysis.csv"
)

maintenance_by_machine.to_csv(
    "data/processed/maintenance_by_machine.csv"
)

machine_performance.to_csv(
    "data/processed/machine_performance.csv"
)

priority_machines.to_csv(
    "data/processed/priority_machines.csv"
)

print("\nPerformance driver analysis completed successfully.")

# OEE vs cycle time variance

oee_cycle_analysis = machine_performance[
    [
        "oee_pct",
        "cycle_time_variance"
    ]
].copy()

oee_cycle_correlation = (
    oee_cycle_analysis[
        "oee_pct"
    ].corr(
        oee_cycle_analysis[
            "cycle_time_variance"
        ]
    )
)

print("\nOEE VS CYCLE TIME VARIANCE")
print("--------------------------")

print(
    f"Correlation: "
    f"{oee_cycle_correlation:.4f}"
)

# OEE vs downtime

oee_downtime_correlation = (
    machine_performance[
        "oee_pct"
    ].corr(
        machine_performance[
            "downtime_minutes"
        ]
    )
)

print("\nOEE VS DOWNTIME")
print("----------------")

print(
    f"Correlation: "
    f"{oee_downtime_correlation:.4f}"
)

# OEE vs maintenance events

oee_maintenance_correlation = (
    machine_performance[
        "oee_pct"
    ].corr(
        machine_performance[
            "maintenance_events"
        ]
    )
)

print("\nOEE VS MAINTENANCE EVENTS")
print("-------------------------")

print(
    f"Correlation: "
    f"{oee_maintenance_correlation:.4f}"
)

# OEE vs quality

oee_quality_correlation = (
    machine_performance[
        "oee_pct"
    ].corr(
        machine_performance[
            "quality_pct"
        ]
    )
)

print("\nOEE VS QUALITY")
print("----------------")

print(
    f"Correlation: "
    f"{oee_quality_correlation:.4f}"
)

# Machine performance correlation matrix

correlation_columns = [
    "downtime_minutes",
    "availability_pct",
    "performance_pct",
    "quality_pct",
    "oee_pct",
    "cycle_time_variance",
    "maintenance_events"
]

correlation_matrix = (
    machine_performance[
        correlation_columns
    ].corr()
)

print("\nMACHINE PERFORMANCE CORRELATION MATRIX")
print("---------------------------------------")

print(
    correlation_matrix.round(3)
)

# Identify strongest correlations with OEE

oee_correlations = (
    correlation_matrix[
        "oee_pct"
    ]
    .drop("oee_pct")
    .sort_values()
)

print("\nCORRELATIONS WITH OEE")
print("---------------------")

print(
    oee_correlations.round(3)
)

# Strongest negative relationship with OEE

strongest_negative_driver = (
    oee_correlations.idxmin()
)

strongest_negative_value = (
    oee_correlations.min()
)

print("\nSTRONGEST NEGATIVE OEE RELATIONSHIP")
print("-----------------------------------")

print(
    f"Variable: "
    f"{strongest_negative_driver}"
)

print(
    f"Correlation: "
    f"{strongest_negative_value:.4f}"
)

# Save correlation analysis

correlation_matrix.to_csv(
    "data/processed/machine_correlation_matrix.csv"
)

oee_correlations.to_csv(
    "data/processed/oee_correlations.csv"
)

print("\nCorrelation analysis completed successfully.")
