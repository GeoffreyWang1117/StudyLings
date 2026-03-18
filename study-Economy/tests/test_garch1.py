# Tests for garch1 exercise

TESTS = [
    {
        "func_name": "unconditional_variance",
        "args": (0.00001, 0.1, 0.85),
        "expected": 0.0002,  # 0.00001 / (1 - 0.1 - 0.85) = 0.0002
        "tolerance": 0.00005,
    },
    {
        "func_name": "volatility_persistence",
        "args": (0.1, 0.85),
        "expected": 0.95,  # 0.1 + 0.85
        "tolerance": 0.01,
    },
    {
        "func_name": "half_life_volatility",
        "args": (0.1, 0.85),
        "expected": 13.51,  # ln(2) / ln(0.95) ≈ 13.51
        "tolerance": 0.5,
    },
]
