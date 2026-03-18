# Tests for nash_equilibrium1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "best_response",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 0, 0),
        "expected": 1,  # When B cooperates, A's best response is defect
    },
    {
        "func_name": "best_response",
        "args": (np.array([[[-1, -1], [-3, 0]], [[0, -3], [-2, -2]]]), 0, 1),
        "expected": 1,  # When B defects, A's best response is defect
    },
    {
        "func_name": "find_pure_nash_equilibria",
        "args": (np.array([[[1, 1], [0, 0]], [[0, 0], [1, 1]]]),),  # Coordination game
        "expected": [(0, 0), (1, 1)],
    },
    {
        "func_name": "mixed_strategy_nash_2x2",
        "args": (np.array([[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]),),  # Matching pennies
        "expected": (0.5, 0.5),
        "tolerance": 0.01,
    },
    {
        "func_name": "expected_payoff_mixed",
        "args": (np.array([[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]), 0.5, 0.5),
        "expected": (0.0, 0.0),
        "tolerance": 0.01,
    },
]
