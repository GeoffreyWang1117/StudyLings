# I AM NOT DONE

"""
PageRank Algorithm

Time Complexity: O(iterations * E)
Space Complexity: O(V)

Your task: Implement PageRank algorithm with damping factor and convergence.
"""

from typing import Dict, List


class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, from_node: int, to_node: int):
        # TODO: Add directed edge
        pass

    def pagerank(self, damping_factor: float = 0.85, max_iterations: int = 100, 
                tolerance: float = 1e-6) -> List[float]:
        """
        Compute PageRank scores
        
        PR(v) = (1-d)/N + d * Σ(PR(u)/out_degree(u)) for all u linking to v
        """
        # TODO: Implement PageRank
        pass

    def get_out_degree(self, vertex: int) -> int:
        # TODO: Return out-degree
        pass

    def top_k_pages(self, k: int) -> List[Tuple[int, float]]:
        # TODO: Return top k pages by PageRank
        pass


import unittest

class TestPageRank(unittest.TestCase):
    def approx_equal(self, a: float, b: float, epsilon: float = 1e-3):
        return abs(a - b) < epsilon

    def test_simple_graph(self):
        graph = Graph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        
        ranks = graph.pagerank()
        self.assertEqual(len(ranks), 3)
        self.assertTrue(self.approx_equal(ranks[0], ranks[1]))
        total = sum(ranks)
        self.assertTrue(self.approx_equal(total, 1.0))

    def test_star_graph(self):
        graph = Graph(4)
        graph.add_edge(1, 0)
        graph.add_edge(2, 0)
        graph.add_edge(3, 0)
        
        ranks = graph.pagerank()
        self.assertGreater(ranks[0], ranks[1])

if __name__ == '__main__':
    unittest.main()
