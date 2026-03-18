"""
Dynamic Array (ArrayList)
=========================

A dynamic array automatically grows when it runs out of space.
This is how Python's list is implemented internally.

Key insight: When the array is full, allocate a new array of double the size
and copy all elements. This gives O(1) amortized time for append.

Operations:
- append(x): Add element to end - O(1) amortized
- get(i): Get element at index i - O(1)
- set(i, x): Set element at index i - O(1)
- remove(i): Remove element at index i - O(n)
- size(): Get number of elements - O(1)

Applications:
- Foundation for most dynamic collections
- When you need indexed access with dynamic size
"""


class DynamicArray:
    """
    A resizable array that grows automatically.
    """

    def __init__(self):
        """Initialize an empty dynamic array"""
        # TODO: Initialize the array
        # Hint: Start with a small capacity (e.g., 1 or 2)
        # Track both capacity and actual size
        pass

    def append(self, item):
        """
        Add an item to the end of the array.

        Args:
            item: The item to add

        Time Complexity: O(1) amortized
        """
        # TODO: Implement append
        # If size == capacity, resize first!
        pass

    def get(self, index: int):
        """
        Get the element at the given index.

        Args:
            index: The index to access

        Returns:
            The element at that index

        Raises:
            IndexError: If index is out of bounds

        Time Complexity: O(1)
        """
        # TODO: Implement get
        pass

    def set(self, index: int, item):
        """
        Set the element at the given index.

        Args:
            index: The index to modify
            item: The new value

        Raises:
            IndexError: If index is out of bounds

        Time Complexity: O(1)
        """
        # TODO: Implement set
        pass

    def remove(self, index: int):
        """
        Remove the element at the given index.

        Args:
            index: The index to remove

        Returns:
            The removed element

        Raises:
            IndexError: If index is out of bounds

        Time Complexity: O(n)
        """
        # TODO: Implement remove
        # Shift all elements after index to the left
        pass

    def size(self) -> int:
        """
        Get the number of elements.

        Returns:
            Number of elements

        Time Complexity: O(1)
        """
        # TODO: Implement size
        pass

    def capacity(self) -> int:
        """
        Get the current capacity.

        Returns:
            Current capacity

        Time Complexity: O(1)
        """
        # TODO: Implement capacity
        pass

    def _resize(self, new_capacity: int):
        """
        Resize the internal array to new_capacity.

        Args:
            new_capacity: The new capacity

        Time Complexity: O(n)
        """
        # TODO: Implement resize
        # Create new array and copy elements
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_append():
    """Test append operation"""
    arr = DynamicArray()
    arr.append(1)
    arr.append(2)
    arr.append(3)

    assert arr.size() == 3
    assert arr.get(0) == 1
    assert arr.get(1) == 2
    assert arr.get(2) == 3


def test_get_and_set():
    """Test get and set operations"""
    arr = DynamicArray()
    arr.append(10)
    arr.append(20)
    arr.append(30)

    assert arr.get(1) == 20
    arr.set(1, 25)
    assert arr.get(1) == 25


def test_remove():
    """Test remove operation"""
    arr = DynamicArray()
    arr.append(1)
    arr.append(2)
    arr.append(3)
    arr.append(4)

    removed = arr.remove(1)  # Remove 2
    assert removed == 2
    assert arr.size() == 3
    assert arr.get(0) == 1
    assert arr.get(1) == 3  # 3 shifted left
    assert arr.get(2) == 4


def test_resize():
    """Test that array resizes correctly"""
    arr = DynamicArray()
    initial_capacity = arr.capacity()

    # Add enough elements to trigger resize
    for i in range(20):
        arr.append(i)

    assert arr.capacity() > initial_capacity
    assert arr.size() == 20

    # Verify all elements are still there
    for i in range(20):
        assert arr.get(i) == i


def test_index_error():
    """Test that invalid indices raise errors"""
    arr = DynamicArray()
    arr.append(1)
    arr.append(2)

    try:
        arr.get(5)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        arr.set(5, 10)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        arr.remove(5)
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
