// db02_bplus_tree.rs
//
// B+ Tree is a variation of B-Tree where all values are stored in leaf nodes,
// and leaf nodes are linked together to allow efficient range queries.
// Internal nodes only store keys for navigation.
//
// Key differences from B-Tree:
// - All data is stored in leaf nodes
// - Leaf nodes are linked together (doubly linked list)
// - Internal nodes only contain keys and child pointers
// - Better for range queries and sequential access
//
// Your task: Implement a B+ Tree with leaf node linking for efficient range queries.

// I AM NOT DONE

use std::fmt::Debug;

const ORDER: usize = 4;

#[derive(Debug, Clone)]
pub struct BPlusTreeNode<K: Ord + Clone + Debug, V: Clone + Debug> {
    keys: Vec<K>,
    is_leaf: bool,
    // For internal nodes
    children: Vec<Box<BPlusTreeNode<K, V>>>,
    // For leaf nodes
    values: Vec<V>,
    next: Option<Box<BPlusTreeNode<K, V>>>,
}

impl<K: Ord + Clone + Debug, V: Clone + Debug> BPlusTreeNode<K, V> {
    fn new_leaf() -> Self {
        Self {
            keys: Vec::new(),
            is_leaf: true,
            children: Vec::new(),
            values: Vec::new(),
            next: None,
        }
    }

    fn new_internal() -> Self {
        Self {
            keys: Vec::new(),
            is_leaf: false,
            children: Vec::new(),
            values: Vec::new(),
            next: None,
        }
    }
}

pub struct BPlusTree<K: Ord + Clone + Debug, V: Clone + Debug> {
    root: Option<Box<BPlusTreeNode<K, V>>>,
}

impl<K: Ord + Clone + Debug, V: Clone + Debug> BPlusTree<K, V> {
    pub fn new() -> Self {
        Self { root: None }
    }

    pub fn insert(&mut self, key: K, value: V) {
        // TODO: Implement insert operation
        // If root is None, create a new leaf node
        // If root is full, split it and create a new internal root
        // Navigate to the appropriate leaf and insert the key-value pair
        todo!()
    }

    pub fn search(&self, key: &K) -> Option<V> {
        // TODO: Search for a key and return its value
        // Navigate through internal nodes to find the leaf
        // Search in the leaf node for the key
        todo!()
    }

    pub fn range_query(&self, start: &K, end: &K) -> Vec<(K, V)> {
        // TODO: Return all key-value pairs in the range [start, end]
        // Find the leaf containing start
        // Traverse linked leaf nodes until we exceed end
        // Collect all matching key-value pairs
        todo!()
    }

    fn find_leaf(&self, key: &K) -> Option<&BPlusTreeNode<K, V>> {
        // TODO: Navigate to the leaf node that should contain the key
        todo!()
    }

    pub fn inorder_keys(&self) -> Vec<K> {
        // TODO: Return all keys in sorted order by traversing leaf nodes
        todo!()
    }

    pub fn height(&self) -> usize {
        // TODO: Return the height of the tree
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_bplus_tree() {
        let tree: BPlusTree<i32, String> = BPlusTree::new();
        assert_eq!(tree.height(), 0);
    }

    #[test]
    fn test_insert_and_search() {
        let mut tree = BPlusTree::new();
        tree.insert(10, "ten".to_string());
        tree.insert(20, "twenty".to_string());

        assert_eq!(tree.search(&10), Some("ten".to_string()));
        assert_eq!(tree.search(&20), Some("twenty".to_string()));
        assert_eq!(tree.search(&30), None);
    }

    #[test]
    fn test_insert_multiple_values() {
        let mut tree = BPlusTree::new();
        for i in 1..=10 {
            tree.insert(i, format!("value_{}", i));
        }

        for i in 1..=10 {
            assert_eq!(tree.search(&i), Some(format!("value_{}", i)));
        }
    }

    #[test]
    fn test_range_query_basic() {
        let mut tree = BPlusTree::new();
        for i in 1..=10 {
            tree.insert(i, i * 10);
        }

        let result = tree.range_query(&3, &7);
        assert_eq!(result.len(), 5);
        assert!(result.iter().all(|(k, v)| *k >= 3 && *k <= 7 && *v == k * 10));
    }

    #[test]
    fn test_range_query_empty_range() {
        let mut tree = BPlusTree::new();
        tree.insert(10, 100);
        tree.insert(20, 200);

        let result = tree.range_query(&15, &15);
        assert!(result.is_empty() || result.len() == 1);
    }

    #[test]
    fn test_range_query_all_elements() {
        let mut tree = BPlusTree::new();
        for i in 1..=5 {
            tree.insert(i, i * 2);
        }

        let result = tree.range_query(&1, &5);
        assert_eq!(result.len(), 5);
    }

    #[test]
    fn test_inorder_keys() {
        let mut tree = BPlusTree::new();
        let keys = [50, 30, 70, 20, 40, 60, 80];
        for &key in &keys {
            tree.insert(key, key);
        }

        let result = tree.inorder_keys();
        assert_eq!(result, vec![20, 30, 40, 50, 60, 70, 80]);
    }

    #[test]
    fn test_update_existing_key() {
        let mut tree = BPlusTree::new();
        tree.insert(10, "first".to_string());
        tree.insert(10, "second".to_string());

        assert_eq!(tree.search(&10), Some("second".to_string()));
    }

    #[test]
    fn test_large_dataset() {
        let mut tree = BPlusTree::new();
        for i in 0..100 {
            tree.insert(i, i * 2);
        }

        for i in 0..100 {
            assert_eq!(tree.search(&i), Some(i * 2));
        }
    }

    #[test]
    fn test_range_query_with_large_dataset() {
        let mut tree = BPlusTree::new();
        for i in 0..50 {
            tree.insert(i, i);
        }

        let result = tree.range_query(&10, &20);
        assert_eq!(result.len(), 11);
        for (k, v) in result {
            assert!(k >= 10 && k <= 20);
            assert_eq!(k, v);
        }
    }

    #[test]
    fn test_reverse_insertion_order() {
        let mut tree = BPlusTree::new();
        for i in (1..=10).rev() {
            tree.insert(i, i);
        }

        let keys = tree.inorder_keys();
        assert_eq!(keys, (1..=10).collect::<Vec<_>>());
    }

    #[test]
    fn test_range_query_beyond_bounds() {
        let mut tree = BPlusTree::new();
        for i in 10..=20 {
            tree.insert(i, i);
        }

        let result = tree.range_query(&1, &100);
        assert_eq!(result.len(), 11);
    }
}
