# Tests for regression2 exercise

import numpy as np

TESTS = [
    {
        "func_name": "adjusted_r_squared",
        "args": (0.8, 100, 3),
        "expected": 0.794,  # 1 - (1-0.8)*99/96
        "tolerance": 0.01,
    },
    {
        "func_name": "f_statistic",
        "args": (0.6, 100, 2),
        "expected": 72.75,  # (0.6/2) / (0.4/97) = 0.3 / 0.00412 = 72.75
        "tolerance": 1.0,
    },
]
