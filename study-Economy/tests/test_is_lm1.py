# Tests for is_lm1 exercise

TESTS = [
    {
        "func_name": "crowding_out",
        "args": (100.0, 0.8, 1000.0, 0.2, 1000.0),
        # First calc Δr from fiscal expansion
        # Δr = (k/(h(1-c) + dk)) * ΔG = (0.2 / (1000*0.2 + 1000*0.2)) * 100 = 0.0005 * 100 = 0.05
        # Crowding out = d * Δr = 1000 * 0.05 = 50
        "expected": 50.0,
        "tolerance": 5.0,
    },
    {
        "func_name": "is_fiscal_more_effective",
        "args": (500.0, 0.2, 2000.0),  # d*k/h = 500*0.2/2000 = 0.05 < 1
        "expected": True,
    },
    {
        "func_name": "is_fiscal_more_effective",
        "args": (2000.0, 0.5, 500.0),  # d*k/h = 2000*0.5/500 = 2 > 1
        "expected": False,
    },
]
