# I AM NOT DONE

"""
Exercise: Rabin-Karp String Matching Algorithm

Rabin-Karp uses rolling hash to efficiently search for patterns in text.
It's particularly effective for multiple pattern matching.

Time Complexity: O(n + m) average case, O(nm) worst case
Space Complexity: O(1)

Key concepts:
- Rolling hash: Update hash in O(1) by removing leftmost char and adding new char
- Hash collision: When hashes match, verify with actual string comparison
- Base and modulo: Choose prime modulo to minimize collisions
- Can easily extend to multiple pattern matching

Your task: Implement Rabin-Karp with rolling hash function.
"""

from typing import List, Optional, Tuple


BASE = 256
MODULO = 1_000_000_007


class RabinKarp:
    """Rabin-Karp string matching algorithm"""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pattern_hash = self._compute_hash(pattern)
        self.pattern_len = len(pattern)
        self.base_power = self._compute_base_power(len(pattern))

    def _compute_hash(self, s: str) -> int:
        """Compute hash of string"""
        # TODO: Compute hash of string
        # - hash = (s[0] * BASE^(n-1) + s[1] * BASE^(n-2) + ... + s[n-1]) mod MODULO
        # - Use Horner's method: hash = ((s[0] * BASE + s[1]) * BASE + s[2]) * BASE ...
        # - Take modulo at each step to prevent overflow
        pass

    def _compute_base_power(self, pattern_len: int) -> int:
        """Compute BASE^(pattern_len-1) mod MODULO"""
        # TODO: Compute BASE^(pattern_len-1) mod MODULO
        # - This is used for rolling hash to remove leftmost character
        # - Use modular exponentiation or iterative multiplication with modulo
        pass

    def _rolling_hash(self, old_hash: int, old_char: str, new_char: str) -> int:
        """Update hash by removing old_char and adding new_char"""
        # TODO: Update hash by removing old_char and adding new_char
        # - Remove old_char: subtract (ord(old_char) * base_power) mod MODULO
        # - Shift: multiply by BASE
        # - Add new_char: add ord(new_char)
        # - Take modulo at each step
        # - Handle potential underflow when subtracting (add MODULO if needed)
        pass

    def search(self, text: str) -> List[int]:
        """Find all occurrences using rolling hash"""
        # TODO: Find all occurrences using rolling hash
        # - Compute initial hash of text[0..pattern_len]
        # - For each position, compare hash with pattern_hash
        # - If hashes match, verify with actual string comparison (handle collisions)
        # - Update hash using rolling_hash for next window
        # - Return all match positions
        pass

    def contains(self, text: str) -> bool:
        """Check if pattern exists in text"""
        # TODO: Check if pattern exists in text
        pass

    def first_occurrence(self, text: str) -> Optional[int]:
        """Return position of first match"""
        # TODO: Return position of first match
        pass


class MultiPatternRabinKarp:
    """Rabin-Karp for multiple patterns"""

    def __init__(self, patterns: List[str]):
        """Initialize for multiple patterns of same length"""
        # TODO: Initialize for multiple patterns of same length
        # - All patterns must have same length
        # - Compute hash for each pattern
        # - Store in a set for O(1) lookup
        # - Raise exception if patterns have different lengths
        pass

    def search(self, text: str) -> List[Tuple[int, int]]:
        """Find all occurrences of any pattern"""
        # TODO: Find all occurrences of any pattern
        # - Return list of (position, pattern_index) tuples
        # - Use rolling hash for text window
        # - Check if window hash matches any pattern hash
        # - Verify actual match on hash collision
        pass


import unittest


class TestRabinKarp(unittest.TestCase):
    def test_compute_hash(self):
        rk = RabinKarp("ABC")
        self.assertGreater(rk.pattern_hash, 0)

        # Same string should have same hash
        rk2 = RabinKarp("ABC")
        self.assertEqual(rk.pattern_hash, rk2.pattern_hash)

    def test_simple_match(self):
        rk = RabinKarp("test")
        positions = rk.search("this is a test string")
        self.assertEqual(positions, [10])

    def test_multiple_matches(self):
        rk = RabinKarp("ab")
        positions = rk.search("ababab")
        self.assertEqual(positions, [0, 2, 4])

    def test_overlapping_matches(self):
        rk = RabinKarp("aaa")
        positions = rk.search("aaaaa")
        self.assertEqual(positions, [0, 1, 2])

    def test_no_match(self):
        rk = RabinKarp("xyz")
        positions = rk.search("abcdef")
        self.assertEqual(positions, [])

    def test_contains(self):
        rk = RabinKarp("world")
        self.assertTrue(rk.contains("hello world"))
        self.assertFalse(rk.contains("hello earth"))

    def test_first_occurrence(self):
        rk = RabinKarp("pattern")
        self.assertEqual(rk.first_occurrence("find the pattern here"), 9)
        self.assertIsNone(rk.first_occurrence("no match"))

    def test_pattern_at_boundaries(self):
        rk = RabinKarp("hello")
        self.assertEqual(rk.search("hello world"), [0])
        self.assertEqual(rk.search("world hello"), [6])
        self.assertEqual(rk.search("hello"), [0])

    def test_single_character(self):
        rk = RabinKarp("x")
        positions = rk.search("axbxcxd")
        self.assertEqual(positions, [1, 3, 5])

    def test_longer_pattern(self):
        rk = RabinKarp("abracadabra")
        positions = rk.search("abracadabra appears once")
        self.assertEqual(positions, [0])

    def test_multi_pattern_same_length(self):
        patterns = ["cat", "dog", "fox"]
        mp = MultiPatternRabinKarp(patterns)

        matches = mp.search("the cat and dog chase the fox")
        match_positions = [m[0] for m in matches]
        self.assertIn(4, match_positions)   # "cat" at position 4
        self.assertIn(12, match_positions)  # "dog" at position 12
        self.assertIn(26, match_positions)  # "fox" at position 26


if __name__ == '__main__':
    unittest.main()
