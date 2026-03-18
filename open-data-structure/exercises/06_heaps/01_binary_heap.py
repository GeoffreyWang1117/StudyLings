"""
Binary Heap
===========

A binary heap is a complete binary tree that satisfies the heap property:
- Max heap: parent >= children
- Min heap: parent <= children

Array representation (0-indexed):
- Parent of i: (i-1) // 2
- Left child of i: 2*i + 1
- Right child of i: 2*i + 2

Operations:
- insert(x): O(log n)
- extract_min/max(): O(log n)
- peek(): O(1)
- heapify: O(n)

Applications:
- Priority queues
- Heap sort
- Graph algorithms (Dijkstra, Prim)
"""


class MinHeap:
    """
    Min heap implementation using an array.
    """

    def __init__(self):
        """Initialize empty heap"""
        # TODO: Initialize array to store heap
        pass

    def insert(self, item):
        """
        Insert an item into the heap.

        Args:
            item: The item to insert

        Time Complexity: O(log n)
        """
        # TODO: Implement insert
        # 1. Add item to end of array
        # 2. Bubble up to maintain heap property
        pass

    def extract_min(self):
        """
        Remove and return the minimum item.

        Returns:
            The minimum item

        Raises:
            IndexError: If heap is empty

        Time Complexity: O(log n)
        """
        # TODO: Implement extract_min
        # 1. Save root value
        # 2. Move last item to root
        # 3. Bubble down to maintain heap property
        pass

    def peek(self):
        """
        Return the minimum without removing.

        Returns:
            The minimum item

        Raises:
            IndexError: If heap is empty

        Time Complexity: O(1)
        """
        # TODO: Return first element
        pass

    def size(self) -> int:
        """Get number of items"""
        # TODO: Return size
        pass

    def is_empty(self) -> bool:
        """Check if heap is empty"""
        # TODO: Check if size is 0
        pass

    def _bubble_up(self, index: int):
        """
        Bubble up the item at index.

        Args:
            index: Index of item to bubble up
        """
        # TODO: Compare with parent and swap if needed
        # Repeat until heap property is satisfied
        pass

    def _bubble_down(self, index: int):
        """
        Bubble down the item at index.

        Args:
            index: Index of item to bubble down
        """
        # TODO: Compare with children and swap with smaller
        # Repeat until heap property is satisfied
        pass

    def _parent(self, index: int) -> int:
        """Get parent index"""
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index"""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index"""
        return 2 * index + 2


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_extract():
    """Test basic insert and extract"""
    heap = MinHeap()
    heap.insert(5)
    heap.insert(3)
    heap.insert(7)
    heap.insert(1)

    assert heap.extract_min() == 1
    assert heap.extract_min() == 3
    assert heap.extract_min() == 5
    assert heap.extract_min() == 7


def test_peek():
    """Test peek operation"""
    heap = MinHeap()
    heap.insert(10)
    heap.insert(5)
    heap.insert(15)

    assert heap.peek() == 5
    assert heap.size() == 3  # Peek doesn't remove


def test_heap_property():
    """Test that heap maintains heap property"""
    heap = MinHeap()
    items = [9, 5, 2, 7, 3, 8, 1, 4, 6]

    for item in items:
        heap.insert(item)

    # Extract all items - should be in sorted order
    result = []
    while not heap.is_empty():
        result.append(heap.extract_min())

    assert result == sorted(items)


def test_extract_empty():
    """Test extracting from empty heap"""
    heap = MinHeap()
    try:
        heap.extract_min()
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_size():
    """Test size tracking"""
    heap = MinHeap()
    assert heap.size() == 0

    heap.insert(1)
    heap.insert(2)
    assert heap.size() == 2

    heap.extract_min()
    assert heap.size() == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
