// db10_trie.rs
//
// Trie (Prefix Tree) is a tree-like data structure used for efficient string
// searching and prefix matching. Each node represents a character, and paths
// from root to leaves represent words or keys.
//
// Key properties:
// - Fast prefix search: O(m) where m is the length of the key
// - Space efficient for common prefixes
// - Supports wildcard and autocomplete queries
//
// Used in databases for:
// - Autocomplete features
// - Spell checkers
// - IP routing tables
// - Text indexing
//
// Your task: Implement a Trie with insert, search, and prefix matching.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug)]
struct TrieNode<V: Clone> {
    children: HashMap<char, TrieNode<V>>,
    value: Option<V>,
    is_end: bool,
}

impl<V: Clone> TrieNode<V> {
    fn new() -> Self {
        Self {
            children: HashMap::new(),
            value: None,
            is_end: false,
        }
    }
}

pub struct Trie<V: Clone> {
    root: TrieNode<V>,
    size: usize,
}

impl<V: Clone> Trie<V> {
    pub fn new() -> Self {
        Self {
            root: TrieNode::new(),
            size: 0,
        }
    }

    pub fn insert(&mut self, key: &str, value: V) {
        // TODO: Insert a key-value pair into the trie
        // Traverse the trie, creating nodes as needed
        // Mark the final node as end of word and store value
        todo!()
    }

    pub fn search(&self, key: &str) -> Option<&V> {
        // TODO: Search for an exact key match
        // Traverse the trie following the key characters
        // Return the value if found and is_end is true
        todo!()
    }

    pub fn starts_with(&self, prefix: &str) -> bool {
        // TODO: Check if any key starts with the given prefix
        // Traverse the trie following the prefix characters
        // Return true if we can complete the traversal
        todo!()
    }

    pub fn get_all_with_prefix(&self, prefix: &str) -> Vec<(String, V)> {
        // TODO: Get all key-value pairs with the given prefix
        // Find the node representing the prefix
        // Do DFS from that node to collect all words
        todo!()
    }

    pub fn delete(&mut self, key: &str) -> bool {
        // TODO: Delete a key from the trie
        // Find the key and mark is_end as false
        // Optionally remove nodes with no children
        // Return true if key was found and deleted
        todo!()
    }

    fn dfs_collect(&self, node: &TrieNode<V>, prefix: String, results: &mut Vec<(String, V)>) {
        // TODO: Helper function for get_all_with_prefix
        // Recursively collect all complete words from this node
        // Add current prefix to results if node.is_end is true
        // Recurse on all children
        todo!()
    }

    pub fn len(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    pub fn contains(&self, key: &str) -> bool {
        self.search(key).is_some()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_trie() {
        let trie: Trie<i32> = Trie::new();
        assert_eq!(trie.len(), 0);
        assert!(trie.is_empty());
    }

    #[test]
    fn test_insert_and_search() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);
        trie.insert("world", 2);

        assert_eq!(trie.search("hello"), Some(&1));
        assert_eq!(trie.search("world"), Some(&2));
        assert_eq!(trie.search("hell"), None);
    }

    #[test]
    fn test_prefix_search() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);
        trie.insert("hell", 2);
        trie.insert("heaven", 3);

        assert!(trie.starts_with("hel"));
        assert!(trie.starts_with("hell"));
        assert!(trie.starts_with("hello"));
        assert!(trie.starts_with("heav"));
        assert!(!trie.starts_with("world"));
    }

    #[test]
    fn test_get_all_with_prefix() {
        let mut trie = Trie::new();
        trie.insert("cat", 1);
        trie.insert("car", 2);
        trie.insert("card", 3);
        trie.insert("dog", 4);

        let results = trie.get_all_with_prefix("car");
        assert_eq!(results.len(), 2);
        assert!(results.iter().any(|(k, v)| k == "car" && *v == 2));
        assert!(results.iter().any(|(k, v)| k == "card" && *v == 3));
    }

    #[test]
    fn test_empty_prefix() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);
        trie.insert("world", 2);

        let results = trie.get_all_with_prefix("");
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_delete() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);
        trie.insert("hell", 2);

        assert!(trie.delete("hello"));
        assert_eq!(trie.search("hello"), None);
        assert_eq!(trie.search("hell"), Some(&2));
    }

    #[test]
    fn test_delete_nonexistent() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);

        assert!(!trie.delete("world"));
        assert_eq!(trie.len(), 1);
    }

    #[test]
    fn test_shared_prefix() {
        let mut trie = Trie::new();
        trie.insert("test", 1);
        trie.insert("testing", 2);
        trie.insert("tester", 3);

        assert_eq!(trie.search("test"), Some(&1));
        assert_eq!(trie.search("testing"), Some(&2));
        assert_eq!(trie.search("tester"), Some(&3));
        assert!(trie.starts_with("test"));
    }

    #[test]
    fn test_contains() {
        let mut trie = Trie::new();
        trie.insert("hello", 1);

        assert!(trie.contains("hello"));
        assert!(!trie.contains("hell"));
        assert!(!trie.contains("helloworld"));
    }

    #[test]
    fn test_update_value() {
        let mut trie = Trie::new();
        trie.insert("key", 1);
        trie.insert("key", 2);

        assert_eq!(trie.search("key"), Some(&2));
        assert_eq!(trie.len(), 1);
    }

    #[test]
    fn test_long_strings() {
        let mut trie = Trie::new();
        let long_key = "a".repeat(100);

        trie.insert(&long_key, 42);
        assert_eq!(trie.search(&long_key), Some(&42));
        assert!(trie.starts_with(&"a".repeat(50)));
    }

    #[test]
    fn test_autocomplete_scenario() {
        let mut trie = Trie::new();
        trie.insert("apple", 1);
        trie.insert("application", 2);
        trie.insert("apply", 3);
        trie.insert("banana", 4);

        let suggestions = trie.get_all_with_prefix("app");
        assert_eq!(suggestions.len(), 3);

        let banana_suggestions = trie.get_all_with_prefix("ban");
        assert_eq!(banana_suggestions.len(), 1);
    }

    #[test]
    fn test_single_character_keys() {
        let mut trie = Trie::new();
        trie.insert("a", 1);
        trie.insert("b", 2);
        trie.insert("c", 3);

        assert_eq!(trie.search("a"), Some(&1));
        assert_eq!(trie.search("b"), Some(&2));
        assert_eq!(trie.search("c"), Some(&3));
    }
}
