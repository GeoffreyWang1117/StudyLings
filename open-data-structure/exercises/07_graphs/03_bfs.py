"""
Breadth-First Search (BFS)
===========================

BFS explores all neighbors at distance k before distance k+1.

Algorithm:
1. Start at source vertex
2. Use a queue to track vertices to visit
3. Mark vertices as visited to avoid cycles
4. Process vertices level by level

Time Complexity: O(V + E)
Space Complexity: O(V)

Applications:
- Shortest path in unweighted graph
- Finding connected components
- Level-order traversal
- Social network connections
"""

from collections import deque


def bfs(graph: dict, start) -> list:
    """
    Perform BFS traversal.

    Args:
        graph: Adjacency list (dict of vertex -> list of neighbors)
        start: Starting vertex

    Returns:
        List of vertices in BFS order

    Time Complexity: O(V + E)
    """
    # TODO: Implement BFS
    # 1. Create queue and visited set
    # 2. Add start to queue
    # 3. While queue not empty:
    #    - Dequeue vertex
    #    - Process it
    #    - Enqueue unvisited neighbors
    pass


def shortest_path(graph: dict, start, end) -> list:
    """
    Find shortest path using BFS.

    Args:
        graph: Adjacency list
        start: Start vertex
        end: End vertex

    Returns:
        List of vertices in shortest path, or None if no path

    Time Complexity: O(V + E)
    """
    # TODO: Implement shortest path using BFS
    # Track parent of each vertex to reconstruct path
    pass


def is_bipartite(graph: dict) -> bool:
    """
    Check if graph is bipartite using BFS.

    A graph is bipartite if vertices can be colored with 2 colors
    such that no adjacent vertices have the same color.

    Args:
        graph: Adjacency list

    Returns:
        True if bipartite, False otherwise

    Time Complexity: O(V + E)
    """
    # TODO: Use BFS with 2-coloring
    # Alternate colors at each level
    pass


def count_connected_components(graph: dict) -> int:
    """
    Count number of connected components.

    Args:
        graph: Adjacency list

    Returns:
        Number of connected components

    Time Complexity: O(V + E)
    """
    # TODO: Run BFS from each unvisited vertex
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_bfs():
    """Test BFS traversal"""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    result = bfs(graph, 'A')

    # Should visit in level order
    assert result[0] == 'A'
    assert set(result[1:3]) == set(['B', 'C'])  # Level 1


def test_shortest_path():
    """Test shortest path finding"""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'E'],
        'E': ['D']
    }

    path = shortest_path(graph, 'A', 'E')
    assert len(path) == 3  # A -> D -> E or A -> B/C -> D -> E
    assert path[0] == 'A'
    assert path[-1] == 'E'


def test_shortest_path_no_path():
    """Test when no path exists"""
    graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C']
    }

    path = shortest_path(graph, 'A', 'C')
    assert path is None


def test_is_bipartite():
    """Test bipartite checking"""
    # Bipartite graph (square)
    bipartite = {
        'A': ['B', 'D'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['A', 'C']
    }
    assert is_bipartite(bipartite) == True

    # Not bipartite (triangle)
    not_bipartite = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']
    }
    assert is_bipartite(not_bipartite) == False


def test_connected_components():
    """Test counting connected components"""
    graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C'],
        'E': []
    }

    assert count_connected_components(graph) == 3  # {A,B}, {C,D}, {E}


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
