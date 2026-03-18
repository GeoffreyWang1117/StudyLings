# Tests for black_scholes1 exercise

TESTS = [
    {
        "func_name": "d1",
        "args": (100.0, 100.0, 0.05, 1.0, 0.20),
        # [ln(1) + (0.05 + 0.02)*1] / (0.2*1) = 0.07/0.2 = 0.35
        "expected": 0.35,
        "tolerance": 0.01,
    },
    {
        "func_name": "d2",
        "args": (100.0, 100.0, 0.05, 1.0, 0.20),
        "expected": 0.15,  # 0.35 - 0.20 = 0.15
        "tolerance": 0.01,
    },
    {
        "func_name": "black_scholes_call",
        "args": (100.0, 100.0, 0.05, 1.0, 0.20),
        "expected": 10.45,  # Standard BS result
        "tolerance": 0.5,
    },
    {
        "func_name": "black_scholes_put",
        "args": (100.0, 100.0, 0.05, 1.0, 0.20),
        "expected": 5.57,  # From put-call parity
        "tolerance": 0.5,
    },
    {
        "func_name": "option_delta_call",
        "args": (100.0, 100.0, 0.05, 1.0, 0.20),
        "expected": 0.6368,  # N(0.35)
        "tolerance": 0.01,
    },
]
