// db01_btree.rs
//
// B-Tree is a self-balancing tree data structure that maintains sorted data and allows
// searches, sequential access, insertions, and deletions in logarithmic time. B-Trees
// are commonly used in databases and file systems because they minimize disk I/O operations.
//
// A B-Tree of order M has the following properties:
// - Every node has at most M children
// - Every non-leaf node (except root) has at least M/2 children
// - The root has at least 2 children if it's not a leaf node
// - All leaves appear at the same level
// - A non-leaf node with k children contains k-1 keys
//
// Your task: Implement a B-Tree with insert, search, and split operations.

// I AM NOT DONE

use std::fmt::Debug;

const ORDER: usize = 4; // Maximum number of children per node

#[derive(Debug, Clone)]
pub struct BTreeNode<K: Ord + Clone + Debug> {
    keys: Vec<K>,
    children: Vec<Box<BTreeNode<K>>>,
    is_leaf: bool,
}

impl<K: Ord + Clone + Debug> BTreeNode<K> {
    fn new(is_leaf: bool) -> Self {
        Self {
            keys: Vec::new(),
            children: Vec::new(),
            is_leaf,
        }
    }

    fn is_full(&self) -> bool {
        self.keys.len() >= ORDER - 1
    }
}

pub struct BTree<K: Ord + Clone + Debug> {
    root: Option<Box<BTreeNode<K>>>,
}

impl<K: Ord + Clone + Debug> BTree<K> {
    pub fn new() -> Self {
        Self { root: None }
    }

    pub fn search(&self, key: &K) -> bool {
        // TODO: Implement search operation
        // Traverse the tree from root to find the key
        // Return true if found, false otherwise
        todo!()
    }

    pub fn insert(&mut self, key: K) {
        // TODO: Implement insert operation
        // If root is None, create a new root
        // If root is full, split it and create a new root
        // Otherwise, insert into the appropriate subtree
        todo!()
    }

    fn insert_non_full(&mut self, node: &mut BTreeNode<K>, key: K) {
        // TODO: Insert key into a non-full node
        // Find the correct position for the key
        // If leaf, insert directly
        // If internal node, recursively insert into the appropriate child
        todo!()
    }

    fn split_child(&mut self, parent: &mut BTreeNode<K>, index: usize) {
        // TODO: Split the child at the given index
        // Create a new node to hold half of the keys
        // Move the median key up to the parent
        // Redistribute keys and children between the two nodes
        todo!()
    }

    pub fn height(&self) -> usize {
        // TODO: Return the height of the tree
        todo!()
    }

    pub fn inorder_traversal(&self) -> Vec<K> {
        // TODO: Return keys in sorted order
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_btree() {
        let btree: BTree<i32> = BTree::new();
        assert_eq!(btree.height(), 0);
    }

    #[test]
    fn test_insert_single_key() {
        let mut btree = BTree::new();
        btree.insert(10);
        assert!(btree.search(&10));
        assert!(!btree.search(&20));
    }

    #[test]
    fn test_insert_multiple_keys() {
        let mut btree = BTree::new();
        for i in [5, 15, 25, 35, 45] {
            btree.insert(i);
        }
        assert!(btree.search(&15));
        assert!(btree.search(&45));
        assert!(!btree.search(&100));
    }

    #[test]
    fn test_insert_triggers_split() {
        let mut btree = BTree::new();
        // Insert enough keys to trigger a split
        for i in 1..=10 {
            btree.insert(i * 10);
        }
        for i in 1..=10 {
            assert!(btree.search(&(i * 10)));
        }
    }

    #[test]
    fn test_search_non_existent_keys() {
        let mut btree = BTree::new();
        btree.insert(10);
        btree.insert(20);
        btree.insert(30);
        assert!(!btree.search(&5));
        assert!(!btree.search(&15));
        assert!(!btree.search(&40));
    }

    #[test]
    fn test_inorder_traversal() {
        let mut btree = BTree::new();
        let keys = [50, 30, 70, 20, 40, 60, 80];
        for &key in &keys {
            btree.insert(key);
        }
        let result = btree.inorder_traversal();
        assert_eq!(result, vec![20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_insert_duplicate_keys() {
        let mut btree = BTree::new();
        btree.insert(10);
        btree.insert(10);
        assert!(btree.search(&10));
    }

    #[test]
    fn test_height_increases_with_splits() {
        let mut btree = BTree::new();
        btree.insert(1);
        let initial_height = btree.height();

        // Insert many keys to force splits
        for i in 2..=20 {
            btree.insert(i);
        }
        assert!(btree.height() >= initial_height);
    }

    #[test]
    fn test_large_dataset() {
        let mut btree = BTree::new();
        for i in 0..100 {
            btree.insert(i);
        }
        for i in 0..100 {
            assert!(btree.search(&i));
        }
        assert!(!btree.search(&100));
    }

    #[test]
    fn test_insert_reverse_order() {
        let mut btree = BTree::new();
        for i in (1..=10).rev() {
            btree.insert(i);
        }
        for i in 1..=10 {
            assert!(btree.search(&i));
        }
        let result = btree.inorder_traversal();
        assert_eq!(result, (1..=10).collect::<Vec<_>>());
    }
}
