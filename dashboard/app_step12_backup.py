import streamlit as st
import pandas as pd

# Page configuration

st.set_page_config(
    page_title="Manufacturing Operations Analytics",
    page_icon="🏭",
    layout="wide"
)

# Dashboard title

st.title("Manufacturing Operations Analytics")

st.markdown(
    "### Production Performance, OEE, Quality, Downtime & Maintenance"
)

# Load dashboard datasets

kpi_summary = pd.read_csv(
    "data/processed/kpi_summary.csv"
)

machine_dashboard = pd.read_csv(
    "data/processed/machine_dashboard.csv"
)

shift_dashboard = pd.read_csv(
    "data/processed/shift_dashboard.csv"
)

downtime_dashboard = pd.read_csv(
    "data/processed/downtime_dashboard.csv"
)

maintenance_dashboard = pd.read_csv(
    "data/processed/maintenance_dashboard.csv"
)

machine_priority = pd.read_csv(
    "data/processed/machine_priority.csv"
)

# Restore machine ID column

if "machine_id" not in machine_dashboard.columns:
    machine_dashboard = machine_dashboard.rename(
        columns={"index": "machine_id"}
    )

if "machine_id" not in machine_priority.columns:
    machine_priority = machine_priority.rename(
        columns={"index": "machine_id"}
    )

# Extract KPI values

total_units = kpi_summary.loc[
    kpi_summary["KPI"] == "Total Units Produced",
    "Value"
].iloc[0]

defect_rate = kpi_summary.loc[
    kpi_summary["KPI"] == "Defect Rate (%)",
    "Value"
].iloc[0]

availability = kpi_summary.loc[
    kpi_summary["KPI"] == "Availability (%)",
    "Value"
].iloc[0]

performance = kpi_summary.loc[
    kpi_summary["KPI"] == "Performance (%)",
    "Value"
].iloc[0]

quality = kpi_summary.loc[
    kpi_summary["KPI"] == "Quality (%)",
    "Value"
].iloc[0]

oee = kpi_summary.loc[
    kpi_summary["KPI"] == "OEE (%)",
    "Value"
].iloc[0]

# Executive KPI cards

st.subheader("Executive KPI Summary")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "OEE",
    f"{oee:.2f}%"
)

col2.metric(
    "Availability",
    f"{availability:.2f}%"
)

col3.metric(
    "Performance",
    f"{performance:.2f}%"
)

col4.metric(
    "Quality",
    f"{quality:.2f}%"
)

col5.metric(
    "Defect Rate",
    f"{defect_rate:.2f}%"
)

col6.metric(
    "Units Produced",
    f"{total_units:,.0f}"
)

st.subheader("OEE by Machine")

machine_oee_chart = (
    machine_dashboard
    .sort_values("oee_pct")
    [["machine_id", "oee_pct"]]
)

st.bar_chart(
    machine_oee_chart,
    x="machine_id",
    y="oee_pct"
)

st.subheader("Downtime by Reason")

downtime_chart = (
    downtime_dashboard
    .set_index("downtime_reason")[
        ["downtime_minutes"]
    ]
)

st.bar_chart(
    downtime_chart
)

st.subheader("Defect Rate by Shift")

shift_quality_chart = (
    shift_dashboard
    .set_index("shift_id")[
        ["defect_rate_pct"]
    ]
)

st.bar_chart(
    shift_quality_chart
)

st.subheader("Cycle-Time Variance by Machine")

cycle_chart = (
    machine_dashboard
    .sort_values(
        "cycle_time_variance",
        ascending=False
    )
    [["machine_id", "cycle_time_variance"]]
)

st.bar_chart(
    cycle_chart,
    x="machine_id",
    y="cycle_time_variance"
)

st.subheader("Maintenance Events by Machine")

maintenance_chart = (
    maintenance_dashboard
    .sort_values(
        "maintenance_events",
        ascending=False
    )
    .set_index("machine_id")[
        ["maintenance_events"]
    ]
)

st.bar_chart(
    maintenance_chart
)

st.subheader("Machines Requiring Attention")

priority_display = machine_priority[
    [
        "machine_id",
        "oee_pct",
        "performance_pct",
        "quality_pct",
        "downtime_minutes",
        "cycle_time_variance",
        "maintenance_events"
    ]
].copy()

priority_display.columns = [
    "Machine",
    "OEE (%)",
    "Performance (%)",
    "Quality (%)",
    "Downtime (min)",
    "Cycle Variance (sec)",
    "Maintenance Events"
]

st.dataframe(
    priority_display,
    width="stretch",
    hide_index=True
)

st.subheader("Key Operational Findings")

st.markdown(
    f"""
- **Overall OEE:** {oee:.2f}% across the manufacturing operation.
- **Lowest-performing machine:** {machine_priority.iloc[0]["machine_id"]} with an OEE of {machine_priority.iloc[0]["oee_pct"]:.2f}%.
- **Highest downtime cause:** {downtime_dashboard.iloc[0]["downtime_reason"]}, accounting for {downtime_dashboard.iloc[0]["downtime_pct"]:.2f}% of total downtime.
- **Highest-defect shift:** {shift_dashboard.loc[shift_dashboard["defect_rate_pct"].idxmax(), "shift_id"]} with a defect rate of {shift_dashboard["defect_rate_pct"].max():.2f}%.
- **Highest cycle-time variance:** {machine_dashboard.loc[machine_dashboard["cycle_time_variance"].idxmax(), "machine_id"]} with a variance of {machine_dashboard["cycle_time_variance"].max():.2f} seconds.
"""
)

