# Tests for capm1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "capm_expected_return",
        "args": (0.03, 1.2, 0.10),
        "expected": 0.114,  # 0.03 + 1.2 * (0.10 - 0.03) = 0.114
        "tolerance": 0.001,
    },
    {
        "func_name": "calculate_beta",
        "args": (0.024, 0.04),
        "expected": 0.6,  # 0.024 / 0.04 = 0.6
        "tolerance": 0.01,
    },
    {
        "func_name": "market_risk_premium",
        "args": (0.10, 0.03),
        "expected": 0.07,  # 0.10 - 0.03 = 0.07
        "tolerance": 0.001,
    },
    {
        "func_name": "alpha",
        "args": (0.15, 0.03, 1.2, 0.10),
        "expected": 0.036,  # 0.15 - (0.03 + 1.2*0.07) = 0.15 - 0.114 = 0.036
        "tolerance": 0.001,
    },
    {
        "func_name": "is_undervalued",
        "args": (0.15, 0.114),
        "expected": True,  # 0.15 > 0.114
    },
    {
        "func_name": "portfolio_beta",
        "args": (np.array([0.5, 0.3, 0.2]), np.array([1.2, 0.8, 1.5])),
        "expected": 1.14,  # 0.5*1.2 + 0.3*0.8 + 0.2*1.5 = 0.6 + 0.24 + 0.3 = 1.14
        "tolerance": 0.01,
    },
]
