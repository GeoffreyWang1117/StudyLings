# I AM NOT DONE

"""
Binary Heap (Min and Max)

Your task: Implement heaps.
"""

from typing import Generic, Optional, TypeVar, List

T = TypeVar('T')


class MinHeap(Generic[T]):
    def __init__(self):
        self.data: List[T] = []

    def push(self, value: T):
        # TODO: Implement
        pass

    def pop(self) -> Optional[T]:
        # TODO: Implement
        pass


class MaxHeap(Generic[T]):
    def __init__(self):
        self.data: List[T] = []

    def push(self, value: T):
        # TODO: Implement
        pass

    def pop(self) -> Optional[T]:
        # TODO: Implement
        pass


import unittest

class TestHeap(unittest.TestCase):
    def test_minheap(self):
        heap = MinHeap()
        heap.push(5)
        heap.push(3)
        self.assertEqual(heap.pop(), 3)

if __name__ == '__main__':
    unittest.main()
