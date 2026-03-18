// str03_boyer_moore.rs
//
// Boyer-Moore String Matching Algorithm
//
// Boyer-Moore is one of the most efficient string matching algorithms,
// scanning the pattern from right to left and using two heuristics to skip sections.
//
// Time Complexity: O(n/m) best case, O(nm) worst case, O(n) typical
// Space Complexity: O(m + σ) where σ is alphabet size
//
// Key concepts:
// - Bad character rule: Skip based on rightmost occurrence of mismatched character
// - Good suffix rule: Skip based on matching suffix pattern
// - Scan pattern from right to left
// - Can skip multiple characters per iteration
// - Sublinear time complexity in practice
//
// Your task: Implement Boyer-Moore with bad character and good suffix rules.

// I AM NOT DONE

use std::collections::HashMap;

pub struct BoyerMoore {
    pattern: String,
    pattern_bytes: Vec<u8>,
    bad_char: HashMap<u8, i32>,
    good_suffix: Vec<usize>,
}

impl BoyerMoore {
    pub fn new(pattern: String) -> Self {
        let pattern_bytes: Vec<u8> = pattern.bytes().collect();
        let bad_char = Self::compute_bad_char_table(&pattern_bytes);
        let good_suffix = Self::compute_good_suffix_table(&pattern_bytes);

        Self {
            pattern,
            pattern_bytes,
            bad_char,
            good_suffix,
        }
    }

    fn compute_bad_char_table(pattern: &[u8]) -> HashMap<u8, i32> {
        // TODO: Build bad character table
        // - For each character, store its rightmost position in pattern
        // - Position is from right: pattern[m-1] is at position 0
        // - If character not in pattern, it will be missing from HashMap
        // - Use i32 to allow -1 for characters not in pattern
        todo!()
    }

    fn compute_good_suffix_table(pattern: &[u8]) -> Vec<usize> {
        // TODO: Build good suffix table
        // - good_suffix[i] = shift distance when mismatch occurs at position i
        // - Consider two cases:
        //   1. Suffix pattern[i+1..] appears elsewhere in pattern
        //   2. A prefix of pattern matches a suffix of pattern[i+1..]
        // - This is complex; simplified version acceptable
        // - Return vector of length pattern.len()
        todo!()
    }

    pub fn search(&self, text: &str) -> Vec<usize> {
        // TODO: Search using Boyer-Moore algorithm
        // - Scan pattern from right to left (high index to low)
        // - On mismatch, use both bad character and good suffix rules
        // - Shift by maximum of the two rules
        // - On complete match, record position and continue searching
        // - Return all match positions
        todo!()
    }

    fn bad_char_shift(&self, char: u8, position: usize) -> usize {
        // TODO: Calculate shift based on bad character rule
        // - If char exists in pattern, shift so that rightmost occurrence aligns
        // - If char doesn't exist, shift by entire pattern length
        // - position is where mismatch occurred in pattern
        todo!()
    }

    fn good_suffix_shift(&self, position: usize) -> usize {
        // TODO: Calculate shift based on good suffix rule
        // - Use precomputed good_suffix table
        // - Return shift amount for given mismatch position
        todo!()
    }

    pub fn contains(&self, text: &str) -> bool {
        // TODO: Check if pattern exists in text
        todo!()
    }

    pub fn first_occurrence(&self, text: &str) -> Option<usize> {
        // TODO: Return first match position
        todo!()
    }

    pub fn get_bad_char_table(&self) -> &HashMap<u8, i32> {
        &self.bad_char
    }

    pub fn get_good_suffix_table(&self) -> &[usize] {
        &self.good_suffix
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bad_char_table() {
        let bm = BoyerMoore::new("EXAMPLE".to_string());
        let table = bm.get_bad_char_table();

        // 'E' appears at positions 0 and 6 (rightmost is 6)
        assert!(table.contains_key(&b'E'));
        assert!(table.contains_key(&b'X'));
        assert!(table.contains_key(&b'A'));
    }

    #[test]
    fn test_simple_match() {
        let bm = BoyerMoore::new("pattern".to_string());
        let positions = bm.search("find the pattern here");
        assert_eq!(positions, vec![9]);
    }

    #[test]
    fn test_multiple_matches() {
        let bm = BoyerMoore::new("ab".to_string());
        let positions = bm.search("ababab");
        assert_eq!(positions, vec![0, 2, 4]);
    }

    #[test]
    fn test_no_match() {
        let bm = BoyerMoore::new("xyz".to_string());
        let positions = bm.search("abcdef");
        assert_eq!(positions, vec![]);
    }

    #[test]
    fn test_contains() {
        let bm = BoyerMoore::new("world".to_string());
        assert!(bm.contains("hello world"));
        assert!(!bm.contains("hello earth"));
    }

    #[test]
    fn test_first_occurrence() {
        let bm = BoyerMoore::new("test".to_string());
        assert_eq!(bm.first_occurrence("this is a test string"), Some(10));
        assert_eq!(bm.first_occurrence("no match"), None);
    }

    #[test]
    fn test_pattern_at_end() {
        let bm = BoyerMoore::new("end".to_string());
        assert_eq!(bm.search("this is the end"), vec![12]);
    }

    #[test]
    fn test_pattern_at_start() {
        let bm = BoyerMoore::new("start".to_string());
        assert_eq!(bm.search("start of text"), vec![0]);
    }

    #[test]
    fn test_overlapping_pattern() {
        let bm = BoyerMoore::new("aaa".to_string());
        let positions = bm.search("aaaaa");
        assert_eq!(positions, vec![0, 1, 2]);
    }

    #[test]
    fn test_single_character() {
        let bm = BoyerMoore::new("x".to_string());
        let positions = bm.search("axbxcxd");
        assert_eq!(positions, vec![1, 3, 5]);
    }

    #[test]
    fn test_repeated_characters() {
        let bm = BoyerMoore::new("aaa".to_string());
        assert_eq!(bm.search("aaaaaa"), vec![0, 1, 2, 3]);
    }

    #[test]
    fn test_longer_pattern_than_text() {
        let bm = BoyerMoore::new("verylongpattern".to_string());
        assert_eq!(bm.search("short"), vec![]);
    }
}
