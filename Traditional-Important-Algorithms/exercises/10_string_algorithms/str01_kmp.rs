// str01_kmp.rs
//
// Knuth-Morris-Pratt (KMP) String Matching Algorithm
//
// KMP is an efficient string matching algorithm that avoids re-examining
// previously matched characters by using a failure function (prefix table).
//
// Time Complexity: O(n + m) where n is text length, m is pattern length
// Space Complexity: O(m) for the failure function
//
// Key concepts:
// - Failure function (LPS array): Longest Proper Prefix which is also Suffix
// - No backtracking in the text - we only backtrack in the pattern
// - Preprocessing the pattern allows linear time matching
//
// Your task: Implement the KMP string matching algorithm with failure function.

// I AM NOT DONE

pub struct KMP {
    pattern: String,
    failure: Vec<usize>,
}

impl KMP {
    pub fn new(pattern: String) -> Self {
        let failure = Self::compute_failure(&pattern);
        Self { pattern, failure }
    }

    fn compute_failure(pattern: &str) -> Vec<usize> {
        // TODO: Compute the failure function (LPS array)
        // - failure[i] = length of longest proper prefix of pattern[0..=i]
        //   that is also a suffix of pattern[0..=i]
        // - Start with failure[0] = 0
        // - Use two pointers: len (length of previous LPS) and i (current position)
        // - If pattern[i] == pattern[len], then failure[i] = len + 1
        // - Otherwise, backtrack using failure[len-1] until match or len = 0
        todo!()
    }

    pub fn search(&self, text: &str) -> Vec<usize> {
        // TODO: Find all occurrences of pattern in text
        // - Use two pointers: i for text, j for pattern
        // - When mismatch occurs, use failure function to determine next j
        // - j = failure[j-1] instead of resetting to 0
        // - When j reaches pattern length, record match position
        // - Return vector of starting positions of all matches
        todo!()
    }

    pub fn contains(&self, text: &str) -> bool {
        // TODO: Check if pattern appears in text (return early on first match)
        todo!()
    }

    pub fn first_occurrence(&self, text: &str) -> Option<usize> {
        // TODO: Return position of first occurrence, or None
        todo!()
    }

    pub fn count_occurrences(&self, text: &str) -> usize {
        // TODO: Count total number of occurrences (including overlapping)
        todo!()
    }

    pub fn get_failure_function(&self) -> &[usize] {
        &self.failure
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_failure_function_simple() {
        let kmp = KMP::new("ABABC".to_string());
        assert_eq!(kmp.get_failure_function(), &[0, 0, 1, 2, 0]);
    }

    #[test]
    fn test_failure_function_repeated() {
        let kmp = KMP::new("AAAA".to_string());
        assert_eq!(kmp.get_failure_function(), &[0, 1, 2, 3]);
    }

    #[test]
    fn test_failure_function_complex() {
        let kmp = KMP::new("AABAACAABAA".to_string());
        assert_eq!(kmp.get_failure_function(), &[0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_simple_match() {
        let kmp = KMP::new("ABC".to_string());
        let positions = kmp.search("XYZABCDEF");
        assert_eq!(positions, vec![3]);
    }

    #[test]
    fn test_multiple_matches() {
        let kmp = KMP::new("AB".to_string());
        let positions = kmp.search("ABABAB");
        assert_eq!(positions, vec![0, 2, 4]);
    }

    #[test]
    fn test_overlapping_matches() {
        let kmp = KMP::new("AAA".to_string());
        let positions = kmp.search("AAAAA");
        assert_eq!(positions, vec![0, 1, 2]);
    }

    #[test]
    fn test_no_match() {
        let kmp = KMP::new("XYZ".to_string());
        let positions = kmp.search("ABCDEF");
        assert_eq!(positions, vec![]);
    }

    #[test]
    fn test_contains() {
        let kmp = KMP::new("world".to_string());
        assert!(kmp.contains("hello world"));
        assert!(!kmp.contains("hello earth"));
    }

    #[test]
    fn test_first_occurrence() {
        let kmp = KMP::new("test".to_string());
        assert_eq!(kmp.first_occurrence("this is a test string"), Some(10));
        assert_eq!(kmp.first_occurrence("no match here"), None);
    }

    #[test]
    fn test_count_occurrences() {
        let kmp = KMP::new("ana".to_string());
        assert_eq!(kmp.count_occurrences("banana"), 2);
        assert_eq!(kmp.count_occurrences("ananana"), 3);
    }

    #[test]
    fn test_pattern_longer_than_text() {
        let kmp = KMP::new("longpattern".to_string());
        assert_eq!(kmp.search("short"), vec![]);
    }

    #[test]
    fn test_single_character() {
        let kmp = KMP::new("a".to_string());
        let positions = kmp.search("aaaaaa");
        assert_eq!(positions, vec![0, 1, 2, 3, 4, 5]);
    }
}
