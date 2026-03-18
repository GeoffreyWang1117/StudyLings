# Tests for supply_demand1 exercise

TESTS = [
    {
        "func_name": "supply",
        "args": (10.0,),
        "expected": 10.0,  # -10 + 2*10 = 10
        "tolerance": 0.01,
    },
    {
        "func_name": "supply",
        "args": (22.0,),
        "expected": 34.0,  # -10 + 2*22 = 34
        "tolerance": 0.01,
    },
    {
        "func_name": "supply",
        "args": (5.0,),
        "expected": 0.0,  # -10 + 2*5 = 0
        "tolerance": 0.01,
    },
    {
        "func_name": "supply",
        "args": (3.0,),
        "expected": 0.0,  # -10 + 2*3 = -4, but can't be negative
        "tolerance": 0.01,
    },
    {
        "func_name": "demand",
        "args": (10.0,),
        "expected": 70.0,  # 100 - 3*10 = 70
        "tolerance": 0.01,
    },
    {
        "func_name": "demand",
        "args": (22.0,),
        "expected": 34.0,  # 100 - 3*22 = 34
        "tolerance": 0.01,
    },
    {
        "func_name": "demand",
        "args": (0.0,),
        "expected": 100.0,  # 100 - 3*0 = 100
        "tolerance": 0.01,
    },
    {
        "func_name": "demand",
        "args": (40.0,),
        "expected": 0.0,  # 100 - 3*40 = -20, but can't be negative
        "tolerance": 0.01,
    },
]
