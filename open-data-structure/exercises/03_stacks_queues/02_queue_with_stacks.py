"""
Implement Queue Using Two Stacks
==================================

An interesting problem: implement a queue using only stack operations.

Insight:
- Use two stacks: inbox and outbox
- Push to inbox
- Pop from outbox (transfer from inbox if outbox is empty)

This gives amortized O(1) operations!

Operations:
- enqueue(x): Add to back - O(1)
- dequeue(): Remove from front - O(1) amortized
- peek(): View front - O(1) amortized

Applications:
- Understanding amortized analysis
- Interview question
"""


class QueueWithStacks:
    """
    Queue implementation using two stacks.
    """

    def __init__(self):
        """Initialize the queue"""
        # TODO: Initialize two stacks (use Python lists)
        # One for enqueue (inbox), one for dequeue (outbox)
        pass

    def enqueue(self, item):
        """
        Add an item to the back of the queue.

        Args:
            item: The item to add

        Time Complexity: O(1)
        """
        # TODO: Push to inbox
        pass

    def dequeue(self):
        """
        Remove and return the front item.

        Returns:
            The front item

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(1) amortized
        """
        # TODO: Pop from outbox
        # If outbox is empty, transfer all from inbox
        pass

    def peek(self):
        """
        Return the front item without removing it.

        Returns:
            The front item

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(1) amortized
        """
        # TODO: Peek at outbox
        # If outbox is empty, transfer from inbox
        pass

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        Returns:
            True if empty, False otherwise

        Time Complexity: O(1)
        """
        # TODO: Check if both stacks are empty
        pass

    def size(self) -> int:
        """
        Get the number of items.

        Returns:
            Number of items

        Time Complexity: O(1)
        """
        # TODO: Sum sizes of both stacks
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_basic_operations():
    """Test basic enqueue and dequeue"""
    q = QueueWithStacks()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3


def test_interleaved_operations():
    """Test mixing enqueue and dequeue"""
    q = QueueWithStacks()
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1

    q.enqueue(3)
    assert q.dequeue() == 2
    assert q.dequeue() == 3


def test_peek():
    """Test peek operation"""
    q = QueueWithStacks()
    q.enqueue(10)
    q.enqueue(20)

    assert q.peek() == 10
    assert q.peek() == 10  # Shouldn't remove
    assert q.dequeue() == 10
    assert q.peek() == 20


def test_is_empty():
    """Test is_empty"""
    q = QueueWithStacks()
    assert q.is_empty() == True

    q.enqueue(1)
    assert q.is_empty() == False

    q.dequeue()
    assert q.is_empty() == True


def test_size():
    """Test size operation"""
    q = QueueWithStacks()
    assert q.size() == 0

    q.enqueue(1)
    q.enqueue(2)
    assert q.size() == 2

    q.dequeue()
    assert q.size() == 1


def test_dequeue_empty():
    """Test dequeuing from empty queue"""
    q = QueueWithStacks()
    try:
        q.dequeue()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
