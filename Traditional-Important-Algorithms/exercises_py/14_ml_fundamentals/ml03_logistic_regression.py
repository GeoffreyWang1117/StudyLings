# I AM NOT DONE

"""
Logistic Regression

Binary classification using sigmoid function.

Your task: Implement logistic regression.
"""

import math
from typing import List


class LogisticRegression:
    def __init__(self):
        self.weights: List[float] = []
        self.bias: float = 0.0

    @staticmethod
    def sigmoid(z: float) -> float:
        """Sigmoid activation"""
        # TODO: Implement sigmoid
        pass

    def fit(self, x: List[List[float]], y: List[int], learning_rate: float, iterations: int):
        """Train model"""
        # TODO: Implement training
        pass

    def predict(self, x: List[List[float]]) -> List[int]:
        """Predict classes"""
        # TODO: Implement prediction
        pass

    def predict_proba(self, x: List[List[float]]) -> List[float]:
        """Predict probabilities"""
        # TODO: Implement probability prediction
        pass


import unittest

class TestLogisticRegression(unittest.TestCase):
    def test_sigmoid(self):
        self.assertAlmostEqual(LogisticRegression.sigmoid(0), 0.5)

if __name__ == '__main__':
    unittest.main()
