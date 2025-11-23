from __future__ import annotations

import numpy as np

from simulation import CostParameters, InitialState, DiscreteDistributions

# -----------------------------
# Discrete distributions
# -----------------------------
# Daily demand distribution (from the assignment)
DEMAND_VALUES = np.array([0, 1, 2, 3, 4], dtype=int)
DEMAND_PROBS = np.array([0.10, 0.25, 0.35, 0.21, 0.09], dtype=float)

# Lead-time distribution (in days)
LEAD_VALUES = np.array([1, 2, 3], dtype=int)
LEAD_PROBS = np.array([0.60, 0.30, 0.10], dtype=float)

DEFAULT_DISTRIBUTIONS = DiscreteDistributions(
    demand_values=DEMAND_VALUES,
    demand_probs=DEMAND_PROBS,
    lead_values=LEAD_VALUES,
    lead_probs=LEAD_PROBS,
)

# -----------------------------
# Cost parameters (defaults from assignment)
# -----------------------------
DEFAULT_COSTS = CostParameters(
    holding_cost=20.0,   # per unit per period
    shortage_cost=10.0,  # per unit per period
    unit_cost=50.0,      # purchasing cost per unit
    ordering_cost=10.0,  # fixed ordering cost
)

# -----------------------------
# Initial state (from assignment)
# -----------------------------
DEFAULT_INITIAL_STATE = InitialState(
    on_hand=3,
    outstanding_qty=8,
    lead_remaining=2,
)

# -----------------------------
# Preset policies (M, N) from assignment
# -----------------------------
PRESET_POLICIES: dict[str, tuple[int, int]] = {
    "Policy A (M=11, N=5)": (11, 5),
    "Policy B (M=11, N=6)": (11, 6),
    "Policy C (M=12, N=5)": (12, 5),
    "Policy D (M=12, N=6)": (12, 6),
}

# Default number of cycles used in the assignment
DEFAULT_NUM_CYCLES: int = 10
