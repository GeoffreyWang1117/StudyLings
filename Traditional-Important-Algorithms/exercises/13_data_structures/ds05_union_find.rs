// ds05_union_find.rs
//
// Union-Find (also called Disjoint Set Union or DSU) is a data structure that keeps track
// of elements partitioned into disjoint (non-overlapping) sets. It provides near-constant-time
// operations to add new sets, merge sets, and determine whether elements are in the same set.
//
// Key Operations:
// - MakeSet(x): Create a new set containing only element x
// - Find(x): Return the representative (root) of the set containing x
// - Union(x, y): Merge the sets containing x and y
//
// Optimizations:
// - Path Compression: During Find, make all nodes on path point directly to root
// - Union by Rank: Always attach smaller tree under root of larger tree
// - Union by Size: Attach tree with fewer nodes under tree with more nodes
//
// Applications:
// - Kruskal's minimum spanning tree algorithm
// - Detecting cycles in undirected graphs
// - Finding connected components
// - Image segmentation
// - Network connectivity
//
// Time Complexity (with both optimizations):
// - MakeSet: O(1)
// - Find: O(α(n)) amortized, where α is inverse Ackermann function (practically constant)
// - Union: O(α(n)) amortized
// - Space: O(n)
//
// Your task: Implement Union-Find with path compression and union by rank.

// I AM NOT DONE

#[derive(Debug, Clone)]
pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
    size: Vec<usize>,
    count: usize,  // Number of disjoint sets
}

impl UnionFind {
    pub fn new(n: usize) -> Self {
        // TODO: Initialize Union-Find for n elements (0 to n-1)
        // Initially, each element is in its own set
        // parent[i] = i (each element is its own parent)
        // rank[i] = 0 (all trees have height 0)
        // size[i] = 1 (each set has 1 element)
        // count = n (n separate sets)
        todo!()
    }

    pub fn find(&mut self, x: usize) -> usize {
        // TODO: Find the representative (root) of the set containing x
        // Implement path compression:
        // - Recursively find the root
        // - On the way back, make every node point directly to the root
        // This flattens the tree structure
        todo!()
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        // TODO: Merge the sets containing x and y
        // 1. Find roots of x and y
        // 2. If they're already in same set, return false
        // 3. Otherwise, implement union by rank:
        //    - Attach smaller rank tree under root of higher rank tree
        //    - If ranks are equal, pick one as new root and increment its rank
        // 4. Update sizes
        // 5. Decrement count of disjoint sets
        // 6. Return true
        todo!()
    }

    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        // TODO: Check if x and y are in the same set
        todo!()
    }

    pub fn count(&self) -> usize {
        // TODO: Return the number of disjoint sets
        self.count
    }

    pub fn get_size(&mut self, x: usize) -> usize {
        // TODO: Return the size of the set containing x
        // Find the root first, then return size[root]
        todo!()
    }

    pub fn get_rank(&mut self, x: usize) -> usize {
        // TODO: Return the rank of the set containing x
        // Find the root first, then return rank[root]
        todo!()
    }

    pub fn get_all_components(&mut self) -> Vec<Vec<usize>> {
        // TODO: Return all disjoint sets as a vector of vectors
        // Group elements by their root
        todo!()
    }
}

// Alternative implementation using union by size instead of rank
#[derive(Debug, Clone)]
pub struct UnionFindBySize {
    parent: Vec<usize>,
    size: Vec<usize>,
    count: usize,
}

impl UnionFindBySize {
    pub fn new(n: usize) -> Self {
        // TODO: Similar to UnionFind::new but using size-based approach
        todo!()
    }

    pub fn find(&mut self, x: usize) -> usize {
        // TODO: Same as UnionFind::find
        todo!()
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        // TODO: Union by size
        // Always attach smaller set under root of larger set
        todo!()
    }

    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        // TODO: Same as UnionFind::connected
        todo!()
    }

    pub fn count(&self) -> usize {
        self.count
    }

    pub fn get_size(&mut self, x: usize) -> usize {
        // TODO: Return the size of the set containing x
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state() {
        let uf = UnionFind::new(5);
        assert_eq!(uf.count(), 5);
    }

    #[test]
    fn test_find_initial() {
        let mut uf = UnionFind::new(5);
        for i in 0..5 {
            assert_eq!(uf.find(i), i);
        }
    }

    #[test]
    fn test_union_two_elements() {
        let mut uf = UnionFind::new(5);
        assert!(uf.union(0, 1));
        assert_eq!(uf.count(), 4);
        assert!(uf.connected(0, 1));
    }

    #[test]
    fn test_union_already_connected() {
        let mut uf = UnionFind::new(5);
        uf.union(0, 1);
        assert!(!uf.union(0, 1)); // Already connected
        assert_eq!(uf.count(), 4);
    }

    #[test]
    fn test_multiple_unions() {
        let mut uf = UnionFind::new(10);
        uf.union(0, 1);
        uf.union(2, 3);
        uf.union(4, 5);
        uf.union(0, 2); // Connect two components

        assert!(uf.connected(0, 3));
        assert!(uf.connected(1, 2));
        assert!(!uf.connected(0, 4));
        assert_eq!(uf.count(), 7); // {0,1,2,3}, {4,5}, {6}, {7}, {8}, {9}
    }

    #[test]
    fn test_path_compression() {
        let mut uf = UnionFind::new(5);
        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(2, 3);

        // After path compression, all should point to same root
        let root = uf.find(3);
        assert_eq!(uf.find(0), root);
        assert_eq!(uf.find(1), root);
        assert_eq!(uf.find(2), root);
    }

    #[test]
    fn test_get_size() {
        let mut uf = UnionFind::new(10);
        uf.union(0, 1);
        uf.union(2, 3);
        uf.union(0, 2);

        assert_eq!(uf.get_size(0), 4);
        assert_eq!(uf.get_size(1), 4);
        assert_eq!(uf.get_size(2), 4);
        assert_eq!(uf.get_size(3), 4);
        assert_eq!(uf.get_size(4), 1);
    }

    #[test]
    fn test_connected_components() {
        let mut uf = UnionFind::new(6);
        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(3, 4);

        let components = uf.get_all_components();
        assert_eq!(components.len(), 3); // {0,1,2}, {3,4}, {5}

        // Find the component with 3 elements
        let has_size_3 = components.iter().any(|c| c.len() == 3);
        assert!(has_size_3);
    }

    #[test]
    fn test_cycle_detection() {
        // Use Union-Find to detect cycles in an undirected graph
        let mut uf = UnionFind::new(4);

        // Edges: (0,1), (1,2), (2,3)
        assert!(uf.union(0, 1));
        assert!(uf.union(1, 2));
        assert!(uf.union(2, 3));

        // Edge (0,3) would create a cycle
        assert!(!uf.union(0, 3));
    }

    #[test]
    fn test_union_by_size() {
        let mut uf = UnionFindBySize::new(10);
        uf.union(0, 1);
        uf.union(2, 3);
        uf.union(4, 5);

        assert!(uf.connected(0, 1));
        assert!(uf.connected(2, 3));
        assert!(!uf.connected(0, 2));

        uf.union(0, 2);
        assert!(uf.connected(0, 3));
        assert_eq!(uf.count(), 7);
    }

    #[test]
    fn test_large_dataset() {
        let mut uf = UnionFind::new(1000);

        // Create chains
        for i in 0..999 {
            uf.union(i, i + 1);
        }

        assert_eq!(uf.count(), 1);
        assert!(uf.connected(0, 999));
        assert_eq!(uf.get_size(0), 1000);
    }

    #[test]
    fn test_union_all_to_one() {
        let mut uf = UnionFind::new(100);

        // Union all elements to element 0
        for i in 1..100 {
            uf.union(0, i);
        }

        assert_eq!(uf.count(), 1);
        for i in 0..100 {
            assert!(uf.connected(0, i));
        }
    }
}
