# I AM NOT DONE

"""
Exercise: Copying Garbage Collection

Copying GC divides the heap into two semi-spaces: from-space and to-space.
During collection:
1. Copy all live objects from from-space to to-space
2. Swap the spaces
3. All dead objects are implicitly freed

Your task: Implement a simple copying garbage collector.
"""


class Object:
    """Represents an object with data and references"""

    def __init__(self, data, references=None):
        self.data = data
        self.references = references if references is not None else []


class CopyingGC:
    """Copying Garbage Collector with semi-space model"""

    def __init__(self):
        self.from_space = {}  # obj_id -> Object
        self.to_space = {}
        self.next_id = 0
        self.roots = []
        self.forwarding = {}  # old_id -> new_id mapping during collection

    def allocate(self, data, references=None):
        """Allocate a new object in from-space"""
        obj_id = self.next_id
        self.next_id += 1

        obj = Object(data, references if references else [])
        self.from_space[obj_id] = obj
        return obj_id

    def add_root(self, obj_id):
        """Add an object as a root"""
        self.roots.append(obj_id)

    def _copy_object(self, old_id):
        """Copy an object from from-space to to-space"""
        # TODO: Copy an object from from-space to to-space
        # 1. Check if already copied (in forwarding table)
        # 2. If not, copy the object to to-space with a new ID
        # 3. Add to forwarding table
        # 4. Return the new ID
        pass

    def _update_references(self, obj_id):
        """Update all references in an object to point to new IDs"""
        # TODO: Update all references in the object to point to new IDs
        # Use the forwarding table to map old IDs to new IDs
        pass

    def collect(self):
        """Perform copying collection"""
        # TODO: Implement the copying collection algorithm
        # 1. Clear to_space and forwarding table
        # 2. Copy all root objects and track new root IDs
        # 3. Update all references in copied objects
        # 4. Swap from_space and to_space
        # 5. Clear the old from_space
        pass

    def object_count(self):
        """Return number of live objects"""
        return len(self.from_space)

    def get_object(self, obj_id):
        """Get an object by ID"""
        return self.from_space.get(obj_id)


import unittest


class TestCopyingGC(unittest.TestCase):
    def test_simple_copy(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1, 2, 3])
        gc.add_root(obj1)

        obj2 = gc.allocate([4, 5, 6])

        self.assertEqual(gc.object_count(), 2)

        gc.collect()

        # Only obj1 should remain (it's a root)
        self.assertEqual(gc.object_count(), 1)

    def test_reference_update(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        obj2 = gc.allocate([2], [obj1])

        gc.add_root(obj2)

        gc.collect()

        # Both should survive and references should be updated
        self.assertEqual(gc.object_count(), 2)

    def test_multiple_collections(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        gc.add_root(obj1)

        gc.collect()
        self.assertEqual(gc.object_count(), 1)

        obj2 = gc.allocate([2])
        gc.collect()

        # obj2 not rooted, should be collected
        self.assertEqual(gc.object_count(), 1)

    def test_no_roots(self):
        gc = CopyingGC()

        gc.allocate([1])
        gc.allocate([2])
        gc.allocate([3])

        gc.collect()

        # All should be collected
        self.assertEqual(gc.object_count(), 0)

    def test_transitive_references(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        obj2 = gc.allocate([2], [obj1])
        obj3 = gc.allocate([3], [obj2])

        gc.add_root(obj3)

        gc.collect()

        # All three should survive
        self.assertEqual(gc.object_count(), 3)

    def test_multiple_roots(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        obj2 = gc.allocate([2])

        gc.add_root(obj1)
        gc.add_root(obj2)

        gc.collect()

        self.assertEqual(gc.object_count(), 2)

    def test_shared_references(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        obj2 = gc.allocate([2], [obj1])
        obj3 = gc.allocate([3], [obj1])

        gc.add_root(obj2)
        gc.add_root(obj3)

        gc.collect()

        # All three should survive (obj1 referenced by both obj2 and obj3)
        self.assertEqual(gc.object_count(), 3)

    def test_data_preservation(self):
        gc = CopyingGC()

        obj1 = gc.allocate([10, 20, 30])
        gc.add_root(obj1)

        gc.collect()

        # Data should be preserved after collection
        # Note: obj_id changes but we can verify count
        self.assertEqual(gc.object_count(), 1)

    def test_complex_graph(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        obj2 = gc.allocate([2], [obj1])
        obj3 = gc.allocate([3], [obj1, obj2])
        obj4 = gc.allocate([4])

        gc.add_root(obj3)

        gc.collect()

        # obj1, obj2, obj3 survive; obj4 collected
        self.assertEqual(gc.object_count(), 3)

    def test_empty_roots(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        gc.add_root(obj1)

        gc.roots = []  # Clear roots

        gc.collect()

        self.assertEqual(gc.object_count(), 0)

    def test_consecutive_collections(self):
        gc = CopyingGC()

        obj1 = gc.allocate([1])
        gc.add_root(obj1)

        for _ in range(5):
            gc.collect()
            self.assertEqual(gc.object_count(), 1)


if __name__ == '__main__':
    unittest.main()
