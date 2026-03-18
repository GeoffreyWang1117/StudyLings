"""
Heap Sort
=========

Heap sort uses a binary heap to sort in O(n log n) time.

Algorithm:
1. Build a max heap from the array - O(n)
2. Repeatedly extract max and place at end - O(n log n)

Properties:
- Time: O(n log n) worst case
- Space: O(1) (in-place)
- Not stable
- Not adaptive

Comparison with other O(n log n) sorts:
- Merge sort: O(n) space, stable
- Quick sort: O(n^2) worst case, but faster average
- Heap sort: O(1) space, O(n log n) guaranteed
"""


def heap_sort(arr: list) -> list:
    """
    Sort array using heap sort.

    Args:
        arr: Array to sort

    Returns:
        Sorted array

    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    # TODO: Implement heap sort
    # 1. Build max heap
    # 2. Repeatedly swap root with last element and heapify
    pass


def heapify(arr: list, n: int, i: int):
    """
    Heapify subtree rooted at index i.

    Args:
        arr: The array
        n: Size of heap
        i: Root of subtree

    Time Complexity: O(log n)
    """
    # TODO: Implement heapify (max heap)
    # Compare with children and swap with largest
    pass


def build_heap(arr: list):
    """
    Build a max heap from array.

    Args:
        arr: The array

    Time Complexity: O(n)
    """
    # TODO: Implement build_heap
    # Start from last non-leaf and heapify each node
    # Last non-leaf: (len(arr) // 2) - 1
    pass


def find_kth_largest(arr: list, k: int):
    """
    Find the kth largest element using a heap.

    Example:
        find_kth_largest([3, 2, 1, 5, 6, 4], 2) -> 5

    Args:
        arr: Array of integers
        k: Which largest element (1-indexed)

    Returns:
        The kth largest element

    Time Complexity: O(n + k log n)
    """
    # TODO: Build max heap and extract k times
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_heap_sort():
    """Test heap sort"""
    arr = [64, 34, 25, 12, 22, 11, 90]
    result = heap_sort(arr.copy())
    assert result == sorted(arr)


def test_heap_sort_edge_cases():
    """Test edge cases"""
    assert heap_sort([]) == []
    assert heap_sort([1]) == [1]
    assert heap_sort([2, 1]) == [1, 2]
    assert heap_sort([1, 1, 1]) == [1, 1, 1]


def test_heap_sort_reverse():
    """Test sorting reverse sorted array"""
    arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    assert heap_sort(arr) == list(range(1, 10))


def test_heap_sort_random():
    """Test with random order"""
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    assert heap_sort(arr) == sorted(arr)


def test_find_kth_largest():
    """Test finding kth largest"""
    arr = [3, 2, 1, 5, 6, 4]

    assert find_kth_largest(arr, 1) == 6  # Largest
    assert find_kth_largest(arr, 2) == 5  # 2nd largest
    assert find_kth_largest(arr, 3) == 4  # 3rd largest


def test_heapify():
    """Test heapify function"""
    arr = [1, 3, 5, 4, 6, 13, 10, 9, 8, 15, 17]
    n = len(arr)

    # Heapify should fix heap property
    heapify(arr, n, 0)

    # After heapify, parent should be >= children
    if n > 1:
        assert arr[0] >= arr[1]
    if n > 2:
        assert arr[0] >= arr[2]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
