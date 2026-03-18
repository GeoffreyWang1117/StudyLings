"""
Union-Find (Disjoint Set Union)
================================

Union-Find tracks a partition of elements into disjoint sets.

Operations:
- find(x): Find which set x belongs to - O(α(n)) amortized
- union(x, y): Merge sets containing x and y - O(α(n)) amortized

Where α(n) is inverse Ackermann function, effectively O(1).

Optimizations:
1. Path compression: Make tree flat during find
2. Union by rank: Attach smaller tree under larger

Applications:
- Kruskal's MST algorithm
- Detecting cycles in graphs
- Connected components
- Image segmentation
- Network connectivity
"""


class UnionFind:
    """
    Union-Find with path compression and union by rank.
    """

    def __init__(self, n: int):
        """
        Initialize with n elements (0 to n-1).

        Args:
            n: Number of elements

        Time Complexity: O(n)
        """
        # TODO: Initialize data structures
        # parent[i] = parent of element i
        # rank[i] = approximate depth of tree rooted at i
        pass

    def find(self, x: int) -> int:
        """
        Find the root (representative) of x's set.

        With path compression: make all nodes on path point to root.

        Args:
            x: The element

        Returns:
            The root of x's set

        Time Complexity: O(α(n)) amortized
        """
        # TODO: Implement find with path compression
        # If x is not its own parent:
        #   - Recursively find root
        #   - Update parent[x] to root (path compression)
        pass

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing x and y.

        With union by rank: attach smaller tree under larger.

        Args:
            x: First element
            y: Second element

        Returns:
            True if sets were merged, False if already in same set

        Time Complexity: O(α(n)) amortized
        """
        # TODO: Implement union by rank
        # 1. Find roots of x and y
        # 2. If same root, already connected
        # 3. Otherwise, attach smaller tree under larger (by rank)
        pass

    def connected(self, x: int, y: int) -> bool:
        """
        Check if x and y are in the same set.

        Args:
            x: First element
            y: Second element

        Returns:
            True if in same set

        Time Complexity: O(α(n))
        """
        # TODO: Check if find(x) == find(y)
        pass

    def count_sets(self) -> int:
        """
        Count the number of disjoint sets.

        Returns:
            Number of sets

        Time Complexity: O(n)
        """
        # TODO: Count unique roots
        pass


def has_cycle_undirected(edges: list, n: int) -> bool:
    """
    Detect cycle in undirected graph using Union-Find.

    Args:
        edges: List of (u, v) edges
        n: Number of vertices

    Returns:
        True if graph has a cycle

    Time Complexity: O(E * α(V))
    """
    # TODO: Use Union-Find
    # For each edge (u, v):
    #   If u and v already connected, cycle exists
    #   Otherwise, union them
    pass


def count_connected_components(edges: list, n: int) -> int:
    """
    Count connected components using Union-Find.

    Args:
        edges: List of (u, v) edges
        n: Number of vertices

    Returns:
        Number of connected components

    Time Complexity: O(E * α(V))
    """
    # TODO: Use Union-Find
    # Process all edges
    # Count number of sets
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_basic_union_find():
    """Test basic operations"""
    uf = UnionFind(5)

    # Initially all separate
    assert uf.connected(0, 1) == False

    # Union 0 and 1
    uf.union(0, 1)
    assert uf.connected(0, 1) == True

    # Union 1 and 2 (should connect 0, 1, 2)
    uf.union(1, 2)
    assert uf.connected(0, 2) == True


def test_union_by_rank():
    """Test union by rank optimization"""
    uf = UnionFind(10)

    # Create two sets
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(2, 3)

    uf.union(5, 6)
    uf.union(6, 7)

    # Merge the two sets
    uf.union(3, 5)

    # All should be connected
    for i in range(8):
        for j in range(8):
            if i <= 3 or i >= 5:
                if j <= 3 or j >= 5:
                    assert uf.connected(i, j) == True


def test_count_sets():
    """Test counting disjoint sets"""
    uf = UnionFind(6)

    assert uf.count_sets() == 6  # All separate

    uf.union(0, 1)
    uf.union(2, 3)
    assert uf.count_sets() == 4  # {0,1}, {2,3}, {4}, {5}

    uf.union(1, 2)
    assert uf.count_sets() == 3  # {0,1,2,3}, {4}, {5}


def test_cycle_detection():
    """Test cycle detection in undirected graph"""
    # Graph with cycle: 0-1-2-0
    edges_with_cycle = [(0, 1), (1, 2), (2, 0)]
    assert has_cycle_undirected(edges_with_cycle, 3) == True

    # Graph without cycle (tree)
    edges_without_cycle = [(0, 1), (1, 2), (1, 3)]
    assert has_cycle_undirected(edges_without_cycle, 4) == False


def test_connected_components():
    """Test counting connected components"""
    # Two components: {0,1,2} and {3,4}
    edges = [(0, 1), (1, 2), (3, 4)]
    assert count_connected_components(edges, 5) == 2

    # One component
    edges = [(0, 1), (1, 2), (2, 3)]
    assert count_connected_components(edges, 4) == 1


def test_path_compression():
    """Test that path compression works"""
    uf = UnionFind(10)

    # Create a long chain
    for i in range(9):
        uf.union(i, i + 1)

    # After find, path should be compressed
    root = uf.find(0)
    assert uf.find(9) == root
    # All should have same root
    for i in range(10):
        assert uf.find(i) == root


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
