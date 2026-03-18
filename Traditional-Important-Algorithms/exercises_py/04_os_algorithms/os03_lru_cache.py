# I AM NOT DONE

"""
os03_lru_cache.py

LRU (Least Recently Used) is a cache eviction policy that discards the least
recently used items first. This is commonly used in operating systems for page
replacement and in various caching systems.

Your task: Implement an LRU cache using a dictionary and a doubly-linked list.
"""

from typing import Optional, Generic, TypeVar, Dict
import unittest


K = TypeVar('K')
V = TypeVar('V')


class Node(Generic[K, V]):
    """Node in doubly-linked list."""
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.prev: Optional['Node[K, V]'] = None
        self.next: Optional['Node[K, V]'] = None


class LRUCache(Generic[K, V]):
    """LRU Cache implementation using hash map and doubly-linked list."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[K, Node[K, V]] = {}
        # Dummy head and tail nodes
        self.head: Node[K, V] = Node(None, None)  # type: ignore
        self.tail: Node[K, V] = Node(None, None)  # type: ignore
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: Node[K, V]) -> None:
        """
        TODO: Remove a node from the doubly-linked list.

        Update the prev and next pointers of neighboring nodes.

        Args:
            node: Node to remove
        """
        pass  # TODO: Implement this

    def _add_to_front(self, node: Node[K, V]) -> None:
        """
        TODO: Add a node to the front of the list (after head).

        Args:
            node: Node to add
        """
        pass  # TODO: Implement this

    def _move_to_front(self, node: Node[K, V]) -> None:
        """
        TODO: Move a node to the front of the list (most recently used).

        Steps:
        1. Remove the node from its current position
        2. Add it to the front

        Args:
            node: Node to move
        """
        pass  # TODO: Implement this

    def _evict_lru(self) -> None:
        """
        TODO: Evict the least recently used item (at the tail).

        Steps:
        1. Get the node before tail
        2. Remove it from the list
        3. Remove it from the cache dictionary
        """
        pass  # TODO: Implement this

    def get(self, key: K) -> Optional[V]:
        """
        TODO: Get a value from the cache.

        Steps:
        1. Look up the key in the cache
        2. Move the node to the front (mark as recently used)
        3. Return the value

        Args:
            key: Key to look up

        Returns:
            Value if found, None otherwise
        """
        pass  # TODO: Implement this

    def put(self, key: K, value: V) -> None:
        """
        TODO: Insert or update a key-value pair.

        Steps:
        1. If key exists, update the value and move to front
        2. If key doesn't exist:
           a. If at capacity, evict the LRU item
           b. Create a new node
           c. Add to front
           d. Add to cache dictionary

        Args:
            key: Key to insert/update
            value: Value to store
        """
        pass  # TODO: Implement this

    def __len__(self) -> int:
        """Get the number of items in cache."""
        return len(self.cache)

    def is_empty(self) -> bool:
        """Check if cache is empty."""
        return len(self.cache) == 0

    def get_capacity(self) -> int:
        """Get the cache capacity."""
        return self.capacity


class TestLRUCache(unittest.TestCase):
    """Test cases for LRU Cache."""

    def test_basic_operations(self):
        """Test basic put and get operations."""
        cache = LRUCache[int, str](2)

        cache.put(1, "one")
        cache.put(2, "two")

        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), "two")

    def test_eviction(self):
        """Test LRU eviction."""
        cache = LRUCache[int, str](2)

        cache.put(1, "one")
        cache.put(2, "two")
        cache.put(3, "three")  # Should evict key 1

        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), "three")

    def test_update_existing(self):
        """Test updating existing key."""
        cache = LRUCache[int, str](2)

        cache.put(1, "one")
        cache.put(2, "two")
        cache.put(1, "ONE")  # Update existing key

        self.assertEqual(cache.get(1), "ONE")
        self.assertEqual(len(cache), 2)

    def test_lru_ordering(self):
        """Test LRU ordering with get operations."""
        cache = LRUCache[int, str](2)

        cache.put(1, "one")
        cache.put(2, "two")
        cache.get(1)  # Access key 1, making it more recent
        cache.put(3, "three")  # Should evict key 2 (least recently used)

        self.assertEqual(cache.get(1), "one")
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(3), "three")

    def test_capacity_one(self):
        """Test cache with capacity 1."""
        cache = LRUCache[int, str](1)

        cache.put(1, "one")
        self.assertEqual(cache.get(1), "one")

        cache.put(2, "two")  # Should evict key 1
        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "two")

    def test_multiple_evictions(self):
        """Test multiple evictions."""
        cache = LRUCache[int, str](3)

        cache.put(1, "one")
        cache.put(2, "two")
        cache.put(3, "three")
        cache.put(4, "four")  # Evict 1
        cache.put(5, "five")  # Evict 2

        self.assertIsNone(cache.get(1))
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.get(4), "four")
        self.assertEqual(cache.get(5), "five")

    def test_get_updates_recency(self):
        """Test that get updates recency."""
        cache = LRUCache[int, str](3)

        cache.put(1, "one")
        cache.put(2, "two")
        cache.put(3, "three")

        cache.get(1)  # Make 1 most recent
        cache.get(2)  # Make 2 most recent

        cache.put(4, "four")  # Should evict 3

        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), "two")
        self.assertIsNone(cache.get(3))
        self.assertEqual(cache.get(4), "four")

    def test_empty_cache(self):
        """Test empty cache."""
        cache = LRUCache[int, str](5)

        self.assertTrue(cache.is_empty())
        self.assertEqual(len(cache), 0)
        self.assertIsNone(cache.get(1))

    def test_string_keys(self):
        """Test with string keys."""
        cache = LRUCache[str, int](3)

        cache.put("key1", 1)
        cache.put("key2", 2)
        cache.put("key3", 3)

        self.assertEqual(cache.get("key1"), 1)
        self.assertEqual(cache.get("key2"), 2)

        cache.put("key4", 4)

        self.assertIsNone(cache.get("key3"))

    def test_full_cache_get_miss(self):
        """Test get miss on full cache."""
        cache = LRUCache[int, str](2)

        cache.put(1, "one")
        cache.put(2, "two")

        # Getting non-existent key shouldn't affect cache
        result = cache.get(3)
        self.assertIsNone(result)
        self.assertEqual(len(cache), 2)

    def test_overwrite_value(self):
        """Test overwriting value doesn't change size."""
        cache = LRUCache[int, str](3)

        cache.put(1, "one")
        cache.put(2, "two")

        self.assertEqual(len(cache), 2)

        cache.put(1, "ONE")

        self.assertEqual(len(cache), 2)
        self.assertEqual(cache.get(1), "ONE")


if __name__ == '__main__':
    unittest.main()
