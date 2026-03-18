// graph03_floyd_warshall.rs
//
// Floyd-Warshall All-Pairs Shortest Paths Algorithm
//
// Floyd-Warshall computes shortest paths between ALL pairs of vertices in a weighted
// directed graph. It works with negative edge weights but not negative cycles.
// The algorithm uses dynamic programming with a 3D approach.
//
// Time Complexity: O(V³) where V = number of vertices
// Space Complexity: O(V²) for distance matrix
//
// Key concepts:
// - Dynamic programming: dist[i][j][k] = shortest path from i to j using vertices 0..k
// - Can be optimized to 2D array by reusing the distance matrix
// - Computes all-pairs shortest paths in one pass
// - Can detect negative cycles by checking diagonal
//
// Your task: Implement Floyd-Warshall algorithm with path reconstruction.

// I AM NOT DONE

pub struct Graph {
    dist: Vec<Vec<Option<i32>>>,
    next: Vec<Vec<Option<usize>>>,
    num_vertices: usize,
}

impl Graph {
    pub fn new(num_vertices: usize) -> Self {
        // TODO: Initialize distance matrix with None (infinity)
        // Initialize next matrix for path reconstruction
        // Set dist[i][i] = Some(0) for all i
        todo!()
    }

    pub fn add_edge(&mut self, from: usize, to: usize, weight: i32) {
        // TODO: Add edge to distance matrix
        // Set dist[from][to] = Some(weight)
        // Set next[from][to] = Some(to) for path reconstruction
        todo!()
    }

    pub fn floyd_warshall(&mut self) -> Result<(), String> {
        // TODO: Implement Floyd-Warshall algorithm
        // For each intermediate vertex k:
        //   For each pair of vertices (i, j):
        //     If path i->k->j is shorter than current i->j:
        //       Update dist[i][j] and next[i][j]
        //
        // After algorithm, check for negative cycles:
        //   If dist[i][i] < 0 for any i, return Err
        //
        // Return Ok(()) if no negative cycles
        todo!()
    }

    pub fn shortest_distance(&self, from: usize, to: usize) -> Option<i32> {
        // TODO: Return shortest distance from 'from' to 'to'
        // Must call floyd_warshall() first
        todo!()
    }

    pub fn shortest_path(&self, from: usize, to: usize) -> Option<Vec<usize>> {
        // TODO: Reconstruct shortest path from 'from' to 'to'
        // Use the 'next' matrix to trace the path
        // Return None if no path exists
        todo!()
    }

    pub fn has_negative_cycle(&self) -> bool {
        // TODO: Check if graph contains negative cycle
        // After running floyd_warshall(), check if any dist[i][i] < 0
        todo!()
    }

    pub fn get_distance_matrix(&self) -> &Vec<Vec<Option<i32>>> {
        &self.dist
    }

    pub fn transitive_closure(&mut self) -> Vec<Vec<bool>> {
        // TODO: Compute transitive closure (reachability matrix)
        // Similar to Floyd-Warshall but with boolean values
        // reach[i][j] = true if there exists a path from i to j
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_graph() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 3);
        graph.add_edge(1, 2, 1);
        graph.add_edge(2, 3, 2);
        graph.add_edge(0, 3, 10);

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_distance(0, 3), Some(6)); // 0->1->2->3
        assert_eq!(graph.shortest_distance(0, 1), Some(3));
        assert_eq!(graph.shortest_distance(1, 3), Some(3));
    }

    #[test]
    fn test_all_pairs_distances() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 4);
        graph.add_edge(1, 2, 3);
        graph.add_edge(0, 2, 8);
        graph.add_edge(2, 0, 2);

        assert!(graph.floyd_warshall().is_ok());

        // Check all pairs
        assert_eq!(graph.shortest_distance(0, 0), Some(0));
        assert_eq!(graph.shortest_distance(0, 1), Some(4));
        assert_eq!(graph.shortest_distance(0, 2), Some(7));
        assert_eq!(graph.shortest_distance(1, 0), Some(5)); // 1->2->0
        assert_eq!(graph.shortest_distance(1, 1), Some(0));
        assert_eq!(graph.shortest_distance(1, 2), Some(3));
        assert_eq!(graph.shortest_distance(2, 0), Some(2));
        assert_eq!(graph.shortest_distance(2, 1), Some(6)); // 2->0->1
        assert_eq!(graph.shortest_distance(2, 2), Some(0));
    }

    #[test]
    fn test_negative_weights() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 4);
        graph.add_edge(1, 2, -2);
        graph.add_edge(0, 2, 3);

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_distance(0, 2), Some(2)); // 0->1->2
    }

    #[test]
    fn test_negative_cycle_detection() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, -3);
        graph.add_edge(2, 0, 1); // cycle with total weight -1

        let result = graph.floyd_warshall();
        assert!(result.is_err());
    }

    #[test]
    fn test_unreachable_vertices() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);
        // Vertex 3 is unreachable from others

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_distance(0, 2), Some(2));
        assert_eq!(graph.shortest_distance(0, 3), None);
        assert_eq!(graph.shortest_distance(3, 0), None);
    }

    #[test]
    fn test_path_reconstruction() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(2, 3, 3);
        graph.add_edge(0, 2, 10);

        assert!(graph.floyd_warshall().is_ok());

        let path = graph.shortest_path(0, 3);
        assert!(path.is_some());
        assert_eq!(path.unwrap(), vec![0, 1, 2, 3]);
    }

    #[test]
    fn test_no_path() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        // No path from 0 to 2

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_path(0, 2), None);
    }

    #[test]
    fn test_self_loops() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 5);
        graph.add_edge(1, 1, 2); // positive self-loop
        graph.add_edge(1, 2, 3);

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_distance(0, 2), Some(8));
    }

    #[test]
    fn test_transitive_closure() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 1);
        graph.add_edge(2, 3, 1);

        let closure = graph.transitive_closure();

        assert!(closure[0][0]); // Can reach self
        assert!(closure[0][1]);
        assert!(closure[0][2]);
        assert!(closure[0][3]);
        assert!(!closure[1][0]); // Cannot reach 0 from 1
        assert!(closure[1][2]);
        assert!(!closure[3][0]); // Cannot reach earlier nodes
    }

    #[test]
    fn test_complete_graph() {
        let mut graph = Graph::new(4);
        // Add edges between all pairs
        for i in 0..4 {
            for j in 0..4 {
                if i != j {
                    graph.add_edge(i, j, (i + j + 1) as i32);
                }
            }
        }

        assert!(graph.floyd_warshall().is_ok());

        // All vertices should be reachable
        for i in 0..4 {
            for j in 0..4 {
                if i != j {
                    assert!(graph.shortest_distance(i, j).is_some());
                }
            }
        }
    }

    #[test]
    fn test_zero_weight_edges() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 0);
        graph.add_edge(1, 2, 0);

        assert!(graph.floyd_warshall().is_ok());
        assert_eq!(graph.shortest_distance(0, 2), Some(0));
    }

    #[test]
    fn test_complex_graph() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1, 3);
        graph.add_edge(0, 2, 8);
        graph.add_edge(0, 4, -4);
        graph.add_edge(1, 3, 1);
        graph.add_edge(1, 4, 7);
        graph.add_edge(2, 1, 4);
        graph.add_edge(3, 0, 2);
        graph.add_edge(3, 2, -5);
        graph.add_edge(4, 3, 6);

        assert!(graph.floyd_warshall().is_ok());

        assert_eq!(graph.shortest_distance(0, 1), Some(1)); // 0->4->3->2->1
        assert_eq!(graph.shortest_distance(0, 2), Some(-3)); // 0->4->3->2
        assert_eq!(graph.shortest_distance(0, 3), Some(2)); // 0->4->3
        assert_eq!(graph.shortest_distance(0, 4), Some(-4));
    }
}
