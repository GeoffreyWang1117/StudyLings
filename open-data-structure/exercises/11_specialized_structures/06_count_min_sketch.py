"""
Count-Min Sketch
================

A probabilistic data structure for estimating frequencies in data streams.
Space-efficient alternative to hash table for frequency counting.

Structure:
- 2D array of counters (d x w)
- d hash functions
- All counters initialized to 0

Operations:
- update(item): Increment counters - O(d)
- estimate(item): Estimate frequency - O(d)
- Space: O(d * w)

Properties:
- Overestimates, never underestimates
- Error bound: ε * N with probability 1-δ
  where N = total count, d = ln(1/δ), w = e/ε

Applications:
- Network traffic monitoring
- Database query optimization
- Natural language processing
- Real-time analytics
- DDoS detection
- Heavy hitter detection
"""


import hashlib
import math


class CountMinSketch:
    """
    Count-Min Sketch for frequency estimation.
    """

    def __init__(self, width: int = 1000, depth: int = 5):
        """
        Initialize Count-Min Sketch.

        Args:
            width: Width of array (w)
            depth: Number of hash functions (d)

        For error ε and confidence δ:
            width = ceil(e / ε)
            depth = ceil(ln(1 / δ))
        """
        # TODO: Initialize 2D array of zeros
        self.width = width
        self.depth = depth
        # self.table[i][j] = count for hash function i, bucket j
        pass

    def _hash(self, item: str, seed: int) -> int:
        """
        Hash function with seed.

        Args:
            item: Item to hash
            seed: Seed for hash function

        Returns:
            Hash value in range [0, width)
        """
        # TODO: Hash with seed
        data = f"{item}{seed}".encode('utf-8')
        hash_val = int(hashlib.md5(data).hexdigest(), 16)
        return hash_val % self.width

    def update(self, item: str, count: int = 1):
        """
        Update count for item.

        Args:
            item: The item
            count: Amount to add (default 1)

        Time Complexity: O(d)
        """
        # TODO: Increment d counters
        # For each hash function i:
        #   bucket = _hash(item, i)
        #   table[i][bucket] += count
        pass

    def estimate(self, item: str) -> int:
        """
        Estimate frequency of item.

        Args:
            item: The item

        Returns:
            Estimated count (may overestimate)

        Time Complexity: O(d)
        """
        # TODO: Query d counters and return minimum
        # min_count = infinity
        # For each hash function i:
        #   bucket = _hash(item, i)
        #   min_count = min(min_count, table[i][bucket])
        # return min_count
        pass

    def merge(self, other: 'CountMinSketch'):
        """
        Merge another sketch into this one.

        Args:
            other: Another Count-Min Sketch (same dimensions)

        Time Complexity: O(d * w)
        """
        # TODO: Add corresponding cells
        if self.width != other.width or self.depth != other.depth:
            raise ValueError("Sketches must have same dimensions")

        # for i in range(self.depth):
        #     for j in range(self.width):
        #         self.table[i][j] += other.table[i][j]
        pass

    def total_count(self) -> int:
        """
        Get total count of all items.

        Returns:
            Total count (approximate)

        Time Complexity: O(1) if tracking, O(w) otherwise
        """
        # TODO: Return sum of first row (or track separately)
        pass

    @staticmethod
    def optimal_parameters(epsilon: float, delta: float) -> tuple:
        """
        Calculate optimal width and depth for given error bounds.

        Args:
            epsilon: Error bound (ε)
            delta: Confidence (δ)

        Returns:
            (width, depth) tuple
        """
        # TODO: Calculate parameters
        # width = ceil(e / epsilon)
        # depth = ceil(ln(1 / delta))
        width = math.ceil(math.e / epsilon)
        depth = math.ceil(math.log(1 / delta))
        return width, depth


class HeavyHitterDetector:
    """
    Use Count-Min Sketch to find heavy hitters.

    Heavy hitters are items with frequency > threshold * total_count
    """

    def __init__(self, threshold: float = 0.01, width: int = 1000, depth: int = 5):
        """
        Initialize detector.

        Args:
            threshold: Threshold for heavy hitter (0-1)
            width: Sketch width
            depth: Sketch depth
        """
        self.sketch = CountMinSketch(width, depth)
        self.threshold = threshold
        self.total = 0

    def add(self, item: str):
        """Add item to stream"""
        self.sketch.update(item)
        self.total += 1

    def is_heavy_hitter(self, item: str) -> bool:
        """Check if item is a heavy hitter"""
        freq = self.sketch.estimate(item)
        return freq >= self.threshold * self.total


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_basic_counting():
    """Test basic frequency counting"""
    cms = CountMinSketch(width=100, depth=5)

    # Add items
    cms.update("apple", 5)
    cms.update("banana", 3)
    cms.update("apple", 2)

    # Estimates should be >= actual counts
    assert cms.estimate("apple") >= 7
    assert cms.estimate("banana") >= 3
    assert cms.estimate("orange") >= 0  # Never added


def test_stream_processing():
    """Test with data stream"""
    cms = CountMinSketch(width=1000, depth=7)

    # Simulate stream
    items = ["a"] * 100 + ["b"] * 50 + ["c"] * 25 + ["d"] * 10

    for item in items:
        cms.update(item)

    # Verify estimates (may be slightly higher due to collisions)
    assert 100 <= cms.estimate("a") <= 110
    assert 50 <= cms.estimate("b") <= 60
    assert 25 <= cms.estimate("c") <= 35


def test_no_underestimation():
    """Test that sketch never underestimates"""
    cms = CountMinSketch(width=500, depth=5)

    actual_counts = {}
    items = ["apple", "banana", "cherry", "date", "elderberry"]

    # Random updates
    import random
    random.seed(42)

    for _ in range(1000):
        item = random.choice(items)
        actual_counts[item] = actual_counts.get(item, 0) + 1
        cms.update(item)

    # All estimates should be >= actual
    for item, count in actual_counts.items():
        assert cms.estimate(item) >= count


def test_merge():
    """Test merging sketches"""
    cms1 = CountMinSketch(width=100, depth=5)
    cms2 = CountMinSketch(width=100, depth=5)

    cms1.update("apple", 10)
    cms2.update("apple", 5)
    cms2.update("banana", 3)

    cms1.merge(cms2)

    assert cms1.estimate("apple") >= 15
    assert cms1.estimate("banana") >= 3


def test_optimal_parameters():
    """Test parameter calculation"""
    # 1% error, 99% confidence
    width, depth = CountMinSketch.optimal_parameters(0.01, 0.01)

    assert width > 0
    assert depth > 0
    # Roughly depth ≈ ln(1/0.01) ≈ 4.6
    assert 3 <= depth <= 7


def test_heavy_hitter():
    """Test heavy hitter detection"""
    detector = HeavyHitterDetector(threshold=0.1)  # 10% threshold

    # Add 100 items: 80 'frequent', 20 others
    for _ in range(80):
        detector.add("frequent")
    for i in range(20):
        detector.add(f"rare{i}")

    assert detector.is_heavy_hitter("frequent") == True
    assert detector.is_heavy_hitter("rare0") == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
