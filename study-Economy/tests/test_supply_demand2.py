# Tests for supply_demand2 exercise

TESTS = [
    {
        "func_name": "find_equilibrium",
        "args": (),
        "expected": (22.0, 34.0),
        "tolerance": 0.01,
    },
    {
        "func_name": "market_status",
        "args": (22.0,),
        "expected": "equilibrium",
    },
    {
        "func_name": "market_status",
        "args": (30.0,),
        "expected": "surplus",  # Qs = 50, Qd = 10, surplus
    },
    {
        "func_name": "market_status",
        "args": (15.0,),
        "expected": "shortage",  # Qs = 20, Qd = 55, shortage
    },
    {
        "func_name": "calculate_surplus_or_shortage",
        "args": (22.0,),
        "expected": 0.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "calculate_surplus_or_shortage",
        "args": (30.0,),
        "expected": 40.0,  # Qs = 50, Qd = 10, surplus of 40
        "tolerance": 0.01,
    },
    {
        "func_name": "calculate_surplus_or_shortage",
        "args": (15.0,),
        "expected": -35.0,  # Qs = 20, Qd = 55, shortage of 35
        "tolerance": 0.01,
    },
]
