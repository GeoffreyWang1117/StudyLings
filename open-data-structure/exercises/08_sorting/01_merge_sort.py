"""
Merge Sort
==========

Divide and conquer sorting algorithm.

Algorithm:
1. Divide array in half
2. Recursively sort each half
3. Merge the sorted halves

Time: O(n log n) - guaranteed
Space: O(n) - for temporary arrays

Properties:
- Stable
- Not in-place
- Consistent O(n log n)
"""


def merge_sort(arr: list) -> list:
    """
    Sort array using merge sort.

    Args:
        arr: Array to sort

    Returns:
        Sorted array

    Time Complexity: O(n log n)
    """
    # TODO: Implement merge sort
    # Base case: array of size 0 or 1 is sorted
    # Recursive case: split, sort halves, merge
    pass


def merge(left: list, right: list) -> list:
    """
    Merge two sorted arrays.

    Args:
        left: Sorted left array
        right: Sorted right array

    Returns:
        Merged sorted array

    Time Complexity: O(n)
    """
    # TODO: Merge two sorted arrays
    # Use two pointers
    pass


# Tests
def test_merge_sort():
    assert merge_sort([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
