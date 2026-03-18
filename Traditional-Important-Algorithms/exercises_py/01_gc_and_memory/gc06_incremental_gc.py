# I AM NOT DONE

"""
Exercise: Incremental Garbage Collection

Incremental GC breaks up collection work into small increments
to avoid long pause times. Based on tricolor marking.

Your task: Implement an incremental garbage collector with configurable work units.
"""

from enum import Enum
from collections import deque


class Color(Enum):
    """Object color in tricolor marking"""
    WHITE = "white"
    GRAY = "gray"
    BLACK = "black"


class GCPhase(Enum):
    """Phases of incremental GC"""
    IDLE = "Idle"
    MARKING = "Marking"
    SWEEPING = "Sweeping"


class IncrementalGC:
    """Incremental garbage collector"""

    def __init__(self):
        self.objects = {}  # obj_id -> (color, references)
        self.next_id = 0
        self.roots = set()
        self.gray_queue = deque()
        self.phase = GCPhase.IDLE
        self.sweep_iterator = []
        self.sweep_index = 0

    def allocate(self, references=None):
        """Allocate a new object"""
        obj_id = self.next_id
        self.next_id += 1
        self.objects[obj_id] = (Color.WHITE, references if references else [])
        return obj_id

    def add_root(self, obj_id):
        """Add an object as a root"""
        self.roots.add(obj_id)

    def start_collection(self):
        """Start a new collection cycle"""
        # TODO: Start a new collection cycle
        # Initialize tricolor marking
        pass

    def incremental_step(self, work_units=1):
        """Perform one incremental step based on current phase"""
        # TODO: Perform one incremental step based on current phase
        # In Marking phase: mark 'work_units' objects
        # In Sweeping phase: sweep 'work_units' objects
        # Transition between phases as needed
        pass

    def _mark_work(self, units):
        """Do marking work"""
        # TODO: Do 'units' amount of marking work
        # Return True if marking phase complete
        pass

    def _sweep_work(self, units):
        """Do sweeping work"""
        # TODO: Do 'units' amount of sweeping work
        # Return True if sweeping phase complete
        pass

    def get_phase(self):
        """Get current GC phase"""
        return self.phase.value

    def object_count(self):
        """Return number of live objects"""
        return len(self.objects)


import unittest


class TestIncrementalGC(unittest.TestCase):
    def test_incremental_collection(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        gc.start_collection()
        self.assertEqual(gc.get_phase(), "Marking")

        # Run incremental steps
        for _ in range(10):
            gc.incremental_step(1)

        self.assertEqual(gc.get_phase(), "Idle")
        self.assertEqual(gc.object_count(), 1)

    def test_multiple_incremental_cycles(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.start_collection()
        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        self.assertEqual(gc.object_count(), 1)

        obj2 = gc.allocate()

        gc.start_collection()
        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        self.assertEqual(gc.object_count(), 1)

    def test_phase_transitions(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        self.assertEqual(gc.get_phase(), "Idle")

        gc.start_collection()
        self.assertEqual(gc.get_phase(), "Marking")

        # Do some marking work
        gc.incremental_step(5)

        # Should eventually transition to sweeping then idle
        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        self.assertEqual(gc.get_phase(), "Idle")

    def test_small_work_units(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])

        gc.add_root(obj3)

        gc.start_collection()

        # Use very small work units
        steps = 0
        while gc.get_phase() != "Idle":
            gc.incremental_step(1)
            steps += 1

        # Should take multiple steps
        self.assertGreater(steps, 1)
        self.assertEqual(gc.object_count(), 3)

    def test_large_work_units(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)

        gc.start_collection()

        # Use large work units
        gc.incremental_step(100)

        # Should complete quickly
        self.assertEqual(gc.get_phase(), "Idle")
        self.assertEqual(gc.object_count(), 1)

    def test_marking_progress(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])

        gc.add_root(obj2)

        gc.start_collection()

        self.assertEqual(gc.get_phase(), "Marking")

        # Do one unit of work
        gc.incremental_step(1)

        # Should still be marking or moved to sweeping
        self.assertIn(gc.get_phase(), ["Marking", "Sweeping", "Idle"])

    def test_sweeping_progress(self):
        gc = IncrementalGC()

        # Allocate many objects
        obj1 = gc.allocate()
        for _ in range(10):
            gc.allocate()

        gc.add_root(obj1)

        gc.start_collection()

        # Fast-forward through marking
        while gc.get_phase() == "Marking":
            gc.incremental_step(10)

        # Should be in sweeping phase
        self.assertIn(gc.get_phase(), ["Sweeping", "Idle"])

    def test_no_roots(self):
        gc = IncrementalGC()

        gc.allocate()
        gc.allocate()
        gc.allocate()

        gc.start_collection()

        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        self.assertEqual(gc.object_count(), 0)

    def test_interleaved_allocation(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.start_collection()

        # Do some GC work
        gc.incremental_step(1)

        # Allocate during GC (should be handled)
        obj2 = gc.allocate()

        # Finish GC
        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        # obj1 should survive, obj2 status depends on implementation
        self.assertGreaterEqual(gc.object_count(), 1)

    def test_multiple_roots(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)
        gc.add_root(obj2)

        gc.start_collection()

        while gc.get_phase() != "Idle":
            gc.incremental_step(1)

        self.assertEqual(gc.object_count(), 2)

    def test_complex_graph(self):
        gc = IncrementalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj1, obj2])
        obj4 = gc.allocate([obj2])
        obj5 = gc.allocate()

        gc.add_root(obj3)

        gc.start_collection()

        while gc.get_phase() != "Idle":
            gc.incremental_step(2)

        # obj1-4 reachable, obj5 is garbage
        self.assertEqual(gc.object_count(), 4)


if __name__ == '__main__':
    unittest.main()
