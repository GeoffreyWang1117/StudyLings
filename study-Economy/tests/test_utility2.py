# Tests for utility2 exercise

TESTS = [
    {
        "func_name": "marginal_utility_x",
        "args": (4.0, 4.0, 0.5, 0.5),
        "expected": 0.5,  # 0.5 * 4^(-0.5) * 4^0.5 = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_utility_y",
        "args": (4.0, 4.0, 0.5, 0.5),
        "expected": 0.5,  # 0.5 * 4^0.5 * 4^(-0.5) = 0.5
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_rate_of_substitution",
        "args": (4.0, 8.0, 0.5, 0.5),
        "expected": 2.0,  # (0.5/0.5) * (8/4) = 2
        "tolerance": 0.01,
    },
    {
        "func_name": "marginal_rate_of_substitution",
        "args": (10.0, 5.0, 0.3, 0.7),
        "expected": 0.214285714,  # (0.3/0.7) * (5/10) = 0.2143
        "tolerance": 0.01,
    },
    {
        "func_name": "is_diminishing_mu",
        "args": ([10.0, 8.0, 6.0, 4.0],),
        "expected": True,
    },
    {
        "func_name": "is_diminishing_mu",
        "args": ([10.0, 12.0, 11.0, 9.0],),
        "expected": False,
    },
]
