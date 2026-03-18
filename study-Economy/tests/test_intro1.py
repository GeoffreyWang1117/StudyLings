# Tests for intro1 exercise

TESTS = [
    {
        "func_name": "percentage_change",
        "args": (100.0, 110.0),
        "expected": 10.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "percentage_change",
        "args": (100.0, 90.0),
        "expected": -10.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "percentage_change",
        "args": (50.0, 75.0),
        "expected": 50.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "annual_to_monthly_rate",
        "args": (0.12,),
        "expected": 0.009488792934583046,  # (1.12)^(1/12) - 1
        "tolerance": 1e-6,
    },
    {
        "func_name": "annual_to_monthly_rate",
        "args": (0.06,),
        "expected": 0.004867550565343048,  # (1.06)^(1/12) - 1
        "tolerance": 1e-6,
    },
    {
        "func_name": "compound_growth",
        "args": (1000.0, 0.05, 10),
        "expected": 1628.894626777442,  # 1000 * (1.05)^10
        "tolerance": 0.01,
    },
    {
        "func_name": "compound_growth",
        "args": (100.0, 0.10, 5),
        "expected": 161.051,  # 100 * (1.10)^5
        "tolerance": 0.01,
    },
]
