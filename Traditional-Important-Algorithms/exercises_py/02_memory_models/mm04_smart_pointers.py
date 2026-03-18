# I AM NOT DONE

"""
Exercise: Smart Pointers

Smart pointers provide automatic memory management through RAII.
Common types: Box<T>, Rc<T>, Arc<T>, RefCell<T>

Your task: Implement simplified versions of smart pointers.
"""


class SimpleBox:
    """Simple Box implementation - heap allocated value"""

    def __init__(self, value):
        # TODO: Store value (simulating heap allocation)
        pass

    def get(self):
        """Get the inner value"""
        # TODO: Return the inner value
        pass

    def __del__(self):
        """Destructor - automatic cleanup"""
        # TODO: Cleanup (in Python this is automatic)
        pass


class RcBox:
    """Container for reference-counted value"""

    def __init__(self, value):
        self.value = value
        self.ref_count = 1


class SimpleRc:
    """Simple reference-counted pointer"""

    def __init__(self, value=None, _box=None):
        if _box is not None:
            self._box = _box
        else:
            # TODO: Create new RcBox with ref_count = 1
            pass

    def clone(self):
        """Clone the Rc (increment ref count)"""
        # TODO: Increment ref count and return new Rc
        pass

    def strong_count(self):
        """Get reference count"""
        # TODO: Return current reference count
        pass

    def get(self):
        """Get the inner value"""
        # TODO: Return the inner value
        pass

    def __del__(self):
        """Destructor - decrement ref count"""
        # TODO: Decrement ref count, deallocate if zero
        pass


class SimpleRefCell:
    """Simple RefCell implementation (interior mutability)"""

    def __init__(self, value):
        self.value = value
        self.borrow_state = 0  # >0: immutable borrows, -1: mutable borrow, 0: no borrows

    def borrow(self):
        """Create immutable borrow"""
        # TODO: Create immutable borrow
        # Fail if mutably borrowed
        # Return Ref object
        pass

    def borrow_mut(self):
        """Create mutable borrow"""
        # TODO: Create mutable borrow
        # Fail if any borrows exist
        # Return RefMut object
        pass


class Ref:
    """Immutable borrow guard"""

    def __init__(self, cell):
        self.cell = cell
        # TODO: Increment borrow count
        pass

    def get(self):
        """Get the value"""
        return self.cell.value

    def __del__(self):
        """Release borrow"""
        # TODO: Decrement borrow count
        pass


class RefMut:
    """Mutable borrow guard"""

    def __init__(self, cell):
        self.cell = cell
        # TODO: Set borrow state to -1
        pass

    def get(self):
        """Get the value"""
        return self.cell.value

    def set(self, value):
        """Set the value"""
        self.cell.value = value

    def __del__(self):
        """Release borrow"""
        # TODO: Reset borrow state to 0
        pass


import unittest


class TestSmartPointers(unittest.TestCase):
    def test_simple_box(self):
        b = SimpleBox(42)
        self.assertEqual(b.get(), 42)

    def test_simple_rc(self):
        rc1 = SimpleRc(100)
        self.assertEqual(rc1.strong_count(), 1)

        rc2 = rc1.clone()
        self.assertEqual(rc1.strong_count(), 2)
        self.assertEqual(rc2.strong_count(), 2)

        del rc2
        self.assertEqual(rc1.strong_count(), 1)

    def test_refcell_immutable(self):
        cell = SimpleRefCell(42)

        b1 = cell.borrow()
        b2 = cell.borrow()

        self.assertEqual(b1.get(), 42)
        self.assertEqual(b2.get(), 42)

    def test_refcell_mutable(self):
        cell = SimpleRefCell(42)

        b = cell.borrow_mut()
        b.set(100)

        del b

        b2 = cell.borrow()
        self.assertEqual(b2.get(), 100)

    def test_refcell_borrow_rules(self):
        cell = SimpleRefCell(42)

        b1 = cell.borrow()

        # Can't borrow mutably while immutably borrowed
        b_mut = cell.borrow_mut()
        self.assertIsNone(b_mut)

    def test_refcell_mut_exclusive(self):
        cell = SimpleRefCell(42)

        b1 = cell.borrow_mut()

        # Can't borrow while mutably borrowed
        b2 = cell.borrow()
        self.assertIsNone(b2)

        b3 = cell.borrow_mut()
        self.assertIsNone(b3)

    def test_box_with_different_types(self):
        box_int = SimpleBox(42)
        box_str = SimpleBox("hello")
        box_list = SimpleBox([1, 2, 3])

        self.assertEqual(box_int.get(), 42)
        self.assertEqual(box_str.get(), "hello")
        self.assertEqual(box_list.get(), [1, 2, 3])

    def test_rc_multiple_clones(self):
        rc1 = SimpleRc("data")
        rc2 = rc1.clone()
        rc3 = rc1.clone()
        rc4 = rc2.clone()

        self.assertEqual(rc1.strong_count(), 4)
        self.assertEqual(rc2.strong_count(), 4)
        self.assertEqual(rc3.strong_count(), 4)
        self.assertEqual(rc4.strong_count(), 4)

    def test_rc_value_sharing(self):
        data = [1, 2, 3]
        rc1 = SimpleRc(data)
        rc2 = rc1.clone()

        # Both should reference the same object
        self.assertIs(rc1.get(), rc2.get())

    def test_refcell_multiple_immutable(self):
        cell = SimpleRefCell(100)

        borrows = []
        for _ in range(5):
            borrows.append(cell.borrow())

        for b in borrows:
            self.assertEqual(b.get(), 100)

    def test_refcell_sequential_mutations(self):
        cell = SimpleRefCell(0)

        for i in range(10):
            b = cell.borrow_mut()
            b.set(i)
            del b

        b = cell.borrow()
        self.assertEqual(b.get(), 9)

    def test_rc_cleanup(self):
        rc1 = SimpleRc(42)
        rc2 = rc1.clone()
        rc3 = rc1.clone()

        self.assertEqual(rc1.strong_count(), 3)

        del rc2
        self.assertEqual(rc1.strong_count(), 2)

        del rc3
        self.assertEqual(rc1.strong_count(), 1)


if __name__ == '__main__':
    unittest.main()
