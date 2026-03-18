# I AM NOT DONE

"""
Exercise: Arena Allocator

Arena allocator (bump allocator) allocates from a large buffer.
Extremely fast allocation (just increment pointer), but can only
free all allocations at once.

Your task: Implement an arena allocator.
"""


class Arena:
    """Arena/bump allocator"""

    def __init__(self, capacity):
        # TODO: Create new arena with given capacity
        pass

    def allocate(self, size, align=1):
        """Allocate size bytes with alignment"""
        # TODO: Allocate 'size' bytes with alignment
        # 1. Align current offset
        # 2. Check if enough space
        # 3. Return offset and increment
        pass

    def allocate_bytes(self, data):
        """Allocate space for byte data"""
        # TODO: Allocate space for byte data
        # Store data and return offset
        pass

    def reset(self):
        """Reset arena (free all allocations)"""
        # TODO: Reset arena (free all allocations)
        pass

    def used(self):
        """Return bytes used"""
        return self.offset

    def capacity(self):
        """Return total capacity"""
        return len(self.buffer)

    def available(self):
        """Return bytes available"""
        return self.capacity() - self.used()

    @staticmethod
    def _align_offset(offset, align):
        """Align offset to alignment boundary"""
        return (offset + align - 1) & ~(align - 1)


class ArenaString:
    """String allocated in arena"""

    def __init__(self, arena, s):
        # TODO: Allocate string in arena
        # Store bytes and remember offset/length
        pass

    def get(self):
        """Get the string value"""
        # TODO: Return string from arena
        pass


import unittest


class TestArena(unittest.TestCase):
    def test_basic_allocation(self):
        arena = Arena(1024)

        addr1 = arena.allocate(100)
        self.assertEqual(addr1, 0)
        self.assertEqual(arena.used(), 100)

        addr2 = arena.allocate(50)
        self.assertEqual(addr2, 100)
        self.assertEqual(arena.used(), 150)

    def test_alignment(self):
        arena = Arena(1024)

        arena.allocate(1)
        addr = arena.allocate(8, align=8)

        # Should be aligned to 8 bytes
        self.assertEqual(addr % 8, 0)

    def test_out_of_memory(self):
        arena = Arena(100)

        result = arena.allocate(150)
        self.assertIsNone(result)

    def test_reset(self):
        arena = Arena(1024)

        arena.allocate(100)
        arena.allocate(200)

        self.assertEqual(arena.used(), 300)

        arena.reset()

        self.assertEqual(arena.used(), 0)
        self.assertEqual(arena.available(), 1024)

    def test_allocate_bytes(self):
        arena = Arena(1024)

        data = b"hello world"
        addr = arena.allocate_bytes(data)

        self.assertIsNotNone(addr)
        self.assertGreaterEqual(arena.used(), len(data))

    def test_arena_string(self):
        arena = Arena(1024)

        s = ArenaString(arena, "hello world")
        self.assertEqual(s.get(), "hello world")

    def test_many_allocations(self):
        arena = Arena(1024)

        for i in range(100):
            addr = arena.allocate(8)
            if addr is None:
                break

        self.assertLessEqual(arena.used(), arena.capacity())

    def test_exact_capacity(self):
        arena = Arena(100)

        addr = arena.allocate(100)
        self.assertIsNotNone(addr)
        self.assertEqual(arena.available(), 0)

        # No more space
        addr2 = arena.allocate(1)
        self.assertIsNone(addr2)

    def test_alignment_padding(self):
        arena = Arena(1024)

        # Allocate 1 byte (offset now at 1)
        arena.allocate(1)

        # Allocate 8 bytes with 8-byte alignment
        # Should pad to offset 8
        addr = arena.allocate(8, align=8)
        self.assertEqual(addr, 8)

        # Total used: 1 (first alloc) + 7 (padding) + 8 (second alloc) = 16
        self.assertEqual(arena.used(), 16)

    def test_multiple_resets(self):
        arena = Arena(1024)

        for _ in range(10):
            arena.allocate(100)
            arena.reset()
            self.assertEqual(arena.used(), 0)

    def test_allocate_after_reset(self):
        arena = Arena(1024)

        arena.allocate(500)
        arena.reset()

        addr = arena.allocate(100)
        self.assertEqual(addr, 0)
        self.assertEqual(arena.used(), 100)

    def test_multiple_strings(self):
        arena = Arena(1024)

        s1 = ArenaString(arena, "hello")
        s2 = ArenaString(arena, "world")
        s3 = ArenaString(arena, "!")

        self.assertEqual(s1.get(), "hello")
        self.assertEqual(s2.get(), "world")
        self.assertEqual(s3.get(), "!")


if __name__ == '__main__':
    unittest.main()
