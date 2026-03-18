"""
Aho-Corasick Automaton
======================

Aho-Corasick algorithm efficiently finds multiple patterns in text
simultaneously. Extension of KMP to multiple patterns.

Structure:
- Trie of all patterns
- Failure links (like KMP failure function)
- Output links to find all matches

Operations:
- Build automaton: O(m) where m = total pattern length
- Search text: O(n + z) where n = text length, z = matches

Compared to running KMP for each pattern (O(k*n)), this is O(n).

Applications:
- Antivirus pattern matching
- Network intrusion detection (Snort)
- DNA sequence analysis
- Plagiarism detection
- Content filtering
- Log analysis
"""


from collections import deque


class ACNode:
    """A node in Aho-Corasick automaton"""

    def __init__(self):
        self.children = {}      # Character -> child node
        self.failure = None     # Failure link
        self.output = []        # Patterns ending at this node


class AhoCorasick:
    """
    Aho-Corasick multi-pattern matching automaton.
    """

    def __init__(self):
        """Initialize empty automaton"""
        self.root = ACNode()

    def add_pattern(self, pattern: str):
        """
        Add a pattern to the automaton.

        Args:
            pattern: Pattern string to add

        Time Complexity: O(m) where m = len(pattern)
        """
        # TODO: Add pattern to trie
        # Similar to trie insert
        # Mark last node with pattern
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = ACNode()
            node = node.children[char]
        node.output.append(pattern)

    def build(self):
        """
        Build failure links using BFS.

        Must be called after adding all patterns.

        Time Complexity: O(m) where m = total length of patterns
        """
        # TODO: Build failure links
        # Similar to KMP failure function but for trie
        # Use BFS level by level
        # For each node, find longest proper suffix that's in trie
        pass

    def search(self, text: str) -> list:
        """
        Find all pattern occurrences in text.

        Args:
            text: Text to search in

        Returns:
            List of (pattern, position) tuples

        Time Complexity: O(n + z) where z = number of matches
        """
        # TODO: Traverse automaton, following failure links on mismatch
        # Collect all patterns at each node (including via output links)
        results = []
        node = self.root

        for i, char in enumerate(text):
            # Follow failure links until we find a match or reach root
            while node != self.root and char not in node.children:
                node = node.failure

            if char in node.children:
                node = node.children[char]

            # Collect all patterns ending here
            # TODO: Also follow output links to find other matches
            temp = node
            while temp != self.root:
                for pattern in temp.output:
                    results.append((pattern, i - len(pattern) + 1))
                temp = temp.failure

        return results

    def contains_any(self, text: str) -> bool:
        """
        Check if text contains any of the patterns.

        Args:
            text: Text to check

        Returns:
            True if any pattern found

        Time Complexity: O(n)
        """
        # TODO: Early termination version of search
        pass

    def find_first(self, text: str) -> tuple:
        """
        Find first occurrence of any pattern.

        Args:
            text: Text to search

        Returns:
            (pattern, position) or None if no match

        Time Complexity: O(n)
        """
        # TODO: Return first match found
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_single_pattern():
    """Test with single pattern (like KMP)"""
    ac = AhoCorasick()
    ac.add_pattern("abc")
    ac.build()

    results = ac.search("xabcyabcz")
    patterns = [p for p, pos in results]

    assert patterns.count("abc") == 2


def test_multiple_patterns():
    """Test finding multiple patterns"""
    ac = AhoCorasick()
    patterns = ["he", "she", "his", "hers"]

    for p in patterns:
        ac.add_pattern(p)
    ac.build()

    text = "ahishers"
    results = ac.search(text)

    # Should find: "his" at 1, "she" at 3, "he" at 4, "hers" at 4
    found_patterns = [p for p, pos in results]
    assert "his" in found_patterns
    assert "she" in found_patterns
    assert "he" in found_patterns
    assert "hers" in found_patterns


def test_overlapping_patterns():
    """Test patterns that overlap"""
    ac = AhoCorasick()
    ac.add_pattern("abc")
    ac.add_pattern("bcd")
    ac.add_pattern("cde")
    ac.build()

    results = ac.search("abcde")
    patterns = [p for p, pos in results]

    assert "abc" in patterns
    assert "bcd" in patterns
    assert "cde" in patterns


def test_no_match():
    """Test when no patterns match"""
    ac = AhoCorasick()
    ac.add_pattern("abc")
    ac.add_pattern("def")
    ac.build()

    results = ac.search("xyz")
    assert len(results) == 0


def test_contains_any():
    """Test contains_any method"""
    ac = AhoCorasick()
    ac.add_pattern("virus")
    ac.add_pattern("malware")
    ac.add_pattern("trojan")
    ac.build()

    assert ac.contains_any("this file contains a virus") == True
    assert ac.contains_any("clean file") == False


def test_find_first():
    """Test finding first match"""
    ac = AhoCorasick()
    ac.add_pattern("abc")
    ac.add_pattern("xyz")
    ac.build()

    result = ac.find_first("123abc456xyz")
    assert result is not None
    assert result[0] == "abc"
    assert result[1] == 3


def test_case_sensitive():
    """Test that search is case-sensitive"""
    ac = AhoCorasick()
    ac.add_pattern("ABC")
    ac.build()

    results = ac.search("abc ABC")
    assert len(results) == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
