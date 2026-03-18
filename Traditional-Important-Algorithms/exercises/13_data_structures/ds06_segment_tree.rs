// ds06_segment_tree.rs
//
// A Segment Tree is a tree data structure used for storing intervals or segments.
// It allows querying which segments contain a given point efficiently. It's particularly
// useful for range queries and updates on arrays.
//
// Structure:
// - Binary tree where each node represents an interval
// - Leaf nodes represent single elements
// - Internal nodes represent the union of their children's intervals
// - Each node stores aggregate information about its interval (sum, min, max, etc.)
//
// Applications:
// - Range sum queries with updates
// - Range minimum/maximum queries
// - Finding k-th smallest element in a range
// - Counting elements in a range
//
// Time Complexity:
// - Build: O(n)
// - Query (range): O(log n)
// - Update (point): O(log n)
// - Update (range): O(log n) with lazy propagation
// - Space: O(n)
//
// Your task: Implement a Segment Tree supporting range sum queries and point updates.

// I AM NOT DONE

use std::fmt::Debug;
use std::ops::Add;

#[derive(Debug, Clone)]
pub struct SegmentTree<T: Copy + Add<Output = T> + Default + Debug> {
    tree: Vec<T>,
    size: usize,
}

impl<T: Copy + Add<Output = T> + Default + Debug> SegmentTree<T> {
    pub fn new(data: &[T]) -> Self {
        // TODO: Build segment tree from array
        // 1. Determine tree size (4 * n is safe upper bound)
        // 2. Build tree recursively from bottom up
        // 3. Each node stores the sum of its range
        todo!()
    }

    fn build(&mut self, data: &[T], node: usize, start: usize, end: usize) {
        // TODO: Recursive helper to build tree
        // Base case: if start == end, we're at a leaf
        //   tree[node] = data[start]
        // Recursive case:
        //   mid = (start + end) / 2
        //   build left child (2*node+1) for [start, mid]
        //   build right child (2*node+2) for [mid+1, end]
        //   tree[node] = tree[left_child] + tree[right_child]
        todo!()
    }

    pub fn query(&self, left: usize, right: usize) -> T {
        // TODO: Query the sum of range [left, right] (inclusive)
        todo!()
    }

    fn query_recursive(&self, node: usize, start: usize, end: usize, left: usize, right: usize) -> T {
        // TODO: Recursive helper for range query
        // If query range [left, right] completely covers [start, end]:
        //   return tree[node]
        // If no overlap:
        //   return default value (0 for sum)
        // Partial overlap:
        //   recursively query both children and combine results
        todo!()
    }

    pub fn update(&mut self, index: usize, value: T) {
        // TODO: Update value at index
        todo!()
    }

    fn update_recursive(&mut self, node: usize, start: usize, end: usize, index: usize, value: T) {
        // TODO: Recursive helper for point update
        // If start == end == index:
        //   tree[node] = value
        // Otherwise:
        //   recursively update appropriate child
        //   tree[node] = tree[left_child] + tree[right_child]
        todo!()
    }

    pub fn len(&self) -> usize {
        self.size
    }
}

// Segment tree with lazy propagation for range updates
#[derive(Debug, Clone)]
pub struct LazySegmentTree {
    tree: Vec<i64>,
    lazy: Vec<i64>,  // Lazy propagation array
    size: usize,
}

impl LazySegmentTree {
    pub fn new(data: &[i64]) -> Self {
        // TODO: Build segment tree with lazy propagation
        todo!()
    }

    fn build(&mut self, data: &[i64], node: usize, start: usize, end: usize) {
        // TODO: Similar to regular segment tree build
        todo!()
    }

    pub fn range_update(&mut self, left: usize, right: usize, value: i64) {
        // TODO: Add value to all elements in range [left, right]
        // Use lazy propagation to defer updates
        todo!()
    }

    fn range_update_recursive(&mut self, node: usize, start: usize, end: usize,
                               left: usize, right: usize, value: i64) {
        // TODO: Recursive helper for range update with lazy propagation
        // 1. Push down any pending updates for this node
        // 2. If no overlap, return
        // 3. If complete overlap, update this node and mark children as lazy
        // 4. If partial overlap, recurse on children
        todo!()
    }

    fn push(&mut self, node: usize, start: usize, end: usize) {
        // TODO: Push down lazy values to children
        // If lazy[node] != 0:
        //   Apply lazy value to this node
        //   Propagate lazy value to children
        //   Reset lazy[node] to 0
        todo!()
    }

    pub fn query(&mut self, left: usize, right: usize) -> i64 {
        // TODO: Query range sum with lazy propagation
        todo!()
    }

    fn query_recursive(&mut self, node: usize, start: usize, end: usize,
                       left: usize, right: usize) -> i64 {
        // TODO: Recursive helper for range query
        // Push down pending updates before querying
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_build_segment_tree() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let st = SegmentTree::new(&data);
        assert_eq!(st.len(), 6);
    }

    #[test]
    fn test_query_full_range() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let st = SegmentTree::new(&data);
        assert_eq!(st.query(0, 5), 36); // Sum of all elements
    }

    #[test]
    fn test_query_subrange() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let st = SegmentTree::new(&data);
        assert_eq!(st.query(1, 3), 15); // 3 + 5 + 7
        assert_eq!(st.query(2, 4), 21); // 5 + 7 + 9
    }

    #[test]
    fn test_query_single_element() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let st = SegmentTree::new(&data);
        assert_eq!(st.query(2, 2), 5);
        assert_eq!(st.query(4, 4), 9);
    }

    #[test]
    fn test_point_update() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let mut st = SegmentTree::new(&data);

        st.update(2, 10); // Change 5 to 10
        assert_eq!(st.query(0, 5), 41); // 1+3+10+7+9+11
        assert_eq!(st.query(2, 2), 10);
    }

    #[test]
    fn test_multiple_updates() {
        let data = vec![1, 2, 3, 4, 5];
        let mut st = SegmentTree::new(&data);

        st.update(0, 10);
        st.update(4, 50);
        assert_eq!(st.query(0, 4), 69); // 10+2+3+4+50
    }

    #[test]
    fn test_query_after_updates() {
        let data = vec![1, 3, 5, 7, 9];
        let mut st = SegmentTree::new(&data);

        assert_eq!(st.query(1, 3), 15);
        st.update(2, 0); // Change 5 to 0
        assert_eq!(st.query(1, 3), 10); // 3 + 0 + 7
    }

    #[test]
    fn test_lazy_segment_tree_build() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let st = LazySegmentTree::new(&data);
        assert_eq!(st.size, 6);
    }

    #[test]
    fn test_lazy_range_update() {
        let data = vec![1, 2, 3, 4, 5];
        let mut st = LazySegmentTree::new(&data);

        st.range_update(1, 3, 10); // Add 10 to indices 1,2,3
        assert_eq!(st.query(0, 4), 45); // 1+(2+10)+(3+10)+(4+10)+5
    }

    #[test]
    fn test_lazy_multiple_range_updates() {
        let data = vec![0, 0, 0, 0, 0];
        let mut st = LazySegmentTree::new(&data);

        st.range_update(0, 2, 5);
        st.range_update(2, 4, 3);

        assert_eq!(st.query(0, 0), 5);
        assert_eq!(st.query(2, 2), 8); // 5 + 3
        assert_eq!(st.query(4, 4), 3);
    }

    #[test]
    fn test_lazy_query_after_updates() {
        let data = vec![1, 3, 5, 7, 9];
        let mut st = LazySegmentTree::new(&data);

        st.range_update(1, 3, 2);
        assert_eq!(st.query(1, 3), 21); // (3+2)+(5+2)+(7+2)
        assert_eq!(st.query(0, 4), 31); // 1+(3+2)+(5+2)+(7+2)+9
    }

    #[test]
    fn test_large_dataset() {
        let data: Vec<i32> = (1..=100).collect();
        let mut st = SegmentTree::new(&data);

        // Sum of 1..=100 is 5050
        assert_eq!(st.query(0, 99), 5050);

        // Update some values
        st.update(0, 100);
        st.update(99, 1);
        assert_eq!(st.query(0, 99), 5050); // Sum stays the same
    }
}
