// ds09_treap.rs
//
// A Treap (Tree + Heap) is a randomized binary search tree that maintains both BST
// ordering by key and heap ordering by priority. Each node has a key (for BST property)
// and a random priority (for heap property). The random priorities ensure the tree
// remains balanced with high probability.
//
// Properties:
// - BST property: left.key < node.key < right.key
// - Heap property: node.priority > children.priority (max-heap)
// - Priorities are assigned randomly during insertion
// - Expected height is O(log n)
//
// Advantages:
// - Simpler than deterministic balanced trees (AVL, Red-Black)
// - No need to store balance information
// - Supports efficient split and merge operations
// - Expected O(log n) performance for all operations
//
// Applications:
// - Randomized algorithms
// - Implicit treaps for array operations
// - Computational geometry (range trees)
// - Maintaining sorted sequences with efficient split/merge
//
// Time Complexity (expected):
// - Search: O(log n)
// - Insert: O(log n)
// - Delete: O(log n)
// - Split: O(log n)
// - Merge: O(log n)
// - Space: O(n)
//
// Your task: Implement a Treap with insert, delete, search, split, and merge operations.

// I AM NOT DONE

use std::fmt::Debug;

#[derive(Debug, Clone)]
pub struct Node<T: Ord + Clone + Debug> {
    key: T,
    priority: u64,
    left: Option<Box<Node<T>>>,
    right: Option<Box<Node<T>>>,
}

impl<T: Ord + Clone + Debug> Node<T> {
    fn new(key: T, priority: u64) -> Self {
        Self {
            key,
            priority,
            left: None,
            right: None,
        }
    }
}

pub struct Treap<T: Ord + Clone + Debug> {
    root: Option<Box<Node<T>>>,
    size: usize,
    rng_state: u64, // Simple random number generator state
}

impl<T: Ord + Clone + Debug> Treap<T> {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
            rng_state: 12345, // Simple seed
        }
    }

    fn random_priority(&mut self) -> u64 {
        // TODO: Generate a random priority using simple LCG
        // Linear Congruential Generator: state = (a * state + c) % m
        // Use: a = 1103515245, c = 12345, m = 2^31
        todo!()
    }

    pub fn insert(&mut self, key: T) {
        // TODO: Insert key with random priority
        // 1. Generate random priority
        // 2. Insert like BST based on key
        // 3. Rotate to maintain heap property based on priority
        // 4. Increment size
        todo!()
    }

    fn insert_recursive(&mut self, node: Option<Box<Node<T>>>, key: T, priority: u64)
        -> Option<Box<Node<T>>> {
        // TODO: Recursive helper for insert
        // 1. If node is None, create new node
        // 2. If key < node.key, insert into left subtree
        // 3. If key > node.key, insert into right subtree
        // 4. If key == node.key, update or ignore (your choice)
        // 5. After insertion, check heap property and rotate if needed
        todo!()
    }

    pub fn delete(&mut self, key: &T) -> bool {
        // TODO: Delete node with given key
        // 1. Find the node
        // 2. Rotate it down until it becomes a leaf
        // 3. Remove the leaf
        // 4. Decrement size if found
        todo!()
    }

    fn delete_recursive(&mut self, node: Option<Box<Node<T>>>, key: &T)
        -> (Option<Box<Node<T>>>, bool) {
        // TODO: Recursive helper for delete
        // Returns (new_node, was_deleted)
        todo!()
    }

    pub fn search(&self, key: &T) -> bool {
        // TODO: Search for key in the treap
        // Standard BST search based on key
        todo!()
    }

    fn rotate_right(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform right rotation
        //       y              x
        //      / \            / \
        //     x   C   =>     A   y
        //    / \                / \
        //   A   B              B   C
        todo!()
    }

    fn rotate_left(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform left rotation
        //     x                y
        //    / \              / \
        //   A   y     =>     x   C
        //      / \          / \
        //     B   C        A   B
        todo!()
    }

    pub fn split(&mut self, key: &T) -> (Treap<T>, Treap<T>) {
        // TODO: Split treap into two treaps
        // Left treap contains all keys < key
        // Right treap contains all keys >= key
        // This is a key operation for implicit treaps
        todo!()
    }

    pub fn merge(left: Treap<T>, right: Treap<T>) -> Treap<T> {
        // TODO: Merge two treaps
        // Precondition: all keys in left < all keys in right
        // Merge based on priorities (heap property)
        todo!()
    }

    fn merge_recursive(left: Option<Box<Node<T>>>, right: Option<Box<Node<T>>>)
        -> Option<Box<Node<T>>> {
        // TODO: Recursive helper for merge
        // Choose root based on which has higher priority
        // Recursively merge the other tree into appropriate subtree
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.root.is_none()
    }

    pub fn inorder(&self) -> Vec<T> {
        // TODO: Return keys in sorted order
        todo!()
    }

    fn inorder_helper(node: &Option<Box<Node<T>>>, result: &mut Vec<T>) {
        // TODO: Recursive inorder traversal
        todo!()
    }

    pub fn verify_bst_property(&self) -> bool {
        // TODO: Verify BST property holds
        // Useful for testing
        todo!()
    }

    pub fn verify_heap_property(&self) -> bool {
        // TODO: Verify heap property holds (parent.priority > children.priority)
        // Useful for testing
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_treap() {
        let treap: Treap<i32> = Treap::new();
        assert!(treap.is_empty());
        assert_eq!(treap.size(), 0);
    }

    #[test]
    fn test_insert_single_element() {
        let mut treap = Treap::new();
        treap.insert(10);
        assert_eq!(treap.size(), 1);
        assert!(treap.search(&10));
    }

    #[test]
    fn test_insert_multiple_elements() {
        let mut treap = Treap::new();
        for i in [5, 3, 7, 1, 9] {
            treap.insert(i);
        }
        assert_eq!(treap.size(), 5);
        for i in [5, 3, 7, 1, 9] {
            assert!(treap.search(&i));
        }
    }

    #[test]
    fn test_bst_property_maintained() {
        let mut treap = Treap::new();
        for i in 1..=20 {
            treap.insert(i);
        }
        assert!(treap.verify_bst_property());
    }

    #[test]
    fn test_heap_property_maintained() {
        let mut treap = Treap::new();
        for i in 1..=20 {
            treap.insert(i);
        }
        assert!(treap.verify_heap_property());
    }

    #[test]
    fn test_inorder_traversal() {
        let mut treap = Treap::new();
        let values = vec![50, 30, 70, 20, 40, 60, 80];
        for &v in &values {
            treap.insert(v);
        }
        let result = treap.inorder();
        assert_eq!(result, vec![20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_delete_element() {
        let mut treap = Treap::new();
        treap.insert(10);
        treap.insert(5);
        treap.insert(15);

        assert!(treap.delete(&10));
        assert_eq!(treap.size(), 2);
        assert!(!treap.search(&10));
        assert!(treap.verify_bst_property());
        assert!(treap.verify_heap_property());
    }

    #[test]
    fn test_delete_non_existing() {
        let mut treap = Treap::new();
        treap.insert(10);
        treap.insert(5);

        assert!(!treap.delete(&20));
        assert_eq!(treap.size(), 2);
    }

    #[test]
    fn test_search_non_existing() {
        let mut treap = Treap::new();
        treap.insert(10);
        treap.insert(20);
        assert!(!treap.search(&15));
        assert!(!treap.search(&5));
    }

    #[test]
    fn test_split() {
        let mut treap = Treap::new();
        for i in 1..=10 {
            treap.insert(i);
        }

        let (left, right) = treap.split(&5);

        // Left should have 1,2,3,4
        assert_eq!(left.size(), 4);
        assert!(left.search(&1));
        assert!(left.search(&4));
        assert!(!left.search(&5));

        // Right should have 5,6,7,8,9,10
        assert_eq!(right.size(), 6);
        assert!(right.search(&5));
        assert!(right.search(&10));
        assert!(!right.search(&4));
    }

    #[test]
    fn test_merge() {
        let mut left = Treap::new();
        for i in 1..=5 {
            left.insert(i);
        }

        let mut right = Treap::new();
        for i in 6..=10 {
            right.insert(i);
        }

        let merged = Treap::merge(left, right);
        assert_eq!(merged.size(), 10);
        assert!(merged.verify_bst_property());
        assert!(merged.verify_heap_property());
    }

    #[test]
    fn test_insert_ascending_order() {
        let mut treap = Treap::new();
        for i in 1..=20 {
            treap.insert(i);
        }
        assert_eq!(treap.size(), 20);
        let result = treap.inorder();
        assert_eq!(result, (1..=20).collect::<Vec<_>>());
    }

    #[test]
    fn test_insert_descending_order() {
        let mut treap = Treap::new();
        for i in (1..=20).rev() {
            treap.insert(i);
        }
        assert_eq!(treap.size(), 20);
        let result = treap.inorder();
        assert_eq!(result, (1..=20).collect::<Vec<_>>());
    }
}
