// str08_huffman.rs
//
// Huffman Coding for Text Compression
//
// Huffman coding is a lossless compression algorithm that assigns variable-length
// codes to characters based on their frequency. More frequent characters get shorter codes.
//
// Time Complexity: O(n log n) for building tree, O(n) for encoding/decoding
// Space Complexity: O(n) for the tree
//
// Key concepts:
// - Frequency analysis: Count character occurrences
// - Binary tree: Build using priority queue (min-heap)
// - Prefix-free codes: No code is prefix of another
// - Optimal compression: Minimizes expected code length
// - Used in ZIP, JPEG, MP3 formats
//
// Your task: Implement Huffman encoding and decoding.

// I AM NOT DONE

use std::collections::{HashMap, BinaryHeap};
use std::cmp::Ordering;

#[derive(Debug, Eq, PartialEq)]
struct Node {
    freq: usize,
    ch: Option<char>,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    fn new_leaf(ch: char, freq: usize) -> Self {
        Self {
            freq,
            ch: Some(ch),
            left: None,
            right: None,
        }
    }

    fn new_internal(freq: usize, left: Box<Node>, right: Box<Node>) -> Self {
        Self {
            freq,
            ch: None,
            left: Some(left),
            right: Some(right),
        }
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        // Reverse ordering for min-heap (BinaryHeap is max-heap by default)
        other.freq.cmp(&self.freq)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct HuffmanEncoder {
    root: Option<Box<Node>>,
    codebook: HashMap<char, String>,
}

impl HuffmanEncoder {
    pub fn new(text: &str) -> Self {
        let frequencies = Self::compute_frequencies(text);
        let root = Self::build_tree(frequencies);
        let codebook = Self::build_codebook(&root);

        Self {
            root: Some(root),
            codebook,
        }
    }

    fn compute_frequencies(text: &str) -> HashMap<char, usize> {
        // TODO: Count frequency of each character
        // - Iterate through text
        // - Build HashMap of char -> count
        todo!()
    }

    fn build_tree(frequencies: HashMap<char, usize>) -> Box<Node> {
        // TODO: Build Huffman tree using priority queue
        // - Create leaf node for each character with its frequency
        // - Add all leaves to min-heap (priority queue)
        // - While heap has more than 1 node:
        //   - Remove two nodes with lowest frequency
        //   - Create internal node with sum of frequencies
        //   - Add internal node back to heap
        // - Final node is root of Huffman tree
        todo!()
    }

    fn build_codebook(root: &Option<Box<Node>>) -> HashMap<char, String> {
        // TODO: Generate codebook by traversing tree
        // - Traverse tree, building binary code string
        // - Left edge = '0', right edge = '1'
        // - At leaf nodes, record character and its code
        // - Return HashMap of char -> binary code string
        todo!()
    }

    fn traverse_tree(node: &Box<Node>, code: String, codebook: &mut HashMap<char, String>) {
        // TODO: Helper function for build_codebook
        // - Recursive traversal
        // - If leaf (ch.is_some()), add to codebook
        // - If internal, recurse left with code + '0', right with code + '1'
        todo!()
    }

    pub fn encode(&self, text: &str) -> String {
        // TODO: Encode text using codebook
        // - Replace each character with its Huffman code
        // - Concatenate all codes into single binary string
        todo!()
    }

    pub fn decode(&self, encoded: &str) -> Result<String, String> {
        // TODO: Decode binary string back to text
        // - Start at root of tree
        // - For each bit in encoded string:
        //   - '0' = go left, '1' = go right
        //   - When reaching leaf, output character and return to root
        // - Return error if invalid code sequence
        todo!()
    }

    pub fn get_codebook(&self) -> &HashMap<char, String> {
        &self.codebook
    }

    pub fn compression_ratio(&self, original: &str) -> f64 {
        // TODO: Calculate compression ratio
        // - Original size: original.len() * 8 bits (assuming 8-bit chars)
        // - Compressed size: sum of (freq[char] * code_length[char])
        // - Ratio: compressed_size / original_size
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_computation() {
        let encoder = HuffmanEncoder::new("aabbc");
        let codebook = encoder.get_codebook();

        // All characters should be in codebook
        assert!(codebook.contains_key(&'a'));
        assert!(codebook.contains_key(&'b'));
        assert!(codebook.contains_key(&'c'));
    }

    #[test]
    fn test_code_lengths() {
        let encoder = HuffmanEncoder::new("aaaaaabbcd");
        let codebook = encoder.get_codebook();

        // 'a' appears most (6 times), should have shortest code
        // 'c' and 'd' appear least (1 each), should have longer codes
        let a_len = codebook.get(&'a').unwrap().len();
        let c_len = codebook.get(&'c').unwrap().len();

        assert!(a_len <= c_len);
    }

    #[test]
    fn test_prefix_free() {
        let encoder = HuffmanEncoder::new("abcdef");
        let codebook = encoder.get_codebook();

        // No code should be prefix of another
        for (_, code1) in codebook.iter() {
            for (_, code2) in codebook.iter() {
                if code1 != code2 {
                    assert!(!code1.starts_with(code2));
                    assert!(!code2.starts_with(code1));
                }
            }
        }
    }

    #[test]
    fn test_encode_decode() {
        let text = "hello world";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);
        let decoded = encoder.decode(&encoded).unwrap();

        assert_eq!(decoded, text);
    }

    #[test]
    fn test_single_character() {
        let text = "aaaa";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);
        let decoded = encoder.decode(&encoded).unwrap();

        assert_eq!(decoded, text);
    }

    #[test]
    fn test_compression() {
        let text = "aaaaaabbcd";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);

        // Encoded length should be less than original * 8
        assert!(encoded.len() < text.len() * 8);
    }

    #[test]
    fn test_compression_ratio() {
        let text = "aaaaaabbbbccde";
        let encoder = HuffmanEncoder::new(text);

        let ratio = encoder.compression_ratio(text);

        // Ratio should be less than 1.0 for good compression
        assert!(ratio < 1.0);
        assert!(ratio > 0.0);
    }

    #[test]
    fn test_all_unique_characters() {
        let text = "abcdefgh";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);
        let decoded = encoder.decode(&encoded).unwrap();

        assert_eq!(decoded, text);
    }

    #[test]
    fn test_empty_string() {
        let text = "";
        let encoder = HuffmanEncoder::new("a"); // Need at least one char for tree

        let encoded = encoder.encode(text);
        assert_eq!(encoded, "");
    }

    #[test]
    fn test_repeated_pattern() {
        let text = "abababab";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);
        let decoded = encoder.decode(&encoded).unwrap();

        assert_eq!(decoded, text);
    }

    #[test]
    fn test_decode_invalid_code() {
        let encoder = HuffmanEncoder::new("abc");

        // Invalid binary string that doesn't correspond to valid path
        let result = encoder.decode("11111111");

        // Should either error or handle gracefully
        // (depending on implementation, might return partial or error)
    }

    #[test]
    fn test_longer_text() {
        let text = "The quick brown fox jumps over the lazy dog. The dog was not amused.";
        let encoder = HuffmanEncoder::new(text);

        let encoded = encoder.encode(text);
        let decoded = encoder.decode(&encoded).unwrap();

        assert_eq!(decoded, text);

        // Should achieve some compression
        assert!(encoded.len() < text.len() * 8);
    }
}
