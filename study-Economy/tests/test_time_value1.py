# Tests for time_value1 exercise

TESTS = [
    {
        "func_name": "future_value",
        "args": (1000.0, 0.05, 10),
        "expected": 1628.89,  # 1000 * (1.05)^10
        "tolerance": 0.1,
    },
    {
        "func_name": "present_value",
        "args": (1628.89, 0.05, 10),
        "expected": 1000.0,
        "tolerance": 0.1,
    },
    {
        "func_name": "annuity_future_value",
        "args": (100.0, 0.05, 10),
        "expected": 1257.79,  # 100 * [(1.05)^10 - 1] / 0.05
        "tolerance": 0.1,
    },
    {
        "func_name": "annuity_present_value",
        "args": (100.0, 0.05, 10),
        "expected": 772.17,  # 100 * [1 - (1.05)^(-10)] / 0.05
        "tolerance": 0.1,
    },
    {
        "func_name": "perpetuity_present_value",
        "args": (100.0, 0.05),
        "expected": 2000.0,  # 100 / 0.05
        "tolerance": 0.01,
    },
    {
        "func_name": "effective_annual_rate",
        "args": (0.12, 12),
        "expected": 0.1268,  # (1 + 0.12/12)^12 - 1
        "tolerance": 0.001,
    },
]
