"""
Hash Table with Linear Probing
================================

Open addressing: Store all items directly in the hash table array.
Linear probing: On collision, try the next slot (with wraparound).

Operations:
- insert(key, value): O(1) average
- search(key): O(1) average
- delete(key): O(1) average (with tombstones)

Key insight: Need to use "tombstones" for deletion to avoid breaking probe chains.

Load factor must be kept < 0.5 for good performance.

Applications:
- More cache-friendly than chaining (better locality)
- Used in some hash table implementations
"""


class LinearProbingHashTable:
    """
    Hash table using linear probing.
    """

    class Entry:
        """An entry in the hash table"""
        def __init__(self, key, value):
            self.key = key
            self.value = value

    TOMBSTONE = object()  # Marker for deleted entries

    def __init__(self, capacity=16):
        """
        Initialize hash table.

        Args:
            capacity: Initial capacity
        """
        # TODO: Initialize the hash table
        # Array of entries (None = empty, TOMBSTONE = deleted)
        pass

    def _hash(self, key) -> int:
        """Hash function"""
        # TODO: Implement hash
        pass

    def insert(self, key, value):
        """
        Insert or update a key-value pair.

        Args:
            key: The key
            value: The value

        Time Complexity: O(1) average
        """
        # TODO: Implement insert with linear probing
        # 1. Compute hash
        # 2. Probe linearly until you find:
        #    - The key (update)
        #    - An empty slot or tombstone (insert)
        # 3. Resize if load factor too high
        pass

    def search(self, key):
        """
        Search for a key.

        Args:
            key: The key to search for

        Returns:
            The value

        Raises:
            KeyError: If not found

        Time Complexity: O(1) average
        """
        # TODO: Implement search with linear probing
        # Probe until you find key or empty slot
        pass

    def delete(self, key):
        """
        Delete a key.

        Args:
            key: The key to delete

        Raises:
            KeyError: If not found

        Time Complexity: O(1) average
        """
        # TODO: Implement delete
        # Replace entry with TOMBSTONE (don't use None!)
        pass

    def contains(self, key) -> bool:
        """Check if key exists"""
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
        Resize the hash table.

        Time Complexity: O(n)
        """
        # TODO: Implement resize
        # Create new table and rehash all non-tombstone entries
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic operations"""
    ht = LinearProbingHashTable()
    ht.insert("apple", 1)
    ht.insert("banana", 2)
    ht.insert("cherry", 3)

    assert ht.search("apple") == 1
    assert ht.search("banana") == 2
    assert ht.search("cherry") == 3


def test_update():
    """Test updating existing key"""
    ht = LinearProbingHashTable()
    ht.insert("key", 10)
    ht.insert("key", 20)

    assert ht.search("key") == 20
    assert ht.size() == 1


def test_delete():
    """Test deletion with tombstones"""
    ht = LinearProbingHashTable()
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)

    ht.delete("b")
    assert ht.contains("a") == True
    assert ht.contains("b") == False
    assert ht.contains("c") == True


def test_delete_and_reinsert():
    """Test that probe chains work after deletion"""
    ht = LinearProbingHashTable(capacity=4)

    # Insert items that may collide
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)

    # Delete middle item
    ht.delete("b")

    # Should still find "c"
    assert ht.contains("c") == True

    # Reinsert at deleted spot
    ht.insert("d", 4)
    assert ht.search("d") == 4


def test_collisions():
    """Test linear probing with collisions"""
    ht = LinearProbingHashTable(capacity=4)

    # Force collisions with small capacity
    for i in range(8):
        ht.insert(f"key{i}", i)

    for i in range(8):
        assert ht.search(f"key{i}") == i


def test_size():
    """Test size tracking"""
    ht = LinearProbingHashTable()
    assert ht.size() == 0

    ht.insert("a", 1)
    ht.insert("b", 2)
    assert ht.size() == 2

    ht.delete("a")
    assert ht.size() == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
