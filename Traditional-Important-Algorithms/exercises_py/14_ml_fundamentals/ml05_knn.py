# I AM NOT DONE

"""
K-Nearest Neighbors

Classification based on nearest neighbors.

Your task: Implement KNN.
"""

import math
from typing import List, Tuple
from collections import Counter


class KNN:
    def __init__(self, k: int):
        self.k = k
        self.x_train: List[List[float]] = []
        self.y_train: List[int] = []

    @staticmethod
    def euclidean_distance(a: List[float], b: List[float]) -> float:
        """Compute distance"""
        # TODO: Implement
        pass

    def fit(self, x: List[List[float]], y: List[int]):
        """Store training data"""
        # TODO: Store data
        pass

    def predict(self, x: List[List[float]]) -> List[int]:
        """Predict classes"""
        # TODO: Implement prediction
        pass


import unittest

class TestKNN(unittest.TestCase):
    def test_predict(self):
        knn = KNN(3)
        knn.fit([[1.0, 1.0], [2.0, 2.0]], [0, 0])
        predictions = knn.predict([[1.5, 1.5]])
        self.assertEqual(predictions[0], 0)

if __name__ == '__main__':
    unittest.main()
