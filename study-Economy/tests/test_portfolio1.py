# Tests for portfolio1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "portfolio_return",
        "args": (np.array([0.6, 0.4]), np.array([0.10, 0.15])),
        "expected": 0.12,  # 0.6*0.10 + 0.4*0.15 = 0.12
        "tolerance": 0.001,
    },
    {
        "func_name": "portfolio_variance_two_assets",
        "args": (0.5, 0.20, 0.30, 0.5),
        # 0.25*0.04 + 0.25*0.09 + 2*0.25*0.5*0.2*0.3 = 0.01 + 0.0225 + 0.015 = 0.0475
        "expected": 0.0475,
        "tolerance": 0.001,
    },
    {
        "func_name": "minimum_variance_weight_two_assets",
        "args": (0.20, 0.30, 0.5),
        # w1 = (0.09 - 0.5*0.2*0.3) / (0.04 + 0.09 - 2*0.5*0.2*0.3)
        # = (0.09 - 0.03) / (0.13 - 0.06) = 0.06 / 0.07 = 0.857
        "expected": 0.857,
        "tolerance": 0.01,
    },
    {
        "func_name": "correlation_from_covariance",
        "args": (0.006, 0.20, 0.15),
        "expected": 0.2,  # 0.006 / (0.2 * 0.15) = 0.2
        "tolerance": 0.01,
    },
]
