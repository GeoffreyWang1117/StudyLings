# Tests for utility1 exercise

TESTS = [
    {
        "func_name": "cobb_douglas_utility",
        "args": (4.0, 9.0, 0.5, 0.5),
        "expected": 6.0,  # 4^0.5 * 9^0.5 = 2 * 3 = 6
        "tolerance": 0.01,
    },
    {
        "func_name": "cobb_douglas_utility",
        "args": (8.0, 8.0, 0.25, 0.75),
        "expected": 8.0,  # 8^0.25 * 8^0.75 = 8
        "tolerance": 0.01,
    },
    {
        "func_name": "perfect_complements_utility",
        "args": (5.0, 10.0, 1.0, 1.0),
        "expected": 5.0,  # min(5, 10) = 5
        "tolerance": 0.01,
    },
    {
        "func_name": "perfect_complements_utility",
        "args": (4.0, 3.0, 2.0, 1.0),
        "expected": 3.0,  # min(2*4, 1*3) = min(8, 3) = 3
        "tolerance": 0.01,
    },
    {
        "func_name": "perfect_substitutes_utility",
        "args": (3.0, 4.0, 2.0, 3.0),
        "expected": 18.0,  # 2*3 + 3*4 = 6 + 12 = 18
        "tolerance": 0.01,
    },
]
