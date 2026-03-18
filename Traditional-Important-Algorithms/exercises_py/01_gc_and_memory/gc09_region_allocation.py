# I AM NOT DONE

"""
Exercise: Region-Based Allocation

Region-based allocation (also called Arena allocation) allocates objects
in regions/arenas. Entire regions are freed at once, making individual
deallocations unnecessary.

Your task: Implement a region-based memory allocator.
"""


class Region:
    """A memory region containing objects"""

    def __init__(self, region_id):
        self.id = region_id
        self.objects = []
        self.size = 0


class RegionAllocator:
    """Region-based memory allocator"""

    def __init__(self):
        self.regions = {}  # region_id -> Region
        self.objects = {}  # obj_id -> data
        self.next_region_id = 0
        self.next_object_id = 0
        self.current_region = None

    def create_region(self):
        """Create a new region and make it current"""
        # TODO: Create a new region and make it current
        pass

    def allocate(self, data):
        """Allocate an object in the current region"""
        # TODO: Allocate an object in the current region
        # Return error if no current region
        # Return object ID
        pass

    def free_region(self, region_id):
        """Free all objects in the region and remove the region"""
        # TODO: Free all objects in the region and remove the region
        pass

    def switch_region(self, region_id):
        """Switch to a different region"""
        # TODO: Switch to a different region
        # Return error if region doesn't exist
        pass

    def region_size(self, region_id):
        """Return total size of objects in region"""
        if region_id in self.regions:
            return self.regions[region_id].size
        return None

    def region_object_count(self, region_id):
        """Return number of objects in region"""
        if region_id in self.regions:
            return len(self.regions[region_id].objects)
        return None

    def total_objects(self):
        """Return total number of objects"""
        return len(self.objects)

    def total_regions(self):
        """Return total number of regions"""
        return len(self.regions)


import unittest


class TestRegionAllocator(unittest.TestCase):
    def test_region_creation(self):
        allocator = RegionAllocator()

        region1 = allocator.create_region()
        region2 = allocator.create_region()

        self.assertEqual(allocator.total_regions(), 2)
        self.assertNotEqual(region1, region2)

    def test_allocation_in_region(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        obj1 = allocator.allocate([1, 2, 3])
        obj2 = allocator.allocate([4, 5, 6])

        self.assertEqual(allocator.region_object_count(region), 2)
        self.assertEqual(allocator.total_objects(), 2)

    def test_free_region(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        allocator.allocate([1, 2, 3])
        allocator.allocate([4, 5, 6])

        self.assertEqual(allocator.total_objects(), 2)

        allocator.free_region(region)

        self.assertEqual(allocator.total_objects(), 0)
        self.assertEqual(allocator.total_regions(), 0)

    def test_multiple_regions(self):
        allocator = RegionAllocator()

        region1 = allocator.create_region()
        allocator.allocate([1])

        region2 = allocator.create_region()
        allocator.allocate([2])
        allocator.allocate([3])

        self.assertEqual(allocator.region_object_count(region1), 1)
        self.assertEqual(allocator.region_object_count(region2), 2)

        allocator.free_region(region1)

        self.assertEqual(allocator.total_objects(), 2)
        self.assertEqual(allocator.total_regions(), 1)

    def test_switch_region(self):
        allocator = RegionAllocator()

        region1 = allocator.create_region()
        allocator.allocate([1])

        region2 = allocator.create_region()
        allocator.allocate([2])

        allocator.switch_region(region1)
        allocator.allocate([3])

        self.assertEqual(allocator.region_object_count(region1), 2)
        self.assertEqual(allocator.region_object_count(region2), 1)

    def test_region_size_tracking(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        allocator.allocate([1, 2, 3])  # 3 bytes
        allocator.allocate([4, 5])     # 2 bytes

        size = allocator.region_size(region)
        self.assertIsNotNone(size)
        self.assertGreater(size, 0)

    def test_allocate_without_region(self):
        allocator = RegionAllocator()

        # Should fail or return None when no region
        result = allocator.allocate([1, 2, 3])
        self.assertIsNone(result)

    def test_switch_to_nonexistent_region(self):
        allocator = RegionAllocator()

        result = allocator.switch_region(999)
        # Should return error
        self.assertIsNotNone(result)

    def test_sequential_allocations(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        for i in range(10):
            allocator.allocate([i])

        self.assertEqual(allocator.region_object_count(region), 10)

    def test_region_isolation(self):
        allocator = RegionAllocator()

        region1 = allocator.create_region()
        allocator.allocate([1])

        region2 = allocator.create_region()
        allocator.allocate([2])

        allocator.free_region(region1)

        # region2 should be unaffected
        self.assertEqual(allocator.region_object_count(region2), 1)

    def test_empty_region(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        self.assertEqual(allocator.region_object_count(region), 0)
        self.assertEqual(allocator.region_size(region), 0)

    def test_large_allocations(self):
        allocator = RegionAllocator()

        region = allocator.create_region()

        large_data = [0] * 1000
        allocator.allocate(large_data)

        self.assertEqual(allocator.region_object_count(region), 1)
        self.assertGreater(allocator.region_size(region), 0)


if __name__ == '__main__':
    unittest.main()
