# I AM NOT DONE

"""
Exercise: Token Bucket Rate Limiter

Token Bucket is a rate limiting algorithm that allows bursts of traffic
while maintaining an average rate limit over time.

How it works:
- Bucket holds tokens, each representing permission to perform one action
- Tokens are added at a fixed rate (refill_rate)
- Bucket has a maximum capacity
- Request consumes tokens; if not enough tokens, request is denied
- Allows bursts up to bucket capacity

Your task: Implement a token bucket rate limiter.

Key concepts:
- Token refill based on time elapsed
- Bucket capacity limiting
- Thread-safe token consumption
- Handling time-based refills
"""

import time
from typing import Optional


class TokenBucket:
    """Token bucket rate limiter"""

    def __init__(self, capacity: float, refill_rate: float):
        """
        Initialize a new token bucket

        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        # TODO: Initialize a new token bucket
        # - Start with full capacity
        # - Set last_refill to current time
        pass

    def _refill(self):
        """Refill tokens based on time elapsed since last refill"""
        # TODO: Refill tokens based on time elapsed since last refill
        # - Calculate elapsed time since last_refill
        # - Calculate new tokens: elapsed_seconds * refill_rate
        # - Add new tokens but don't exceed capacity
        # - Update last_refill to current time
        pass

    def try_consume(self, tokens: float) -> bool:
        """
        Try to consume the specified number of tokens

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False otherwise
        """
        # TODO: Try to consume the specified number of tokens
        # - First call _refill() to update token count
        # - Check if enough tokens available
        # - If yes, subtract tokens and return True
        # - If no, return False (don't consume any tokens)
        pass

    def available_tokens(self) -> float:
        """Return current number of available tokens"""
        # TODO: Return current number of available tokens
        # - Call _refill() first to update count
        # - Return current tokens
        pass

    def wait_time_for(self, tokens: float) -> Optional[float]:
        """
        Calculate how long to wait until requested tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds, or None if tokens are already available
        """
        # TODO: Calculate how long to wait until requested tokens are available
        # - Call _refill() first
        # - If tokens already available, return None
        # - Calculate tokens needed: tokens - self.tokens
        # - Calculate wait time: tokens_needed / refill_rate
        # - Return wait time in seconds
        pass


import unittest


class TestTokenBucket(unittest.TestCase):
    def test_token_bucket_creation(self):
        bucket = TokenBucket(10.0, 5.0)
        self.assertEqual(bucket.available_tokens(), 10.0)

    def test_consume_tokens(self):
        bucket = TokenBucket(10.0, 5.0)
        self.assertTrue(bucket.try_consume(5.0))
        self.assertEqual(bucket.available_tokens(), 5.0)
        self.assertTrue(bucket.try_consume(5.0))
        self.assertEqual(bucket.available_tokens(), 0.0)

    def test_consume_too_many_tokens(self):
        bucket = TokenBucket(10.0, 5.0)
        self.assertFalse(bucket.try_consume(15.0))
        self.assertEqual(bucket.available_tokens(), 10.0)  # No tokens consumed

    def test_insufficient_tokens(self):
        bucket = TokenBucket(10.0, 5.0)
        bucket.try_consume(8.0)
        self.assertFalse(bucket.try_consume(5.0))  # Only 2 tokens left

    def test_token_refill(self):
        bucket = TokenBucket(10.0, 10.0)  # 10 tokens per second
        bucket.try_consume(10.0)
        self.assertEqual(bucket.available_tokens(), 0.0)

        time.sleep(0.5)  # Wait 0.5 seconds

        # Should have approximately 5 tokens (10 tokens/sec * 0.5 sec)
        available = bucket.available_tokens()
        self.assertGreaterEqual(available, 4.5)
        self.assertLessEqual(available, 5.5)

    def test_refill_does_not_exceed_capacity(self):
        bucket = TokenBucket(10.0, 10.0)
        bucket.try_consume(5.0)

        time.sleep(2.0)  # Wait 2 seconds

        # Should refill to capacity (10), not beyond
        available = bucket.available_tokens()
        self.assertEqual(available, 10.0)

    def test_burst_traffic(self):
        bucket = TokenBucket(10.0, 2.0)  # Low refill rate

        # Can handle burst up to capacity
        self.assertTrue(bucket.try_consume(3.0))
        self.assertTrue(bucket.try_consume(3.0))
        self.assertTrue(bucket.try_consume(3.0))
        self.assertEqual(bucket.available_tokens(), 1.0)

    def test_wait_time_calculation(self):
        bucket = TokenBucket(10.0, 5.0)  # 5 tokens per second
        bucket.try_consume(10.0)

        wait_time = bucket.wait_time_for(5.0)
        self.assertIsNotNone(wait_time)

        # Should wait approximately 1 second (5 tokens / 5 tokens per second)
        self.assertGreaterEqual(wait_time, 0.9)
        self.assertLessEqual(wait_time, 1.1)

    def test_wait_time_when_tokens_available(self):
        bucket = TokenBucket(10.0, 5.0)

        wait_time = bucket.wait_time_for(5.0)
        self.assertIsNone(wait_time)  # Tokens already available

    def test_partial_refill(self):
        bucket = TokenBucket(10.0, 20.0)  # 20 tokens per second
        bucket.try_consume(10.0)

        time.sleep(0.25)  # 0.25 seconds

        # Should have approximately 5 tokens (20 tokens/sec * 0.25 sec)
        available = bucket.available_tokens()
        self.assertGreaterEqual(available, 4.5)
        self.assertLessEqual(available, 5.5)

    def test_zero_consumption(self):
        bucket = TokenBucket(10.0, 5.0)
        self.assertTrue(bucket.try_consume(0.0))
        self.assertEqual(bucket.available_tokens(), 10.0)

    def test_fractional_tokens(self):
        bucket = TokenBucket(10.0, 5.0)
        self.assertTrue(bucket.try_consume(2.5))
        self.assertEqual(bucket.available_tokens(), 7.5)
        self.assertTrue(bucket.try_consume(1.25))
        self.assertEqual(bucket.available_tokens(), 6.25)


if __name__ == '__main__':
    unittest.main()
