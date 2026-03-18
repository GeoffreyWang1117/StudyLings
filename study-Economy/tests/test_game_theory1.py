# Tests for game_theory1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "get_payoff",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 0, 0),
        "expected": (-1.0, -1.0),
        "tolerance": 0.01,
    },
    {
        "func_name": "get_payoff",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 1, 0),
        "expected": (0.0, -3.0),
        "tolerance": 0.01,
    },
    {
        "func_name": "find_dominant_strategy",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 0),
        "expected": 1,  # Player A's dominant strategy is to defect
    },
    {
        "func_name": "is_nash_equilibrium",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 1, 1),
        "expected": True,  # (Defect, Defect) is Nash equilibrium
    },
    {
        "func_name": "is_nash_equilibrium",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 0, 0),
        "expected": False,  # (Cooperate, Cooperate) is not Nash equilibrium
    },
    {
        "func_name": "find_all_nash_equilibria",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]),),
        "expected": [(1, 1)],  # Only (Defect, Defect)
    },
]
