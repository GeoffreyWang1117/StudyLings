# Tests for arima1 exercise

TESTS = [
    {
        "func_name": "aic",
        "args": (100, 3, -150.0),
        "expected": 306.0,  # 2*3 - 2*(-150) = 306
        "tolerance": 0.1,
    },
    {
        "func_name": "bic",
        "args": (100, 3, -150.0),
        "expected": 313.82,  # 3*ln(100) - 2*(-150) ≈ 313.82
        "tolerance": 0.5,
    },
]
