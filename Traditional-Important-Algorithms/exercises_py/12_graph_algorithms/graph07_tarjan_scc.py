# I AM NOT DONE

"""
Tarjan's Strongly Connected Components Algorithm

A strongly connected component (SCC) is a maximal set of vertices where every
vertex is reachable from every other vertex. Tarjan's algorithm finds all SCCs
in a directed graph using a single DFS pass with a stack.

Time Complexity: O(V + E)
Space Complexity: O(V)

Your task: Implement Tarjan's SCC algorithm.
"""

from typing import Dict, List, Set


class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, from_node: int, to_node: int):
        # TODO: Add directed edge
        pass

    def tarjan_scc(self) -> List[List[int]]:
        """Find all SCCs using Tarjan's algorithm"""
        # TODO: Implement Tarjan's algorithm
        pass

    def _strongconnect(self, v: int, index: Dict[int, int], low_link: Dict[int, int],
                      on_stack: Dict[int, bool], stack: List[int], current_index: List[int],
                      sccs: List[List[int]]):
        # TODO: Recursive helper for Tarjan's algorithm
        pass

    def count_sccs(self) -> int:
        # TODO: Return number of SCCs
        pass

    def is_strongly_connected(self) -> bool:
        # TODO: Check if entire graph is one SCC
        pass


import unittest

class TestTarjanSCC(unittest.TestCase):
    def test_single_scc(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        sccs = graph.tarjan_scc()
        self.assertEqual(len(sccs), 1)
        self.assertEqual(len(sccs[0]), 3)

    def test_multiple_sccs(self):
        graph = Graph(5)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        graph.add_edge(3, 4)
        graph.add_edge(4, 3)
        graph.add_edge(2, 3)
        
        sccs = graph.tarjan_scc()
        self.assertEqual(len(sccs), 2)

    def test_linear_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        sccs = graph.tarjan_scc()
        self.assertEqual(len(sccs), 4)

    def test_count_sccs(self):
        graph = Graph(5)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        graph.add_edge(3, 4)
        
        self.assertEqual(graph.count_sccs(), 3)

    def test_is_strongly_connected(self):
        strongly = Graph(3)
        strongly.add_edge(0, 1)
        strongly.add_edge(1, 2)
        strongly.add_edge(2, 0)
        self.assertTrue(strongly.is_strongly_connected())
        
        weakly = Graph(3)
        weakly.add_edge(0, 1)
        weakly.add_edge(1, 2)
        self.assertFalse(weakly.is_strongly_connected())

if __name__ == '__main__':
    unittest.main()
