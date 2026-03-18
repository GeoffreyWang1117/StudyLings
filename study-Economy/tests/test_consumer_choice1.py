# Tests for consumer_choice1 exercise

TESTS = [
    {
        "func_name": "optimal_consumption",
        "args": (0.5, 0.5, 10.0, 5.0, 100.0),
        "expected": (5.0, 10.0),  # x = 0.5 * 100/10 = 5, y = 0.5 * 100/5 = 10
        "tolerance": 0.01,
    },
    {
        "func_name": "optimal_consumption",
        "args": (0.3, 0.7, 10.0, 10.0, 200.0),
        "expected": (6.0, 14.0),  # x = 0.3 * 200/10 = 6, y = 0.7 * 200/10 = 14
        "tolerance": 0.01,
    },
    {
        "func_name": "optimal_utility",
        "args": (0.5, 0.5, 10.0, 5.0, 100.0),
        "expected": 7.071067811865476,  # 5^0.5 * 10^0.5 = sqrt(50)
        "tolerance": 0.01,
    },
    {
        "func_name": "expenditure_share",
        "args": (0.3, 0.7),
        "expected": (0.3, 0.7),
        "tolerance": 0.01,
    },
    {
        "func_name": "expenditure_share",
        "args": (0.5, 0.5),
        "expected": (0.5, 0.5),
        "tolerance": 0.01,
    },
    {
        "func_name": "price_effect_on_x",
        "args": (0.5, 0.5, 10.0, 20.0, 5.0, 100.0),
        "expected": -2.5,  # 0.5*100/20 - 0.5*100/10 = 2.5 - 5 = -2.5
        "tolerance": 0.01,
    },
]
