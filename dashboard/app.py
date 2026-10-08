import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Manufacturing Operations Analytics",
    page_icon="🏭",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

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


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🏭 Manufacturing Operations Analytics")

st.markdown(
    """
    **Production Performance, OEE, Quality, Downtime & Maintenance**
    
    This dashboard provides an operational overview of manufacturing
    performance and identifies machines and production areas requiring
    attention.
    """
)


# =========================================================
# EXECUTIVE KPI SUMMARY
# =========================================================

st.subheader("Executive KPI Summary")

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


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Overall OEE",
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


col4, col5, col6 = st.columns(3)

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


# =========================================================
# MACHINE FILTER
# =========================================================

st.subheader("Machine Analysis")

machine_list = sorted(
    machine_dashboard["machine_id"].unique()
)

selected_machine = st.selectbox(
    "Select a machine",
    ["All Machines"] + machine_list
)


# =========================================================
# FILTER MACHINE DATA
# =========================================================

if selected_machine == "All Machines":

    filtered_machine = machine_dashboard.copy()

else:

    filtered_machine = machine_dashboard[
        machine_dashboard["machine_id"] == selected_machine
    ]


# =========================================================
# MACHINE PERFORMANCE
# =========================================================

if selected_machine == "All Machines":

    st.markdown(
        "### OEE by Machine"
    )

    machine_oee_chart = (
        machine_dashboard
        .sort_values(
            "oee_pct"
        )
        [
            [
                "machine_id",
                "oee_pct"
            ]
        ]
    )

    st.bar_chart(
        machine_oee_chart,
        x="machine_id",
        y="oee_pct"
    )

else:

    st.markdown(
        f"### {selected_machine} Performance"
    )

    selected = filtered_machine.iloc[0]

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "OEE",
        f"{selected['oee_pct']:.2f}%"
    )

    metric2.metric(
        "Availability",
        f"{selected['availability_pct']:.2f}%"
    )

    metric3.metric(
        "Performance",
        f"{selected['performance_pct']:.2f}%"
    )

    metric4.metric(
        "Quality",
        f"{selected['quality_pct']:.2f}%"
    )


# =========================================================
# TWO-COLUMN ANALYSIS
# =========================================================

left_column, right_column = st.columns(2)


with left_column:

    st.subheader("Downtime by Reason")

    downtime_chart = (
        downtime_dashboard
        [
            [
                "downtime_reason",
                "downtime_minutes"
            ]
        ]
    )

    st.bar_chart(
        downtime_chart,
        x="downtime_reason",
        y="downtime_minutes"
    )


with right_column:

    st.subheader("Defect Rate by Shift")

    shift_quality_chart = (
        shift_dashboard
        [
            [
                "shift_id",
                "defect_rate_pct"
            ]
        ]
    )

    st.bar_chart(
        shift_quality_chart,
        x="shift_id",
        y="defect_rate_pct"
    )


# =========================================================
# CYCLE TIME ANALYSIS
# =========================================================

st.subheader("Cycle-Time Variance by Machine")

cycle_chart = (
    machine_dashboard
    .sort_values(
        "cycle_time_variance",
        ascending=False
    )
    [
        [
            "machine_id",
            "cycle_time_variance"
        ]
    ]
)

st.bar_chart(
    cycle_chart,
    x="machine_id",
    y="cycle_time_variance"
)


# =========================================================
# MAINTENANCE ANALYSIS
# =========================================================

st.subheader("Maintenance Events by Machine")

maintenance_chart = (
    maintenance_dashboard
    .sort_values(
        "maintenance_events",
        ascending=False
    )
    [
        [
            "machine_id",
            "maintenance_events"
        ]
    ]
)

st.bar_chart(
    maintenance_chart,
    x="machine_id",
    y="maintenance_events"
)


# =========================================================
# MACHINE PRIORITY
# =========================================================

st.subheader("🚨 Machines Requiring Attention")

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


# =========================================================
# KEY OPERATIONAL FINDINGS
# =========================================================

st.subheader("Key Operational Findings")

lowest_oee_machine = (
    machine_dashboard
    .sort_values("oee_pct")
    .iloc[0]
)

highest_downtime_reason = (
    downtime_dashboard
    .sort_values(
        "downtime_minutes",
        ascending=False
    )
    .iloc[0]
)

highest_defect_shift = (
    shift_dashboard
    .sort_values(
        "defect_rate_pct",
        ascending=False
    )
    .iloc[0]
)

highest_cycle_variance = (
    machine_dashboard
    .sort_values(
        "cycle_time_variance",
        ascending=False
    )
    .iloc[0]
)

st.markdown(
    f"""
    - **Overall OEE:** {oee:.2f}% across the manufacturing operation.
    
    - **Lowest-performing machine:** 
      {lowest_oee_machine["machine_id"]} with an OEE of 
      {lowest_oee_machine["oee_pct"]:.2f}%.
    
    - **Highest downtime cause:** 
      {highest_downtime_reason["downtime_reason"]}, accounting for 
      {highest_downtime_reason["downtime_pct"]:.2f}% of total downtime.
    
    - **Highest-defect shift:** 
      {highest_defect_shift["shift_id"]} with a defect rate of 
      {highest_defect_shift["defect_rate_pct"]:.2f}%.
    
    - **Highest cycle-time variance:** 
      {highest_cycle_variance["machine_id"]} with a variance of 
      {highest_cycle_variance["cycle_time_variance"]:.2f} seconds.
    """
)


# =========================================================
# PROJECT NOTE
# =========================================================

st.divider()

st.caption(
    """
    Manufacturing Operations Analytics | Portfolio Data Analyst Project |
    Analysis based on generated manufacturing operational data.
    """
)
