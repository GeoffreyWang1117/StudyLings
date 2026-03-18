# I AM NOT DONE

"""
Persistent Data Structure (Immutable List)

Your task: Implement persistent list.
"""

from typing import Generic, Optional, TypeVar, List

T = TypeVar('T')


class PersistentList(Generic[T]):
    def __init__(self):
        # TODO: Initialize
        pass

    def append(self, value: T) -> 'PersistentList[T]':
        # TODO: Return new list with value
        pass

    def get(self, index: int) -> T:
        # TODO: Get value at index
        pass

    def set(self, index: int, value: T) -> 'PersistentList[T]':
        # TODO: Return new list with updated value
        pass


import unittest

class TestPersistentList(unittest.TestCase):
    def test_append(self):
        lst1 = PersistentList()
        lst2 = lst1.append(5)
        self.assertEqual(lst2.get(0), 5)

if __name__ == '__main__':
    unittest.main()
