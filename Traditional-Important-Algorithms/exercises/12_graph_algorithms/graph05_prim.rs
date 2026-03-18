// graph05_prim.rs
//
// Prim's Minimum Spanning Tree Algorithm
//
// Prim's algorithm finds a minimum spanning tree for a connected weighted graph.
// Starting from an arbitrary vertex, it grows the MST one edge at a time by
// always adding the minimum weight edge that connects a vertex in the tree
// to a vertex outside the tree.
//
// Time Complexity: O((V + E) log V) with binary heap, O(V²) with array
// Space Complexity: O(V + E) for adjacency list and heap
//
// Key concepts:
// - Greedy algorithm: Always pick minimum weight edge connecting tree to non-tree
// - Priority queue (min-heap) for efficient minimum edge selection
// - Grows tree from a single vertex
// - Similar to Dijkstra but minimizes edge weight instead of path distance
//
// Your task: Implement Prim's MST algorithm with priority queue optimization.

// I AM NOT DONE

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Ordering;

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
struct Edge {
    weight: i32,
    to: usize,
    from: usize,
}

impl Ord for Edge {
    fn cmp(&self, other: &Self) -> Ordering {
        // Min-heap: reverse the ordering
        other.weight.cmp(&self.weight)
            .then_with(|| self.to.cmp(&other.to))
    }
}

impl PartialOrd for Edge {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct Graph {
    // Adjacency list: node -> vec of (neighbor, weight)
    adj: HashMap<usize, Vec<(usize, i32)>>,
    num_vertices: usize,
}

impl Graph {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            adj: HashMap::new(),
            num_vertices,
        }
    }

    pub fn add_edge(&mut self, u: usize, v: usize, weight: i32) {
        // TODO: Add undirected edge (add both u->v and v->u)
        todo!()
    }

    pub fn prim(&self, start: usize) -> Option<(i32, Vec<(usize, usize, i32)>)> {
        // TODO: Implement Prim's MST algorithm starting from 'start' vertex
        // Returns Some((total_weight, mst_edges)) or None if graph not connected
        //
        // Algorithm:
        // 1. Initialize empty MST edge list
        // 2. Initialize visited set with start vertex
        // 3. Add all edges from start to priority queue
        // 4. While MST has fewer than V-1 edges:
        //    a. Pop minimum weight edge from heap
        //    b. If destination already visited, skip
        //    c. Add edge to MST
        //    d. Mark destination as visited
        //    e. Add all edges from destination to non-visited vertices to heap
        // 5. If MST has V-1 edges, return Some((weight, edges))
        //    Otherwise, return None (graph not connected)
        todo!()
    }

    pub fn mst_weight(&self) -> Option<i32> {
        // TODO: Return total weight of MST starting from vertex 0
        todo!()
    }

    pub fn is_connected(&self) -> bool {
        // TODO: Check if graph is connected by running Prim from vertex 0
        // Graph is connected if MST contains V-1 edges
        todo!()
    }

    pub fn prim_from_any_vertex(&self) -> Option<(i32, Vec<(usize, usize, i32)>)> {
        // TODO: Run Prim from first vertex that has edges
        // Useful for graphs where vertex 0 might be isolated
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_mst() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 10);
        graph.add_edge(0, 2, 6);
        graph.add_edge(0, 3, 5);
        graph.add_edge(1, 3, 15);
        graph.add_edge(2, 3, 4);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 19); // 4 + 5 + 10
        assert_eq!(edges.len(), 3);
    }

    #[test]
    fn test_line_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(2, 3, 3);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 6);
        assert_eq!(edges.len(), 3);
    }

    #[test]
    fn test_complete_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(0, 2, 2);
        graph.add_edge(0, 3, 3);
        graph.add_edge(1, 2, 4);
        graph.add_edge(1, 3, 5);
        graph.add_edge(2, 3, 6);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 6); // 1 + 2 + 3
        assert_eq!(edges.len(), 3);
    }

    #[test]
    fn test_disconnected_graph() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        // Vertices 3 and 4 are disconnected

        let result = graph.prim(0);
        assert!(result.is_none()); // Cannot form spanning tree
    }

    #[test]
    fn test_single_vertex() {
        let graph = Graph::new(1);
        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 0);
        assert_eq!(edges.len(), 0);
    }

    #[test]
    fn test_two_vertices() {
        let mut graph = Graph::new(2);
        graph.add_edge(0, 1, 5);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 5);
        assert_eq!(edges.len(), 1);
    }

    #[test]
    fn test_equal_weight_edges() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);
        graph.add_edge(2, 3, 1);
        graph.add_edge(3, 0, 1);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, _) = result.unwrap();
        assert_eq!(weight, 3);
    }

    #[test]
    fn test_different_start_vertex() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(2, 3, 3);

        let result1 = graph.prim(0);
        let result2 = graph.prim(2);

        assert!(result1.is_some());
        assert!(result2.is_some());

        // MST weight should be same regardless of start vertex
        assert_eq!(result1.unwrap().0, result2.unwrap().0);
    }

    #[test]
    fn test_is_connected() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);
        graph.add_edge(2, 3, 1);
        assert!(graph.is_connected());

        let mut disconnected = Graph::new(4);
        disconnected.add_edge(0, 1, 1);
        assert!(!disconnected.is_connected());
    }

    #[test]
    fn test_negative_weights() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, -1);
        graph.add_edge(1, 2, -2);
        graph.add_edge(0, 2, 5);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, _) = result.unwrap();
        assert_eq!(weight, -3);
    }

    #[test]
    fn test_mst_weight() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 10);
        graph.add_edge(0, 2, 6);
        graph.add_edge(0, 3, 5);
        graph.add_edge(1, 3, 15);
        graph.add_edge(2, 3, 4);

        assert_eq!(graph.mst_weight(), Some(19));
    }

    #[test]
    fn test_large_graph() {
        let mut graph = Graph::new(100);
        // Create a path graph with weight 1
        for i in 0..99 {
            graph.add_edge(i, i + 1, 1);
        }
        // Add some cross edges with higher weights
        graph.add_edge(0, 50, 100);
        graph.add_edge(25, 75, 100);

        let result = graph.prim(0);
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 99);
        assert_eq!(edges.len(), 99);
    }
}
