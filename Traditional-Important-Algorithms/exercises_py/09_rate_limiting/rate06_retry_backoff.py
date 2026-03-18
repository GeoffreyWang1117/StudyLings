# I AM NOT DONE

"""
Exercise: Exponential Backoff Retry Strategy

Exponential Backoff is a retry strategy that progressively increases wait time
between retries to avoid overwhelming a failing service.

How it works:
- First retry after short delay (e.g., 100ms)
- Each subsequent retry doubles the delay (exponential growth)
- Optional jitter adds randomness to prevent thundering herd
- Maximum retry limit and maximum backoff cap

Your task: Implement exponential backoff retry strategy.

Key concepts:
- Exponential delay growth
- Jitter for distributed systems
- Max retry attempts
- Backoff ceiling
"""

import time
import random
from typing import Callable, TypeVar, Generic, Optional
from dataclasses import dataclass


T = TypeVar('T')
E = TypeVar('E')


@dataclass
class RetryConfig:
    """Configuration for retry strategy"""
    max_attempts: int = 3
    initial_delay: float = 0.1  # seconds
    max_delay: float = 30.0     # seconds
    multiplier: float = 2.0
    use_jitter: bool = True


class RetryStrategy:
    """Exponential backoff retry strategy"""

    def __init__(self, config: RetryConfig):
        """Initialize retry strategy"""
        # TODO: Initialize retry strategy
        pass

    @classmethod
    def with_defaults(cls):
        """Create with default configuration"""
        # TODO: Create with default configuration
        pass

    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number (0-indexed)

        Args:
            attempt: Attempt number (0-based)

        Returns:
            Delay in seconds
        """
        # TODO: Calculate delay for given attempt number (0-indexed)
        # - Base delay = initial_delay * (multiplier ^ attempt)
        # - Cap at max_delay
        # - If use_jitter, add random jitter (0% to 25% of delay)
        # - Return calculated duration in seconds
        #
        # Hint: Use random.random() for jitter
        pass

    def next_delay(self) -> Optional[float]:
        """Get delay for next retry attempt"""
        # TODO: Get delay for next retry attempt
        # - If current_attempt >= max_attempts, return None
        # - Otherwise, calculate and return delay for current_attempt
        pass

    def execute(self, operation: Callable[[], T]) -> T:
        """
        Execute operation with exponential backoff retry

        Args:
            operation: Function to execute

        Returns:
            Result of operation

        Raises:
            RetryError: If all attempts exhausted
        """
        # TODO: Execute operation with exponential backoff retry
        #
        # Logic:
        # 1. Loop through retry attempts (0 to max_attempts - 1)
        # 2. Try to execute operation
        # 3. If success, return result
        # 4. If failure:
        #    - If more attempts available, sleep for calculated delay
        #    - Increment current_attempt
        #    - Continue loop
        # 5. If all attempts exhausted, raise RetryError
        pass

    def current_attempt(self) -> int:
        """Return current attempt number"""
        # TODO: Return current attempt number
        pass

    def reset(self):
        """Reset attempt counter"""
        # TODO: Reset attempt counter
        pass

    def attempts_remaining(self) -> int:
        """Return number of attempts remaining"""
        # TODO: Return number of attempts remaining
        pass


class RetryError(Exception):
    """Exception raised when max attempts exceeded"""

    def __init__(self, last_error: Exception, attempts: int):
        self.last_error = last_error
        self.attempts = attempts
        super().__init__(f"Max attempts ({attempts}) exceeded. Last error: {last_error}")


def calculate_total_retry_time(config: RetryConfig) -> float:
    """
    Calculate total time spent on retries (excluding first attempt)

    Args:
        config: Retry configuration

    Returns:
        Total time in seconds
    """
    # TODO: Calculate total time spent on retries (excluding first attempt)
    # - Sum delays for all retry attempts
    # - Don't include jitter in this calculation (use base delays)
    pass


import unittest


class TestRetryStrategy(unittest.TestCase):
    def test_retry_config_default(self):
        config = RetryConfig()
        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.initial_delay, 0.1)
        self.assertEqual(config.multiplier, 2.0)

    def test_successful_first_attempt(self):
        strategy = RetryStrategy.with_defaults()
        result = strategy.execute(lambda: 42)
        self.assertEqual(result, 42)
        self.assertEqual(strategy.current_attempt(), 0)  # No retries needed

    def test_retry_after_failure(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.01,
            max_delay=1.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)
        counter = [0]

        def operation():
            counter[0] += 1
            if counter[0] < 3:
                raise Exception("temporary failure")
            return 42

        result = strategy.execute(operation)
        self.assertEqual(result, 42)
        self.assertEqual(counter[0], 3)  # Two failures, one success

    def test_max_attempts_exceeded(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.01,
            max_delay=1.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)
        counter = [0]

        def operation():
            counter[0] += 1
            raise Exception("persistent failure")

        with self.assertRaises(RetryError) as context:
            strategy.execute(operation)

        self.assertEqual(context.exception.attempts, 3)
        self.assertEqual(counter[0], 3)  # All attempts used

    def test_exponential_delay_growth(self):
        config = RetryConfig(
            max_attempts=4,
            initial_delay=0.1,
            max_delay=10.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)

        # Attempt 0: 100ms
        delay0 = strategy._calculate_delay(0)
        self.assertAlmostEqual(delay0, 0.1, places=3)

        # Attempt 1: 200ms
        delay1 = strategy._calculate_delay(1)
        self.assertAlmostEqual(delay1, 0.2, places=3)

        # Attempt 2: 400ms
        delay2 = strategy._calculate_delay(2)
        self.assertAlmostEqual(delay2, 0.4, places=3)

        # Attempt 3: 800ms
        delay3 = strategy._calculate_delay(3)
        self.assertAlmostEqual(delay3, 0.8, places=3)

    def test_max_delay_cap(self):
        config = RetryConfig(
            max_attempts=10,
            initial_delay=0.1,
            max_delay=0.5,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)

        # Attempt 5 would be 3.2s, but should be capped at 0.5s
        delay5 = strategy._calculate_delay(5)
        self.assertAlmostEqual(delay5, 0.5, places=3)

    def test_jitter_adds_randomness(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.1,
            max_delay=10.0,
            multiplier=2.0,
            use_jitter=True
        )

        strategy = RetryStrategy(config)

        # Calculate delay multiple times and check for reasonable range
        delay1 = strategy._calculate_delay(1)

        # With jitter, delay should be in range [0.1, 0.3] for attempt 1
        self.assertGreaterEqual(delay1, 0.1)
        self.assertLessEqual(delay1, 0.3)

    def test_reset(self):
        strategy = RetryStrategy.with_defaults()

        try:
            strategy.execute(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass

        self.assertGreater(strategy.current_attempt(), 0)

        strategy.reset()
        self.assertEqual(strategy.current_attempt(), 0)

    def test_attempts_remaining(self):
        config = RetryConfig(
            max_attempts=5,
            initial_delay=0.01,
            max_delay=1.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)
        self.assertEqual(strategy.attempts_remaining(), 5)

        try:
            strategy.execute(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass

        self.assertEqual(strategy.attempts_remaining(), 0)  # All used

    def test_next_delay(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.1,
            max_delay=10.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)

        self.assertIsNotNone(strategy.next_delay())

        # Exhaust attempts
        try:
            strategy.execute(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass

        self.assertIsNone(strategy.next_delay())

    def test_calculate_total_retry_time(self):
        config = RetryConfig(
            max_attempts=4,
            initial_delay=0.1,
            max_delay=10.0,
            multiplier=2.0,
            use_jitter=False
        )

        # Total = 0.1 + 0.2 + 0.4 = 0.7s (first attempt doesn't count)
        total = calculate_total_retry_time(config)
        self.assertAlmostEqual(total, 0.7, places=2)

    def test_custom_multiplier(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.1,
            max_delay=10.0,
            multiplier=3.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)

        delay0 = strategy._calculate_delay(0)
        delay1 = strategy._calculate_delay(1)
        delay2 = strategy._calculate_delay(2)

        self.assertAlmostEqual(delay0, 0.1, places=3)
        self.assertAlmostEqual(delay1, 0.3, places=3)  # 0.1 * 3
        self.assertAlmostEqual(delay2, 0.9, places=3)  # 0.1 * 3^2

    def test_eventual_success_timing(self):
        config = RetryConfig(
            max_attempts=3,
            initial_delay=0.05,
            max_delay=10.0,
            multiplier=2.0,
            use_jitter=False
        )

        strategy = RetryStrategy(config)
        counter = [0]

        def operation():
            counter[0] += 1
            if counter[0] < 3:
                raise Exception("fail")
            return "success"

        start = time.time()
        result = strategy.execute(operation)
        elapsed = time.time() - start

        # Should take at least 0.05s (first retry) + 0.1s (second retry) = 0.15s
        self.assertGreaterEqual(elapsed, 0.14)
        self.assertEqual(result, "success")


if __name__ == '__main__':
    unittest.main()
