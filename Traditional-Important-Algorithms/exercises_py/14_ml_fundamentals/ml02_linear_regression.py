# I AM NOT DONE

"""
Linear Regression

Models the relationship between features and output: y = w*x + b

Your task: Implement linear regression.
"""

from typing import List, Optional


class LinearRegression:
    def __init__(self):
        self.weights: Optional[List[float]] = None
        self.bias: float = 0.0

    def fit_gradient_descent(self, x: List[List[float]], y: List[float], 
                            learning_rate: float, iterations: int):
        """Fit using gradient descent"""
        # TODO: Implement gradient descent training
        pass

    def predict(self, x: List[List[float]]) -> List[float]:
        """Make predictions"""
        # TODO: Implement prediction
        pass

    def score(self, x: List[List[float]], y: List[float]) -> float:
        """Compute R² score"""
        # TODO: Implement R² score
        pass


import unittest

class TestLinearRegression(unittest.TestCase):
    def test_simple_fit(self):
        x = [[1.0], [2.0], [3.0]]
        y = [3.0, 5.0, 7.0]  # y = 2x + 1
        
        model = LinearRegression()
        model.fit_gradient_descent(x, y, 0.01, 1000)
        
        predictions = model.predict([[4.0]])
        self.assertLess(abs(predictions[0] - 9.0), 0.5)

if __name__ == '__main__':
    unittest.main()
