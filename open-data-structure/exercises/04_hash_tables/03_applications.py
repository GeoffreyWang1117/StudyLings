"""
Hash Table Applications
========================

Hash tables are incredibly useful for many problems.
Let's implement some common applications.

Applications covered:
1. Frequency counting
2. Two-sum problem
3. First unique character
4. Group anagrams
"""


def count_frequency(items: list) -> dict:
    """
    Count the frequency of each item.

    Example:
        count_frequency([1, 2, 2, 3, 3, 3]) -> {1: 1, 2: 2, 3: 3}

    Args:
        items: List of items

    Returns:
        Dictionary mapping items to their frequencies

    Time Complexity: O(n)
    """
    # TODO: Use a dictionary to count frequencies
    pass


def two_sum(nums: list, target: int) -> tuple:
    """
    Find two numbers that add up to target.

    Example:
        two_sum([2, 7, 11, 15], 9) -> (0, 1)  # nums[0] + nums[1] = 9

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        Tuple of (index1, index2) or None if not found

    Time Complexity: O(n) with hash table
    """
    # TODO: Use a hash table to find complement
    # For each number x, check if (target - x) exists
    pass


def first_unique_char(s: str) -> str:
    """
    Find the first character that appears only once.

    Example:
        first_unique_char("leetcode") -> "l"
        first_unique_char("loveleetcode") -> "v"

    Args:
        s: Input string

    Returns:
        First unique character, or None if no unique char

    Time Complexity: O(n)
    """
    # TODO: Two passes:
    # 1. Count frequency of each character
    # 2. Find first character with frequency 1
    pass


def group_anagrams(words: list) -> list:
    """
    Group words that are anagrams of each other.

    Example:
        group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

    Args:
        words: List of words

    Returns:
        List of groups (each group is a list of anagrams)

    Time Complexity: O(n * k log k) where k is max word length
    """
    # TODO: Use a hash table
    # Key: sorted characters (anagrams have same sorted form)
    # Value: list of words with that key
    pass


def has_duplicate(nums: list) -> bool:
    """
    Check if array has any duplicates.

    Example:
        has_duplicate([1, 2, 3, 1]) -> True
        has_duplicate([1, 2, 3, 4]) -> False

    Args:
        nums: List of numbers

    Returns:
        True if there are duplicates

    Time Complexity: O(n)
    """
    # TODO: Use a set to track seen numbers
    pass


def longest_consecutive(nums: list) -> int:
    """
    Find the length of the longest consecutive sequence.

    Example:
        longest_consecutive([100, 4, 200, 1, 3, 2]) -> 4
        # The sequence is [1, 2, 3, 4]

    Args:
        nums: List of integers

    Returns:
        Length of longest consecutive sequence

    Time Complexity: O(n)
    """
    # TODO: Use a set for O(1) lookups
    # For each number that starts a sequence, count length
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_count_frequency():
    """Test frequency counting"""
    assert count_frequency([1, 2, 2, 3, 3, 3]) == {1: 1, 2: 2, 3: 3}
    assert count_frequency(['a', 'b', 'a']) == {'a': 2, 'b': 1}
    assert count_frequency([]) == {}


def test_two_sum():
    """Test two sum problem"""
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([1, 2, 3], 10) == None


def test_first_unique_char():
    """Test first unique character"""
    assert first_unique_char("leetcode") == "l"
    assert first_unique_char("loveleetcode") == "v"
    assert first_unique_char("aabb") == None


def test_group_anagrams():
    """Test grouping anagrams"""
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])

    # Convert to sets for comparison (order doesn't matter)
    result_sets = [set(group) for group in result]

    assert set(["eat", "tea", "ate"]) in result_sets
    assert set(["tan", "nat"]) in result_sets
    assert set(["bat"]) in result_sets


def test_has_duplicate():
    """Test duplicate detection"""
    assert has_duplicate([1, 2, 3, 1]) == True
    assert has_duplicate([1, 2, 3, 4]) == False
    assert has_duplicate([]) == False


def test_longest_consecutive():
    """Test longest consecutive sequence"""
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
