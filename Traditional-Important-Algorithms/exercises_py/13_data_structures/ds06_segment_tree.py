# I AM NOT DONE

"""
Segment Tree

Your task: Implement Segment Tree.
"""

from typing import List, Callable


class SegmentTree:
    def __init__(self, arr: List[int]):
        # TODO: Build tree
        pass

    def query(self, left: int, right: int) -> int:
        # TODO: Range query
        pass

    def update(self, index: int, value: int):
        # TODO: Update value
        pass


import unittest

class TestSegmentTree(unittest.TestCase):
    def test_query(self):
        tree = SegmentTree([1, 2, 3, 4])
        self.assertEqual(tree.query(0, 3), 10)

if __name__ == '__main__':
    unittest.main()
