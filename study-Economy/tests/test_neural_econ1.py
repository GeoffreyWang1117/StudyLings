# Tests for neural_econ1 exercise

import numpy as np

TESTS = [
    {
        "func_name": "relu",
        "args": (np.array([-1.0, 0.0, 1.0, 2.0]),),
        "expected": np.array([0.0, 0.0, 1.0, 2.0]),
        "tolerance": 0.001,
    },
    {
        "func_name": "relu_derivative",
        "args": (np.array([-1.0, 0.0, 1.0, 2.0]),),
        "expected": np.array([0.0, 0.0, 1.0, 1.0]),
        "tolerance": 0.001,
    },
    {
        "func_name": "sigmoid",
        "args": (np.array([0.0]),),
        "expected": np.array([0.5]),
        "tolerance": 0.001,
    },
    {
        "func_name": "mse_loss",
        "args": (np.array([1.0, 2.0, 3.0]), np.array([1.1, 2.2, 2.8])),
        "expected": 0.03,  # ((0.1)^2 + (0.2)^2 + (0.2)^2) / 3 = 0.09/3
        "tolerance": 0.01,
    },
    {
        "func_name": "gradient_descent_step",
        "args": (np.array([1.0, 2.0]), np.array([0.1, 0.2]), 0.1),
        "expected": np.array([0.99, 1.98]),  # [1-0.01, 2-0.02]
        "tolerance": 0.001,
    },
]
