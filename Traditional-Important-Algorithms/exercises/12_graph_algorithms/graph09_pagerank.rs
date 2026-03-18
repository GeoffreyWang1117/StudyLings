// graph09_pagerank.rs
//
// PageRank Algorithm
//
// PageRank is Google's algorithm for ranking web pages by importance. It models
// a random surfer who clicks on links with probability d (damping factor) or
// jumps to a random page with probability (1-d). The PageRank of a page is
// the probability that the random surfer is at that page.
//
// Time Complexity: O(iterations * E) where E = number of edges
// Space Complexity: O(V) for rank vectors
//
// Key concepts:
// - Iterative algorithm converging to steady state
// - Damping factor (typically 0.85) handles dead ends and teleportation
// - Power iteration method to solve eigenvector equation
// - Rank is distributed from a page to its outgoing links
// - Handles dangling nodes (pages with no outlinks)
//
// Your task: Implement PageRank algorithm with damping factor and convergence.

// I AM NOT DONE

use std::collections::HashMap;

pub struct Graph {
    // Adjacency list: node -> vec of outgoing links
    adj: HashMap<usize, Vec<usize>>,
    num_vertices: usize,
}

impl Graph {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            adj: HashMap::new(),
            num_vertices,
        }
    }

    pub fn add_edge(&mut self, from: usize, to: usize) {
        // TODO: Add directed edge from 'from' to 'to'
        todo!()
    }

    pub fn pagerank(&self, damping_factor: f64, max_iterations: usize, tolerance: f64) -> Vec<f64> {
        // TODO: Implement PageRank algorithm
        // Returns vector of PageRank scores for each vertex
        //
        // Algorithm:
        // 1. Initialize all ranks to 1/N where N = num_vertices
        // 2. For each iteration:
        //    a. Create new_rank vector, initialize all to (1-d)/N
        //    b. For each vertex v:
        //       - Calculate rank contribution: rank[v] / out_degree[v]
        //       - Distribute to all outgoing neighbors
        //    c. Handle dangling nodes (no outlinks):
        //       - Distribute their rank equally to all nodes
        //    d. Check convergence: if max change < tolerance, stop
        //    e. Update ranks with new_rank
        // 3. Return final ranks
        //
        // PageRank formula:
        // PR(v) = (1-d)/N + d * Σ(PR(u)/out_degree(u)) for all u linking to v
        todo!()
    }

    pub fn pagerank_simple(&self, iterations: usize) -> Vec<f64> {
        // TODO: Simplified PageRank with default damping factor 0.85
        todo!()
    }

    pub fn get_out_degree(&self, vertex: usize) -> usize {
        // TODO: Return number of outgoing edges from vertex
        todo!()
    }

    pub fn get_dangling_nodes(&self) -> Vec<usize> {
        // TODO: Return vertices with no outgoing edges
        todo!()
    }

    pub fn top_k_pages(&self, k: usize, damping_factor: f64) -> Vec<(usize, f64)> {
        // TODO: Return top k pages by PageRank score
        // Returns vector of (vertex_id, score) sorted by score descending
        todo!()
    }

    pub fn normalize_scores(&self, scores: &mut Vec<f64>) {
        // TODO: Normalize scores so they sum to 1.0
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_equal(a: f64, b: f64, epsilon: f64) -> bool {
        (a - b).abs() < epsilon
    }

    #[test]
    fn test_simple_graph() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        let ranks = graph.pagerank(0.85, 100, 1e-6);
        assert_eq!(ranks.len(), 3);

        // All nodes should have equal rank in a cycle
        assert!(approx_equal(ranks[0], ranks[1], 1e-3));
        assert!(approx_equal(ranks[1], ranks[2], 1e-3));

        // Sum should be approximately 1
        let sum: f64 = ranks.iter().sum();
        assert!(approx_equal(sum, 1.0, 1e-3));
    }

    #[test]
    fn test_star_graph() {
        let mut graph = Graph::new(4);
        // Node 0 links to all others
        graph.add_edge(1, 0);
        graph.add_edge(2, 0);
        graph.add_edge(3, 0);

        let ranks = graph.pagerank(0.85, 100, 1e-6);

        // Node 0 should have highest rank
        assert!(ranks[0] > ranks[1]);
        assert!(ranks[0] > ranks[2]);
        assert!(ranks[0] > ranks[3]);

        // Other nodes should have equal rank
        assert!(approx_equal(ranks[1], ranks[2], 1e-3));
        assert!(approx_equal(ranks[2], ranks[3], 1e-3));
    }

    #[test]
    fn test_linear_chain() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 3);

        let ranks = graph.pagerank(0.85, 100, 1e-6);

        // Later nodes should have higher rank (accumulate from predecessors)
        assert!(ranks[3] > ranks[0]);
    }

    #[test]
    fn test_dangling_node() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        // Node 2 is dangling (no outlinks)

        let dangling = graph.get_dangling_nodes();
        assert!(dangling.contains(&2));

        let ranks = graph.pagerank(0.85, 100, 1e-6);
        // Should still converge
        let sum: f64 = ranks.iter().sum();
        assert!(approx_equal(sum, 1.0, 1e-2));
    }

    #[test]
    fn test_different_damping_factors() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        let ranks_085 = graph.pagerank(0.85, 100, 1e-6);
        let ranks_050 = graph.pagerank(0.50, 100, 1e-6);

        // Results should be different but both valid
        assert!(!approx_equal(ranks_085[0], ranks_050[0], 1e-6));

        let sum1: f64 = ranks_085.iter().sum();
        let sum2: f64 = ranks_050.iter().sum();
        assert!(approx_equal(sum1, 1.0, 1e-3));
        assert!(approx_equal(sum2, 1.0, 1e-3));
    }

    #[test]
    fn test_single_node() {
        let graph = Graph::new(1);
        let ranks = graph.pagerank(0.85, 100, 1e-6);

        assert_eq!(ranks.len(), 1);
        assert!(approx_equal(ranks[0], 1.0, 1e-3));
    }

    #[test]
    fn test_disconnected_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(2, 3);

        let ranks = graph.pagerank(0.85, 100, 1e-6);

        // All nodes should still get some rank due to teleportation
        for rank in &ranks {
            assert!(*rank > 0.0);
        }

        let sum: f64 = ranks.iter().sum();
        assert!(approx_equal(sum, 1.0, 1e-3));
    }

    #[test]
    fn test_get_out_degree() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);

        assert_eq!(graph.get_out_degree(0), 2);
        assert_eq!(graph.get_out_degree(1), 0);
        assert_eq!(graph.get_out_degree(2), 0);
    }

    #[test]
    fn test_top_k_pages() {
        let mut graph = Graph::new(4);
        graph.add_edge(1, 0);
        graph.add_edge(2, 0);
        graph.add_edge(3, 0);

        let top = graph.top_k_pages(2, 0.85);

        assert_eq!(top.len(), 2);
        // Node 0 should be first
        assert_eq!(top[0].0, 0);
        // Scores should be in descending order
        assert!(top[0].1 >= top[1].1);
    }

    #[test]
    fn test_convergence() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        // Should converge before max iterations
        let ranks1 = graph.pagerank(0.85, 10, 1e-6);
        let ranks2 = graph.pagerank(0.85, 100, 1e-6);

        // Results should be very similar
        for i in 0..3 {
            assert!(approx_equal(ranks1[i], ranks2[i], 1e-3));
        }
    }

    #[test]
    fn test_self_loop() {
        let mut graph = Graph::new(2);
        graph.add_edge(0, 0); // self loop
        graph.add_edge(0, 1);

        let ranks = graph.pagerank(0.85, 100, 1e-6);

        // Should handle self loops gracefully
        let sum: f64 = ranks.iter().sum();
        assert!(approx_equal(sum, 1.0, 1e-3));
    }

    #[test]
    fn test_complex_web_graph() {
        let mut graph = Graph::new(6);
        // Create a more complex web-like structure
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(1, 3);
        graph.add_edge(2, 3);
        graph.add_edge(3, 4);
        graph.add_edge(4, 0);
        graph.add_edge(4, 5);
        graph.add_edge(5, 3);

        let ranks = graph.pagerank(0.85, 100, 1e-6);

        // Node 3 should have high rank (many incoming links)
        assert!(ranks[3] > ranks[0]);
        assert!(ranks[3] > ranks[1]);

        let sum: f64 = ranks.iter().sum();
        assert!(approx_equal(sum, 1.0, 1e-3));
    }
}
