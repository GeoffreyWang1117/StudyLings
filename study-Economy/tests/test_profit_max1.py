# Tests for profit_max1 exercise

TESTS = [
    {
        "func_name": "profit",
        "args": (10.0, 50.0, 300.0),
        "expected": 200.0,  # 10*50 - 300 = 200
        "tolerance": 0.01,
    },
    {
        "func_name": "total_revenue",
        "args": (10.0, 50.0),
        "expected": 500.0,  # 10*50 = 500
        "tolerance": 0.01,
    },
    {
        "func_name": "should_produce",
        "args": (10.0, 8.0),
        "expected": True,  # P > AVC_min
    },
    {
        "func_name": "should_produce",
        "args": (5.0, 8.0),
        "expected": False,  # P < AVC_min
    },
    {
        "func_name": "break_even_price",
        "args": (100.0, 5.0, 0.1, 0.01, 10.0),
        "expected": 17.0,  # TC/Q = 170/10 = 17
        "tolerance": 0.1,
    },
]
