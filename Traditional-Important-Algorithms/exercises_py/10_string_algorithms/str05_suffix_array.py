# I AM NOT DONE

"""
Exercise: Suffix Array

A suffix array is a sorted array of all suffixes of a string.
Enables fast pattern matching and substring queries.

Time Complexity: O(n log n) construction, O(m log n) search
Space Complexity: O(n)

Key concepts:
- All suffixes sorted lexicographically
- Binary search for pattern matching
- LCP (Longest Common Prefix) array for advanced queries
- Space-efficient alternative to suffix tree

Your task: Implement suffix array with pattern searching.
"""

from typing import List, Tuple, Optional


class SuffixArray:
    """Suffix array data structure"""

    def __init__(self, text: str):
        self.text = text
        self.suffix_array = self._build_suffix_array(text)
        self.lcp = self._build_lcp_array()

    def _build_suffix_array(self, text: str) -> List[int]:
        """Build suffix array"""
        # TODO: Build suffix array
        # - Create list of (suffix, index) pairs
        # - Sort by suffix
        # - Return indices
        pass

    def _build_lcp_array(self) -> List[int]:
        """Build LCP (Longest Common Prefix) array"""
        # TODO: Build LCP array
        # - lcp[i] = length of longest common prefix between suffix[i] and suffix[i-1]
        # - lcp[0] = 0
        pass

    def search(self, pattern: str) -> List[int]:
        """Find all occurrences of pattern"""
        # TODO: Find all occurrences of pattern
        # - Use binary search on suffix array
        # - Find range of suffixes starting with pattern
        # - Return sorted list of positions
        pass

    def contains(self, pattern: str) -> bool:
        """Check if pattern exists"""
        # TODO: Check if pattern exists
        pass

    def longest_repeated_substring(self) -> str:
        """Find longest repeated substring"""
        # TODO: Find longest repeated substring using LCP array
        pass


import unittest


class TestSuffixArray(unittest.TestCase):
    def test_suffix_array_construction(self):
        sa = SuffixArray("banana")
        self.assertEqual(len(sa.suffix_array), 6)

    def test_search_pattern(self):
        sa = SuffixArray("banana")
        positions = sa.search("ana")
        self.assertEqual(sorted(positions), [1, 3])

    def test_search_no_match(self):
        sa = SuffixArray("banana")
        positions = sa.search("xyz")
        self.assertEqual(positions, [])

    def test_contains(self):
        sa = SuffixArray("hello world")
        self.assertTrue(sa.contains("world"))
        self.assertFalse(sa.contains("xyz"))

    def test_longest_repeated_substring(self):
        sa = SuffixArray("banana")
        lrs = sa.longest_repeated_substring()
        self.assertEqual(lrs, "ana")

    def test_single_character(self):
        sa = SuffixArray("a")
        self.assertEqual(sa.search("a"), [0])

    def test_repeated_characters(self):
        sa = SuffixArray("aaaa")
        positions = sa.search("aa")
        self.assertEqual(len(positions), 3)


if __name__ == '__main__':
    unittest.main()
