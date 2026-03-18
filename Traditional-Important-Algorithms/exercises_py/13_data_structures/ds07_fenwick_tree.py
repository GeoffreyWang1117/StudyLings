# I AM NOT DONE

"""
Fenwick Tree (Binary Indexed Tree)

Your task: Implement Fenwick Tree.
"""

from typing import List


class FenwickTree:
    def __init__(self, n: int):
        # TODO: Initialize
        pass

    def update(self, index: int, delta: int):
        # TODO: Update
        pass

    def prefix_sum(self, index: int) -> int:
        # TODO: Compute prefix sum
        pass

    def range_sum(self, left: int, right: int) -> int:
        # TODO: Compute range sum
        pass


import unittest

class TestFenwickTree(unittest.TestCase):
    def test_update_and_sum(self):
        tree = FenwickTree(5)
        tree.update(0, 1)
        tree.update(1, 2)
        self.assertEqual(tree.prefix_sum(1), 3)

if __name__ == '__main__':
    unittest.main()
