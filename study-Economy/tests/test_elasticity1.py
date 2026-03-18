# Tests for elasticity1 exercise

TESTS = [
    {
        "func_name": "point_elasticity",
        "args": (10.0, 70.0, -3.0),  # P=10, Q=70, dQ/dP=-3 for Qd = 100 - 3P
        "expected": -0.42857142857142855,  # -3 * (10/70)
        "tolerance": 0.01,
    },
    {
        "func_name": "point_elasticity",
        "args": (20.0, 40.0, -3.0),  # P=20, Q=40
        "expected": -1.5,  # -3 * (20/40)
        "tolerance": 0.01,
    },
    {
        "func_name": "arc_elasticity",
        "args": (10.0, 70.0, 15.0, 55.0),  # Price goes from 10 to 15, Q from 70 to 55
        "expected": -0.6,  # [(-15)/62.5] / [5/12.5] = -0.24 / 0.4 = -0.6
        "tolerance": 0.01,
    },
    {
        "func_name": "arc_elasticity",
        "args": (20.0, 40.0, 25.0, 25.0),
        "expected": -1.3846153846153846,  # [(-15)/32.5] / [5/22.5]
        "tolerance": 0.01,
    },
    {
        "func_name": "classify_elasticity",
        "args": (-1.5,),
        "expected": "elastic",
    },
    {
        "func_name": "classify_elasticity",
        "args": (-1.0,),
        "expected": "unit_elastic",
    },
    {
        "func_name": "classify_elasticity",
        "args": (-0.5,),
        "expected": "inelastic",
    },
    {
        "func_name": "classify_elasticity",
        "args": (2.0,),
        "expected": "elastic",
    },
]
