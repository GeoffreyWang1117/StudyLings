# I AM NOT DONE

"""
Gradient Descent Optimization

Gradient Descent is a fundamental optimization algorithm used to minimize functions
by iteratively moving in the direction of steepest descent (negative gradient).

Your task: Implement gradient descent variants.
"""

from typing import Callable, List


class GradientDescent:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def optimize(self, gradient_fn: Callable[[List[float]], List[float]], 
                initial: List[float], iterations: int) -> List[float]:
        """Run basic gradient descent"""
        # TODO: Implement gradient descent
        # theta = theta - learning_rate * gradient
        pass


class MomentumGD:
    def __init__(self, learning_rate: float, momentum: float):
        self.learning_rate = learning_rate
        self.momentum = momentum

    def optimize(self, gradient_fn: Callable[[List[float]], List[float]], 
                initial: List[float], iterations: int) -> List[float]:
        """Gradient descent with momentum"""
        # TODO: Implement momentum
        # v = momentum * v - learning_rate * gradient
        # theta = theta + v
        pass


class Adam:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8

    def optimize(self, gradient_fn: Callable[[List[float]], List[float]], 
                initial: List[float], iterations: int) -> List[float]:
        """Adam optimizer"""
        # TODO: Implement Adam
        pass


import unittest

class TestGradientDescent(unittest.TestCase):
    def quadratic_gradient(self, params: List[float]) -> List[float]:
        return [2.0 * x for x in params]

    def test_gradient_descent(self):
        gd = GradientDescent(0.1)
        result = gd.optimize(self.quadratic_gradient, [10.0], 50)
        self.assertLess(abs(result[0]), 0.1)

    def test_momentum(self):
        momentum = MomentumGD(0.01, 0.9)
        result = momentum.optimize(self.quadratic_gradient, [10.0], 100)
        self.assertLess(abs(result[0]), 0.1)

if __name__ == '__main__':
    unittest.main()
