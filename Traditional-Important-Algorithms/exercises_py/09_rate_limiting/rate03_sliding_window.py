# I AM NOT DONE

"""
Exercise: Sliding Window Rate Limiter

Sliding Window Rate Limiter provides precise rate limiting by tracking
requests in a rolling time window. More accurate than fixed windows.

How it works:
- Maintains timestamps of all requests in current window
- Window slides with each new request
- Removes requests older than window duration
- Rejects requests if count exceeds limit

Your task: Implement a sliding window rate limiter.

Key concepts:
- Rolling time window
- Request timestamp tracking
- Automatic cleanup of old requests
- Precise rate limiting
"""

import time
from collections import deque
from typing import Optional


class SlidingWindowRateLimiter:
    """Sliding window rate limiter"""

    def __init__(self, max_requests: int, window_duration: float):
        """
        Initialize a new sliding window rate limiter

        Args:
            max_requests: Maximum requests per window
            window_duration: Time window duration in seconds
        """
        # TODO: Initialize a new sliding window rate limiter
        # - Create empty request queue
        pass

    def _cleanup_old_requests(self, now: float):
        """Remove requests outside the current window"""
        # TODO: Remove requests outside the current window
        # - Calculate window start: now - window_duration
        # - Remove all requests from front of queue older than window start
        # - Use a loop with popleft() while condition is true
        pass

    def try_acquire(self) -> bool:
        """
        Try to acquire a slot for a new request

        Returns:
            True if request was allowed, False otherwise
        """
        # TODO: Try to acquire a slot for a new request
        # - Get current time
        # - Cleanup old requests
        # - Check if current count < max_requests
        # - If yes, add current time to queue and return True
        # - If no, return False
        pass

    def current_count(self) -> int:
        """Return current number of requests in window"""
        # TODO: Return current number of requests in window
        # - Cleanup old requests first
        # - Return queue length
        pass

    def remaining_capacity(self) -> int:
        """Return number of available request slots"""
        # TODO: Return number of available request slots
        # - Return max_requests - current_count()
        pass

    def time_until_next_slot(self) -> Optional[float]:
        """
        Calculate time until a slot becomes available

        Returns:
            Time in seconds, or None if capacity available
        """
        # TODO: Calculate time until a slot becomes available
        # - Cleanup old requests first
        # - If capacity available, return None
        # - Otherwise, calculate when oldest request will expire
        # - Return time until that expiration
        pass

    def reset(self):
        """Clear all requests from the window"""
        # TODO: Clear all requests from the window
        pass


import unittest


class TestSlidingWindowRateLimiter(unittest.TestCase):
    def test_sliding_window_creation(self):
        limiter = SlidingWindowRateLimiter(10, 1.0)
        self.assertEqual(limiter.current_count(), 0)
        self.assertEqual(limiter.remaining_capacity(), 10)

    def test_acquire_requests(self):
        limiter = SlidingWindowRateLimiter(5, 1.0)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())

        self.assertEqual(limiter.current_count(), 3)
        self.assertEqual(limiter.remaining_capacity(), 2)

    def test_max_requests_limit(self):
        limiter = SlidingWindowRateLimiter(3, 1.0)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())  # Should be rejected

        self.assertEqual(limiter.current_count(), 3)
        self.assertEqual(limiter.remaining_capacity(), 0)

    def test_window_sliding(self):
        limiter = SlidingWindowRateLimiter(2, 0.5)

        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())  # Full

        time.sleep(0.6)  # Wait for window to pass

        # Window has slid, old requests should be gone
        self.assertEqual(limiter.current_count(), 0)
        self.assertTrue(limiter.try_acquire())
        self.assertTrue(limiter.try_acquire())

    def test_partial_window_cleanup(self):
        limiter = SlidingWindowRateLimiter(5, 1.0)

        # Add 3 requests
        limiter.try_acquire()
        time.sleep(0.1)
        limiter.try_acquire()
        time.sleep(0.1)
        limiter.try_acquire()

        time.sleep(0.9)  # First request should expire

        # Should have approximately 2 requests left
        count = limiter.current_count()
        self.assertGreaterEqual(count, 1)
        self.assertLessEqual(count, 2)

    def test_time_until_next_slot(self):
        limiter = SlidingWindowRateLimiter(2, 1.0)

        limiter.try_acquire()
        time.sleep(0.1)
        limiter.try_acquire()

        # Limiter is full
        wait_time = limiter.time_until_next_slot()
        self.assertIsNotNone(wait_time)

        # Should wait approximately 0.9s (until first request expires)
        self.assertGreaterEqual(wait_time, 0.8)
        self.assertLessEqual(wait_time, 1.0)

    def test_time_until_next_slot_when_available(self):
        limiter = SlidingWindowRateLimiter(5, 1.0)

        limiter.try_acquire()
        limiter.try_acquire()

        wait_time = limiter.time_until_next_slot()
        self.assertIsNone(wait_time)  # Capacity still available

    def test_reset(self):
        limiter = SlidingWindowRateLimiter(3, 10.0)

        limiter.try_acquire()
        limiter.try_acquire()
        limiter.try_acquire()

        self.assertEqual(limiter.current_count(), 3)

        limiter.reset()

        self.assertEqual(limiter.current_count(), 0)
        self.assertTrue(limiter.try_acquire())  # Can acquire again

    def test_burst_handling(self):
        limiter = SlidingWindowRateLimiter(10, 0.5)

        # Try to acquire 15 requests rapidly
        accepted = 0
        rejected = 0

        for _ in range(15):
            if limiter.try_acquire():
                accepted += 1
            else:
                rejected += 1

        self.assertEqual(accepted, 10)
        self.assertEqual(rejected, 5)

    def test_sustained_rate(self):
        limiter = SlidingWindowRateLimiter(5, 0.5)

        # First batch
        for _ in range(5):
            limiter.try_acquire()
        self.assertFalse(limiter.try_acquire())

        time.sleep(0.6)

        # Second batch after window slides
        for _ in range(5):
            self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())

    def test_gradual_window_sliding(self):
        limiter = SlidingWindowRateLimiter(3, 0.3)

        limiter.try_acquire()
        time.sleep(0.1)
        limiter.try_acquire()
        time.sleep(0.1)
        limiter.try_acquire()

        self.assertFalse(limiter.try_acquire())  # Full

        time.sleep(0.12)  # First request should expire

        self.assertTrue(limiter.try_acquire())  # Should succeed now

    def test_empty_limiter(self):
        limiter = SlidingWindowRateLimiter(5, 1.0)

        self.assertEqual(limiter.current_count(), 0)
        self.assertEqual(limiter.remaining_capacity(), 5)
        self.assertIsNone(limiter.time_until_next_slot())

    def test_precise_rate_limiting(self):
        limiter = SlidingWindowRateLimiter(10, 1.0)

        # Fill limiter
        for _ in range(10):
            self.assertTrue(limiter.try_acquire())

        # Wait exactly half window
        time.sleep(0.5)

        # Should still be full (all requests still in window)
        self.assertFalse(limiter.try_acquire())

        # Wait for window to fully pass
        time.sleep(0.6)

        # Now should be able to acquire
        self.assertTrue(limiter.try_acquire())


if __name__ == '__main__':
    unittest.main()
