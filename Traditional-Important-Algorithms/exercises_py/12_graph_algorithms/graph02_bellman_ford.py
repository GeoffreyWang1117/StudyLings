# I AM NOT DONE

"""
Bellman-Ford Shortest Path Algorithm

Bellman-Ford finds shortest paths from a source vertex to all other vertices,
even when the graph contains negative edge weights. It can also detect negative
weight cycles, which make shortest paths undefined.

Time Complexity: O(V * E) where V = vertices, E = edges
Space Complexity: O(V) for distance and predecessor arrays

Key concepts:
- Relaxation: Update distances by checking all edges repeatedly
- V-1 iterations guarantee shortest paths if no negative cycles exist
- Extra iteration detects negative cycles
- Slower than Dijkstra but handles negative weights

Your task: Implement Bellman-Ford algorithm with negative cycle detection.
"""

from typing import List, Optional, Tuple


class Edge:
    """Represents a directed edge in the graph"""

    def __init__(self, from_node: int, to_node: int, weight: int):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Graph:
    """Weighted directed graph using edge list representation"""

    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.edges: List[Edge] = []

    def add_edge(self, from_node: int, to_node: int, weight: int):
        """Add a directed edge to the edge list"""
        # TODO: Add a directed edge to the edge list
        pass

    def add_undirected_edge(self, u: int, v: int, weight: int):
        """Add edges in both directions"""
        # TODO: Add edges in both directions
        pass

    def bellman_ford(self, start: int) -> Tuple[bool, List[Optional[int]], List[Optional[int]]]:
        """
        Run Bellman-Ford algorithm from start vertex

        Returns:
            Tuple of (success, distances, predecessors)
            - success: True if no negative cycle, False otherwise
            - distances[i]: shortest distance from start to i (None if unreachable)
            - predecessors[i]: previous node in shortest path to i

        Algorithm:
        1. Initialize distances to infinity (None), except start = 0
        2. Repeat V-1 times:
           a. For each edge (u, v) with weight w:
              - If dist[u] + w < dist[v], update dist[v] and pred[v]
        3. Check for negative cycles:
           a. For each edge (u, v) with weight w:
              - If dist[u] + w < dist[v], negative cycle exists
        4. Return success flag, distances and predecessors
        """
        # TODO: Implement Bellman-Ford algorithm
        pass

    def shortest_path(self, start: int, end: int) -> Optional[Tuple[int, List[int]]]:
        """
        Find shortest path from start to end

        Returns:
            - Some((cost, path)) if path exists and no negative cycle
            - None if no path exists or negative cycle detected
        """
        # TODO: Find shortest path from start to end
        pass

    def has_negative_cycle(self) -> bool:
        """Detect if graph contains negative cycle"""
        # TODO: Detect if graph contains negative cycle
        # Run Bellman-Ford from vertex 0 and check result
        pass

    def find_negative_cycle(self) -> Optional[List[int]]:
        """
        Find and return a negative cycle if one exists

        Algorithm:
        1. Run modified Bellman-Ford to detect cycle
        2. Track predecessors
        3. Reconstruct cycle from predecessors
        4. Return Some(cycle) or None
        """
        # TODO: Find and return a negative cycle if one exists
        pass


import unittest


class TestBellmanFord(unittest.TestCase):
    def test_simple_path(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[2], 3)
        self.assertEqual(distances[3], 6)

    def test_negative_weights(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 4)
        graph.add_edge(0, 2, 5)
        graph.add_edge(1, 2, -3)  # negative weight
        graph.add_edge(2, 3, 2)

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 4)
        self.assertEqual(distances[2], 1)  # through 1 with negative edge
        self.assertEqual(distances[3], 3)

    def test_negative_cycle_detection(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -3)
        graph.add_edge(2, 0, 1)  # cycle: 0->1->2->0 with total weight -1

        success, _, _ = graph.bellman_ford(0)
        self.assertFalse(success)

    def test_no_negative_cycle(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -1)
        graph.add_edge(2, 0, 2)  # cycle with positive total weight

        success, _, _ = graph.bellman_ford(0)
        self.assertTrue(success)

    def test_unreachable_nodes(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 2, 3)
        # Nodes 3 and 4 are unreachable

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 2)
        self.assertEqual(distances[2], 5)
        self.assertIsNone(distances[3])
        self.assertIsNone(distances[4])

    def test_shortest_path_with_negatives(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 5)
        graph.add_edge(0, 2, 2)
        graph.add_edge(2, 1, -3)
        graph.add_edge(1, 3, 1)

        result = graph.shortest_path(0, 3)
        self.assertIsNotNone(result)
        cost, path = result
        self.assertEqual(cost, 0)  # 0->2->1->3: 2+(-3)+1 = 0
        self.assertEqual(path, [0, 2, 1, 3])

    def test_zero_weight_edges(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 0)
        graph.add_edge(1, 2, 0)

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 0)
        self.assertEqual(distances[2], 0)

    def test_has_negative_cycle(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -2)
        graph.add_edge(2, 0, -1)

        self.assertTrue(graph.has_negative_cycle())

    def test_find_negative_cycle(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -3)
        graph.add_edge(2, 0, 1)

        cycle = graph.find_negative_cycle()
        self.assertIsNotNone(cycle)
        self.assertGreaterEqual(len(cycle), 2)
        # Verify it's actually a cycle
        self.assertEqual(cycle[0], cycle[-1])

    def test_undirected_negative_edge(self):
        graph = Graph(2)
        graph.add_undirected_edge(0, 1, -1)

        # Undirected negative edge creates negative cycle
        self.assertTrue(graph.has_negative_cycle())

    def test_large_graph(self):
        graph = Graph(100)
        for i in range(99):
            graph.add_edge(i, i + 1, 1)

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[50], 50)
        self.assertEqual(distances[99], 99)

    def test_complex_negative_weights(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 6)
        graph.add_edge(0, 2, 7)
        graph.add_edge(1, 2, 8)
        graph.add_edge(1, 3, -4)
        graph.add_edge(1, 4, 5)
        graph.add_edge(2, 3, 9)
        graph.add_edge(2, 4, -3)
        graph.add_edge(3, 4, 7)
        graph.add_edge(3, 0, 2)

        success, distances, _ = graph.bellman_ford(0)
        self.assertTrue(success)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 6)
        self.assertEqual(distances[2], 7)
        self.assertEqual(distances[3], 2)
        self.assertEqual(distances[4], 4)


if __name__ == '__main__':
    unittest.main()
