"""
Counting Sort
=============

Non-comparison sort for integers in limited range.

Algorithm:
1. Count frequency of each value
2. Calculate cumulative counts
3. Place items in sorted order

Time: O(n + k) where k is range
Space: O(k)

Only works for non-negative integers!
"""


def counting_sort(arr: list) -> list:
    """Sort using counting sort"""
    # TODO: Implement counting sort
    pass


# Tests
def test_counting_sort():
    assert counting_sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
