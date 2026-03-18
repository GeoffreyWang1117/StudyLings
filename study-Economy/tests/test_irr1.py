# Tests for irr1 exercise

TESTS = [
    {
        "func_name": "irr_decision",
        "args": (0.15, 0.10),
        "expected": "accept",
    },
    {
        "func_name": "irr_decision",
        "args": (0.08, 0.10),
        "expected": "reject",
    },
    {
        "func_name": "npv_at_rate",
        "args": ([-1000.0, 500.0, 600.0], 0.10),
        "expected": -49.59,  # -1000 + 500/1.1 + 600/1.21
        "tolerance": 1.0,
    },
    {
        "func_name": "has_multiple_irrs",
        "args": ([-100.0, 230.0, -132.0],),  # Sign changes twice
        "expected": True,
    },
    {
        "func_name": "has_multiple_irrs",
        "args": ([-100.0, 50.0, 60.0],),  # Sign changes once
        "expected": False,
    },
]
