"""
Suffix Array
============

A suffix array stores sorted suffixes of a string.
More space-efficient than suffix tree, easier to implement.

For string "banana":
Suffixes: banana, anana, nana, ana, na, a
Sorted suffixes: a, ana, anana, banana, na, nana
Suffix array: [5, 3, 1, 0, 4, 2] (starting indices)

Operations:
- Build suffix array: O(n log n) with optimization
- Pattern search: O(m log n) where m = pattern length
- LCP (Longest Common Prefix): O(n) to build

Applications:
- DNA sequence analysis
- Text compression
- Full-text indexing
- Finding repeated substrings
- Burrows-Wheeler Transform
"""


def build_suffix_array(text: str) -> list:
    """
    Build suffix array for given text.

    Args:
        text: The input text

    Returns:
        Suffix array (list of starting indices)

    Time Complexity: O(n log² n)
    """
    # TODO: Build suffix array
    # Simple approach:
    # 1. Create list of (suffix, index) pairs
    # 2. Sort by suffix
    # 3. Extract indices
    #
    # Advanced: Use SA-IS algorithm for O(n)
    pass


def build_lcp_array(text: str, suffix_array: list) -> list:
    """
    Build LCP (Longest Common Prefix) array.

    LCP[i] = length of longest common prefix between
    suffix_array[i] and suffix_array[i-1]

    Args:
        text: The input text
        suffix_array: The suffix array

    Returns:
        LCP array

    Time Complexity: O(n)
    """
    # TODO: Build LCP array using Kasai's algorithm
    # Uses the property that LCP values decrease by at most 1
    pass


def search_pattern(text: str, suffix_array: list, pattern: str) -> list:
    """
    Find all occurrences of pattern using suffix array.

    Args:
        text: The text to search in
        suffix_array: The suffix array of text
        pattern: The pattern to find

    Returns:
        List of starting positions

    Time Complexity: O(m log n) where m = len(pattern)
    """
    # TODO: Binary search for pattern in sorted suffixes
    # Find leftmost and rightmost occurrences
    # Return all indices in that range
    pass


def find_longest_repeated_substring(text: str) -> str:
    """
    Find the longest substring that appears at least twice.

    Args:
        text: The input text

    Returns:
        Longest repeated substring

    Time Complexity: O(n log n)
    """
    # TODO: Use suffix array + LCP array
    # The longest repeated substring is the maximum LCP value
    # Find max LCP and extract substring
    pass


def count_distinct_substrings(text: str) -> int:
    """
    Count number of distinct substrings.

    Args:
        text: The input text

    Returns:
        Number of distinct substrings

    Time Complexity: O(n log n)
    """
    # TODO: Use suffix array + LCP array
    # Total substrings = n*(n+1)/2
    # Subtract sum of LCP values to get distinct count
    pass


def find_longest_common_substring(s1: str, s2: str) -> str:
    """
    Find longest common substring of two strings.

    Args:
        s1: First string
        s2: Second string

    Returns:
        Longest common substring

    Time Complexity: O((n+m) log(n+m))
    """
    # TODO: Concatenate s1 + "$" + s2
    # Build suffix array and LCP
    # Find max LCP where adjacent suffixes come from different strings
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_build_suffix_array():
    """Test suffix array construction"""
    sa = build_suffix_array("banana")
    # Sorted suffixes: a, ana, anana, banana, na, nana
    assert sa == [5, 3, 1, 0, 4, 2]

    sa = build_suffix_array("abab")
    # Suffixes: abab, bab, ab, b
    # Sorted: ab, abab, b, bab
    assert sa == [2, 0, 3, 1]


def test_build_lcp_array():
    """Test LCP array construction"""
    text = "banana"
    sa = build_suffix_array(text)
    lcp = build_lcp_array(text, sa)

    # LCP between consecutive sorted suffixes
    # a vs ana: 1
    # ana vs anana: 3
    # anana vs banana: 0
    # banana vs na: 0
    # na vs nana: 2
    assert lcp == [0, 1, 3, 0, 0, 2]


def test_search_pattern():
    """Test pattern searching"""
    text = "banana"
    sa = build_suffix_array(text)

    positions = search_pattern(text, sa, "ana")
    assert set(positions) == {1, 3}  # "ana" at indices 1 and 3

    positions = search_pattern(text, sa, "na")
    assert set(positions) == {2, 4}


def test_longest_repeated_substring():
    """Test finding longest repeated substring"""
    assert find_longest_repeated_substring("banana") == "ana"
    assert find_longest_repeated_substring("abcabcabc") == "abcabc"
    assert find_longest_repeated_substring("abcd") == ""  # No repetition


def test_count_distinct_substrings():
    """Test counting distinct substrings"""
    # "abc": a, b, c, ab, bc, abc = 6 distinct
    assert count_distinct_substrings("abc") == 6

    # "aa": a, aa (note: only one 'a', not two)
    assert count_distinct_substrings("aa") == 2


def test_longest_common_substring():
    """Test finding longest common substring"""
    lcs = find_longest_common_substring("abcdef", "xbcde")
    assert lcs == "bcde"

    lcs = find_longest_common_substring("hello", "world")
    assert lcs in ["o", "l"]  # Either is valid


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
