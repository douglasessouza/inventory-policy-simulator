import streamlit as st
import pandas as pd

from config import (
    PRESET_POLICIES,
    DEFAULT_COSTS,
    DEFAULT_INITIAL_STATE,
    DEFAULT_DISTRIBUTIONS,
    DEFAULT_NUM_CYCLES,
)
from simulation import simulate_policy, CostParameters


st.title("Summary & Charts – Preset Policies")

st.markdown(
    """
This page provides a **high-level summary and visual comparison** of the four
preset policies from the assignment.
"""
)

# ---- Sidebar controls ----
st.sidebar.header("Summary – Global Parameters")

num_cycles = st.sidebar.slider(
    "Number of cycles", min_value=5, max_value=30, value=DEFAULT_NUM_CYCLES, step=1
)

holding_cost = st.sidebar.number_input(
    "Holding cost per unit per period", value=DEFAULT_COSTS.holding_cost, step=1.0
)
shortage_cost = st.sidebar.number_input(
    "Shortage cost per unit per period", value=DEFAULT_COSTS.shortage_cost, step=1.0
)
unit_cost = st.sidebar.number_input(
    "Purchasing cost per unit", value=DEFAULT_COSTS.unit_cost, step=1.0
)
ordering_cost = st.sidebar.number_input(
    "Fixed ordering cost", value=DEFAULT_COSTS.ordering_cost, step=1.0
)

seed_input = st.sidebar.text_input("Random seed (optional)", value="0")
try:
    seed = int(seed_input)
except ValueError:
    seed = None

cost_params = CostParameters(
    holding_cost=holding_cost,
    shortage_cost=shortage_cost,
    unit_cost=unit_cost,
    ordering_cost=ordering_cost,
)

# ---- Run simulations ----
summary_rows = []

for name, (M, N) in PRESET_POLICIES.items():
    df, total_cost, avg_cost = simulate_policy(
        M=M,
        N=N,
        num_cycles=num_cycles,
        costs=cost_params,
        initial_state=DEFAULT_INITIAL_STATE,
        distributions=DEFAULT_DISTRIBUTIONS,
        seed=seed,
    )

    summary_rows.append(
        {
            "Policy": name,
            "M": M,
            "N": N,
            "Total Cost": round(total_cost, 2),
            "Avg. Cost per Cycle": round(avg_cost, 2),
        }
    )

summary_df = pd.DataFrame(summary_rows)

st.subheader("Summary Table")
st.dataframe(summary_df, use_container_width=True)

# ---- Charts ----
st.subheader("Average Cost per Cycle – Bar Chart")
chart_df = summary_df.set_index("Policy")[["Avg. Cost per Cycle"]]
st.bar_chart(chart_df)

st.subheader("Total Cost – Bar Chart")
total_chart_df = summary_df.set_index("Policy")[["Total Cost"]]
st.bar_chart(total_chart_df)

# Best policy highlight
best_idx = summary_df["Avg. Cost per Cycle"].idxmin()
best_policy = summary_df.loc[best_idx, "Policy"]
best_cost = summary_df.loc[best_idx, "Avg. Cost per Cycle"]

st.success(
    f"With the current parameters, the **best preset policy** is **{best_policy}** "
    f"with an average cost per cycle of **${best_cost:,.2f}**."
)

st.caption(
    "You can modify the cost parameters and number of cycles in the sidebar "
    "to explore how the optimal policy changes."
)
