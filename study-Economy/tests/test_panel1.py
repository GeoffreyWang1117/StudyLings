# Tests for panel1 exercise

TESTS = [
    {
        "func_name": "calculate_theta",
        "args": (0.2, 0.5, 5),
        "expected": 0.553,  # 1 - sqrt(0.25 / (5*0.04 + 0.25))
        "tolerance": 0.05,
    },
]
