# I AM NOT DONE

"""
Red-Black Tree

A self-balancing binary search tree with O(log n) operations.

Your task: Implement Red-Black Tree with insert and search.
"""

from enum import Enum
from typing import Generic, Optional, TypeVar, List

T = TypeVar('T')


class Color(Enum):
    RED = 1
    BLACK = 2


class Node(Generic[T]):
    def __init__(self, value: T, color: Color = Color.RED):
        self.value = value
        self.color = color
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None


class RedBlackTree(Generic[T]):
    def __init__(self):
        self.root: Optional[Node[T]] = None
        self.size_val = 0

    def insert(self, value: T):
        # TODO: Implement insert
        pass

    def search(self, value: T) -> bool:
        # TODO: Implement search
        pass

    def size(self) -> int:
        return self.size_val

    def validate(self) -> bool:
        # TODO: Validate properties
        pass


import unittest

class TestRedBlackTree(unittest.TestCase):
    def test_insert(self):
        tree = RedBlackTree()
        tree.insert(10)
        self.assertTrue(tree.search(10))

if __name__ == '__main__':
    unittest.main()
