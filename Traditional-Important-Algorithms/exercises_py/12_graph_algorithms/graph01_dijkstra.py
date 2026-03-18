# I AM NOT DONE

"""
Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm finds the shortest paths from a source vertex to all other
vertices in a weighted graph with non-negative edge weights. It uses a greedy
approach, always selecting the unvisited vertex with the smallest known distance.

Time Complexity: O((V + E) log V) with binary heap, O(V²) with array
Space Complexity: O(V) for distance array and visited set

Key concepts:
- Greedy algorithm: Always picks the closest unvisited vertex
- Priority queue (min-heap) to efficiently get minimum distance vertex
- Relaxation: Update distance if shorter path found
- Does NOT work with negative edge weights (use Bellman-Ford instead)

Your task: Implement Dijkstra's algorithm with priority queue optimization.
"""

import heapq
from typing import Dict, List, Optional, Tuple


class Graph:
    """Weighted directed graph using adjacency list representation"""

    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        # Adjacency list: node -> list of (neighbor, weight) tuples
        self.adj: Dict[int, List[Tuple[int, int]]] = {}

    def add_edge(self, from_node: int, to_node: int, weight: int):
        """Add a directed edge from 'from_node' to 'to_node' with given weight"""
        # TODO: Add edge to adjacency list
        # Use adjacency list representation
        pass

    def add_undirected_edge(self, u: int, v: int, weight: int):
        """Add an undirected edge (add both directions)"""
        # TODO: Add edges in both directions
        pass

    def dijkstra(self, start: int) -> Tuple[List[Optional[int]], List[Optional[int]]]:
        """
        Run Dijkstra's algorithm from start vertex

        Returns:
            Tuple of (distances, predecessors)
            - distances[i] = shortest distance from start to i (None if unreachable)
            - predecessors[i] = previous node in shortest path to i

        Algorithm:
        1. Initialize distances to infinity (None), except start = 0
        2. Initialize empty priority queue (min-heap)
        3. Push (0, start) to heap
        4. While heap is not empty:
           a. Pop vertex with minimum distance
           b. Skip if already processed (distance check)
           c. For each neighbor:
              - Calculate new distance through current vertex
              - If shorter than known distance, update and push to heap
        5. Return distances and predecessors
        """
        # TODO: Implement Dijkstra's algorithm
        # Hint: Use heapq for priority queue
        # heapq.heappush(heap, (priority, value))
        # heapq.heappop(heap) returns smallest element
        pass

    def shortest_path(self, start: int, end: int) -> Optional[Tuple[int, List[int]]]:
        """
        Find shortest path from start to end

        Returns:
            Some((total_cost, path)) or None if no path exists
            Use dijkstra() and reconstruct path from predecessors
        """
        # TODO: Find shortest path from start to end
        pass

    def has_path(self, start: int, end: int) -> bool:
        """Check if path exists from start to end"""
        # TODO: Check if path exists
        pass


import unittest


class TestDijkstra(unittest.TestCase):
    def test_simple_path(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[2], 3)
        self.assertEqual(distances[3], 6)

    def test_multiple_paths(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 4)
        graph.add_edge(0, 2, 1)
        graph.add_edge(2, 1, 2)
        graph.add_edge(1, 3, 1)
        graph.add_edge(2, 3, 5)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 3)  # via 2
        self.assertEqual(distances[2], 1)
        self.assertEqual(distances[3], 4)  # via 2->1->3

    def test_unreachable_node(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        # Node 3 and 4 are disconnected

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[2], 2)
        self.assertIsNone(distances[3])
        self.assertIsNone(distances[4])

    def test_shortest_path_reconstruction(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(0, 2, 5)
        graph.add_edge(2, 3, 1)

        result = graph.shortest_path(0, 3)
        self.assertIsNotNone(result)
        cost, path = result
        self.assertEqual(cost, 4)  # 0->1->2->3
        self.assertEqual(path, [0, 1, 2, 3])

    def test_no_path(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        # No path from 0 to 2

        self.assertIsNone(graph.shortest_path(0, 2))
        self.assertFalse(graph.has_path(0, 2))

    def test_undirected_graph(self):
        graph = Graph(4)
        graph.add_undirected_edge(0, 1, 2)
        graph.add_undirected_edge(1, 2, 3)
        graph.add_undirected_edge(2, 3, 1)
        graph.add_undirected_edge(0, 3, 10)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[3], 6)  # 0->1->2->3, not 0->3

    def test_self_loop(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 5)
        graph.add_edge(1, 1, 2)  # self loop
        graph.add_edge(1, 2, 3)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[1], 5)
        self.assertEqual(distances[2], 8)

    def test_zero_weight_edges(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 0)
        graph.add_edge(1, 2, 0)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 0)
        self.assertEqual(distances[2], 0)

    def test_has_path(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)

        self.assertTrue(graph.has_path(0, 0))
        self.assertTrue(graph.has_path(0, 1))
        self.assertTrue(graph.has_path(0, 2))
        self.assertFalse(graph.has_path(0, 3))

    def test_large_graph(self):
        graph = Graph(100)
        for i in range(99):
            graph.add_edge(i, i + 1, 1)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[50], 50)
        self.assertEqual(distances[99], 99)

    def test_complex_graph(self):
        graph = Graph(6)
        graph.add_edge(0, 1, 4)
        graph.add_edge(0, 2, 2)
        graph.add_edge(1, 2, 1)
        graph.add_edge(1, 3, 5)
        graph.add_edge(2, 3, 8)
        graph.add_edge(2, 4, 10)
        graph.add_edge(3, 4, 2)
        graph.add_edge(3, 5, 6)
        graph.add_edge(4, 5, 3)

        distances, _ = graph.dijkstra(0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 3)  # 0->2->1
        self.assertEqual(distances[2], 2)
        self.assertEqual(distances[3], 8)  # 0->2->1->3
        self.assertEqual(distances[4], 10)  # 0->2->1->3->4
        self.assertEqual(distances[5], 13)  # 0->2->1->3->4->5


if __name__ == '__main__':
    unittest.main()
