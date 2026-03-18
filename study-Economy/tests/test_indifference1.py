# Tests for indifference1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "indifference_curve_y",
        "args": (4.0, 6.0, 0.5, 0.5),  # x=4, U=6, alpha=0.5, beta=0.5
        "expected": 9.0,  # y = (6 / 4^0.5)^2 = (6/2)^2 = 9
        "tolerance": 0.01,
    },
    {
        "func_name": "indifference_curve_y",
        "args": (1.0, 4.0, 0.5, 0.5),
        "expected": 16.0,  # y = (4 / 1^0.5)^2 = 16
        "tolerance": 0.01,
    },
    {
        "func_name": "indifference_curve_slope",
        "args": (4.0, 9.0, 0.5, 0.5),
        "expected": -2.25,  # -(0.5/0.5) * (9/4) = -2.25
        "tolerance": 0.01,
    },
    {
        "func_name": "is_convex_to_origin",
        "args": ([1.0, 2.0, 4.0, 8.0], [16.0, 8.0, 4.0, 2.0]),
        "expected": True,
    },
]
