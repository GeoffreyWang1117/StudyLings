# Tests for efficient_frontier1 exercise

TESTS = [
    {
        "func_name": "sharpe_ratio",
        "args": (0.12, 0.03, 0.18),
        "expected": 0.5,  # (0.12 - 0.03) / 0.18 = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "capital_market_line_return",
        "args": (0.03, 0.10, 0.15, 0.20),
        # 0.03 + [(0.10 - 0.03) / 0.15] * 0.20 = 0.03 + 0.0933 = 0.1233
        "expected": 0.1233,
        "tolerance": 0.01,
    },
    {
        "func_name": "treynor_ratio",
        "args": (0.12, 0.03, 1.2),
        "expected": 0.075,  # (0.12 - 0.03) / 1.2 = 0.075
        "tolerance": 0.001,
    },
    {
        "func_name": "is_efficient_portfolio",
        "args": (0.12, 0.15, 0.08, 0.10),  # Above min variance
        "expected": True,
    },
]
