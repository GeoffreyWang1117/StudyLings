// str04_aho_corasick.rs
//
// Aho-Corasick Multi-Pattern String Matching Algorithm
//
// Aho-Corasick efficiently searches for multiple patterns simultaneously using
// a trie with failure links (similar to KMP for multiple patterns).
//
// Time Complexity: O(n + m + z) where n=text length, m=total pattern length, z=matches
// Space Complexity: O(m × σ) where σ is alphabet size
//
// Key concepts:
// - Trie structure: Build trie of all patterns
// - Failure links: Like KMP failure function, for fallback on mismatch
// - Output links: Direct links to all matching patterns at current state
// - Single pass through text matches all patterns simultaneously
// - Used in tools like grep, antivirus scanners
//
// Your task: Implement Aho-Corasick automaton with trie and failure links.

// I AM NOT DONE

use std::collections::{HashMap, VecDeque, HashSet};

#[derive(Debug, Clone)]
struct TrieNode {
    children: HashMap<char, usize>,
    failure_link: Option<usize>,
    output: Vec<usize>, // Indices of patterns that end at this node
}

impl TrieNode {
    fn new() -> Self {
        Self {
            children: HashMap::new(),
            failure_link: None,
            output: Vec::new(),
        }
    }
}

pub struct AhoCorasick {
    nodes: Vec<TrieNode>,
    patterns: Vec<String>,
}

impl AhoCorasick {
    pub fn new(patterns: Vec<String>) -> Self {
        let mut ac = Self {
            nodes: vec![TrieNode::new()],
            patterns: patterns.clone(),
        };

        ac.build_trie(&patterns);
        ac.build_failure_links();
        ac
    }

    fn build_trie(&mut self, patterns: &[String]) {
        // TODO: Build trie from patterns
        // - Start from root (node 0)
        // - For each pattern, insert characters one by one
        // - Create new nodes as needed
        // - Mark pattern end by adding pattern index to output vector
        todo!()
    }

    fn build_failure_links(&mut self) {
        // TODO: Build failure links using BFS
        // - Root's failure link is None (or points to itself conceptually)
        // - For each node at depth 1, failure link points to root
        // - For deeper nodes:
        //   - Follow parent's failure link
        //   - Find longest proper suffix that's a prefix of another pattern
        // - Use BFS to process level by level
        // - Also build output links (copy outputs from failure link target)
        todo!()
    }

    pub fn search(&self, text: &str) -> Vec<(usize, usize)> {
        // TODO: Search for all patterns in text
        // - Start at root (node 0)
        // - For each character in text:
        //   - Try to follow edge for that character
        //   - If no edge, follow failure links until edge found or at root
        //   - Check output at current node for matches
        // - Return Vec of (position, pattern_index) for all matches
        // - Position is where pattern ends in text
        todo!()
    }

    pub fn search_with_positions(&self, text: &str) -> Vec<Match> {
        // TODO: Search returning Match structs with start positions
        // - Similar to search() but calculate start position
        // - start = end - pattern.len() + 1
        todo!()
    }

    pub fn contains_any(&self, text: &str) -> bool {
        // TODO: Check if any pattern appears in text
        todo!()
    }

    pub fn count_matches(&self, text: &str) -> usize {
        // TODO: Count total number of pattern occurrences
        todo!()
    }

    pub fn get_patterns(&self) -> &[String] {
        &self.patterns
    }

    pub fn node_count(&self) -> usize {
        self.nodes.len()
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Match {
    pub pattern_index: usize,
    pub start: usize,
    pub end: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_pattern() {
        let patterns = vec!["hello".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("hello world");
        assert_eq!(matches.len(), 1);
        assert_eq!(matches[0], (4, 0)); // "hello" ends at position 4, pattern index 0
    }

    #[test]
    fn test_multiple_patterns() {
        let patterns = vec!["he".to_string(), "she".to_string(), "his".to_string(), "hers".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("ushers");
        // Should find "she" and "he" and "hers"
        assert!(matches.len() >= 2);
    }

    #[test]
    fn test_overlapping_patterns() {
        let patterns = vec!["abc".to_string(), "bcd".to_string(), "cde".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("abcde");
        assert_eq!(matches.len(), 3); // All three patterns should be found
    }

    #[test]
    fn test_no_matches() {
        let patterns = vec!["foo".to_string(), "bar".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("hello world");
        assert_eq!(matches.len(), 0);
    }

    #[test]
    fn test_contains_any() {
        let patterns = vec!["apple".to_string(), "banana".to_string(), "cherry".to_string()];
        let ac = AhoCorasick::new(patterns);

        assert!(ac.contains_any("I like bananas"));
        assert!(!ac.contains_any("I like oranges"));
    }

    #[test]
    fn test_repeated_pattern() {
        let patterns = vec!["ab".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("ababab");
        assert_eq!(matches.len(), 3); // "ab" at positions 1, 3, 5
    }

    #[test]
    fn test_count_matches() {
        let patterns = vec!["a".to_string(), "aa".to_string()];
        let ac = AhoCorasick::new(patterns);

        let count = ac.count_matches("aaaa");
        assert!(count >= 4); // At least 4 "a" matches
    }

    #[test]
    fn test_search_with_positions() {
        let patterns = vec!["test".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search_with_positions("this is a test");
        assert_eq!(matches.len(), 1);
        assert_eq!(matches[0].start, 10);
        assert_eq!(matches[0].end, 13);
        assert_eq!(matches[0].pattern_index, 0);
    }

    #[test]
    fn test_prefix_patterns() {
        let patterns = vec!["a".to_string(), "ab".to_string(), "abc".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("abc");
        assert_eq!(matches.len(), 3); // All three patterns match
    }

    #[test]
    fn test_trie_structure() {
        let patterns = vec!["abc".to_string(), "abd".to_string()];
        let ac = AhoCorasick::new(patterns);

        // Trie should share "ab" prefix
        // Should have: root, 'a', 'b', 'c', 'd' = 5 nodes minimum
        assert!(ac.node_count() >= 5);
    }

    #[test]
    fn test_single_character_patterns() {
        let patterns = vec!["a".to_string(), "b".to_string(), "c".to_string()];
        let ac = AhoCorasick::new(patterns);

        let matches = ac.search("abcabc");
        assert_eq!(matches.len(), 6); // 2 of each character
    }

    #[test]
    fn test_case_sensitive() {
        let patterns = vec!["Hello".to_string()];
        let ac = AhoCorasick::new(patterns);

        assert!(ac.contains_any("Hello world"));
        assert!(!ac.contains_any("hello world")); // Case sensitive
    }
}
