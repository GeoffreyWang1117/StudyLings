# I AM NOT DONE

"""
db01_btree.py

B-Tree is a self-balancing tree data structure that maintains sorted data and allows
searches, sequential access, insertions, and deletions in logarithmic time. B-Trees
are commonly used in databases and file systems because they minimize disk I/O operations.

A B-Tree of order M has the following properties:
- Every node has at most M children
- Every non-leaf node (except root) has at least M/2 children
- The root has at least 2 children if it's not a leaf node
- All leaves appear at the same level
- A non-leaf node with k children contains k-1 keys

Your task: Implement a B-Tree with insert, search, and split operations.
"""

import unittest
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')
ORDER = 4  # Maximum number of children per node


class BTreeNode(Generic[T]):
    """A node in the B-Tree."""
    
    def __init__(self, is_leaf: bool = True):
        self.keys: List[T] = []
        self.children: List['BTreeNode[T]'] = []
        self.is_leaf = is_leaf
    
    def is_full(self) -> bool:
        return len(self.keys) >= ORDER - 1


class BTree(Generic[T]):
    """B-Tree implementation."""
    
    def __init__(self):
        self.root: Optional[BTreeNode[T]] = None
    
    def search(self, key: T) -> bool:
        """
        TODO: Implement search operation.
        Traverse the tree from root to find the key.
        Return True if found, False otherwise.
        """
        pass
    
    def insert(self, key: T) -> None:
        """
        TODO: Implement insert operation.
        If root is None, create a new root.
        If root is full, split it and create a new root.
        Otherwise, insert into the appropriate subtree.
        """
        pass
    
    def _insert_non_full(self, node: BTreeNode[T], key: T) -> None:
        """
        TODO: Insert key into a non-full node.
        Find the correct position for the key.
        If leaf, insert directly.
        If internal node, recursively insert into the appropriate child.
        """
        pass
    
    def _split_child(self, parent: BTreeNode[T], index: int) -> None:
        """
        TODO: Split the child at the given index.
        Create a new node to hold half of the keys.
        Move the median key up to the parent.
        Redistribute keys and children between the two nodes.
        """
        pass
    
    def height(self) -> int:
        """TODO: Return the height of the tree."""
        pass
    
    def inorder_traversal(self) -> List[T]:
        """TODO: Return keys in sorted order."""
        pass


class TestBTree(unittest.TestCase):
    """Comprehensive test cases for B-Tree."""
    
    def test_create_empty_btree(self):
        """Test creating empty B-Tree."""
        btree = BTree()
        self.assertEqual(btree.height(), 0)
    
    def test_insert_single_key(self):
        """Test inserting a single key."""
        btree = BTree()
        btree.insert(10)
        self.assertTrue(btree.search(10))
        self.assertFalse(btree.search(20))
    
    def test_insert_multiple_keys(self):
        """Test inserting multiple keys."""
        btree = BTree()
        for i in [5, 15, 25, 35, 45]:
            btree.insert(i)
        self.assertTrue(btree.search(15))
        self.assertTrue(btree.search(45))
        self.assertFalse(btree.search(100))
    
    def test_insert_triggers_split(self):
        """Test that inserting enough keys triggers a split."""
        btree = BTree()
        for i in range(1, 11):
            btree.insert(i * 10)
        for i in range(1, 11):
            self.assertTrue(btree.search(i * 10))
    
    def test_search_non_existent_keys(self):
        """Test searching for non-existent keys."""
        btree = BTree()
        btree.insert(10)
        btree.insert(20)
        btree.insert(30)
        self.assertFalse(btree.search(5))
        self.assertFalse(btree.search(15))
        self.assertFalse(btree.search(40))
    
    def test_inorder_traversal(self):
        """Test inorder traversal returns sorted keys."""
        btree = BTree()
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            btree.insert(key)
        result = btree.inorder_traversal()
        self.assertEqual(result, [20, 30, 40, 50, 60, 70, 80])
    
    def test_insert_duplicate_keys(self):
        """Test inserting duplicate keys."""
        btree = BTree()
        btree.insert(10)
        btree.insert(10)
        self.assertTrue(btree.search(10))
    
    def test_height_increases_with_splits(self):
        """Test that height increases as tree grows."""
        btree = BTree()
        btree.insert(1)
        initial_height = btree.height()
        for i in range(2, 21):
            btree.insert(i)
        self.assertGreaterEqual(btree.height(), initial_height)
    
    def test_large_dataset(self):
        """Test with large dataset."""
        btree = BTree()
        for i in range(100):
            btree.insert(i)
        for i in range(100):
            self.assertTrue(btree.search(i))
        self.assertFalse(btree.search(100))
    
    def test_insert_reverse_order(self):
        """Test inserting in reverse order."""
        btree = BTree()
        for i in range(10, 0, -1):
            btree.insert(i)
        for i in range(1, 11):
            self.assertTrue(btree.search(i))
        result = btree.inorder_traversal()
        self.assertEqual(result, list(range(1, 11)))


if __name__ == '__main__':
    unittest.main()
