# Tests for ad_as1 exercise

TESTS = [
    {
        "func_name": "sras_price",
        "args": (1100.0, 1000.0, 2.0, 0.5),
        "expected": 2.5,  # 2 + 0.5*(1100-1000) = 2 + 50 = 52... wait that's wrong
        # P = Pe + lambda*(Y - Yn) = 2.0 + 0.5*(1100-1000) = 2.0 + 0.005*100 = 2.05
        # Actually if lambda is small like 0.005: 2 + 0.005*100 = 2.05
        # Let me use lambda = 0.01: P = 2.0 + 0.01*100 = 3.0
        "expected": 52.0,  # With lambda = 0.5
        "tolerance": 0.1,
    },
    {
        "func_name": "sras_output",
        "args": (2.5, 1000.0, 2.0, 0.5),
        "expected": 1001.0,  # Y = 1000 + (2.5 - 2.0) / 0.5 = 1000 + 1 = 1001
        "tolerance": 0.1,
    },
    {
        "func_name": "lras_output",
        "args": (1000.0,),
        "expected": 1000.0,
        "tolerance": 0.01,
    },
    {
        "func_name": "output_gap",
        "args": (1100.0, 1000.0),
        "expected": 100.0,  # 1100 - 1000 = 100
        "tolerance": 0.01,
    },
    {
        "func_name": "inflation_from_output_gap",
        "args": (100.0, 0.02),
        "expected": 2.0,  # 0.02 * 100 = 2
        "tolerance": 0.01,
    },
]
