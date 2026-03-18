// db09_skip_list.rs
//
// Skip List is a probabilistic data structure that allows O(log n) search, insert,
// and delete operations. It's an alternative to balanced trees that's simpler to
// implement and provides similar performance.
//
// Structure:
// - Multiple levels of linked lists
// - Bottom level contains all elements in sorted order
// - Each higher level is a "fast lane" that skips some elements
// - Elements are promoted to higher levels with probability p (typically 0.5)
//
// Benefits:
// - Simpler to implement than balanced trees
// - Lock-free implementations possible (good for concurrency)
// - Used in Redis (sorted sets) and LevelDB (memtable)
//
// Your task: Implement a Skip List with insert, search, and delete operations.

// I AM NOT DONE

use std::fmt::Debug;
use rand::Rng;

const MAX_LEVEL: usize = 16;
const PROBABILITY: f64 = 0.5;

struct Node<K: Ord + Clone + Debug, V: Clone + Debug> {
    key: K,
    value: V,
    forward: Vec<Option<Box<Node<K, V>>>>,
}

impl<K: Ord + Clone + Debug, V: Clone + Debug> Node<K, V> {
    fn new(key: K, value: V, level: usize) -> Self {
        Self {
            key,
            value,
            forward: vec![None; level + 1],
        }
    }
}

pub struct SkipList<K: Ord + Clone + Debug, V: Clone + Debug> {
    head: Node<K, V>,
    level: usize,
    size: usize,
}

impl<K: Ord + Clone + Debug + Default, V: Clone + Debug + Default> SkipList<K, V> {
    pub fn new() -> Self {
        Self {
            head: Node::new(K::default(), V::default(), MAX_LEVEL),
            level: 0,
            size: 0,
        }
    }

    pub fn insert(&mut self, key: K, value: V) {
        // TODO: Insert a key-value pair into the skip list
        // Find the position for insertion at each level
        // Determine random level for the new node
        // Insert the node and update forward pointers
        todo!()
    }

    pub fn search(&self, key: &K) -> Option<&V> {
        // TODO: Search for a key in the skip list
        // Start from the highest level
        // Move forward while next key is less than target
        // Drop down to next level when needed
        // Return value if found at level 0
        todo!()
    }

    pub fn delete(&mut self, key: &K) -> bool {
        // TODO: Delete a key from the skip list
        // Find the node at each level
        // Update forward pointers to skip the deleted node
        // Return true if deleted, false if not found
        todo!()
    }

    fn random_level(&self) -> usize {
        // TODO: Generate a random level for a new node
        // Use probability to determine how many levels
        // Flip a coin: if heads, go to next level
        // Maximum level is MAX_LEVEL
        let mut rng = rand::thread_rng();
        let mut level = 0;
        while rng.gen::<f64>() < PROBABILITY && level < MAX_LEVEL {
            level += 1;
        }
        level
    }

    pub fn len(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    pub fn contains(&self, key: &K) -> bool {
        self.search(key).is_some()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_skip_list() {
        let list: SkipList<i32, String> = SkipList::new();
        assert_eq!(list.len(), 0);
        assert!(list.is_empty());
    }

    #[test]
    fn test_insert_and_search() {
        let mut list = SkipList::new();
        list.insert(10, "ten".to_string());
        list.insert(20, "twenty".to_string());

        assert_eq!(list.search(&10), Some(&"ten".to_string()));
        assert_eq!(list.search(&20), Some(&"twenty".to_string()));
        assert_eq!(list.search(&30), None);
    }

    #[test]
    fn test_insert_maintains_order() {
        let mut list = SkipList::new();
        list.insert(30, 30);
        list.insert(10, 10);
        list.insert(20, 20);
        list.insert(40, 40);

        assert_eq!(list.search(&10), Some(&10));
        assert_eq!(list.search(&20), Some(&20));
        assert_eq!(list.search(&30), Some(&30));
        assert_eq!(list.search(&40), Some(&40));
    }

    #[test]
    fn test_update_existing_key() {
        let mut list = SkipList::new();
        list.insert(10, "first".to_string());
        list.insert(10, "second".to_string());

        assert_eq!(list.search(&10), Some(&"second".to_string()));
    }

    #[test]
    fn test_delete() {
        let mut list = SkipList::new();
        list.insert(10, 100);
        list.insert(20, 200);
        list.insert(30, 300);

        assert!(list.delete(&20));
        assert_eq!(list.search(&20), None);
        assert_eq!(list.search(&10), Some(&100));
        assert_eq!(list.search(&30), Some(&300));
    }

    #[test]
    fn test_delete_nonexistent() {
        let mut list = SkipList::new();
        list.insert(10, 100);

        assert!(!list.delete(&20));
        assert_eq!(list.len(), 1);
    }

    #[test]
    fn test_contains() {
        let mut list = SkipList::new();
        list.insert(10, 100);
        list.insert(20, 200);

        assert!(list.contains(&10));
        assert!(list.contains(&20));
        assert!(!list.contains(&30));
    }

    #[test]
    fn test_size_tracking() {
        let mut list = SkipList::new();
        assert_eq!(list.len(), 0);

        list.insert(10, 100);
        assert_eq!(list.len(), 1);

        list.insert(20, 200);
        assert_eq!(list.len(), 2);

        list.delete(&10);
        assert_eq!(list.len(), 1);
    }

    #[test]
    fn test_large_dataset() {
        let mut list = SkipList::new();

        for i in 0..100 {
            list.insert(i, i * 2);
        }

        assert_eq!(list.len(), 100);

        for i in 0..100 {
            assert_eq!(list.search(&i), Some(&(i * 2)));
        }
    }

    #[test]
    fn test_delete_all_elements() {
        let mut list = SkipList::new();

        for i in 0..10 {
            list.insert(i, i);
        }

        for i in 0..10 {
            assert!(list.delete(&i));
        }

        assert!(list.is_empty());
    }

    #[test]
    fn test_reverse_insertion_order() {
        let mut list = SkipList::new();

        for i in (0..10).rev() {
            list.insert(i, i * 10);
        }

        for i in 0..10 {
            assert_eq!(list.search(&i), Some(&(i * 10)));
        }
    }

    #[test]
    fn test_mixed_operations() {
        let mut list = SkipList::new();

        list.insert(5, 50);
        list.insert(3, 30);
        list.insert(7, 70);
        assert_eq!(list.len(), 3);

        list.delete(&3);
        assert_eq!(list.len(), 2);

        list.insert(9, 90);
        list.insert(1, 10);
        assert_eq!(list.len(), 4);

        assert_eq!(list.search(&1), Some(&10));
        assert_eq!(list.search(&5), Some(&50));
        assert_eq!(list.search(&7), Some(&70));
        assert_eq!(list.search(&9), Some(&90));
        assert_eq!(list.search(&3), None);
    }
}
