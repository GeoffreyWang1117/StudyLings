"""
Depth-First Search (DFS)
=========================

DFS explores as deep as possible before backtracking.

Algorithm:
1. Start at source vertex
2. Use recursion or stack
3. Mark vertices as visited
4. Explore deeply before backtracking

Time Complexity: O(V + E)
Space Complexity: O(V)

Applications:
- Cycle detection
- Topological sorting
- Finding strongly connected components
- Maze solving
"""


def dfs_recursive(graph: dict, start, visited=None) -> list:
    """
    Perform DFS traversal (recursive).

    Args:
        graph: Adjacency list
        start: Starting vertex
        visited: Set of visited vertices

    Returns:
        List of vertices in DFS order

    Time Complexity: O(V + E)
    """
    # TODO: Implement recursive DFS
    # 1. Mark current as visited
    # 2. Add to result
    # 3. Recursively visit unvisited neighbors
    pass


def dfs_iterative(graph: dict, start) -> list:
    """
    Perform DFS traversal (iterative).

    Args:
        graph: Adjacency list
        start: Starting vertex

    Returns:
        List of vertices in DFS order

    Time Complexity: O(V + E)
    """
    # TODO: Implement iterative DFS using a stack
    pass


def has_cycle(graph: dict) -> bool:
    """
    Check if directed graph has a cycle using DFS.

    Args:
        graph: Adjacency list (directed graph)

    Returns:
        True if graph has a cycle

    Time Complexity: O(V + E)
    """
    # TODO: Use DFS with three colors:
    # WHITE: unvisited
    # GRAY: visiting (on current path)
    # BLACK: visited
    # Cycle exists if we encounter GRAY vertex
    pass


def topological_sort(graph: dict) -> list:
    """
    Topological sort using DFS.

    Only works for DAG (Directed Acyclic Graph).

    Args:
        graph: Adjacency list

    Returns:
        List of vertices in topological order

    Time Complexity: O(V + E)
    """
    # TODO: Implement topological sort
    # Use DFS and prepend vertex to result when done exploring
    # Or append and reverse at end
    pass


def find_path(graph: dict, start, end) -> list:
    """
    Find any path from start to end using DFS.

    Args:
        graph: Adjacency list
        start: Start vertex
        end: End vertex

    Returns:
        A path from start to end, or None

    Time Complexity: O(V + E)
    """
    # TODO: DFS that tracks path
    # Return when end is found
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_dfs_recursive():
    """Test recursive DFS"""
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    result = dfs_recursive(graph, 'A')
    assert result[0] == 'A'
    assert len(result) == 6


def test_dfs_iterative():
    """Test iterative DFS"""
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    result = dfs_iterative(graph, 'A')
    assert result[0] == 'A'
    assert len(result) == 6


def test_has_cycle():
    """Test cycle detection"""
    # Acyclic graph
    acyclic = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    assert has_cycle(acyclic) == False

    # Cyclic graph
    cyclic = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    assert has_cycle(cyclic) == True


def test_topological_sort():
    """Test topological sorting"""
    # DAG representing task dependencies
    graph = {
        'A': ['C'],
        'B': ['C', 'D'],
        'C': ['E'],
        'D': ['E'],
        'E': []
    }

    result = topological_sort(graph)

    # A and B should come before C
    assert result.index('A') < result.index('C')
    assert result.index('B') < result.index('C')
    # C and D should come before E
    assert result.index('C') < result.index('E')
    assert result.index('D') < result.index('E')


def test_find_path():
    """Test path finding"""
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D', 'E'],
        'D': ['E'],
        'E': []
    }

    path = find_path(graph, 'A', 'E')
    assert path is not None
    assert path[0] == 'A'
    assert path[-1] == 'E'


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
