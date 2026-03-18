// str09_lz77.rs
//
// LZ77 Compression Algorithm
//
// LZ77 is a lossless compression algorithm that replaces repeated occurrences
// of data with references to earlier occurrences. It uses a sliding window.
//
// Time Complexity: O(n × w) where n is input size, w is window size
// Space Complexity: O(w) for the sliding window
//
// Key concepts:
// - Sliding window: Look-back buffer and look-ahead buffer
// - Tokens: (offset, length, next_char) triplets
// - Longest match: Find longest match in window for current position
// - Foundation for DEFLATE (used in gzip, PNG, ZIP)
// - Trade-off between window size and compression ratio
//
// Your task: Implement LZ77 compression and decompression.

// I AM NOT DONE

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Token {
    pub offset: usize,  // Distance back to start of match
    pub length: usize,  // Length of match
    pub next: char,     // Next character after match
}

pub struct LZ77 {
    window_size: usize,      // Size of look-back buffer
    lookahead_size: usize,   // Size of look-ahead buffer
}

impl LZ77 {
    pub fn new(window_size: usize, lookahead_size: usize) -> Self {
        Self {
            window_size,
            lookahead_size,
        }
    }

    pub fn default() -> Self {
        Self::new(4096, 18) // Common sizes for DEFLATE
    }

    pub fn compress(&self, text: &str) -> Vec<Token> {
        // TODO: Compress text using LZ77
        // - Iterate through text with sliding window
        // - For each position:
        //   - Search window for longest match with lookahead buffer
        //   - Create token (offset, length, next_char)
        //   - offset = 0, length = 0 if no match found
        //   - next_char = character after the match (or current if no match)
        // - Return vector of tokens
        todo!()
    }

    fn find_longest_match(&self, text: &str, pos: usize) -> (usize, usize) {
        // TODO: Find longest match in window for current position
        // - Window: text[max(0, pos - window_size)..pos]
        // - Lookahead: text[pos..min(pos + lookahead_size, text.len())]
        // - Search window for substring that matches beginning of lookahead
        // - Return (offset, length) where offset is distance back from pos
        // - Return (0, 0) if no match found
        todo!()
    }

    pub fn decompress(&self, tokens: &[Token]) -> String {
        // TODO: Decompress tokens back to original text
        // - Build output string incrementally
        // - For each token (offset, length, next):
        //   - If length > 0: copy 'length' characters from offset positions back
        //   - Append next character
        //   - Handle case where match extends into itself (offset < length)
        // - Return reconstructed string
        todo!()
    }

    pub fn compression_ratio(&self, original: &str, compressed: &[Token]) -> f64 {
        // TODO: Calculate compression ratio
        // - Original size: original.len() bytes
        // - Compressed size: tokens.len() * size_of_token
        // - For simplicity, assume each token is fixed size (e.g., 3-4 bytes)
        // - Ratio: compressed_size / original_size
        todo!()
    }
}

pub struct LZ77Optimized {
    window_size: usize,
    lookahead_size: usize,
}

impl LZ77Optimized {
    pub fn new(window_size: usize, lookahead_size: usize) -> Self {
        Self {
            window_size,
            lookahead_size,
        }
    }

    pub fn compress(&self, text: &str) -> Vec<Token> {
        // TODO: Optimized compression using hash table
        // - Use HashMap to index positions of substrings
        // - Key: hash of substring (e.g., first 3 characters)
        // - Value: positions where this substring appears
        // - Speeds up match finding from O(w) to O(1) average
        todo!()
    }

    pub fn decompress(&self, tokens: &[Token]) -> String {
        // Same as regular LZ77
        LZ77::new(self.window_size, self.lookahead_size).decompress(tokens)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_repetition() {
        let lz77 = LZ77::default();
        let text = "abcdefgh";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_simple_repetition() {
        let lz77 = LZ77::default();
        let text = "aaaaaa";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);

        // Should achieve compression (fewer tokens than characters)
        assert!(compressed.len() < text.len());
    }

    #[test]
    fn test_pattern_repetition() {
        let lz77 = LZ77::default();
        let text = "abcabcabc";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_overlapping_match() {
        let lz77 = LZ77::default();
        // "aaa" can be encoded as (1, 2, 'a') from second 'a'
        let text = "aaaaaa";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_long_distance_match() {
        let lz77 = LZ77::new(100, 20);
        let text = "abcdefghijklmnop abcdefghijklmnop";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_empty_string() {
        let lz77 = LZ77::default();
        let text = "";

        let compressed = lz77.compress(text);
        assert_eq!(compressed.len(), 0);

        let decompressed = lz77.decompress(&compressed);
        assert_eq!(decompressed, "");
    }

    #[test]
    fn test_single_character() {
        let lz77 = LZ77::default();
        let text = "a";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_compression_ratio() {
        let lz77 = LZ77::default();
        let text = "abcabcabcabcabcabc"; // Highly repetitive

        let compressed = lz77.compress(text);
        let ratio = lz77.compression_ratio(text, &compressed);

        // Ratio should be less than 1.0 for repetitive text
        assert!(ratio < 1.0);
    }

    #[test]
    fn test_window_size_limit() {
        let lz77 = LZ77::new(5, 10); // Small window
        let text = "abc_________abc"; // Match outside window

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_real_text() {
        let lz77 = LZ77::default();
        let text = "The quick brown fox jumps over the lazy dog. The dog was lazy.";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_optimized_compression() {
        let lz77 = LZ77Optimized::new(4096, 18);
        let text = "abcabcabcabcabc";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }

    #[test]
    fn test_self_referencing_match() {
        let lz77 = LZ77::default();
        // Pattern where match extends into itself
        let text = "aaaaaaaaa";

        let compressed = lz77.compress(text);
        let decompressed = lz77.decompress(&compressed);

        assert_eq!(decompressed, text);
    }
}
