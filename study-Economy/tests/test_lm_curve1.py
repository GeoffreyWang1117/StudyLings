# Tests for lm_curve1 exercise

TESTS = [
    {
        "func_name": "lm_curve_interest_rate",
        "args": (1000.0, 500.0, 1.0, 0.2, 1000.0),
        # r = (0.2/1000)*1000 - (1/1000)*(500/1) = 0.2 - 0.5 = -0.3... but let's check
        # r = (k/h)*Y - (1/h)*(M/P) = (0.2/1000)*1000 - (1/1000)*500 = 0.2 - 0.5 = -0.3
        "expected": -0.3,
        "tolerance": 0.01,
    },
    {
        "func_name": "lm_curve_slope",
        "args": (0.2, 1000.0),
        "expected": 0.0002,  # 0.2/1000 = 0.0002
        "tolerance": 0.00001,
    },
    {
        "func_name": "money_demand",
        "args": (1000.0, 0.05, 0.2, 1000.0),
        "expected": 150.0,  # 0.2*1000 - 1000*0.05 = 200 - 50 = 150
        "tolerance": 0.01,
    },
    {
        "func_name": "real_money_supply",
        "args": (500.0, 1.0),
        "expected": 500.0,  # 500/1 = 500
        "tolerance": 0.01,
    },
    {
        "func_name": "lm_shift_from_money_supply",
        "args": (100.0, 1.0, 0.2),
        "expected": 500.0,  # 100 / (1 * 0.2) = 500
        "tolerance": 0.1,
    },
]
