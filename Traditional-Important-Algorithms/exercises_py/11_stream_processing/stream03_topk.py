# I AM NOT DONE

"""
Exercise: Top-K Elements in Stream

Maintain top-K most frequent or largest elements in a data stream efficiently.

Algorithms:
- Min-heap based approach (K-sized heap)
- Count-Min Sketch + Min-heap for frequency
- Space-Saving algorithm

Your task: Implement top-K tracking for streaming data.
"""

import heapq
from typing import List, Tuple
from collections import Counter


class TopKElements:
    """Track top-K elements in stream"""

    def __init__(self, k: int):
        self.k = k
        self.heap = []  # Min-heap of (value, element) pairs
        self.counts = Counter()

    def add(self, element: int):
        """Add element to stream"""
        # TODO: Add element and maintain top-K
        # - Increment count
        # - Update heap to keep top-K by frequency
        pass

    def get_topk(self) -> List[Tuple[int, int]]:
        """Return top-K elements as (element, count) pairs"""
        # TODO: Return top-K elements
        pass

    def get_topk_values(self) -> List[int]:
        """Return just the top-K element values"""
        # TODO: Return top-K element values
        pass


class TopKLargest:
    """Track top-K largest elements"""

    def __init__(self, k: int):
        self.k = k
        self.heap = []  # Min-heap

    def add(self, value: int):
        """Add value to stream"""
        # TODO: Maintain top-K largest using min-heap
        pass

    def get_topk(self) -> List[int]:
        """Return top-K largest elements"""
        # TODO: Return sorted top-K
        pass


import unittest


class TestTopK(unittest.TestCase):
    def test_topk_frequency(self):
        topk = TopKElements(3)
        for val in [1, 2, 2, 3, 3, 3, 4]:
            topk.add(val)

        top_vals = topk.get_topk_values()
        self.assertIn(3, top_vals)
        self.assertIn(2, top_vals)

    def test_topk_largest(self):
        topk = TopKLargest(3)
        for val in [5, 2, 8, 1, 9, 3]:
            topk.add(val)

        top = topk.get_topk()
        self.assertEqual(sorted(top, reverse=True), [9, 8, 5])


if __name__ == '__main__':
    unittest.main()
