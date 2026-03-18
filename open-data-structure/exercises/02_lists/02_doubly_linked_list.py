"""
Doubly Linked List
==================

A doubly linked list has nodes with pointers to both next AND previous nodes.
This allows O(1) deletion when you have a reference to a node.

Advantages over singly linked list:
- Can traverse backwards
- O(1) deletion with node reference
- O(1) add_last with tail pointer

Disadvantages:
- More memory (extra pointer per node)
- More complex code

Operations:
- add_first(x): Add to front - O(1)
- add_last(x): Add to end - O(1) with tail pointer
- remove_first(): Remove from front - O(1)
- remove_last(): Remove from end - O(1) with tail pointer
- remove_node(node): Remove specific node - O(1)
"""


class Node:
    """A node in a doubly linked list"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    A doubly linked list implementation with head and tail pointers.
    """

    def __init__(self):
        """Initialize an empty list"""
        # TODO: Initialize head and tail pointers
        # Optional: Track size
        pass

    def add_first(self, data):
        """
        Add a new node at the beginning.

        Args:
            data: The data to add

        Time Complexity: O(1)
        """
        # TODO: Create new node and update pointers
        # Don't forget to update tail if list was empty!
        pass

    def add_last(self, data):
        """
        Add a new node at the end.

        Args:
            data: The data to add

        Time Complexity: O(1)
        """
        # TODO: Create new node and update tail pointer
        # Don't forget to update head if list was empty!
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
        # TODO: Remove head node and update pointers
        pass

    def remove_last(self):
        """
        Remove and return the last element.

        Returns:
            The data from the removed node

        Raises:
            IndexError: If the list is empty

        Time Complexity: O(1)
        """
        # TODO: Remove tail node and update pointers
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

        Time Complexity: O(1) if tracking size
        """
        # TODO: Return the size
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

def test_add_first_and_last():
    """Test adding to both ends"""
    lst = DoublyLinkedList()
    lst.add_first(2)
    lst.add_first(1)
    lst.add_last(3)
    lst.add_last(4)

    assert lst.to_list() == [1, 2, 3, 4]


def test_remove_first():
    """Test removing from the front"""
    lst = DoublyLinkedList()
    lst.add_last(1)
    lst.add_last(2)
    lst.add_last(3)

    assert lst.remove_first() == 1
    assert lst.remove_first() == 2
    assert lst.to_list() == [3]


def test_remove_last():
    """Test removing from the end"""
    lst = DoublyLinkedList()
    lst.add_last(1)
    lst.add_last(2)
    lst.add_last(3)

    assert lst.remove_last() == 3
    assert lst.remove_last() == 2
    assert lst.to_list() == [1]


def test_find():
    """Test finding elements"""
    lst = DoublyLinkedList()
    lst.add_last(10)
    lst.add_last(20)
    lst.add_last(30)

    assert lst.find(20) == True
    assert lst.find(40) == False


def test_size():
    """Test size operation"""
    lst = DoublyLinkedList()
    assert lst.size() == 0

    lst.add_last(1)
    lst.add_last(2)
    assert lst.size() == 2

    lst.remove_first()
    assert lst.size() == 1


def test_single_element():
    """Test operations on single element list"""
    lst = DoublyLinkedList()
    lst.add_first(42)

    assert lst.size() == 1
    assert lst.remove_last() == 42
    assert lst.is_empty() == True


def test_remove_from_empty():
    """Test removing from empty list"""
    lst = DoublyLinkedList()

    try:
        lst.remove_first()
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        lst.remove_last()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
