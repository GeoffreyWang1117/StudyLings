"""
Skip List
=========

A skip list is a probabilistic data structure that allows O(log n) search,
insertion, and deletion. It's an alternative to balanced trees.

How it works:
- Multiple levels of linked lists
- Bottom level contains all elements
- Each higher level skips over more elements
- Element appears in level i with probability 1/2^i

Expected Time Complexity:
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)

Applications:
- Alternative to balanced trees (simpler code)
- Redis sorted sets
- Concurrent data structures (easier to lock)
"""

import random


class SkipNode:
    """A node in a skip list"""

    def __init__(self, data, level):
        self.data = data
        self.forward = [None] * (level + 1)


class SkipList:
    """
    A skip list implementation.
    """

    def __init__(self, max_level=16):
        """
        Initialize an empty skip list.

        Args:
            max_level: Maximum number of levels
        """
        self.max_level = max_level
        self.level = 0
        # TODO: Create sentinel head node
        # The head should have max_level levels
        pass

    def _random_level(self) -> int:
        """
        Generate a random level for a new node.

        Returns:
            Random level (geometric distribution)
        """
        # TODO: Implement random level generation
        # Keep flipping a coin until you get tails
        # Level should be between 0 and max_level
        level = 0
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def search(self, data) -> bool:
        """
        Search for an element.

        Args:
            data: The data to search for

        Returns:
            True if found, False otherwise

        Time Complexity: O(log n) expected
        """
        # TODO: Implement search
        # Start from top level, move forward while possible
        # Drop down a level when next node is too large
        pass

    def insert(self, data):
        """
        Insert an element.

        Args:
            data: The data to insert

        Time Complexity: O(log n) expected
        """
        # TODO: Implement insert
        # 1. Find the position to insert (track update pointers)
        # 2. Generate random level for new node
        # 3. Create new node
        # 4. Update forward pointers
        pass

    def delete(self, data) -> bool:
        """
        Delete an element.

        Args:
            data: The data to delete

        Returns:
            True if deleted, False if not found

        Time Complexity: O(log n) expected
        """
        # TODO: Implement delete
        # Similar to insert, but remove the node
        pass

    def to_list(self) -> list:
        """
        Convert to a Python list (bottom level only).

        Returns:
            List of all elements in sorted order
        """
        # TODO: Traverse the bottom level
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic insert and search"""
    sl = SkipList()
    sl.insert(3)
    sl.insert(1)
    sl.insert(4)
    sl.insert(2)

    assert sl.search(1) == True
    assert sl.search(2) == True
    assert sl.search(3) == True
    assert sl.search(4) == True
    assert sl.search(5) == False


def test_sorted_order():
    """Test that elements are kept in sorted order"""
    sl = SkipList()
    elements = [5, 2, 8, 1, 9, 3]

    for elem in elements:
        sl.insert(elem)

    result = sl.to_list()
    assert result == sorted(elements)


def test_delete():
    """Test deletion"""
    sl = SkipList()
    sl.insert(1)
    sl.insert(2)
    sl.insert(3)

    assert sl.delete(2) == True
    assert sl.search(2) == False
    assert sl.to_list() == [1, 3]

    assert sl.delete(5) == False  # Not in list


def test_duplicates():
    """Test handling of duplicates"""
    sl = SkipList()
    sl.insert(1)
    sl.insert(2)
    sl.insert(2)
    sl.insert(3)

    # Should contain duplicate
    result = sl.to_list()
    assert result.count(2) == 2


def test_large_dataset():
    """Test with larger dataset"""
    sl = SkipList()
    elements = list(range(100))
    random.shuffle(elements)

    for elem in elements:
        sl.insert(elem)

    # All elements should be found
    for elem in range(100):
        assert sl.search(elem) == True

    # Elements should be in sorted order
    assert sl.to_list() == list(range(100))


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
