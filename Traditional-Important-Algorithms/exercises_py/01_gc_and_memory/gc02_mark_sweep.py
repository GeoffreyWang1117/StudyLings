# I AM NOT DONE

"""
Exercise: Mark-Sweep Garbage Collection

Mark-Sweep is a classic garbage collection algorithm with two phases:
1. Mark: Starting from root objects, traverse and mark all reachable objects
2. Sweep: Free all unmarked objects

Your task: Implement a simple mark-sweep garbage collector.
"""


class Object:
    """Represents an object in the heap"""

    def __init__(self, obj_id, references=None):
        self.id = obj_id
        self.marked = False
        self.references = references if references is not None else []


class MarkSweepGC:
    """Mark-Sweep Garbage Collector"""

    def __init__(self):
        self.objects = {}  # obj_id -> Object
        self.next_id = 0
        self.roots = set()

    def allocate(self, references=None):
        """Allocate a new object with given references"""
        obj_id = self.next_id
        self.next_id += 1

        obj = Object(obj_id, references if references else [])
        self.objects[obj_id] = obj
        return obj_id

    def add_root(self, obj_id):
        """Add an object as a root (keeps it alive)"""
        self.roots.add(obj_id)

    def remove_root(self, obj_id):
        """Remove an object from roots"""
        self.roots.discard(obj_id)

    def _mark(self, obj_id):
        """Mark phase helper - recursively mark object and references"""
        # TODO: Implement the mark phase
        # 1. If object is already marked, return
        # 2. Mark this object
        # 3. Recursively mark all objects this one references
        pass

    def _mark_all_roots(self):
        """Mark all objects reachable from roots"""
        # TODO: Mark all objects reachable from roots
        # Hint: Iterate through roots and call _mark on each
        pass

    def _sweep(self):
        """Sweep phase - remove all unmarked objects"""
        # TODO: Implement the sweep phase
        # Remove all unmarked objects from the objects dict
        # Reset the marked flag on remaining objects
        pass

    def collect(self):
        """Run a full mark-sweep collection cycle"""
        # TODO: Run a full mark-sweep collection cycle
        # 1. Mark all reachable objects
        # 2. Sweep unmarked objects
        pass

    def object_count(self):
        """Return the number of live objects"""
        return len(self.objects)


import unittest


class TestMarkSweep(unittest.TestCase):
    def test_simple_collection(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        self.assertEqual(gc.object_count(), 2)

        gc.collect()

        # obj2 should be collected, obj1 should remain
        self.assertEqual(gc.object_count(), 1)

    def test_transitive_reachability(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])
        obj4 = gc.allocate()

        gc.add_root(obj3)

        self.assertEqual(gc.object_count(), 4)

        gc.collect()

        # obj1, obj2, obj3 are reachable; obj4 is not
        self.assertEqual(gc.object_count(), 3)

    def test_no_roots(self):
        gc = MarkSweepGC()

        gc.allocate()
        gc.allocate()
        gc.allocate()

        self.assertEqual(gc.object_count(), 3)

        gc.collect()

        # All should be collected
        self.assertEqual(gc.object_count(), 0)

    def test_multiple_roots(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)
        gc.add_root(obj2)

        gc.collect()

        # obj1 and obj2 survive, obj3 is collected
        self.assertEqual(gc.object_count(), 2)

    def test_remove_root(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.collect()
        self.assertEqual(gc.object_count(), 1)

        gc.remove_root(obj1)
        gc.collect()

        # After removing root, obj1 should be collected
        self.assertEqual(gc.object_count(), 0)

    def test_cycle(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        # Create cycle: obj1 -> obj2 -> obj1
        gc.objects[obj1].references.append(obj2)

        # No roots - cycle should be collected
        gc.collect()
        self.assertEqual(gc.object_count(), 0)

    def test_cycle_with_root(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        gc.objects[obj1].references.append(obj2)

        gc.add_root(obj1)

        # With root, cycle should survive
        gc.collect()
        self.assertEqual(gc.object_count(), 2)

    def test_complex_graph(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj1, obj2])
        obj4 = gc.allocate([obj2])
        obj5 = gc.allocate()

        gc.add_root(obj3)

        gc.collect()

        # obj1-4 reachable from obj3, obj5 is garbage
        self.assertEqual(gc.object_count(), 4)

    def test_multiple_collections(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.collect()
        self.assertEqual(gc.object_count(), 1)

        obj2 = gc.allocate()
        gc.collect()
        self.assertEqual(gc.object_count(), 1)  # obj2 collected

        gc.add_root(obj2 := gc.allocate())
        gc.collect()
        self.assertEqual(gc.object_count(), 2)  # both survive

    def test_empty_references(self):
        gc = MarkSweepGC()

        obj1 = gc.allocate([])
        obj2 = gc.allocate([])

        gc.add_root(obj1)

        gc.collect()
        self.assertEqual(gc.object_count(), 1)

    def test_long_chain(self):
        gc = MarkSweepGC()

        # Create chain: root -> obj1 -> obj2 -> ... -> obj9
        prev = gc.allocate()
        gc.add_root(prev)

        for _ in range(9):
            prev = gc.allocate([prev])

        gc.collect()

        # All 10 objects should survive
        self.assertEqual(gc.object_count(), 10)


if __name__ == '__main__':
    unittest.main()
