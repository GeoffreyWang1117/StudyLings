# I AM NOT DONE

"""
Exercise: Memory Pool

Memory pool pre-allocates fixed-size blocks and reuses them.
Very efficient for allocating many objects of the same size.

Your task: Implement a memory pool allocator.
"""


class MemoryPool:
    """Fixed-size block memory pool"""

    def __init__(self, block_size, initial_blocks):
        # TODO: Create pool with initial blocks
        # All blocks start in free list
        pass

    def allocate(self):
        """Allocate a block"""
        # TODO: Allocate a block
        # 1. Pop from free list if available
        # 2. Otherwise allocate new block
        # 3. Return block reference/index
        pass

    def deallocate(self, block_id):
        """Return block to free list"""
        # TODO: Return block to free list
        # Verify block_id is valid (owned by this pool)
        pass

    def allocated_count(self):
        """Return number of allocated blocks"""
        return self.allocated

    def free_count(self):
        """Return number of free blocks"""
        return len(self.free_list)

    def total_blocks(self):
        """Return total number of blocks"""
        return len(self.blocks)

    def _allocate_block(self):
        """Allocate a new block from system"""
        # TODO: Create new block and add to blocks list
        pass

    def _is_owned(self, block_id):
        """Check if block_id belongs to this pool"""
        # TODO: Check if block_id is valid
        pass


class TypedPool:
    """Type-safe wrapper around MemoryPool"""

    def __init__(self, initial_capacity):
        # TODO: Create typed pool
        # Use MemoryPool internally
        pass

    def allocate(self, value):
        """Allocate and initialize with value"""
        # TODO: Allocate block and store value
        # Return object reference
        pass

    def deallocate(self, obj_ref):
        """Deallocate object"""
        # TODO: Clear value and return block to pool
        pass

    def allocated_count(self):
        """Return number of allocated objects"""
        return self.pool.allocated_count()


import unittest


class TestMemoryPool(unittest.TestCase):
    def test_pool_allocation(self):
        pool = MemoryPool(block_size=64, initial_blocks=10)

        self.assertEqual(pool.total_blocks(), 10)
        self.assertEqual(pool.free_count(), 10)

        block = pool.allocate()
        self.assertEqual(pool.free_count(), 9)
        self.assertEqual(pool.allocated_count(), 1)

        pool.deallocate(block)
        self.assertEqual(pool.free_count(), 10)
        self.assertEqual(pool.allocated_count(), 0)

    def test_pool_reuse(self):
        pool = MemoryPool(block_size=64, initial_blocks=5)

        block1 = pool.allocate()
        pool.deallocate(block1)

        block2 = pool.allocate()

        # Should reuse the same block
        self.assertEqual(block1, block2)
        self.assertEqual(pool.total_blocks(), 5)

    def test_pool_expansion(self):
        pool = MemoryPool(block_size=64, initial_blocks=2)

        b1 = pool.allocate()
        b2 = pool.allocate()
        b3 = pool.allocate()

        # Should have allocated more blocks
        self.assertEqual(pool.total_blocks(), 3)

    def test_typed_pool(self):
        pool = TypedPool(initial_capacity=10)

        obj = pool.allocate("hello")

        self.assertIsNotNone(obj)

        pool.deallocate(obj)
        self.assertEqual(pool.allocated_count(), 0)

    def test_invalid_dealloc(self):
        pool = MemoryPool(block_size=64, initial_blocks=10)

        fake_block = 9999

        result = pool.deallocate(fake_block)
        self.assertIsNone(result)

    def test_multiple_allocations(self):
        pool = MemoryPool(block_size=32, initial_blocks=5)

        blocks = []
        for _ in range(10):
            blocks.append(pool.allocate())

        self.assertEqual(pool.allocated_count(), 10)
        self.assertEqual(pool.total_blocks(), 10)

    def test_partial_deallocation(self):
        pool = MemoryPool(block_size=64, initial_blocks=10)

        blocks = [pool.allocate() for _ in range(5)]

        pool.deallocate(blocks[1])
        pool.deallocate(blocks[3])

        self.assertEqual(pool.allocated_count(), 3)
        self.assertEqual(pool.free_count(), 7)

    def test_allocate_all_free_all(self):
        pool = MemoryPool(block_size=64, initial_blocks=5)

        blocks = [pool.allocate() for _ in range(5)]

        self.assertEqual(pool.free_count(), 0)

        for block in blocks:
            pool.deallocate(block)

        self.assertEqual(pool.free_count(), 5)
        self.assertEqual(pool.allocated_count(), 0)

    def test_typed_pool_values(self):
        pool = TypedPool(initial_capacity=5)

        obj1 = pool.allocate(42)
        obj2 = pool.allocate("hello")
        obj3 = pool.allocate([1, 2, 3])

        self.assertEqual(pool.allocated_count(), 3)

    def test_sequential_alloc_dealloc(self):
        pool = MemoryPool(block_size=64, initial_blocks=3)

        for _ in range(10):
            block = pool.allocate()
            self.assertIsNotNone(block)
            pool.deallocate(block)

        # Should reuse blocks without expanding
        self.assertEqual(pool.total_blocks(), 3)

    def test_zero_initial_blocks(self):
        pool = MemoryPool(block_size=64, initial_blocks=0)

        self.assertEqual(pool.total_blocks(), 0)

        block = pool.allocate()
        self.assertIsNotNone(block)
        self.assertEqual(pool.total_blocks(), 1)

    def test_large_pool(self):
        pool = MemoryPool(block_size=128, initial_blocks=100)

        blocks = [pool.allocate() for _ in range(50)]

        self.assertEqual(pool.allocated_count(), 50)
        self.assertEqual(pool.free_count(), 50)


if __name__ == '__main__':
    unittest.main()
