# Tests for gdp1 exercise

TESTS = [
    {
        "func_name": "gdp_expenditure_approach",
        "args": (7000.0, 2000.0, 2500.0, 1500.0, 1000.0),
        "expected": 12000.0,  # 7000 + 2000 + 2500 + (1500-1000) = 12000
        "tolerance": 0.01,
    },
    {
        "func_name": "real_gdp",
        "args": (11000.0, 110.0),
        "expected": 10000.0,  # 11000 / 110 * 100 = 10000
        "tolerance": 0.01,
    },
    {
        "func_name": "gdp_growth_rate",
        "args": (11000.0, 10000.0),
        "expected": 10.0,  # (11000-10000)/10000 * 100 = 10%
        "tolerance": 0.01,
    },
    {
        "func_name": "gdp_per_capita",
        "args": (10000000.0, 1000.0),
        "expected": 10000.0,  # 10000000/1000 = 10000
        "tolerance": 0.01,
    },
    {
        "func_name": "net_exports",
        "args": (1500.0, 1000.0),
        "expected": 500.0,  # 1500 - 1000 = 500
        "tolerance": 0.01,
    },
]
