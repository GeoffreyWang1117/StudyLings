# Tests for npv1 exercise

TESTS = [
    {
        "func_name": "npv",
        "args": ([-1000.0, 300.0, 400.0, 500.0, 200.0], 0.10),
        "expected": 108.72,
        "tolerance": 1.0,
    },
    {
        "func_name": "npv_decision",
        "args": (108.72,),
        "expected": "accept",
    },
    {
        "func_name": "npv_decision",
        "args": (-50.0,),
        "expected": "reject",
    },
    {
        "func_name": "profitability_index",
        "args": ([-1000.0, 300.0, 400.0, 500.0, 200.0], 0.10),
        "expected": 1.1087,
        "tolerance": 0.01,
    },
    {
        "func_name": "compare_projects",
        "args": ([-1000.0, 600.0, 600.0], [-1000.0, 300.0, 1000.0], 0.10),
        "expected": "B",  # NPV_A ≈ 41, NPV_B ≈ 99
    },
]
