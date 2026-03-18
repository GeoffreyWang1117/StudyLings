# I AM NOT DONE

"""
os01_paging.py

Paging is a memory management scheme that eliminates the need for contiguous
allocation of physical memory. The physical address space is divided into fixed-size
blocks called frames, and the logical address space is divided into blocks of the
same size called pages.

Your task: Implement a simple paging system with a page table for address translation.
"""

from typing import Dict, Optional
import unittest


PAGE_SIZE = 4096  # 4KB pages


class PageNumber:
    """Represents a page number."""
    def __init__(self, number: int):
        self.number = number

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return isinstance(other, PageNumber) and self.number == other.number


class FrameNumber:
    """Represents a frame number."""
    def __init__(self, number: int):
        self.number = number

    def __eq__(self, other):
        return isinstance(other, FrameNumber) and self.number == other.number


class PageTableEntry:
    """Entry in the page table."""
    def __init__(self, frame: FrameNumber):
        self.frame = frame
        self.valid = True
        self.dirty = False
        self.referenced = False


class PageTable:
    """Page table for address translation."""

    def __init__(self):
        self.entries: Dict[PageNumber, PageTableEntry] = {}

    def map_page(self, page: PageNumber, frame: FrameNumber) -> None:
        """
        TODO: Create a new page table entry mapping the page to the frame.

        Set valid=True, dirty=False, referenced=False.

        Args:
            page: Page number to map
            frame: Frame number to map to
        """
        pass  # TODO: Implement this

    def unmap_page(self, page: PageNumber) -> None:
        """
        TODO: Remove the page table entry for the given page.

        Args:
            page: Page number to unmap
        """
        pass  # TODO: Implement this

    def translate(self, page: PageNumber) -> Optional[FrameNumber]:
        """
        TODO: Translate a page number to a frame number.

        Return None if the page is not mapped or not valid.

        Args:
            page: Page number to translate

        Returns:
            Frame number, or None if not mapped
        """
        pass  # TODO: Implement this

    def set_dirty(self, page: PageNumber) -> None:
        """
        TODO: Mark a page as dirty (modified).

        Args:
            page: Page number to mark dirty
        """
        pass  # TODO: Implement this

    def set_referenced(self, page: PageNumber) -> None:
        """
        TODO: Mark a page as referenced (accessed).

        Args:
            page: Page number to mark referenced
        """
        pass  # TODO: Implement this

    def is_dirty(self, page: PageNumber) -> bool:
        """
        TODO: Check if a page is dirty.

        Args:
            page: Page number to check

        Returns:
            True if dirty, False otherwise
        """
        pass  # TODO: Implement this

    def is_referenced(self, page: PageNumber) -> bool:
        """
        TODO: Check if a page is referenced.

        Args:
            page: Page number to check

        Returns:
            True if referenced, False otherwise
        """
        pass  # TODO: Implement this


class PagingSystem:
    """Complete paging system with page table and frame management."""

    def __init__(self, total_frames: int):
        """
        TODO: Initialize the paging system with the given number of frames.

        All frames should initially be free.

        Args:
            total_frames: Number of frames in physical memory
        """
        pass  # TODO: Implement this

    def allocate_page(self, page: PageNumber) -> Optional[FrameNumber]:
        """
        TODO: Allocate a free frame for the given page.

        Return None if no free frames are available.
        Update the page table to map the page to the allocated frame.

        Args:
            page: Page number to allocate

        Returns:
            Frame number allocated, or None if no frames available
        """
        pass  # TODO: Implement this

    def free_page(self, page: PageNumber) -> bool:
        """
        TODO: Free the frame associated with the given page.

        Add the frame back to the free list.
        Unmap the page from the page table.

        Args:
            page: Page number to free

        Returns:
            True if successful, False if page was not mapped
        """
        pass  # TODO: Implement this

    def translate_address(self, virtual_addr: int) -> Optional[int]:
        """
        TODO: Translate a virtual address to a physical address.

        Virtual address = page_number * PAGE_SIZE + offset
        Physical address = frame_number * PAGE_SIZE + offset

        Args:
            virtual_addr: Virtual address to translate

        Returns:
            Physical address, or None if page not mapped
        """
        pass  # TODO: Implement this

    def free_frames_count(self) -> int:
        """Get the number of free frames."""
        return len(self.free_frames)


class TestPagingSystem(unittest.TestCase):
    """Test cases for Paging System."""

    def test_page_table_mapping(self):
        """Test basic page table mapping."""
        pt = PageTable()

        pt.map_page(PageNumber(0), FrameNumber(5))
        pt.map_page(PageNumber(1), FrameNumber(10))

        self.assertEqual(pt.translate(PageNumber(0)), FrameNumber(5))
        self.assertEqual(pt.translate(PageNumber(1)), FrameNumber(10))
        self.assertIsNone(pt.translate(PageNumber(2)))

    def test_page_table_unmap(self):
        """Test unmapping pages."""
        pt = PageTable()

        pt.map_page(PageNumber(0), FrameNumber(5))
        self.assertEqual(pt.translate(PageNumber(0)), FrameNumber(5))

        pt.unmap_page(PageNumber(0))
        self.assertIsNone(pt.translate(PageNumber(0)))

    def test_dirty_and_referenced_bits(self):
        """Test dirty and referenced bit management."""
        pt = PageTable()

        pt.map_page(PageNumber(0), FrameNumber(5))
        self.assertFalse(pt.is_dirty(PageNumber(0)))
        self.assertFalse(pt.is_referenced(PageNumber(0)))

        pt.set_dirty(PageNumber(0))
        self.assertTrue(pt.is_dirty(PageNumber(0)))

        pt.set_referenced(PageNumber(0))
        self.assertTrue(pt.is_referenced(PageNumber(0)))

    def test_allocate_and_free_pages(self):
        """Test allocating and freeing pages."""
        system = PagingSystem(10)

        self.assertEqual(system.free_frames_count(), 10)

        frame1 = system.allocate_page(PageNumber(0))
        self.assertIsNotNone(frame1)
        self.assertEqual(system.free_frames_count(), 9)

        frame2 = system.allocate_page(PageNumber(1))
        self.assertIsNotNone(frame2)
        self.assertEqual(system.free_frames_count(), 8)

        system.free_page(PageNumber(0))
        self.assertEqual(system.free_frames_count(), 9)

    def test_address_translation(self):
        """Test virtual to physical address translation."""
        system = PagingSystem(10)

        system.allocate_page(PageNumber(0))
        system.allocate_page(PageNumber(1))

        # Test address translation
        virtual_addr = PAGE_SIZE + 100  # Page 1, offset 100
        physical_addr = system.translate_address(virtual_addr)

        self.assertIsNotNone(physical_addr)
        self.assertEqual(physical_addr % PAGE_SIZE, 100)  # Offset should be preserved

    def test_out_of_frames(self):
        """Test allocation when out of frames."""
        system = PagingSystem(2)

        system.allocate_page(PageNumber(0))
        system.allocate_page(PageNumber(1))

        result = system.allocate_page(PageNumber(2))
        self.assertIsNone(result)

    def test_multiple_allocations(self):
        """Test multiple allocations and frees."""
        system = PagingSystem(5)

        for i in range(5):
            result = system.allocate_page(PageNumber(i))
            self.assertIsNotNone(result)

        self.assertEqual(system.free_frames_count(), 0)

        system.free_page(PageNumber(2))
        self.assertEqual(system.free_frames_count(), 1)

        result = system.allocate_page(PageNumber(10))
        self.assertIsNotNone(result)
        self.assertEqual(system.free_frames_count(), 0)

    def test_translate_unmapped_page(self):
        """Test translating unmapped virtual address."""
        system = PagingSystem(10)

        virtual_addr = PAGE_SIZE * 5 + 100  # Page 5, not mapped
        physical_addr = system.translate_address(virtual_addr)

        self.assertIsNone(physical_addr)

    def test_free_unmapped_page(self):
        """Test freeing an unmapped page."""
        system = PagingSystem(10)

        result = system.free_page(PageNumber(5))
        self.assertFalse(result)

    def test_page_offset_preservation(self):
        """Test that page offset is preserved in translation."""
        system = PagingSystem(10)

        system.allocate_page(PageNumber(3))

        for offset in [0, 100, 2048, 4095]:
            virtual_addr = PAGE_SIZE * 3 + offset
            physical_addr = system.translate_address(virtual_addr)

            self.assertIsNotNone(physical_addr)
            self.assertEqual(physical_addr % PAGE_SIZE, offset)

    def test_different_pages_different_frames(self):
        """Test that different pages map to different frames."""
        system = PagingSystem(10)

        frame0 = system.allocate_page(PageNumber(0))
        frame1 = system.allocate_page(PageNumber(1))
        frame2 = system.allocate_page(PageNumber(2))

        self.assertNotEqual(frame0, frame1)
        self.assertNotEqual(frame1, frame2)
        self.assertNotEqual(frame0, frame2)


if __name__ == '__main__':
    unittest.main()
