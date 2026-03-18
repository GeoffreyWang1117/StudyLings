"""
LRU Cache
=========

Least Recently Used cache with O(1) operations.

Implementation:
- Hash map for O(1) access
- Doubly-linked list for O(1) eviction

Operations:
- get(key): O(1)
- put(key, value): O(1)

When cache is full, evict least recently used item.

Applications:
- Web browsers
- Database caches
- OS page replacement
"""


class LRUCache:
    """
    LRU Cache with O(1) get and put.
    """

    def __init__(self, capacity: int):
        """
        Initialize cache with given capacity.

        Args:
            capacity: Maximum number of items
        """
        # TODO: Initialize:
        # - Hash map: key -> node
        # - Doubly-linked list for LRU order
        # - Head and tail sentinels
        pass

    def get(self, key: int) -> int:
        """
        Get value for key.

        Args:
            key: The key

        Returns:
            Value if found, -1 otherwise

        Time Complexity: O(1)
        """
        # TODO: If key exists:
        # 1. Move node to front (most recently used)
        # 2. Return value
        # Otherwise return -1
        pass

    def put(self, key: int, value: int):
        """
        Put key-value pair in cache.

        Args:
            key: The key
            value: The value

        Time Complexity: O(1)
        """
        # TODO:
        # If key exists: update value and move to front
        # Otherwise:
        # 1. Create new node
        # 2. Add to front
        # 3. Add to hash map
        # 4. If over capacity: evict LRU (tail)
        pass


# Tests
def test_lru_cache():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # Evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # Evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
