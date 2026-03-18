# Tests for hypothesis1 exercise

TESTS = [
    {
        "func_name": "is_significant",
        "args": (0.03, 0.05),
        "expected": True,
    },
    {
        "func_name": "is_significant",
        "args": (0.08, 0.05),
        "expected": False,
    },
    {
        "func_name": "confidence_interval",
        "args": (2.5, 0.5, 0.05, 100),
        "expected": (1.51, 3.49),  # Approximately 2.5 ± 1.96*0.5
        "tolerance": 0.1,
    },
]
