# Tests for production1 exercise

TESTS = [
    {
        "func_name": "cobb_douglas_production",
        "args": (100.0, 100.0, 1.0, 0.5, 0.5),
        "expected": 100.0,  # 1 * 100^0.5 * 100^0.5 = 100
        "tolerance": 0.01,
    },
    {
        "func_name": "cobb_douglas_production",
        "args": (8.0, 27.0, 2.0, 0.25, 0.75),
        "expected": 27.0,  # 2 * 8^0.25 * 27^0.75 = 2 * 1.68 * 8.03 ≈ 27
        "tolerance": 0.5,
    },
    {
        "func_name": "marginal_product_labor",
        "args": (100.0, 100.0, 1.0, 0.5, 0.5),
        "expected": 0.5,  # 0.5 * 100 / 100 = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_product_capital",
        "args": (100.0, 100.0, 1.0, 0.5, 0.5),
        "expected": 0.5,  # 0.5 * 100 / 100 = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "returns_to_scale",
        "args": (0.6, 0.6),
        "expected": "increasing",
    },
    {
        "func_name": "returns_to_scale",
        "args": (0.5, 0.5),
        "expected": "constant",
    },
    {
        "func_name": "returns_to_scale",
        "args": (0.3, 0.4),
        "expected": "decreasing",
    },
    {
        "func_name": "technical_rate_of_substitution",
        "args": (50.0, 100.0, 0.5, 0.5),
        "expected": 2.0,  # (0.5/0.5) * (100/50) = 2
        "tolerance": 0.01,
    },
]
