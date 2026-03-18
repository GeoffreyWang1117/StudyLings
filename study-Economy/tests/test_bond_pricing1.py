# Tests for bond_pricing1 exercise

TESTS = [
    {
        "func_name": "bond_price",
        "args": (1000.0, 0.06, 0.05, 5, 2),
        "expected": 1043.76,  # Premium bond (coupon > yield)
        "tolerance": 1.0,
    },
    {
        "func_name": "zero_coupon_bond_price",
        "args": (1000.0, 0.05, 10),
        "expected": 613.91,  # 1000 / (1.05)^10
        "tolerance": 0.5,
    },
    {
        "func_name": "current_yield",
        "args": (0.06, 1000.0, 950.0),
        "expected": 0.0632,  # 60 / 950
        "tolerance": 0.001,
    },
    {
        "func_name": "ytm_approximation",
        "args": (1000.0, 0.06, 950.0, 10),
        # [60 + (1000-950)/10] / [(1000+950)/2] = 65/975 = 0.0667
        "expected": 0.0667,
        "tolerance": 0.01,
    },
    {
        "func_name": "modified_duration",
        "args": (7.0, 0.06, 2),
        "expected": 6.80,  # 7 / (1 + 0.03) = 6.80
        "tolerance": 0.1,
    },
    {
        "func_name": "price_change_from_duration",
        "args": (6.8, 1000.0, 0.01),
        "expected": -68.0,  # -6.8 * 1000 * 0.01 = -68
        "tolerance": 0.1,
    },
]
