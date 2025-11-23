import streamlit as st

from config import PRESET_POLICIES, DEFAULT_COSTS, DEFAULT_NUM_CYCLES

st.set_page_config(page_title="Inventory (M, N) Policy Simulator", layout="wide")

st.title("Probabilistic Inventory System – (M, N) Policy")

st.markdown(
    """
This Streamlit application implements the **probabilistic inventory system** from the
prescriptive analytics assignment.

The model assumes:

- A periodic review inventory policy **(M, N)**  
- Random **daily demand** and **stochastic lead time**  
- Cost components: holding, shortage, purchasing, and ordering  
- An initial on-hand inventory and an outstanding order in transit  

Use the navigation menu (on the left) to:

1. Explore the **four preset policies** from the assignment  
2. Run simulations with a **custom (M, N) policy and custom cost values**  
3. See a **summary page** with tables and charts comparing the preset policies  

The default configuration reproduces the original assignment:
- Policies: {policies}
- Holding cost: {hc:.2f}
- Shortage cost: {sc:.2f}
- Unit purchasing cost: {uc:.2f}
- Ordering cost: {oc:.2f}
- Number of cycles: {cycles}
""".format(
        policies=", ".join(PRESET_POLICIES.keys()),
        hc=DEFAULT_COSTS.holding_cost,
        sc=DEFAULT_COSTS.shortage_cost,
        uc=DEFAULT_COSTS.unit_cost,
        oc=DEFAULT_COSTS.ordering_cost,
        cycles=DEFAULT_NUM_CYCLES,
    )
)

st.info(
    "Use the **pages** in the sidebar to run simulations and inspect results. "
    "Each page is independent and re-runs the simulation when you change parameters."
)
