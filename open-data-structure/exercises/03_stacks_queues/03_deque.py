"""
Deque (Double-Ended Queue)
===========================

A deque (pronounced "deck") allows insertion and deletion from both ends.

Operations (all O(1)):
- add_first(x): Add to front
- add_last(x): Add to back
- remove_first(): Remove from front
- remove_last(): Remove from back

Implementation options:
- Doubly linked list
- Circular array

Applications:
- Sliding window problems
- Palindrome checking
- Browser history (back/forward)
- Task scheduling
"""


class Deque:
    """
    Deque implementation using a doubly linked list.
    """

    class Node:
        """A node in the deque"""
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        """Initialize an empty deque"""
        # TODO: Initialize head, tail, and size
        pass

    def add_first(self, item):
        """
        Add an item to the front.

        Args:
            item: The item to add

        Time Complexity: O(1)
        """
        # TODO: Add to front
        pass

    def add_last(self, item):
        """
        Add an item to the back.

        Args:
            item: The item to add

        Time Complexity: O(1)
        """
        # TODO: Add to back
        pass

    def remove_first(self):
        """
        Remove and return the front item.

        Returns:
            The front item

        Raises:
            IndexError: If deque is empty

        Time Complexity: O(1)
        """
        # TODO: Remove from front
        pass

    def remove_last(self):
        """
        Remove and return the back item.

        Returns:
            The back item

        Raises:
            IndexError: If deque is empty

        Time Complexity: O(1)
        """
        # TODO: Remove from back
        pass

    def peek_first(self):
        """
        Return the front item without removing.

        Returns:
            The front item

        Raises:
            IndexError: If deque is empty

        Time Complexity: O(1)
        """
        # TODO: Return front item
        pass

    def peek_last(self):
        """
        Return the back item without removing.

        Returns:
            The back item

        Raises:
            IndexError: If deque is empty

        Time Complexity: O(1)
        """
        # TODO: Return back item
        pass

    def is_empty(self) -> bool:
        """Check if deque is empty"""
        # TODO: Implement
        pass

    def size(self) -> int:
        """Get number of items"""
        # TODO: Implement
        pass

    def to_list(self) -> list:
        """Convert to list (for testing)"""
        # TODO: Traverse from head to tail
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_add_first():
    """Test adding to front"""
    dq = Deque()
    dq.add_first(3)
    dq.add_first(2)
    dq.add_first(1)

    assert dq.to_list() == [1, 2, 3]


def test_add_last():
    """Test adding to back"""
    dq = Deque()
    dq.add_last(1)
    dq.add_last(2)
    dq.add_last(3)

    assert dq.to_list() == [1, 2, 3]


def test_remove_first():
    """Test removing from front"""
    dq = Deque()
    dq.add_last(1)
    dq.add_last(2)
    dq.add_last(3)

    assert dq.remove_first() == 1
    assert dq.remove_first() == 2
    assert dq.to_list() == [3]


def test_remove_last():
    """Test removing from back"""
    dq = Deque()
    dq.add_last(1)
    dq.add_last(2)
    dq.add_last(3)

    assert dq.remove_last() == 3
    assert dq.remove_last() == 2
    assert dq.to_list() == [1]


def test_peek():
    """Test peek operations"""
    dq = Deque()
    dq.add_last(1)
    dq.add_last(2)
    dq.add_last(3)

    assert dq.peek_first() == 1
    assert dq.peek_last() == 3
    assert dq.size() == 3  # Peek doesn't remove


def test_mixed_operations():
    """Test mixing front and back operations"""
    dq = Deque()
    dq.add_first(2)
    dq.add_first(1)
    dq.add_last(3)
    dq.add_last(4)

    assert dq.to_list() == [1, 2, 3, 4]

    assert dq.remove_first() == 1
    assert dq.remove_last() == 4
    assert dq.to_list() == [2, 3]


def test_empty_operations():
    """Test operations on empty deque"""
    dq = Deque()
    assert dq.is_empty() == True

    try:
        dq.remove_first()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
