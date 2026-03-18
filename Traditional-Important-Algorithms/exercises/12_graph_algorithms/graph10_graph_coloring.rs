// graph10_graph_coloring.rs
//
// Graph Coloring Algorithms
//
// Graph coloring assigns colors to vertices such that no two adjacent vertices
// share the same color. The goal is to use the minimum number of colors (chromatic
// number). This is an NP-complete problem, but approximation algorithms exist.
//
// Time Complexity:
// - Greedy: O(V + E)
// - Backtracking: O(k^V) worst case, where k = number of colors
// Space Complexity: O(V) for color assignments
//
// Key concepts:
// - Chromatic number: minimum colors needed
// - Greedy coloring: heuristic that gives upper bound
// - Backtracking: finds optimal solution but exponential time
// - Applications: register allocation, scheduling, map coloring
// - Welsh-Powell algorithm: greedy with vertex ordering by degree
//
// Your task: Implement greedy and backtracking graph coloring algorithms.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

pub struct Graph {
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

    pub fn add_edge(&mut self, u: usize, v: usize) {
        // TODO: Add undirected edge between u and v
        todo!()
    }

    pub fn greedy_coloring(&self) -> HashMap<usize, usize> {
        // TODO: Implement greedy graph coloring
        // Returns map of vertex -> color
        //
        // Algorithm:
        // 1. For each vertex in order (0 to n-1):
        //    a. Find colors used by adjacent vertices
        //    b. Assign smallest available color (starting from 0)
        // 2. Return color assignment
        //
        // Note: This gives an upper bound but may not be optimal
        todo!()
    }

    pub fn welsh_powell_coloring(&self) -> HashMap<usize, usize> {
        // TODO: Implement Welsh-Powell algorithm (improved greedy)
        // Returns map of vertex -> color
        //
        // Algorithm:
        // 1. Sort vertices by degree (highest first)
        // 2. Apply greedy coloring in this order
        // 3. Return color assignment
        //
        // Generally produces better results than simple greedy
        todo!()
    }

    pub fn backtracking_coloring(&self, max_colors: usize) -> Option<HashMap<usize, usize>> {
        // TODO: Implement backtracking to find optimal coloring
        // Returns Some(coloring) if graph can be colored with max_colors,
        // None otherwise
        //
        // Algorithm:
        // 1. Try to assign colors to vertices one by one
        // 2. For each vertex, try each color from 0 to max_colors-1
        // 3. Check if color is safe (no adjacent vertex has same color)
        // 4. If safe, assign and recurse
        // 5. If recursion succeeds, return solution
        // 6. If recursion fails, backtrack and try next color
        // 7. If no color works, return None
        todo!()
    }

    fn is_safe_color(
        &self,
        vertex: usize,
        color: usize,
        coloring: &HashMap<usize, usize>,
    ) -> bool {
        // TODO: Check if assigning 'color' to 'vertex' is safe
        // Safe means no adjacent vertex has the same color
        todo!()
    }

    fn backtrack_helper(
        &self,
        vertex: usize,
        max_colors: usize,
        coloring: &mut HashMap<usize, usize>,
    ) -> bool {
        // TODO: Recursive backtracking helper
        // Returns true if coloring is successful, false otherwise
        todo!()
    }

    pub fn chromatic_number(&self) -> usize {
        // TODO: Find chromatic number (minimum colors needed)
        // Try backtracking with increasing number of colors
        // Start from 1 and increment until solution found
        todo!()
    }

    pub fn is_bipartite(&self) -> bool {
        // TODO: Check if graph is bipartite (2-colorable)
        // Use BFS or DFS to attempt 2-coloring
        todo!()
    }

    pub fn get_degree(&self, vertex: usize) -> usize {
        // TODO: Return degree of vertex (number of adjacent vertices)
        todo!()
    }

    pub fn verify_coloring(&self, coloring: &HashMap<usize, usize>) -> bool {
        // TODO: Verify that a coloring is valid
        // Check that no two adjacent vertices have the same color
        todo!()
    }

    pub fn count_colors(&self, coloring: &HashMap<usize, usize>) -> usize {
        // TODO: Count number of distinct colors used in coloring
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_coloring() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);

        let coloring = graph.greedy_coloring();
        assert_eq!(coloring.len(), 3);
        assert_ne!(coloring[&0], coloring[&1]);
        assert_ne!(coloring[&1], coloring[&2]);
        // 0 and 2 can have same color
    }

    #[test]
    fn test_triangle_coloring() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        let coloring = graph.greedy_coloring();
        // All three vertices need different colors
        assert_ne!(coloring[&0], coloring[&1]);
        assert_ne!(coloring[&1], coloring[&2]);
        assert_ne!(coloring[&2], coloring[&0]);

        assert!(graph.verify_coloring(&coloring));
    }

    #[test]
    fn test_bipartite_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 2);
        graph.add_edge(0, 3);
        graph.add_edge(1, 2);
        graph.add_edge(1, 3);

        assert!(graph.is_bipartite());

        let coloring = graph.greedy_coloring();
        assert!(graph.count_colors(&coloring) <= 2);
    }

    #[test]
    fn test_non_bipartite() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0); // Triangle

        assert!(!graph.is_bipartite());
    }

    #[test]
    fn test_complete_graph() {
        let mut graph = Graph::new(4);
        // K4 - complete graph on 4 vertices
        for i in 0..4 {
            for j in i + 1..4 {
                graph.add_edge(i, j);
            }
        }

        let coloring = graph.greedy_coloring();
        assert!(graph.verify_coloring(&coloring));
        assert_eq!(graph.count_colors(&coloring), 4);
    }

    #[test]
    fn test_welsh_powell() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(0, 3);
        graph.add_edge(0, 4);
        graph.add_edge(1, 2);
        graph.add_edge(3, 4);

        let coloring = graph.welsh_powell_coloring();
        assert!(graph.verify_coloring(&coloring));

        // Should use 3 colors optimally
        assert!(graph.count_colors(&coloring) <= 4);
    }

    #[test]
    fn test_backtracking_coloring() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        // Triangle needs at least 3 colors
        assert!(graph.backtracking_coloring(2).is_none());

        let coloring = graph.backtracking_coloring(3);
        assert!(coloring.is_some());
        assert!(graph.verify_coloring(&coloring.unwrap()));
    }

    #[test]
    fn test_chromatic_number() {
        let mut triangle = Graph::new(3);
        triangle.add_edge(0, 1);
        triangle.add_edge(1, 2);
        triangle.add_edge(2, 0);
        assert_eq!(triangle.chromatic_number(), 3);

        let mut line = Graph::new(3);
        line.add_edge(0, 1);
        line.add_edge(1, 2);
        assert_eq!(line.chromatic_number(), 2);
    }

    #[test]
    fn test_empty_graph() {
        let graph = Graph::new(5);
        let coloring = graph.greedy_coloring();

        // All vertices can have same color
        assert_eq!(graph.count_colors(&coloring), 1);
    }

    #[test]
    fn test_verify_coloring() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);

        let mut valid_coloring = HashMap::new();
        valid_coloring.insert(0, 0);
        valid_coloring.insert(1, 1);
        valid_coloring.insert(2, 0);
        assert!(graph.verify_coloring(&valid_coloring));

        let mut invalid_coloring = HashMap::new();
        invalid_coloring.insert(0, 0);
        invalid_coloring.insert(1, 0);
        invalid_coloring.insert(2, 1);
        assert!(!graph.verify_coloring(&invalid_coloring));
    }

    #[test]
    fn test_get_degree() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(0, 3);

        assert_eq!(graph.get_degree(0), 3);
        assert_eq!(graph.get_degree(1), 1);
    }

    #[test]
    fn test_large_bipartite() {
        let mut graph = Graph::new(100);
        // Create bipartite graph: even vertices connect to odd vertices
        for i in (0..100).step_by(2) {
            for j in (1..100).step_by(2) {
                if i + j < 100 {
                    graph.add_edge(i, j);
                }
            }
        }

        assert!(graph.is_bipartite());
        let coloring = graph.greedy_coloring();
        assert!(graph.count_colors(&coloring) <= 2);
    }

    #[test]
    fn test_count_colors() {
        let mut coloring = HashMap::new();
        coloring.insert(0, 0);
        coloring.insert(1, 1);
        coloring.insert(2, 0);
        coloring.insert(3, 2);

        let graph = Graph::new(4);
        assert_eq!(graph.count_colors(&coloring), 3);
    }
}
