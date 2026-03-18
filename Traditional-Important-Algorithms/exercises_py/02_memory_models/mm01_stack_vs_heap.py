# I AM NOT DONE

"""
Exercise: Stack vs Heap Allocation

Understanding the difference between stack and heap allocation is fundamental.
Stack: LIFO, fast, automatic cleanup, fixed size, local scope
Heap: flexible size, manual management, slower, can outlive scope

Your task: Implement a simple memory allocator that simulates stack and heap.
"""

from enum import Enum


class AllocLocation(Enum):
    """Allocation location"""
    STACK = "stack"
    HEAP = "heap"


class MemorySimulator:
    """Simulates stack and heap memory"""

    def __init__(self, stack_capacity):
        self.stack = [0] * stack_capacity
        self.stack_pointer = 0
        self.heap = []  # List of optional byte arrays (None = free slot)
        self.stack_capacity = stack_capacity

    def stack_alloc(self, size):
        """Allocate on stack"""
        # TODO: Allocate on stack
        # Return the address (stack_pointer) if successful
        # Return error if not enough space
        pass

    def stack_free(self, size):
        """Free from stack"""
        # TODO: Free from stack (just move stack pointer)
        # Stack frees in LIFO order
        pass

    def heap_alloc(self, data):
        """Allocate on heap"""
        # TODO: Allocate on heap
        # Find a free slot or add new one
        # Return the index as "address"
        pass

    def heap_free(self, addr):
        """Free heap allocation"""
        # TODO: Free heap allocation
        # Mark slot as free (None)
        pass

    def stack_usage(self):
        """Return current stack usage"""
        return self.stack_pointer

    def heap_usage(self):
        """Return number of allocated heap slots"""
        return sum(1 for slot in self.heap if slot is not None)

    def can_stack_alloc(self, size):
        """Check if stack has enough space"""
        # TODO: Check if stack has enough space
        pass


import unittest


class TestMemorySimulator(unittest.TestCase):
    def test_stack_allocation(self):
        sim = MemorySimulator(1024)

        addr1 = sim.stack_alloc(100)
        self.assertEqual(addr1, 0)
        self.assertEqual(sim.stack_usage(), 100)

        addr2 = sim.stack_alloc(50)
        self.assertEqual(addr2, 100)
        self.assertEqual(sim.stack_usage(), 150)

    def test_stack_free_lifo(self):
        sim = MemorySimulator(1024)

        sim.stack_alloc(100)
        sim.stack_alloc(50)

        sim.stack_free(50)
        self.assertEqual(sim.stack_usage(), 100)

        sim.stack_free(100)
        self.assertEqual(sim.stack_usage(), 0)

    def test_stack_overflow(self):
        sim = MemorySimulator(100)

        result = sim.stack_alloc(150)
        self.assertIsNone(result)

    def test_heap_allocation(self):
        sim = MemorySimulator(1024)

        addr1 = sim.heap_alloc([1, 2, 3])
        addr2 = sim.heap_alloc([4, 5, 6])

        self.assertEqual(sim.heap_usage(), 2)
        self.assertNotEqual(addr1, addr2)

    def test_heap_free_and_reuse(self):
        sim = MemorySimulator(1024)

        addr1 = sim.heap_alloc([1, 2, 3])
        sim.heap_free(addr1)

        self.assertEqual(sim.heap_usage(), 0)

        addr2 = sim.heap_alloc([4, 5, 6])
        # Should reuse the freed slot
        self.assertEqual(addr1, addr2)

    def test_can_stack_alloc(self):
        sim = MemorySimulator(100)

        self.assertTrue(sim.can_stack_alloc(50))
        self.assertTrue(sim.can_stack_alloc(100))
        self.assertFalse(sim.can_stack_alloc(101))

        sim.stack_alloc(50)

        self.assertTrue(sim.can_stack_alloc(50))
        self.assertFalse(sim.can_stack_alloc(51))

    def test_stack_multiple_allocs(self):
        sim = MemorySimulator(1000)

        addrs = []
        for i in range(10):
            addr = sim.stack_alloc(10)
            addrs.append(addr)

        self.assertEqual(sim.stack_usage(), 100)
        self.assertEqual(addrs, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])

    def test_heap_multiple_allocs(self):
        sim = MemorySimulator(1024)

        addrs = []
        for i in range(10):
            addr = sim.heap_alloc([i])
            addrs.append(addr)

        self.assertEqual(sim.heap_usage(), 10)
        self.assertEqual(len(set(addrs)), 10)  # All unique

    def test_heap_fragmentation(self):
        sim = MemorySimulator(1024)

        addr0 = sim.heap_alloc([0])
        addr1 = sim.heap_alloc([1])
        addr2 = sim.heap_alloc([2])

        sim.heap_free(addr1)

        self.assertEqual(sim.heap_usage(), 2)

        # Next allocation should reuse freed slot
        addr3 = sim.heap_alloc([3])
        self.assertEqual(addr3, addr1)

    def test_stack_underflow(self):
        sim = MemorySimulator(1024)

        sim.stack_alloc(100)

        sim.stack_free(100)

        # Trying to free more than allocated
        result = sim.stack_free(100)
        self.assertIsNone(result)

    def test_mixed_operations(self):
        sim = MemorySimulator(1024)

        # Stack operations
        sim.stack_alloc(100)
        sim.stack_alloc(200)

        # Heap operations
        heap_addr = sim.heap_alloc([1, 2, 3])

        self.assertEqual(sim.stack_usage(), 300)
        self.assertEqual(sim.heap_usage(), 1)

        sim.stack_free(200)
        sim.heap_free(heap_addr)

        self.assertEqual(sim.stack_usage(), 100)
        self.assertEqual(sim.heap_usage(), 0)

    def test_heap_free_invalid(self):
        sim = MemorySimulator(1024)

        sim.heap_alloc([1, 2, 3])

        # Try to free invalid address
        result = sim.heap_free(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
