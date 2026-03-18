// ds07_fenwick_tree.rs
//
// A Fenwick Tree (also called Binary Indexed Tree or BIT) is a data structure that can
// efficiently update elements and calculate prefix sums in O(log n) time. It was proposed
// by Peter Fenwick in 1994.
//
// Key Insight:
// - Uses binary representation of indices to organize data
// - Each index is responsible for a range of elements based on its lowest set bit
// - Index i is responsible for range [i - (i & -i) + 1, i]
//
// Binary Index Trick:
// - i & -i gives the lowest set bit (LSB) of i
// - Parent of i is i - (i & -i)
// - Next index is i + (i & -i)
//
// Comparison with Segment Tree:
// - Fenwick Tree uses less memory (O(n) vs O(4n))
// - Fenwick Tree has simpler implementation
// - Segment Tree is more versatile (can handle more complex operations)
// - Both have O(log n) query and update
//
// Applications:
// - Cumulative frequency tables
// - Range sum queries
// - Counting inversions in an array
// - Dynamic ranking
//
// Time Complexity:
// - Build: O(n log n) or O(n) with optimization
// - Prefix sum query: O(log n)
// - Range sum query: O(log n)
// - Point update: O(log n)
// - Space: O(n)
//
// Your task: Implement a Fenwick Tree with prefix/range sum queries and point updates.

// I AM NOT DONE

use std::fmt::Debug;
use std::ops::{Add, Sub};

#[derive(Debug, Clone)]
pub struct FenwickTree<T: Copy + Add<Output = T> + Sub<Output = T> + Default + Debug> {
    tree: Vec<T>,
    size: usize,
}

impl<T: Copy + Add<Output = T> + Sub<Output = T> + Default + Debug> FenwickTree<T> {
    pub fn new(size: usize) -> Self {
        // TODO: Create a Fenwick tree of given size
        // Initialize with default values
        // Note: tree is 1-indexed, so allocate size+1 elements
        todo!()
    }

    pub fn from_vec(data: &[T]) -> Self {
        // TODO: Build Fenwick tree from an array
        // Can use naive approach: create empty tree and update each element
        // Or optimized approach: build in O(n)
        todo!()
    }

    fn lowbit(&self, i: usize) -> usize {
        // TODO: Calculate i & -i (lowest set bit)
        // This gives the size of the range that index i is responsible for
        // Hint: In Rust, use i & (i.wrapping_neg())
        todo!()
    }

    pub fn prefix_sum(&self, mut index: usize) -> T {
        // TODO: Calculate prefix sum from index 0 to index (inclusive)
        // Start with sum = 0
        // While index > 0:
        //   sum += tree[index]
        //   index -= lowbit(index)
        todo!()
    }

    pub fn range_sum(&self, left: usize, right: usize) -> T {
        // TODO: Calculate sum of range [left, right] (inclusive)
        // Use prefix sums: sum(left, right) = sum(0, right) - sum(0, left-1)
        todo!()
    }

    pub fn update(&mut self, mut index: usize, delta: T) {
        // TODO: Add delta to the element at index
        // While index <= size:
        //   tree[index] += delta
        //   index += lowbit(index)
        todo!()
    }

    pub fn set(&mut self, index: usize, value: T) {
        // TODO: Set element at index to value
        // First calculate current value using range_sum
        // Then update with the difference
        todo!()
    }

    pub fn get(&self, index: usize) -> T {
        // TODO: Get value at index
        // Use range_sum(index, index)
        todo!()
    }

    pub fn len(&self) -> usize {
        self.size
    }
}

// 2D Fenwick Tree for matrix range sum queries
#[derive(Debug, Clone)]
pub struct FenwickTree2D {
    tree: Vec<Vec<i64>>,
    rows: usize,
    cols: usize,
}

impl FenwickTree2D {
    pub fn new(rows: usize, cols: usize) -> Self {
        // TODO: Create 2D Fenwick tree
        // Both dimensions are 1-indexed
        todo!()
    }

    fn lowbit(&self, i: usize) -> usize {
        // TODO: Same as 1D version
        todo!()
    }

    pub fn update(&mut self, mut row: usize, mut col: usize, delta: i64) {
        // TODO: Add delta to element at (row, col)
        // Nested loop: iterate through row indices, for each row iterate through col indices
        todo!()
    }

    pub fn prefix_sum(&self, mut row: usize, mut col: usize) -> i64 {
        // TODO: Get sum of rectangle from (0,0) to (row, col)
        // Nested loop similar to update but subtracting lowbit
        todo!()
    }

    pub fn range_sum(&self, row1: usize, col1: usize, row2: usize, col2: usize) -> i64 {
        // TODO: Get sum of rectangle from (row1, col1) to (row2, col2)
        // Use inclusion-exclusion principle:
        // sum = prefix(row2,col2) - prefix(row1-1,col2) - prefix(row2,col1-1) + prefix(row1-1,col1-1)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_fenwick_tree() {
        let ft: FenwickTree<i32> = FenwickTree::new(10);
        assert_eq!(ft.len(), 10);
    }

    #[test]
    fn test_build_from_array() {
        let data = vec![1, 3, 5, 7, 9, 11];
        let ft = FenwickTree::from_vec(&data);
        assert_eq!(ft.len(), 6);
    }

    #[test]
    fn test_prefix_sum() {
        let data = vec![1, 2, 3, 4, 5];
        let ft = FenwickTree::from_vec(&data);

        assert_eq!(ft.prefix_sum(0), 1);   // sum of [1]
        assert_eq!(ft.prefix_sum(2), 6);   // sum of [1,2,3]
        assert_eq!(ft.prefix_sum(4), 15);  // sum of [1,2,3,4,5]
    }

    #[test]
    fn test_range_sum() {
        let data = vec![1, 2, 3, 4, 5];
        let ft = FenwickTree::from_vec(&data);

        assert_eq!(ft.range_sum(1, 3), 9);  // 2+3+4
        assert_eq!(ft.range_sum(0, 2), 6);  // 1+2+3
        assert_eq!(ft.range_sum(2, 4), 12); // 3+4+5
    }

    #[test]
    fn test_point_update() {
        let data = vec![1, 2, 3, 4, 5];
        let mut ft = FenwickTree::from_vec(&data);

        ft.update(2, 7); // Add 7 to index 2 (3 becomes 10)
        assert_eq!(ft.range_sum(0, 4), 22); // 1+2+10+4+5
        assert_eq!(ft.range_sum(2, 2), 10); // Just the updated element
    }

    #[test]
    fn test_set_value() {
        let data = vec![1, 2, 3, 4, 5];
        let mut ft = FenwickTree::from_vec(&data);

        ft.set(2, 10); // Set index 2 to 10
        assert_eq!(ft.get(2), 10);
        assert_eq!(ft.range_sum(0, 4), 22); // 1+2+10+4+5
    }

    #[test]
    fn test_multiple_updates() {
        let mut ft: FenwickTree<i32> = FenwickTree::new(5);

        ft.update(0, 1);
        ft.update(1, 2);
        ft.update(2, 3);
        ft.update(3, 4);
        ft.update(4, 5);

        assert_eq!(ft.prefix_sum(4), 15);
    }

    #[test]
    fn test_get_individual_elements() {
        let data = vec![10, 20, 30, 40, 50];
        let ft = FenwickTree::from_vec(&data);

        assert_eq!(ft.get(0), 10);
        assert_eq!(ft.get(2), 30);
        assert_eq!(ft.get(4), 50);
    }

    #[test]
    fn test_lowbit_calculation() {
        let ft: FenwickTree<i32> = FenwickTree::new(10);

        assert_eq!(ft.lowbit(1), 1);  // binary: 1
        assert_eq!(ft.lowbit(2), 2);  // binary: 10
        assert_eq!(ft.lowbit(4), 4);  // binary: 100
        assert_eq!(ft.lowbit(6), 2);  // binary: 110 -> LSB is 10
    }

    #[test]
    fn test_2d_fenwick_tree_update() {
        let mut ft = FenwickTree2D::new(5, 5);

        ft.update(0, 0, 1);
        ft.update(1, 1, 2);
        ft.update(2, 2, 3);

        assert_eq!(ft.prefix_sum(2, 2), 6); // 1+2+3
    }

    #[test]
    fn test_2d_range_sum() {
        let mut ft = FenwickTree2D::new(5, 5);

        // Create a 3x3 matrix with all 1s
        for i in 0..3 {
            for j in 0..3 {
                ft.update(i, j, 1);
            }
        }

        assert_eq!(ft.range_sum(0, 0, 2, 2), 9); // 3x3 = 9
        assert_eq!(ft.range_sum(1, 1, 2, 2), 4); // 2x2 = 4
    }

    #[test]
    fn test_large_dataset() {
        let data: Vec<i32> = (1..=1000).collect();
        let mut ft = FenwickTree::from_vec(&data);

        // Sum of 1..=1000 is 500500
        assert_eq!(ft.prefix_sum(999), 500500);

        // Update some values
        ft.update(0, 999);   // Add 999 to first element
        ft.update(999, -999); // Subtract 999 from last element
        assert_eq!(ft.prefix_sum(999), 500500); // Sum unchanged
    }
}
