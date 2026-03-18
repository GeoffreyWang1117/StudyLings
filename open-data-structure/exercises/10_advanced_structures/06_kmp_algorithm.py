"""
KMP String Matching Algorithm
==============================

Knuth-Morris-Pratt algorithm finds pattern in text efficiently.

Key idea: When mismatch occurs, use information from previous matches
to avoid re-comparing characters we already know match.

Uses a "failure function" (LPS array):
- LPS[i] = length of longest proper prefix which is also suffix
- Allows skipping characters during mismatch

Operations:
- build_lps(pattern): Build failure function - O(m)
- search(text, pattern): Find all occurrences - O(n + m)

Where n = len(text), m = len(pattern)

Compared to naive O(n*m), KMP is O(n+m).

Applications:
- Text editors (search/replace)
- DNA sequence matching
- Plagiarism detection
- Network packet inspection
"""


def build_lps(pattern: str) -> list:
    """
    Build the Longest Proper Prefix which is also Suffix array.

    For pattern "ABABC":
    - LPS = [0, 0, 1, 2, 0]

    Args:
        pattern: The pattern string

    Returns:
        LPS array

    Time Complexity: O(m) where m = len(pattern)
    """
    # TODO: Build LPS array
    # lps[0] = 0 (no proper prefix for single char)
    # For i from 1 to len(pattern)-1:
    #   Find longest proper prefix that matches suffix ending at i
    pass


def kmp_search(text: str, pattern: str) -> list:
    """
    Find all occurrences of pattern in text using KMP.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        List of starting indices where pattern occurs

    Time Complexity: O(n + m)
    """
    # TODO: Implement KMP search
    # 1. Build LPS array for pattern
    # 2. Use two pointers: i for text, j for pattern
    # 3. When match: advance both
    # 4. When mismatch: use LPS to skip comparisons
    #    - If j > 0: j = lps[j-1]
    #    - Else: i += 1
    # 5. When j == len(pattern): found match, record index
    pass


def count_pattern_occurrences(text: str, pattern: str) -> int:
    """
    Count number of times pattern appears in text.

    Args:
        text: The text
        pattern: The pattern

    Returns:
        Number of occurrences

    Time Complexity: O(n + m)
    """
    # TODO: Use kmp_search and return count
    pass


def find_repeating_substring(s: str) -> str:
    """
    Find the shortest repeating substring.

    For "abcabcabc" returns "abc"
    For "abab" returns "ab"

    Uses LPS array property.

    Args:
        s: The string

    Returns:
        Shortest repeating substring, or empty if no repetition

    Time Complexity: O(n)
    """
    # TODO: Use LPS array
    # If len(s) % (len(s) - lps[-1]) == 0:
    #   String is made of repetitions
    #   Repeating part = s[: len(s) - lps[-1]]
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_build_lps():
    """Test LPS array construction"""
    assert build_lps("ABABC") == [0, 0, 1, 2, 0]
    assert build_lps("AAAA") == [0, 1, 2, 3]
    assert build_lps("ABCD") == [0, 0, 0, 0]
    assert build_lps("AABAACAABAA") == [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]


def test_kmp_search():
    """Test KMP pattern matching"""
    text = "ABABDABACDABABCABAB"
    pattern = "ABABC"

    indices = kmp_search(text, pattern)
    assert 10 in indices  # Pattern at index 10

    # Test multiple occurrences
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    indices = kmp_search(text, pattern)
    assert len(indices) == 3  # Occurs 3 times


def test_kmp_no_match():
    """Test when pattern not found"""
    text = "ABABABABAB"
    pattern = "XYZ"

    indices = kmp_search(text, pattern)
    assert len(indices) == 0


def test_kmp_edge_cases():
    """Test edge cases"""
    # Pattern longer than text
    assert kmp_search("AB", "ABCD") == []

    # Empty pattern
    assert kmp_search("ABC", "") == []

    # Single character
    assert kmp_search("AAAAA", "A") == [0, 1, 2, 3, 4]


def test_count_occurrences():
    """Test counting pattern occurrences"""
    assert count_pattern_occurrences("AABAACAADAABAABA", "AABA") == 3
    assert count_pattern_occurrences("ABABABAB", "AB") == 4
    assert count_pattern_occurrences("HELLO", "LL") == 1


def test_repeating_substring():
    """Test finding repeating substring"""
    assert find_repeating_substring("abcabcabc") == "abc"
    assert find_repeating_substring("abababab") == "ab"
    assert find_repeating_substring("aaaa") == "a"
    assert find_repeating_substring("abcd") == ""  # No repetition


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
