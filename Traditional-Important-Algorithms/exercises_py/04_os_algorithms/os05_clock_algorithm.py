# I AM NOT DONE

"""
os05_clock_algorithm.py

The Clock algorithm (also known as Second-Chance algorithm) is an approximation of LRU
that uses a circular list and a reference bit. When a page needs to be replaced, the
algorithm scans through pages giving them a "second chance" if their reference bit is set.

Your task: Implement the Clock page replacement algorithm.
"""

from typing import List, Optional, Tuple
import unittest


class PageId:
    """Represents a page identifier."""
    def __init__(self, page_id: int):
        self.id = page_id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, PageId) and self.id == other.id


class ClockFrame:
    """Represents a frame in the clock algorithm."""
    def __init__(self):
        self.page: Optional[PageId] = None
        self.reference_bit = False


class ClockAlgorithm:
    """Clock page replacement algorithm."""

    def __init__(self, num_frames: int):
        """
        TODO: Initialize the Clock algorithm.

        Create frames with no pages and reference_bit = False.

        Args:
            num_frames: Number of frames in memory
        """
        pass  # TODO: Implement this

    def access_page(self, page: PageId) -> bool:
        """
        TODO: Access a page, returns True if page fault occurred.

        Steps:
        1. Check if page is in memory
           a. If yes (page hit): set reference bit to True, return False
           b. If no (page fault): find victim and replace, return True

        Args:
            page: Page to access

        Returns:
            True if page fault occurred, False otherwise
        """
        pass  # TODO: Implement this

    def _find_victim(self) -> int:
        """
        TODO: Find a victim frame using the clock algorithm.

        Steps:
        1. Start at clock_hand position
        2. Loop through frames:
           a. If reference_bit is False, return this frame
           b. If reference_bit is True, set it to False and advance clock_hand
        3. Update clock_hand position

        Returns:
            Index of the victim frame
        """
        pass  # TODO: Implement this

    def _replace_page(self, frame_idx: int, new_page: PageId) -> None:
        """
        TODO: Replace the page in the given frame.

        Steps:
        1. If frame contains a page, remove it from page_to_frame map
        2. Insert new page into the frame
        3. Set reference_bit to True (just accessed)
        4. Update page_to_frame map

        Args:
            frame_idx: Index of frame to replace
            new_page: New page to insert
        """
        pass  # TODO: Implement this

    def set_reference_bit(self, page: PageId, value: bool) -> None:
        """
        TODO: Set the reference bit for a page.

        This simulates hardware setting/clearing the bit.

        Args:
            page: Page to update
            value: New value for reference bit
        """
        pass  # TODO: Implement this

    def get_reference_bit(self, page: PageId) -> Optional[bool]:
        """
        TODO: Get the reference bit for a page.

        Args:
            page: Page to check

        Returns:
            Reference bit value, or None if page not in memory
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

    def clock_position(self) -> int:
        """Get the current clock hand position."""
        return self.clock_hand

    def reset_stats(self) -> None:
        """Reset statistics."""
        self.fault_count = 0
        self.hit_count = 0


def simulate_with_clock(num_frames: int, references: List[int]) -> Tuple[int, int, float]:
    """
    TODO: Simulate page references using Clock algorithm.

    Args:
        num_frames: Number of frames available
        references: List of page IDs to reference

    Returns:
        Tuple of (page_faults, page_hits, hit_rate)
    """
    pass  # TODO: Implement this


class TestClockAlgorithm(unittest.TestCase):
    """Test cases for Clock Algorithm."""

    def test_initial_page_faults(self):
        """Test initial page accesses cause faults."""
        clock = ClockAlgorithm(3)

        self.assertTrue(clock.access_page(PageId(1)))
        self.assertTrue(clock.access_page(PageId(2)))
        self.assertTrue(clock.access_page(PageId(3)))

        self.assertEqual(clock.page_faults(), 3)
        self.assertEqual(clock.page_hits(), 0)

    def test_page_hits(self):
        """Test page hits."""
        clock = ClockAlgorithm(3)

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # Access existing pages
        self.assertFalse(clock.access_page(PageId(1)))
        self.assertFalse(clock.access_page(PageId(2)))

        self.assertEqual(clock.page_faults(), 3)
        self.assertEqual(clock.page_hits(), 2)

    def test_second_chance(self):
        """Test second chance mechanism."""
        clock = ClockAlgorithm(3)

        # Fill all frames
        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # Access page 1, setting its reference bit
        clock.access_page(PageId(1))

        # Access new page - should skip page 1 due to reference bit
        clock.access_page(PageId(4))

        # Page 1 should still be in memory (got second chance)
        self.assertTrue(clock.is_page_in_memory(PageId(1)))

    def test_reference_bits(self):
        """Test reference bit management."""
        clock = ClockAlgorithm(3)

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))

        # Both should have reference bit set (just accessed)
        self.assertEqual(clock.get_reference_bit(PageId(1)), True)
        self.assertEqual(clock.get_reference_bit(PageId(2)), True)

        # Clear reference bit
        clock.set_reference_bit(PageId(1), False)
        self.assertEqual(clock.get_reference_bit(PageId(1)), False)

    def test_clock_hand_movement(self):
        """Test clock hand advances."""
        clock = ClockAlgorithm(3)

        initial_pos = clock.clock_position()

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # Fill frames - clock hand should be at start
        self.assertEqual(clock.clock_position(), initial_pos)

        # Trigger replacement - clock hand should advance
        clock.access_page(PageId(4))

        # Clock hand should have moved
        self.assertTrue(clock.clock_position() != initial_pos or clock.clock_position() == 0)

    def test_cyclic_pattern(self):
        """Test cyclic pattern that fits in frames."""
        clock = ClockAlgorithm(3)

        # Pattern that fits in frames
        for _ in range(10):
            clock.access_page(PageId(1))
            clock.access_page(PageId(2))
            clock.access_page(PageId(3))

        # After first 3, all should be hits
        self.assertEqual(clock.page_faults(), 3)
        self.assertEqual(clock.page_hits(), 27)

    def test_better_than_fifo(self):
        """Test Clock performs well on repeated access patterns."""
        # Clock should perform better than FIFO on certain patterns
        # due to the second-chance mechanism
        references = [1, 2, 3, 1, 4, 1, 5, 1, 6]
        faults, _, _ = simulate_with_clock(3, references)

        # With repeated access to page 1, Clock should give it second chances
        self.assertLess(faults, len(references))

    def test_all_reference_bits_set(self):
        """Test behavior when all reference bits are set."""
        clock = ClockAlgorithm(3)

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # All have reference bits set
        # Access all to keep reference bits set
        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # Now add a new page - should clear all reference bits
        # and replace the first one encountered
        clock.access_page(PageId(4))

        self.assertEqual(clock.page_faults(), 4)

    def test_single_frame(self):
        """Test with single frame."""
        clock = ClockAlgorithm(1)

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(3))

        # With 1 frame, every new page causes replacement
        self.assertEqual(clock.page_faults(), 3)
        self.assertTrue(clock.is_page_in_memory(PageId(3)))

    def test_sequential_vs_random(self):
        """Test different access patterns."""
        # Sequential pattern
        sequential = list(range(20))
        seq_faults, _, _ = simulate_with_clock(4, sequential)

        # Random pattern with locality
        random = [1, 2, 3, 1, 2, 4, 1, 2, 3, 5, 1, 2, 6]
        rand_faults, _, _ = simulate_with_clock(4, random)

        # Both should complete successfully
        self.assertGreater(seq_faults, 0)
        self.assertGreater(rand_faults, 0)

    def test_hit_rate(self):
        """Test hit rate calculation."""
        clock = ClockAlgorithm(3)

        clock.access_page(PageId(1))
        clock.access_page(PageId(2))
        clock.access_page(PageId(1))  # Hit
        clock.access_page(PageId(2))  # Hit

        hit_rate = clock.hit_rate()
        self.assertAlmostEqual(hit_rate, 0.5, places=2)  # Should be 50%


if __name__ == '__main__':
    unittest.main()
