# I AM NOT DONE

"""
Exercise: Reference Counting GC

Reference Counting is a simple garbage collection technique where each object
keeps track of how many references point to it. When the count reaches zero,
the object can be safely deallocated.

Your task: Implement a simple reference-counted smart pointer.

Note: This implementation won't handle cycles - that's a known limitation!
"""


class RcBox:
    """Container for reference-counted value"""

    def __init__(self, value):
        self.value = value
        self.ref_count = 1


class Rc:
    """Reference-counted smart pointer"""

    def __init__(self, value=None, _box=None):
        if _box is not None:
            self._box = _box
        else:
            # TODO: Create a new RcBox with ref_count = 1
            pass

    def clone(self):
        """Create a new reference to the same data"""
        # TODO: Increment the reference count and return a new Rc pointing to the same data
        pass

    def strong_count(self):
        """Return the current reference count"""
        # TODO: Return the current reference count
        pass

    def get(self):
        """Get the inner value"""
        # TODO: Return the inner value
        pass

    def __del__(self):
        """Destructor - called when Rc is garbage collected"""
        # TODO: Decrement ref count. If it reaches 0, the RcBox will be cleaned up
        # Hint: Check if self._box exists before decrementing
        pass


import unittest


class TestReferenceCount(unittest.TestCase):
    def test_reference_counting(self):
        rc1 = Rc(42)
        self.assertEqual(rc1.strong_count(), 1)

        rc2 = rc1.clone()
        self.assertEqual(rc1.strong_count(), 2)
        self.assertEqual(rc2.strong_count(), 2)

        del rc2
        self.assertEqual(rc1.strong_count(), 1)

    def test_get_value(self):
        rc = Rc("hello")
        self.assertEqual(rc.get(), "hello")
        self.assertEqual(len(rc.get()), 5)

    def test_multiple_clones(self):
        rc1 = Rc(100)
        rc2 = rc1.clone()
        rc3 = rc1.clone()
        rc4 = rc2.clone()

        self.assertEqual(rc1.strong_count(), 4)
        self.assertEqual(rc4.get(), 100)

    def test_clone_and_delete(self):
        rc1 = Rc([1, 2, 3])
        rc2 = rc1.clone()
        rc3 = rc1.clone()

        self.assertEqual(rc1.strong_count(), 3)

        del rc2
        self.assertEqual(rc1.strong_count(), 2)

        del rc3
        self.assertEqual(rc1.strong_count(), 1)

    def test_value_types(self):
        # Test with different value types
        rc_int = Rc(42)
        self.assertEqual(rc_int.get(), 42)

        rc_str = Rc("test")
        self.assertEqual(rc_str.get(), "test")

        rc_list = Rc([1, 2, 3])
        self.assertEqual(rc_list.get(), [1, 2, 3])

    def test_multiple_independent_rcs(self):
        rc1 = Rc(1)
        rc2 = Rc(2)

        self.assertEqual(rc1.strong_count(), 1)
        self.assertEqual(rc2.strong_count(), 1)
        self.assertNotEqual(rc1.get(), rc2.get())

    def test_chain_of_clones(self):
        rc1 = Rc("original")
        rc2 = rc1.clone()
        rc3 = rc2.clone()
        rc4 = rc3.clone()

        self.assertEqual(rc1.strong_count(), 4)
        self.assertEqual(rc2.strong_count(), 4)
        self.assertEqual(rc3.strong_count(), 4)
        self.assertEqual(rc4.strong_count(), 4)

    def test_value_sharing(self):
        rc1 = Rc([1, 2, 3])
        rc2 = rc1.clone()

        # Both should reference the same list
        self.assertIs(rc1.get(), rc2.get())

    def test_single_reference_cleanup(self):
        rc = Rc(999)
        self.assertEqual(rc.strong_count(), 1)
        # After this test, rc should be cleaned up automatically

    def test_nested_data_structures(self):
        data = {"key": "value", "list": [1, 2, 3]}
        rc1 = Rc(data)
        rc2 = rc1.clone()

        self.assertEqual(rc1.strong_count(), 2)
        self.assertEqual(rc1.get()["key"], "value")
        self.assertEqual(rc2.get()["list"], [1, 2, 3])

    def test_zero_count_after_all_deleted(self):
        rc1 = Rc(42)
        rc2 = rc1.clone()
        rc3 = rc1.clone()

        self.assertEqual(rc1.strong_count(), 3)

        del rc2
        del rc3

        self.assertEqual(rc1.strong_count(), 1)


if __name__ == '__main__':
    unittest.main()
