# Tests for solow2 exercise

TESTS = [
    {
        "func_name": "golden_rule_savings_rate",
        "args": (0.3,),
        "expected": 0.3,  # s_gold = alpha
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_product_of_capital",
        "args": (100.0, 1.0, 0.3),
        # MPK = 0.3 * 1 * 100^(-0.7) = 0.3 * 0.0398 = 0.01194
        "expected": 0.01194,
        "tolerance": 0.001,
    },
    {
        "func_name": "is_dynamically_efficient",
        "args": (0.08, 0.05, 0.02),
        "expected": True,  # MPK > delta + n
    },
    {
        "func_name": "is_dynamically_efficient",
        "args": (0.05, 0.05, 0.02),
        "expected": False,  # MPK < delta + n
    },
    {
        "func_name": "convergence_speed",
        "args": (0.05, 0.02, 0.3),
        "expected": 0.049,  # (1-0.3)*(0.05+0.02) = 0.7*0.07 = 0.049
        "tolerance": 0.001,
    },
]
