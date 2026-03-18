"""
Treap (Tree + Heap)
===================

Combines BST property (by key) with heap property (by priority).

Each node has:
- Key (BST property: left < parent < right)
- Priority (heap property: parent.priority > children.priority)

Expected operations: O(log n)
"""

import random


class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = None
        self.right = None


class Treap:
    """Treap implementation"""

    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert with random priority"""
        # TODO: Insert and rotate to maintain heap property
        pass

    def search(self, key) -> bool:
        """Search for key"""
        # TODO: Standard BST search
        pass


# Tests
def test_insert():
    treap = Treap()
    treap.insert(10)
    assert treap.search(10) == True

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
