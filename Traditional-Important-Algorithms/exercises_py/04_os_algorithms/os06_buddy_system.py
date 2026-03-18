# I AM NOT DONE

"""
os06_buddy_system.py

The Buddy System is a memory allocation algorithm that divides memory into partitions
to try to satisfy memory requests as efficiently as possible. When a request is made,
it rounds up to the next power of 2 and allocates a block of that size by splitting
larger blocks if necessary.

Your task: Implement a buddy system memory allocator.
"""

from typing import Dict, List, Optional
import unittest


class Block:
    """Represents a memory block."""
    def __init__(self, start: int, size: int):
        self.start = start
        self.size = size
        self.allocated = False


class BuddySystem:
    """Buddy system memory allocator."""

    def __init__(self, total_size: int, min_block_size: int):
        """
        TODO: Initialize the buddy system.

        Steps:
        1. Ensure total_size is a power of 2
        2. Create free lists for each power of 2 from min_block_size to total_size
        3. Add one large block to the largest free list

        Args:
            total_size: Total memory size (must be power of 2)
            min_block_size: Minimum block size (must be power of 2)
        """
        pass  # TODO: Implement this

    def _get_buddy_address(self, addr: int, size: int) -> int:
        """
        TODO: Calculate the address of the buddy block.

        The buddy of a block at address addr with size is at addr XOR size.

        Args:
            addr: Block address
            size: Block size

        Returns:
            Buddy block address
        """
        pass  # TODO: Implement this

    def _next_power_of_2(self, size: int) -> int:
        """
        TODO: Round up to the next power of 2.

        Args:
            size: Size to round up

        Returns:
            Next power of 2
        """
        pass  # TODO: Implement this

    def allocate(self, size: int) -> Optional[int]:
        """
        TODO: Allocate a block of at least 'size' bytes.

        Steps:
        1. Round size up to next power of 2, but at least min_block_size
        2. Find a free block of appropriate size (may need to split larger blocks)
        3. Mark as allocated and return block ID

        Args:
            size: Requested size in bytes

        Returns:
            Block ID, or None if allocation fails
        """
        pass  # TODO: Implement this

    def _find_and_remove_free_block(self, size: int) -> Optional[Block]:
        """
        TODO: Find and remove a free block of the given size.

        If not available, try to split a larger block recursively.

        Args:
            size: Size of block to find

        Returns:
            Free block, or None if not available
        """
        pass  # TODO: Implement this

    def _split_block(self, block: Block) -> tuple:
        """
        TODO: Split a block into two buddy blocks of half the size.

        Args:
            block: Block to split

        Returns:
            Tuple of (left_block, right_block)
        """
        pass  # TODO: Implement this

    def free(self, block_id: int) -> bool:
        """
        TODO: Free a block and merge with buddy if possible.

        Steps:
        1. Remove from allocated_blocks
        2. Try to merge with buddy recursively
        3. Add to appropriate free list

        Args:
            block_id: ID of block to free

        Returns:
            True if successful, False otherwise
        """
        pass  # TODO: Implement this

    def _try_merge(self, block: Block) -> Block:
        """
        TODO: Try to merge block with its buddy.

        Steps:
        1. Calculate buddy address
        2. Check if buddy is free and same size
        3. If yes, merge and try to merge the larger block recursively
        4. If no, return the block as-is

        Args:
            block: Block to merge

        Returns:
            Merged block (or original if no merge)
        """
        pass  # TODO: Implement this

    def _remove_from_free_list(self, block: Block) -> bool:
        """
        TODO: Remove a specific block from its free list.

        Args:
            block: Block to remove

        Returns:
            True if found and removed, False otherwise
        """
        pass  # TODO: Implement this

    def _add_to_free_list(self, block: Block) -> None:
        """
        TODO: Add a block to the appropriate free list based on its size.

        Args:
            block: Block to add
        """
        pass  # TODO: Implement this

    def get_block_info(self, block_id: int) -> Optional[Block]:
        """Get information about an allocated block."""
        return self.allocated_blocks.get(block_id)

    def total_free_memory(self) -> int:
        """
        TODO: Calculate total free memory across all free lists.

        Returns:
            Total free memory
        """
        pass  # TODO: Implement this

    def free_blocks_of_size(self, size: int) -> int:
        """
        TODO: Count number of free blocks of a specific size.

        Args:
            size: Block size to count

        Returns:
            Number of free blocks of that size
        """
        pass  # TODO: Implement this

    def fragmentation_ratio(self) -> float:
        """
        TODO: Calculate fragmentation as ratio of largest free block to total free memory.

        Lower fragmentation means memory is less fragmented.

        Returns:
            Fragmentation ratio (0.0 to 1.0)
        """
        pass  # TODO: Implement this


class TestBuddySystem(unittest.TestCase):
    """Test cases for Buddy System."""

    def test_simple_allocation(self):
        """Test basic allocation."""
        buddy = BuddySystem(1024, 64)

        block1 = buddy.allocate(64)
        block2 = buddy.allocate(128)

        self.assertIsNotNone(block1)
        self.assertIsNotNone(block2)
        self.assertIsNotNone(buddy.get_block_info(block1))
        self.assertIsNotNone(buddy.get_block_info(block2))

    def test_allocation_and_free(self):
        """Test allocating and freeing."""
        buddy = BuddySystem(1024, 64)

        block = buddy.allocate(128)
        info = buddy.get_block_info(block)

        self.assertEqual(info.size, 128)

        buddy.free(block)

        # After freeing, should be able to allocate again
        block2 = buddy.allocate(128)
        self.assertIsNotNone(buddy.get_block_info(block2))

    def test_buddy_merging(self):
        """Test merging of buddy blocks."""
        buddy = BuddySystem(1024, 64)

        # Allocate two buddy blocks
        block1 = buddy.allocate(256)
        block2 = buddy.allocate(256)

        buddy.free(block1)
        buddy.free(block2)

        # After freeing both buddies, they should merge
        # We should be able to allocate a 512-byte block
        large_block = buddy.allocate(512)
        self.assertIsNotNone(buddy.get_block_info(large_block))

    def test_splitting(self):
        """Test block splitting."""
        buddy = BuddySystem(1024, 64)

        # Request small block, should split larger ones
        block = buddy.allocate(64)
        info = buddy.get_block_info(block)

        self.assertEqual(info.size, 64)

    def test_out_of_memory(self):
        """Test allocation when out of memory."""
        buddy = BuddySystem(256, 64)

        buddy.allocate(128)
        buddy.allocate(64)
        buddy.allocate(64)

        # Should be out of memory now
        result = buddy.allocate(64)
        self.assertIsNone(result)

    def test_power_of_two_rounding(self):
        """Test rounding to power of 2."""
        buddy = BuddySystem(1024, 64)

        # Request 100 bytes, should allocate 128 (next power of 2)
        block = buddy.allocate(100)
        info = buddy.get_block_info(block)

        self.assertEqual(info.size, 128)

    def test_minimum_block_size(self):
        """Test minimum block size enforcement."""
        buddy = BuddySystem(1024, 64)

        # Request less than minimum, should allocate minimum
        block = buddy.allocate(32)
        info = buddy.get_block_info(block)

        self.assertEqual(info.size, 64)

    def test_multiple_allocations(self):
        """Test multiple allocations."""
        buddy = BuddySystem(1024, 64)

        blocks = []
        for _ in range(5):
            block = buddy.allocate(64)
            self.assertIsNotNone(block)
            blocks.append(block)

        # All blocks should be valid
        for block_id in blocks:
            self.assertIsNotNone(buddy.get_block_info(block_id))

        # Free all blocks
        for block_id in blocks:
            buddy.free(block_id)

    def test_fragmentation(self):
        """Test fragmentation calculation."""
        buddy = BuddySystem(1024, 64)

        b1 = buddy.allocate(64)
        _ = buddy.allocate(64)
        b3 = buddy.allocate(64)

        # Free alternating blocks to create fragmentation
        buddy.free(b1)
        buddy.free(b3)

        frag = buddy.fragmentation_ratio()
        self.assertGreaterEqual(frag, 0.0)
        self.assertLessEqual(frag, 1.0)

    def test_total_free_memory(self):
        """Test total free memory tracking."""
        buddy = BuddySystem(1024, 64)

        initial_free = buddy.total_free_memory()
        self.assertEqual(initial_free, 1024)

        block = buddy.allocate(256)

        after_alloc = buddy.total_free_memory()
        self.assertEqual(after_alloc, 1024 - 256)

        buddy.free(block)

        after_free = buddy.total_free_memory()
        self.assertEqual(after_free, 1024)

    def test_complex_merging(self):
        """Test complex merging scenario."""
        buddy = BuddySystem(1024, 64)

        # Allocate several blocks
        b1 = buddy.allocate(128)
        b2 = buddy.allocate(128)
        b3 = buddy.allocate(128)
        b4 = buddy.allocate(128)

        # Free in specific order to test merging
        buddy.free(b2)
        buddy.free(b1)
        buddy.free(b4)
        buddy.free(b3)

        # All blocks should be merged back
        self.assertEqual(buddy.total_free_memory(), 1024)


if __name__ == '__main__':
    unittest.main()
