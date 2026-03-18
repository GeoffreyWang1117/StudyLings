# I AM NOT DONE

"""
Exercise: Circuit Breaker Pattern

Circuit Breaker is a fault tolerance pattern that prevents cascading failures
by stopping requests to a failing service and allowing it time to recover.

States:
- Closed: Normal operation, requests pass through
- Open: Service failing, requests rejected immediately (fail fast)
- Half-Open: Testing recovery, limited requests allowed

Your task: Implement a circuit breaker with three states.

Key concepts:
- State transitions based on failure/success thresholds
- Timeout for recovery attempts
- Failure tracking in sliding window
- Fail-fast behavior
"""

import time
from typing import Callable, TypeVar, Generic, List
from enum import Enum


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"        # Normal operation
    OPEN = "open"           # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing recovery


T = TypeVar('T')
E = TypeVar('E')


class RequestResult:
    """Record of a request result"""

    def __init__(self, success: bool, timestamp: float):
        self.success = success
        self.timestamp = timestamp


class CircuitBreaker:
    """Circuit breaker for fault tolerance"""

    def __init__(self,
                 failure_threshold: int,
                 success_threshold: int,
                 timeout: float,
                 window_size: int):
        """
        Initialize circuit breaker

        Args:
            failure_threshold: Failures needed to open circuit
            success_threshold: Successes needed to close from half-open
            timeout: Time to wait before half-open (in seconds)
            window_size: Number of recent requests to track
        """
        # TODO: Initialize circuit breaker in CLOSED state
        pass

    def _count_recent_failures(self) -> int:
        """Count failures in the recent window"""
        # TODO: Count failures in the recent window
        # - Iterate through recent_results
        # - Count how many have success = False
        # - Only consider up to window_size most recent results
        pass

    def _should_transition_to_half_open(self) -> bool:
        """Check if enough time has passed to try half-open"""
        # TODO: Check if enough time has passed to try half-open
        # - Return True if state is OPEN and timeout has elapsed since opened_at
        # - Otherwise return False
        pass

    def _update_state(self):
        """Update circuit state based on current conditions"""
        # TODO: Update circuit state based on current conditions
        #
        # Logic:
        # 1. If state is OPEN and should_transition_to_half_open:
        #    - Set state to HALF_OPEN
        #    - Reset half_open_successes to 0
        #
        # 2. If state is CLOSED and count_recent_failures >= failure_threshold:
        #    - Set state to OPEN
        #    - Set opened_at to current time
        #
        # 3. If state is HALF_OPEN and half_open_successes >= success_threshold:
        #    - Set state to CLOSED
        #    - Clear recent_results
        pass

    def call(self, operation: Callable[[], T]) -> T:
        """
        Execute operation with circuit breaker protection

        Args:
            operation: Function to execute

        Returns:
            Result of operation

        Raises:
            CircuitBreakerError: If circuit is open
            Exception: If operation raises an exception
        """
        # TODO: Execute operation with circuit breaker protection
        #
        # 1. Update state first
        # 2. If state is OPEN, raise CircuitBreakerError("Circuit breaker is open")
        # 3. Try to execute operation
        # 4. Record result:
        #    - Add to recent_results (keep only last window_size entries)
        #    - If HALF_OPEN and success, increment half_open_successes
        #    - If HALF_OPEN and failure, set state to OPEN with new timeout
        # 5. Update state again
        # 6. Return result or raise exception
        pass

    def state(self) -> CircuitState:
        """Return current state (update state first)"""
        # TODO: Return current state (update state first)
        pass

    def failure_count(self) -> int:
        """Return count of recent failures"""
        # TODO: Return count of recent failures
        pass

    def success_rate(self) -> float:
        """Calculate success rate from recent results"""
        # TODO: Calculate success rate from recent results
        # - If no results, return 1.0 (100%)
        # - Otherwise: successes / total_results
        # - Only consider last window_size results
        pass

    def reset(self):
        """Reset circuit breaker to initial CLOSED state"""
        # TODO: Reset circuit breaker to initial CLOSED state
        # - Clear recent_results
        # - Set state to CLOSED
        # - Reset counters
        pass


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open"""
    pass


import unittest


class TestCircuitBreaker(unittest.TestCase):
    def test_circuit_breaker_creation(self):
        cb = CircuitBreaker(3, 2, 1.0, 10)
        self.assertEqual(cb.state(), CircuitState.CLOSED)

    def test_successful_calls_stay_closed(self):
        cb = CircuitBreaker(3, 2, 1.0, 10)

        for _ in range(10):
            result = cb.call(lambda: 42)
            self.assertEqual(result, 42)

        self.assertEqual(cb.state(), CircuitState.CLOSED)

    def test_failures_open_circuit(self):
        cb = CircuitBreaker(3, 2, 0.1, 10)

        # First 2 failures don't open circuit
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        self.assertEqual(cb.state(), CircuitState.CLOSED)

        # Third failure opens circuit
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        self.assertEqual(cb.state(), CircuitState.OPEN)

    def test_open_circuit_rejects_requests(self):
        cb = CircuitBreaker(2, 2, 1.0, 10)

        # Open the circuit
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass

        self.assertEqual(cb.state(), CircuitState.OPEN)

        # Next request should be rejected without calling operation
        with self.assertRaises(CircuitBreakerError):
            cb.call(lambda: 42)

    def test_transition_to_half_open(self):
        cb = CircuitBreaker(2, 2, 0.1, 10)

        # Open circuit
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass

        self.assertEqual(cb.state(), CircuitState.OPEN)

        # Wait for timeout
        time.sleep(0.15)

        # Should transition to half-open on next state check
        self.assertEqual(cb.state(), CircuitState.HALF_OPEN)

    def test_half_open_success_closes_circuit(self):
        cb = CircuitBreaker(2, 2, 0.1, 10)

        # Open circuit
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass

        # Wait and transition to half-open
        time.sleep(0.15)
        cb.state()

        self.assertEqual(cb.state(), CircuitState.HALF_OPEN)

        # Successful calls should close circuit
        cb.call(lambda: 1)
        cb.call(lambda: 2)

        self.assertEqual(cb.state(), CircuitState.CLOSED)

    def test_half_open_failure_reopens_circuit(self):
        cb = CircuitBreaker(2, 2, 0.1, 10)

        # Open circuit
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass

        # Wait and transition to half-open
        time.sleep(0.15)
        cb.state()

        self.assertEqual(cb.state(), CircuitState.HALF_OPEN)

        # Failure in half-open should reopen circuit
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass

        self.assertEqual(cb.state(), CircuitState.OPEN)

    def test_failure_count(self):
        cb = CircuitBreaker(5, 2, 1.0, 10)

        cb.call(lambda: 1)
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        cb.call(lambda: 2)

        self.assertEqual(cb.failure_count(), 2)

    def test_success_rate(self):
        cb = CircuitBreaker(5, 2, 1.0, 10)

        cb.call(lambda: 1)
        cb.call(lambda: 2)
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        cb.call(lambda: 3)

        # 3 successes out of 4 = 75%
        self.assertAlmostEqual(cb.success_rate(), 0.75, places=2)

    def test_window_size_limit(self):
        cb = CircuitBreaker(5, 2, 1.0, 3)

        # Add more results than window size
        for _ in range(5):
            cb.call(lambda: 1)

        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass

        # Should only count failure in window of last 3 requests
        self.assertEqual(cb.failure_count(), 1)

    def test_reset(self):
        cb = CircuitBreaker(2, 2, 1.0, 10)

        # Open circuit
        for _ in range(2):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
            except:
                pass

        self.assertEqual(cb.state(), CircuitState.OPEN)

        # Reset
        cb.reset()

        self.assertEqual(cb.state(), CircuitState.CLOSED)
        self.assertEqual(cb.failure_count(), 0)

    def test_mixed_results(self):
        cb = CircuitBreaker(3, 2, 1.0, 10)

        cb.call(lambda: 1)
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        cb.call(lambda: 2)
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("error")))
        except:
            pass
        cb.call(lambda: 3)

        # Only 2 failures, should still be closed
        self.assertEqual(cb.state(), CircuitState.CLOSED)
        self.assertEqual(cb.failure_count(), 2)


if __name__ == '__main__':
    unittest.main()
