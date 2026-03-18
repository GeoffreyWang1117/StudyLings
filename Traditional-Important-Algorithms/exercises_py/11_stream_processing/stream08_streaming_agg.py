# I AM NOT DONE

"""
Exercise: Streaming Aggregation

Compute aggregations (sum, count, avg, min, max) over streaming data
with incremental updates.

Key concepts:
- Incremental aggregation
- Combining partial results
- Associative and commutative operations
- Handling retractions/updates

Your task: Implement streaming aggregation operators.
"""

from typing import Optional


class StreamingAggregator:
    """Streaming aggregation"""

    def __init__(self):
        self.count = 0
        self.sum = 0
        self.min_val = None
        self.max_val = None

    def add(self, value: int):
        """Add value to aggregation"""
        # TODO: Update all aggregates incrementally
        pass

    def get_count(self) -> int:
        """Return count"""
        # TODO: Return count
        pass

    def get_sum(self) -> int:
        """Return sum"""
        # TODO: Return sum
        pass

    def get_avg(self) -> Optional[float]:
        """Return average"""
        # TODO: Return average (or None if no values)
        pass

    def get_min(self) -> Optional[int]:
        """Return minimum"""
        # TODO: Return min
        pass

    def get_max(self) -> Optional[int]:
        """Return max"""
        # TODO: Return max
        pass

    def merge(self, other: 'StreamingAggregator'):
        """Merge with another aggregator"""
        # TODO: Combine two aggregators
        pass


import unittest


class TestStreamingAggregator(unittest.TestCase):
    def test_basic_aggregation(self):
        agg = StreamingAggregator()
        agg.add(10)
        agg.add(20)
        agg.add(30)

        self.assertEqual(agg.get_count(), 3)
        self.assertEqual(agg.get_sum(), 60)
        self.assertAlmostEqual(agg.get_avg(), 20.0)
        self.assertEqual(agg.get_min(), 10)
        self.assertEqual(agg.get_max(), 30)

    def test_merge(self):
        agg1 = StreamingAggregator()
        agg1.add(10)
        agg1.add(20)

        agg2 = StreamingAggregator()
        agg2.add(30)
        agg2.add(40)

        agg1.merge(agg2)

        self.assertEqual(agg1.get_count(), 4)
        self.assertEqual(agg1.get_sum(), 100)


if __name__ == '__main__':
    unittest.main()
