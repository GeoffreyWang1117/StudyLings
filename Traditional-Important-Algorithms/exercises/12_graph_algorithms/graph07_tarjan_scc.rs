// graph07_tarjan_scc.rs
//
// Tarjan's Strongly Connected Components Algorithm
//
// A strongly connected component (SCC) is a maximal set of vertices where every
// vertex is reachable from every other vertex. Tarjan's algorithm finds all SCCs
// in a directed graph using a single DFS pass with a stack.
//
// Time Complexity: O(V + E) where V = vertices, E = edges
// Space Complexity: O(V) for stack, index arrays, and recursion
//
// Key concepts:
// - Single DFS pass to find all SCCs
// - Low-link values: smallest index reachable from subtree
// - Stack maintains vertices in current SCC candidate
// - When low[v] == index[v], v is root of an SCC
// - Also useful for finding bridges and articulation points
//
// Your task: Implement Tarjan's SCC algorithm.

// I AM NOT DONE

use std::collections::HashMap;

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

    pub fn tarjan_scc(&self) -> Vec<Vec<usize>> {
        // TODO: Implement Tarjan's algorithm to find all SCCs
        // Returns vector of SCCs, where each SCC is a vector of vertices
        //
        // Algorithm:
        // 1. Initialize:
        //    - index: discovery time of each vertex
        //    - low_link: lowest index reachable from vertex
        //    - on_stack: whether vertex is on stack
        //    - stack: vertices in current path
        //    - current_index: global counter
        // 2. For each unvisited vertex, call strongconnect
        // 3. Return all found SCCs
        todo!()
    }

    fn strongconnect(
        &self,
        v: usize,
        index: &mut HashMap<usize, usize>,
        low_link: &mut HashMap<usize, usize>,
        on_stack: &mut HashMap<usize, bool>,
        stack: &mut Vec<usize>,
        current_index: &mut usize,
        sccs: &mut Vec<Vec<usize>>,
    ) {
        // TODO: Recursive helper for Tarjan's algorithm
        //
        // 1. Set index[v] and low_link[v] to current_index
        // 2. Increment current_index
        // 3. Push v onto stack, mark on_stack[v] = true
        // 4. For each neighbor w of v:
        //    a. If w not visited:
        //       - Recursively call strongconnect(w)
        //       - Update low_link[v] = min(low_link[v], low_link[w])
        //    b. Else if w is on stack:
        //       - Update low_link[v] = min(low_link[v], index[w])
        // 5. If low_link[v] == index[v]:
        //    - v is root of SCC
        //    - Pop vertices from stack until v is popped
        //    - Add them as a new SCC
        todo!()
    }

    pub fn count_sccs(&self) -> usize {
        // TODO: Return number of strongly connected components
        todo!()
    }

    pub fn is_strongly_connected(&self) -> bool {
        // TODO: Check if entire graph is one SCC
        todo!()
    }

    pub fn condensation_graph(&self) -> (Graph, HashMap<usize, usize>) {
        // TODO: Build condensation graph (DAG of SCCs)
        // Returns (condensation_graph, vertex_to_scc_map)
        // In condensation graph:
        // - Each SCC becomes a single vertex
        // - Edge exists between SCC_i and SCC_j if any edge exists
        //   from a vertex in SCC_i to a vertex in SCC_j
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_scc() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 1);
        assert_eq!(sccs[0].len(), 3);
    }

    #[test]
    fn test_multiple_sccs() {
        let mut graph = Graph::new(5);
        // SCC 1: {0, 1, 2}
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);
        // SCC 2: {3, 4}
        graph.add_edge(3, 4);
        graph.add_edge(4, 3);
        // Edge between SCCs
        graph.add_edge(2, 3);

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 2);
    }

    #[test]
    fn test_linear_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 3);

        let sccs = graph.tarjan_scc();
        // Each vertex is its own SCC
        assert_eq!(sccs.len(), 4);
        for scc in sccs {
            assert_eq!(scc.len(), 1);
        }
    }

    #[test]
    fn test_self_loop() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1);
        graph.add_edge(1, 1); // self loop
        graph.add_edge(1, 2);

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 3);
    }

    #[test]
    fn test_disconnected_components() {
        let mut graph = Graph::new(6);
        // Component 1: {0, 1}
        graph.add_edge(0, 1);
        graph.add_edge(1, 0);
        // Component 2: {2, 3}
        graph.add_edge(2, 3);
        graph.add_edge(3, 2);
        // Isolated vertices: {4}, {5}

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 4);
    }

    #[test]
    fn test_complex_graph() {
        let mut graph = Graph::new(8);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);
        graph.add_edge(2, 3);
        graph.add_edge(3, 4);
        graph.add_edge(4, 5);
        graph.add_edge(5, 3);
        graph.add_edge(5, 6);
        graph.add_edge(6, 7);
        graph.add_edge(7, 6);

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 3);
        // SCC 1: {0,1,2}, SCC 2: {3,4,5}, SCC 3: {6,7}
    }

    #[test]
    fn test_count_sccs() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);
        graph.add_edge(3, 4);

        assert_eq!(graph.count_sccs(), 3); // {0,1,2}, {3}, {4}
    }

    #[test]
    fn test_is_strongly_connected() {
        let mut strongly = Graph::new(3);
        strongly.add_edge(0, 1);
        strongly.add_edge(1, 2);
        strongly.add_edge(2, 0);
        assert!(strongly.is_strongly_connected());

        let mut weakly = Graph::new(3);
        weakly.add_edge(0, 1);
        weakly.add_edge(1, 2);
        assert!(!weakly.is_strongly_connected());
    }

    #[test]
    fn test_empty_graph() {
        let graph = Graph::new(3);
        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 3); // Each vertex is its own SCC
    }

    #[test]
    fn test_bidirectional_edges() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1);
        graph.add_edge(1, 0);
        graph.add_edge(2, 3);
        graph.add_edge(3, 2);

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 2);
    }

    #[test]
    fn test_condensation_graph() {
        let mut graph = Graph::new(5);
        // SCC 1: {0, 1, 2}
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 0);
        // SCC 2: {3, 4}
        graph.add_edge(3, 4);
        graph.add_edge(4, 3);
        // Edge from SCC 1 to SCC 2
        graph.add_edge(2, 3);

        let (condensed, vertex_to_scc) = graph.condensation_graph();
        // Should have 2 SCCs
        assert_eq!(condensed.num_vertices, 2);
        // Verify vertices are mapped correctly
        assert_eq!(vertex_to_scc[&0], vertex_to_scc[&1]);
        assert_eq!(vertex_to_scc[&0], vertex_to_scc[&2]);
        assert_eq!(vertex_to_scc[&3], vertex_to_scc[&4]);
        assert_ne!(vertex_to_scc[&0], vertex_to_scc[&3]);
    }

    #[test]
    fn test_large_cycle() {
        let mut graph = Graph::new(100);
        for i in 0..99 {
            graph.add_edge(i, i + 1);
        }
        graph.add_edge(99, 0); // Complete the cycle

        let sccs = graph.tarjan_scc();
        assert_eq!(sccs.len(), 1);
        assert_eq!(sccs[0].len(), 100);
    }
}
