"""
Bloom Filter
============

A Bloom Filter is a space-efficient probabilistic data structure
for testing set membership.

Key properties:
- False positives possible, but NO false negatives
- Extremely space-efficient
- Cannot remove elements (use Counting Bloom Filter for that)

Operations:
- add(item): O(k) where k = number of hash functions
- contains(item): O(k)
- Space: O(m) where m = number of bits

Parameters:
- m: Number of bits in array
- k: Number of hash functions
- n: Expected number of elements

Optimal: k = (m/n) * ln(2)
False positive rate: (1 - e^(-kn/m))^k

Applications:
- Web browsers (checking malicious URLs)
- Databases (avoiding disk reads)
- Distributed systems (sync checks)
- Spell checkers
- Bitcoin wallets
"""


import hashlib
import math


class BloomFilter:
    """
    Bloom Filter for approximate set membership testing.
    """

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01):
        """
        Initialize Bloom Filter.

        Args:
            expected_elements: Expected number of elements (n)
            false_positive_rate: Desired false positive rate (p)

        The filter calculates optimal m and k values.
        """
        # TODO: Calculate optimal parameters
        # m = - (n * ln(p)) / (ln(2)^2)
        # k = (m/n) * ln(2)

        # Initialize bit array of size m
        # Store number of hash functions k
        pass

    def _hash(self, item: str, seed: int) -> int:
        """
        Generate hash value for item with given seed.

        Args:
            item: The item to hash
            seed: Seed for hash function

        Returns:
            Hash value in range [0, m)
        """
        # TODO: Use hashlib to create hash
        # Different seeds give different hash functions
        # Return hash % m
        pass

    def add(self, item: str):
        """
        Add an item to the filter.

        Args:
            item: The item to add

        Time Complexity: O(k)
        """
        # TODO: Set k bits to 1
        # For each hash function (0 to k-1):
        #   hash_val = _hash(item, seed)
        #   Set bit_array[hash_val] = 1
        pass

    def contains(self, item: str) -> bool:
        """
        Check if item might be in the set.

        Returns:
            True if item might be present (or false positive)
            False if item is definitely not present

        Time Complexity: O(k)
        """
        # TODO: Check all k bits
        # For each hash function:
        #   hash_val = _hash(item, seed)
        #   If bit_array[hash_val] == 0:
        #     return False (definitely not present)
        # return True (possibly present)
        pass

    def false_positive_rate(self, n: int) -> float:
        """
        Calculate actual false positive rate.

        Args:
            n: Number of elements inserted

        Returns:
            Estimated false positive probability
        """
        # TODO: Calculate (1 - e^(-kn/m))^k
        pass

    def __len__(self) -> int:
        """
        Count number of set bits (approximation of elements).

        Note: This is an approximation, not exact count.

        Returns:
            Estimated number of elements
        """
        # TODO: Count bits set to 1
        # Or estimate using: n ≈ -(m/k) * ln(1 - X/m)
        # where X = number of bits set to 1
        pass


class CountingBloomFilter(BloomFilter):
    """
    Counting Bloom Filter - supports deletions.

    Uses counters instead of bits.
    """

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01):
        """Initialize with counters instead of bits"""
        # TODO: Use counter array instead of bit array
        pass

    def remove(self, item: str) -> bool:
        """
        Remove an item from the filter.

        Args:
            item: The item to remove

        Returns:
            True if item was likely present, False otherwise
        """
        # TODO: Decrement all k counters
        # Check if all counters > 0 before decrementing
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_bloom_filter_basic():
    """Test basic add and contains"""
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)

    # Add some elements
    bf.add("apple")
    bf.add("banana")
    bf.add("orange")

    # Should find added elements
    assert bf.contains("apple") == True
    assert bf.contains("banana") == True
    assert bf.contains("orange") == True

    # Should not find elements not added (probably)
    assert bf.contains("grape") == False
    assert bf.contains("watermelon") == False


def test_bloom_filter_no_false_negatives():
    """Test that there are no false negatives"""
    bf = BloomFilter(expected_elements=50)

    items = [f"item{i}" for i in range(50)]

    for item in items:
        bf.add(item)

    # All added items should be found
    for item in items:
        assert bf.contains(item) == True


def test_bloom_filter_false_positives():
    """Test false positive rate"""
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.05)

    # Add 100 items
    for i in range(100):
        bf.add(f"item{i}")

    # Check 1000 items not in filter
    false_positives = 0
    test_items = 1000

    for i in range(100, 100 + test_items):
        if bf.contains(f"item{i}"):
            false_positives += 1

    # False positive rate should be roughly around 5%
    actual_rate = false_positives / test_items
    # Allow some variance
    assert actual_rate < 0.15  # Should be well under 15%


def test_counting_bloom_filter():
    """Test counting bloom filter with deletions"""
    cbf = CountingBloomFilter(expected_elements=100)

    cbf.add("apple")
    cbf.add("banana")

    assert cbf.contains("apple") == True

    # Remove apple
    cbf.remove("apple")
    assert cbf.contains("apple") == False
    assert cbf.contains("banana") == True  # Should still exist


def test_bloom_filter_size():
    """Test that bloom filter is space-efficient"""
    # Even with 10000 expected elements and 1% FP rate
    bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)

    # Add a few items
    for i in range(100):
        bf.add(f"item{i}")

    # Bloom filter should still work
    assert bf.contains("item50") == True
    assert bf.contains("notadded") == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
