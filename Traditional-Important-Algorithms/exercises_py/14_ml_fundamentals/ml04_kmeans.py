# I AM NOT DONE

"""
K-Means Clustering

Unsupervised clustering algorithm.

Your task: Implement K-Means.
"""

import math
from typing import List


class KMeans:
    def __init__(self, k: int, max_iterations: int = 100):
        self.k = k
        self.max_iterations = max_iterations
        self.centroids: List[List[float]] = []

    @staticmethod
    def euclidean_distance(a: List[float], b: List[float]) -> float:
        """Compute Euclidean distance"""
        # TODO: Implement distance
        pass

    def fit(self, data: List[List[float]]):
        """Run K-Means algorithm"""
        # TODO: Implement K-Means
        pass

    def predict(self, data: List[List[float]]) -> List[int]:
        """Assign points to clusters"""
        # TODO: Implement prediction
        pass


import unittest

class TestKMeans(unittest.TestCase):
    def test_distance(self):
        dist = KMeans.euclidean_distance([0.0, 0.0], [3.0, 4.0])
        self.assertAlmostEqual(dist, 5.0)

if __name__ == '__main__':
    unittest.main()
