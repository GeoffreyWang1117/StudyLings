# I AM NOT DONE

"""
dist06_lease_mechanism.py

Leases are time-based locks used in distributed systems to grant exclusive
access to a resource for a limited time. They're essential for coordination
without requiring continuous communication.

Key properties:
- Time-bounded: Automatically expire after a duration
- No revocation needed: Holder knows when lease expires
- Fault-tolerant: System recovers when lease expires
- Used for: Leader election, distributed locks, cache consistency

Your task: Implement a lease-based distributed lock system.

Key concepts:
- Lease grant: Server grants lease to a client for specific duration
- Lease renewal: Client can renew before expiration
- Lease expiration: Automatic release when time runs out
- Clock skew: Handle minor time differences between nodes
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional
import unittest


@dataclass
class Lease:
    """A lease on a resource."""
    resource: str
    holder: str
    granted_at: int
    expires_at: int
    version: int

    def is_expired(self, current_time: int) -> bool:
        """Check if the lease has expired."""
        return current_time >= self.expires_at

    def remaining_time(self, current_time: int) -> int:
        """Get remaining time on the lease."""
        if self.is_expired(current_time):
            return 0
        return self.expires_at - current_time


class LeaseError(Enum):
    """Lease error types."""
    ALREADY_LEASED = auto()
    NOT_HOLDER = auto()
    EXPIRED = auto()
    RESOURCE_NOT_FOUND = auto()


@dataclass
class LeaseInfo:
    """Information about a lease."""
    resource: str
    holder: str
    is_expired: bool
    remaining_time: int
    version: int


class LeaseManager:
    """Manager for time-based leases."""

    def __init__(self, default_duration: int, max_duration: int):
        """Initialize the lease manager."""
        self.leases: Dict[str, Lease] = {}
        self.current_time = 0
        self.default_duration = default_duration
        self.max_duration = max_duration
        self.version_counter = 0

    def acquire_lease(self, resource: str, holder: str,
                     duration: Optional[int] = None) -> tuple:
        """
        TODO: Acquire a new lease.

        - Check if resource already has a valid (non-expired) lease
        - If expired or no lease, grant new lease
        - Use provided duration or default_duration (capped at max_duration)
        - Increment version_counter for new lease
        - Return (lease, None) on success or (None, LeaseError) on failure
        """
        pass  # TODO: Implement this

    def renew_lease(self, resource: str, holder: str,
                   duration: Optional[int] = None) -> tuple:
        """
        TODO: Renew an existing lease.

        - Check if lease exists
        - Verify caller is the holder
        - Check if lease has expired (if so, return Expired error)
        - Extend expires_at by duration (capped at max_duration from current_time)
        - Increment version
        - Return (updated_lease, None) or (None, LeaseError)
        """
        pass  # TODO: Implement this

    def release_lease(self, resource: str, holder: str) -> Optional[LeaseError]:
        """
        TODO: Release a lease early.

        - Check if lease exists
        - Verify caller is the holder
        - Remove the lease
        - Return None on success or LeaseError on failure
        """
        pass  # TODO: Implement this

    def check_lease(self, resource: str) -> Optional[Lease]:
        """
        TODO: Check current lease status.

        - Return the lease if it exists and is not expired
        - Return None if no lease or expired
        """
        pass  # TODO: Implement this

    def advance_time(self, delta: int):
        """
        TODO: Advance current time and clean up expired leases.

        - Increment current_time by delta
        - Remove all expired leases from the dict
        """
        pass  # TODO: Implement this

    def set_time(self, time: int):
        """Set the current time."""
        self.current_time = time
        # Clean up expired leases
        self.leases = {
            res: lease for res, lease in self.leases.items()
            if not lease.is_expired(self.current_time)
        }

    def get_time(self) -> int:
        """Get the current time."""
        return self.current_time

    def get_active_leases(self) -> List[Lease]:
        """Get all active (non-expired) leases."""
        return [
            lease for lease in self.leases.values()
            if not lease.is_expired(self.current_time)
        ]

    def get_lease_info(self, resource: str) -> Optional[LeaseInfo]:
        """Get information about a lease."""
        lease = self.leases.get(resource)
        if not lease:
            return None

        return LeaseInfo(
            resource=lease.resource,
            holder=lease.holder,
            is_expired=lease.is_expired(self.current_time),
            remaining_time=lease.remaining_time(self.current_time),
            version=lease.version
        )


# Unit Tests
class TestLeaseMechanism(unittest.TestCase):

    def test_acquire_lease(self):
        manager = LeaseManager(100, 500)

        lease, error = manager.acquire_lease("resource1", "client1")
        self.assertIsNone(error)
        self.assertIsNotNone(lease)

        self.assertEqual(lease.resource, "resource1")
        self.assertEqual(lease.holder, "client1")
        self.assertEqual(lease.expires_at, 100)

    def test_cannot_acquire_leased_resource(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")

        lease, error = manager.acquire_lease("resource1", "client2")
        self.assertIsNone(lease)
        self.assertEqual(error, LeaseError.ALREADY_LEASED)

    def test_lease_expiration(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")

        # Before expiration
        self.assertIsNotNone(manager.check_lease("resource1"))

        # Advance time past expiration
        manager.advance_time(101)

        # After expiration
        self.assertIsNone(manager.check_lease("resource1"))

    def test_acquire_after_expiration(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.advance_time(101)

        # Different client can now acquire
        lease, error = manager.acquire_lease("resource1", "client2")
        self.assertIsNone(error)
        self.assertEqual(lease.holder, "client2")

    def test_renew_lease(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.advance_time(50)

        lease, error = manager.renew_lease("resource1", "client1", 100)
        self.assertIsNone(error)
        self.assertIsNotNone(lease)

        self.assertEqual(lease.expires_at, 150)  # 50 + 100

    def test_cannot_renew_others_lease(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")

        lease, error = manager.renew_lease("resource1", "client2", 100)
        self.assertIsNone(lease)
        self.assertEqual(error, LeaseError.NOT_HOLDER)

    def test_cannot_renew_expired_lease(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.advance_time(101)

        lease, error = manager.renew_lease("resource1", "client1", 100)
        self.assertIsNone(lease)
        self.assertEqual(error, LeaseError.EXPIRED)

    def test_release_lease(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")

        error = manager.release_lease("resource1", "client1")
        self.assertIsNone(error)

        # Resource should now be available
        self.assertIsNone(manager.check_lease("resource1"))

    def test_cannot_release_others_lease(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")

        error = manager.release_lease("resource1", "client2")
        self.assertEqual(error, LeaseError.NOT_HOLDER)

    def test_max_duration_cap(self):
        manager = LeaseManager(100, 200)

        lease, error = manager.acquire_lease("resource1", "client1", 500)
        self.assertIsNone(error)

        # Should be capped at max_duration (200), not requested 500
        self.assertEqual(lease.expires_at, 200)

    def test_lease_versions(self):
        manager = LeaseManager(100, 500)

        lease1, _ = manager.acquire_lease("resource1", "client1")
        self.assertEqual(lease1.version, 1)

        manager.advance_time(50)
        lease2, _ = manager.renew_lease("resource1", "client1")
        self.assertEqual(lease2.version, 2)

    def test_multiple_resources(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.acquire_lease("resource2", "client2")
        manager.acquire_lease("resource3", "client1")

        active = manager.get_active_leases()
        self.assertEqual(len(active), 3)

    def test_lease_info(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.advance_time(30)

        info = manager.get_lease_info("resource1")
        self.assertIsNotNone(info)
        self.assertEqual(info.holder, "client1")
        self.assertFalse(info.is_expired)
        self.assertEqual(info.remaining_time, 70)

    def test_cleanup_expired_leases(self):
        manager = LeaseManager(100, 500)

        manager.acquire_lease("resource1", "client1")
        manager.acquire_lease("resource2", "client2")

        manager.advance_time(101)

        active = manager.get_active_leases()
        self.assertEqual(len(active), 0)


if __name__ == '__main__':
    unittest.main()
