// dist03_consistent_hashing.rs
//
// Consistent Hashing is a distributed hashing scheme that minimizes key
// redistribution when nodes are added or removed. It's crucial for distributed
// caches, databases, and load balancers.
//
// Key properties:
// - When a node is added/removed, only K/n keys need to be remapped (K=total keys, n=nodes)
// - Contrast with traditional hashing where almost all keys need remapping
// - Virtual nodes improve load distribution
//
// Your task: Implement a consistent hash ring with virtual nodes.
//
// Key concepts:
// - Hash ring: Circular space of hash values (0 to 2^32-1)
// - Virtual nodes: Multiple positions per physical node for better distribution
// - Key lookup: Find the first node clockwise from the key's hash
// - Minimal disruption on topology changes

// I AM NOT DONE

use std::collections::{BTreeMap, HashMap, HashSet};
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

fn hash_value(data: &str) -> u64 {
    let mut hasher = DefaultHasher::new();
    data.hash(&mut hasher);
    hasher.finish()
}

#[derive(Debug, Clone)]
pub struct Node {
    pub id: String,
    pub keys: HashSet<String>,
}

impl Node {
    pub fn new(id: String) -> Self {
        Self {
            id,
            keys: HashSet::new(),
        }
    }
}

pub struct ConsistentHashRing {
    ring: BTreeMap<u64, String>,        // hash -> node_id (virtual nodes)
    nodes: HashMap<String, Node>,       // node_id -> node
    virtual_nodes: usize,               // Number of virtual nodes per physical node
    key_mapping: HashMap<String, String>, // key -> node_id for quick lookup
}

impl ConsistentHashRing {
    pub fn new(virtual_nodes: usize) -> Self {
        Self {
            ring: BTreeMap::new(),
            nodes: HashMap::new(),
            virtual_nodes,
            key_mapping: HashMap::new(),
        }
    }

    pub fn add_node(&mut self, node_id: String) {
        // TODO: Add a physical node with its virtual nodes
        // - Create virtual_nodes number of entries in the ring
        // - Virtual node hash: hash(node_id + "#" + replica_number)
        // - Add to nodes HashMap
        // - Redistribute keys that now belong to this node
        todo!()
    }

    pub fn remove_node(&mut self, node_id: &str) {
        // TODO: Remove a physical node and all its virtual nodes
        // - Remove all virtual nodes from the ring
        // - Redistribute keys to successor nodes
        // - Remove from nodes HashMap
        todo!()
    }

    pub fn get_node(&self, key: &str) -> Option<String> {
        // TODO: Find which node should store this key
        // - Hash the key
        // - Find the first virtual node at or after this hash (clockwise)
        // - If no node found after hash, wrap around to first node
        // - Return the physical node ID (not virtual node)
        // - Return None if no nodes in ring
        todo!()
    }

    pub fn add_key(&mut self, key: String) -> Option<String> {
        // TODO: Add a key to the appropriate node
        // - Determine which node should store the key
        // - Add key to that node's key set
        // - Update key_mapping
        // - Return the node_id where key was added
        todo!()
    }

    pub fn remove_key(&mut self, key: &str) -> bool {
        // TODO: Remove a key from its node
        // - Find which node has the key
        // - Remove from node's key set
        // - Remove from key_mapping
        // - Return true if key was found and removed
        todo!()
    }

    pub fn get_key_location(&self, key: &str) -> Option<String> {
        self.key_mapping.get(key).cloned()
    }

    pub fn get_node_info(&self, node_id: &str) -> Option<&Node> {
        self.nodes.get(node_id)
    }

    pub fn get_node_count(&self) -> usize {
        self.nodes.len()
    }

    pub fn get_virtual_node_count(&self) -> usize {
        self.ring.len()
    }

    pub fn get_all_nodes(&self) -> Vec<String> {
        self.nodes.keys().cloned().collect()
    }

    pub fn get_distribution(&self) -> HashMap<String, usize> {
        // Return how many keys each node has
        self.nodes
            .iter()
            .map(|(id, node)| (id.clone(), node.keys.len()))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_single_node() {
        let mut ring = ConsistentHashRing::new(3);
        ring.add_node("node1".to_string());

        assert_eq!(ring.get_node_count(), 1);
        assert_eq!(ring.get_virtual_node_count(), 3);
    }

    #[test]
    fn test_add_multiple_nodes() {
        let mut ring = ConsistentHashRing::new(5);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());
        ring.add_node("node3".to_string());

        assert_eq!(ring.get_node_count(), 3);
        assert_eq!(ring.get_virtual_node_count(), 15); // 3 nodes * 5 virtual nodes
    }

    #[test]
    fn test_get_node_for_key() {
        let mut ring = ConsistentHashRing::new(100);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());

        let node = ring.get_node("my_key");
        assert!(node.is_some());
        assert!(node.unwrap() == "node1" || node.unwrap() == "node2");
    }

    #[test]
    fn test_consistent_key_mapping() {
        let mut ring = ConsistentHashRing::new(100);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());

        // Same key should always map to same node
        let node1 = ring.get_node("test_key").unwrap();
        let node2 = ring.get_node("test_key").unwrap();
        assert_eq!(node1, node2);
    }

    #[test]
    fn test_add_and_retrieve_keys() {
        let mut ring = ConsistentHashRing::new(50);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());

        ring.add_key("key1".to_string());
        ring.add_key("key2".to_string());
        ring.add_key("key3".to_string());

        assert!(ring.get_key_location("key1").is_some());
        assert!(ring.get_key_location("key2").is_some());
        assert!(ring.get_key_location("key3").is_some());
    }

    #[test]
    fn test_minimal_redistribution_on_add() {
        let mut ring = ConsistentHashRing::new(100);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());

        // Add 100 keys
        for i in 0..100 {
            ring.add_key(format!("key{}", i));
        }

        // Track original distribution
        let dist_before = ring.get_distribution();

        // Add a new node
        ring.add_node("node3".to_string());

        // Track new distribution
        let dist_after = ring.get_distribution();

        // Most keys should stay on their original nodes
        let node1_before = dist_before.get("node1").unwrap_or(&0);
        let node2_before = dist_before.get("node2").unwrap_or(&0);
        let node1_after = dist_after.get("node1").unwrap_or(&0);
        let node2_after = dist_after.get("node2").unwrap_or(&0);

        // Each original node should have lost some keys but not all
        assert!(node1_after < node1_before);
        assert!(node2_after < node2_before);
        assert!(*node1_after > 0);
        assert!(*node2_after > 0);

        // New node should have some keys
        let node3_after = dist_after.get("node3").unwrap_or(&0);
        assert!(*node3_after > 0);
    }

    #[test]
    fn test_remove_node_redistribution() {
        let mut ring = ConsistentHashRing::new(100);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());
        ring.add_node("node3".to_string());

        // Add keys
        for i in 0..90 {
            ring.add_key(format!("key{}", i));
        }

        // Remove a node
        ring.remove_node("node2");

        assert_eq!(ring.get_node_count(), 2);

        // All keys should still be accessible
        for i in 0..90 {
            assert!(ring.get_key_location(&format!("key{}", i)).is_some());
        }

        // Keys should only be on node1 and node3
        let dist = ring.get_distribution();
        assert!(!dist.contains_key("node2"));
        assert!(dist.get("node1").unwrap_or(&0) > &0);
        assert!(dist.get("node3").unwrap_or(&0) > &0);
    }

    #[test]
    fn test_load_distribution_with_virtual_nodes() {
        let mut ring = ConsistentHashRing::new(150);
        ring.add_node("node1".to_string());
        ring.add_node("node2".to_string());
        ring.add_node("node3".to_string());

        // Add many keys
        for i in 0..300 {
            ring.add_key(format!("key{}", i));
        }

        let dist = ring.get_distribution();

        // With enough virtual nodes, distribution should be relatively balanced
        // Each node should have roughly 100 keys (±30%)
        for (_, count) in dist.iter() {
            assert!(*count > 70 && *count < 130);
        }
    }

    #[test]
    fn test_remove_key() {
        let mut ring = ConsistentHashRing::new(50);
        ring.add_node("node1".to_string());
        ring.add_key("test_key".to_string());

        assert!(ring.get_key_location("test_key").is_some());

        assert!(ring.remove_key("test_key"));
        assert!(ring.get_key_location("test_key").is_none());

        assert!(!ring.remove_key("test_key")); // Already removed
    }

    #[test]
    fn test_no_nodes() {
        let ring = ConsistentHashRing::new(100);
        assert_eq!(ring.get_node("any_key"), None);
    }

    #[test]
    fn test_virtual_nodes_improve_distribution() {
        // Test with few virtual nodes
        let mut ring_few = ConsistentHashRing::new(1);
        ring_few.add_node("node1".to_string());
        ring_few.add_node("node2".to_string());
        ring_few.add_node("node3".to_string());

        for i in 0..300 {
            ring_few.add_key(format!("key{}", i));
        }

        let dist_few = ring_few.get_distribution();
        let counts_few: Vec<usize> = dist_few.values().cloned().collect();
        let max_few = *counts_few.iter().max().unwrap();
        let min_few = *counts_few.iter().min().unwrap();
        let variance_few = max_few - min_few;

        // Test with many virtual nodes
        let mut ring_many = ConsistentHashRing::new(150);
        ring_many.add_node("node1".to_string());
        ring_many.add_node("node2".to_string());
        ring_many.add_node("node3".to_string());

        for i in 0..300 {
            ring_many.add_key(format!("key{}", i));
        }

        let dist_many = ring_many.get_distribution();
        let counts_many: Vec<usize> = dist_many.values().cloned().collect();
        let max_many = *counts_many.iter().max().unwrap();
        let min_many = *counts_many.iter().min().unwrap();
        let variance_many = max_many - min_many;

        // More virtual nodes should reduce variance
        assert!(variance_many < variance_few);
    }

    #[test]
    fn test_single_node_gets_all_keys() {
        let mut ring = ConsistentHashRing::new(50);
        ring.add_node("node1".to_string());

        for i in 0..100 {
            ring.add_key(format!("key{}", i));
        }

        let dist = ring.get_distribution();
        assert_eq!(*dist.get("node1").unwrap(), 100);
    }
}
