// graph08_max_flow.rs
//
// Maximum Flow Algorithms (Ford-Fulkerson and Edmonds-Karp)
//
// The maximum flow problem finds the maximum amount of flow that can be sent
// from a source to a sink in a flow network. Ford-Fulkerson is the general
// method; Edmonds-Karp is a specific implementation using BFS for augmenting paths.
//
// Time Complexity:
// - Ford-Fulkerson: O(E * max_flow) - depends on flow value
// - Edmonds-Karp: O(V * E²) - polynomial time guarantee
// Space Complexity: O(V²) for capacity/flow matrices or O(V + E) for adjacency list
//
// Key concepts:
// - Residual graph: remaining capacity after flow
// - Augmenting path: path from source to sink with available capacity
// - Max-flow min-cut theorem: max flow equals min cut capacity
// - Multiple applications: network routing, bipartite matching, etc.
//
// Your task: Implement both Ford-Fulkerson and Edmonds-Karp algorithms.

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

pub struct FlowNetwork {
    // Capacity matrix: capacity[u][v] = capacity of edge u->v
    capacity: Vec<Vec<i32>>,
    // Flow matrix: flow[u][v] = current flow on edge u->v
    flow: Vec<Vec<i32>>,
    num_vertices: usize,
}

impl FlowNetwork {
    pub fn new(num_vertices: usize) -> Self {
        // TODO: Initialize capacity and flow matrices with zeros
        todo!()
    }

    pub fn add_edge(&mut self, from: usize, to: usize, capacity: i32) {
        // TODO: Add edge with given capacity
        // Set capacity[from][to] = capacity
        // For undirected edges, also set capacity[to][from] = capacity
        todo!()
    }

    pub fn ford_fulkerson(&mut self, source: usize, sink: usize) -> i32 {
        // TODO: Implement Ford-Fulkerson algorithm using DFS
        // Returns maximum flow from source to sink
        //
        // Algorithm:
        // 1. Initialize flow to 0
        // 2. While augmenting path exists (using DFS):
        //    a. Find path and bottleneck capacity
        //    b. Update flow along path
        //    c. Add bottleneck to total flow
        // 3. Return total flow
        todo!()
    }

    pub fn edmonds_karp(&mut self, source: usize, sink: usize) -> i32 {
        // TODO: Implement Edmonds-Karp algorithm using BFS
        // Returns maximum flow from source to sink
        //
        // Algorithm (same as Ford-Fulkerson but uses BFS):
        // 1. Initialize flow to 0
        // 2. While augmenting path exists (using BFS):
        //    a. Find shortest augmenting path
        //    b. Find bottleneck capacity on path
        //    c. Update flow along path
        //    d. Add bottleneck to total flow
        // 3. Return total flow
        todo!()
    }

    fn bfs_augmenting_path(&self, source: usize, sink: usize) -> Option<(Vec<usize>, i32)> {
        // TODO: Find augmenting path from source to sink using BFS
        // Returns Some((path, bottleneck_capacity)) or None if no path exists
        //
        // Use residual capacity: residual[u][v] = capacity[u][v] - flow[u][v]
        // Consider edge only if residual capacity > 0
        todo!()
    }

    fn dfs_augmenting_path(
        &self,
        current: usize,
        sink: usize,
        visited: &mut Vec<bool>,
        path: &mut Vec<usize>,
        min_capacity: i32,
    ) -> Option<i32> {
        // TODO: DFS helper to find augmenting path
        // Returns Some(bottleneck_capacity) if path found, None otherwise
        todo!()
    }

    pub fn min_cut(&self, source: usize) -> (Vec<usize>, Vec<usize>) {
        // TODO: Find minimum cut in the network after computing max flow
        // Returns (source_side, sink_side) - partition of vertices
        //
        // After max flow is computed:
        // 1. Run DFS/BFS from source using only edges with residual capacity > 0
        // 2. Vertices reachable from source form one side of cut
        // 3. Remaining vertices form other side
        todo!()
    }

    pub fn get_flow(&self, from: usize, to: usize) -> i32 {
        // TODO: Return flow on edge from->to
        todo!()
    }

    pub fn reset_flow(&mut self) {
        // TODO: Reset all flows to zero
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_flow() {
        let mut network = FlowNetwork::new(4);
        network.add_edge(0, 1, 10);
        network.add_edge(1, 2, 5);
        network.add_edge(2, 3, 10);

        let max_flow = network.edmonds_karp(0, 3);
        assert_eq!(max_flow, 5); // Bottleneck is edge 1->2
    }

    #[test]
    fn test_multiple_paths() {
        let mut network = FlowNetwork::new(4);
        network.add_edge(0, 1, 10);
        network.add_edge(0, 2, 10);
        network.add_edge(1, 3, 10);
        network.add_edge(2, 3, 10);

        let max_flow = network.edmonds_karp(0, 3);
        assert_eq!(max_flow, 20); // Both paths contribute 10 each
    }

    #[test]
    fn test_bottleneck() {
        let mut network = FlowNetwork::new(6);
        network.add_edge(0, 1, 16);
        network.add_edge(0, 2, 13);
        network.add_edge(1, 2, 10);
        network.add_edge(1, 3, 12);
        network.add_edge(2, 1, 4);
        network.add_edge(2, 4, 14);
        network.add_edge(3, 2, 9);
        network.add_edge(3, 5, 20);
        network.add_edge(4, 3, 7);
        network.add_edge(4, 5, 4);

        let max_flow = network.edmonds_karp(0, 5);
        assert_eq!(max_flow, 23);
    }

    #[test]
    fn test_no_path() {
        let mut network = FlowNetwork::new(4);
        network.add_edge(0, 1, 10);
        network.add_edge(2, 3, 10);
        // No path from 0 to 3

        let max_flow = network.edmonds_karp(0, 3);
        assert_eq!(max_flow, 0);
    }

    #[test]
    fn test_zero_capacity() {
        let mut network = FlowNetwork::new(3);
        network.add_edge(0, 1, 0);
        network.add_edge(1, 2, 10);

        let max_flow = network.edmonds_karp(0, 2);
        assert_eq!(max_flow, 0);
    }

    #[test]
    fn test_ford_fulkerson() {
        let mut network = FlowNetwork::new(4);
        network.add_edge(0, 1, 10);
        network.add_edge(0, 2, 10);
        network.add_edge(1, 3, 10);
        network.add_edge(2, 3, 10);

        let max_flow = network.ford_fulkerson(0, 3);
        assert_eq!(max_flow, 20);
    }

    #[test]
    fn test_both_algorithms_same_result() {
        let mut network1 = FlowNetwork::new(6);
        let mut network2 = FlowNetwork::new(6);

        let edges = vec![
            (0, 1, 16), (0, 2, 13), (1, 2, 10),
            (1, 3, 12), (2, 4, 14), (3, 5, 20),
            (4, 3, 7), (4, 5, 4),
        ];

        for (u, v, c) in edges {
            network1.add_edge(u, v, c);
            network2.add_edge(u, v, c);
        }

        let flow1 = network1.ford_fulkerson(0, 5);
        let flow2 = network2.edmonds_karp(0, 5);

        assert_eq!(flow1, flow2);
    }

    #[test]
    fn test_min_cut() {
        let mut network = FlowNetwork::new(4);
        network.add_edge(0, 1, 10);
        network.add_edge(0, 2, 10);
        network.add_edge(1, 3, 10);
        network.add_edge(2, 3, 10);

        network.edmonds_karp(0, 3);
        let (source_side, sink_side) = network.min_cut(0);

        assert!(source_side.contains(&0));
        assert!(sink_side.contains(&3));
        assert_eq!(source_side.len() + sink_side.len(), 4);
    }

    #[test]
    fn test_get_flow() {
        let mut network = FlowNetwork::new(3);
        network.add_edge(0, 1, 10);
        network.add_edge(1, 2, 5);

        network.edmonds_karp(0, 2);

        assert_eq!(network.get_flow(0, 1), 5);
        assert_eq!(network.get_flow(1, 2), 5);
    }

    #[test]
    fn test_reset_flow() {
        let mut network = FlowNetwork::new(3);
        network.add_edge(0, 1, 10);
        network.add_edge(1, 2, 10);

        network.edmonds_karp(0, 2);
        assert_eq!(network.get_flow(0, 1), 10);

        network.reset_flow();
        assert_eq!(network.get_flow(0, 1), 0);
    }

    #[test]
    fn test_bipartite_matching() {
        // Maximum bipartite matching using max flow
        // Left set: {0, 1, 2}, Right set: {3, 4, 5}
        // Source: 6, Sink: 7
        let mut network = FlowNetwork::new(8);

        // Source to left set
        network.add_edge(6, 0, 1);
        network.add_edge(6, 1, 1);
        network.add_edge(6, 2, 1);

        // Left to right (edges in bipartite graph)
        network.add_edge(0, 3, 1);
        network.add_edge(0, 4, 1);
        network.add_edge(1, 4, 1);
        network.add_edge(2, 5, 1);

        // Right set to sink
        network.add_edge(3, 7, 1);
        network.add_edge(4, 7, 1);
        network.add_edge(5, 7, 1);

        let max_matching = network.edmonds_karp(6, 7);
        assert_eq!(max_matching, 3); // Perfect matching
    }

    #[test]
    fn test_single_edge() {
        let mut network = FlowNetwork::new(2);
        network.add_edge(0, 1, 42);

        let max_flow = network.edmonds_karp(0, 1);
        assert_eq!(max_flow, 42);
    }
}
