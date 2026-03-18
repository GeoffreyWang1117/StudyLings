// graph04_kruskal.rs
//
// Kruskal's Minimum Spanning Tree Algorithm
//
// Kruskal's algorithm finds a minimum spanning tree for a connected weighted graph.
// It uses a greedy approach: sort all edges by weight and add them one by one,
// skipping edges that would create a cycle (using Union-Find data structure).
//
// Time Complexity: O(E log E) or O(E log V) for sorting edges
// Space Complexity: O(V) for Union-Find structure
//
// Key concepts:
// - Greedy algorithm: Always pick minimum weight edge that doesn't create cycle
// - Union-Find (Disjoint Set Union) for efficient cycle detection
// - Sort edges by weight first
// - Works on undirected graphs
//
// Your task: Implement Kruskal's MST algorithm with Union-Find.

// I AM NOT DONE

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Edge {
    pub u: usize,
    pub v: usize,
    pub weight: i32,
}

impl Ord for Edge {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.weight.cmp(&other.weight)
            .then_with(|| self.u.cmp(&other.u))
            .then_with(|| self.v.cmp(&other.v))
    }
}

impl PartialOrd for Edge {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl UnionFind {
    pub fn new(size: usize) -> Self {
        // TODO: Initialize Union-Find structure
        // parent[i] = i (each element is its own parent initially)
        // rank[i] = 0 (tree height)
        todo!()
    }

    pub fn find(&mut self, x: usize) -> usize {
        // TODO: Find root of element x with path compression
        // If parent[x] != x, recursively find root and compress path
        // Return root
        todo!()
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        // TODO: Union two sets containing x and y
        // Find roots of x and y
        // If same root, they're already in same set, return false
        // Otherwise, union by rank and return true
        // Attach smaller rank tree under root of higher rank tree
        todo!()
    }

    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        // TODO: Check if x and y are in the same set
        todo!()
    }
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

    pub fn add_edge(&mut self, u: usize, v: usize, weight: i32) {
        // TODO: Add undirected edge (store once, as Kruskal treats edges as undirected)
        todo!()
    }

    pub fn kruskal(&self) -> Option<(i32, Vec<Edge>)> {
        // TODO: Implement Kruskal's MST algorithm
        // Returns Some((total_weight, mst_edges)) or None if graph not connected
        //
        // Algorithm:
        // 1. Sort all edges by weight
        // 2. Initialize Union-Find with num_vertices
        // 3. Initialize empty MST edge list
        // 4. For each edge (u, v, w) in sorted order:
        //    a. If u and v not in same set (no cycle):
        //       - Add edge to MST
        //       - Union sets containing u and v
        // 5. If MST has V-1 edges, return Some((weight, edges))
        //    Otherwise, graph is not connected, return None
        todo!()
    }

    pub fn is_connected(&self) -> bool {
        // TODO: Check if graph is connected using Union-Find
        todo!()
    }

    pub fn mst_weight(&self) -> Option<i32> {
        // TODO: Return total weight of MST (without edges)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_union_find_basic() {
        let mut uf = UnionFind::new(5);
        assert!(!uf.connected(0, 1));

        uf.union(0, 1);
        assert!(uf.connected(0, 1));

        uf.union(2, 3);
        assert!(uf.connected(2, 3));
        assert!(!uf.connected(0, 2));

        uf.union(1, 3);
        assert!(uf.connected(0, 3));
    }

    #[test]
    fn test_simple_mst() {
        let mut graph = Graph::new(4);
        graph.add_edge(0, 1, 10);
        graph.add_edge(0, 2, 6);
        graph.add_edge(0, 3, 5);
        graph.add_edge(1, 3, 15);
        graph.add_edge(2, 3, 4);

        let result = graph.kruskal();
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

        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 6);
        assert_eq!(edges.len(), 3);
    }

    #[test]
    fn test_complete_graph() {
        let mut graph = Graph::new(4);
        // Complete graph K4
        graph.add_edge(0, 1, 1);
        graph.add_edge(0, 2, 2);
        graph.add_edge(0, 3, 3);
        graph.add_edge(1, 2, 4);
        graph.add_edge(1, 3, 5);
        graph.add_edge(2, 3, 6);

        let result = graph.kruskal();
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

        let result = graph.kruskal();
        assert!(result.is_none()); // No spanning tree for disconnected graph
    }

    #[test]
    fn test_single_vertex() {
        let graph = Graph::new(1);
        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 0);
        assert_eq!(edges.len(), 0);
    }

    #[test]
    fn test_two_vertices() {
        let mut graph = Graph::new(2);
        graph.add_edge(0, 1, 5);

        let result = graph.kruskal();
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

        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, _) = result.unwrap();
        assert_eq!(weight, 3); // Any 3 edges work
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

        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, _) = result.unwrap();
        assert_eq!(weight, -3); // MST works with negative weights too
    }

    #[test]
    fn test_cycle_avoidance() {
        let mut graph = Graph::new(3);
        graph.add_edge(0, 1, 1);
        graph.add_edge(1, 2, 2);
        graph.add_edge(0, 2, 10); // This creates a cycle, should be ignored

        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 3);
        assert_eq!(edges.len(), 2);
        // Edge (0,2) with weight 10 should not be in MST
        assert!(!edges.iter().any(|e|
            (e.u == 0 && e.v == 2 || e.u == 2 && e.v == 0) && e.weight == 10
        ));
    }

    #[test]
    fn test_large_graph() {
        let mut graph = Graph::new(100);
        // Create a path graph
        for i in 0..99 {
            graph.add_edge(i, i + 1, 1);
        }
        // Add some cross edges with higher weights
        graph.add_edge(0, 50, 100);
        graph.add_edge(25, 75, 100);

        let result = graph.kruskal();
        assert!(result.is_some());
        let (weight, edges) = result.unwrap();
        assert_eq!(weight, 99); // Only path edges should be selected
        assert_eq!(edges.len(), 99);
    }
}
