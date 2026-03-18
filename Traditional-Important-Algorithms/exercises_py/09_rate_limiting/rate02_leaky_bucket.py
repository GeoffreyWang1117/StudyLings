# I AM NOT DONE

"""
Exercise: Leaky Bucket Rate Limiter

Leaky Bucket is a rate limiting algorithm that enforces a constant output rate
regardless of input bursts. It's similar to token bucket but processes requests
at a fixed rate.

How it works:
- Requests enter a queue (bucket)
- Requests are processed at a constant rate (leak rate)
- If bucket is full, new requests are rejected
- Smooths out bursts to maintain steady flow

Your task: Implement a leaky bucket rate limiter.

Key concepts:
- Queue-based request handling
- Fixed processing rate
- Bucket overflow protection
- Time-based request processing
"""

import time
from collections import deque
from typing import List, Optional


class Request:
    """Represents a request in the leaky bucket"""

    def __init__(self, request_id: int, timestamp: float):
        self.id = request_id
        self.timestamp = timestamp


class LeakyBucket:
    """Leaky bucket rate limiter"""

    def __init__(self, capacity: int, leak_rate: float):
        """
        Initialize a new leaky bucket

        Args:
            capacity: Maximum requests in bucket
            leak_rate: Requests processed per second
        """
        # TODO: Initialize a new leaky bucket
        # - Create empty queue
        # - Set last_leak to current time
        pass

    def _leak(self):
        """Process (remove) requests based on time elapsed"""
        # TODO: Process (remove) requests based on time elapsed
        # - Calculate elapsed time since last_leak
        # - Calculate requests to process: elapsed_seconds * leak_rate
        # - Remove that many requests from front of queue
        # - Update last_leak to current time
        # - Don't remove more requests than available
        pass

    def try_add(self, request: Request) -> bool:
        """
        Try to add a request to the bucket

        Args:
            request: Request to add

        Returns:
            True if request was added, False if bucket is full
        """
        # TODO: Try to add a request to the bucket
        # - First call _leak() to process pending requests
        # - Check if queue is at capacity
        # - If yes, return False (bucket full)
        # - If no, add request to back of queue and return True
        pass

    def current_size(self) -> int:
        """Return current number of requests in bucket"""
        # TODO: Return current number of requests in bucket
        # - Call _leak() first to update queue
        # - Return queue length
        pass

    def is_full(self) -> bool:
        """Check if bucket is at capacity"""
        # TODO: Check if bucket is at capacity
        # - Call _leak() first to update queue
        # - Return True if queue length >= capacity
        pass

    def pending_requests(self) -> List[Request]:
        """Return a copy of all pending requests"""
        # TODO: Return a copy of all pending requests
        # - Call _leak() first
        # - Return list of requests from queue
        pass

    def time_until_space(self) -> Optional[float]:
        """
        Calculate time until there's space for a new request

        Returns:
            Time in seconds, or None if space is available
        """
        # TODO: Calculate time until there's space for a new request
        # - Call _leak() first
        # - If not full, return None
        # - Calculate time to leak one request: 1.0 / leak_rate seconds
        # - Return time in seconds
        pass


import unittest


class TestLeakyBucket(unittest.TestCase):
    def test_leaky_bucket_creation(self):
        bucket = LeakyBucket(10, 5.0)
        self.assertEqual(bucket.current_size(), 0)
        self.assertFalse(bucket.is_full())

    def test_add_requests(self):
        bucket = LeakyBucket(5, 2.0)
        req1 = Request(1, time.time())
        req2 = Request(2, time.time())

        self.assertTrue(bucket.try_add(req1))
        self.assertTrue(bucket.try_add(req2))
        self.assertEqual(bucket.current_size(), 2)

    def test_bucket_full(self):
        bucket = LeakyBucket(3, 1.0)

        for i in range(3):
            req = Request(i, time.time())
            self.assertTrue(bucket.try_add(req))

        self.assertTrue(bucket.is_full())

        req = Request(99, time.time())
        self.assertFalse(bucket.try_add(req))  # Should be rejected

    def test_leak_over_time(self):
        bucket = LeakyBucket(10, 10.0)  # 10 requests per second

        # Add 10 requests
        for i in range(10):
            req = Request(i, time.time())
            bucket.try_add(req)

        self.assertEqual(bucket.current_size(), 10)

        time.sleep(0.5)  # Wait 0.5 seconds

        # Should have leaked approximately 5 requests (10/sec * 0.5 sec)
        size = bucket.current_size()
        self.assertGreaterEqual(size, 4)
        self.assertLessEqual(size, 6)

    def test_leak_all_requests(self):
        bucket = LeakyBucket(5, 5.0)  # 5 requests per second

        for i in range(5):
            req = Request(i, time.time())
            bucket.try_add(req)

        time.sleep(2.0)  # Wait 2 seconds (more than needed)

        self.assertEqual(bucket.current_size(), 0)  # All leaked

    def test_add_after_leak(self):
        bucket = LeakyBucket(3, 10.0)

        # Fill bucket
        for i in range(3):
            req = Request(i, time.time())
            bucket.try_add(req)

        self.assertTrue(bucket.is_full())

        time.sleep(0.2)  # Leak approximately 2 requests

        # Should have space now
        req = Request(99, time.time())
        self.assertTrue(bucket.try_add(req))

    def test_pending_requests(self):
        bucket = LeakyBucket(5, 1.0)

        for i in range(3):
            req = Request(i, time.time())
            bucket.try_add(req)

        pending = bucket.pending_requests()
        self.assertEqual(len(pending), 3)
        self.assertEqual(pending[0].id, 0)
        self.assertEqual(pending[1].id, 1)
        self.assertEqual(pending[2].id, 2)

    def test_time_until_space(self):
        bucket = LeakyBucket(2, 5.0)  # 5 requests per second

        # Fill bucket
        for i in range(2):
            req = Request(i, time.time())
            bucket.try_add(req)

        wait_time = bucket.time_until_space()
        self.assertIsNotNone(wait_time)

        # Should wait approximately 0.2 seconds (1 / 5 requests per second)
        self.assertGreaterEqual(wait_time, 0.15)
        self.assertLessEqual(wait_time, 0.25)

    def test_time_until_space_when_not_full(self):
        bucket = LeakyBucket(5, 2.0)

        req = Request(1, time.time())
        bucket.try_add(req)

        wait_time = bucket.time_until_space()
        self.assertIsNone(wait_time)  # Not full, no wait needed

    def test_constant_leak_rate(self):
        bucket = LeakyBucket(20, 4.0)  # 4 requests per second

        # Fill bucket
        for i in range(20):
            req = Request(i, time.time())
            bucket.try_add(req)

        time.sleep(0.5)  # 0.5 seconds

        size1 = bucket.current_size()
        # Should have leaked ~2 requests

        time.sleep(0.5)  # Another 0.5 seconds

        size2 = bucket.current_size()
        # Should have leaked ~2 more requests

        leaked1 = 20 - size1
        leaked2 = size1 - size2

        # Both should be approximately 2 (allowing for timing variance)
        self.assertGreaterEqual(leaked1, 1)
        self.assertLessEqual(leaked1, 3)
        self.assertGreaterEqual(leaked2, 1)
        self.assertLessEqual(leaked2, 3)

    def test_rapid_add_attempts(self):
        bucket = LeakyBucket(3, 1.0)

        accepted = 0
        rejected = 0

        for i in range(10):
            req = Request(i, time.time())
            if bucket.try_add(req):
                accepted += 1
            else:
                rejected += 1

        self.assertEqual(accepted, 3)  # Only capacity worth accepted
        self.assertEqual(rejected, 7)  # Rest rejected

    def test_empty_bucket_operations(self):
        bucket = LeakyBucket(5, 2.0)

        self.assertEqual(bucket.current_size(), 0)
        self.assertFalse(bucket.is_full())
        self.assertEqual(len(bucket.pending_requests()), 0)
        self.assertIsNone(bucket.time_until_space())


if __name__ == '__main__':
    unittest.main()
