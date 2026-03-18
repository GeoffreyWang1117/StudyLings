# Tests for elasticity2 exercise

TESTS = [
    {
        "func_name": "cross_price_elasticity",
        "args": (100.0, 120.0, 5.0, 6.0),  # Q_A: 100->120, P_B: 5->6
        "expected": 1.0,  # (20/110) / (1/5.5) = 0.182 / 0.182 = 1.0
        "tolerance": 0.01,
    },
    {
        "func_name": "cross_price_elasticity",
        "args": (100.0, 80.0, 5.0, 6.0),  # Q_A: 100->80, P_B: 5->6 (complements)
        "expected": -1.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "income_elasticity",
        "args": (100.0, 150.0, 50000.0, 60000.0),
        "expected": 2.2,  # (50/125) / (10000/55000) = 0.4 / 0.182 ≈ 2.2
        "tolerance": 0.1,
    },
    {
        "func_name": "income_elasticity",
        "args": (100.0, 90.0, 50000.0, 60000.0),  # Inferior good
        "expected": -0.55,
        "tolerance": 0.1,
    },
    {
        "func_name": "classify_by_cross_elasticity",
        "args": (1.5,),
        "expected": "substitutes",
    },
    {
        "func_name": "classify_by_cross_elasticity",
        "args": (-0.8,),
        "expected": "complements",
    },
    {
        "func_name": "classify_by_cross_elasticity",
        "args": (0.05,),
        "expected": "independent",
    },
    {
        "func_name": "classify_by_income_elasticity",
        "args": (2.0,),
        "expected": "luxury",
    },
    {
        "func_name": "classify_by_income_elasticity",
        "args": (0.5,),
        "expected": "necessity",
    },
    {
        "func_name": "classify_by_income_elasticity",
        "args": (-0.3,),
        "expected": "inferior",
    },
]
