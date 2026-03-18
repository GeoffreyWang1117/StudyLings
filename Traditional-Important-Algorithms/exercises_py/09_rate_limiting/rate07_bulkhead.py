# I AM NOT DONE

"""
Exercise: Bulkhead Isolation Pattern

Bulkhead is a fault tolerance pattern that isolates resources into pools
to prevent failure in one area from affecting others.

Inspired by ship bulkheads that prevent entire ship from sinking if one
compartment is breached.

How it works:
- Divide resources into isolated pools (e.g., thread pools per service)
- Each pool has fixed capacity
- Failure/exhaustion in one pool doesn't affect others
- Limits blast radius of failures

Your task: Implement a bulkhead isolation pattern.

Key concepts:
- Resource pool isolation
- Capacity limits per bulkhead
- Independent failure domains
- Resource acquisition and release
"""

from typing import Callable, TypeVar, Dict, List, Optional
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class BulkheadId:
    """Identifier for a bulkhead"""
    id: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, BulkheadId):
            return self.id == other.id
        return False


@dataclass
class BulkheadStats:
    """Statistics for a bulkhead"""
    name: str
    capacity: int
    in_use: int
    available: int
    total_accepted: int
    total_rejected: int
    utilization: float  # in_use / capacity


class BulkheadPool:
    """Internal representation of a bulkhead pool"""

    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.in_use = 0
        self.total_accepted = 0
        self.total_rejected = 0


class BulkheadIsolation:
    """Bulkhead isolation system for resource management"""

    def __init__(self):
        """Initialize empty bulkhead isolation system"""
        # TODO: Initialize empty bulkhead isolation system
        pass

    def create_bulkhead(self, bulkhead_id: BulkheadId, name: str, capacity: int):
        """Create a new bulkhead with given parameters"""
        # TODO: Create a new bulkhead with given parameters
        # - Initialize BulkheadPool with capacity and name
        # - Set in_use, total_accepted, total_rejected to 0
        # - Insert into bulkheads map
        pass

    def try_acquire(self, bulkhead_id: BulkheadId) -> bool:
        """
        Try to acquire a resource slot from bulkhead

        Args:
            bulkhead_id: ID of bulkhead to acquire from

        Returns:
            True if acquired, False if not found or full

        Raises:
            BulkheadError: If bulkhead not found or full
        """
        # TODO: Try to acquire a resource slot from bulkhead
        # - Check if bulkhead exists, raise BulkheadError("Not found") if not
        # - Check if in_use < capacity
        # - If yes, increment in_use and total_accepted, return True
        # - If no, increment total_rejected, raise BulkheadError("Full")
        pass

    def release(self, bulkhead_id: BulkheadId):
        """
        Release a resource slot back to bulkhead

        Args:
            bulkhead_id: ID of bulkhead to release to

        Raises:
            BulkheadError: If bulkhead not found
        """
        # TODO: Release a resource slot back to bulkhead
        # - Check if bulkhead exists
        # - Decrement in_use (but don't go below 0)
        # - Raise BulkheadError if not found
        pass

    def execute(self, bulkhead_id: BulkheadId, operation: Callable[[], T]) -> T:
        """
        Execute operation with bulkhead protection

        Args:
            bulkhead_id: ID of bulkhead to use
            operation: Function to execute

        Returns:
            Result of operation

        Raises:
            BulkheadError: If bulkhead issues occur
        """
        # TODO: Execute operation with bulkhead protection
        # - Try to acquire slot
        # - If successful, execute operation
        # - Release slot (even if operation raises - use try/finally)
        # - Return result or propagate BulkheadError
        pass

    def get_stats(self, bulkhead_id: BulkheadId) -> Optional[BulkheadStats]:
        """Return statistics for given bulkhead"""
        # TODO: Return statistics for given bulkhead
        # - Return None if not found
        # - Return BulkheadStats with current values
        pass

    def available_capacity(self, bulkhead_id: BulkheadId) -> Optional[int]:
        """Return available capacity for bulkhead"""
        # TODO: Return available capacity for bulkhead
        # - Return None if not found
        # - Return capacity - in_use
        pass

    def is_full(self, bulkhead_id: BulkheadId) -> bool:
        """Check if bulkhead is at capacity"""
        # TODO: Check if bulkhead is at capacity
        # - Return True if in_use >= capacity
        # - Return False if not found or has capacity
        pass

    def reset(self, bulkhead_id: BulkheadId):
        """
        Reset bulkhead statistics (keep capacity)

        Args:
            bulkhead_id: ID of bulkhead to reset

        Raises:
            BulkheadError: If bulkhead not found
        """
        # TODO: Reset bulkhead statistics (keep capacity)
        # - Reset in_use, total_accepted, total_rejected to 0
        pass

    def list_bulkheads(self) -> List[BulkheadId]:
        """Return list of all bulkhead IDs"""
        # TODO: Return list of all bulkhead IDs
        pass


class BulkheadError(Exception):
    """Exception raised for bulkhead errors"""
    pass


import unittest


class TestBulkheadIsolation(unittest.TestCase):
    def test_create_bulkhead(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "service-a", 5)

        stats = isolation.get_stats(BulkheadId(1))
        self.assertIsNotNone(stats)
        self.assertEqual(stats.name, "service-a")
        self.assertEqual(stats.capacity, 5)
        self.assertEqual(stats.in_use, 0)

    def test_acquire_and_release(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "test", 3)

        self.assertTrue(isolation.try_acquire(BulkheadId(1)))
        self.assertEqual(isolation.available_capacity(BulkheadId(1)), 2)

        isolation.release(BulkheadId(1))
        self.assertEqual(isolation.available_capacity(BulkheadId(1)), 3)

    def test_capacity_limit(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "limited", 2)

        self.assertTrue(isolation.try_acquire(BulkheadId(1)))
        self.assertTrue(isolation.try_acquire(BulkheadId(1)))

        with self.assertRaises(BulkheadError):
            isolation.try_acquire(BulkheadId(1))

        self.assertTrue(isolation.is_full(BulkheadId(1)))

    def test_nonexistent_bulkhead(self):
        isolation = BulkheadIsolation()

        with self.assertRaises(BulkheadError):
            isolation.try_acquire(BulkheadId(99))

        self.assertIsNone(isolation.get_stats(BulkheadId(99)))

    def test_execute_with_bulkhead(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "exec", 3)

        result = isolation.execute(BulkheadId(1), lambda: 42)
        self.assertEqual(result, 42)

        # After execution, slot should be released
        self.assertEqual(isolation.available_capacity(BulkheadId(1)), 3)

    def test_execute_when_full(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "full", 1)

        isolation.try_acquire(BulkheadId(1))

        with self.assertRaises(BulkheadError):
            isolation.execute(BulkheadId(1), lambda: 42)

    def test_isolation_between_bulkheads(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "service-a", 2)
        isolation.create_bulkhead(BulkheadId(2), "service-b", 2)

        # Fill bulkhead 1
        isolation.try_acquire(BulkheadId(1))
        isolation.try_acquire(BulkheadId(1))

        # Bulkhead 1 full, but bulkhead 2 still available
        self.assertTrue(isolation.is_full(BulkheadId(1)))
        self.assertFalse(isolation.is_full(BulkheadId(2)))
        self.assertTrue(isolation.try_acquire(BulkheadId(2)))

    def test_statistics_tracking(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "stats", 2)

        isolation.try_acquire(BulkheadId(1))
        isolation.try_acquire(BulkheadId(1))
        try:
            isolation.try_acquire(BulkheadId(1))  # Rejected
        except:
            pass

        stats = isolation.get_stats(BulkheadId(1))
        self.assertEqual(stats.total_accepted, 2)
        self.assertEqual(stats.total_rejected, 1)

    def test_utilization_calculation(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "util", 4)

        isolation.try_acquire(BulkheadId(1))
        isolation.try_acquire(BulkheadId(1))

        stats = isolation.get_stats(BulkheadId(1))
        self.assertAlmostEqual(stats.utilization, 0.5, places=2)  # 2/4 = 50%

    def test_reset(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "reset", 3)

        isolation.try_acquire(BulkheadId(1))
        isolation.try_acquire(BulkheadId(1))

        isolation.reset(BulkheadId(1))

        stats = isolation.get_stats(BulkheadId(1))
        self.assertEqual(stats.in_use, 0)
        self.assertEqual(stats.total_accepted, 0)
        self.assertEqual(stats.total_rejected, 0)
        self.assertEqual(stats.capacity, 3)  # Capacity unchanged

    def test_list_bulkheads(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "a", 1)
        isolation.create_bulkhead(BulkheadId(2), "b", 2)
        isolation.create_bulkhead(BulkheadId(3), "c", 3)

        ids = isolation.list_bulkheads()
        id_values = sorted([bid.id for bid in ids])

        self.assertEqual(id_values, [1, 2, 3])

    def test_multiple_operations(self):
        isolation = BulkheadIsolation()
        isolation.create_bulkhead(BulkheadId(1), "multi", 3)

        r1 = isolation.execute(BulkheadId(1), lambda: "first")
        r2 = isolation.execute(BulkheadId(1), lambda: "second")
        r3 = isolation.execute(BulkheadId(1), lambda: "third")

        self.assertEqual(r1, "first")
        self.assertEqual(r2, "second")
        self.assertEqual(r3, "third")

        stats = isolation.get_stats(BulkheadId(1))
        self.assertEqual(stats.total_accepted, 3)
        self.assertEqual(stats.in_use, 0)  # All released


if __name__ == '__main__':
    unittest.main()
