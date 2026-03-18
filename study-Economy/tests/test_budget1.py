# Tests for budget1 exercise

TESTS = [
    {
        "func_name": "budget_line_y",
        "args": (5.0, 10.0, 5.0, 100.0),  # x=5, px=10, py=5, M=100
        "expected": 10.0,  # (100 - 10*5) / 5 = 50/5 = 10
        "tolerance": 0.01,
    },
    {
        "func_name": "budget_line_slope",
        "args": (10.0, 5.0),  # px=10, py=5
        "expected": -2.0,  # -10/5 = -2
        "tolerance": 0.01,
    },
    {
        "func_name": "is_affordable",
        "args": (5.0, 10.0, 10.0, 5.0, 100.0),
        "expected": True,  # 10*5 + 5*10 = 100 <= 100
    },
    {
        "func_name": "is_affordable",
        "args": (6.0, 10.0, 10.0, 5.0, 100.0),
        "expected": False,  # 10*6 + 5*10 = 110 > 100
    },
    {
        "func_name": "max_x",
        "args": (10.0, 100.0),
        "expected": 10.0,  # 100/10 = 10
        "tolerance": 0.01,
    },
    {
        "func_name": "max_y",
        "args": (5.0, 100.0),
        "expected": 20.0,  # 100/5 = 20
        "tolerance": 0.01,
    },
]
