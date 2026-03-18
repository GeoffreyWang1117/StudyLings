# I AM NOT DONE

"""
Exercise: Simple Regex Engine

Implement a basic regular expression engine supporting common operators.

Supported operators:
- . (any character)
- * (zero or more of previous)
- + (one or more of previous)
- ? (zero or one of previous)
- [] (character class)
- ^ (start of string)
- $ (end of string)

Your task: Implement basic regex matching.
"""

from typing import Optional


class RegexEngine:
    """Simple regex matching engine"""

    @staticmethod
    def match(pattern: str, text: str) -> bool:
        """Match pattern against entire text"""
        # TODO: Implement regex matching
        # - Handle all supported operators
        # - Use recursive or DP approach
        pass

    @staticmethod
    def search(pattern: str, text: str) -> Optional[int]:
        """Find first occurrence of pattern in text"""
        # TODO: Find first occurrence
        pass

    @staticmethod
    def match_char(pattern_char: str, text_char: str) -> bool:
        """Match single character or '.'"""
        # TODO: Match single character
        pass


import unittest


class TestRegexEngine(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(RegexEngine.match("hello", "hello"))
        self.assertFalse(RegexEngine.match("hello", "world"))

    def test_dot_wildcard(self):
        self.assertTrue(RegexEngine.match("h.llo", "hello"))
        self.assertTrue(RegexEngine.match("h.llo", "hallo"))

    def test_star_operator(self):
        self.assertTrue(RegexEngine.match("a*b", "b"))
        self.assertTrue(RegexEngine.match("a*b", "ab"))
        self.assertTrue(RegexEngine.match("a*b", "aaab"))

    def test_plus_operator(self):
        self.assertFalse(RegexEngine.match("a+b", "b"))
        self.assertTrue(RegexEngine.match("a+b", "ab"))
        self.assertTrue(RegexEngine.match("a+b", "aaab"))

    def test_question_operator(self):
        self.assertTrue(RegexEngine.match("a?b", "b"))
        self.assertTrue(RegexEngine.match("a?b", "ab"))
        self.assertFalse(RegexEngine.match("a?b", "aab"))

    def test_start_anchor(self):
        self.assertTrue(RegexEngine.match("^hello", "hello"))
        self.assertFalse(RegexEngine.match("^hello", "say hello"))

    def test_end_anchor(self):
        self.assertTrue(RegexEngine.match("world$", "world"))
        self.assertFalse(RegexEngine.match("world$", "world!"))


if __name__ == '__main__':
    unittest.main()
