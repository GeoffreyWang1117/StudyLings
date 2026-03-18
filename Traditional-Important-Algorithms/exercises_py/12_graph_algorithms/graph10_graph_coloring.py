# I AM NOT DONE

"""
Graph Coloring Algorithms

Time Complexity: Greedy O(V + E), Backtracking O(k^V)
Space Complexity: O(V)

Your task: Implement greedy and backtracking graph coloring algorithms.
"""

from typing import Dict, List, Set


class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, u: int, v: int):
        # TODO: Add undirected edge
        pass

    def greedy_coloring(self) -> Dict[int, int]:
        """Greedy graph coloring"""
        # TODO: Implement greedy coloring
        pass

    def welsh_powell_coloring(self) -> Dict[int, int]:
        """Welsh-Powell algorithm (improved greedy)"""
        # TODO: Implement Welsh-Powell
        pass

    def backtracking_coloring(self, max_colors: int) -> Optional[Dict[int, int]]:
        """Backtracking to find optimal coloring"""
        # TODO: Implement backtracking
        pass

    def _is_safe_color(self, vertex: int, color: int, coloring: Dict[int, int]) -> bool:
        # TODO: Check if color is safe
        pass

    def is_bipartite(self) -> bool:
        """Check if graph is 2-colorable"""
        # TODO: Check if bipartite
        pass

    def verify_coloring(self, coloring: Dict[int, int]) -> bool:
        """Verify coloring is valid"""
        # TODO: Verify coloring
        pass


import unittest

class TestGraphColoring(unittest.TestCase):
    def test_simple_coloring(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        
        coloring = graph.greedy_coloring()
        self.assertEqual(len(coloring), 3)
        self.assertNotEqual(coloring[0], coloring[1])
        self.assertNotEqual(coloring[1], coloring[2])

    def test_triangle_coloring(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        coloring = graph.greedy_coloring()
        self.assertNotEqual(coloring[0], coloring[1])
        self.assertNotEqual(coloring[1], coloring[2])
        self.assertNotEqual(coloring[2], coloring[0])

    def test_bipartite_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 2)
        graph.add_edge(0, 3)
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        
        self.assertTrue(graph.is_bipartite())

if __name__ == '__main__':
    unittest.main()
