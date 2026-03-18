# Tests for multiplier1 exercise

TESTS = [
    {
        "func_name": "spending_multiplier",
        "args": (0.8,),
        "expected": 5.0,  # 1 / (1-0.8) = 5
        "tolerance": 0.01,
    },
    {
        "func_name": "spending_multiplier",
        "args": (0.6,),
        "expected": 2.5,  # 1 / (1-0.6) = 2.5
        "tolerance": 0.01,
    },
    {
        "func_name": "tax_multiplier",
        "args": (0.8,),
        "expected": -4.0,  # -0.8 / (1-0.8) = -4
        "tolerance": 0.01,
    },
    {
        "func_name": "gdp_change_from_spending",
        "args": (100.0, 0.8),
        "expected": 500.0,  # 100 * 5 = 500
        "tolerance": 0.01,
    },
    {
        "func_name": "gdp_change_from_tax",
        "args": (100.0, 0.8),
        "expected": -400.0,  # 100 * -4 = -400
        "tolerance": 0.01,
    },
    {
        "func_name": "balanced_budget_multiplier",
        "args": (),
        "expected": 1.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_propensity_to_save",
        "args": (0.8,),
        "expected": 0.2,  # 1 - 0.8 = 0.2
        "tolerance": 0.01,
    },
]
