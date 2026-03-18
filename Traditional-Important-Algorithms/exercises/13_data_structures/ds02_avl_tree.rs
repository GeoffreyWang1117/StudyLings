// ds02_avl_tree.rs
//
// AVL Tree is a self-balancing binary search tree named after inventors Adelson-Velsky and Landis.
// In an AVL tree, the heights of the two child subtrees of any node differ by at most one.
// If at any time they differ by more than one, rebalancing is performed to restore this property.
//
// Balance Factor = height(left subtree) - height(right subtree)
// Valid balance factors: -1, 0, 1
//
// Rotations for rebalancing:
// - Left-Left (LL): Single right rotation
// - Right-Right (RR): Single left rotation
// - Left-Right (LR): Left rotation then right rotation
// - Right-Left (RL): Right rotation then left rotation
//
// Time Complexity:
// - Search: O(log n)
// - Insert: O(log n)
// - Delete: O(log n)
// - Space: O(n)
//
// Your task: Implement an AVL Tree with insert, search, and all four rotation types.

// I AM NOT DONE

use std::fmt::Debug;

#[derive(Debug, Clone)]
pub struct Node<T: Ord + Clone + Debug> {
    value: T,
    height: i32,
    left: Option<Box<Node<T>>>,
    right: Option<Box<Node<T>>>,
}

impl<T: Ord + Clone + Debug> Node<T> {
    fn new(value: T) -> Self {
        Self {
            value,
            height: 1,
            left: None,
            right: None,
        }
    }

    fn update_height(&mut self) {
        // TODO: Update the height based on children's heights
        // height = 1 + max(left_height, right_height)
        todo!()
    }

    fn balance_factor(&self) -> i32 {
        // TODO: Calculate balance factor
        // balance_factor = left_height - right_height
        todo!()
    }
}

pub struct AVLTree<T: Ord + Clone + Debug> {
    root: Option<Box<Node<T>>>,
    size: usize,
}

impl<T: Ord + Clone + Debug> AVLTree<T> {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
        }
    }

    pub fn insert(&mut self, value: T) {
        // TODO: Implement insert operation
        // 1. Insert like a regular BST
        // 2. Update heights on the way back up
        // 3. Check balance factors and perform rotations if needed
        // 4. Increment size
        todo!()
    }

    fn insert_recursive(&mut self, node: Option<Box<Node<T>>>, value: T) -> Option<Box<Node<T>>> {
        // TODO: Recursive helper for insert
        // After inserting, update height and rebalance
        todo!()
    }

    pub fn search(&self, value: &T) -> bool {
        // TODO: Implement search operation
        // Search like a regular BST
        todo!()
    }

    fn rotate_left(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform left rotation (RR case)
        //     y                x
        //    / \              / \
        //   T1  x     =>     y   T3
        //      / \          / \
        //     T2 T3        T1 T2
        todo!()
    }

    fn rotate_right(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform right rotation (LL case)
        //       y              x
        //      / \            / \
        //     x  T3   =>     T1  y
        //    / \                / \
        //   T1 T2              T2 T3
        todo!()
    }

    fn rotate_left_right(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform left-right rotation (LR case)
        // First rotate left on left child, then rotate right on node
        todo!()
    }

    fn rotate_right_left(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Perform right-left rotation (RL case)
        // First rotate right on right child, then rotate left on node
        todo!()
    }

    fn rebalance(&mut self, mut node: Box<Node<T>>) -> Box<Node<T>> {
        // TODO: Rebalance the node based on balance factor
        // Check balance factor and perform appropriate rotation:
        // - BF > 1 and left child BF >= 0: LL case (rotate right)
        // - BF > 1 and left child BF < 0: LR case (rotate left-right)
        // - BF < -1 and right child BF <= 0: RR case (rotate left)
        // - BF < -1 and right child BF > 0: RL case (rotate right-left)
        todo!()
    }

    pub fn height(&self) -> i32 {
        // TODO: Return the height of the tree
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn is_balanced(&self) -> bool {
        // TODO: Check if the tree is balanced (all nodes have BF in [-1, 0, 1])
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
        let tree: AVLTree<i32> = AVLTree::new();
        assert_eq!(tree.size(), 0);
        assert_eq!(tree.height(), 0);
    }

    #[test]
    fn test_insert_single_element() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        assert_eq!(tree.size(), 1);
        assert!(tree.search(&10));
        assert_eq!(tree.height(), 1);
    }

    #[test]
    fn test_insert_triggers_ll_rotation() {
        let mut tree = AVLTree::new();
        // Insert in descending order: triggers LL rotations
        tree.insert(30);
        tree.insert(20);
        tree.insert(10);

        assert!(tree.is_balanced());
        assert_eq!(tree.size(), 3);
        let result = tree.inorder();
        assert_eq!(result, vec![10, 20, 30]);
    }

    #[test]
    fn test_insert_triggers_rr_rotation() {
        let mut tree = AVLTree::new();
        // Insert in ascending order: triggers RR rotations
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);

        assert!(tree.is_balanced());
        assert_eq!(tree.size(), 3);
        let result = tree.inorder();
        assert_eq!(result, vec![10, 20, 30]);
    }

    #[test]
    fn test_insert_triggers_lr_rotation() {
        let mut tree = AVLTree::new();
        tree.insert(30);
        tree.insert(10);
        tree.insert(20); // Triggers LR rotation

        assert!(tree.is_balanced());
        let result = tree.inorder();
        assert_eq!(result, vec![10, 20, 30]);
    }

    #[test]
    fn test_insert_triggers_rl_rotation() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        tree.insert(30);
        tree.insert(20); // Triggers RL rotation

        assert!(tree.is_balanced());
        let result = tree.inorder();
        assert_eq!(result, vec![10, 20, 30]);
    }

    #[test]
    fn test_insert_multiple_elements() {
        let mut tree = AVLTree::new();
        for i in [50, 25, 75, 10, 30, 60, 80, 5, 15] {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 9);
        assert!(tree.is_balanced());
        for i in [50, 25, 75, 10, 30, 60, 80, 5, 15] {
            assert!(tree.search(&i));
        }
    }

    #[test]
    fn test_insert_ascending_order() {
        let mut tree = AVLTree::new();
        for i in 1..=20 {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 20);
        assert!(tree.is_balanced());
        let result = tree.inorder();
        assert_eq!(result, (1..=20).collect::<Vec<_>>());
    }

    #[test]
    fn test_insert_descending_order() {
        let mut tree = AVLTree::new();
        for i in (1..=20).rev() {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 20);
        assert!(tree.is_balanced());
        let result = tree.inorder();
        assert_eq!(result, (1..=20).collect::<Vec<_>>());
    }

    #[test]
    fn test_height_is_logarithmic() {
        let mut tree = AVLTree::new();
        for i in 1..=15 {
            tree.insert(i);
        }
        // For 15 nodes, height should be at most log2(15) + 1 ≈ 4-5
        assert!(tree.height() <= 5);
        assert!(tree.is_balanced());
    }

    #[test]
    fn test_search_non_existent() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);
        assert!(!tree.search(&5));
        assert!(!tree.search(&15));
        assert!(!tree.search(&40));
    }

    #[test]
    fn test_large_dataset_remains_balanced() {
        let mut tree = AVLTree::new();
        for i in 0..100 {
            tree.insert(i);
        }
        assert_eq!(tree.size(), 100);
        assert!(tree.is_balanced());
        // Height should be approximately log2(100) ≈ 6-7
        assert!(tree.height() <= 10);
    }
}
