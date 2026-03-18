# I AM NOT DONE

"""
Exercise: Ownership and Borrowing

Rust's ownership system ensures memory safety without garbage collection.
Rules:
1. Each value has one owner
2. When owner goes out of scope, value is dropped
3. Can have many immutable borrows OR one mutable borrow

Your task: Implement a simplified ownership system.
"""


class Value:
    """A value with data"""

    def __init__(self, data):
        self.data = data


class OwnershipSystem:
    """Simulated ownership system"""

    def __init__(self):
        self.values = {}              # value_id -> Value
        self.owners = {}              # value_id -> owner_name
        self.immutable_borrows = {}   # value_id -> list of borrower names
        self.mutable_borrow = {}      # value_id -> borrower name (or None)
        self.next_id = 0

    def create_value(self, owner, data):
        """Create a new value with owner"""
        # TODO: Create a new value with owner
        pass

    def transfer_ownership(self, value_id, new_owner):
        """Transfer ownership from current owner to new owner"""
        # TODO: Transfer ownership from current owner to new owner
        # Clear all borrows when ownership transfers
        pass

    def borrow_immutable(self, value_id, borrower):
        """Create immutable borrow"""
        # TODO: Create immutable borrow
        # Fail if there's a mutable borrow
        pass

    def borrow_mutable(self, value_id, borrower):
        """Create mutable borrow"""
        # TODO: Create mutable borrow
        # Fail if there are any other borrows (mutable or immutable)
        pass

    def release_immutable_borrow(self, value_id, borrower):
        """Release an immutable borrow"""
        # TODO: Release an immutable borrow
        pass

    def release_mutable_borrow(self, value_id):
        """Release the mutable borrow"""
        # TODO: Release the mutable borrow
        pass

    def drop_value(self, value_id):
        """Drop value (owner must exist, no borrows can be active)"""
        # TODO: Drop value (owner must exist, no borrows can be active)
        pass

    def get_owner(self, value_id):
        """Get owner of a value"""
        return self.owners.get(value_id)

    def has_mutable_borrow(self, value_id):
        """Check if value has a mutable borrow"""
        return self.mutable_borrow.get(value_id) is not None

    def immutable_borrow_count(self, value_id):
        """Get count of immutable borrows"""
        return len(self.immutable_borrows.get(value_id, []))


import unittest


class TestOwnershipSystem(unittest.TestCase):
    def test_ownership_transfer(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner1", "data")
        self.assertEqual(sys.get_owner(val), "owner1")

        sys.transfer_ownership(val, "owner2")
        self.assertEqual(sys.get_owner(val), "owner2")

    def test_immutable_borrows(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_immutable(val, "borrower1")
        sys.borrow_immutable(val, "borrower2")

        self.assertEqual(sys.immutable_borrow_count(val), 2)

    def test_mutable_borrow_exclusive(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_mutable(val, "borrower1")

        # Can't borrow immutably while mutably borrowed
        result = sys.borrow_immutable(val, "borrower2")
        self.assertIsNone(result)

        # Can't borrow mutably while already mutably borrowed
        result = sys.borrow_mutable(val, "borrower3")
        self.assertIsNone(result)

    def test_no_mutable_with_immutable(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_immutable(val, "borrower1")

        # Can't borrow mutably while immutably borrowed
        result = sys.borrow_mutable(val, "borrower2")
        self.assertIsNone(result)

    def test_borrow_release(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_mutable(val, "borrower")
        sys.release_mutable_borrow(val)

        # Can borrow again after release
        result = sys.borrow_immutable(val, "borrower2")
        self.assertIsNotNone(result)

    def test_drop_with_borrows(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_immutable(val, "borrower")

        # Can't drop while borrowed
        result = sys.drop_value(val)
        self.assertIsNone(result)

        sys.release_immutable_borrow(val, "borrower")

        # Can drop after releasing borrows
        result = sys.drop_value(val)
        self.assertIsNotNone(result)

    def test_multiple_immutable_borrows_allowed(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        for i in range(5):
            sys.borrow_immutable(val, f"borrower{i}")

        self.assertEqual(sys.immutable_borrow_count(val), 5)

    def test_release_specific_immutable_borrow(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        sys.borrow_immutable(val, "borrower1")
        sys.borrow_immutable(val, "borrower2")
        sys.borrow_immutable(val, "borrower3")

        self.assertEqual(sys.immutable_borrow_count(val), 3)

        sys.release_immutable_borrow(val, "borrower2")

        self.assertEqual(sys.immutable_borrow_count(val), 2)

    def test_ownership_transfer_clears_borrows(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner1", "data")

        sys.borrow_immutable(val, "borrower")

        sys.transfer_ownership(val, "owner2")

        # Borrows should be cleared after ownership transfer
        self.assertEqual(sys.immutable_borrow_count(val), 0)

    def test_mutable_borrow_tracking(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        self.assertFalse(sys.has_mutable_borrow(val))

        sys.borrow_mutable(val, "borrower")

        self.assertTrue(sys.has_mutable_borrow(val))

        sys.release_mutable_borrow(val)

        self.assertFalse(sys.has_mutable_borrow(val))

    def test_drop_removes_value(self):
        sys = OwnershipSystem()

        val = sys.create_value("owner", "data")

        self.assertIsNotNone(sys.get_owner(val))

        sys.drop_value(val)

        self.assertIsNone(sys.get_owner(val))

    def test_cant_borrow_nonexistent(self):
        sys = OwnershipSystem()

        result = sys.borrow_immutable(999, "borrower")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
