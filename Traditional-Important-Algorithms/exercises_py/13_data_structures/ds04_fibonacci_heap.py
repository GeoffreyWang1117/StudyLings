# I AM NOT DONE

"""
Fibonacci Heap

Your task: Implement Fibonacci Heap.
"""

from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class FibonacciHeap(Generic[T]):
    def __init__(self):
        self.min_node = None
        self.size_val = 0

    def insert(self, value: T):
        # TODO: Implement
        pass

    def extract_min(self) -> Optional[T]:
        # TODO: Implement
        pass


import unittest

class TestFibonacciHeap(unittest.TestCase):
    def test_insert(self):
        heap = FibonacciHeap()
        heap.insert(5)
        self.assertEqual(heap.extract_min(), 5)

if __name__ == '__main__':
    unittest.main()
