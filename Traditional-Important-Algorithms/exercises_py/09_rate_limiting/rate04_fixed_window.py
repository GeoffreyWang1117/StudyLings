# I AM NOT DONE

"""
Exercise: Fixed Window Counter Rate Limiter

Fixed Window Counter is a simple rate limiting algorithm that divides time
into fixed windows and counts requests per window.

How it works:
- Time is divided into fixed-size windows (e.g., every minute starts at :00)
- Each window has a counter starting at 0
- When request arrives, check if in current window and increment counter
- If counter exceeds limit, reject request
- Counter resets at window boundary

Your task: Implement a fixed window counter rate limiter.

Key concepts:
- Window boundary calculation
- Counter reset on window change
- Simple but allows burst at window edges
- Trade-off: simplicity vs accuracy
"""

import time
from typing import Optional


class FixedWindowCounter:
    """Fixed window counter rate limiter"""

    def __init__(self, max_requests: int, window_duration: float):
        """
        Initialize a new fixed window counter

        Args:
            max_requests: Maximum requests per window
            window_duration: Duration of each window in seconds
        """
        # TODO: Initialize a new fixed window counter
        # - Set window_start to current time
        # - Set current_count to 0
        pass

    def _check_and_reset_window(self, now: float):
        """Check if we've moved to a new window and reset if needed"""
        # TODO: Check if we've moved to a new window and reset if needed
        # - Calculate time elapsed since window_start
        # - If elapsed >= window_duration:
        #   - Calculate how many complete windows have passed
        #   - Update window_start to start of current window
        #   - Reset current_count to 0
        pass

    def try_acquire(self) -> bool:
        """
        Try to acquire a request slot

        Returns:
            True if request was allowed, False otherwise
        """
        # TODO: Try to acquire a request slot
        # - Get current time
        # - Check and reset window if needed
        # - If current_count < max_requests:
        #   - Increment current_count
        #   - Return True
        # - Otherwise return False
        pass

    def current_count(self) -> int:
        """Return current request count in window"""
        # TODO: Return current request count in window
        # - Check and reset window first
        # - Return current_count
        pass

    def remaining_capacity(self) -> int:
        """Return remaining request slots in current window"""
        # TODO: Return remaining request slots in current window
        # - Return max_requests - current_count()
        pass

    def time_until_reset(self) -> float:
        """Return time until current window resets (in seconds)"""
        # TODO: Return time until current window resets
        # - Get current time
        # - Calculate window_end = window_start + window_duration
        # - Return window_end - now
        # - If result is negative or zero, return 0.0
        pass

    def reset(self):
        """Manually reset the counter to start a new window"""
        # TODO: Manually reset the counter to start a new window
        # - Set window_start to current time
        # - Set current_count to 0
        pass

    def window_start_time(self) -> float:
        """Return the start time of current window"""
        # TODO: Return the start time of current window
        pass


import unittest


class TestFixedWindowCounter(unittest.TestCase):
    def test_fixed_window_creation(self):
        limiter = FixedWindowCounter(10, 1.0)
        self.assertEqual(limiter.current_count(), 0)
        self.assertEqual(limiter.remaining_capacity(), 10)

    def test_acquire_requests(self):
        limiter = FixedWindowCounter(5, 1.0)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())

        self.assertEqual(limiter.current_count(), 3)
        self.assertEqual(limiter.remaining_capacity(), 2)

    def test_max_requests_limit(self):
        limiter = FixedWindowCounter(3, 1.0)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())  # Should be rejected

        self.assertEqual(limiter.current_count(), 3)
        self.assertEqual(limiter.remaining_capacity(), 0)

    def test_window_reset(self):
        limiter = FixedWindowCounter(2, 0.5)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())  # Full

        time.sleep(0.6)  # Wait for window to reset

        # New window, should be able to acquire again
        self.assertEqual(limiter.current_count(), 0)
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())

    def test_time_until_reset(self):
        limiter = FixedWindowCounter(5, 1.0)

        time_until = limiter.time_until_reset()

        # Should be approximately 1 second (just created)
        self.assertGreaterEqual(time_until, 0.9)
        self.assertLessEqual(time_until, 1.1)

    def test_time_until_reset_decreases(self):
        limiter = FixedWindowCounter(5, 1.0)

        time.sleep(0.3)

        time_until = limiter.time_until_reset()

        # Should be approximately 0.7s remaining
        self.assertGreaterEqual(time_until, 0.6)
        self.assertLessEqual(time_until, 0.8)

    def test_manual_reset(self):
        limiter = FixedWindowCounter(3, 10.0)

        limiter.try_acquire()
        limiter.try_acquire()
        limiter.try_acquire()

        self.assertEqual(limiter.current_count(), 3)

        limiter.reset()

        self.assertEqual(limiter.current_count(), 0)
        self.assertTrue(limiter.try_acquire())  # Can acquire again

    def test_burst_at_window_edge(self):
        limiter = FixedWindowCounter(5, 0.2)

        # Fill current window
        for _ in range(5):
            self.assertTrue(limiter.try_acquire())

        time.sleep(0.25)  # New window

        # Can burst again
        for _ in range(5):
            self.assertTrue(limiter.try_acquire())

        self.assertEqual(limiter.current_count(), 5)

    def test_multiple_window_transitions(self):
        limiter = FixedWindowCounter(2, 0.3)

        # Window 1
        limiter.try_acquire()
        limiter.try_acquire()

        time.sleep(0.35)  # Window 2

        self.assertEqual(limiter.current_count(), 0)
        limiter.try_acquire()

        time.sleep(0.35)  # Window 3

        self.assertEqual(limiter.current_count(), 0)
        limiter.try_acquire()
        limiter.try_acquire()

    def test_partial_window_usage(self):
        limiter = FixedWindowCounter(10, 1.0)

        limiter.try_acquire()
        limiter.try_acquire()
        limiter.try_acquire()

        time.sleep(0.5)  # Still in same window

        self.assertEqual(limiter.current_count(), 3)  # Count preserved
        self.assertTrue(limiter.try_acquire())

    def test_rapid_requests_in_window(self):
        limiter = FixedWindowCounter(100, 1.0)

        accepted = 0
        for _ in range(150):
            if limiter.try_acquire():
                accepted += 1

        self.assertEqual(accepted, 100)
        self.assertEqual(limiter.current_count(), 100)

    def test_window_start_time(self):
        limiter = FixedWindowCounter(5, 1.0)
        start = limiter.window_start_time()
        now = time.time()

        # Window start should be very close to now
        diff = now - start
        self.assertLess(diff, 0.1)

    def test_zero_count_after_reset(self):
        limiter = FixedWindowCounter(3, 0.1)

        limiter.try_acquire()
        time.sleep(0.15)

        # After window reset, checking count should show 0
        self.assertEqual(limiter.current_count(), 0)


if __name__ == '__main__':
    unittest.main()
