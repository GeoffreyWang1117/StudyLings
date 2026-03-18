# I AM NOT DONE

"""
Exercise: Reservoir Sampling

Reservoir sampling is an algorithm for randomly sampling K items from a stream
of unknown or very large size, where each item has equal probability of being selected.

Algorithm R:
- Keep first K items in reservoir
- For item i (i > K), include it with probability K/i
- If included, replace random item in reservoir

Your task: Implement reservoir sampling for stream processing.
"""

import random
from typing import List, TypeVar


T = TypeVar('T')


class ReservoirSampler:
    """Reservoir sampling for streams"""

    def __init__(self, k: int):
        self.k = k
        self.reservoir = []
        self.count = 0

    def add(self, item: T):
        """Add item to stream and update sample"""
        # TODO: Implement reservoir sampling
        # - If fewer than K items, add to reservoir
        # - Otherwise, include with probability K/count
        # - If included, replace random item
        pass

    def get_sample(self) -> List[T]:
        """Return current reservoir sample"""
        # TODO: Return current sample
        pass

    def sample_size(self) -> int:
        """Return current sample size"""
        # TODO: Return sample size
        pass


import unittest


class TestReservoirSampler(unittest.TestCase):
    def test_small_stream(self):
        sampler = ReservoirSampler(5)
        for i in range(3):
            sampler.add(i)

        sample = sampler.get_sample()
        self.assertEqual(len(sample), 3)
        self.assertEqual(set(sample), {0, 1, 2})

    def test_large_stream(self):
        sampler = ReservoirSampler(10)
        for i in range(100):
            sampler.add(i)

        sample = sampler.get_sample()
        self.assertEqual(len(sample), 10)
        # All samples should be from 0-99
        for item in sample:
            self.assertGreaterEqual(item, 0)
            self.assertLess(item, 100)


if __name__ == '__main__':
    unittest.main()
