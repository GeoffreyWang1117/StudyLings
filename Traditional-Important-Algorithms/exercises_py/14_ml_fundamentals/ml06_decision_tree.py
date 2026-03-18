# I AM NOT DONE

"""
Decision Tree Classifier

Tree-based classification.

Your task: Implement decision tree.
"""

from typing import List, Optional
import math


class Node:
    def __init__(self):
        self.feature: Optional[int] = None
        self.threshold: Optional[float] = None
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.value: Optional[int] = None


class DecisionTree:
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
        self.root: Optional[Node] = None

    def fit(self, x: List[List[float]], y: List[int]):
        """Build tree"""
        # TODO: Implement tree building
        pass

    def predict(self, x: List[List[float]]) -> List[int]:
        """Predict classes"""
        # TODO: Implement prediction
        pass


import unittest

class TestDecisionTree(unittest.TestCase):
    def test_fit(self):
        tree = DecisionTree()
        tree.fit([[1.0], [2.0], [3.0]], [0, 0, 1])
        predictions = tree.predict([[1.5]])
        self.assertIn(predictions[0], [0, 1])

if __name__ == '__main__':
    unittest.main()
