# I AM NOT DONE

"""
Prim's Minimum Spanning Tree Algorithm

Prim's algorithm finds a minimum spanning tree for a connected weighted graph.
Starting from an arbitrary vertex, it grows the MST one edge at a time by
always adding the minimum weight edge that connects a vertex in the tree
to a vertex outside the tree.

Time Complexity: O((V + E) log V) with binary heap, O(V²) with array
Space Complexity: O(V + E) for adjacency list and heap

Key concepts:
- Greedy algorithm: Always pick minimum weight edge connecting tree to non-tree
- Priority queue (min-heap) for efficient minimum edge selection
- Grows tree from a single vertex
- Similar to Dijkstra but minimizes edge weight instead of path distance

Your task: Implement Prim's MST algorithm with priority queue optimization.
"""

import heapq
from typing import Dict, List, Optional, Tuple


class Graph:
    """Undirected weighted graph using adjacency list"""

    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        # Adjacency list: node -> list of (neighbor, weight) tuples
        self.adj: Dict[int, List[Tuple[int, int]]] = {}

    def add_edge(self, u: int, v: int, weight: int):
        """Add undirected edge (add both u->v and v->u)"""
        # TODO: Add undirected edge
        pass

    def prim(self, start: int) -> Optional[Tuple[int, List[Tuple[int, int, int]]]]:
        """
        Run Prim's MST algorithm starting from 'start' vertex

        Returns:
            Some((total_weight, mst_edges)) or None if graph not connected
            where mst_edges is list of (from, to, weight) tuples

        Algorithm:
        1. Initialize empty MST edge list
        2. Initialize visited set with start vertex
        3. Add all edges from start to priority queue
        4. While MST has fewer than V-1 edges:
           a. Pop minimum weight edge from heap
           b. If destination already visited, skip
           c. Add edge to MST
           d. Mark destination as visited
           e. Add all edges from destination to non-visited vertices to heap
        5. If MST has V-1 edges, return Some((weight, edges))
           Otherwise, return None (graph not connected)
        """
        # TODO: Implement Prim's MST algorithm
        # Hint: Use heapq.heappush(heap, (weight, to, from))
        #       Use heapq.heappop(heap)
        pass

    def mst_weight(self) -> Optional[int]:
        """Return total weight of MST starting from vertex 0"""
        # TODO: Return total weight of MST
        pass

    def is_connected(self) -> bool:
        """Check if graph is connected by running Prim from vertex 0"""
        # TODO: Check if graph is connected
        # Graph is connected if MST contains V-1 edges
        pass

    def prim_from_any_vertex(self) -> Optional[Tuple[int, List[Tuple[int, int, int]]]]:
        """Run Prim from first vertex that has edges"""
        # TODO: Run Prim from first vertex that has edges
        # Useful for graphs where vertex 0 might be isolated
        pass


import unittest


class TestPrim(unittest.TestCase):
    def test_simple_mst(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 6)
        graph.add_edge(0, 3, 5)
        graph.add_edge(1, 3, 15)
        graph.add_edge(2, 3, 4)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 19)  # 4 + 5 + 10
        self.assertEqual(len(edges), 3)

    def test_line_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 6)
        self.assertEqual(len(edges), 3)

    def test_complete_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(0, 2, 2)
        graph.add_edge(0, 3, 3)
        graph.add_edge(1, 2, 4)
        graph.add_edge(1, 3, 5)
        graph.add_edge(2, 3, 6)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 6)  # 1 + 2 + 3
        self.assertEqual(len(edges), 3)

    def test_disconnected_graph(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        # Vertices 3 and 4 are disconnected

        result = graph.prim(0)
        self.assertIsNone(result)  # Cannot form spanning tree

    def test_single_vertex(self):
        graph = Graph(1)
        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 0)
        self.assertEqual(len(edges), 0)

    def test_two_vertices(self):
        graph = Graph(2)
        graph.add_edge(0, 1, 5)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 5)
        self.assertEqual(len(edges), 1)

    def test_equal_weight_edges(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        graph.add_edge(3, 0, 1)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, _ = result
        self.assertEqual(weight, 3)

    def test_different_start_vertex(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)

        result1 = graph.prim(0)
        result2 = graph.prim(2)

        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)

        # MST weight should be same regardless of start vertex
        self.assertEqual(result1[0], result2[0])

    def test_is_connected(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        self.assertTrue(graph.is_connected())

        disconnected = Graph(4)
        disconnected.add_edge(0, 1, 1)
        self.assertFalse(disconnected.is_connected())

    def test_negative_weights(self):
        graph = Graph(3)
        graph.add_edge(0, 1, -1)
        graph.add_edge(1, 2, -2)
        graph.add_edge(0, 2, 5)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, _ = result
        self.assertEqual(weight, -3)

    def test_mst_weight(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 6)
        graph.add_edge(0, 3, 5)
        graph.add_edge(1, 3, 15)
        graph.add_edge(2, 3, 4)

        self.assertEqual(graph.mst_weight(), 19)

    def test_large_graph(self):
        graph = Graph(100)
        # Create a path graph with weight 1
        for i in range(99):
            graph.add_edge(i, i + 1, 1)
        # Add some cross edges with higher weights
        graph.add_edge(0, 50, 100)
        graph.add_edge(25, 75, 100)

        result = graph.prim(0)
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 99)
        self.assertEqual(len(edges), 99)


if __name__ == '__main__':
    unittest.main()
