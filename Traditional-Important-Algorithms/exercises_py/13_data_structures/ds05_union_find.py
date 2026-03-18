# I AM NOT DONE

"""
Union-Find Data Structure

Your task: Implement Union-Find.
"""

from typing import List


class UnionFind:
    def __init__(self, n: int):
        # TODO: Initialize
        pass

    def find(self, x: int) -> int:
        # TODO: Implement
        pass

    def union(self, x: int, y: int) -> bool:
        # TODO: Implement
        pass

    def connected(self, x: int, y: int) -> bool:
        # TODO: Implement
        pass


import unittest

class TestUnionFind(unittest.TestCase):
    def test_union(self):
        uf = UnionFind(5)
        uf.union(0, 1)
        self.assertTrue(uf.connected(0, 1))

if __name__ == '__main__':
    unittest.main()
