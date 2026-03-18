# Tests for monopoly1 exercise

TESTS = [
    {
        "func_name": "inverse_demand",
        "args": (20.0, 100.0, 2.0),
        "expected": 60.0,  # 100 - 2*20 = 60
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_revenue_monopoly",
        "args": (20.0, 100.0, 2.0),
        "expected": 20.0,  # 100 - 4*20 = 20
        "tolerance": 0.01,
    },
    {
        "func_name": "monopoly_quantity",
        "args": (100.0, 2.0, 20.0),
        "expected": 20.0,  # (100 - 20) / (2*2) = 80/4 = 20
        "tolerance": 0.01,
    },
    {
        "func_name": "monopoly_price",
        "args": (100.0, 2.0, 20.0),
        "expected": 60.0,  # 100 - 2*20 = 60
        "tolerance": 0.01,
    },
    {
        "func_name": "monopoly_profit",
        "args": (100.0, 2.0, 20.0, 0.0),
        "expected": 800.0,  # (60-20)*20 = 40*20 = 800
        "tolerance": 0.01,
    },
    {
        "func_name": "deadweight_loss",
        "args": (100.0, 2.0, 20.0),
        "expected": 400.0,  # 0.5 * (40-20) * (60-20) = 0.5 * 20 * 40 = 400
        "tolerance": 0.1,
    },
    {
        "func_name": "lerner_index",
        "args": (60.0, 20.0),
        "expected": 0.666666667,  # (60-20)/60 = 40/60 = 2/3
        "tolerance": 0.01,
    },
]
