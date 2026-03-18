# I AM NOT DONE

"""
Topological Sort Algorithms

Topological sorting orders vertices of a Directed Acyclic Graph (DAG) such that
for every directed edge (u, v), vertex u comes before v in the ordering.
Two common approaches: Kahn's algorithm (BFS-based) and DFS-based algorithm.

Time Complexity: O(V + E) for both algorithms
Space Complexity: O(V) for in-degree array and queue/stack

Key concepts:
- Only works on DAGs (Directed Acyclic Graphs)
- Kahn's algorithm: Remove vertices with in-degree 0 iteratively
- DFS-based: Post-order DFS traversal, reverse the result
- Can detect cycles (if sort fails to include all vertices)

Your task: Implement both Kahn's and DFS-based topological sort algorithms.
"""

from typing import Dict, List, Set
from collections import deque


class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, from_node: int, to_node: int):
        """Add directed edge from 'from_node' to 'to_node'"""
        # TODO: Add directed edge
        pass

    def topological_sort_kahn(self) -> List[int]:
        """
        Kahn's algorithm (BFS-based topological sort)
        
        Algorithm:
        1. Calculate in-degree for each vertex
        2. Initialize queue with all vertices having in-degree 0
        3. While queue is not empty:
           a. Remove vertex from queue, add to result
           b. For each neighbor, decrement in-degree
           c. If neighbor's in-degree becomes 0, add to queue
        4. If result contains all vertices, return result
           Otherwise, raise exception (cycle detected)
        """
        # TODO: Implement Kahn's algorithm
        pass

    def topological_sort_dfs(self) -> List[int]:
        """DFS-based topological sort"""
        # TODO: Implement DFS-based topological sort
        pass

    def _dfs_helper(self, v: int, visited: Set[int], rec_stack: Set[int], result: List[int]) -> bool:
        """DFS helper, returns True if cycle detected"""
        # TODO: DFS helper for topological sort
        pass

    def is_dag(self) -> bool:
        """Check if graph is a DAG"""
        # TODO: Check if graph is a DAG
        pass


import unittest

class TestTopologicalSort(unittest.TestCase):
    def test_simple_dag(self):
        graph = Graph(4)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        
        order = graph.topological_sort_kahn()
        self.assertEqual(len(order), 4)
        pos_0 = order.index(0)
        pos_1 = order.index(1)
        pos_2 = order.index(2)
        pos_3 = order.index(3)
        self.assertLess(pos_0, pos_1)
        self.assertLess(pos_0, pos_2)
        self.assertLess(pos_1, pos_3)
        self.assertLess(pos_2, pos_3)

    def test_dfs_topological_sort(self):
        graph = Graph(4)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        
        order = graph.topological_sort_dfs()
        self.assertEqual(len(order), 4)

    def test_cycle_detection_kahn(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        with self.assertRaises(Exception):
            graph.topological_sort_kahn()

    def test_cycle_detection_dfs(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        with self.assertRaises(Exception):
            graph.topological_sort_dfs()

    def test_linear_graph(self):
        graph = Graph(5)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        
        order = graph.topological_sort_kahn()
        self.assertEqual(order, [0, 1, 2, 3, 4])

    def test_is_dag(self):
        dag = Graph(3)
        dag.add_edge(0, 1)
        dag.add_edge(1, 2)
        self.assertTrue(dag.is_dag())
        
        cyclic = Graph(3)
        cyclic.add_edge(0, 1)
        cyclic.add_edge(1, 2)
        cyclic.add_edge(2, 0)
        self.assertFalse(cyclic.is_dag())

if __name__ == '__main__':
    unittest.main()
