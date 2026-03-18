// ds01_red_black_tree.rs
//
// Red-Black Tree is a self-balancing binary search tree where each node has a color
// (red or black) and the tree maintains balance through color properties and rotations.
// Red-Black Trees guarantee O(log n) worst-case performance for insertions, deletions,
// and searches, making them ideal for use in standard library implementations (e.g., TreeMap).
//
// Red-Black Tree Properties:
// 1. Every node is either red or black
// 2. The root is always black
// 3. All leaves (NIL nodes) are black
// 4. If a node is red, both its children must be black (no two red nodes in a row)
// 5. Every path from root to leaf contains the same number of black nodes
//
// Time Complexity:
// - Search: O(log n)
// - Insert: O(log n)
// - Delete: O(log n)
// - Space: O(n)
//
// Your task: Implement a Red-Black Tree with insert, search, and rotation operations.

// I AM NOT DONE

use std::fmt::Debug;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Color {
    Red,
    Black,
}

#[derive(Debug, Clone)]
pub struct Node<T: Ord + Clone + Debug> {
    value: T,
    color: Color,
    left: Option<Box<Node<T>>>,
    right: Option<Box<Node<T>>>,
}

impl<T: Ord + Clone + Debug> Node<T> {
    fn new(value: T, color: Color) -> Self {
        Self {
            value,
            color,
            left: None,
            right: None,
        }
    }

    fn is_red(&self) -> bool {
        self.color == Color::Red
    }
}

pub struct RedBlackTree<T: Ord + Clone + Debug> {
    root: Option<Box<Node<T>>>,
    size: usize,
}

impl<T: Ord + Clone + Debug> RedBlackTree<T> {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
        }
    }

    pub fn insert(&mut self, value: T) {
        // TODO: Implement insert operation
        // 1. Insert like a regular BST (as red node)
        // 2. Fix violations of red-black properties using rotations and recoloring
        // 3. Ensure root is black
        // Hint: You may want to implement helper functions for:
        //   - rotate_left, rotate_right
        //   - fix_violation (recolor and rotate as needed)
        todo!()
    }

    pub fn search(&self, value: &T) -> bool {
        // TODO: Implement search operation
        // Search like a regular BST
        // Return true if found, false otherwise
        todo!()
    }

    fn rotate_left(&mut self, node: &mut Box<Node<T>>) {
        // TODO: Perform left rotation
        // Used to restore balance after insertion
        todo!()
    }

    fn rotate_right(&mut self, node: &mut Box<Node<T>>) {
        // TODO: Perform right rotation
        // Used to restore balance after insertion
        todo!()
    }

    fn fix_violation(&mut self, node: &mut Box<Node<T>>) {
        // TODO: Fix red-black tree violations after insertion
        // Handle cases:
        // 1. Parent and uncle are red: recolor
        // 2. Parent is red, uncle is black: rotate
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.root.is_none()
    }

    pub fn black_height(&self) -> usize {
        // TODO: Calculate the black height of the tree
        // (number of black nodes from root to any leaf)
        todo!()
    }

    pub fn validate(&self) -> bool {
        // TODO: Validate that the tree satisfies all Red-Black properties
        // This is useful for testing
        todo!()
    }

    pub fn inorder(&self) -> Vec<T> {
        // TODO: Return values in sorted order
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_tree() {
        let tree: RedBlackTree<i32> = RedBlackTree::new();
        assert!(tree.is_empty());
        assert_eq!(tree.size(), 0);
    }

    #[test]
    fn test_insert_single_element() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        assert!(!tree.is_empty());
        assert_eq!(tree.size(), 1);
        assert!(tree.search(&10));
    }

    #[test]
    fn test_insert_multiple_elements() {
        let mut tree = RedBlackTree::new();
        for i in [5, 3, 7, 1, 9] {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 5);
        assert!(tree.search(&5));
        assert!(tree.search(&1));
        assert!(tree.search(&9));
        assert!(!tree.search(&100));
    }

    #[test]
    fn test_insert_ascending_order() {
        let mut tree = RedBlackTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 10);
        for i in 1..=10 {
            assert!(tree.search(&i));
        }
    }

    #[test]
    fn test_insert_descending_order() {
        let mut tree = RedBlackTree::new();
        for i in (1..=10).rev() {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 10);
        for i in 1..=10 {
            assert!(tree.search(&i));
        }
    }

    #[test]
    fn test_root_is_black() {
        let mut tree = RedBlackTree::new();
        tree.insert(5);
        tree.insert(3);
        tree.insert(7);
        // Root should always be black
        if let Some(ref root) = tree.root {
            assert_eq!(root.color, Color::Black);
        }
    }

    #[test]
    fn test_red_black_properties() {
        let mut tree = RedBlackTree::new();
        for i in [10, 5, 15, 3, 7, 12, 17, 1, 4, 6, 8] {
            tree.insert(i);
        }
        assert!(tree.validate());
    }

    #[test]
    fn test_black_height_consistent() {
        let mut tree = RedBlackTree::new();
        for i in 1..=7 {
            tree.insert(i);
        }
        let bh = tree.black_height();
        assert!(bh > 0);
        assert!(tree.validate());
    }

    #[test]
    fn test_inorder_traversal() {
        let mut tree = RedBlackTree::new();
        let values = [50, 30, 70, 20, 40, 60, 80];
        for &v in &values {
            tree.insert(v);
        }
        let result = tree.inorder();
        assert_eq!(result, vec![20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_search_non_existent() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);
        assert!(!tree.search(&5));
        assert!(!tree.search(&15));
        assert!(!tree.search(&40));
    }

    #[test]
    fn test_large_dataset() {
        let mut tree = RedBlackTree::new();
        for i in 0..100 {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 100);
        assert!(tree.validate());
        for i in 0..100 {
            assert!(tree.search(&i));
        }
    }

    #[test]
    fn test_duplicate_insertion() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        tree.insert(10);
        // Implementation can either ignore duplicates or store them
        assert!(tree.search(&10));
        assert!(tree.validate());
    }
}
