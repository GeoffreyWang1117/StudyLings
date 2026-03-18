"""
Interval Tree
=============

An interval tree stores intervals and efficiently queries overlaps.

Each node stores:
- An interval [low, high]
- Maximum high value in subtree

Operations:
- insert(interval): O(log n)
- delete(interval): O(log n)
- search_overlap(interval): Find any overlapping interval - O(log n)
- find_all_overlaps(interval): Find all overlapping intervals - O(k + log n)

Where k = number of overlaps found.

Applications:
- Calendar scheduling (finding conflicts)
- Computational geometry
- Window management systems
- Resource allocation
- Gene sequencing
"""


class Interval:
    """Represents an interval [low, high]"""

    def __init__(self, low, high):
        self.low = low
        self.high = high

    def overlaps(self, other) -> bool:
        """Check if this interval overlaps with other"""
        # TODO: Intervals overlap if:
        # self.low <= other.high and other.low <= self.high
        pass

    def __repr__(self):
        return f"[{self.low}, {self.high}]"


class IntervalTreeNode:
    """A node in the interval tree"""

    def __init__(self, interval: Interval):
        self.interval = interval
        self.max_high = interval.high  # Max high in subtree
        self.left = None
        self.right = None


class IntervalTree:
    """
    Interval Tree based on BST ordered by interval.low.
    """

    def __init__(self):
        """Initialize empty interval tree"""
        self.root = None

    def insert(self, interval: Interval):
        """
        Insert an interval.

        Args:
            interval: The interval to insert

        Time Complexity: O(log n) average
        """
        # TODO: Insert like BST, ordered by interval.low
        # Update max_high on path
        self.root = self._insert(self.root, interval)

    def _insert(self, node: IntervalTreeNode, interval: Interval) -> IntervalTreeNode:
        """Recursive insert helper"""
        # TODO: Implement recursive insert
        # Base case: node is None, create new node
        # Recursive case: compare interval.low with node.interval.low
        # Update node.max_high = max(node.max_high, interval.high)
        pass

    def search_overlap(self, interval: Interval):
        """
        Find any interval that overlaps with given interval.

        Args:
            interval: The query interval

        Returns:
            An overlapping interval, or None if no overlap

        Time Complexity: O(log n)
        """
        # TODO: Implement overlap search
        # Start from root
        # If current interval overlaps, return it
        # If left child exists and left.max_high >= interval.low:
        #   Search left (might have overlap)
        # Else:
        #   Search right
        return self._search_overlap(self.root, interval)

    def _search_overlap(self, node: IntervalTreeNode, interval: Interval):
        """Recursive overlap search"""
        # TODO: Implement recursive search
        pass

    def find_all_overlaps(self, interval: Interval) -> list:
        """
        Find all intervals that overlap with given interval.

        Args:
            interval: The query interval

        Returns:
            List of all overlapping intervals

        Time Complexity: O(k + log n) where k = number of overlaps
        """
        # TODO: Traverse tree and collect all overlaps
        result = []
        self._find_all_overlaps(self.root, interval, result)
        return result

    def _find_all_overlaps(self, node: IntervalTreeNode, interval: Interval, result: list):
        """Recursive helper to find all overlaps"""
        # TODO: Check current node
        # Recursively check left and right subtrees
        # Prune search using max_high
        pass

    def delete(self, interval: Interval) -> bool:
        """
        Delete an interval.

        Args:
            interval: The interval to delete

        Returns:
            True if deleted, False if not found

        Time Complexity: O(log n)
        """
        # TODO: Implement delete (similar to BST delete)
        # Update max_high values on path
        pass


def find_meeting_conflicts(meetings: list) -> list:
    """
    Find all pairs of conflicting meetings.

    Args:
        meetings: List of (start, end) tuples

    Returns:
        List of conflicting pairs

    Time Complexity: O(n log n + k) where k = conflicts
    """
    # TODO: Use interval tree
    # Insert intervals one by one
    # For each, find overlaps with previously inserted
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_interval_overlap():
    """Test interval overlap detection"""
    i1 = Interval(15, 20)
    i2 = Interval(10, 30)
    i3 = Interval(25, 35)

    assert i1.overlaps(i2) == True
    assert i1.overlaps(i3) == False
    assert i2.overlaps(i3) == True


def test_insert_and_search():
    """Test basic insert and search"""
    tree = IntervalTree()
    tree.insert(Interval(15, 20))
    tree.insert(Interval(10, 30))
    tree.insert(Interval(17, 19))

    # Query [14, 16] should overlap with [10, 30] and [15, 20]
    result = tree.search_overlap(Interval(14, 16))
    assert result is not None


def test_search_no_overlap():
    """Test search when no overlap"""
    tree = IntervalTree()
    tree.insert(Interval(15, 20))
    tree.insert(Interval(10, 12))
    tree.insert(Interval(25, 30))

    # Query [21, 24] doesn't overlap any
    result = tree.search_overlap(Interval(21, 24))
    assert result is None


def test_find_all_overlaps():
    """Test finding all overlapping intervals"""
    tree = IntervalTree()
    intervals = [
        Interval(15, 20),
        Interval(10, 30),
        Interval(17, 19),
        Interval(5, 20),
        Interval(12, 15)
    ]

    for interval in intervals:
        tree.insert(interval)

    # Query [14, 16]
    overlaps = tree.find_all_overlaps(Interval(14, 16))

    # Should overlap with [15,20], [10,30], [5,20], [12,15]
    assert len(overlaps) >= 3  # At least 3 overlaps


def test_meeting_conflicts():
    """Test finding meeting conflicts"""
    meetings = [
        (9, 10),   # Meeting 1
        (9, 11),   # Meeting 2 - conflicts with 1
        (10, 12),  # Meeting 3 - conflicts with 2
        (13, 14),  # Meeting 4 - no conflict
    ]

    conflicts = find_meeting_conflicts(meetings)

    # Should find at least 2 conflicts: (1,2) and (2,3)
    assert len(conflicts) >= 2


def test_interval_tree_efficiency():
    """Test with many intervals"""
    tree = IntervalTree()

    # Insert 100 intervals
    for i in range(100):
        tree.insert(Interval(i * 10, i * 10 + 5))

    # Search should be fast (O(log n))
    result = tree.search_overlap(Interval(250, 255))
    assert result is not None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
