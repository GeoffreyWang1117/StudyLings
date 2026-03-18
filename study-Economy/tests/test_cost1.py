# Tests for cost1 exercise

TESTS = [
    {
        "func_name": "total_cost",
        "args": (10.0, 100.0, 5.0, 0.1, 0.01),
        "expected": 260.0,  # 100 + 5*10 + 0.1*100 + 0.01*1000 = 100 + 50 + 10 + 10 = 170... let me recalc
        # TC = 100 + 5*10 + 0.1*10^2 + 0.01*10^3 = 100 + 50 + 10 + 10 = 170
        "tolerance": 0.1,
    },
    {
        "func_name": "variable_cost",
        "args": (10.0, 5.0, 0.1, 0.01),
        "expected": 70.0,  # 5*10 + 0.1*100 + 0.01*1000 = 50 + 10 + 10 = 70
        "tolerance": 0.1,
    },
    {
        "func_name": "marginal_cost",
        "args": (10.0, 5.0, 0.1, 0.01),
        "expected": 10.0,  # 5 + 2*0.1*10 + 3*0.01*100 = 5 + 2 + 3 = 10
        "tolerance": 0.1,
    },
    {
        "func_name": "average_total_cost",
        "args": (10.0, 100.0, 5.0, 0.1, 0.01),
        "expected": 17.0,  # 170 / 10 = 17
        "tolerance": 0.1,
    },
    {
        "func_name": "average_variable_cost",
        "args": (10.0, 5.0, 0.1, 0.01),
        "expected": 7.0,  # 5 + 0.1*10 + 0.01*100 = 5 + 1 + 1 = 7
        "tolerance": 0.1,
    },
]
