"""
Array-Based Queue
=================

A queue is a First-In-First-Out (FIFO) data structure.
Think of it like a line at a store - first person in line is served first.

This implementation uses a circular buffer to avoid shifting elements.

Operations:
- enqueue(x): Add element to back - O(1) amortized
- dequeue(): Remove and return front element - O(1)
- is_empty(): Check if queue is empty - O(1)
- size(): Get number of elements - O(1)

Applications:
- Task scheduling
- Breadth-first search
- Print queue
- Message queues
"""


class ArrayQueue:
    """
    Queue implementation using a circular buffer.
    """

    def __init__(self, capacity=10):
        """
        Initialize an empty queue with given capacity.

        Args:
            capacity: Initial capacity of the queue
        """
        # TODO: Initialize the queue
        # Hint: You'll need:
        # - An array (list) to store elements
        # - A front index
        # - A back index
        # - A count of elements
        pass

    def enqueue(self, item):
        """
        Add an item to the back of the queue.

        Args:
            item: The item to add

        Time Complexity: O(1) amortized
        """
        # TODO: Implement enqueue
        # Hint: Add at the back index, then increment back (with wraparound)
        # Don't forget to resize if the queue is full!
        pass

    def dequeue(self):
        """
        Remove and return the front item from the queue.

        Returns:
            The front item

        Raises:
            IndexError: If the queue is empty

        Time Complexity: O(1)
        """
        # TODO: Implement dequeue
        # Hint: Get item at front index, then increment front (with wraparound)
        pass

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if empty, False otherwise

        Time Complexity: O(1)
        """
        # TODO: Implement is_empty
        pass

    def size(self) -> int:
        """
        Get the number of items in the queue.

        Returns:
            Number of items

        Time Complexity: O(1)
        """
        # TODO: Implement size
        pass

    def _resize(self):
        """
        Resize the internal array when it gets full.

        Time Complexity: O(n)
        """
        # TODO: Implement resize
        # Hint: Create a new array of double size
        # Copy elements in order from front to back
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_enqueue_and_dequeue():
    """Test basic enqueue and dequeue operations"""
    queue = ArrayQueue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3


def test_is_empty():
    """Test is_empty operation"""
    queue = ArrayQueue()
    assert queue.is_empty() == True

    queue.enqueue(1)
    assert queue.is_empty() == False

    queue.dequeue()
    assert queue.is_empty() == True


def test_size():
    """Test size operation"""
    queue = ArrayQueue()
    assert queue.size() == 0

    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    assert queue.size() == 3

    queue.dequeue()
    assert queue.size() == 2


def test_resize():
    """Test that queue resizes when full"""
    queue = ArrayQueue(capacity=2)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)  # Should trigger resize
    queue.enqueue(4)

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert queue.dequeue() == 4


def test_circular_behavior():
    """Test circular buffer behavior"""
    queue = ArrayQueue(capacity=3)
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1  # Front wraps around

    queue.enqueue(3)
    queue.enqueue(4)
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert queue.dequeue() == 4


def test_dequeue_empty():
    """Test dequeuing from empty queue raises error"""
    queue = ArrayQueue()
    try:
        queue.dequeue()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
