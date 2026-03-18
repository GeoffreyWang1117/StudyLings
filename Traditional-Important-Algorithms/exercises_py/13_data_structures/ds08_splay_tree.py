# I AM NOT DONE

"""
Splay Tree

Your task: Implement Splay Tree.
"""

from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None


class SplayTree(Generic[T]):
    def __init__(self):
        self.root: Optional[Node[T]] = None

    def insert(self, value: T):
        # TODO: Implement
        pass

    def search(self, value: T) -> bool:
        # TODO: Implement
        pass


import unittest

class TestSplayTree(unittest.TestCase):
    def test_insert(self):
        tree = SplayTree()
        tree.insert(10)
        self.assertTrue(tree.search(10))

if __name__ == '__main__':
    unittest.main()
