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


st.title("Preset Policies (A–D)")

st.markdown(
    """
This page simulates the **four preset (M, N) policies** defined in the assignment
using the probabilistic inventory model.

You can adjust cost parameters and the number of cycles in the sidebar to see how
the performance of each policy changes.
"""
)

# ---- Sidebar controls ----
st.sidebar.header("Preset Policy Simulation – Global Parameters")

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

# ---- Run simulations for all preset policies ----
summary_rows = []
results: dict[str, dict] = {}

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

    results[name] = {
        "M": M,
        "N": N,
        "df": df,
        "total_cost": total_cost,
        "avg_cost": avg_cost,
    }

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

st.subheader("Summary Table – Preset Policies")
st.dataframe(summary_df, use_container_width=True)

# Identify best policy
best_idx = summary_df["Avg. Cost per Cycle"].idxmin()
best_policy = summary_df.loc[best_idx, "Policy"]
best_cost = summary_df.loc[best_idx, "Avg. Cost per Cycle"]

st.success(
    f"Best preset policy (with current parameters): **{best_policy}** "
    f"with average cost per cycle = **${best_cost:,.2f}**."
)

st.markdown("---")
st.subheader("Inspect Daily Simulation Results")

selected_policy = st.selectbox("Choose a policy to inspect:", list(PRESET_POLICIES.keys()))

st.markdown(f"### {selected_policy}")
st.dataframe(results[selected_policy]["df"], use_container_width=True)
