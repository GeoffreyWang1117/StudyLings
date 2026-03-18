# I AM NOT DONE

"""
AVL Tree - Self-balancing BST

Your task: Implement AVL Tree.
"""

from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None
        self.height = 1


class AVLTree(Generic[T]):
    def __init__(self):
        self.root: Optional[Node[T]] = None

    def insert(self, value: T):
        # TODO: Implement
        pass

    def search(self, value: T) -> bool:
        # TODO: Implement
        pass


import unittest

class TestAVLTree(unittest.TestCase):
    def test_insert(self):
        tree = AVLTree()
        tree.insert(10)
        self.assertTrue(tree.search(10))

if __name__ == '__main__':
    unittest.main()
