# Tests for is_curve1 exercise

TESTS = [
    {
        "func_name": "is_curve_output",
        "args": (0.05, 100.0, 0.8, 200.0, 200.0, 1000.0, 300.0),
        # A = 100 - 0.8*200 + 200 + 300 = 440
        # Y = 440/0.2 - (1000/0.2)*0.05 = 2200 - 250 = 1950
        "expected": 1950.0,
        "tolerance": 1.0,
    },
    {
        "func_name": "is_curve_slope",
        "args": (0.8, 1000.0),
        "expected": -0.0002,  # -(1-0.8)/1000 = -0.0002
        "tolerance": 0.0001,
    },
    {
        "func_name": "is_shift_from_government_spending",
        "args": (100.0, 0.8),
        "expected": 500.0,  # 100 / (1-0.8) = 500
        "tolerance": 0.1,
    },
    {
        "func_name": "investment",
        "args": (200.0, 1000.0, 0.05),
        "expected": 150.0,  # 200 - 1000*0.05 = 150
        "tolerance": 0.01,
    },
]
