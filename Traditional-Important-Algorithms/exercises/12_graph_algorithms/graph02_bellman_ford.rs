// graph02_bellman_ford.rs
//
// Bellman-Ford Shortest Path Algorithm
//
// Bellman-Ford finds shortest paths from a source vertex to all other vertices,
// even when the graph contains negative edge weights. It can also detect negative
// weight cycles, which make shortest paths undefined.
//
// Time Complexity: O(V * E) where V = vertices, E = edges
// Space Complexity: O(V) for distance and predecessor arrays
//
// Key concepts:
// - Relaxation: Update distances by checking all edges repeatedly
// - V-1 iterations guarantee shortest paths if no negative cycles exist
// - Extra iteration detects negative cycles
// - Slower than Dijkstra but handles negative weights
//
// Your task: Implement Bellman-Ford algorithm with negative cycle detection.

// I AM NOT DONE

#[derive(Debug, Clone)]
pub struct Edge {
    pub from: usize,
    pub to: usize,
    pub weight: i32,
}

pub struct Graph {
    edges: Vec<Edge>,
    num_vertices: usize,
}

impl Graph {
    pub fn new(num_vertices: usize) -> Self {
        Self {
            edges: Vec::new(),
            num_vertices,
        }
    }

    pub fn add_edge(&mut self, from: usize, to: usize, weight: i32) {
        // TODO: Add a directed edge to the edge list
        todo!()
    }

    pub fn add_undirected_edge(&mut self, u: usize, v: usize, weight: i32) {
        // TODO: Add edges in both directions
        todo!()
    }

    pub fn bellman_ford(&self, start: usize) -> Result<(Vec<Option<i32>>, Vec<Option<usize>>), String> {
        // TODO: Implement Bellman-Ford algorithm
        // Returns Ok((distances, predecessors)) or Err("Negative cycle detected")
        //
        // Algorithm:
        // 1. Initialize distances to infinity (None), except start = 0
        // 2. Repeat V-1 times:
        //    a. For each edge (u, v) with weight w:
        //       - If dist[u] + w < dist[v], update dist[v] and pred[v]
        // 3. Check for negative cycles:
        //    a. For each edge (u, v) with weight w:
        //       - If dist[u] + w < dist[v], negative cycle exists
        // 4. Return distances and predecessors
        todo!()
    }

    pub fn shortest_path(&self, start: usize, end: usize) -> Result<Option<(i32, Vec<usize>)>, String> {
        // TODO: Find shortest path from start to end
        // Returns:
        // - Ok(Some((cost, path))) if path exists
        // - Ok(None) if no path exists
        // - Err("Negative cycle detected") if negative cycle exists
        todo!()
    }

    pub fn has_negative_cycle(&self) -> bool {
        // TODO: Detect if graph contains negative cycle
        // Run Bellman-Ford from vertex 0 and check result
        todo!()
    }

    pub fn find_negative_cycle(&self) -> Option<Vec<usize>> {
        // TODO: Find and return a negative cycle if one exists
        // 1. Run modified Bellman-Ford to detect cycle
        // 2. Track predecessors
        // 3. Reconstruct cycle from predecessors
        // 4. Return Some(cycle) or None
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

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(1));
        assert_eq!(distances[2], Some(3));
        assert_eq!(distances[3], Some(6));
    }

    #[test]
    fn test_negative_weights() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 4);
        graph.add_edge(0, 2, 5);
        graph.add_edge(1, 2, -3); // negative weight
        graph.add_edge(2, 3, 2);

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(4));
        assert_eq!(distances[2], Some(1)); // through 1 with negative edge
        assert_eq!(distances[3], Some(3));
    }

    #[test]
    fn test_negative_cycle_detection() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, -3);
        graph.add_edge(2, 0, 1); // cycle: 0->1->2->0 with total weight -1

        let result = graph.bellman_ford(0);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Negative cycle detected");
    }

    #[test]
    fn test_no_negative_cycle() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, -1);
        graph.add_edge(2, 0, 2); // cycle with positive total weight

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
    }

    #[test]
    fn test_unreachable_nodes() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1, 2);
        graph.add_edge(1, 2, 3);
        // Nodes 3 and 4 are unreachable

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(2));
        assert_eq!(distances[2], Some(5));
        assert_eq!(distances[3], None);
        assert_eq!(distances[4], None);
    }

    #[test]
    fn test_shortest_path_with_negatives() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 5);
        graph.add_edge(0, 2, 2);
        graph.add_edge(2, 1, -3);
        graph.add_edge(1, 3, 1);

        let result = graph.shortest_path(0, 3);
        assert!(result.is_ok());
        let path_result = result.unwrap();
        assert!(path_result.is_some());
        let (cost, path) = path_result.unwrap();
        assert_eq!(cost, 0); // 0->2->1->3: 2+(-3)+1 = 0
        assert_eq!(path, vec![0, 2, 1, 3]);
    }

    #[test]
    fn test_zero_weight_edges() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 0);
        graph.add_edge(1, 2, 0);

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(0));
        assert_eq!(distances[2], Some(0));
    }

    #[test]
    fn test_has_negative_cycle() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, -2);
        graph.add_edge(2, 0, -1);

        assert!(graph.has_negative_cycle());
    }

    #[test]
    fn test_find_negative_cycle() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, -3);
        graph.add_edge(2, 0, 1);

        let cycle = graph.find_negative_cycle();
        assert!(cycle.is_some());
        let cycle_nodes = cycle.unwrap();
        assert!(cycle_nodes.len() >= 2);
        // Verify it's actually a cycle
        assert_eq!(cycle_nodes.first(), cycle_nodes.last());
    }

    #[test]
    fn test_undirected_negative_edge() {
        let mut graph = Graph::new(2);
        graph.add_undirected_edge(0, 1, -1);

        // Undirected negative edge creates negative cycle
        assert!(graph.has_negative_cycle());
    }

    #[test]
    fn test_large_graph() {
        let mut graph = Graph::new(100);
        for i in 0..99 {
            graph.add_edge(i, i + 1, 1);
        }

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[50], Some(50));
        assert_eq!(distances[99], Some(99));
    }

    #[test]
    fn test_complex_negative_weights() {
        let mut graph = Graph::new(5);
        graph.add_edge(0, 1, 6);
        graph.add_edge(0, 2, 7);
        graph.add_edge(1, 2, 8);
        graph.add_edge(1, 3, -4);
        graph.add_edge(1, 4, 5);
        graph.add_edge(2, 3, 9);
        graph.add_edge(2, 4, -3);
        graph.add_edge(3, 4, 7);
        graph.add_edge(3, 0, 2);

        let result = graph.bellman_ford(0);
        assert!(result.is_ok());
        let (distances, _) = result.unwrap();
        assert_eq!(distances[0], Some(0));
        assert_eq!(distances[1], Some(6));
        assert_eq!(distances[2], Some(7));
        assert_eq!(distances[3], Some(2));
        assert_eq!(distances[4], Some(4));
    }
}
