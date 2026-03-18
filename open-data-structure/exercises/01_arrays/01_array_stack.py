"""
Array-Based Stack
=================

A stack is a Last-In-First-Out (LIFO) data structure.
Think of it like a stack of plates - you add and remove from the top.

Operations:
- push(x): Add element to top - O(1) amortized
- pop(): Remove and return top element - O(1)
- peek(): View top element without removing - O(1)
- is_empty(): Check if stack is empty - O(1)
- size(): Get number of elements - O(1)

Applications:
- Function call stack
- Undo/redo functionality
- Expression evaluation
- Backtracking algorithms
"""


class ArrayStack:
    """
    Stack implementation using a Python list (dynamic array).
    """

    def __init__(self):
        """Initialize an empty stack"""
        # TODO: Initialize the internal storage
        # Hint: Use a Python list
        pass

    def push(self, item):
        """
        Add an item to the top of the stack.

        Args:
            item: The item to add

        Time Complexity: O(1) amortized
        """
        # TODO: Implement push
        pass

    def pop(self):
        """
        Remove and return the top item from the stack.

        Returns:
            The top item

        Raises:
            IndexError: If the stack is empty

        Time Complexity: O(1)
        """
        # TODO: Implement pop
        # Remember to check if the stack is empty!
        pass

    def peek(self):
        """
        Return the top item without removing it.

        Returns:
            The top item

        Raises:
            IndexError: If the stack is empty

        Time Complexity: O(1)
        """
        # TODO: Implement peek
        pass

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        Returns:
            True if empty, False otherwise

        Time Complexity: O(1)
        """
        # TODO: Implement is_empty
        pass

    def size(self) -> int:
        """
        Get the number of items in the stack.

        Returns:
            Number of items

        Time Complexity: O(1)
        """
        # TODO: Implement size
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_push_and_pop():
    """Test basic push and pop operations"""
    stack = ArrayStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_peek():
    """Test peek operation"""
    stack = ArrayStack()
    stack.push(10)
    stack.push(20)

    assert stack.peek() == 20
    assert stack.peek() == 20  # Peek shouldn't remove
    assert stack.size() == 2


def test_is_empty():
    """Test is_empty operation"""
    stack = ArrayStack()
    assert stack.is_empty() == True

    stack.push(1)
    assert stack.is_empty() == False

    stack.pop()
    assert stack.is_empty() == True


def test_size():
    """Test size operation"""
    stack = ArrayStack()
    assert stack.size() == 0

    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.size() == 3

    stack.pop()
    assert stack.size() == 2


def test_pop_empty():
    """Test popping from empty stack raises error"""
    stack = ArrayStack()
    try:
        stack.pop()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_peek_empty():
    """Test peeking at empty stack raises error"""
    stack = ArrayStack()
    try:
        stack.peek()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
