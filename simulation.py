from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CostParameters:
    """Cost structure for the inventory system."""
    holding_cost: float       # cost per unit of ending inventory per period
    shortage_cost: float      # cost per unit of unsatisfied demand per period
    unit_cost: float          # purchasing cost per unit ordered
    ordering_cost: float      # fixed cost incurred whenever an order is placed


@dataclass(frozen=True)
class InitialState:
    """Initial inventory and outstanding order state."""
    on_hand: int              # units available on hand at the start
    outstanding_qty: int      # units already ordered but not yet received
    lead_remaining: int       # days remaining for the outstanding order to arrive


@dataclass(frozen=True)
class DiscreteDistributions:
    """Discrete probability distributions for demand and lead time."""
    demand_values: np.ndarray   # possible demand values
    demand_probs: np.ndarray    # probabilities for each demand value
    lead_values: np.ndarray     # possible lead-time values (in days)
    lead_probs: np.ndarray      # probabilities for each lead-time value


def _sample_from_discrete(
    values: np.ndarray,
    probs: np.ndarray,
    rng: np.random.Generator,
) -> int:
    """Sample a value from a discrete distribution defined by `values` and `probs`."""
    return int(rng.choice(values, p=probs))


def simulate_policy(
    M: int,
    N: int,
    num_cycles: int,
    costs: CostParameters,
    initial_state: InitialState,
    distributions: DiscreteDistributions,
    seed: Optional[int] = None,
) -> tuple[pd.DataFrame, float, float]:
    """
    Simulate the (M, N) inventory policy.

    Parameters
    ----------
    M : int
        Maximum inventory level (order-up-to level).
    N : int
        Review period length in days.
    num_cycles : int
        Number of review cycles to simulate.
    costs : CostParameters
        Cost configuration (holding, shortage, purchasing, ordering).
    initial_state : InitialState
        Initial inventory and outstanding order conditions.
    distributions : DiscreteDistributions
        Discrete distributions for daily demand and lead time.
    seed : Optional[int]
        Random seed for reproducibility.

    Returns
    -------
    df : pandas.DataFrame
        Daily simulation results.
    total_cost : float
        Total cost accumulated over the simulation horizon.
    avg_cost_per_cycle : float
        Average cost per review cycle (= total_cost / num_cycles).
    """
    rng = np.random.default_rng(seed)
    num_days = N * num_cycles

    # Copy initial state into mutable local variables
    on_hand = int(initial_state.on_hand)
    outstanding_qty = int(initial_state.outstanding_qty)
    lead_remaining = int(initial_state.lead_remaining)

    records: list[dict] = []
    total_cost = 0.0

    for day in range(1, num_days + 1):
        cycle = (day - 1) // N + 1

        # 1) Receive outstanding order at the start of the day, if its lead time has expired
        incoming_today = 0
        if lead_remaining == 0 and outstanding_qty > 0:
            incoming_today = outstanding_qty
            on_hand += incoming_today
            outstanding_qty = 0

        on_hand_start = on_hand

        # 2) Sample daily demand from the distribution
        demand = _sample_from_discrete(
            distributions.demand_values,
            distributions.demand_probs,
            rng,
        )

        # 3) Compute sales, ending inventory, and shortage quantity
        sales = min(on_hand, demand)
        shortage_qty = max(demand - on_hand, 0)
        ending_inventory = on_hand - sales

        # 4) Compute holding and shortage costs for the day
        holding_cost = ending_inventory * costs.holding_cost
        shortage_cost = shortage_qty * costs.shortage_cost

        # 5) Check if today is a review day
        is_review_day = (day % N == 0)

        order_qty = 0
        purchasing_cost = 0.0
        ordering_cost = 0.0
        lead_time_assigned: Optional[int] = None

        # 6) At the end of a review day, place an order if needed
        if is_review_day and ending_inventory < M and outstanding_qty == 0:
            order_qty = M - ending_inventory

            # Sample lead time for the new order
            lead_time_assigned = _sample_from_discrete(
                distributions.lead_values,
                distributions.lead_probs,
                rng,
            )

            outstanding_qty = order_qty
            lead_remaining = lead_time_assigned

            purchasing_cost = order_qty * costs.unit_cost
            ordering_cost = costs.ordering_cost

        # 7) Decrease lead time for outstanding orders
        if outstanding_qty > 0 and lead_remaining > 0:
            lead_remaining -= 1

        # 8) Prepare on-hand inventory for the next day
        on_hand = ending_inventory

        # 9) Aggregate total daily cost
        day_cost = holding_cost + shortage_cost + purchasing_cost + ordering_cost
        total_cost += day_cost

        records.append(
            {
                "Day": day,
                "Cycle": cycle,
                "On-hand start": on_hand_start,
                "Incoming today": incoming_today,
                "Demand": demand,
                "Sales": sales,
                "Ending inventory": ending_inventory,
                "Shortage qty": shortage_qty,
                "Holding cost": holding_cost,
                "Shortage cost": shortage_cost,
                "Order qty": order_qty,
                "Lead time (new order)": lead_time_assigned,
                "Lead remaining end": lead_remaining,
                "Purchasing cost": purchasing_cost,
                "Ordering cost": ordering_cost,
                "Total cost (day)": day_cost,
            }
        )

    df = pd.DataFrame(records)
    avg_cost_per_cycle = total_cost / num_cycles
    return df, total_cost, avg_cost_per_cycle
