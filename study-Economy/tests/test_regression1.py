# Tests for regression1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "ols_slope",
        "args": (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array([2.0, 4.0, 5.0, 4.0, 5.0])),
        "expected": 0.6,
        "tolerance": 0.1,
    },
    {
        "func_name": "ols_intercept",
        "args": (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array([2.0, 4.0, 5.0, 4.0, 5.0])),
        "expected": 2.2,
        "tolerance": 0.1,
    },
    {
        "func_name": "predict",
        "args": (np.array([1.0, 2.0, 3.0]), 2.0, 0.5),
        "expected": np.array([2.5, 3.0, 3.5]),
        "tolerance": 0.01,
    },
    {
        "func_name": "residuals",
        "args": (np.array([3.0, 4.0, 5.0]), np.array([2.5, 4.0, 5.5])),
        "expected": np.array([0.5, 0.0, -0.5]),
        "tolerance": 0.01,
    },
    {
        "func_name": "correlation_coefficient",
        "args": (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array([2.0, 4.0, 5.0, 4.0, 5.0])),
        "expected": 0.6,
        "tolerance": 0.1,
    },
]
