"""
Hash Table with Chaining
=========================

A hash table provides O(1) average-case insert, search, and delete.

Chaining: Handle collisions by storing a linked list at each bucket.

Operations:
- insert(key, value): O(1) average, O(n) worst
- search(key): O(1) average, O(n) worst
- delete(key): O(1) average, O(n) worst

Load factor α = n/m (items / buckets)
- Keep α < 1 for good performance
- Resize when α gets too large

Applications:
- Dictionaries/maps
- Caches
- Symbol tables in compilers
- Database indexing
"""


class HashTable:
    """
    Hash table implementation using chaining.
    """

    class Node:
        """A node in the chain"""
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, capacity=16):
        """
        Initialize hash table.

        Args:
            capacity: Initial number of buckets
        """
        # TODO: Initialize the hash table
        # - Array of buckets (each bucket is a linked list head)
        # - Track size (number of items)
        pass

    def _hash(self, key) -> int:
        """
        Hash function.

        Args:
            key: The key to hash

        Returns:
            Bucket index
        """
        # TODO: Implement hash function
        # Use Python's built-in hash() and mod by capacity
        pass

    def insert(self, key, value):
        """
        Insert or update a key-value pair.

        Args:
            key: The key
            value: The value

        Time Complexity: O(1) average
        """
        # TODO: Implement insert
        # 1. Compute hash
        # 2. Check if key exists in chain (update if yes)
        # 3. Otherwise add new node to chain
        # 4. Resize if load factor too high
        pass

    def search(self, key):
        """
        Search for a key.

        Args:
            key: The key to search for

        Returns:
            The value associated with the key

        Raises:
            KeyError: If key not found

        Time Complexity: O(1) average
        """
        # TODO: Implement search
        # Compute hash and traverse chain
        pass

    def delete(self, key):
        """
        Delete a key-value pair.

        Args:
            key: The key to delete

        Raises:
            KeyError: If key not found

        Time Complexity: O(1) average
        """
        # TODO: Implement delete
        # Find and remove node from chain
        pass

    def contains(self, key) -> bool:
        """
        Check if key exists.

        Args:
            key: The key to check

        Returns:
            True if key exists, False otherwise
        """
        # TODO: Implement contains
        try:
            self.search(key)
            return True
        except KeyError:
            return False

    def size(self) -> int:
        """Get number of items"""
        # TODO: Return size
        pass

    def _resize(self):
        """
        Resize the hash table when load factor is too high.

        Time Complexity: O(n)
        """
        # TODO: Implement resize
        # 1. Create new larger table
        # 2. Rehash all items into new table
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic insert and search"""
    ht = HashTable()
    ht.insert("apple", 1)
    ht.insert("banana", 2)
    ht.insert("cherry", 3)

    assert ht.search("apple") == 1
    assert ht.search("banana") == 2
    assert ht.search("cherry") == 3


def test_update():
    """Test updating existing key"""
    ht = HashTable()
    ht.insert("key", 10)
    assert ht.search("key") == 10

    ht.insert("key", 20)
    assert ht.search("key") == 20
    assert ht.size() == 1  # Size shouldn't increase


def test_delete():
    """Test deletion"""
    ht = HashTable()
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)

    ht.delete("b")
    assert ht.contains("a") == True
    assert ht.contains("b") == False
    assert ht.contains("c") == True


def test_delete_not_found():
    """Test deleting non-existent key"""
    ht = HashTable()
    try:
        ht.delete("notfound")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_search_not_found():
    """Test searching for non-existent key"""
    ht = HashTable()
    try:
        ht.search("notfound")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_collisions():
    """Test handling collisions"""
    # Use small capacity to force collisions
    ht = HashTable(capacity=2)
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)
    ht.insert("d", 4)

    assert ht.search("a") == 1
    assert ht.search("b") == 2
    assert ht.search("c") == 3
    assert ht.search("d") == 4


def test_size():
    """Test size tracking"""
    ht = HashTable()
    assert ht.size() == 0

    ht.insert("a", 1)
    assert ht.size() == 1

    ht.insert("b", 2)
    assert ht.size() == 2

    ht.delete("a")
    assert ht.size() == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
