# I AM NOT DONE

"""
Treap (Tree + Heap)

Your task: Implement Treap.
"""

from typing import Generic, Optional, TypeVar
import random

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.priority = random.random()
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None


class Treap(Generic[T]):
    def __init__(self):
        self.root: Optional[Node[T]] = None

    def insert(self, value: T):
        # TODO: Implement
        pass

    def search(self, value: T) -> bool:
        # TODO: Implement
        pass


import unittest

class TestTreap(unittest.TestCase):
    def test_insert(self):
        tree = Treap()
        tree.insert(10)
        self.assertTrue(tree.search(10))

if __name__ == '__main__':
    unittest.main()
