// ds03_heap.rs
//
// A Binary Heap is a complete binary tree that satisfies the heap property.
// In a max-heap, for any given node, the node's value is greater than or equal to
// the values of its children. In a min-heap, the node's value is less than or equal
// to the values of its children.
//
// Binary heaps are commonly implemented using arrays where for a node at index i:
// - Left child is at index 2*i + 1
// - Right child is at index 2*i + 2
// - Parent is at index (i - 1) / 2
//
// Applications:
// - Priority queues
// - Heap sort algorithm
// - Finding k-th largest/smallest element
// - Median maintenance
//
// Time Complexity:
// - Insert (push): O(log n)
// - Extract min/max (pop): O(log n)
// - Peek min/max: O(1)
// - Heapify: O(n)
// - Space: O(n)
//
// Your task: Implement both MinHeap and MaxHeap with standard operations.

// I AM NOT DONE

use std::fmt::Debug;

#[derive(Debug, Clone)]
pub struct MinHeap<T: Ord + Clone + Debug> {
    data: Vec<T>,
}

impl<T: Ord + Clone + Debug> MinHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn from_vec(vec: Vec<T>) -> Self {
        // TODO: Build a heap from a vector using heapify
        // Hint: Start from the last non-leaf node and sift down
        todo!()
    }

    pub fn push(&mut self, value: T) {
        // TODO: Insert a new element and maintain heap property
        // 1. Add element to the end
        // 2. Bubble up (sift up) to maintain heap property
        todo!()
    }

    pub fn pop(&mut self) -> Option<T> {
        // TODO: Remove and return the minimum element
        // 1. If empty, return None
        // 2. Swap root with last element
        // 3. Remove last element (the old root)
        // 4. Sift down the new root to maintain heap property
        // 5. Return the old root
        todo!()
    }

    pub fn peek(&self) -> Option<&T> {
        // TODO: Return a reference to the minimum element without removing it
        todo!()
    }

    fn sift_up(&mut self, mut index: usize) {
        // TODO: Move element up until heap property is satisfied
        // Compare with parent and swap if needed
        todo!()
    }

    fn sift_down(&mut self, mut index: usize) {
        // TODO: Move element down until heap property is satisfied
        // Compare with children and swap with smaller child if needed
        todo!()
    }

    pub fn size(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    pub fn is_valid_heap(&self) -> bool {
        // TODO: Validate that the heap property is maintained
        // For each node, check that it's <= both children
        todo!()
    }
}

#[derive(Debug, Clone)]
pub struct MaxHeap<T: Ord + Clone + Debug> {
    data: Vec<T>,
}

impl<T: Ord + Clone + Debug> MaxHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn from_vec(vec: Vec<T>) -> Self {
        // TODO: Build a heap from a vector using heapify
        todo!()
    }

    pub fn push(&mut self, value: T) {
        // TODO: Insert a new element and maintain heap property
        todo!()
    }

    pub fn pop(&mut self) -> Option<T> {
        // TODO: Remove and return the maximum element
        todo!()
    }

    pub fn peek(&self) -> Option<&T> {
        // TODO: Return a reference to the maximum element
        todo!()
    }

    fn sift_up(&mut self, mut index: usize) {
        // TODO: Move element up until heap property is satisfied
        // Compare with parent and swap if needed (parent should be >= child)
        todo!()
    }

    fn sift_down(&mut self, mut index: usize) {
        // TODO: Move element down until heap property is satisfied
        // Compare with children and swap with larger child if needed
        todo!()
    }

    pub fn size(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    pub fn is_valid_heap(&self) -> bool {
        // TODO: Validate that the heap property is maintained
        // For each node, check that it's >= both children
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_minheap_create_empty() {
        let heap: MinHeap<i32> = MinHeap::new();
        assert!(heap.is_empty());
        assert_eq!(heap.size(), 0);
    }

    #[test]
    fn test_minheap_push_pop() {
        let mut heap = MinHeap::new();
        heap.push(5);
        heap.push(3);
        heap.push(7);
        heap.push(1);

        assert_eq!(heap.pop(), Some(1));
        assert_eq!(heap.pop(), Some(3));
        assert_eq!(heap.pop(), Some(5));
        assert_eq!(heap.pop(), Some(7));
        assert_eq!(heap.pop(), None);
    }

    #[test]
    fn test_minheap_peek() {
        let mut heap = MinHeap::new();
        heap.push(10);
        heap.push(5);
        heap.push(15);

        assert_eq!(heap.peek(), Some(&5));
        assert_eq!(heap.size(), 3); // Peek doesn't remove
    }

    #[test]
    fn test_minheap_from_vec() {
        let heap = MinHeap::from_vec(vec![5, 3, 7, 1, 9, 2]);
        assert!(heap.is_valid_heap());
        assert_eq!(heap.peek(), Some(&1));
    }

    #[test]
    fn test_minheap_maintains_property() {
        let mut heap = MinHeap::new();
        for i in [50, 30, 70, 20, 40, 60, 80] {
            heap.push(i);
            assert!(heap.is_valid_heap());
        }
    }

    #[test]
    fn test_maxheap_create_empty() {
        let heap: MaxHeap<i32> = MaxHeap::new();
        assert!(heap.is_empty());
        assert_eq!(heap.size(), 0);
    }

    #[test]
    fn test_maxheap_push_pop() {
        let mut heap = MaxHeap::new();
        heap.push(5);
        heap.push(3);
        heap.push(7);
        heap.push(1);

        assert_eq!(heap.pop(), Some(7));
        assert_eq!(heap.pop(), Some(5));
        assert_eq!(heap.pop(), Some(3));
        assert_eq!(heap.pop(), Some(1));
        assert_eq!(heap.pop(), None);
    }

    #[test]
    fn test_maxheap_peek() {
        let mut heap = MaxHeap::new();
        heap.push(10);
        heap.push(5);
        heap.push(15);

        assert_eq!(heap.peek(), Some(&15));
        assert_eq!(heap.size(), 3);
    }

    #[test]
    fn test_maxheap_from_vec() {
        let heap = MaxHeap::from_vec(vec![5, 3, 7, 1, 9, 2]);
        assert!(heap.is_valid_heap());
        assert_eq!(heap.peek(), Some(&9));
    }

    #[test]
    fn test_maxheap_maintains_property() {
        let mut heap = MaxHeap::new();
        for i in [50, 30, 70, 20, 40, 60, 80] {
            heap.push(i);
            assert!(heap.is_valid_heap());
        }
    }

    #[test]
    fn test_heap_sort_with_minheap() {
        let mut heap = MinHeap::from_vec(vec![5, 2, 8, 1, 9, 3]);
        let mut sorted = Vec::new();
        while let Some(val) = heap.pop() {
            sorted.push(val);
        }
        assert_eq!(sorted, vec![1, 2, 3, 5, 8, 9]);
    }

    #[test]
    fn test_heap_sort_with_maxheap() {
        let mut heap = MaxHeap::from_vec(vec![5, 2, 8, 1, 9, 3]);
        let mut sorted = Vec::new();
        while let Some(val) = heap.pop() {
            sorted.push(val);
        }
        assert_eq!(sorted, vec![9, 8, 5, 3, 2, 1]);
    }
}
