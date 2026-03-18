"""
Fenwick Tree (Binary Indexed Tree)
===================================

A Fenwick Tree efficiently computes prefix sums with updates.

Operations:
- update(i, delta): Add delta to element i - O(log n)
- prefix_sum(i): Sum of elements [0, i] - O(log n)
- range_sum(l, r): Sum of range [l, r] - O(log n)

More space-efficient than Segment Tree for simple operations.

Key insight: Use binary representation to efficiently navigate tree.
- Each index i is responsible for range [i - (i & -i) + 1, i]
- i & -i extracts the lowest set bit

Applications:
- Prefix sum with updates
- Counting inversions
- Range updates (with difference array)
- 2D range queries
"""


class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for prefix sums.

    1-indexed internally for simpler bit operations.
    """

    def __init__(self, n: int):
        """
        Initialize Fenwick Tree for n elements.

        Args:
            n: Number of elements

        Time Complexity: O(n)
        """
        # TODO: Initialize tree array
        # Use 1-indexed array (size n+1)
        pass

    def update(self, i: int, delta: int):
        """
        Add delta to element at index i.

        Args:
            i: Index (0-indexed for user)
            delta: Value to add

        Time Complexity: O(log n)
        """
        # TODO: Implement update
        # Convert to 1-indexed: i += 1
        # While i <= n:
        #   tree[i] += delta
        #   i += (i & -i)  # Move to next responsible index
        pass

    def prefix_sum(self, i: int) -> int:
        """
        Calculate sum of elements [0, i].

        Args:
            i: End index (0-indexed, inclusive)

        Returns:
            Sum of elements from 0 to i

        Time Complexity: O(log n)
        """
        # TODO: Implement prefix sum
        # Convert to 1-indexed: i += 1
        # result = 0
        # While i > 0:
        #   result += tree[i]
        #   i -= (i & -i)  # Move to parent
        pass

    def range_sum(self, l: int, r: int) -> int:
        """
        Calculate sum of range [l, r].

        Args:
            l: Left index (inclusive)
            r: Right index (inclusive)

        Returns:
            Sum of elements in range [l, r]

        Time Complexity: O(log n)
        """
        # TODO: Use prefix sum
        # range_sum(l, r) = prefix_sum(r) - prefix_sum(l-1)
        pass

    @staticmethod
    def build_from_array(arr: list):
        """
        Build Fenwick Tree from existing array.

        Args:
            arr: Input array

        Returns:
            FenwickTree initialized with array values

        Time Complexity: O(n log n)
        """
        # TODO: Create tree and update each element
        pass


def count_inversions(arr: list) -> int:
    """
    Count inversions in array using Fenwick Tree.

    An inversion is a pair (i, j) where i < j but arr[i] > arr[j].

    Args:
        arr: Input array

    Returns:
        Number of inversions

    Time Complexity: O(n log n)
    """
    # TODO: Use Fenwick Tree to count inversions
    # 1. Coordinate compression (map values to indices)
    # 2. Process elements right to left
    # 3. For each element, count how many smaller elements seen so far
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_prefix_sum():
    """Test prefix sum queries"""
    ft = FenwickTree(6)

    # Add elements: [1, 3, 5, 7, 9, 11]
    for i, val in enumerate([1, 3, 5, 7, 9, 11]):
        ft.update(i, val)

    assert ft.prefix_sum(0) == 1
    assert ft.prefix_sum(2) == 1 + 3 + 5
    assert ft.prefix_sum(5) == 1 + 3 + 5 + 7 + 9 + 11


def test_range_sum():
    """Test range sum queries"""
    ft = FenwickTree(6)

    for i, val in enumerate([1, 3, 5, 7, 9, 11]):
        ft.update(i, val)

    assert ft.range_sum(0, 2) == 1 + 3 + 5
    assert ft.range_sum(2, 4) == 5 + 7 + 9
    assert ft.range_sum(1, 3) == 3 + 5 + 7


def test_update():
    """Test updating values"""
    ft = FenwickTree(5)

    # Initialize: [1, 2, 3, 4, 5]
    for i in range(5):
        ft.update(i, i + 1)

    # Add 10 to index 2
    ft.update(2, 10)

    assert ft.prefix_sum(4) == 1 + 2 + 13 + 4 + 5
    assert ft.range_sum(2, 2) == 13


def test_build_from_array():
    """Test building from array"""
    arr = [1, 3, 5, 7, 9, 11]
    ft = FenwickTree.build_from_array(arr)

    assert ft.prefix_sum(2) == 1 + 3 + 5
    assert ft.range_sum(1, 4) == 3 + 5 + 7 + 9


def test_empty_range():
    """Test edge cases"""
    ft = FenwickTree(5)

    for i in range(5):
        ft.update(i, i + 1)

    # Single element range
    assert ft.range_sum(2, 2) == 3

    # First element
    assert ft.range_sum(0, 0) == 1


def test_count_inversions():
    """Test counting inversions"""
    # [3, 1, 2] has 2 inversions: (3,1) and (3,2)
    assert count_inversions([3, 1, 2]) == 2

    # Sorted array has 0 inversions
    assert count_inversions([1, 2, 3, 4]) == 0

    # Reverse sorted has maximum inversions
    arr = [4, 3, 2, 1]
    # Inversions: (4,3), (4,2), (4,1), (3,2), (3,1), (2,1) = 6
    assert count_inversions(arr) == 6


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
