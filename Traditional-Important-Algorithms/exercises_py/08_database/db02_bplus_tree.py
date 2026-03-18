# I AM NOT DONE

"""
db02_bplus_tree.py

B+ Tree is a variation of B-Tree where all values are stored in leaf nodes,
and leaf nodes are linked together to allow efficient range queries.
Internal nodes only store keys for navigation.

Key differences from B-Tree:
- All data is stored in leaf nodes
- Leaf nodes are linked together (doubly linked list)
- Internal nodes only contain keys and child pointers
- Better for range queries and sequential access

Your task: Implement a B+ Tree with leaf node linking for efficient range queries.
"""

import unittest
from typing import List, Optional, TypeVar, Generic, Tuple

K = TypeVar('K')
V = TypeVar('V')
ORDER = 4


class BPlusTreeNode(Generic[K, V]):
    """A node in the B+ Tree."""
    
    def __init__(self, is_leaf: bool = True):
        self.keys: List[K] = []
        self.is_leaf = is_leaf
        # For internal nodes
        self.children: List['BPlusTreeNode[K, V]'] = []
        # For leaf nodes
        self.values: List[V] = []
        self.next: Optional['BPlusTreeNode[K, V]'] = None


class BPlusTree(Generic[K, V]):
    """B+ Tree implementation."""
    
    def __init__(self):
        self.root: Optional[BPlusTreeNode[K, V]] = None
    
    def insert(self, key: K, value: V) -> None:
        """
        TODO: Implement insert operation.
        If root is None, create a new leaf node.
        If root is full, split it and create a new internal root.
        Navigate to the appropriate leaf and insert the key-value pair.
        """
        pass
    
    def search(self, key: K) -> Optional[V]:
        """
        TODO: Search for a key and return its value.
        Navigate through internal nodes to find the leaf.
        Search in the leaf node for the key.
        """
        pass
    
    def range_query(self, start: K, end: K) -> List[Tuple[K, V]]:
        """
        TODO: Return all key-value pairs in the range [start, end].
        Find the leaf containing start.
        Traverse linked leaf nodes until we exceed end.
        Collect all matching key-value pairs.
        """
        pass
    
    def _find_leaf(self, key: K) -> Optional[BPlusTreeNode[K, V]]:
        """
        TODO: Navigate to the leaf node that should contain the key.
        """
        pass
    
    def inorder_keys(self) -> List[K]:
        """
        TODO: Return all keys in sorted order by traversing leaf nodes.
        """
        pass
    
    def height(self) -> int:
        """TODO: Return the height of the tree."""
        pass


class TestBPlusTree(unittest.TestCase):
    """Comprehensive test cases for B+ Tree."""
    
    def test_create_empty_bplus_tree(self):
        """Test creating empty B+ Tree."""
        tree = BPlusTree()
        self.assertEqual(tree.height(), 0)
    
    def test_insert_and_search(self):
        """Test insert and search."""
        tree = BPlusTree()
        tree.insert(10, "ten")
        tree.insert(20, "twenty")
        self.assertEqual(tree.search(10), "ten")
        self.assertEqual(tree.search(20), "twenty")
        self.assertIsNone(tree.search(30))
    
    def test_insert_multiple_values(self):
        """Test inserting multiple values."""
        tree = BPlusTree()
        for i in range(1, 11):
            tree.insert(i, f"value_{i}")
        for i in range(1, 11):
            self.assertEqual(tree.search(i), f"value_{i}")
    
    def test_range_query_basic(self):
        """Test basic range query."""
        tree = BPlusTree()
        for i in range(1, 11):
            tree.insert(i, i * 10)
        result = tree.range_query(3, 7)
        self.assertEqual(len(result), 5)
        for k, v in result:
            self.assertGreaterEqual(k, 3)
            self.assertLessEqual(k, 7)
            self.assertEqual(v, k * 10)
    
    def test_range_query_empty_range(self):
        """Test range query with empty range."""
        tree = BPlusTree()
        tree.insert(10, 100)
        tree.insert(20, 200)
        result = tree.range_query(15, 15)
        self.assertTrue(len(result) == 0 or len(result) == 1)
    
    def test_range_query_all_elements(self):
        """Test range query covering all elements."""
        tree = BPlusTree()
        for i in range(1, 6):
            tree.insert(i, i * 2)
        result = tree.range_query(1, 5)
        self.assertEqual(len(result), 5)
    
    def test_inorder_keys(self):
        """Test inorder key traversal."""
        tree = BPlusTree()
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            tree.insert(key, key)
        result = tree.inorder_keys()
        self.assertEqual(result, [20, 30, 40, 50, 60, 70, 80])
    
    def test_update_existing_key(self):
        """Test updating existing key."""
        tree = BPlusTree()
        tree.insert(10, "first")
        tree.insert(10, "second")
        self.assertEqual(tree.search(10), "second")
    
    def test_large_dataset(self):
        """Test with large dataset."""
        tree = BPlusTree()
        for i in range(100):
            tree.insert(i, i * 2)
        for i in range(100):
            self.assertEqual(tree.search(i), i * 2)
    
    def test_range_query_with_large_dataset(self):
        """Test range query with large dataset."""
        tree = BPlusTree()
        for i in range(50):
            tree.insert(i, i)
        result = tree.range_query(10, 20)
        self.assertEqual(len(result), 11)
        for k, v in result:
            self.assertGreaterEqual(k, 10)
            self.assertLessEqual(k, 20)
            self.assertEqual(k, v)
    
    def test_reverse_insertion_order(self):
        """Test inserting in reverse order."""
        tree = BPlusTree()
        for i in range(10, 0, -1):
            tree.insert(i, i)
        keys = tree.inorder_keys()
        self.assertEqual(keys, list(range(1, 11)))
    
    def test_range_query_beyond_bounds(self):
        """Test range query beyond tree bounds."""
        tree = BPlusTree()
        for i in range(10, 21):
            tree.insert(i, i)
        result = tree.range_query(1, 100)
        self.assertEqual(len(result), 11)


if __name__ == '__main__':
    unittest.main()
