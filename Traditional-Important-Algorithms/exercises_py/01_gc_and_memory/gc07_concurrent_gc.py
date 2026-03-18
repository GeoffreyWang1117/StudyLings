# I AM NOT DONE

"""
Exercise: Concurrent Garbage Collection

Concurrent GC runs the collector concurrently with the mutator (application).
This requires synchronization and write barriers to maintain correctness.

Your task: Implement a simplified concurrent GC with basic write barrier.
"""

import threading


class Object:
    """Object with references and mark bit"""

    def __init__(self, references=None):
        self.references = references if references is not None else []
        self.marked = False


class ConcurrentGC:
    """Concurrent garbage collector with write barrier"""

    def __init__(self):
        self.objects = {}  # obj_id -> Object
        self.next_id = 0
        self.roots = set()
        self.write_barrier_log = []  # Log of (from_id, to_id) writes
        self.lock = threading.Lock()

    def allocate(self, references=None):
        """Allocate a new object"""
        with self.lock:
            obj_id = self.next_id
            self.next_id += 1

            obj = Object(references if references else [])
            self.objects[obj_id] = obj
            return obj_id

    def add_root(self, obj_id):
        """Add an object as a root"""
        with self.lock:
            self.roots.add(obj_id)

    def write_barrier(self, from_id, to_id):
        """Record a pointer write"""
        # TODO: Implement write barrier
        # Log pointer writes during concurrent marking
        # This ensures we don't miss references created during GC
        pass

    def update_reference(self, from_id, index, to_id):
        """Update a reference with write barrier"""
        # TODO: Update a reference with write barrier
        # 1. Call write barrier
        # 2. Update the actual reference
        pass

    def _mark(self, obj_id, marked):
        """Mark an object and its references"""
        if obj_id in marked:
            return

        marked.add(obj_id)

        with self.lock:
            if obj_id in self.objects:
                obj = self.objects[obj_id]
                refs = obj.references.copy()

        for ref_id in refs:
            self._mark(ref_id, marked)

    def concurrent_collect(self):
        """Perform concurrent collection"""
        # TODO: Implement concurrent collection
        # 1. Mark from roots
        # 2. Process write barrier log
        # 3. Sweep unmarked objects
        pass

    def object_count(self):
        """Return number of live objects"""
        with self.lock:
            return len(self.objects)


import unittest


class TestConcurrentGC(unittest.TestCase):
    def test_concurrent_allocation(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])

        gc.add_root(obj2)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 2)

    def test_write_barrier(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        gc.update_reference(obj1, 0, obj2)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 2)

    def test_concurrent_threads(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        def collector_thread():
            gc.concurrent_collect()

        thread = threading.Thread(target=collector_thread)
        thread.start()

        # Allocate while GC runs
        obj2 = gc.allocate()

        thread.join()

        # At least obj1 should survive
        self.assertGreaterEqual(gc.object_count(), 1)

    def test_multiple_writes(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)

        gc.update_reference(obj1, 0, obj2)
        gc.update_reference(obj1, 1, obj3)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 3)

    def test_no_roots(self):
        gc = ConcurrentGC()

        gc.allocate()
        gc.allocate()

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 0)

    def test_transitive_marking(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])

        gc.add_root(obj3)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 3)

    def test_write_during_collection(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        # Simulate write during collection
        gc.write_barrier(obj1, obj2)

        gc.concurrent_collect()

        # Both should survive due to write barrier
        self.assertEqual(gc.object_count(), 2)

    def test_multiple_roots(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)
        gc.add_root(obj2)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 2)

    def test_complex_graph(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj1, obj2])
        obj4 = gc.allocate()

        gc.add_root(obj3)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 3)

    def test_sequential_collections(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.concurrent_collect()
        self.assertEqual(gc.object_count(), 1)

        gc.concurrent_collect()
        self.assertEqual(gc.object_count(), 1)

    def test_barrier_log_processing(self):
        gc = ConcurrentGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        # Multiple writes
        gc.write_barrier(obj1, obj2)
        gc.write_barrier(obj1, obj2)

        gc.concurrent_collect()

        self.assertEqual(gc.object_count(), 2)


if __name__ == '__main__':
    unittest.main()
