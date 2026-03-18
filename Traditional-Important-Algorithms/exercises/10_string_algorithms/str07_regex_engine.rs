// str07_regex_engine.rs
//
// Simple Regular Expression Engine
//
// A basic regex engine supporting fundamental pattern matching operations.
// Implements a subset of regex features using recursive backtracking or NFA.
//
// Time Complexity: O(2^n) worst case (backtracking), O(nm) with NFA
// Space Complexity: O(n) for recursion stack or NFA states
//
// Key concepts:
// - Pattern matching with special characters
// - Supported: . (any char), * (zero or more), + (one or more), ? (optional)
// - Character classes: [abc], [a-z]
// - Anchors: ^ (start), $ (end)
// - Backtracking or NFA-based implementation
// - Foundation for tools like grep, sed
//
// Your task: Implement a simple regex engine with basic operators.

// I AM NOT DONE

#[derive(Debug, Clone, PartialEq)]
enum Token {
    Char(char),
    Dot,              // . matches any character
    Star,             // * matches zero or more of previous
    Plus,             // + matches one or more of previous
    Question,         // ? matches zero or one of previous
    Caret,            // ^ matches start of string
    Dollar,           // $ matches end of string
    CharClass(Vec<char>), // [abc] matches any of a, b, c
}

pub struct Regex {
    pattern: String,
    tokens: Vec<Token>,
}

impl Regex {
    pub fn new(pattern: &str) -> Result<Self, String> {
        let tokens = Self::parse(pattern)?;
        Ok(Self {
            pattern: pattern.to_string(),
            tokens,
        })
    }

    fn parse(pattern: &str) -> Result<Vec<Token>, String> {
        // TODO: Parse pattern string into tokens
        // - Iterate through pattern characters
        // - Handle special characters: . * + ? ^ $
        // - Handle character classes: [abc] or [a-z]
        // - Return error for invalid patterns (e.g., [abc with no closing bracket)
        todo!()
    }

    pub fn is_match(&self, text: &str) -> bool {
        // TODO: Check if pattern matches entire text
        // - Use backtracking or NFA approach
        // - Start matching from beginning
        // - Return true if entire text matches pattern
        todo!()
    }

    pub fn find(&self, text: &str) -> Option<(usize, usize)> {
        // TODO: Find first match in text (doesn't need to match entire string)
        // - Try matching at each position in text
        // - Return (start, end) of first match
        // - Return None if no match found
        todo!()
    }

    pub fn find_all(&self, text: &str) -> Vec<(usize, usize)> {
        // TODO: Find all non-overlapping matches
        // - Return Vec of (start, end) positions
        todo!()
    }

    fn match_at(&self, text: &str, start: usize) -> Option<usize> {
        // TODO: Try to match pattern starting at position 'start'
        // - Return end position if match succeeds
        // - Return None if no match
        // - This is the core matching logic
        todo!()
    }

    fn match_tokens(&self, text_chars: &[char], text_pos: usize, token_pos: usize) -> bool {
        // TODO: Recursive backtracking matcher
        // - Base case: if token_pos reaches end, check if text_pos at end (or $ allows)
        // - Handle each token type:
        //   - Char(c): match if text[text_pos] == c
        //   - Dot: match any character
        //   - Star: try matching 0, 1, 2, ... times (backtrack)
        //   - Plus: match at least once, then like Star
        //   - Question: try matching 0 or 1 time
        //   - Caret: only match at start
        //   - Dollar: only match at end
        //   - CharClass: match if text[text_pos] in class
        // - Return true if any path leads to complete match
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_literal_match() {
        let re = Regex::new("hello").unwrap();
        assert!(re.is_match("hello"));
        assert!(!re.is_match("world"));
    }

    #[test]
    fn test_dot_operator() {
        let re = Regex::new("h.llo").unwrap();
        assert!(re.is_match("hello"));
        assert!(re.is_match("hallo"));
        assert!(re.is_match("hxllo"));
        assert!(!re.is_match("hllo"));
    }

    #[test]
    fn test_star_operator() {
        let re = Regex::new("ab*c").unwrap();
        assert!(re.is_match("ac"));      // b appears 0 times
        assert!(re.is_match("abc"));     // b appears 1 time
        assert!(re.is_match("abbc"));    // b appears 2 times
        assert!(re.is_match("abbbc"));   // b appears 3 times
        assert!(!re.is_match("abdc"));
    }

    #[test]
    fn test_plus_operator() {
        let re = Regex::new("ab+c").unwrap();
        assert!(!re.is_match("ac"));     // b must appear at least once
        assert!(re.is_match("abc"));
        assert!(re.is_match("abbc"));
        assert!(re.is_match("abbbc"));
    }

    #[test]
    fn test_question_operator() {
        let re = Regex::new("colou?r").unwrap();
        assert!(re.is_match("color"));
        assert!(re.is_match("colour"));
        assert!(!re.is_match("colouur"));
    }

    #[test]
    fn test_caret_anchor() {
        let re = Regex::new("^hello").unwrap();
        assert!(re.is_match("hello"));
        assert!(re.is_match("hello world"));
        // Note: is_match checks entire string, find checks substring
    }

    #[test]
    fn test_dollar_anchor() {
        let re = Regex::new("world$").unwrap();
        assert!(re.is_match("world"));
        assert!(re.is_match("hello world"));
    }

    #[test]
    fn test_find() {
        let re = Regex::new("test").unwrap();
        assert_eq!(re.find("this is a test"), Some((10, 14)));
        assert_eq!(re.find("no match"), None);
    }

    #[test]
    fn test_find_all() {
        let re = Regex::new("ab").unwrap();
        let matches = re.find_all("ababab");
        assert_eq!(matches, vec![(0, 2), (2, 4), (4, 6)]);
    }

    #[test]
    fn test_char_class() {
        let re = Regex::new("[abc]").unwrap();
        assert!(re.is_match("a"));
        assert!(re.is_match("b"));
        assert!(re.is_match("c"));
        assert!(!re.is_match("d"));
    }

    #[test]
    fn test_complex_pattern() {
        let re = Regex::new("a.*b").unwrap();
        assert!(re.is_match("ab"));
        assert!(re.is_match("axyzb"));
        assert!(!re.is_match("ba"));
    }

    #[test]
    fn test_multiple_operators() {
        let re = Regex::new("a+b*c?").unwrap();
        assert!(re.is_match("a"));       // a+, b* (0 times), c? (0 times)
        assert!(re.is_match("aaa"));     // a+, b* (0 times), c? (0 times)
        assert!(re.is_match("aaabbc"));  // a+, b*, c?
    }
}
