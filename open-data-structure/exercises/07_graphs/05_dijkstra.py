"""
Dijkstra's Shortest Path Algorithm
===================================

Finds shortest path in weighted graph with non-negative weights.

Algorithm:
1. Initialize distances (source = 0, others = ∞)
2. Use min-heap to always process closest unvisited vertex
3. For each neighbor, update distance if shorter path found
4. Repeat until all vertices processed

Time Complexity: O((V + E) log V) with binary heap
Space Complexity: O(V)

Applications:
- GPS navigation
- Network routing
- Social network connections
"""

import heapq


def dijkstra(graph: dict, start):
    """
    Find shortest paths from start to all vertices.

    Args:
        graph: Adjacency list with weights
               Format: {vertex: [(neighbor, weight), ...]}
        start: Starting vertex

    Returns:
        Dictionary mapping each vertex to its shortest distance

    Time Complexity: O((V + E) log V)
    """
    # TODO: Implement Dijkstra's algorithm
    # 1. Initialize distances (all infinity except start = 0)
    # 2. Use min-heap with (distance, vertex) tuples
    # 3. While heap not empty:
    #    - Pop vertex with minimum distance
    #    - For each neighbor:
    #      - Calculate new distance
    #      - If shorter, update and add to heap
    pass


def dijkstra_path(graph: dict, start, end):
    """
    Find shortest path from start to end.

    Args:
        graph: Adjacency list with weights
        start: Start vertex
        end: End vertex

    Returns:
        Tuple of (distance, path), or (None, None) if no path

    Time Complexity: O((V + E) log V)
    """
    # TODO: Implement Dijkstra with path reconstruction
    # Track parent of each vertex to rebuild path
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_dijkstra_simple():
    """Test Dijkstra on simple graph"""
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 8), ('E', 10)],
        'D': [('E', 2)],
        'E': []
    }

    distances = dijkstra(graph, 'A')

    assert distances['A'] == 0
    assert distances['B'] == 4
    assert distances['C'] == 2
    assert distances['D'] == 9  # A -> B -> D
    assert distances['E'] == 11  # A -> B -> D -> E


def test_dijkstra_path():
    """Test finding actual path"""
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }

    distance, path = dijkstra_path(graph, 'A', 'D')

    assert distance == 4  # A -> B -> C -> D
    assert path == ['A', 'B', 'C', 'D']


def test_dijkstra_no_path():
    """Test when no path exists"""
    graph = {
        'A': [('B', 1)],
        'B': [],
        'C': [('D', 1)],
        'D': []
    }

    distances = dijkstra(graph, 'A')
    assert distances['A'] == 0
    assert distances['B'] == 1
    assert distances.get('C') == float('inf') or 'C' not in distances


def test_dijkstra_direct_vs_indirect():
    """Test choosing shorter indirect path"""
    graph = {
        'A': [('B', 1), ('C', 10)],
        'B': [('C', 1)],
        'C': []
    }

    distances = dijkstra(graph, 'A')

    # A -> B -> C (cost 2) is better than A -> C (cost 10)
    assert distances['C'] == 2


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
