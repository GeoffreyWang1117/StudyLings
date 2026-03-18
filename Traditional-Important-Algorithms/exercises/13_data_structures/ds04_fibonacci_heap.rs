// ds04_fibonacci_heap.rs
//
// A Fibonacci Heap is an advanced data structure for priority queue operations.
// It supports very fast amortized running times for many operations. Fibonacci heaps
// are particularly useful in graph algorithms like Dijkstra's shortest path and
// Prim's minimum spanning tree.
//
// Structure:
// - Collection of heap-ordered trees (min-heap property)
// - Trees are not necessarily binary
// - Supports lazy consolidation: structure is cleaned up during extract-min
// - Uses marking to maintain balance
//
// Key Features:
// - Nodes can have any number of children
// - Maintains a pointer to the minimum element
// - Trees are combined lazily during extract-min
// - Decrease-key is very efficient due to lazy approach
//
// Time Complexity (amortized):
// - Insert: O(1)
// - Find-min: O(1)
// - Extract-min: O(log n)
// - Decrease-key: O(1)
// - Delete: O(log n)
// - Merge: O(1)
//
// Your task: Implement a simplified Fibonacci Heap with core operations.

// I AM NOT DONE

use std::collections::HashMap;
use std::fmt::Debug;

#[derive(Debug, Clone)]
pub struct FibNode<T: Ord + Clone + Debug> {
    value: T,
    degree: usize,               // Number of children
    marked: bool,                // Whether node has lost a child
    parent: Option<usize>,       // Parent node ID
    children: Vec<usize>,        // Child node IDs
}

impl<T: Ord + Clone + Debug> FibNode<T> {
    fn new(value: T) -> Self {
        Self {
            value,
            degree: 0,
            marked: false,
            parent: None,
            children: Vec::new(),
        }
    }
}

pub struct FibonacciHeap<T: Ord + Clone + Debug> {
    nodes: HashMap<usize, FibNode<T>>,
    roots: Vec<usize>,           // Root list
    min_node: Option<usize>,     // ID of minimum node
    next_id: usize,              // Next node ID to assign
    size: usize,
}

impl<T: Ord + Clone + Debug> FibonacciHeap<T> {
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
            roots: Vec::new(),
            min_node: None,
            next_id: 0,
            size: 0,
        }
    }

    pub fn insert(&mut self, value: T) -> usize {
        // TODO: Insert a new element
        // 1. Create a new node with unique ID
        // 2. Add it to the root list
        // 3. Update min_node if necessary
        // 4. Increment size
        // 5. Return the node ID (useful for decrease_key later)
        todo!()
    }

    pub fn find_min(&self) -> Option<&T> {
        // TODO: Return a reference to the minimum value
        // Simply look at min_node
        todo!()
    }

    pub fn extract_min(&mut self) -> Option<T> {
        // TODO: Remove and return the minimum element
        // 1. If empty, return None
        // 2. Remove min_node from roots
        // 3. Add all children of min_node to root list
        // 4. Consolidate trees of same degree
        // 5. Find new minimum
        // 6. Decrement size
        todo!()
    }

    fn consolidate(&mut self) {
        // TODO: Consolidate trees so no two roots have same degree
        // 1. Create array indexed by degree
        // 2. For each root, link with other roots of same degree
        // 3. Repeat until all roots have different degrees
        todo!()
    }

    fn link(&mut self, child_id: usize, parent_id: usize) {
        // TODO: Make child_id a child of parent_id
        // 1. Remove child from roots
        // 2. Add child to parent's children
        // 3. Increment parent's degree
        // 4. Unmark child
        todo!()
    }

    pub fn decrease_key(&mut self, node_id: usize, new_value: T) -> Result<(), String> {
        // TODO: Decrease the value of a node
        // 1. Verify new_value < current value
        // 2. Update the value
        // 3. If heap property violated (parent > child):
        //    a. Cut the node from parent and add to root list
        //    b. Perform cascading cut on parent
        // 4. Update min_node if necessary
        todo!()
    }

    fn cut(&mut self, node_id: usize) {
        // TODO: Cut node from its parent and add to root list
        // 1. Remove from parent's children list
        // 2. Update parent's degree
        // 3. Add to roots
        // 4. Clear parent reference
        // 5. Unmark the node
        todo!()
    }

    fn cascading_cut(&mut self, node_id: usize) {
        // TODO: Perform cascading cut
        // If node is marked and has parent:
        // 1. Cut the node
        // 2. Recursively cascading cut on parent
        // Otherwise, mark the node
        todo!()
    }

    pub fn merge(&mut self, other: FibonacciHeap<T>) {
        // TODO: Merge another Fibonacci heap into this one
        // 1. Add all nodes from other heap
        // 2. Concatenate root lists
        // 3. Update min_node
        // 4. Update size
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    pub fn num_roots(&self) -> usize {
        self.roots.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_heap() {
        let heap: FibonacciHeap<i32> = FibonacciHeap::new();
        assert!(heap.is_empty());
        assert_eq!(heap.size(), 0);
    }

    #[test]
    fn test_insert_single_element() {
        let mut heap = FibonacciHeap::new();
        heap.insert(10);
        assert_eq!(heap.size(), 1);
        assert_eq!(heap.find_min(), Some(&10));
    }

    #[test]
    fn test_insert_multiple_elements() {
        let mut heap = FibonacciHeap::new();
        heap.insert(5);
        heap.insert(3);
        heap.insert(7);
        heap.insert(1);

        assert_eq!(heap.size(), 4);
        assert_eq!(heap.find_min(), Some(&1));
    }

    #[test]
    fn test_extract_min() {
        let mut heap = FibonacciHeap::new();
        heap.insert(5);
        heap.insert(3);
        heap.insert(7);
        heap.insert(1);

        assert_eq!(heap.extract_min(), Some(1));
        assert_eq!(heap.extract_min(), Some(3));
        assert_eq!(heap.extract_min(), Some(5));
        assert_eq!(heap.extract_min(), Some(7));
        assert_eq!(heap.extract_min(), None);
    }

    #[test]
    fn test_find_min_no_removal() {
        let mut heap = FibonacciHeap::new();
        heap.insert(10);
        heap.insert(5);

        assert_eq!(heap.find_min(), Some(&5));
        assert_eq!(heap.size(), 2); // Size unchanged
    }

    #[test]
    fn test_decrease_key() {
        let mut heap = FibonacciHeap::new();
        let id1 = heap.insert(10);
        let id2 = heap.insert(20);
        let id3 = heap.insert(30);

        assert_eq!(heap.find_min(), Some(&10));

        // Decrease 20 to 5, should become new minimum
        assert!(heap.decrease_key(id2, 5).is_ok());
        assert_eq!(heap.find_min(), Some(&5));
    }

    #[test]
    fn test_decrease_key_invalid() {
        let mut heap = FibonacciHeap::new();
        let id = heap.insert(10);

        // Try to increase key (should fail)
        assert!(heap.decrease_key(id, 20).is_err());
    }

    #[test]
    fn test_merge_heaps() {
        let mut heap1 = FibonacciHeap::new();
        heap1.insert(5);
        heap1.insert(10);

        let mut heap2 = FibonacciHeap::new();
        heap2.insert(3);
        heap2.insert(8);

        heap1.merge(heap2);
        assert_eq!(heap1.size(), 4);
        assert_eq!(heap1.find_min(), Some(&3));
    }

    #[test]
    fn test_consolidate_reduces_roots() {
        let mut heap = FibonacciHeap::new();
        for i in 1..=10 {
            heap.insert(i);
        }

        // Before extract_min, many roots
        let roots_before = heap.num_roots();

        heap.extract_min();

        // After extract_min, consolidation should reduce roots
        let roots_after = heap.num_roots();
        assert!(roots_after < roots_before);
    }

    #[test]
    fn test_extract_min_from_complex_heap() {
        let mut heap = FibonacciHeap::new();
        let values = vec![50, 30, 70, 20, 40, 60, 80, 10];
        for &v in &values {
            heap.insert(v);
        }

        let mut result = Vec::new();
        while let Some(val) = heap.extract_min() {
            result.push(val);
        }

        assert_eq!(result, vec![10, 20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_large_dataset() {
        let mut heap = FibonacciHeap::new();
        for i in (0..100).rev() {
            heap.insert(i);
        }

        assert_eq!(heap.size(), 100);
        assert_eq!(heap.find_min(), Some(&0));

        for i in 0..100 {
            assert_eq!(heap.extract_min(), Some(i));
        }
    }

    #[test]
    fn test_decrease_key_cascading() {
        let mut heap = FibonacciHeap::new();

        // Build a heap and extract min to create some structure
        for i in 1..=20 {
            heap.insert(i);
        }
        heap.extract_min(); // Trigger consolidation

        // Now decrease a key (this may trigger cascading cuts)
        let id = heap.insert(100);
        assert!(heap.decrease_key(id, 0).is_ok());
        assert_eq!(heap.find_min(), Some(&0));
    }
}
