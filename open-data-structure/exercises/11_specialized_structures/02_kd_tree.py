"""
K-D Tree (k-Dimensional Tree)
==============================

A K-D Tree organizes points in k-dimensional space for efficient
nearest neighbor and range searches.

Structure:
- Binary tree where each level alternates splitting dimension
- Nodes contain k-dimensional points
- Left subtree: points with smaller value in split dimension
- Right subtree: points with larger value in split dimension

Operations:
- Build: O(n log n)
- Insert: O(log n) average
- Search: O(log n) average
- Nearest neighbor: O(log n) average, O(n) worst
- Range search: O(n^(1-1/k) + m) where m = points in range

Applications:
- Computer graphics (ray tracing)
- Geographic information systems (GIS)
- Machine learning (k-NN classification)
- Computer vision
- Robotics path planning
"""


import math


class KDNode:
    """A node in the K-D Tree"""

    def __init__(self, point, axis=0):
        self.point = point  # k-dimensional point (tuple)
        self.axis = axis    # splitting dimension
        self.left = None
        self.right = None


class KDTree:
    """
    K-D Tree for k-dimensional points.

    For 2D: k=2, dimensions are x and y
    For 3D: k=3, dimensions are x, y, z
    """

    def __init__(self, k=2):
        """
        Initialize K-D Tree.

        Args:
            k: Number of dimensions
        """
        self.k = k
        self.root = None

    def build(self, points: list):
        """
        Build K-D Tree from list of points.

        Args:
            points: List of k-dimensional points (tuples)

        Time Complexity: O(n log n)
        """
        # TODO: Build tree recursively
        self.root = self._build(points, 0)

    def _build(self, points: list, depth: int) -> KDNode:
        """
        Recursively build K-D Tree.

        Args:
            points: Points to include
            depth: Current depth (determines axis)

        Returns:
            Root of subtree
        """
        # TODO: Implement recursive build
        # Base case: no points, return None
        # Recursive case:
        #   axis = depth % k
        #   Sort points by axis
        #   Find median
        #   Create node with median
        #   Recursively build left and right subtrees
        pass

    def insert(self, point: tuple):
        """
        Insert a point.

        Args:
            point: k-dimensional point to insert

        Time Complexity: O(log n) average
        """
        # TODO: Insert like BST, alternating dimension
        self.root = self._insert(self.root, point, 0)

    def _insert(self, node: KDNode, point: tuple, depth: int) -> KDNode:
        """Recursive insert helper"""
        # TODO: Implement recursive insert
        pass

    def search(self, point: tuple) -> bool:
        """
        Search for exact point.

        Args:
            point: Point to search for

        Returns:
            True if point exists

        Time Complexity: O(log n) average
        """
        # TODO: Search like BST, using appropriate dimension
        pass

    def nearest_neighbor(self, target: tuple) -> tuple:
        """
        Find nearest neighbor to target point.

        Args:
            target: Query point

        Returns:
            Nearest point in tree

        Time Complexity: O(log n) average, O(n) worst
        """
        # TODO: Implement nearest neighbor search
        # Use branch and bound pruning
        best = {'point': None, 'distance': float('inf')}
        self._nearest_neighbor(self.root, target, 0, best)
        return best['point']

    def _nearest_neighbor(self, node: KDNode, target: tuple, depth: int, best: dict):
        """Recursive nearest neighbor search"""
        # TODO: Implement with pruning
        # 1. Update best if current node is closer
        # 2. Recursively search near subtree
        # 3. Check if far subtree could contain closer point
        # 4. If yes, search far subtree too
        pass

    def range_search(self, min_bounds: tuple, max_bounds: tuple) -> list:
        """
        Find all points in rectangular range.

        Args:
            min_bounds: Minimum values for each dimension
            max_bounds: Maximum values for each dimension

        Returns:
            List of points in range

        Time Complexity: O(n^(1-1/k) + m)
        """
        # TODO: Recursively search tree
        # Prune branches that don't intersect range
        result = []
        self._range_search(self.root, min_bounds, max_bounds, 0, result)
        return result

    def _range_search(self, node: KDNode, min_bounds: tuple, max_bounds: tuple,
                      depth: int, result: list):
        """Recursive range search"""
        # TODO: Check if point is in range
        # Recursively search subtrees that might contain points in range
        pass

    @staticmethod
    def distance(p1: tuple, p2: tuple) -> float:
        """Euclidean distance between two points"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_build_and_search():
    """Test building and searching"""
    tree = KDTree(k=2)
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree.build(points)

    assert tree.search((5, 4)) == True
    assert tree.search((9, 6)) == True
    assert tree.search((1, 1)) == False


def test_insert():
    """Test insertion"""
    tree = KDTree(k=2)
    tree.insert((5, 5))
    tree.insert((2, 3))
    tree.insert((8, 7))

    assert tree.search((5, 5)) == True
    assert tree.search((2, 3)) == True
    assert tree.search((8, 7)) == True


def test_nearest_neighbor():
    """Test nearest neighbor search"""
    tree = KDTree(k=2)
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree.build(points)

    # Closest to (9, 2) should be (8, 1) or (7, 2)
    nearest = tree.nearest_neighbor((9, 2))
    assert nearest in [(8, 1), (7, 2)]

    # Closest to (2, 4) should be (2, 3)
    nearest = tree.nearest_neighbor((2, 4))
    assert nearest == (2, 3)


def test_range_search():
    """Test range search"""
    tree = KDTree(k=2)
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree.build(points)

    # Search in range [4, 8] x [1, 5]
    result = tree.range_search((4, 1), (8, 5))
    result_set = set(result)

    # Should contain (5, 4), (8, 1), (7, 2)
    assert (5, 4) in result_set
    assert (8, 1) in result_set
    assert (7, 2) in result_set
    assert (9, 6) not in result_set  # Outside range


def test_3d_tree():
    """Test with 3D points"""
    tree = KDTree(k=3)
    points = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (2, 3, 4)]
    tree.build(points)

    assert tree.search((4, 5, 6)) == True
    assert tree.search((1, 1, 1)) == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
