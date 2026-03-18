"""
Priority Queue
==============

A priority queue gives O(1) access to the highest (or lowest) priority item.

Implementation using a heap:
- insert: O(log n)
- extract_max/min: O(log n)
- peek: O(1)

Applications:
- Task scheduling (OS, job queues)
- Event-driven simulation
- Dijkstra's algorithm
- A* pathfinding
- Huffman coding
"""


class PriorityQueue:
    """
    Max-priority queue (higher priority = larger number).

    Can be used for min-priority by negating values.
    """

    def __init__(self):
        """Initialize empty priority queue"""
        # TODO: Use a max heap
        # Hint: Use a list as array-based heap
        pass

    def enqueue(self, item, priority):
        """
        Add an item with given priority.

        Args:
            item: The item to add
            priority: Priority (higher = more important)

        Time Complexity: O(log n)
        """
        # TODO: Insert (item, priority) tuple into heap
        # Use priority for comparisons
        pass

    def dequeue(self):
        """
        Remove and return the highest priority item.

        Returns:
            The item (not the priority)

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(log n)
        """
        # TODO: Extract max from heap, return item only
        pass

    def peek(self):
        """
        View the highest priority item.

        Returns:
            The item

        Raises:
            IndexError: If queue is empty

        Time Complexity: O(1)
        """
        # TODO: Return item at root
        pass

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        # TODO: Implement
        pass

    def size(self) -> int:
        """Get number of items"""
        # TODO: Implement
        pass

    # Helper methods for heap operations
    def _bubble_up(self, index: int):
        """Bubble up (max heap property)"""
        # TODO: Compare with parent, swap if child > parent
        pass

    def _bubble_down(self, index: int):
        """Bubble down (max heap property)"""
        # TODO: Compare with children, swap with larger child
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_basic_operations():
    """Test basic priority queue operations"""
    pq = PriorityQueue()
    pq.enqueue("low", 1)
    pq.enqueue("high", 10)
    pq.enqueue("medium", 5)

    assert pq.dequeue() == "high"   # Priority 10
    assert pq.dequeue() == "medium" # Priority 5
    assert pq.dequeue() == "low"    # Priority 1


def test_peek():
    """Test peek operation"""
    pq = PriorityQueue()
    pq.enqueue("task1", 3)
    pq.enqueue("task2", 7)

    assert pq.peek() == "task2"
    assert pq.size() == 2  # Peek doesn't remove


def test_same_priority():
    """Test items with same priority"""
    pq = PriorityQueue()
    pq.enqueue("a", 5)
    pq.enqueue("b", 5)
    pq.enqueue("c", 10)

    assert pq.dequeue() == "c"  # Highest priority
    # a and b have same priority, either is fine
    result = pq.dequeue()
    assert result in ["a", "b"]


def test_task_scheduling():
    """Test task scheduling scenario"""
    pq = PriorityQueue()

    # Add tasks with priorities
    pq.enqueue("Email", 2)
    pq.enqueue("Bug fix", 10)
    pq.enqueue("Documentation", 1)
    pq.enqueue("Code review", 7)

    # Process in priority order
    schedule = []
    while not pq.is_empty():
        schedule.append(pq.dequeue())

    assert schedule == ["Bug fix", "Code review", "Email", "Documentation"]


def test_empty_queue():
    """Test operations on empty queue"""
    pq = PriorityQueue()
    assert pq.is_empty() == True

    try:
        pq.dequeue()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
