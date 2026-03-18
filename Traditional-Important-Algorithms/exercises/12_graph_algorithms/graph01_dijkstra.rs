// graph01_dijkstra.rs
//
// Dijkstra's Shortest Path Algorithm
//
// Dijkstra's algorithm finds the shortest paths from a source vertex to all other
// vertices in a weighted graph with non-negative edge weights. It uses a greedy
// approach, always selecting the unvisited vertex with the smallest known distance.
//
// Time Complexity: O((V + E) log V) with binary heap, O(V²) with array
// Space Complexity: O(V) for distance array and visited set
//
// Key concepts:
// - Greedy algorithm: Always picks the closest unvisited vertex
// - Priority queue (min-heap) to efficiently get minimum distance vertex
// - Relaxation: Update distance if shorter path found
// - Does NOT work with negative edge weights (use Bellman-Ford instead)
//
// Your task: Implement Dijkstra's algorithm with priority queue optimization.

// I AM NOT DONE

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Ordering;

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
struct State {
    cost: u32,
    node: usize,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Min-heap: reverse the ordering
        other.cost.cmp(&self.cost)
            .then_with(|| self.node.cmp(&other.node))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct Graph {
    // Adjacency list: node -> vec of (neighbor, weight)
    adj: HashMap<usize, Vec<(usize, u32)>>,
    num_vertices: usize,
}

impl Graph {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            adj: HashMap::new(),
            num_vertices,
        }
    }

    pub fn add_edge(&mut self, from: usize, to: usize, weight: u32) {
        // TODO: Add a directed edge from 'from' to 'to' with given weight
        // Use adjacency list representation
        todo!()
    }

    pub fn add_undirected_edge(&mut self, u: usize, v: usize, weight: u32) {
        // TODO: Add an undirected edge (add both directions)
        todo!()
    }

    pub fn dijkstra(&self, start: usize) -> (Vec<Option<u32>>, Vec<Option<usize>>) {
        // TODO: Implement Dijkstra's algorithm
        // Returns (distances, predecessors)
        // - distances[i] = shortest distance from start to i (None if unreachable)
        // - predecessors[i] = previous node in shortest path to i
        //
        // Algorithm:
        // 1. Initialize distances to infinity (None), except start = 0
        // 2. Initialize empty priority queue (min-heap)
        // 3. Push (0, start) to heap
        // 4. While heap is not empty:
        //    a. Pop vertex with minimum distance
        //    b. Skip if already processed (distance check)
        //    c. For each neighbor:
        //       - Calculate new distance through current vertex
        //       - If shorter than known distance, update and push to heap
        // 5. Return distances and predecessors
        todo!()
    }

    pub fn shortest_path(&self, start: usize, end: usize) -> Option<(u32, Vec<usize>)> {
        // TODO: Find shortest path from start to end
        // Returns Some((total_cost, path)) or None if no path exists
        // Use dijkstra() and reconstruct path from predecessors
        todo!()
    }

    pub fn has_path(&self, start: usize, end: usize) -> bool {
        // TODO: Check if path exists from start to end
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_path() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(2, 3, 3);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(1));
        assert_eq!(distances[2], Some(3));
        assert_eq!(distances[3], Some(6));
    }

    #[test]
    fn test_multiple_paths() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 4);
        graph.add_edge(0, 2, 1);
        graph.add_edge(2, 1, 2);
        graph.add_edge(1, 3, 1);
        graph.add_edge(2, 3, 5);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(3)); // via 2
        assert_eq!(distances[2], Some(1));
        assert_eq!(distances[3], Some(4)); // via 2->1->3
    }

    #[test]
    fn test_unreachable_node() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);
        // Node 3 and 4 are disconnected

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(1));
        assert_eq!(distances[2], Some(2));
        assert_eq!(distances[3], None);
        assert_eq!(distances[4], None);
    }

    #[test]
    fn test_shortest_path_reconstruction() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(0, 2, 5);
        graph.add_edge(2, 3, 1);

        let result = graph.shortest_path(0, 3);
        assert!(result.is_some());
        let (cost, path) = result.unwrap();
        assert_eq!(cost, 4); // 0->1->2->3
        assert_eq!(path, vec![0, 1, 2, 3]);
    }

    #[test]
    fn test_no_path() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        // No path from 0 to 2

        assert!(graph.shortest_path(0, 2).is_none());
        assert!(!graph.has_path(0, 2));
    }

    #[test]
    fn test_undirected_graph() {
        let mut graph = Graph::new(4);
        graph.add_undirected_edge(0, 1, 2);
        graph.add_undirected_edge(1, 2, 3);
        graph.add_undirected_edge(2, 3, 1);
        graph.add_undirected_edge(0, 3, 10);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[3], Some(6)); // 0->1->2->3, not 0->3
    }

    #[test]
    fn test_self_loop() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 5);
        graph.add_edge(1, 1, 2); // self loop
        graph.add_edge(1, 2, 3);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[1], Some(5));
        assert_eq!(distances[2], Some(8));
    }

    #[test]
    fn test_zero_weight_edges() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 0);
        graph.add_edge(1, 2, 0);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(0));
        assert_eq!(distances[2], Some(0));
    }

    #[test]
    fn test_has_path() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);

        assert!(graph.has_path(0, 0));
        assert!(graph.has_path(0, 1));
        assert!(graph.has_path(0, 2));
        assert!(!graph.has_path(0, 3));
    }

    #[test]
    fn test_large_graph() {
        let mut graph = Graph::new(100);
        for i in 0..99 {
            graph.add_edge(i, i + 1, 1);
        }

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[50], Some(50));
        assert_eq!(distances[99], Some(99));
    }

    #[test]
    fn test_complex_graph() {
        let mut graph = Graph::new(6);
        graph.add_edge(0, 1, 4);
        graph.add_edge(0, 2, 2);
        graph.add_edge(1, 2, 1);
        graph.add_edge(1, 3, 5);
        graph.add_edge(2, 3, 8);
        graph.add_edge(2, 4, 10);
        graph.add_edge(3, 4, 2);
        graph.add_edge(3, 5, 6);
        graph.add_edge(4, 5, 3);

        let (distances, _) = graph.dijkstra(0);
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(3)); // 0->2->1
        assert_eq!(distances[2], Some(2));
        assert_eq!(distances[3], Some(8)); // 0->2->1->3
        assert_eq!(distances[4], Some(10)); // 0->2->1->3->4
        assert_eq!(distances[5], Some(13)); // 0->2->1->3->4->5
    }
}
