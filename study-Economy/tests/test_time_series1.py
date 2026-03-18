# Tests for time_series1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "autocorrelation",
        "args": (np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), 1),
        "expected": 0.714,  # Approximate
        "tolerance": 0.1,
    },
    {
        "func_name": "difference",
        "args": (np.array([1.0, 3.0, 6.0, 10.0]), 1),
        "expected": np.array([2.0, 3.0, 4.0]),
        "tolerance": 0.01,
    },
    {
        "func_name": "moving_average",
        "args": (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), 3),
        "expected": np.array([2.0, 3.0, 4.0]),
        "tolerance": 0.01,
    },
    {
        "func_name": "is_stationary",
        "args": (-3.5, -2.86),
        "expected": True,  # -3.5 < -2.86
    },
]
