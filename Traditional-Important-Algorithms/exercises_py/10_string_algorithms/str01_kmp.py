# I AM NOT DONE

"""
Exercise: Knuth-Morris-Pratt (KMP) String Matching Algorithm

KMP is an efficient string matching algorithm that avoids re-examining
previously matched characters by using a failure function (prefix table).

Time Complexity: O(n + m) where n is text length, m is pattern length
Space Complexity: O(m) for the failure function

Key concepts:
- Failure function (LPS array): Longest Proper Prefix which is also Suffix
- No backtracking in the text - we only backtrack in the pattern
- Preprocessing the pattern allows linear time matching

Your task: Implement the KMP string matching algorithm with failure function.
"""

from typing import List, Optional


class KMP:
    """KMP string matching algorithm"""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.failure = self._compute_failure(pattern)

    def _compute_failure(self, pattern: str) -> List[int]:
        """
        Compute the failure function (LPS array)

        Args:
            pattern: The pattern string

        Returns:
            List of failure function values
        """
        # TODO: Compute the failure function (LPS array)
        # - failure[i] = length of longest proper prefix of pattern[0..=i]
        #   that is also a suffix of pattern[0..=i]
        # - Start with failure[0] = 0
        # - Use two pointers: len (length of previous LPS) and i (current position)
        # - If pattern[i] == pattern[len], then failure[i] = len + 1
        # - Otherwise, backtrack using failure[len-1] until match or len = 0
        pass

    def search(self, text: str) -> List[int]:
        """Find all occurrences of pattern in text"""
        # TODO: Find all occurrences of pattern in text
        # - Use two pointers: i for text, j for pattern
        # - When mismatch occurs, use failure function to determine next j
        # - j = failure[j-1] instead of resetting to 0
        # - When j reaches pattern length, record match position
        # - Return list of starting positions of all matches
        pass

    def contains(self, text: str) -> bool:
        """Check if pattern appears in text (return early on first match)"""
        # TODO: Check if pattern appears in text (return early on first match)
        pass

    def first_occurrence(self, text: str) -> Optional[int]:
        """Return position of first occurrence, or None"""
        # TODO: Return position of first occurrence, or None
        pass

    def count_occurrences(self, text: str) -> int:
        """Count total number of occurrences (including overlapping)"""
        # TODO: Count total number of occurrences (including overlapping)
        pass

    def get_failure_function(self) -> List[int]:
        """Return the failure function"""
        return self.failure


import unittest


class TestKMP(unittest.TestCase):
    def test_failure_function_simple(self):
        kmp = KMP("ABABC")
        self.assertEqual(kmp.get_failure_function(), [0, 0, 1, 2, 0])

    def test_failure_function_repeated(self):
        kmp = KMP("AAAA")
        self.assertEqual(kmp.get_failure_function(), [0, 1, 2, 3])

    def test_failure_function_complex(self):
        kmp = KMP("AABAACAABAA")
        self.assertEqual(kmp.get_failure_function(), [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5])

    def test_simple_match(self):
        kmp = KMP("ABC")
        positions = kmp.search("XYZABCDEF")
        self.assertEqual(positions, [3])

    def test_multiple_matches(self):
        kmp = KMP("AB")
        positions = kmp.search("ABABAB")
        self.assertEqual(positions, [0, 2, 4])

    def test_overlapping_matches(self):
        kmp = KMP("AAA")
        positions = kmp.search("AAAAA")
        self.assertEqual(positions, [0, 1, 2])

    def test_no_match(self):
        kmp = KMP("XYZ")
        positions = kmp.search("ABCDEF")
        self.assertEqual(positions, [])

    def test_contains(self):
        kmp = KMP("world")
        self.assertTrue(kmp.contains("hello world"))
        self.assertFalse(kmp.contains("hello earth"))

    def test_first_occurrence(self):
        kmp = KMP("test")
        self.assertEqual(kmp.first_occurrence("this is a test string"), 10)
        self.assertIsNone(kmp.first_occurrence("no match here"))

    def test_count_occurrences(self):
        kmp = KMP("ana")
        self.assertEqual(kmp.count_occurrences("banana"), 2)
        self.assertEqual(kmp.count_occurrences("ananana"), 3)

    def test_pattern_longer_than_text(self):
        kmp = KMP("longpattern")
        self.assertEqual(kmp.search("short"), [])

    def test_single_character(self):
        kmp = KMP("a")
        positions = kmp.search("aaaaaa")
        self.assertEqual(positions, [0, 1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()
