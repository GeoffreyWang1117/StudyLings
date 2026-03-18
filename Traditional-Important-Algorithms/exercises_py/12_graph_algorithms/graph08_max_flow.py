# I AM NOT DONE

"""
Maximum Flow Algorithms (Ford-Fulkerson and Edmonds-Karp)

Time Complexity: Edmonds-Karp O(V * E²)
Space Complexity: O(V²)

Your task: Implement Ford-Fulkerson and Edmonds-Karp algorithms.
"""

from typing import List, Optional, Tuple
from collections import deque


class FlowNetwork:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.capacity: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]
        self.flow: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, from_node: int, to_node: int, capacity: int):
        # TODO: Add edge with capacity
        pass

    def edmonds_karp(self, source: int, sink: int) -> int:
        """Run Edmonds-Karp (BFS-based Ford-Fulkerson)"""
        # TODO: Implement Edmonds-Karp
        pass

    def _bfs_augmenting_path(self, source: int, sink: int) -> Optional[Tuple[List[int], int]]:
        """Find augmenting path using BFS"""
        # TODO: Find augmenting path
        pass

    def get_flow(self, from_node: int, to_node: int) -> int:
        # TODO: Return flow on edge
        pass

    def reset_flow(self):
        # TODO: Reset all flows to zero
        pass


import unittest

class TestMaxFlow(unittest.TestCase):
    def test_simple_flow(self):
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10)
        network.add_edge(1, 2, 5)
        network.add_edge(2, 3, 10)
        
        max_flow = network.edmonds_karp(0, 3)
        self.assertEqual(max_flow, 5)

    def test_multiple_paths(self):
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10)
        network.add_edge(0, 2, 10)
        network.add_edge(1, 3, 10)
        network.add_edge(2, 3, 10)
        
        max_flow = network.edmonds_karp(0, 3)
        self.assertEqual(max_flow, 20)

    def test_no_path(self):
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10)
        network.add_edge(2, 3, 10)
        
        max_flow = network.edmonds_karp(0, 3)
        self.assertEqual(max_flow, 0)

if __name__ == '__main__':
    unittest.main()
