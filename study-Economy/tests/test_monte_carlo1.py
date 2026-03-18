# Tests for monte_carlo1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "monte_carlo_standard_error",
        "args": (np.array([10.0, 12.0, 11.0, 9.0, 10.5]),),
        "expected": 0.5,  # Approximate SE
        "tolerance": 0.2,
    },
    {
        "func_name": "required_simulations_for_precision",
        "args": (0.1, 5.0),
        "expected": 2500,  # (5/0.1)^2 = 2500
        "tolerance": 10,
    },
]
