// ds08_splay_tree.rs
//
// A Splay Tree is a self-adjusting binary search tree with the additional property that
// recently accessed elements are quick to access again. After every operation (search,
// insert, delete), the tree performs "splaying" - rotating the accessed node to the root.
//
// Splaying Operations:
// - Zig: Single rotation when node is child of root
// - Zig-Zig: Double rotation when node and parent are both left or both right children
// - Zig-Zag: Double rotation when node is left child and parent is right (or vice versa)
//
// Properties:
// - No explicit balance information stored (unlike AVL or Red-Black trees)
// - Self-optimizing based on access patterns
// - Amortized O(log n) performance
// - Works well for non-uniform access patterns (locality of reference)
//
// Applications:
// - Cache implementation (frequently accessed items near root)
// - Garbage collection
// - Data compression
// - Network routing tables
//
// Time Complexity (amortized):
// - Search: O(log n)
// - Insert: O(log n)
// - Delete: O(log n)
// - Worst case for single operation: O(n)
// - Space: O(n)
//
// Your task: Implement a Splay Tree with search, insert, delete, and splay operations.

// I AM NOT DONE

use std::fmt::Debug;

#[derive(Debug, Clone)]
pub struct Node<T: Ord + Clone + Debug> {
    value: T,
    left: Option<Box<Node<T>>>,
    right: Option<Box<Node<T>>>,
}

impl<T: Ord + Clone + Debug> Node<T> {
    fn new(value: T) -> Self {
        Self {
            value,
            left: None,
            right: None,
        }
    }
}

pub struct SplayTree<T: Ord + Clone + Debug> {
    root: Option<Box<Node<T>>>,
    size: usize,
}

impl<T: Ord + Clone + Debug> SplayTree<T> {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
        }
    }

    pub fn insert(&mut self, value: T) {
        // TODO: Insert value and splay it to root
        // 1. If tree is empty, create root
        // 2. Otherwise, insert like BST
        // 3. Splay the newly inserted node to root
        // 4. Increment size
        todo!()
    }

    pub fn search(&mut self, value: &T) -> bool {
        // TODO: Search for value and splay it to root if found
        // If found, splay the node containing value to root and return true
        // If not found, splay the last accessed node to root and return false
        todo!()
    }

    pub fn delete(&mut self, value: &T) -> bool {
        // TODO: Delete value from tree
        // 1. Search for value (this splays it to root if found)
        // 2. If not found, return false
        // 3. If found:
        //    a. Delete root (now contains value)
        //    b. Split into left and right subtrees
        //    c. If left subtree exists, splay its maximum to root, then attach right subtree
        //    d. Otherwise, right subtree becomes new root
        // 4. Decrement size and return true
        todo!()
    }

    fn splay(&mut self, value: &T) {
        // TODO: Splay the node containing value to the root
        // Perform rotations based on the position of the node:
        // - Zig: node is child of root
        // - Zig-Zig: node and parent are both left or both right children
        // - Zig-Zag: node and parent are on opposite sides
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

    fn zig(&mut self, is_left: bool) {
        // TODO: Single rotation (when node is child of root)
        todo!()
    }

    fn zig_zig(&mut self, is_left: bool) {
        // TODO: Double rotation (same direction)
        // Both node and parent are left children or both are right children
        todo!()
    }

    fn zig_zag(&mut self, parent_is_left: bool) {
        // TODO: Double rotation (opposite directions)
        // Node is left child and parent is right child (or vice versa)
        todo!()
    }

    pub fn find_min(&mut self) -> Option<T> {
        // TODO: Find and return minimum value (splay it to root)
        todo!()
    }

    pub fn find_max(&mut self) -> Option<T> {
        // TODO: Find and return maximum value (splay it to root)
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.root.is_none()
    }

    pub fn inorder(&self) -> Vec<T> {
        // TODO: Return values in sorted order
        // Helper function for testing
        todo!()
    }

    fn inorder_helper(node: &Option<Box<Node<T>>>, result: &mut Vec<T>) {
        // TODO: Recursive inorder traversal
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_tree() {
        let tree: SplayTree<i32> = SplayTree::new();
        assert!(tree.is_empty());
        assert_eq!(tree.size(), 0);
    }

    #[test]
    fn test_insert_single_element() {
        let mut tree = SplayTree::new();
        tree.insert(10);
        assert_eq!(tree.size(), 1);
        assert!(!tree.is_empty());
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 10);
        }
    }

    #[test]
    fn test_insert_multiple_elements() {
        let mut tree = SplayTree::new();
        tree.insert(5);
        tree.insert(3);
        tree.insert(7);

        assert_eq!(tree.size(), 3);
        // Last inserted element should be at root
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 7);
        }
    }

    #[test]
    fn test_search_existing_element() {
        let mut tree = SplayTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);

        assert!(tree.search(&5));
        // Searched element should now be at root
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 5);
        }
    }

    #[test]
    fn test_search_non_existing_element() {
        let mut tree = SplayTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);

        assert!(!tree.search(&20));
    }

    #[test]
    fn test_delete_element() {
        let mut tree = SplayTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);

        assert!(tree.delete(&10));
        assert_eq!(tree.size(), 2);
        assert!(!tree.search(&10));
    }

    #[test]
    fn test_delete_non_existing() {
        let mut tree = SplayTree::new();
        tree.insert(10);
        tree.insert(5);

        assert!(!tree.delete(&20));
        assert_eq!(tree.size(), 2);
    }

    #[test]
    fn test_inorder_traversal() {
        let mut tree = SplayTree::new();
        let values = vec![50, 30, 70, 20, 40, 60, 80];
        for &v in &values {
            tree.insert(v);
        }

        let result = tree.inorder();
        assert_eq!(result, vec![20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_find_min() {
        let mut tree = SplayTree::new();
        tree.insert(50);
        tree.insert(30);
        tree.insert(70);
        tree.insert(20);

        assert_eq!(tree.find_min(), Some(20));
        // Min should now be at root
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 20);
        }
    }

    #[test]
    fn test_find_max() {
        let mut tree = SplayTree::new();
        tree.insert(50);
        tree.insert(30);
        tree.insert(70);
        tree.insert(80);

        assert_eq!(tree.find_max(), Some(80));
        // Max should now be at root
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 80);
        }
    }

    #[test]
    fn test_access_pattern_optimization() {
        let mut tree = SplayTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }

        // Access 5 repeatedly
        for _ in 0..3 {
            tree.search(&5);
        }

        // 5 should be at root due to splaying
        if let Some(ref root) = tree.root {
            assert_eq!(root.value, 5);
        }
    }

    #[test]
    fn test_insert_ascending_order() {
        let mut tree = SplayTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }

        assert_eq!(tree.size(), 10);
        let result = tree.inorder();
        assert_eq!(result, (1..=10).collect::<Vec<_>>());
    }

    #[test]
    fn test_multiple_deletes() {
        let mut tree = SplayTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }

        assert!(tree.delete(&5));
        assert!(tree.delete(&1));
        assert!(tree.delete(&10));

        assert_eq!(tree.size(), 7);
        let result = tree.inorder();
        assert_eq!(result, vec![2, 3, 4, 6, 7, 8, 9]);
    }
}
