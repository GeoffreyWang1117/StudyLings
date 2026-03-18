"""
Graph - Adjacency List Representation
======================================

Adjacency list: Each vertex stores a list of its neighbors.

Space: O(V + E) - efficient for sparse graphs
Add edge: O(1)
Check edge: O(degree) - need to search neighbor list
Get neighbors: O(1)

Applications:
- Social networks (sparse)
- Web graphs
- Most real-world graphs are sparse
"""


class Graph:
    """
    Directed graph using adjacency list.
    """

    def __init__(self):
        """Initialize empty graph"""
        # TODO: Use a dictionary to map vertex -> list of neighbors
        pass

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.

        Args:
            vertex: The vertex to add
        """
        # TODO: Add vertex to dictionary if not present
        pass

    def add_edge(self, from_vertex, to_vertex, weight=1):
        """
        Add a directed edge.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex
            weight: Edge weight (default 1)
        """
        # TODO: Add to_vertex to from_vertex's neighbor list
        # For weighted graphs, store (to_vertex, weight) tuples
        pass

    def get_neighbors(self, vertex) -> list:
        """
        Get neighbors of a vertex.

        Args:
            vertex: The vertex

        Returns:
            List of neighbors

        Raises:
            KeyError: If vertex doesn't exist
        """
        # TODO: Return neighbor list
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
        # TODO: Check if to_vertex in from_vertex's neighbors
        pass

    def get_vertices(self) -> list:
        """Get all vertices"""
        # TODO: Return list of all vertices
        pass

    def get_edges(self) -> list:
        """
        Get all edges.

        Returns:
            List of (from, to, weight) tuples
        """
        # TODO: Collect all edges from all neighbor lists
        pass


class UndirectedGraph(Graph):
    """Undirected graph - edge goes both ways"""

    def add_edge(self, vertex1, vertex2, weight=1):
        """Add an undirected edge"""
        # TODO: Add edge in both directions
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_add_vertex():
    """Test adding vertices"""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")

    assert "A" in g.get_vertices()
    assert "B" in g.get_vertices()


def test_add_edge():
    """Test adding edges"""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")

    assert g.has_edge("A", "B") == True
    assert g.has_edge("B", "A") == False  # Directed


def test_get_neighbors():
    """Test getting neighbors"""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_edge("A", "B")
    g.add_edge("A", "C")

    neighbors = g.get_neighbors("A")
    assert "B" in [n if isinstance(n, str) else n[0] for n in neighbors]
    assert "C" in [n if isinstance(n, str) else n[0] for n in neighbors]


def test_undirected_graph():
    """Test undirected graph"""
    g = UndirectedGraph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")

    # Edge should exist in both directions
    assert g.has_edge("A", "B") == True
    assert g.has_edge("B", "A") == True


def test_weighted_edges():
    """Test weighted edges"""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", weight=5)

    neighbors = g.get_neighbors("A")
    # Should contain (vertex, weight) tuple
    assert ("B", 5) in neighbors or "B" in neighbors


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
