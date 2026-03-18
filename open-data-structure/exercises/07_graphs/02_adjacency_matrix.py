"""
Graph - Adjacency Matrix Representation
========================================

Adjacency matrix: 2D array where matrix[i][j] = 1 if edge exists.

Space: O(V²) - wasteful for sparse graphs
Add edge: O(1)
Check edge: O(1)
Get neighbors: O(V) - must scan entire row

Applications:
- Dense graphs
- When edge lookup needs to be very fast
- Graph algorithms that need matrix operations
"""


class GraphMatrix:
    """
    Directed graph using adjacency matrix.
    """

    def __init__(self, num_vertices):
        """
        Initialize graph with given number of vertices.

        Args:
            num_vertices: Number of vertices
        """
        # TODO: Create 2D matrix initialized to 0
        # Also map vertex names to indices
        pass

    def add_edge(self, from_vertex, to_vertex, weight=1):
        """
        Add a directed edge.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex
            weight: Edge weight (default 1)
        """
        # TODO: Set matrix[from_index][to_index] = weight
        pass

    def has_edge(self, from_vertex, to_vertex) -> bool:
        """
        Check if edge exists.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            True if edge exists
        """
        # TODO: Check if matrix[from_index][to_index] != 0
        pass

    def get_neighbors(self, vertex) -> list:
        """
        Get all neighbors of a vertex.

        Args:
            vertex: The vertex

        Returns:
            List of neighbors
        """
        # TODO: Scan row for non-zero entries
        pass

    def get_edge_weight(self, from_vertex, to_vertex):
        """
        Get weight of an edge.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            Edge weight, or None if no edge
        """
        # TODO: Return matrix[from_index][to_index]
        pass

    def remove_edge(self, from_vertex, to_vertex):
        """
        Remove an edge.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex
        """
        # TODO: Set matrix[from_index][to_index] = 0
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_add_edge():
    """Test adding edges"""
    g = GraphMatrix(3)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)

    assert g.has_edge(0, 1) == True
    assert g.has_edge(0, 2) == True
    assert g.has_edge(1, 0) == False  # Directed


def test_weighted_edges():
    """Test weighted edges"""
    g = GraphMatrix(3)
    g.add_edge(0, 1, weight=5)
    g.add_edge(1, 2, weight=3)

    assert g.get_edge_weight(0, 1) == 5
    assert g.get_edge_weight(1, 2) == 3
    assert g.get_edge_weight(0, 2) in [0, None]  # No edge


def test_get_neighbors():
    """Test getting neighbors"""
    g = GraphMatrix(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)

    neighbors = g.get_neighbors(0)
    assert 1 in neighbors
    assert 2 in neighbors
    assert 3 in neighbors


def test_remove_edge():
    """Test removing edges"""
    g = GraphMatrix(3)
    g.add_edge(0, 1)
    assert g.has_edge(0, 1) == True

    g.remove_edge(0, 1)
    assert g.has_edge(0, 1) == False


def test_no_edge():
    """Test checking non-existent edges"""
    g = GraphMatrix(3)
    assert g.has_edge(0, 1) == False
    assert g.has_edge(1, 2) == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
