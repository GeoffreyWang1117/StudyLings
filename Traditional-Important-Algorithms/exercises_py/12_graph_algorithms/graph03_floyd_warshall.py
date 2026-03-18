# I AM NOT DONE

"""
Floyd-Warshall All-Pairs Shortest Paths Algorithm

Floyd-Warshall computes shortest paths between ALL pairs of vertices in a weighted
directed graph. It works with negative edge weights but not negative cycles.
The algorithm uses dynamic programming with a 3D approach.

Time Complexity: O(V³) where V = number of vertices
Space Complexity: O(V²) for distance matrix

Key concepts:
- Dynamic programming: dist[i][j][k] = shortest path from i to j using vertices 0..k
- Can be optimized to 2D array by reusing the distance matrix
- Computes all-pairs shortest paths in one pass
- Can detect negative cycles by checking diagonal

Your task: Implement Floyd-Warshall algorithm with path reconstruction.
"""

from typing import List, Optional


class Graph:
    """Weighted directed graph using adjacency matrix representation"""

    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        # Distance matrix initialized with None (infinity)
        self.dist: List[List[Optional[int]]] = [[None] * num_vertices for _ in range(num_vertices)]
        # Next matrix for path reconstruction
        self.next: List[List[Optional[int]]] = [[None] * num_vertices for _ in range(num_vertices)]

        # TODO: Set dist[i][i] = 0 for all i
        pass

    def add_edge(self, from_node: int, to_node: int, weight: int):
        """
        Add edge to distance matrix

        Set dist[from_node][to_node] = weight
        Set next[from_node][to_node] = to_node for path reconstruction
        """
        # TODO: Add edge to distance matrix
        pass

    def floyd_warshall(self) -> bool:
        """
        Run Floyd-Warshall algorithm

        Returns:
            True if no negative cycles, False otherwise

        Algorithm:
        For each intermediate vertex k:
          For each pair of vertices (i, j):
            If path i->k->j is shorter than current i->j:
              Update dist[i][j] and next[i][j]

        After algorithm, check for negative cycles:
          If dist[i][i] < 0 for any i, return False

        Return True if no negative cycles
        """
        # TODO: Implement Floyd-Warshall algorithm
        pass

    def shortest_distance(self, from_node: int, to_node: int) -> Optional[int]:
        """Return shortest distance from 'from_node' to 'to_node'"""
        # TODO: Return shortest distance
        # Must call floyd_warshall() first
        pass

    def shortest_path(self, from_node: int, to_node: int) -> Optional[List[int]]:
        """
        Reconstruct shortest path from 'from_node' to 'to_node'

        Use the 'next' matrix to trace the path
        Return None if no path exists
        """
        # TODO: Reconstruct shortest path
        pass

    def has_negative_cycle(self) -> bool:
        """
        Check if graph contains negative cycle

        After running floyd_warshall(), check if any dist[i][i] < 0
        """
        # TODO: Check if graph contains negative cycle
        pass

    def get_distance_matrix(self) -> List[List[Optional[int]]]:
        """Return the distance matrix"""
        return self.dist

    def transitive_closure(self) -> List[List[bool]]:
        """
        Compute transitive closure (reachability matrix)

        Similar to Floyd-Warshall but with boolean values
        reach[i][j] = True if there exists a path from i to j
        """
        # TODO: Compute transitive closure
        pass


import unittest


class TestFloydWarshall(unittest.TestCase):
    def test_simple_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 3)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 2)
        graph.add_edge(0, 3, 10)

        self.assertTrue(graph.floyd_warshall())
        self.assertEqual(graph.shortest_distance(0, 3), 6)  # 0->1->2->3
        self.assertEqual(graph.shortest_distance(0, 1), 3)
        self.assertEqual(graph.shortest_distance(1, 3), 3)

    def test_all_pairs_distances(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 4)
        graph.add_edge(1, 2, 3)
        graph.add_edge(0, 2, 8)
        graph.add_edge(2, 0, 2)

        self.assertTrue(graph.floyd_warshall())

        # Check all pairs
        self.assertEqual(graph.shortest_distance(0, 0), 0)
        self.assertEqual(graph.shortest_distance(0, 1), 4)
        self.assertEqual(graph.shortest_distance(0, 2), 7)
        self.assertEqual(graph.shortest_distance(1, 0), 5)  # 1->2->0
        self.assertEqual(graph.shortest_distance(1, 1), 0)
        self.assertEqual(graph.shortest_distance(1, 2), 3)
        self.assertEqual(graph.shortest_distance(2, 0), 2)
        self.assertEqual(graph.shortest_distance(2, 1), 6)  # 2->0->1
        self.assertEqual(graph.shortest_distance(2, 2), 0)

    def test_negative_weights(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 4)
        graph.add_edge(1, 2, -2)
        graph.add_edge(0, 2, 3)

        self.assertTrue(graph.floyd_warshall())
        self.assertEqual(graph.shortest_distance(0, 2), 2)  # 0->1->2

    def test_negative_cycle_detection(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -3)
        graph.add_edge(2, 0, 1)  # cycle with total weight -1

        result = graph.floyd_warshall()
        self.assertFalse(result)

    def test_unreachable_vertices(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        # Vertex 3 is unreachable from others

        self.assertTrue(graph.floyd_warshall())
        self.assertEqual(graph.shortest_distance(0, 2), 2)
        self.assertIsNone(graph.shortest_distance(0, 3))
        self.assertIsNone(graph.shortest_distance(3, 0))

    def test_path_reconstruction(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)
        graph.add_edge(0, 2, 10)

        self.assertTrue(graph.floyd_warshall())

        path = graph.shortest_path(0, 3)
        self.assertIsNotNone(path)
        self.assertEqual(path, [0, 1, 2, 3])

    def test_no_path(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        # No path from 0 to 2

        self.assertTrue(graph.floyd_warshall())
        self.assertIsNone(graph.shortest_path(0, 2))

    def test_self_loops(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 5)
        graph.add_edge(1, 1, 2)  # positive self-loop
        graph.add_edge(1, 2, 3)

        self.assertTrue(graph.floyd_warshall())
        self.assertEqual(graph.shortest_distance(0, 2), 8)

    def test_transitive_closure(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)

        closure = graph.transitive_closure()

        self.assertTrue(closure[0][0])  # Can reach self
        self.assertTrue(closure[0][1])
        self.assertTrue(closure[0][2])
        self.assertTrue(closure[0][3])
        self.assertFalse(closure[1][0])  # Cannot reach 0 from 1
        self.assertTrue(closure[1][2])
        self.assertFalse(closure[3][0])  # Cannot reach earlier nodes

    def test_complete_graph(self):
        graph = Graph(4)
        # Add edges between all pairs
        for i in range(4):
            for j in range(4):
                if i != j:
                    graph.add_edge(i, j, i + j + 1)

        self.assertTrue(graph.floyd_warshall())

        # All vertices should be reachable
        for i in range(4):
            for j in range(4):
                if i != j:
                    self.assertIsNotNone(graph.shortest_distance(i, j))

    def test_zero_weight_edges(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 0)
        graph.add_edge(1, 2, 0)

        self.assertTrue(graph.floyd_warshall())
        self.assertEqual(graph.shortest_distance(0, 2), 0)

    def test_complex_graph(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 3)
        graph.add_edge(0, 2, 8)
        graph.add_edge(0, 4, -4)
        graph.add_edge(1, 3, 1)
        graph.add_edge(1, 4, 7)
        graph.add_edge(2, 1, 4)
        graph.add_edge(3, 0, 2)
        graph.add_edge(3, 2, -5)
        graph.add_edge(4, 3, 6)

        self.assertTrue(graph.floyd_warshall())

        self.assertEqual(graph.shortest_distance(0, 1), 1)  # 0->4->3->2->1
        self.assertEqual(graph.shortest_distance(0, 2), -3)  # 0->4->3->2
        self.assertEqual(graph.shortest_distance(0, 3), 2)  # 0->4->3
        self.assertEqual(graph.shortest_distance(0, 4), -4)


if __name__ == '__main__':
    unittest.main()
