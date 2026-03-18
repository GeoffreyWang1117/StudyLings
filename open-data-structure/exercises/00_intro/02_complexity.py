"""
Big-O Notation and Complexity Analysis
=======================================

Understanding time and space complexity is crucial for analyzing data structures.

In this exercise, you'll implement functions and identify their complexity.
"""


def find_max(arr: list) -> int:
    """
    Find the maximum element in an array.

    Time Complexity: O(?)  # TODO: Fill in the complexity
    Space Complexity: O(?) # TODO: Fill in the complexity

    Args:
        arr: A non-empty list of integers

    Returns:
        The maximum element
    """
    # TODO: Implement this function
    # Hint: You need to check every element
    pass


def has_duplicates(arr: list) -> bool:
    """
    Check if an array has any duplicate elements.

    Time Complexity: O(?)  # TODO: Fill in the complexity
    Space Complexity: O(?) # TODO: Fill in the complexity

    Args:
        arr: A list of integers

    Returns:
        True if there are duplicates, False otherwise
    """
    # TODO: Implement this function using a set
    # Hint: Sets have O(1) lookup time
    pass


def sum_pairs(arr: list) -> int:
    """
    Calculate the sum of all possible pairs in the array.

    For example: [1, 2, 3] -> (1+2) + (1+3) + (2+3) = 12

    Time Complexity: O(?)  # TODO: Fill in the complexity
    Space Complexity: O(?) # TODO: Fill in the complexity

    Args:
        arr: A list of integers

    Returns:
        Sum of all pairs
    """
    # TODO: Implement this function
    # Hint: You need nested loops
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_find_max():
    """Test find_max function"""
    assert find_max([1, 5, 3, 9, 2]) == 9
    assert find_max([1]) == 1
    assert find_max([-5, -2, -10, -1]) == -1
    assert find_max([7, 7, 7]) == 7


def test_has_duplicates():
    """Test has_duplicates function"""
    assert has_duplicates([1, 2, 3, 2]) == True
    assert has_duplicates([1, 2, 3, 4]) == False
    assert has_duplicates([]) == False
    assert has_duplicates([5, 5]) == True
    assert has_duplicates([1, 2, 3, 4, 5, 1]) == True


def test_sum_pairs():
    """Test sum_pairs function"""
    assert sum_pairs([1, 2, 3]) == 12  # (1+2) + (1+3) + (2+3)
    assert sum_pairs([1, 1]) == 2       # (1+1)
    assert sum_pairs([1]) == 0          # No pairs
    assert sum_pairs([]) == 0           # No pairs
    assert sum_pairs([1, 2, 3, 4]) == 20  # All pairs


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
