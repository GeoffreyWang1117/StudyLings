"""
Singly Linked List
==================

A linked list stores elements in nodes, where each node points to the next.
Unlike arrays, linked lists don't require contiguous memory.

Advantages over arrays:
- O(1) insertion/deletion at the front
- No need to shift elements
- Dynamic size without resizing

Disadvantages:
- O(n) access to arbitrary elements
- Extra memory for pointers
- Poor cache locality

Operations:
- add_first(x): Add to front - O(1)
- add_last(x): Add to end - O(n) without tail pointer, O(1) with tail
- remove_first(): Remove from front - O(1)
- find(x): Search for element - O(n)
"""


class Node:
    """A node in a singly linked list"""

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """
    A singly linked list implementation.
    """

    def __init__(self):
        """Initialize an empty list"""
        # TODO: Initialize head pointer
        # Optional: Also track size
        pass

    def add_first(self, data):
        """
        Add a new node at the beginning.

        Args:
            data: The data to add

        Time Complexity: O(1)
        """
        # TODO: Create new node and make it the new head
        pass

    def add_last(self, data):
        """
        Add a new node at the end.

        Args:
            data: The data to add

        Time Complexity: O(n)
        """
        # TODO: Traverse to the end and add new node
        # Special case: empty list
        pass

    def remove_first(self):
        """
        Remove and return the first element.

        Returns:
            The data from the removed node

        Raises:
            IndexError: If the list is empty

        Time Complexity: O(1)
        """
        # TODO: Remove the head node
        pass

    def find(self, data) -> bool:
        """
        Check if the list contains the given data.

        Args:
            data: The data to search for

        Returns:
            True if found, False otherwise

        Time Complexity: O(n)
        """
        # TODO: Traverse the list looking for data
        pass

    def size(self) -> int:
        """
        Get the number of elements.

        Returns:
            Number of elements

        Time Complexity: O(n) if not tracking size, O(1) if tracking
        """
        # TODO: Count the nodes
        pass

    def is_empty(self) -> bool:
        """
        Check if the list is empty.

        Returns:
            True if empty, False otherwise

        Time Complexity: O(1)
        """
        # TODO: Check if head is None
        pass

    def to_list(self) -> list:
        """
        Convert to a Python list (for testing).

        Returns:
            List of all elements in order

        Time Complexity: O(n)
        """
        # TODO: Traverse and collect all data
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_add_first():
    """Test adding to the front"""
    lst = SinglyLinkedList()
    lst.add_first(3)
    lst.add_first(2)
    lst.add_first(1)

    assert lst.to_list() == [1, 2, 3]


def test_add_last():
    """Test adding to the end"""
    lst = SinglyLinkedList()
    lst.add_last(1)
    lst.add_last(2)
    lst.add_last(3)

    assert lst.to_list() == [1, 2, 3]


def test_remove_first():
    """Test removing from the front"""
    lst = SinglyLinkedList()
    lst.add_last(1)
    lst.add_last(2)
    lst.add_last(3)

    assert lst.remove_first() == 1
    assert lst.remove_first() == 2
    assert lst.to_list() == [3]


def test_find():
    """Test finding elements"""
    lst = SinglyLinkedList()
    lst.add_last(10)
    lst.add_last(20)
    lst.add_last(30)

    assert lst.find(20) == True
    assert lst.find(40) == False


def test_size():
    """Test size operation"""
    lst = SinglyLinkedList()
    assert lst.size() == 0

    lst.add_last(1)
    lst.add_last(2)
    assert lst.size() == 2


def test_is_empty():
    """Test is_empty operation"""
    lst = SinglyLinkedList()
    assert lst.is_empty() == True

    lst.add_first(1)
    assert lst.is_empty() == False


def test_remove_first_empty():
    """Test removing from empty list"""
    lst = SinglyLinkedList()
    try:
        lst.remove_first()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
