# I AM NOT DONE

"""
os04_fifo_replacement.py

FIFO (First-In-First-Out) is the simplest page replacement algorithm. When a page
needs to be replaced, the oldest page (the one that has been in memory the longest)
is chosen for replacement.

Your task: Implement a FIFO page replacement algorithm to simulate page faults.
"""

from collections import deque
from typing import Dict, List, Tuple, Optional
import unittest


class PageId:
    """Represents a page identifier."""
    def __init__(self, page_id: int):
        self.id = page_id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, PageId) and self.id == other.id


class FrameId:
    """Represents a frame identifier."""
    def __init__(self, frame_id: int):
        self.id = frame_id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, FrameId) and self.id == other.id


class FIFOPageReplacement:
    """FIFO page replacement algorithm."""

    def __init__(self, num_frames: int):
        """
        TODO: Initialize the FIFO page replacement system.

        Create the specified number of frames.

        Args:
            num_frames: Number of frames in memory
        """
        pass  # TODO: Implement this

    def access_page(self, page: PageId) -> bool:
        """
        TODO: Access a page, returns True if page fault occurred.

        Steps:
        1. Check if page is already in memory (page hit)
        2. If not, a page fault occurs:
           a. If there are free frames, use one
           b. Otherwise, evict the oldest page (front of FIFO queue)
        3. Update statistics

        Args:
            page: Page to access

        Returns:
            True if page fault occurred, False otherwise
        """
        pass  # TODO: Implement this

    def _find_free_frame(self) -> Optional[FrameId]:
        """
        TODO: Find a free frame (one that doesn't contain a page).

        Returns:
            Free frame ID, or None if all frames are occupied
        """
        pass  # TODO: Implement this

    def _evict_page(self) -> Optional[PageId]:
        """
        TODO: Evict the oldest page using FIFO policy.

        Steps:
        1. Remove the front frame from the FIFO queue
        2. Get the page in that frame
        3. Remove the page-to-frame mapping
        4. Return the evicted page

        Returns:
            The evicted page ID, or None if queue is empty
        """
        pass  # TODO: Implement this

    def page_faults(self) -> int:
        """Get the number of page faults."""
        return self.fault_count

    def page_hits(self) -> int:
        """Get the number of page hits."""
        return self.hit_count

    def hit_rate(self) -> float:
        """Calculate the hit rate."""
        total = self.fault_count + self.hit_count
        return self.hit_count / total if total > 0 else 0.0

    def is_page_in_memory(self, page: PageId) -> bool:
        """Check if a page is in memory."""
        return page in self.page_to_frame

    def reset_stats(self) -> None:
        """Reset statistics."""
        self.fault_count = 0
        self.hit_count = 0


def simulate_page_references(num_frames: int, references: List[int]) -> Tuple[int, int, float]:
    """
    TODO: Simulate a sequence of page references.

    Args:
        num_frames: Number of frames available
        references: List of page IDs to reference

    Returns:
        Tuple of (page_faults, page_hits, hit_rate)
    """
    pass  # TODO: Implement this


class TestFIFOPageReplacement(unittest.TestCase):
    """Test cases for FIFO Page Replacement."""

    def test_all_page_faults(self):
        """Test all unique pages cause page faults."""
        fifo = FIFOPageReplacement(3)

        # All unique pages, all should be page faults
        self.assertTrue(fifo.access_page(PageId(1)))
        self.assertTrue(fifo.access_page(PageId(2)))
        self.assertTrue(fifo.access_page(PageId(3)))

        self.assertEqual(fifo.page_faults(), 3)
        self.assertEqual(fifo.page_hits(), 0)

    def test_page_hits(self):
        """Test page hits."""
        fifo = FIFOPageReplacement(3)

        fifo.access_page(PageId(1))
        fifo.access_page(PageId(2))
        fifo.access_page(PageId(3))

        # Access existing pages - should be hits
        self.assertFalse(fifo.access_page(PageId(1)))
        self.assertFalse(fifo.access_page(PageId(2)))

        self.assertEqual(fifo.page_faults(), 3)
        self.assertEqual(fifo.page_hits(), 2)

    def test_fifo_replacement(self):
        """Test FIFO replacement order."""
        fifo = FIFOPageReplacement(3)

        fifo.access_page(PageId(1))
        fifo.access_page(PageId(2))
        fifo.access_page(PageId(3))

        # This should evict page 1 (oldest)
        fifo.access_page(PageId(4))

        self.assertFalse(fifo.is_page_in_memory(PageId(1)))
        self.assertTrue(fifo.is_page_in_memory(PageId(2)))
        self.assertTrue(fifo.is_page_in_memory(PageId(3)))
        self.assertTrue(fifo.is_page_in_memory(PageId(4)))

    def test_belady_anomaly(self):
        """Test Belady's anomaly scenario."""
        # With 3 frames
        faults_3, _, _ = simulate_page_references(3, [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])

        # With 4 frames
        faults_4, _, _ = simulate_page_references(4, [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5])

        # Both should complete successfully
        self.assertGreater(faults_3, 0)
        self.assertGreater(faults_4, 0)

    def test_sequential_pattern(self):
        """Test sequential access pattern."""
        fifo = FIFOPageReplacement(3)

        # Sequential access pattern
        for i in range(10):
            fifo.access_page(PageId(i))

        # Should have many page faults due to sequential access
        self.assertGreater(fifo.page_faults(), 7)

    def test_cyclic_pattern(self):
        """Test cyclic pattern that fits in frames."""
        fifo = FIFOPageReplacement(3)

        # Cyclic pattern that fits in frames
        for _ in range(10):
            fifo.access_page(PageId(1))
            fifo.access_page(PageId(2))
            fifo.access_page(PageId(3))

        # After first 3 accesses, all should be hits
        self.assertEqual(fifo.page_faults(), 3)
        self.assertEqual(fifo.page_hits(), 27)  # 3 * 10 - 3

    def test_worst_case_pattern(self):
        """Test worst case pattern."""
        fifo = FIFOPageReplacement(3)

        # Worst case: cyclic pattern with 4 pages (frames + 1)
        for _ in range(5):
            fifo.access_page(PageId(1))
            fifo.access_page(PageId(2))
            fifo.access_page(PageId(3))
            fifo.access_page(PageId(4))

        # Every 4th access causes a page fault
        self.assertEqual(fifo.page_faults(), 20)  # All accesses are faults

    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        fifo = FIFOPageReplacement(2)

        fifo.access_page(PageId(1))  # Fault
        fifo.access_page(PageId(2))  # Fault
        fifo.access_page(PageId(1))  # Hit
        fifo.access_page(PageId(2))  # Hit

        self.assertAlmostEqual(fifo.hit_rate(), 0.5, places=2)

    def test_reset_stats(self):
        """Test resetting statistics."""
        fifo = FIFOPageReplacement(3)

        fifo.access_page(PageId(1))
        fifo.access_page(PageId(2))

        self.assertEqual(fifo.page_faults(), 2)

        fifo.reset_stats()

        self.assertEqual(fifo.page_faults(), 0)
        self.assertEqual(fifo.page_hits(), 0)

    def test_single_frame(self):
        """Test with single frame."""
        fifo = FIFOPageReplacement(1)

        fifo.access_page(PageId(1))
        fifo.access_page(PageId(2))
        fifo.access_page(PageId(3))

        # With only 1 frame, every new page is a fault
        self.assertEqual(fifo.page_faults(), 3)
        self.assertTrue(fifo.is_page_in_memory(PageId(3)))
        self.assertFalse(fifo.is_page_in_memory(PageId(1)))
        self.assertFalse(fifo.is_page_in_memory(PageId(2)))

    def test_zero_hit_rate(self):
        """Test hit rate with no hits."""
        fifo = FIFOPageReplacement(3)

        fifo.access_page(PageId(1))
        fifo.access_page(PageId(2))

        # Only faults, no hits
        self.assertEqual(fifo.hit_rate(), 0.0)


if __name__ == '__main__':
    unittest.main()
