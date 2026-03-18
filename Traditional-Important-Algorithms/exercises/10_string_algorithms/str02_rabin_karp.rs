// str02_rabin_karp.rs
//
// Rabin-Karp String Matching Algorithm
//
// Rabin-Karp uses rolling hash to efficiently search for patterns in text.
// It's particularly effective for multiple pattern matching.
//
// Time Complexity: O(n + m) average case, O(nm) worst case
// Space Complexity: O(1)
//
// Key concepts:
// - Rolling hash: Update hash in O(1) by removing leftmost char and adding new char
// - Hash collision: When hashes match, verify with actual string comparison
// - Base and modulo: Choose prime modulo to minimize collisions
// - Can easily extend to multiple pattern matching
//
// Your task: Implement Rabin-Karp with rolling hash function.

// I AM NOT DONE

const BASE: u64 = 256;
const MODULO: u64 = 1_000_000_007;

pub struct RabinKarp {
    pattern: String,
    pattern_hash: u64,
    pattern_len: usize,
    base_power: u64, // BASE^(m-1) mod MODULO, for rolling hash
}

impl RabinKarp {
    pub fn new(pattern: String) -> Self {
        let pattern_len = pattern.len();
        let pattern_hash = Self::compute_hash(&pattern);
        let base_power = Self::compute_base_power(pattern_len);

        Self {
            pattern,
            pattern_hash,
            pattern_len,
            base_power,
        }
    }

    fn compute_hash(s: &str) -> u64 {
        // TODO: Compute hash of string
        // - hash = (s[0] * BASE^(n-1) + s[1] * BASE^(n-2) + ... + s[n-1]) mod MODULO
        // - Use Horner's method: hash = ((s[0] * BASE + s[1]) * BASE + s[2]) * BASE ...
        // - Take modulo at each step to prevent overflow
        todo!()
    }

    fn compute_base_power(pattern_len: usize) -> u64 {
        // TODO: Compute BASE^(pattern_len-1) mod MODULO
        // - This is used for rolling hash to remove leftmost character
        // - Use modular exponentiation or iterative multiplication with modulo
        todo!()
    }

    fn rolling_hash(&self, old_hash: u64, old_char: u8, new_char: u8) -> u64 {
        // TODO: Update hash by removing old_char and adding new_char
        // - Remove old_char: subtract (old_char * base_power) mod MODULO
        // - Shift: multiply by BASE
        // - Add new_char: add new_char
        // - Take modulo at each step
        // - Handle potential underflow when subtracting (add MODULO if needed)
        todo!()
    }

    pub fn search(&self, text: &str) -> Vec<usize> {
        // TODO: Find all occurrences using rolling hash
        // - Compute initial hash of text[0..pattern_len]
        // - For each position, compare hash with pattern_hash
        // - If hashes match, verify with actual string comparison (handle collisions)
        // - Update hash using rolling_hash for next window
        // - Return all match positions
        todo!()
    }

    pub fn contains(&self, text: &str) -> bool {
        // TODO: Check if pattern exists in text
        todo!()
    }

    pub fn first_occurrence(&self, text: &str) -> Option<usize> {
        // TODO: Return position of first match
        todo!()
    }
}

pub struct MultiPatternRabinKarp {
    patterns: Vec<String>,
    pattern_hashes: Vec<u64>,
    pattern_len: usize,
    base_power: u64,
}

impl MultiPatternRabinKarp {
    pub fn new(patterns: Vec<String>) -> Option<Self> {
        // TODO: Initialize for multiple patterns of same length
        // - All patterns must have same length
        // - Compute hash for each pattern
        // - Store in a HashSet for O(1) lookup
        // - Return None if patterns have different lengths
        todo!()
    }

    pub fn search(&self, text: &str) -> Vec<(usize, usize)> {
        // TODO: Find all occurrences of any pattern
        // - Return Vec of (position, pattern_index) tuples
        // - Use rolling hash for text window
        // - Check if window hash matches any pattern hash
        // - Verify actual match on hash collision
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_hash() {
        let rk = RabinKarp::new("ABC".to_string());
        assert!(rk.pattern_hash > 0);

        // Same string should have same hash
        let rk2 = RabinKarp::new("ABC".to_string());
        assert_eq!(rk.pattern_hash, rk2.pattern_hash);
    }

    #[test]
    fn test_simple_match() {
        let rk = RabinKarp::new("test".to_string());
        let positions = rk.search("this is a test string");
        assert_eq!(positions, vec![10]);
    }

    #[test]
    fn test_multiple_matches() {
        let rk = RabinKarp::new("ab".to_string());
        let positions = rk.search("ababab");
        assert_eq!(positions, vec![0, 2, 4]);
    }

    #[test]
    fn test_overlapping_matches() {
        let rk = RabinKarp::new("aaa".to_string());
        let positions = rk.search("aaaaa");
        assert_eq!(positions, vec![0, 1, 2]);
    }

    #[test]
    fn test_no_match() {
        let rk = RabinKarp::new("xyz".to_string());
        let positions = rk.search("abcdef");
        assert_eq!(positions, vec![]);
    }

    #[test]
    fn test_contains() {
        let rk = RabinKarp::new("world".to_string());
        assert!(rk.contains("hello world"));
        assert!(!rk.contains("hello earth"));
    }

    #[test]
    fn test_first_occurrence() {
        let rk = RabinKarp::new("pattern".to_string());
        assert_eq!(rk.first_occurrence("find the pattern here"), Some(9));
        assert_eq!(rk.first_occurrence("no match"), None);
    }

    #[test]
    fn test_pattern_at_boundaries() {
        let rk = RabinKarp::new("hello".to_string());
        assert_eq!(rk.search("hello world"), vec![0]);
        assert_eq!(rk.search("world hello"), vec![6]);
        assert_eq!(rk.search("hello"), vec![0]);
    }

    #[test]
    fn test_single_character() {
        let rk = RabinKarp::new("x".to_string());
        let positions = rk.search("axbxcxd");
        assert_eq!(positions, vec![1, 3, 5]);
    }

    #[test]
    fn test_longer_pattern() {
        let rk = RabinKarp::new("abracadabra".to_string());
        let positions = rk.search("abracadabra appears once");
        assert_eq!(positions, vec![0]);
    }

    #[test]
    fn test_multi_pattern_same_length() {
        let patterns = vec!["cat".to_string(), "dog".to_string(), "fox".to_string()];
        let mp = MultiPatternRabinKarp::new(patterns);
        assert!(mp.is_some());

        let mp = mp.unwrap();
        let matches = mp.search("the cat and dog chase the fox");
        assert!(matches.contains(&(4, 0))); // "cat" at position 4
        assert!(matches.contains(&(12, 1))); // "dog" at position 12
        assert!(matches.contains(&(26, 2))); // "fox" at position 26
    }

    #[test]
    fn test_multi_pattern_different_lengths() {
        let patterns = vec!["cat".to_string(), "dogs".to_string()];
        let mp = MultiPatternRabinKarp::new(patterns);
        assert!(mp.is_none()); // Should return None for different length patterns
    }
}
