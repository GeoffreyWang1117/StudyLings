# I AM NOT DONE

"""
Exercise: Adaptive Rate Limiting

Adaptive Rate Limiting dynamically adjusts rate limits based on system load,
performance metrics, and historical patterns.

How it works:
- Monitor system metrics (CPU, memory, latency, error rate)
- Adjust rate limits based on current capacity
- Increase limits when system is healthy
- Decrease limits when system is under stress
- Use feedback loops for continuous optimization

Your task: Implement an adaptive rate limiter that adjusts to system load.

Key concepts:
- System health monitoring
- Dynamic threshold adjustment
- Feedback control loops
- Load-based rate limiting
"""

import time
from collections import deque
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_usage: float         # 0.0 to 1.0
    memory_usage: float      # 0.0 to 1.0
    error_rate: float        # 0.0 to 1.0
    avg_latency_ms: float
    timestamp: float


@dataclass
class AdaptiveConfig:
    """Configuration for adaptive rate limiter"""
    min_rate: int = 10            # Minimum requests per second
    max_rate: int = 1000          # Maximum requests per second
    cpu_threshold: float = 0.7    # Start reducing rate above this
    memory_threshold: float = 0.8  # Start reducing rate above this
    error_threshold: float = 0.05  # Start reducing rate above this
    latency_threshold_ms: float = 1000.0  # Start reducing rate above this
    increase_factor: float = 1.1  # Rate increase multiplier
    decrease_factor: float = 0.8  # Rate decrease multiplier


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts to system load"""

    def __init__(self, config: AdaptiveConfig, adjustment_interval: float):
        """
        Initialize adaptive rate limiter

        Args:
            config: Configuration for adaptation
            adjustment_interval: Time between rate adjustments (seconds)
        """
        # TODO: Initialize adaptive rate limiter
        # - Set current_rate to max_rate (start optimistic)
        # - Create empty histories
        # - Set last_adjustment to now
        pass

    @classmethod
    def with_defaults(cls):
        """Create with default config and 1-second adjustment interval"""
        # TODO: Create with default config and 1-second adjustment interval
        pass

    def _cleanup_old_requests(self, window: float):
        """Remove requests older than window from history"""
        # TODO: Remove requests older than window from history
        # - Calculate cutoff time
        # - Remove old requests from front of queue
        pass

    def _should_adjust(self) -> bool:
        """Check if enough time has passed to adjust rate"""
        # TODO: Check if enough time has passed to adjust rate
        # - Return True if time since last_adjustment >= adjustment_interval
        pass

    def _calculate_new_rate(self, metrics: SystemMetrics) -> int:
        """Calculate new rate based on system metrics"""
        # TODO: Calculate new rate based on system metrics
        #
        # Logic:
        # 1. Start with current_rate
        # 2. Check each threshold:
        #    - If CPU > threshold, multiply by decrease_factor
        #    - If memory > threshold, multiply by decrease_factor
        #    - If error_rate > threshold, multiply by decrease_factor
        #    - If latency > threshold, multiply by decrease_factor
        # 3. If all metrics healthy, multiply by increase_factor
        # 4. Clamp result between min_rate and max_rate
        # 5. Return new rate as int
        pass

    def update_metrics(self, metrics: SystemMetrics):
        """Update system metrics and adjust rate if needed"""
        # TODO: Update system metrics and adjust rate if needed
        # - Add metrics to metrics_history
        # - Keep only recent metrics (e.g., last 100)
        # - If should_adjust():
        #   - Calculate new rate
        #   - Update current_rate
        #   - Update last_adjustment
        pass

    def try_acquire(self) -> bool:
        """Try to acquire request slot"""
        # TODO: Try to acquire request slot
        # - Cleanup old requests (1 second window)
        # - Count requests in last second
        # - If count < current_rate:
        #   - Add current time to request_history
        #   - Return True
        # - Otherwise return False
        pass

    def current_rate(self) -> int:
        """Return current rate limit"""
        # TODO: Return current rate limit
        pass

    def request_count_last_second(self) -> int:
        """Return number of requests in last second"""
        # TODO: Return number of requests in last second
        # - Cleanup old requests first
        # - Return request_history length
        pass

    def average_cpu_usage(self) -> Optional[float]:
        """Calculate average CPU usage from recent metrics"""
        # TODO: Calculate average CPU usage from recent metrics
        # - Return None if no metrics
        # - Otherwise average the cpu_usage values
        pass

    def average_latency(self) -> Optional[float]:
        """Calculate average latency from recent metrics"""
        # TODO: Calculate average latency from recent metrics
        # - Return None if no metrics
        # - Otherwise average the avg_latency_ms values
        pass

    def is_system_healthy(self) -> bool:
        """Check if system is healthy based on recent metrics"""
        # TODO: Check if system is healthy based on recent metrics
        # - Get most recent metrics, return True if none
        # - Check all thresholds
        # - Return True only if all metrics below thresholds
        pass

    def reset(self):
        """Reset to initial state"""
        # TODO: Reset to initial state
        # - Clear histories
        # - Reset current_rate to max_rate
        # - Update last_adjustment
        pass


class AIMDRateLimiter:
    """AIMD (Additive Increase Multiplicative Decrease) rate limiter"""

    def __init__(self, initial_rate: float, min_rate: float, max_rate: float,
                 increase_amount: float, decrease_factor: float):
        """Initialize AIMD rate limiter"""
        # TODO: Initialize AIMD rate limiter
        pass

    def on_success(self):
        """Handle successful request"""
        # TODO: Handle successful request
        # - Additively increase rate
        # - current_rate += increase_amount
        # - Clamp to max_rate
        # - Set last_success to True
        pass

    def on_failure(self):
        """Handle failed request"""
        # TODO: Handle failed request
        # - Multiplicatively decrease rate
        # - current_rate *= decrease_factor
        # - Clamp to min_rate
        # - Set last_success to False
        pass

    def get_rate(self) -> float:
        """Return current rate"""
        # TODO: Return current rate
        pass

    def reset(self, rate: float):
        """Reset to specific rate"""
        # TODO: Reset to specific rate
        pass


import unittest


class TestAdaptiveRateLimiter(unittest.TestCase):
    def test_adaptive_limiter_creation(self):
        limiter = AdaptiveRateLimiter.with_defaults()
        self.assertEqual(limiter.current_rate(), 1000)  # Starts at max

    def test_acquire_under_limit(self):
        limiter = AdaptiveRateLimiter.with_defaults()

        # Should be able to acquire up to current rate
        for _ in range(10):
            self.assertTrue(limiter.try_acquire())

    def test_rate_limiting(self):
        config = AdaptiveConfig(min_rate=5, max_rate=10)

        limiter = AdaptiveRateLimiter(config, 1.0)

        # Fill up to limit
        for _ in range(10):
            limiter.try_acquire()

        # Next should be rejected
        self.assertFalse(limiter.try_acquire())

    def test_rate_decrease_on_high_cpu(self):
        config = AdaptiveConfig(cpu_threshold=0.5, decrease_factor=0.5)

        limiter = AdaptiveRateLimiter(config, 0.01)
        initial_rate = limiter.current_rate()

        time.sleep(0.015)

        # High CPU usage
        metrics = SystemMetrics(
            cpu_usage=0.9,
            memory_usage=0.3,
            error_rate=0.0,
            avg_latency_ms=100.0,
            timestamp=time.time()
        )

        limiter.update_metrics(metrics)

        # Rate should decrease
        self.assertLess(limiter.current_rate(), initial_rate)

    def test_rate_increase_when_healthy(self):
        config = AdaptiveConfig(increase_factor=1.5, max_rate=1000)

        limiter = AdaptiveRateLimiter(config, 0.01)

        # Start at lower rate
        limiter.update_metrics(SystemMetrics(
            cpu_usage=0.9, memory_usage=0.9, error_rate=0.0,
            avg_latency_ms=100.0, timestamp=time.time()
        ))

        time.sleep(0.015)

        rate_before = limiter.current_rate()

        # Healthy metrics
        metrics = SystemMetrics(
            cpu_usage=0.3, memory_usage=0.3, error_rate=0.0,
            avg_latency_ms=100.0, timestamp=time.time()
        )

        limiter.update_metrics(metrics)

        # Rate should increase
        self.assertGreater(limiter.current_rate(), rate_before)

    def test_rate_bounds(self):
        config = AdaptiveConfig(
            min_rate=10, max_rate=100,
            decrease_factor=0.1, increase_factor=10.0
        )

        limiter = AdaptiveRateLimiter(config, 0.01)

        # Try to decrease below min
        time.sleep(0.015)
        for _ in range(10):
            limiter.update_metrics(SystemMetrics(
                cpu_usage=1.0, memory_usage=1.0, error_rate=1.0,
                avg_latency_ms=10000.0, timestamp=time.time()
            ))
            time.sleep(0.015)

        self.assertEqual(limiter.current_rate(), 10)  # Clamped to min

        # Try to increase above max
        for _ in range(10):
            limiter.update_metrics(SystemMetrics(
                cpu_usage=0.0, memory_usage=0.0, error_rate=0.0,
                avg_latency_ms=1.0, timestamp=time.time()
            ))
            time.sleep(0.015)

        self.assertEqual(limiter.current_rate(), 100)  # Clamped to max

    def test_request_count(self):
        limiter = AdaptiveRateLimiter.with_defaults()

        limiter.try_acquire()
        limiter.try_acquire()
        limiter.try_acquire()

        self.assertEqual(limiter.request_count_last_second(), 3)

    def test_average_metrics(self):
        limiter = AdaptiveRateLimiter.with_defaults()

        limiter.update_metrics(SystemMetrics(
            cpu_usage=0.5, memory_usage=0.5, error_rate=0.0,
            avg_latency_ms=200.0, timestamp=time.time()
        ))

        limiter.update_metrics(SystemMetrics(
            cpu_usage=0.7, memory_usage=0.6, error_rate=0.0,
            avg_latency_ms=300.0, timestamp=time.time()
        ))

        avg_cpu = limiter.average_cpu_usage()
        avg_latency = limiter.average_latency()

        self.assertAlmostEqual(avg_cpu, 0.6, places=1)
        self.assertAlmostEqual(avg_latency, 250.0, places=0)

    def test_system_health_check(self):
        limiter = AdaptiveRateLimiter.with_defaults()

        # Healthy metrics
        limiter.update_metrics(SystemMetrics(
            cpu_usage=0.3, memory_usage=0.4, error_rate=0.01,
            avg_latency_ms=100.0, timestamp=time.time()
        ))

        self.assertTrue(limiter.is_system_healthy())

        # Unhealthy metrics
        limiter.update_metrics(SystemMetrics(
            cpu_usage=0.9, memory_usage=0.9, error_rate=0.1,
            avg_latency_ms=5000.0, timestamp=time.time()
        ))

        self.assertFalse(limiter.is_system_healthy())

    def test_aimd_creation(self):
        aimd = AIMDRateLimiter(100.0, 10.0, 1000.0, 5.0, 0.8)
        self.assertEqual(aimd.get_rate(), 100.0)

    def test_aimd_additive_increase(self):
        aimd = AIMDRateLimiter(100.0, 10.0, 1000.0, 10.0, 0.8)

        aimd.on_success()
        self.assertEqual(aimd.get_rate(), 110.0)

        aimd.on_success()
        self.assertEqual(aimd.get_rate(), 120.0)

    def test_aimd_multiplicative_decrease(self):
        aimd = AIMDRateLimiter(100.0, 10.0, 1000.0, 5.0, 0.5)

        aimd.on_failure()
        self.assertEqual(aimd.get_rate(), 50.0)

        aimd.on_failure()
        self.assertEqual(aimd.get_rate(), 25.0)

    def test_aimd_bounds(self):
        aimd = AIMDRateLimiter(50.0, 10.0, 100.0, 20.0, 0.5)

        # Try to increase above max
        for _ in range(10):
            aimd.on_success()
        self.assertEqual(aimd.get_rate(), 100.0)

        # Try to decrease below min
        for _ in range(10):
            aimd.on_failure()
        self.assertEqual(aimd.get_rate(), 10.0)

    def test_aimd_reset(self):
        aimd = AIMDRateLimiter(100.0, 10.0, 1000.0, 5.0, 0.8)

        aimd.on_success()
        aimd.on_success()

        aimd.reset(200.0)
        self.assertEqual(aimd.get_rate(), 200.0)

    def test_adaptive_reset(self):
        limiter = AdaptiveRateLimiter.with_defaults()

        limiter.try_acquire()
        limiter.try_acquire()

        limiter.reset()

        self.assertEqual(limiter.request_count_last_second(), 0)
        self.assertEqual(limiter.current_rate(), 1000)


if __name__ == '__main__':
    unittest.main()
