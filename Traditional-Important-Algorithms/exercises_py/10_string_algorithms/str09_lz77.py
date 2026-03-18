# I AM NOT DONE

"""
Exercise: LZ77 Compression

LZ77 is a lossless compression algorithm that replaces repeated occurrences
of data with references to earlier occurrences.

Key concepts:
- Sliding window buffer
- Look-ahead buffer
- (offset, length, next_char) tuples
- Used in gzip, PNG, etc.

Your task: Implement LZ77 compression and decompression.
"""

from typing import List, Tuple


class LZ77:
    """LZ77 compression algorithm"""

    def __init__(self, window_size: int = 4096, lookahead_size: int = 18):
        self.window_size = window_size
        self.lookahead_size = lookahead_size

    def compress(self, text: str) -> List[Tuple[int, int, str]]:
        """Compress text using LZ77"""
        # TODO: Implement LZ77 compression
        # - Scan text with sliding window
        # - For each position, find longest match in window
        # - Output (offset, length, next_char) tuples
        pass

    def decompress(self, compressed: List[Tuple[int, int, str]]) -> str:
        """Decompress LZ77-encoded data"""
        # TODO: Decompress data
        # - Process each (offset, length, next_char) tuple
        # - Copy from previous data using offset and length
        # - Append next_char
        pass

    def _find_longest_match(self, text: str, pos: int) -> Tuple[int, int]:
        """Find longest match in sliding window"""
        # TODO: Find longest match
        # - Search in window for best match
        # - Return (offset, length)
        pass


import unittest


class TestLZ77(unittest.TestCase):
    def test_compress_decompress(self):
        lz = LZ77()
        text = "abracadabra"
        compressed = lz.compress(text)
        decompressed = lz.decompress(compressed)
        self.assertEqual(decompressed, text)

    def test_repeated_pattern(self):
        lz = LZ77()
        text = "aaaaaaaaaa"
        compressed = lz.compress(text)
        self.assertLess(len(compressed), len(text))
        decompressed = lz.decompress(compressed)
        self.assertEqual(decompressed, text)

    def test_no_repetition(self):
        lz = LZ77()
        text = "abcdefgh"
        compressed = lz.compress(text)
        decompressed = lz.decompress(compressed)
        self.assertEqual(decompressed, text)


if __name__ == '__main__':
    unittest.main()
