# Tests for dsge1 exercise

TESTS = [
    {
        "func_name": "nkpc",
        "args": (0.02, 0.01, 0.99, 0.1),
        "expected": 0.0208,  # 0.99*0.02 + 0.1*0.01
        "tolerance": 0.001,
    },
    {
        "func_name": "taylor_rule",
        "args": (0.02, 0.03, 0.01, 1.5, 0.5),
        "expected": 0.07,  # 0.02 + 1.5*0.03 + 0.5*0.01
        "tolerance": 0.001,
    },
    {
        "func_name": "check_taylor_principle",
        "args": (1.5,),
        "expected": True,
    },
    {
        "func_name": "check_taylor_principle",
        "args": (0.8,),
        "expected": False,
    },
    {
        "func_name": "discount_factor_from_interest_rate",
        "args": (0.04,),
        "expected": 0.9901,  # 1 / (1 + 0.04/4)
        "tolerance": 0.001,
    },
]
