"""
Cartesian Tree
==============

A binary tree derived from a sequence that combines properties of
both a binary search tree (by index) and a heap (by value).

Properties:
- In-order traversal gives original sequence
- Heap property: parent value ≤ children values (for min-heap variant)
- Each node's value is minimum in its subtree range

Construction:
- Can be built in O(n) time using a stack
- Unique for a given sequence

Operations:
- Build: O(n)
- Range Minimum Query (RMQ): O(log n) after O(n) preprocessing
- Lowest Common Ancestor (LCA): O(log n)

Applications:
- Range Minimum Query (RMQ) in O(1) with O(n log n) preprocessing
- Suffix tree construction
- Finding all nearest smaller values
- Treap construction
"""


class CartesianNode:
    """A node in the Cartesian tree"""

    def __init__(self, index: int, value):
        self.index = index      # Position in original array
        self.value = value      # Value at that position
        self.left = None        # Left child
        self.right = None       # Right child
        self.parent = None      # Parent node


class CartesianTree:
    """
    Cartesian Tree for Range Minimum Query.

    Min-heap variant: parent.value ≤ children.value
    """

    def __init__(self, arr: list):
        """
        Build Cartesian tree from array.

        Args:
            arr: Input array

        Time Complexity: O(n)
        """
        self.arr = arr
        self.root = self._build(arr)

    def _build(self, arr: list) -> CartesianNode:
        """
        Build Cartesian tree in linear time using stack.

        Algorithm:
        - Process elements left to right
        - Use stack to maintain right spine
        - For each element, pop while top.value > current.value
        - Current becomes right child of new top
        - Last popped becomes left child of current

        Args:
            arr: Input array

        Returns:
            Root of Cartesian tree
        """
        # TODO: Implement O(n) construction
        # Use a stack to build tree efficiently
        pass

    def range_min_query(self, left: int, right: int):
        """
        Find minimum value in range [left, right].

        Args:
            left: Left index (inclusive)
            right: Right index (inclusive)

        Returns:
            Minimum value in range

        Time Complexity: O(log n) average
        """
        # TODO: Find LCA of nodes at left and right
        # Minimum is at the LCA
        pass

    def _find_lca(self, i: int, j: int) -> CartesianNode:
        """
        Find Lowest Common Ancestor of nodes at indices i and j.

        The LCA contains the minimum value in range [i, j].
        """
        # TODO: Implement LCA finding
        # Can use parent pointers or other techniques
        pass

    def verify_properties(self) -> bool:
        """
        Verify that tree satisfies Cartesian tree properties.

        Returns:
            True if valid Cartesian tree
        """
        # TODO: Verify:
        # 1. In-order gives original sequence
        # 2. Heap property holds
        return self._verify_heap(self.root) and \
               self._verify_inorder(self.root, [])

    def _verify_heap(self, node: CartesianNode) -> bool:
        """Verify min-heap property"""
        if not node:
            return True

        # Check children are not smaller
        if node.left and node.left.value < node.value:
            return False
        if node.right and node.right.value < node.value:
            return False

        return self._verify_heap(node.left) and self._verify_heap(node.right)

    def _verify_inorder(self, node: CartesianNode, result: list) -> bool:
        """Verify in-order gives original sequence"""
        if not node:
            return True

        self._verify_inorder(node.left, result)
        result.append(node.value)
        self._verify_inorder(node.right, result)

        return result == self.arr

    def find_all_nearest_smaller(self) -> tuple:
        """
        For each element, find nearest smaller element on left and right.

        Uses Cartesian tree structure.

        Returns:
            (left_smaller, right_smaller) where each is list of indices
            -1 if no smaller element exists

        Time Complexity: O(n)
        """
        # TODO: Use Cartesian tree to find nearest smaller values
        # Left smaller: parent if left child, else ancestor
        # Right smaller: symmetric
        pass


def range_minimum_query_naive(arr: list, left: int, right: int):
    """
    Naive RMQ for comparison.

    Time Complexity: O(n)
    """
    return min(arr[left:right+1])


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_build_cartesian_tree():
    """Test building Cartesian tree"""
    arr = [3, 2, 6, 1, 4, 5]
    tree = CartesianTree(arr)

    assert tree.root is not None
    assert tree.verify_properties() == True


def test_heap_property():
    """Test that heap property holds"""
    arr = [9, 3, 7, 1, 8, 12, 10, 20, 15]
    tree = CartesianTree(arr)

    # Root should have minimum value
    min_val = min(arr)
    assert tree.root.value == min_val


def test_range_min_query():
    """Test RMQ using Cartesian tree"""
    arr = [3, 2, 6, 1, 4, 5, 2, 7]
    tree = CartesianTree(arr)

    # Test various ranges
    assert tree.range_min_query(0, 3) == 1  # min of [3,2,6,1]
    assert tree.range_min_query(2, 5) == 1  # min of [6,1,4,5]
    assert tree.range_min_query(4, 7) == 2  # min of [4,5,2,7]


def test_single_element():
    """Test with single element"""
    arr = [42]
    tree = CartesianTree(arr)

    assert tree.root.value == 42
    assert tree.range_min_query(0, 0) == 42


def test_sorted_array():
    """Test with sorted array"""
    arr = [1, 2, 3, 4, 5]
    tree = CartesianTree(arr)

    # For ascending array, tree is right-skewed
    assert tree.root.value == 1
    assert tree.verify_properties() == True


def test_reverse_sorted():
    """Test with reverse sorted array"""
    arr = [5, 4, 3, 2, 1]
    tree = CartesianTree(arr)

    # For descending array, tree is left-skewed
    assert tree.root.value == 1
    assert tree.verify_properties() == True


def test_nearest_smaller():
    """Test finding nearest smaller values"""
    arr = [3, 7, 2, 8, 1, 9]
    tree = CartesianTree(arr)

    left_smaller, right_smaller = tree.find_all_nearest_smaller()

    # For 7: left smaller is 3 (index 0), right smaller is 2 (index 2)
    assert left_smaller[1] == 0
    assert right_smaller[1] == 2


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
