"""
Segment Tree
============

A segment tree allows efficient range queries and updates.

For array [a₀, a₁, ..., aₙ₋₁], supports:
- range_query(l, r): Query over range [l, r] - O(log n)
- update(i, val): Update single element - O(log n)
- build(): Build tree - O(n)

Common queries:
- Range sum
- Range minimum/maximum
- Range GCD

Structure:
- Binary tree where each node represents a range
- Leaf nodes represent single elements
- Internal nodes represent merged ranges

Applications:
- Range sum/min/max queries
- Computational geometry
- Database indexing
"""


class SegmentTree:
    """
    Segment Tree for range sum queries.

    Can be modified for other operations (min, max, GCD, etc.)
    """

    def __init__(self, arr: list):
        """
        Build segment tree from array.

        Args:
            arr: Input array

        Time Complexity: O(n)
        """
        self.n = len(arr)
        # TODO: Initialize tree array
        # Tree size = 4 * n (safe upper bound)
        # Build the tree
        pass

    def _build(self, arr: list, node: int, start: int, end: int):
        """
        Recursively build the segment tree.

        Args:
            arr: Input array
            node: Current tree node index
            start: Start of current range
            end: End of current range
        """
        # TODO: Implement recursive build
        # Base case: leaf node (start == end)
        #   tree[node] = arr[start]
        # Recursive case:
        #   mid = (start + end) // 2
        #   Build left subtree: [start, mid]
        #   Build right subtree: [mid+1, end]
        #   tree[node] = tree[left] + tree[right]  # For sum
        pass

    def query(self, l: int, r: int) -> int:
        """
        Query the sum of range [l, r].

        Args:
            l: Left index (inclusive)
            r: Right index (inclusive)

        Returns:
            Sum of elements in range [l, r]

        Time Complexity: O(log n)
        """
        # TODO: Start query from root
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """
        Recursive range query.

        Args:
            node: Current tree node
            start: Start of node's range
            end: End of node's range
            l: Query left bound
            r: Query right bound

        Returns:
            Sum of range [l, r] within [start, end]
        """
        # TODO: Implement recursive query
        # Case 1: No overlap [l, r] outside [start, end]
        #   return 0 (identity for sum)
        # Case 2: Complete overlap [l, r] contains [start, end]
        #   return tree[node]
        # Case 3: Partial overlap
        #   Query left and right subtrees
        #   Return sum of results
        pass

    def update(self, idx: int, val: int):
        """
        Update element at index to new value.

        Args:
            idx: Index to update
            val: New value

        Time Complexity: O(log n)
        """
        # TODO: Start update from root
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int):
        """
        Recursive update.

        Args:
            node: Current tree node
            start: Start of node's range
            end: End of node's range
            idx: Index to update
            val: New value
        """
        # TODO: Implement recursive update
        # Base case: Leaf node (start == end == idx)
        #   tree[node] = val
        # Recursive case:
        #   mid = (start + end) // 2
        #   Update appropriate child
        #   Recalculate current node: tree[node] = tree[left] + tree[right]
        pass


class SegmentTreeMin:
    """
    Segment Tree for range minimum queries.
    """

    def __init__(self, arr: list):
        """Build segment tree for range min"""
        # TODO: Similar to SegmentTree but use min instead of sum
        pass

    def query_min(self, l: int, r: int) -> int:
        """Query minimum in range [l, r]"""
        # TODO: Implement range min query
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_segment_tree_build():
    """Test building segment tree"""
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)

    # Query entire range
    assert st.query(0, 5) == sum(arr)


def test_range_query():
    """Test range sum queries"""
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)

    assert st.query(0, 2) == 1 + 3 + 5  # 9
    assert st.query(2, 4) == 5 + 7 + 9  # 21
    assert st.query(1, 3) == 3 + 5 + 7  # 15
    assert st.query(3, 3) == 7  # Single element


def test_update():
    """Test updating elements"""
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)

    # Update index 2 from 5 to 10
    st.update(2, 10)

    assert st.query(0, 5) == 1 + 3 + 10 + 7 + 9 + 11
    assert st.query(2, 2) == 10
    assert st.query(1, 3) == 3 + 10 + 7


def test_multiple_updates():
    """Test multiple updates"""
    arr = [1, 2, 3, 4, 5]
    st = SegmentTree(arr)

    st.update(0, 10)
    st.update(4, 50)

    assert st.query(0, 4) == 10 + 2 + 3 + 4 + 50


def test_range_min():
    """Test range minimum queries"""
    arr = [5, 2, 8, 1, 9, 3]
    st = SegmentTreeMin(arr)

    assert st.query_min(0, 5) == 1
    assert st.query_min(0, 2) == 2
    assert st.query_min(3, 5) == 1
    assert st.query_min(4, 5) == 3


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
