# I AM NOT DONE

"""
Exercise: Aho-Corasick Algorithm

Aho-Corasick is a string matching algorithm for finding multiple patterns simultaneously.
Uses a trie structure with failure links for efficient multi-pattern matching.

Time Complexity: O(n + m + z) where n is text length, m is total pattern length, z is matches
Space Complexity: O(m * σ) where σ is alphabet size

Key concepts:
- Build trie of all patterns
- Add failure links for efficient backtracking
- Single pass through text finds all patterns
- Used in antivirus, intrusion detection, search engines

Your task: Implement Aho-Corasick multi-pattern matching.
"""

from typing import List, Dict, Set, Tuple
from collections import deque, defaultdict


class AhoCorasick:
    """Aho-Corasick multi-pattern matching"""

    def __init__(self, patterns: List[str]):
        self.patterns = patterns
        self.goto = {}  # Trie transitions
        self.fail = {}  # Failure links
        self.output = defaultdict(list)  # Output patterns at each state
        self._build_automaton()

    def _build_automaton(self):
        """Build trie and failure links"""
        # TODO: Build Aho-Corasick automaton
        # 1. Build trie (goto function)
        # 2. Build failure links using BFS
        # 3. Build output function
        pass

    def search(self, text: str) -> List[Tuple[int, str]]:
        """Find all pattern occurrences in text"""
        # TODO: Find all pattern occurrences in text
        # - Traverse automaton following text
        # - Use goto and fail functions
        # - Record all matches from output function
        # - Return list of (position, pattern) tuples
        pass

    def search_all_positions(self, text: str) -> Dict[str, List[int]]:
        """Return dictionary mapping each pattern to its match positions"""
        # TODO: Return dictionary mapping each pattern to its match positions
        pass


import unittest


class TestAhoCorasick(unittest.TestCase):
    def test_single_pattern(self):
        ac = AhoCorasick(["he"])
        matches = ac.search("she")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][1], "he")

    def test_multiple_patterns(self):
        ac = AhoCorasick(["he", "she", "his", "hers"])
        matches = ac.search("ushers")
        patterns = [m[1] for m in matches]
        self.assertIn("she", patterns)
        self.assertIn("he", patterns)
        self.assertIn("hers", patterns)

    def test_overlapping_patterns(self):
        ac = AhoCorasick(["ab", "bc", "abc"])
        matches = ac.search("abc")
        self.assertEqual(len(matches), 3)

    def test_no_match(self):
        ac = AhoCorasick(["test"])
        matches = ac.search("no match here")
        self.assertEqual(len(matches), 0)

    def test_search_all_positions(self):
        ac = AhoCorasick(["the", "he"])
        result = ac.search_all_positions("the weather is nice")
        self.assertIn("the", result)
        self.assertEqual(result["the"], [0])

    def test_repeated_patterns(self):
        ac = AhoCorasick(["a"])
        result = ac.search_all_positions("aaa")
        self.assertEqual(result["a"], [0, 1, 2])

    def test_case_sensitive(self):
        ac = AhoCorasick(["The"])
        matches = ac.search("the")
        self.assertEqual(len(matches), 0)

    def test_empty_pattern_list(self):
        ac = AhoCorasick([])
        matches = ac.search("any text")
        self.assertEqual(len(matches), 0)


if __name__ == '__main__':
    unittest.main()
