import streamlit as st

from config import (
    DEFAULT_COSTS,
    DEFAULT_INITIAL_STATE,
    DEFAULT_DISTRIBUTIONS,
    DEFAULT_NUM_CYCLES,
)
from simulation import simulate_policy, CostParameters


st.title("Custom (M, N) Policy")

st.markdown(
    """
Use this page to experiment with a **custom (M, N) policy** and custom cost parameters.

This is useful to explore how different inventory strategies perform beyond
the four preset policies from the assignment.
"""
)

# ---- Sidebar controls ----
st.sidebar.header("Custom Policy Parameters")

custom_M = st.sidebar.number_input(
    "M – Maximum inventory level (order-up-to level)",
    min_value=0,
    value=11,
    step=1,
)
custom_N = st.sidebar.number_input(
    "N – Review period (days)",
    min_value=1,
    value=5,
    step=1,
)

num_cycles = st.sidebar.slider(
    "Number of cycles", min_value=5, max_value=30, value=DEFAULT_NUM_CYCLES, step=1
)

st.sidebar.markdown("---")
st.sidebar.header("Cost Parameters")

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

st.info(
    f"Simulating custom policy with **M = {custom_M}**, **N = {custom_N}**, "
    f"**{num_cycles} cycles**, and the cost parameters specified in the sidebar."
)

# ---- Run simulation ----
df, total_cost, avg_cost = simulate_policy(
    M=int(custom_M),
    N=int(custom_N),
    num_cycles=num_cycles,
    costs=cost_params,
    initial_state=DEFAULT_INITIAL_STATE,
    distributions=DEFAULT_DISTRIBUTIONS,
    seed=seed,
)

st.subheader("Cost Results")
st.write(f"**Total cost over the horizon**: ${total_cost:,.2f}")
st.write(f"**Average cost per cycle**: ${avg_cost:,.2f}")

st.subheader("Daily Simulation Output")
st.dataframe(df, use_container_width=True)
