# I AM NOT DONE

"""
Exercise: Generational Garbage Collection

Generational GC is based on the observation that most objects die young.
Objects are separated into generations (young, old) and young generation
is collected more frequently.

Your task: Implement a simple two-generation garbage collector.
"""

from enum import Enum


class Generation(Enum):
    """Object generation"""
    YOUNG = "young"
    OLD = "old"


class Object:
    """Represents an object with generation tracking"""

    def __init__(self, obj_id, generation, references=None):
        self.id = obj_id
        self.generation = generation
        self.age = 0
        self.references = references if references is not None else []


class GenerationalGC:
    """Two-generation garbage collector"""

    def __init__(self, promotion_threshold=2):
        self.objects = {}  # obj_id -> Object
        self.next_id = 0
        self.roots = set()
        self.promotion_threshold = promotion_threshold

    def allocate(self, references=None):
        """Allocate a new object (always starts in young generation)"""
        obj_id = self.next_id
        self.next_id += 1

        obj = Object(obj_id, Generation.YOUNG, references if references else [])
        self.objects[obj_id] = obj
        return obj_id

    def add_root(self, obj_id):
        """Add an object as a root"""
        self.roots.add(obj_id)

    def _mark_from(self, obj_id, marked):
        """Mark objects reachable from obj_id"""
        if obj_id in marked:
            return

        marked.add(obj_id)

        if obj_id in self.objects:
            obj = self.objects[obj_id]
            for ref_id in obj.references:
                self._mark_from(ref_id, marked)

    def minor_collection(self):
        """Collect young generation only"""
        # TODO: Implement minor collection (young generation only)
        # 1. Mark all reachable objects from roots
        # 2. Remove unmarked young objects
        # 3. Age surviving young objects
        # 4. Promote old enough objects to old generation
        pass

    def major_collection(self):
        """Collect all generations"""
        # TODO: Implement major collection (all generations)
        # 1. Mark all reachable objects from roots
        # 2. Remove all unmarked objects (young and old)
        # 3. Age surviving objects
        # 4. Promote objects that reach threshold
        pass

    def object_count(self):
        """Return total number of objects"""
        return len(self.objects)

    def young_count(self):
        """Return number of young generation objects"""
        return sum(1 for obj in self.objects.values()
                   if obj.generation == Generation.YOUNG)

    def old_count(self):
        """Return number of old generation objects"""
        return sum(1 for obj in self.objects.values()
                   if obj.generation == Generation.OLD)


import unittest


class TestGenerationalGC(unittest.TestCase):
    def test_minor_collection(self):
        gc = GenerationalGC(promotion_threshold=2)

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        self.assertEqual(gc.young_count(), 2)

        gc.minor_collection()

        # obj2 should be collected
        self.assertEqual(gc.young_count(), 1)

    def test_promotion(self):
        gc = GenerationalGC(promotion_threshold=2)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        self.assertEqual(gc.young_count(), 1)
        self.assertEqual(gc.old_count(), 0)

        gc.minor_collection()
        gc.minor_collection()

        # After 2 collections, should be promoted
        self.assertEqual(gc.young_count(), 0)
        self.assertEqual(gc.old_count(), 1)

    def test_major_collection(self):
        gc = GenerationalGC(promotion_threshold=1)

        obj1 = gc.allocate()
        obj2 = gc.allocate()

        gc.add_root(obj1)

        gc.minor_collection()  # obj1 promoted, obj2 collected

        obj3 = gc.allocate()

        gc.major_collection()

        # Only obj1 should remain
        self.assertEqual(gc.object_count(), 1)

    def test_young_objects_die_young(self):
        gc = GenerationalGC()

        # Allocate many young objects
        for _ in range(10):
            gc.allocate()

        # Only root one
        obj_root = gc.allocate()
        gc.add_root(obj_root)

        gc.minor_collection()

        # Only rooted object survives
        self.assertEqual(gc.young_count(), 1)

    def test_promotion_threshold(self):
        gc = GenerationalGC(promotion_threshold=3)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.minor_collection()
        self.assertEqual(gc.old_count(), 0)

        gc.minor_collection()
        self.assertEqual(gc.old_count(), 0)

        gc.minor_collection()
        # Should be promoted after 3 collections
        self.assertEqual(gc.old_count(), 1)

    def test_old_gen_survives_minor(self):
        gc = GenerationalGC(promotion_threshold=1)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.minor_collection()  # Promote to old

        self.assertEqual(gc.old_count(), 1)

        # Allocate young garbage
        gc.allocate()
        gc.allocate()

        gc.minor_collection()

        # Old object survives, young garbage collected
        self.assertEqual(gc.old_count(), 1)
        self.assertEqual(gc.young_count(), 0)

    def test_cross_generation_references(self):
        gc = GenerationalGC(promotion_threshold=1)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.minor_collection()  # obj1 promoted to old

        obj2 = gc.allocate([obj1])  # Young object references old
        gc.add_root(obj2)

        gc.minor_collection()

        # Both should survive
        self.assertEqual(gc.object_count(), 2)

    def test_multiple_promotions(self):
        gc = GenerationalGC(promotion_threshold=2)

        obj1 = gc.allocate()
        obj2 = gc.allocate()
        obj3 = gc.allocate()

        gc.add_root(obj1)
        gc.add_root(obj2)
        gc.add_root(obj3)

        gc.minor_collection()
        self.assertEqual(gc.old_count(), 0)

        gc.minor_collection()
        # All three should be promoted
        self.assertEqual(gc.old_count(), 3)
        self.assertEqual(gc.young_count(), 0)

    def test_major_cleans_old_gen(self):
        gc = GenerationalGC(promotion_threshold=1)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        gc.minor_collection()  # Promote to old

        gc.roots.clear()  # Remove root

        gc.major_collection()

        # Should be collected even though it's old
        self.assertEqual(gc.object_count(), 0)

    def test_transitive_reachability_young(self):
        gc = GenerationalGC()

        obj1 = gc.allocate()
        obj2 = gc.allocate([obj1])
        obj3 = gc.allocate([obj2])

        gc.add_root(obj3)

        gc.minor_collection()

        # All three should survive
        self.assertEqual(gc.young_count(), 3)

    def test_aging_increments(self):
        gc = GenerationalGC(promotion_threshold=5)

        obj1 = gc.allocate()
        gc.add_root(obj1)

        for i in range(4):
            gc.minor_collection()
            # Should still be young
            self.assertEqual(gc.young_count(), 1)
            self.assertEqual(gc.old_count(), 0)

        gc.minor_collection()
        # Now should be promoted
        self.assertEqual(gc.old_count(), 1)


if __name__ == '__main__':
    unittest.main()
