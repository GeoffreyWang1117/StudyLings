# Tests for reinforcement1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "q_learning_update",
        "args": (1.0, 0.5, 2.0, 0.1, 0.9),
        "expected": 1.13,  # 1.0 + 0.1*(0.5 + 0.9*2.0 - 1.0) = 1.0 + 0.1*1.3 = 1.13
        "tolerance": 0.01,
    },
    {
        "func_name": "temporal_difference_error",
        "args": (1.0, 5.0, 6.0, 0.9),
        "expected": 1.4,  # 1 + 0.9*6 - 5 = 1 + 5.4 - 5 = 1.4
        "tolerance": 0.01,
    },
    {
        "func_name": "discount_sum",
        "args": (np.array([1.0, 1.0, 1.0, 1.0]), 0.9),
        "expected": 3.439,  # 1 + 0.9 + 0.81 + 0.729
        "tolerance": 0.01,
    },
    {
        "func_name": "consumption_savings_reward",
        "args": (10.0, 2.0),
        "expected": -0.1,  # 10^(-1) / (-1) = -0.1
        "tolerance": 0.01,
    },
]
