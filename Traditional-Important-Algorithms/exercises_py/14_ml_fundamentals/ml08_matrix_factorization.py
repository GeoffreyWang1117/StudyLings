# I AM NOT DONE

"""
Matrix Factorization

Factorize matrix into product of lower-rank matrices.

Your task: Implement matrix factorization.
"""

from typing import List
import random


class MatrixFactorization:
    def __init__(self, num_factors: int):
        self.num_factors = num_factors
        self.user_factors: List[List[float]] = []
        self.item_factors: List[List[float]] = []

    def fit(self, ratings: List[tuple], num_users: int, num_items: int, 
           learning_rate: float, iterations: int):
        """Train model"""
        # TODO: Implement training
        pass

    def predict(self, user_id: int, item_id: int) -> float:
        """Predict rating"""
        # TODO: Implement prediction
        pass


import unittest

class TestMatrixFactorization(unittest.TestCase):
    def test_predict(self):
        mf = MatrixFactorization(5)
        ratings = [(0, 0, 5.0), (0, 1, 3.0)]
        mf.fit(ratings, 2, 2, 0.01, 100)
        prediction = mf.predict(0, 0)
        self.assertGreater(prediction, 0)

if __name__ == '__main__':
    unittest.main()
