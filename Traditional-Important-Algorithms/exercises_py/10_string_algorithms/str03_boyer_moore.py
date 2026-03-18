# I AM NOT DONE

"""
Exercise: Boyer-Moore String Matching Algorithm

Boyer-Moore is one of the most efficient string matching algorithms,
scanning the pattern from right to left and using two heuristics to skip sections.

Time Complexity: O(n/m) best case, O(nm) worst case, O(n) typical
Space Complexity: O(m + σ) where σ is alphabet size

Key concepts:
- Bad character rule: Skip based on rightmost occurrence of mismatched character
- Good suffix rule: Skip based on matching suffix pattern
- Scan pattern from right to left
- Can skip multiple characters per iteration
- Sublinear time complexity in practice

Your task: Implement Boyer-Moore with bad character and good suffix rules.
"""

from typing import List, Dict, Optional


class BoyerMoore:
    """Boyer-Moore string matching algorithm"""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pattern_bytes = pattern.encode()
        self.bad_char = self._compute_bad_char_table(self.pattern_bytes)
        self.good_suffix = self._compute_good_suffix_table(self.pattern_bytes)

    def _compute_bad_char_table(self, pattern: bytes) -> Dict[int, int]:
        """Build bad character table"""
        # TODO: Build bad character table
        # - For each character, store its rightmost position in pattern
        # - Position is from right: pattern[m-1] is at position 0
        # - If character not in pattern, it will be missing from dict
        pass

    def _compute_good_suffix_table(self, pattern: bytes) -> List[int]:
        """Build good suffix table"""
        # TODO: Build good suffix table
        # - good_suffix[i] = shift distance when mismatch occurs at position i
        # - Consider two cases:
        #   1. Suffix pattern[i+1..] appears elsewhere in pattern
        #   2. A prefix of pattern matches a suffix of pattern[i+1..]
        # - This is complex; simplified version acceptable
        # - Return list of length len(pattern)
        pass

    def search(self, text: str) -> List[int]:
        """Search using Boyer-Moore algorithm"""
        # TODO: Search using Boyer-Moore algorithm
        # - Scan pattern from right to left (high index to low)
        # - On mismatch, use both bad character and good suffix rules
        # - Shift by maximum of the two rules
        # - On complete match, record position and continue searching
        # - Return all match positions
        pass

    def _bad_char_shift(self, char: int, position: int) -> int:
        """Calculate shift based on bad character rule"""
        # TODO: Calculate shift based on bad character rule
        # - If char exists in pattern, shift so that rightmost occurrence aligns
        # - If char doesn't exist, shift by entire pattern length
        # - position is where mismatch occurred in pattern
        pass

    def _good_suffix_shift(self, position: int) -> int:
        """Calculate shift based on good suffix rule"""
        # TODO: Calculate shift based on good suffix rule
        # - Use precomputed good_suffix table
        # - Return shift amount for given mismatch position
        pass

    def contains(self, text: str) -> bool:
        """Check if pattern exists in text"""
        # TODO: Check if pattern exists in text
        pass

    def first_occurrence(self, text: str) -> Optional[int]:
        """Return first match position"""
        # TODO: Return first match position
        pass

    def get_bad_char_table(self) -> Dict[int, int]:
        return self.bad_char

    def get_good_suffix_table(self) -> List[int]:
        return self.good_suffix


import unittest


class TestBoyerMoore(unittest.TestCase):
    def test_bad_char_table(self):
        bm = BoyerMoore("EXAMPLE")
        table = bm.get_bad_char_table()
        self.assertIn(ord('E'), table)
        self.assertIn(ord('X'), table)
        self.assertIn(ord('A'), table)

    def test_simple_match(self):
        bm = BoyerMoore("pattern")
        positions = bm.search("find the pattern here")
        self.assertEqual(positions, [9])

    def test_multiple_matches(self):
        bm = BoyerMoore("ab")
        positions = bm.search("ababab")
        self.assertEqual(positions, [0, 2, 4])

    def test_no_match(self):
        bm = BoyerMoore("xyz")
        positions = bm.search("abcdef")
        self.assertEqual(positions, [])

    def test_contains(self):
        bm = BoyerMoore("world")
        self.assertTrue(bm.contains("hello world"))
        self.assertFalse(bm.contains("hello earth"))

    def test_first_occurrence(self):
        bm = BoyerMoore("test")
        self.assertEqual(bm.first_occurrence("this is a test string"), 10)
        self.assertIsNone(bm.first_occurrence("no match"))

    def test_pattern_at_end(self):
        bm = BoyerMoore("end")
        self.assertEqual(bm.search("this is the end"), [12])

    def test_pattern_at_start(self):
        bm = BoyerMoore("start")
        self.assertEqual(bm.search("start of text"), [0])

    def test_overlapping_pattern(self):
        bm = BoyerMoore("aaa")
        positions = bm.search("aaaaa")
        self.assertEqual(positions, [0, 1, 2])

    def test_single_character(self):
        bm = BoyerMoore("x")
        positions = bm.search("axbxcxd")
        self.assertEqual(positions, [1, 3, 5])

    def test_repeated_characters(self):
        bm = BoyerMoore("aaa")
        self.assertEqual(bm.search("aaaaaa"), [0, 1, 2, 3])

    def test_longer_pattern_than_text(self):
        bm = BoyerMoore("verylongpattern")
        self.assertEqual(bm.search("short"), [])


if __name__ == '__main__':
    unittest.main()
