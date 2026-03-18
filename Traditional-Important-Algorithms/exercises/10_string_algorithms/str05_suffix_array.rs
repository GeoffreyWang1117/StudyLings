// str05_suffix_array.rs
//
// Suffix Array Construction
//
// A suffix array is a sorted array of all suffixes of a string. It's a space-efficient
// alternative to suffix trees and enables fast pattern matching and other string operations.
//
// Time Complexity: O(n log n) with efficient construction, O(n²log n) naive
// Space Complexity: O(n)
//
// Key concepts:
// - Suffix array: Array of starting positions of suffixes in sorted order
// - LCP array: Longest Common Prefix between consecutive suffixes
// - Pattern matching: Binary search on suffix array in O(m log n)
// - Can answer many string queries efficiently
// - Building block for Burrows-Wheeler transform
//
// Your task: Implement suffix array construction with LCP array.

// I AM NOT DONE

pub struct SuffixArray {
    text: String,
    suffix_array: Vec<usize>,
    lcp: Vec<usize>,
}

impl SuffixArray {
    pub fn new(text: String) -> Self {
        let suffix_array = Self::build_suffix_array(&text);
        let lcp = Self::build_lcp_array(&text, &suffix_array);

        Self {
            text,
            suffix_array,
            lcp,
        }
    }

    fn build_suffix_array(text: &str) -> Vec<usize> {
        // TODO: Build suffix array
        // Naive approach (acceptable):
        // - Create vector of (suffix_string, index) pairs
        // - Sort by suffix_string
        // - Extract indices
        //
        // Advanced approach (bonus):
        // - Use prefix doubling or DC3 algorithm for O(n log n)
        // - Sort by first k characters, then use previous sort for next k
        todo!()
    }

    fn build_lcp_array(text: &str, suffix_array: &[usize]) -> Vec<usize> {
        // TODO: Build LCP (Longest Common Prefix) array
        // - lcp[i] = length of longest common prefix between
        //   suffix_array[i] and suffix_array[i+1]
        // - lcp[0] = 0 by convention
        // - Can use Kasai's algorithm for O(n) construction
        // - Simple approach: compare suffixes character by character
        todo!()
    }

    pub fn search(&self, pattern: &str) -> Vec<usize> {
        // TODO: Find all occurrences of pattern
        // - Use binary search to find range in suffix array where pattern matches
        // - All suffixes in this range start with the pattern
        // - Return the original indices (values in suffix_array)
        // - Time: O(m log n) where m is pattern length
        todo!()
    }

    pub fn contains(&self, pattern: &str) -> bool {
        // TODO: Check if pattern exists
        todo!()
    }

    pub fn count_occurrences(&self, pattern: &str) -> usize {
        // TODO: Count occurrences of pattern
        todo!()
    }

    pub fn longest_repeated_substring(&self) -> Option<String> {
        // TODO: Find longest substring that appears at least twice
        // - This is the maximum value in the LCP array
        // - Extract substring from text using LCP value and suffix position
        // - Return None if no repeated substring
        todo!()
    }

    pub fn longest_common_substring(&self, other: &str) -> Option<String> {
        // TODO: Find longest common substring with another string
        // - Concatenate text + separator + other
        // - Build suffix array for combined string
        // - Find maximum LCP where suffixes come from different strings
        // - This is a bonus challenge - simplified version acceptable
        todo!()
    }

    pub fn get_suffix_array(&self) -> &[usize] {
        &self.suffix_array
    }

    pub fn get_lcp_array(&self) -> &[usize] {
        &self.lcp
    }

    pub fn get_suffix(&self, index: usize) -> &str {
        if index >= self.suffix_array.len() {
            return "";
        }
        let start = self.suffix_array[index];
        &self.text[start..]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_suffix_array() {
        let sa = SuffixArray::new("banana".to_string());
        let arr = sa.get_suffix_array();

        // Suffixes in sorted order: "a", "ana", "anana", "banana", "na", "nana"
        // Starting positions:        5,    3,      1,        0,      4,     2
        assert_eq!(arr, &[5, 3, 1, 0, 4, 2]);
    }

    #[test]
    fn test_lcp_array() {
        let sa = SuffixArray::new("banana".to_string());
        let lcp = sa.get_lcp_array();

        // LCP between consecutive sorted suffixes
        // "a" vs "ana" = 1
        // "ana" vs "anana" = 3
        // "anana" vs "banana" = 0
        // "banana" vs "na" = 0
        // "na" vs "nana" = 2
        assert_eq!(lcp, &[0, 1, 3, 0, 0, 2]);
    }

    #[test]
    fn test_search_pattern() {
        let sa = SuffixArray::new("banana".to_string());
        let positions = sa.search("ana");

        // "ana" appears at positions 1 and 3
        assert_eq!(positions.len(), 2);
        assert!(positions.contains(&1));
        assert!(positions.contains(&3));
    }

    #[test]
    fn test_contains() {
        let sa = SuffixArray::new("hello world".to_string());
        assert!(sa.contains("world"));
        assert!(sa.contains("ello"));
        assert!(!sa.contains("xyz"));
    }

    #[test]
    fn test_count_occurrences() {
        let sa = SuffixArray::new("abababa".to_string());
        assert_eq!(sa.count_occurrences("aba"), 3);
        assert_eq!(sa.count_occurrences("ab"), 3);
        assert_eq!(sa.count_occurrences("ba"), 3);
    }

    #[test]
    fn test_longest_repeated_substring() {
        let sa = SuffixArray::new("banana".to_string());
        let lrs = sa.longest_repeated_substring();

        assert!(lrs.is_some());
        let lrs = lrs.unwrap();
        assert_eq!(lrs, "ana"); // "ana" is longest repeated substring
    }

    #[test]
    fn test_no_repeated_substring() {
        let sa = SuffixArray::new("abcdef".to_string());
        let lrs = sa.longest_repeated_substring();

        assert!(lrs.is_none() || lrs.unwrap().is_empty());
    }

    #[test]
    fn test_get_suffix() {
        let sa = SuffixArray::new("hello".to_string());

        // First suffix in sorted order should be shortest
        let first_suffix = sa.get_suffix(0);
        assert!(first_suffix.len() <= "hello".len());
    }

    #[test]
    fn test_single_character() {
        let sa = SuffixArray::new("a".to_string());
        assert_eq!(sa.get_suffix_array(), &[0]);
        assert_eq!(sa.get_lcp_array(), &[0]);
    }

    #[test]
    fn test_repeated_characters() {
        let sa = SuffixArray::new("aaaa".to_string());
        assert!(sa.contains("aa"));
        assert_eq!(sa.count_occurrences("aa"), 3);
    }

    #[test]
    fn test_pattern_not_found() {
        let sa = SuffixArray::new("abcdef".to_string());
        assert_eq!(sa.search("xyz"), vec![]);
        assert_eq!(sa.count_occurrences("xyz"), 0);
    }

    #[test]
    fn test_full_string_search() {
        let sa = SuffixArray::new("test".to_string());
        let positions = sa.search("test");
        assert_eq!(positions, vec![0]);
    }
}
