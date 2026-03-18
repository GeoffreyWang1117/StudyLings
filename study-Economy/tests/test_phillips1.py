# Tests for phillips1 exercise

TESTS = [
    {
        "func_name": "phillips_curve_inflation",
        "args": (6.0, 5.0, 2.0, 0.5),
        "expected": 1.5,  # 2.0 - 0.5*(6-5) = 2.0 - 0.5 = 1.5
        "tolerance": 0.01,
    },
    {
        "func_name": "phillips_curve_unemployment",
        "args": (3.0, 5.0, 2.0, 0.5),
        "expected": 3.0,  # 5.0 - (3.0-2.0)/0.5 = 5.0 - 2.0 = 3.0
        "tolerance": 0.01,
    },
    {
        "func_name": "sacrifice_ratio",
        "args": (-2.0, 1.0),
        "expected": 0.5,  # 1.0 / 2.0 = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "adaptive_expectations",
        "args": (3.0, 2.0, 0.5),
        "expected": 2.5,  # 2.0 + 0.5*(3.0-2.0) = 2.5
        "tolerance": 0.01,
    },
    {
        "func_name": "unemployment_gap",
        "args": (6.0, 5.0),
        "expected": 1.0,  # 6.0 - 5.0 = 1.0
        "tolerance": 0.01,
    },
    {
        "func_name": "is_stagflation",
        "args": (8.0, 8.0, 5.0, 6.0),
        "expected": True,  # Both above thresholds
    },
    {
        "func_name": "is_stagflation",
        "args": (3.0, 4.0, 5.0, 6.0),
        "expected": False,  # Both below thresholds
    },
]
