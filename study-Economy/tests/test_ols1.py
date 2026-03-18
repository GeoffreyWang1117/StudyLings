# Tests for ols1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "residual_sum_of_squares",
        "args": (np.array([1.0, 2.0, 3.0]), np.array([1.1, 1.9, 3.2])),
        "expected": 0.06,  # 0.01 + 0.01 + 0.04
        "tolerance": 0.01,
    },
    {
        "func_name": "total_sum_of_squares",
        "args": (np.array([1.0, 2.0, 3.0]),),
        "expected": 2.0,  # (1-2)^2 + (2-2)^2 + (3-2)^2 = 2
        "tolerance": 0.01,
    },
    {
        "func_name": "durbin_watson",
        "args": (np.array([0.1, -0.1, 0.05, -0.05]),),
        "expected": 2.2,  # Calculated DW statistic
        "tolerance": 0.5,
    },
]
