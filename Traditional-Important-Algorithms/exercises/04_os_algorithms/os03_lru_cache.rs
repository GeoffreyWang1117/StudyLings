// os03_lru_cache.rs
//
// LRU (Least Recently Used) is a cache eviction policy that discards the least
// recently used items first. This is commonly used in operating systems for page
// replacement and in various caching systems.
//
// Your task: Implement an LRU cache using a HashMap and a doubly-linked list.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct NodePtr(usize);

#[derive(Debug)]
struct Node<K, V> {
    key: K,
    value: V,
    prev: Option<NodePtr>,
    next: Option<NodePtr>,
}

pub struct LRUCache<K, V>
where
    K: Clone + Eq + std::hash::Hash,
    V: Clone,
{
    capacity: usize,
    map: HashMap<K, NodePtr>,
    nodes: Vec<Option<Node<K, V>>>,
    head: Option<NodePtr>,
    tail: Option<NodePtr>,
    free_list: Vec<NodePtr>,
}

impl<K, V> LRUCache<K, V>
where
    K: Clone + Eq + std::hash::Hash,
    V: Clone,
{
    pub fn new(capacity: usize) -> Self {
        Self {
            capacity,
            map: HashMap::new(),
            nodes: Vec::new(),
            head: None,
            tail: None,
            free_list: Vec::new(),
        }
    }

    fn allocate_node(&mut self, key: K, value: V) -> NodePtr {
        // TODO: Allocate a new node
        // If there's a free node in free_list, reuse it
        // Otherwise, push a new node to the nodes vector
        todo!()
    }

    fn free_node(&mut self, ptr: NodePtr) {
        // TODO: Mark a node as free and add it to the free_list
        todo!()
    }

    fn move_to_front(&mut self, ptr: NodePtr) {
        // TODO: Move a node to the front of the list (most recently used)
        // 1. Remove the node from its current position
        // 2. Insert it at the head
        todo!()
    }

    fn remove_node(&mut self, ptr: NodePtr) {
        // TODO: Remove a node from the doubly-linked list
        // Update the prev and next pointers of neighboring nodes
        todo!()
    }

    fn add_to_front(&mut self, ptr: NodePtr) {
        // TODO: Add a node to the front of the list
        // Update head, tail, and the node's prev/next pointers
        todo!()
    }

    fn evict_lru(&mut self) -> Option<K> {
        // TODO: Evict the least recently used item (at the tail)
        // 1. Remove the tail node from the list
        // 2. Remove it from the map
        // 3. Free the node
        // 4. Return the evicted key
        todo!()
    }

    pub fn get(&mut self, key: &K) -> Option<V> {
        // TODO: Get a value from the cache
        // 1. Look up the key in the map
        // 2. Move the node to the front (mark as recently used)
        // 3. Return the value
        todo!()
    }

    pub fn put(&mut self, key: K, value: V) {
        // TODO: Insert or update a key-value pair
        // 1. If key exists, update the value and move to front
        // 2. If key doesn't exist:
        //    a. If at capacity, evict the LRU item
        //    b. Allocate a new node
        //    c. Add to front
        //    d. Add to map
        todo!()
    }

    pub fn len(&self) -> usize {
        self.map.len()
    }

    pub fn is_empty(&self) -> bool {
        self.map.is_empty()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_operations() {
        let mut cache = LRUCache::new(2);

        cache.put(1, "one");
        cache.put(2, "two");

        assert_eq!(cache.get(&1), Some("one"));
        assert_eq!(cache.get(&2), Some("two"));
    }

    #[test]
    fn test_eviction() {
        let mut cache = LRUCache::new(2);

        cache.put(1, "one");
        cache.put(2, "two");
        cache.put(3, "three"); // Should evict key 1

        assert_eq!(cache.get(&1), None);
        assert_eq!(cache.get(&2), Some("two"));
        assert_eq!(cache.get(&3), Some("three"));
    }

    #[test]
    fn test_update_existing() {
        let mut cache = LRUCache::new(2);

        cache.put(1, "one");
        cache.put(2, "two");
        cache.put(1, "ONE"); // Update existing key

        assert_eq!(cache.get(&1), Some("ONE"));
        assert_eq!(cache.len(), 2);
    }

    #[test]
    fn test_lru_ordering() {
        let mut cache = LRUCache::new(2);

        cache.put(1, "one");
        cache.put(2, "two");
        cache.get(&1); // Access key 1, making it more recent
        cache.put(3, "three"); // Should evict key 2 (least recently used)

        assert_eq!(cache.get(&1), Some("one"));
        assert_eq!(cache.get(&2), None);
        assert_eq!(cache.get(&3), Some("three"));
    }

    #[test]
    fn test_capacity_one() {
        let mut cache = LRUCache::new(1);

        cache.put(1, "one");
        assert_eq!(cache.get(&1), Some("one"));

        cache.put(2, "two"); // Should evict key 1
        assert_eq!(cache.get(&1), None);
        assert_eq!(cache.get(&2), Some("two"));
    }

    #[test]
    fn test_multiple_evictions() {
        let mut cache = LRUCache::new(3);

        cache.put(1, "one");
        cache.put(2, "two");
        cache.put(3, "three");
        cache.put(4, "four"); // Evict 1
        cache.put(5, "five"); // Evict 2

        assert_eq!(cache.get(&1), None);
        assert_eq!(cache.get(&2), None);
        assert_eq!(cache.get(&3), Some("three"));
        assert_eq!(cache.get(&4), Some("four"));
        assert_eq!(cache.get(&5), Some("five"));
    }

    #[test]
    fn test_get_updates_recency() {
        let mut cache = LRUCache::new(3);

        cache.put(1, "one");
        cache.put(2, "two");
        cache.put(3, "three");

        cache.get(&1); // Make 1 most recent
        cache.get(&2); // Make 2 most recent

        cache.put(4, "four"); // Should evict 3

        assert_eq!(cache.get(&1), Some("one"));
        assert_eq!(cache.get(&2), Some("two"));
        assert_eq!(cache.get(&3), None);
        assert_eq!(cache.get(&4), Some("four"));
    }

    #[test]
    fn test_empty_cache() {
        let mut cache: LRUCache<i32, &str> = LRUCache::new(5);

        assert!(cache.is_empty());
        assert_eq!(cache.len(), 0);
        assert_eq!(cache.get(&1), None);
    }

    #[test]
    fn test_string_keys() {
        let mut cache = LRUCache::new(3);

        cache.put("key1".to_string(), 1);
        cache.put("key2".to_string(), 2);
        cache.put("key3".to_string(), 3);

        assert_eq!(cache.get(&"key1".to_string()), Some(1));
        assert_eq!(cache.get(&"key2".to_string()), Some(2));

        cache.put("key4".to_string(), 4);

        assert_eq!(cache.get(&"key3".to_string()), None);
    }
}
