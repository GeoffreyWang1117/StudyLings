// str06_levenshtein.rs
//
// Levenshtein Distance (Edit Distance)
//
// Levenshtein distance measures the minimum number of single-character edits
// (insertions, deletions, substitutions) needed to transform one string into another.
//
// Time Complexity: O(mn) where m, n are string lengths
// Space Complexity: O(mn) or O(min(m,n)) with optimization
//
// Key concepts:
// - Dynamic programming solution
// - Three operations: insert, delete, substitute
// - Can track the actual edit sequence (alignment)
// - Used in spell checkers, DNA sequence alignment, diff tools
// - Can be optimized to O(min(m,n)) space
//
// Your task: Implement Levenshtein distance with edit sequence tracking.

// I AM NOT DONE

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EditOperation {
    Insert(char),
    Delete(char),
    Substitute(char, char),
    Match(char),
}

pub struct Levenshtein;

impl Levenshtein {
    pub fn distance(source: &str, target: &str) -> usize {
        // TODO: Compute Levenshtein distance
        // - Use dynamic programming with 2D table
        // - dp[i][j] = min edit distance between source[0..i] and target[0..j]
        // - Base cases: dp[0][j] = j, dp[i][0] = i
        // - Recurrence:
        //   if source[i-1] == target[j-1]:
        //     dp[i][j] = dp[i-1][j-1]
        //   else:
        //     dp[i][j] = 1 + min(dp[i-1][j],      // delete
        //                       dp[i][j-1],        // insert
        //                       dp[i-1][j-1])      // substitute
        todo!()
    }

    pub fn distance_with_ops(source: &str, target: &str) -> (usize, Vec<EditOperation>) {
        // TODO: Compute distance and track edit operations
        // - Build DP table as above
        // - Backtrack from dp[m][n] to dp[0][0] to reconstruct operations
        // - Return (distance, operations)
        todo!()
    }

    pub fn similarity(source: &str, target: &str) -> f64 {
        // TODO: Compute similarity ratio (0.0 to 1.0)
        // - similarity = 1.0 - (distance / max_length)
        // - Or use: similarity = (max_length - distance) / max_length
        // - Return 1.0 for identical strings, 0.0 for completely different
        todo!()
    }

    pub fn is_within_distance(source: &str, target: &str, max_distance: usize) -> bool {
        // TODO: Check if distance is within threshold
        // - Can optimize by early termination if distance exceeds threshold
        // - Useful for fuzzy matching
        todo!()
    }
}

pub struct LevenshteinOptimized;

impl LevenshteinOptimized {
    pub fn distance(source: &str, target: &str) -> usize {
        // TODO: Space-optimized version using O(min(m,n)) space
        // - Use only two rows instead of full 2D table
        // - Alternate between current and previous row
        // - Make source the shorter string for space optimization
        todo!()
    }
}

pub struct DamerauLevenshtein;

impl DamerauLevenshtein {
    pub fn distance(source: &str, target: &str) -> usize {
        // TODO: Damerau-Levenshtein distance (bonus)
        // - Extends Levenshtein to include transpositions
        // - Transposition: swapping two adjacent characters
        // - Example: "ab" -> "ba" is distance 1 (not 2)
        // - Requires more complex DP with additional state
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_identical_strings() {
        assert_eq!(Levenshtein::distance("hello", "hello"), 0);
        assert_eq!(Levenshtein::distance("", ""), 0);
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(Levenshtein::distance("", "hello"), 5);
        assert_eq!(Levenshtein::distance("hello", ""), 5);
    }

    #[test]
    fn test_single_substitution() {
        assert_eq!(Levenshtein::distance("kitten", "sitten"), 1);
        assert_eq!(Levenshtein::distance("hello", "hallo"), 1);
    }

    #[test]
    fn test_single_insertion() {
        assert_eq!(Levenshtein::distance("cat", "cats"), 1);
        assert_eq!(Levenshtein::distance("tet", "test"), 1);
    }

    #[test]
    fn test_single_deletion() {
        assert_eq!(Levenshtein::distance("cats", "cat"), 1);
        assert_eq!(Levenshtein::distance("test", "tet"), 1);
    }

    #[test]
    fn test_multiple_operations() {
        assert_eq!(Levenshtein::distance("kitten", "sitting"), 3);
        // k->s (substitute), e->i (substitute), insert g
        assert_eq!(Levenshtein::distance("saturday", "sunday"), 3);
    }

    #[test]
    fn test_completely_different() {
        assert_eq!(Levenshtein::distance("abc", "xyz"), 3);
    }

    #[test]
    fn test_similarity() {
        assert_eq!(Levenshtein::similarity("hello", "hello"), 1.0);
        assert!(Levenshtein::similarity("hello", "hallo") > 0.8);
        assert!(Levenshtein::similarity("abc", "xyz") < 0.1);
    }

    #[test]
    fn test_is_within_distance() {
        assert!(Levenshtein::is_within_distance("hello", "hallo", 1));
        assert!(!Levenshtein::is_within_distance("hello", "world", 1));
        assert!(Levenshtein::is_within_distance("hello", "world", 5));
    }

    #[test]
    fn test_optimized_distance() {
        assert_eq!(LevenshteinOptimized::distance("kitten", "sitting"), 3);
        assert_eq!(LevenshteinOptimized::distance("hello", "hello"), 0);
        assert_eq!(LevenshteinOptimized::distance("", "test"), 4);
    }

    #[test]
    fn test_damerau_levenshtein() {
        // Transposition: "ab" -> "ba" should be 1, not 2
        assert_eq!(DamerauLevenshtein::distance("ab", "ba"), 1);
        assert_eq!(DamerauLevenshtein::distance("abc", "acb"), 1);

        // Regular operations still work
        assert_eq!(DamerauLevenshtein::distance("hello", "hello"), 0);
    }

    #[test]
    fn test_edit_operations() {
        let (dist, ops) = Levenshtein::distance_with_ops("cat", "cats");
        assert_eq!(dist, 1);
        assert_eq!(ops.len(), 4); // 3 matches + 1 insert
    }
}
