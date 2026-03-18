# I AM NOT DONE

"""
Exercise: Tricolor Marking Algorithm

Tricolor marking is an algorithm for incremental/concurrent GC.
Objects are classified into three colors:
- White: Not yet visited (potentially garbage)
- Gray: Visited but not scanned (work queue)
- Black: Visited and scanned (definitely live)

Your task: Implement tricolor marking for incremental collection.
"""

from enum import Enum
from collections import deque


class Color(Enum):
    """Object color in tricolor marking"""
    WHITE = "white"
    GRAY = "gray"
    BLACK = "black"


class Object:
    """Object with color and references"""

    def __init__(self, obj_id, references=None):
        self.id = obj_id
        self.color = Color.WHITE
        self.references = references if references is not None else []


class TricolorGC:
    """Garbage collector using tricolor marking"""

    def __init__(self):
        self.objects = {}  # obj_id -> Object
        self.next_id = 0
        self.roots = set()
        self.gray_queue = deque()

    def allocate(self, references=None):
        """Allocate a new object"""
        obj_id = self.next_id
        self.next_id += 1

        obj = Object(obj_id, references if references else [])
        self.objects[obj_id] = obj
        return obj_id

    def add_root(self, obj_id):
        """Add an object as a root"""
        self.roots.add(obj_id)

    def init_collection(self):
        """Initialize a collection cycle"""
        # TODO: Initialize a collection cycle
        # 1. Set all objects to white
        # 2. Clear gray queue
        # 3. Mark roots as gray and add to queue
        pass

    def mark_step(self, steps=1):
        """Perform incremental marking steps"""
        # TODO: Perform 'steps' marking steps
        # For each step:
        # 1. Pop an object from gray queue
        # 2. Mark it black
        # 3. Mark all its white references as gray and add to queue
        # Return True if marking is complete (gray queue empty)
        pass

    def sweep(self):
        """Remove all white objects"""
        # TODO: Remove all white objects
        pass

    def incremental_collect(self, steps_per_round=10):
        """Run a complete incremental collection"""
        # TODO: Run a complete incremental collection
        # 1. Initialize
        # 2. Keep calling mark_step until complete
        # 3. Sweep
        pass

    def object_count(self):
        """Return number of live objects"""
        return len(self.objects)

    def get_color(self, obj_id):
        """Get color of an object"""
        obj = self.objects.get(obj_id)
        return obj.color if obj else None

    def white_count(self):
        """Count white objects"""
        return sum(1 for obj in self.objects.values()
                   if obj.color == Color.WHITE)

    def gray_count(self):
        """Count gray objects"""
        return sum(1 for obj in self.objects.values()
                   if obj.color == Color.GRAY)

    def black_count(self):
        """Count black objects"""
        return sum(1 for obj in self.objects.values()
                   if obj.color == Color.BLACK)


import unittest


class TestTricolorGC(unittest.TestCase):
    def test_tricolor_marking(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate()

        gc.add_root(obj2)

        gc.init_collection()

        # Root should be gray
        self.assertEqual(gc.get_color(obj2), Color.GRAY)

        # Mark all
        while not gc.mark_step(1):
            pass

        # obj1 and obj2 should be black, obj3 white
        self.assertEqual(gc.get_color(obj1), Color.BLACK)
        self.assertEqual(gc.get_color(obj2), Color.BLACK)
        self.assertEqual(gc.get_color(obj3), Color.WHITE)

        gc.sweep()

        self.assertEqual(gc.object_count(), 2)

    def test_incremental_steps(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])

        gc.add_root(obj2)

        gc.init_collection()

        # First step: mark root
        complete = gc.mark_step(1)
        self.assertFalse(complete)
        self.assertEqual(gc.black_count(), 1)

        # Second step: mark referenced object
        complete = gc.mark_step(1)
        self.assertTrue(complete)
        self.assertEqual(gc.black_count(), 2)

    def test_initialization(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        gc.init_collection()

        # All non-root objects should be white, roots gray
        self.assertEqual(gc.get_color(obj1), Color.GRAY)
        self.assertEqual(gc.get_color(obj2), Color.WHITE)
        self.assertEqual(gc.gray_count(), 1)

    def test_full_incremental_collect(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate()

        gc.add_root(obj2)

        gc.incremental_collect(steps_per_round=1)

        self.assertEqual(gc.object_count(), 2)

    def test_multiple_roots(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)
        gc.add_root(obj2)

        gc.init_collection()

        self.assertEqual(gc.gray_count(), 2)

        while not gc.mark_step(1):
            pass

        self.assertEqual(gc.black_count(), 2)

    def test_transitive_marking(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])
        obj4 = gc.allocate([obj3])

        gc.add_root(obj4)

        gc.init_collection()

        while not gc.mark_step(1):
            pass

        # All should be black
        self.assertEqual(gc.black_count(), 4)
        self.assertEqual(gc.white_count(), 0)

    def test_gray_queue_processing(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate([obj1, obj2])

        gc.add_root(obj3)

        gc.init_collection()

        # Process gray queue step by step
        step1 = gc.mark_step(1)  # Process obj3
        self.assertFalse(step1)
        self.assertGreater(gc.gray_count(), 0)  # obj1 and obj2 now gray

        while not gc.mark_step(1):
            pass

        self.assertEqual(gc.black_count(), 3)

    def test_no_roots_all_white(self):
        gc = TricolorGC()

        gc.allocate()
        gc.allocate()
        gc.allocate()

        gc.init_collection()

        complete = gc.mark_step(1)
        self.assertTrue(complete)  # Nothing to mark

        self.assertEqual(gc.white_count(), 3)

        gc.sweep()

        self.assertEqual(gc.object_count(), 0)

    def test_batch_marking(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])

        gc.add_root(obj3)

        gc.init_collection()

        # Process multiple steps at once
        complete = gc.mark_step(5)
        self.assertTrue(complete)

        self.assertEqual(gc.black_count(), 3)

    def test_color_transitions(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])

        gc.add_root(obj2)

        # Initially white
        self.assertEqual(gc.get_color(obj2), Color.WHITE)

        gc.init_collection()

        # Root becomes gray
        self.assertEqual(gc.get_color(obj2), Color.GRAY)

        gc.mark_step(1)

        # After processing, becomes black
        self.assertEqual(gc.get_color(obj2), Color.BLACK)

    def test_shared_references(self):
        gc = TricolorGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj1])

        gc.add_root(obj2)
        gc.add_root(obj3)

        gc.init_collection()

        while not gc.mark_step(1):
            pass

        # All should be marked
        self.assertEqual(gc.black_count(), 3)


if __name__ == '__main__':
    unittest.main()
