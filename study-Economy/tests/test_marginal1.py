# Tests for marginal1 exercise

TESTS = [
    {
        "func_name": "marginal_revenue",
        "args": ([1, 2, 3, 4, 5], [10, 19, 27, 34, 40]),
        "expected": [9.0, 8.0, 7.0, 6.0],
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_cost",
        "args": ([1, 2, 3, 4, 5], [5, 9, 12, 14, 18]),
        "expected": [4.0, 3.0, 2.0, 4.0],
        "tolerance": 0.01,
    },
    {
        "func_name": "find_profit_maximizing_quantity",
        "args": ([1, 2, 3, 4, 5], [10, 19, 27, 34, 40], [5, 9, 12, 14, 18]),
        "expected": 4.0,  # MR=[9,8,7,6], MC=[4,3,2,4], closest at Q=4 or Q=5
        "tolerance": 0.5,
    },
    {
        "func_name": "calculate_profit",
        "args": (100.0, 60.0),
        "expected": 40.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "calculate_profit",
        "args": (50.0, 80.0),
        "expected": -30.0,
        "tolerance": 0.01,
    },
]
