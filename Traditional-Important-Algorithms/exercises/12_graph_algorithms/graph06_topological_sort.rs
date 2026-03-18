// graph06_topological_sort.rs
//
// Topological Sort Algorithms
//
// Topological sorting orders vertices of a Directed Acyclic Graph (DAG) such that
// for every directed edge (u, v), vertex u comes before v in the ordering.
// Two common approaches: Kahn's algorithm (BFS-based) and DFS-based algorithm.
//
// Time Complexity: O(V + E) for both algorithms
// Space Complexity: O(V) for in-degree array and queue/stack
//
// Key concepts:
// - Only works on DAGs (Directed Acyclic Graphs)
// - Kahn's algorithm: Remove vertices with in-degree 0 iteratively
// - DFS-based: Post-order DFS traversal, reverse the result
// - Can detect cycles (if sort fails to include all vertices)
// - Multiple valid topological orderings may exist
//
// Your task: Implement both Kahn's and DFS-based topological sort algorithms.

// I AM NOT DONE

use std::collections::{HashMap, HashSet, VecDeque};

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

    pub fn add_edge(&mut self, from: usize, to: usize) {
        // TODO: Add directed edge from 'from' to 'to'
        todo!()
    }

    pub fn topological_sort_kahn(&self) -> Result<Vec<usize>, String> {
        // TODO: Implement Kahn's algorithm (BFS-based topological sort)
        // Returns Ok(sorted_vertices) or Err("Graph contains cycle")
        //
        // Algorithm:
        // 1. Calculate in-degree for each vertex
        // 2. Initialize queue with all vertices having in-degree 0
        // 3. While queue is not empty:
        //    a. Remove vertex from queue, add to result
        //    b. For each neighbor, decrement in-degree
        //    c. If neighbor's in-degree becomes 0, add to queue
        // 4. If result contains all vertices, return Ok(result)
        //    Otherwise, return Err (cycle detected)
        todo!()
    }

    pub fn topological_sort_dfs(&self) -> Result<Vec<usize>, String> {
        // TODO: Implement DFS-based topological sort
        // Returns Ok(sorted_vertices) or Err("Graph contains cycle")
        //
        // Algorithm:
        // 1. Initialize visited and recursion stack sets
        // 2. Initialize empty result stack
        // 3. For each unvisited vertex:
        //    a. Call DFS helper
        // 4. Reverse result and return
        //
        // DFS helper:
        // - If vertex in recursion stack, cycle detected
        // - If already visited, return
        // - Mark as in recursion stack
        // - Recursively visit all neighbors
        // - Remove from recursion stack, mark as visited
        // - Add to result stack
        todo!()
    }

    fn dfs_helper(
        &self,
        v: usize,
        visited: &mut HashSet<usize>,
        rec_stack: &mut HashSet<usize>,
        result: &mut Vec<usize>,
    ) -> bool {
        // TODO: DFS helper for topological sort
        // Returns true if cycle detected, false otherwise
        todo!()
    }

    pub fn is_dag(&self) -> bool {
        // TODO: Check if graph is a DAG (Directed Acyclic Graph)
        // Try topological sort - if it succeeds, it's a DAG
        todo!()
    }

    pub fn all_topological_sorts(&self) -> Vec<Vec<usize>> {
        // TODO: Find all possible topological orderings
        // Use backtracking to generate all valid orderings
        // This is more complex - consider vertices with in-degree 0 at each step
        todo!()
    }

    fn all_topological_sorts_helper(
        &self,
        in_degree: &mut HashMap<usize, usize>,
        current: &mut Vec<usize>,
        visited: &mut HashSet<usize>,
        result: &mut Vec<Vec<usize>>,
    ) {
        // TODO: Backtracking helper for finding all topological sorts
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_dag() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(1, 3);
        graph.add_edge(2, 3);

        let result = graph.topological_sort_kahn();
        assert!(result.is_ok());
        let order = result.unwrap();
        assert_eq!(order.len(), 4);
        // 0 should come before 1 and 2
        assert!(order.iter().position(|&x| x == 0).unwrap() < order.iter().position(|&x| x == 1).unwrap());
        assert!(order.iter().position(|&x| x == 0).unwrap() < order.iter().position(|&x| x == 2).unwrap());
        // 1 and 2 should come before 3
        assert!(order.iter().position(|&x| x == 1).unwrap() < order.iter().position(|&x| x == 3).unwrap());
        assert!(order.iter().position(|&x| x == 2).unwrap() < order.iter().position(|&x| x == 3).unwrap());
    }

    #[test]
    fn test_dfs_topological_sort() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(1, 3);
        graph.add_edge(2, 3);

        let result = graph.topological_sort_dfs();
        assert!(result.is_ok());
        let order = result.unwrap();
        assert_eq!(order.len(), 4);
        // Same ordering constraints as above
        assert!(order.iter().position(|&x| x == 0).unwrap() < order.iter().position(|&x| x == 1).unwrap());
        assert!(order.iter().position(|&x| x == 1).unwrap() < order.iter().position(|&x| x == 3).unwrap());
    }

    #[test]
    fn test_cycle_detection_kahn() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0); // Creates cycle

        let result = graph.topological_sort_kahn();
        assert!(result.is_err());
    }

    #[test]
    fn test_cycle_detection_dfs() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        let result = graph.topological_sort_dfs();
        assert!(result.is_err());
    }

    #[test]
    fn test_linear_graph() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 3);
        graph.add_edge(3, 4);

        let result = graph.topological_sort_kahn();
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), vec![0, 1, 2, 3, 4]);
    }

    #[test]
    fn test_disconnected_dag() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1);
        graph.add_edge(2, 3);
        // Vertex 4 is isolated

        let result = graph.topological_sort_kahn();
        assert!(result.is_ok());
        let order = result.unwrap();
        assert_eq!(order.len(), 5);
        assert!(order.iter().position(|&x| x == 0).unwrap() < order.iter().position(|&x| x == 1).unwrap());
        assert!(order.iter().position(|&x| x == 2).unwrap() < order.iter().position(|&x| x == 3).unwrap());
    }

    #[test]
    fn test_is_dag() {
        let mut dag = Graph::new(3);
        dag.add_edge(0, 1);
        dag.add_edge(1, 2);
        assert!(dag.is_dag());

        let mut cyclic = Graph::new(3);
        cyclic.add_edge(0, 1);
        cyclic.add_edge(1, 2);
        cyclic.add_edge(2, 0);
        assert!(!cyclic.is_dag());
    }

    #[test]
    fn test_self_loop() {
        let mut graph = Graph::new(2);
        graph.add_edge(0, 0); // Self loop creates cycle

        assert!(!graph.is_dag());
    }

    #[test]
    fn test_empty_graph() {
        let graph = Graph::new(3);
        let result = graph.topological_sort_kahn();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().len(), 3);
    }

    #[test]
    fn test_all_topological_sorts() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 2);
        graph.add_edge(1, 2);

        let all_sorts = graph.all_topological_sorts();
        assert!(all_sorts.len() >= 1);
        // Valid orderings: [0,1,2] or [1,0,2]
        for sort in all_sorts {
            assert_eq!(sort.len(), 3);
            assert_eq!(sort[2], 2); // 2 must be last
            assert!(sort[0] == 0 || sort[0] == 1);
        }
    }

    #[test]
    fn test_both_algorithms_same_result() {
        let mut graph = Graph::new(6);
        graph.add_edge(5, 2);
        graph.add_edge(5, 0);
        graph.add_edge(4, 0);
        graph.add_edge(4, 1);
        graph.add_edge(2, 3);
        graph.add_edge(3, 1);

        let kahn_result = graph.topological_sort_kahn();
        let dfs_result = graph.topological_sort_dfs();

        assert!(kahn_result.is_ok());
        assert!(dfs_result.is_ok());

        let kahn_order = kahn_result.unwrap();
        let dfs_order = dfs_result.unwrap();

        // Both should contain all vertices
        assert_eq!(kahn_order.len(), 6);
        assert_eq!(dfs_order.len(), 6);

        // Verify both orderings are valid (respect edge constraints)
        assert!(kahn_order.iter().position(|&x| x == 5).unwrap() < kahn_order.iter().position(|&x| x == 2).unwrap());
        assert!(dfs_order.iter().position(|&x| x == 5).unwrap() < dfs_order.iter().position(|&x| x == 2).unwrap());
    }

    #[test]
    fn test_complex_dag() {
        let mut graph = Graph::new(8);
        graph.add_edge(0, 3);
        graph.add_edge(0, 4);
        graph.add_edge(1, 3);
        graph.add_edge(2, 4);
        graph.add_edge(2, 7);
        graph.add_edge(3, 5);
        graph.add_edge(3, 6);
        graph.add_edge(4, 6);

        assert!(graph.is_dag());
        let result = graph.topological_sort_kahn();
        assert!(result.is_ok());
        assert_eq!(result.unwrap().len(), 8);
    }
}
