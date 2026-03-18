# I AM NOT DONE

"""
Exercise: Huffman Coding

Huffman coding is a lossless compression algorithm that assigns variable-length
codes to characters based on their frequencies.

Time Complexity: O(n log n)
Space Complexity: O(n)

Key concepts:
- Build frequency table
- Construct Huffman tree using priority queue
- Generate prefix-free codes
- Encode and decode text

Your task: Implement Huffman encoding and decoding.
"""

from typing import Dict, Tuple, Optional
import heapq
from collections import Counter


class HuffmanNode:
    """Node in Huffman tree"""
    def __init__(self, char: Optional[str], freq: int, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    """Huffman encoding/decoding"""

    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def build_tree(self, text: str) -> HuffmanNode:
        """Build Huffman tree from text"""
        # TODO: Build Huffman tree
        # - Count character frequencies
        # - Create leaf nodes for each character
        # - Use min-heap to build tree bottom-up
        # - Return root node
        pass

    def generate_codes(self, node: HuffmanNode, code: str = ""):
        """Generate Huffman codes from tree"""
        # TODO: Generate codes via tree traversal
        # - Traverse tree, building codes
        # - Left = 0, Right = 1
        # - Store in self.codes
        pass

    def encode(self, text: str) -> Tuple[str, HuffmanNode]:
        """Encode text using Huffman coding"""
        # TODO: Encode text
        # - Build tree
        # - Generate codes
        # - Encode text using codes
        # - Return (encoded_bits, tree)
        pass

    def decode(self, encoded: str, tree: HuffmanNode) -> str:
        """Decode Huffman-encoded text"""
        # TODO: Decode text
        # - Traverse tree following bits
        # - Decode one character at a time
        pass


import unittest


class TestHuffmanCoding(unittest.TestCase):
    def test_encode_decode(self):
        huff = HuffmanCoding()
        text = "hello world"
        encoded, tree = huff.encode(text)
        decoded = huff.decode(encoded, tree)
        self.assertEqual(decoded, text)

    def test_compression(self):
        huff = HuffmanCoding()
        text = "aaabbc"
        encoded, _ = huff.encode(text)
        # Should be shorter than 6*8 = 48 bits
        self.assertLess(len(encoded), 48)

    def test_single_character(self):
        huff = HuffmanCoding()
        text = "aaaa"
        encoded, tree = huff.encode(text)
        decoded = huff.decode(encoded, tree)
        self.assertEqual(decoded, text)


if __name__ == '__main__':
    unittest.main()
