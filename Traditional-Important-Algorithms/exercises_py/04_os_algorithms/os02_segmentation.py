# I AM NOT DONE

"""
os02_segmentation.py

Segmentation is a memory management scheme that supports the user's view of memory.
A program is a collection of segments such as main program, procedures, functions,
stack, symbol table, arrays, etc. Each segment has a name and a length.

Your task: Implement a segmentation system with a segment table for address translation.
"""

from typing import Dict, Optional
import unittest


class SegmentId:
    """Represents a segment identifier."""
    def __init__(self, seg_id: int):
        self.id = seg_id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, SegmentId) and self.id == other.id


class SegmentTableEntry:
    """Entry in the segment table."""
    def __init__(self, base: int, limit: int, readable: bool,
                 writable: bool, executable: bool):
        self.base = base
        self.limit = limit
        self.valid = True
        self.readable = readable
        self.writable = writable
        self.executable = executable


class SegmentTable:
    """Segment table for address translation."""

    def __init__(self):
        self.entries: Dict[SegmentId, SegmentTableEntry] = {}

    def add_segment(self, segment_id: SegmentId, base: int, limit: int,
                   readable: bool, writable: bool, executable: bool) -> None:
        """
        TODO: Add a new segment to the segment table.

        Args:
            segment_id: Segment identifier
            base: Base address in physical memory
            limit: Length of the segment
            readable: Whether segment is readable
            writable: Whether segment is writable
            executable: Whether segment is executable
        """
        pass  # TODO: Implement this

    def remove_segment(self, segment_id: SegmentId) -> None:
        """
        TODO: Remove a segment from the segment table.

        Args:
            segment_id: Segment to remove
        """
        pass  # TODO: Implement this

    def translate(self, segment: SegmentId, offset: int) -> Optional[int]:
        """
        TODO: Translate a logical address (segment, offset) to a physical address.

        Steps:
        1. Check if segment is valid
        2. Check if offset is within the segment limit
        3. Return base + offset

        Args:
            segment: Segment ID
            offset: Offset within segment

        Returns:
            Physical address, or None if invalid
        """
        pass  # TODO: Implement this

    def check_permission(self, segment: SegmentId, read: bool,
                        write: bool, execute: bool) -> bool:
        """
        TODO: Check if the requested operations are allowed on the segment.

        Args:
            segment: Segment ID
            read: Whether read access is requested
            write: Whether write access is requested
            execute: Whether execute access is requested

        Returns:
            True if all requested permissions are allowed, False otherwise
        """
        pass  # TODO: Implement this

    def get_segment_size(self, segment: SegmentId) -> Optional[int]:
        """
        TODO: Return the size (limit) of the segment.

        Args:
            segment: Segment ID

        Returns:
            Segment size, or None if not found
        """
        pass  # TODO: Implement this


class SegmentationSystem:
    """Complete segmentation system with segment table and memory management."""

    def __init__(self, memory_size: int):
        self.segment_table = SegmentTable()
        self.next_base = 0
        self.memory_size = memory_size

    def allocate_segment(self, segment_id: SegmentId, size: int,
                        readable: bool, writable: bool, executable: bool) -> bool:
        """
        TODO: Allocate a new segment.

        Steps:
        1. Check if there's enough free space
        2. Add segment to the table with the current next_base
        3. Update next_base

        Args:
            segment_id: Segment identifier
            size: Size of the segment
            readable: Whether segment is readable
            writable: Whether segment is writable
            executable: Whether segment is executable

        Returns:
            True if successful, False if not enough space
        """
        pass  # TODO: Implement this

    def free_segment(self, segment_id: SegmentId) -> bool:
        """
        TODO: Free a segment.

        Note: This simple implementation doesn't compact memory,
        so it won't reduce next_base.

        Args:
            segment_id: Segment to free

        Returns:
            True if successful, False if segment not found
        """
        pass  # TODO: Implement this

    def translate_address(self, segment: SegmentId, offset: int) -> Optional[int]:
        """Translate a logical address to physical address."""
        return self.segment_table.translate(segment, offset)

    def check_access(self, segment: SegmentId, offset: int,
                    read: bool, write: bool, execute: bool) -> Optional[int]:
        """
        TODO: Check permissions and translate address.

        Steps:
        1. Check if the operation is permitted on the segment
        2. Translate the address

        Args:
            segment: Segment ID
            offset: Offset within segment
            read: Whether read access is requested
            write: Whether write access is requested
            execute: Whether execute access is requested

        Returns:
            Physical address if valid, None otherwise
        """
        pass  # TODO: Implement this

    def free_space(self) -> int:
        """
        TODO: Calculate remaining free space.

        Returns:
            Amount of free memory
        """
        pass  # TODO: Implement this


class TestSegmentationSystem(unittest.TestCase):
    """Test cases for Segmentation System."""

    def test_segment_table(self):
        """Test basic segment table operations."""
        st = SegmentTable()

        st.add_segment(SegmentId(0), 1000, 500, True, True, False)
        st.add_segment(SegmentId(1), 2000, 1000, True, False, True)

        self.assertEqual(st.translate(SegmentId(0), 100), 1100)
        self.assertEqual(st.translate(SegmentId(1), 500), 2500)

    def test_segment_limit_violation(self):
        """Test offset exceeding segment limit."""
        st = SegmentTable()

        st.add_segment(SegmentId(0), 1000, 500, True, True, False)

        # Offset exceeds segment limit
        result = st.translate(SegmentId(0), 600)
        self.assertIsNone(result)

    def test_invalid_segment(self):
        """Test translating invalid segment."""
        st = SegmentTable()

        # Segment doesn't exist
        result = st.translate(SegmentId(0), 100)
        self.assertIsNone(result)

    def test_permissions(self):
        """Test permission checking."""
        st = SegmentTable()

        st.add_segment(SegmentId(0), 1000, 500, True, False, False)  # Read-only

        self.assertTrue(st.check_permission(SegmentId(0), True, False, False))
        self.assertFalse(st.check_permission(SegmentId(0), False, True, False))

    def test_allocate_segments(self):
        """Test segment allocation."""
        system = SegmentationSystem(10000)

        self.assertEqual(system.free_space(), 10000)

        result = system.allocate_segment(SegmentId(0), 1000, True, True, False)
        self.assertTrue(result)
        self.assertEqual(system.free_space(), 9000)

        result = system.allocate_segment(SegmentId(1), 2000, True, False, True)
        self.assertTrue(result)
        self.assertEqual(system.free_space(), 7000)

    def test_out_of_memory(self):
        """Test allocation when out of memory."""
        system = SegmentationSystem(1000)

        system.allocate_segment(SegmentId(0), 800, True, True, False)

        result = system.allocate_segment(SegmentId(1), 300, True, True, False)
        self.assertFalse(result)

    def test_free_segment(self):
        """Test freeing segments."""
        system = SegmentationSystem(10000)

        system.allocate_segment(SegmentId(0), 1000, True, True, False)
        system.allocate_segment(SegmentId(1), 2000, True, True, False)

        result = system.free_segment(SegmentId(0))
        self.assertTrue(result)

        # Segment should not be accessible after freeing
        self.assertIsNone(system.translate_address(SegmentId(0), 100))

    def test_access_control(self):
        """Test access control."""
        system = SegmentationSystem(10000)

        system.allocate_segment(SegmentId(0), 1000, True, False, False)

        # Read should succeed
        result = system.check_access(SegmentId(0), 100, True, False, False)
        self.assertIsNotNone(result)

        # Write should fail
        result = system.check_access(SegmentId(0), 100, False, True, False)
        self.assertIsNone(result)

    def test_multiple_segments(self):
        """Test multiple segments with different permissions."""
        system = SegmentationSystem(10000)

        # Code segment
        system.allocate_segment(SegmentId(0), 2000, True, False, True)

        # Data segment
        system.allocate_segment(SegmentId(1), 3000, True, True, False)

        # Stack segment
        system.allocate_segment(SegmentId(2), 1000, True, True, False)

        code_addr = system.translate_address(SegmentId(0), 500)
        data_addr = system.translate_address(SegmentId(1), 1000)
        stack_addr = system.translate_address(SegmentId(2), 100)

        # All segments should have different base addresses
        self.assertLess(code_addr, data_addr)
        self.assertLess(data_addr, stack_addr)

    def test_segment_size(self):
        """Test getting segment size."""
        st = SegmentTable()

        st.add_segment(SegmentId(0), 1000, 500, True, True, False)

        self.assertEqual(st.get_segment_size(SegmentId(0)), 500)
        self.assertIsNone(st.get_segment_size(SegmentId(1)))

    def test_zero_size_segment(self):
        """Test allocating zero-size segment."""
        system = SegmentationSystem(10000)

        result = system.allocate_segment(SegmentId(0), 0, True, False, False)
        self.assertTrue(result)
        self.assertEqual(system.free_space(), 10000)


if __name__ == '__main__':
    unittest.main()
