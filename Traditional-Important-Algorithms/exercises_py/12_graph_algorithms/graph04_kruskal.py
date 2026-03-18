# I AM NOT DONE

"""
Kruskal's Minimum Spanning Tree Algorithm

Kruskal's algorithm finds a minimum spanning tree for a connected weighted graph.
It uses a greedy approach: sort all edges by weight and add them one by one,
skipping edges that would create a cycle (using Union-Find data structure).

Time Complexity: O(E log E) or O(E log V) for sorting edges
Space Complexity: O(V) for Union-Find structure

Key concepts:
- Greedy algorithm: Always pick minimum weight edge that doesn't create cycle
- Union-Find (Disjoint Set Union) for efficient cycle detection
- Sort edges by weight first
- Works on undirected graphs

Your task: Implement Kruskal's MST algorithm with Union-Find.
"""

from typing import List, Optional, Tuple


class Edge:
    """Represents an edge in an undirected graph"""
    
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight
    
    def __lt__(self, other):
        """For sorting edges by weight"""
        if self.weight != other.weight:
            return self.weight < other.weight
        if self.u != other.u:
            return self.u < other.u
        return self.v < other.v


class UnionFind:
    """Union-Find data structure for cycle detection"""
    
    def __init__(self, size: int):
        # TODO: Initialize Union-Find structure
        # parent[i] = i (each element is its own parent initially)
        # rank[i] = 0 (tree height)
        pass
    
    def find(self, x: int) -> int:
        """Find root of element x with path compression"""
        # TODO: Find root of element x with path compression
        # If parent[x] != x, recursively find root and compress path
        # Return root
        pass
    
    def union(self, x: int, y: int) -> bool:
        """
        Union two sets containing x and y
        
        Returns:
            True if sets were merged, False if already in same set
        """
        # TODO: Union two sets containing x and y
        # Find roots of x and y
        # If same root, they're already in same set, return False
        # Otherwise, union by rank and return True
        # Attach smaller rank tree under root of higher rank tree
        pass
    
    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set"""
        # TODO: Check if x and y are in the same set
        pass


class Graph:
    """Undirected weighted graph for MST algorithms"""
    
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.edges: List[Edge] = []
    
    def add_edge(self, u: int, v: int, weight: int):
        """Add undirected edge (store once, as Kruskal treats edges as undirected)"""
        # TODO: Add undirected edge
        pass
    
    def kruskal(self) -> Optional[Tuple[int, List[Edge]]]:
        """
        Run Kruskal's MST algorithm
        
        Returns:
            Some((total_weight, mst_edges)) or None if graph not connected
            
        Algorithm:
        1. Sort all edges by weight
        2. Initialize Union-Find with num_vertices
        3. Initialize empty MST edge list
        4. For each edge (u, v, w) in sorted order:
           a. If u and v not in same set (no cycle):
              - Add edge to MST
              - Union sets containing u and v
        5. If MST has V-1 edges, return Some((weight, edges))
           Otherwise, graph is not connected, return None
        """
        # TODO: Implement Kruskal's MST algorithm
        pass
    
    def is_connected(self) -> bool:
        """Check if graph is connected using Union-Find"""
        # TODO: Check if graph is connected
        pass
    
    def mst_weight(self) -> Optional[int]:
        """Return total weight of MST (without edges)"""
        # TODO: Return total weight of MST
        pass


import unittest


class TestKruskal(unittest.TestCase):
    def test_union_find_basic(self):
        uf = UnionFind(5)
        self.assertFalse(uf.connected(0, 1))
        
        uf.union(0, 1)
        self.assertTrue(uf.connected(0, 1))
        
        uf.union(2, 3)
        self.assertTrue(uf.connected(2, 3))
        self.assertFalse(uf.connected(0, 2))
        
        uf.union(1, 3)
        self.assertTrue(uf.connected(0, 3))
    
    def test_simple_mst(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 6)
        graph.add_edge(0, 3, 5)
        graph.add_edge(1, 3, 15)
        graph.add_edge(2, 3, 4)
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 19)  # 4 + 5 + 10
        self.assertEqual(len(edges), 3)
    
    def test_line_graph(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 3, 3)
        
        result = graph.kruskal()
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
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 6)  # 1 + 2 + 3
        self.assertEqual(len(edges), 3)
    
    def test_disconnected_graph(self):
        graph = Graph(5)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        # Vertices 3 and 4 are disconnected
        
        result = graph.kruskal()
        self.assertIsNone(result)  # No spanning tree for disconnected graph
    
    def test_single_vertex(self):
        graph = Graph(1)
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 0)
        self.assertEqual(len(edges), 0)
    
    def test_two_vertices(self):
        graph = Graph(2)
        graph.add_edge(0, 1, 5)
        
        result = graph.kruskal()
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
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, _ = result
        self.assertEqual(weight, 3)  # Any 3 edges work
    
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
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, _ = result
        self.assertEqual(weight, -3)  # MST works with negative weights too
    
    def test_cycle_avoidance(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(0, 2, 10)  # This creates a cycle, should be ignored
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 3)
        self.assertEqual(len(edges), 2)
        # Edge (0,2) with weight 10 should not be in MST
        has_expensive_edge = any((e.u == 0 and e.v == 2 or e.u == 2 and e.v == 0) and e.weight == 10 for e in edges)
        self.assertFalse(has_expensive_edge)
    
    def test_large_graph(self):
        graph = Graph(100)
        # Create a path graph
        for i in range(99):
            graph.add_edge(i, i + 1, 1)
        # Add some cross edges with higher weights
        graph.add_edge(0, 50, 100)
        graph.add_edge(25, 75, 100)
        
        result = graph.kruskal()
        self.assertIsNotNone(result)
        weight, edges = result
        self.assertEqual(weight, 99)  # Only path edges should be selected
        self.assertEqual(len(edges), 99)


if __name__ == '__main__':
    unittest.main()
