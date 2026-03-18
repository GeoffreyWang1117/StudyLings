# Tests for okun1 exercise

TESTS = [
    {
        "func_name": "okun_gdp_growth",
        "args": (-1.0, 3.0, 2.0),
        "expected": 5.0,  # 3 - 2*(-1) = 5
        "tolerance": 0.01,
    },
    {
        "func_name": "okun_unemployment_change",
        "args": (5.0, 3.0, 2.0),
        "expected": -1.0,  # (3-5)/2 = -1
        "tolerance": 0.01,
    },
    {
        "func_name": "output_gap_from_unemployment",
        "args": (6.0, 5.0, 2.0),
        "expected": -2.0,  # -2*(6-5) = -2%
        "tolerance": 0.01,
    },
    {
        "func_name": "unemployment_from_output_gap",
        "args": (-4.0, 5.0, 2.0),
        "expected": 7.0,  # 5 - (-4)/2 = 5 + 2 = 7
        "tolerance": 0.01,
    },
    {
        "func_name": "required_growth_for_unemployment_reduction",
        "args": (1.0, 3.0, 2.0),
        "expected": 5.0,  # 3 + 2*1 = 5
        "tolerance": 0.01,
    },
]
