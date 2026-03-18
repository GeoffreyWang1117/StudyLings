# Tests for solow1 exercise

TESTS = [
    {
        "func_name": "per_capita_output",
        "args": (100.0, 1.0, 0.3),
        "expected": 3.981,  # 1 * 100^0.3 ≈ 3.981
        "tolerance": 0.01,
    },
    {
        "func_name": "steady_state_capital",
        "args": (0.3, 1.0, 0.05, 0.02, 0.3),
        # k* = [0.3*1 / (0.05+0.02)]^(1/0.7) = (4.286)^1.429 ≈ 8.57
        "expected": 8.57,
        "tolerance": 0.5,
    },
    {
        "func_name": "capital_change",
        "args": (4.0, 0.3, 1.0, 0.05, 0.02, 0.3),
        # Δk = 0.3*1*4^0.3 - (0.05+0.02)*4 = 0.3*1.516 - 0.28 = 0.455 - 0.28 = 0.175
        "expected": 0.175,
        "tolerance": 0.02,
    },
    {
        "func_name": "investment_per_capita",
        "args": (100.0, 0.3, 1.0, 0.3),
        "expected": 1.194,  # 0.3 * 1 * 100^0.3 = 0.3 * 3.981 = 1.194
        "tolerance": 0.01,
    },
    {
        "func_name": "break_even_investment",
        "args": (100.0, 0.05, 0.02),
        "expected": 7.0,  # (0.05+0.02)*100 = 7
        "tolerance": 0.01,
    },
]
