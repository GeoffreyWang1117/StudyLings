# I AM NOT DONE

"""
os09_reader_writer.py

The Reader-Writer problem involves synchronizing access to a shared resource where
multiple readers can access the resource simultaneously, but writers need exclusive
access. This is a fundamental concurrency control problem.

Your task: Implement reader-writer locks with different fairness policies.
"""

import threading
from enum import Enum
from typing import Generic, TypeVar
import unittest
import time


T = TypeVar('T')


class LockPolicy(Enum):
    """Lock fairness policies."""
    READERS_PREFERENCE = "readers_preference"  # Readers are preferred, writers may starve
    WRITERS_PREFERENCE = "writers_preference"  # Writers are preferred, readers may starve
    FAIR = "fair"  # Fair scheduling, no starvation


class RwLock(Generic[T]):
    """Reader-writer lock with configurable fairness policy."""

    def __init__(self, data: T, policy: LockPolicy):
        self.data = data
        self.policy = policy
        self.lock = threading.Lock()
        self.read_condvar = threading.Condition(self.lock)
        self.write_condvar = threading.Condition(self.lock)
        self.readers = 0
        self.writers = 0
        self.waiting_readers = 0
        self.waiting_writers = 0

    def _can_read(self) -> bool:
        """
        TODO: Determine if a reader can acquire the lock based on policy.

        Returns:
            True if reader can acquire, False otherwise
        """
        pass  # TODO: Implement this

    def _can_write(self) -> bool:
        """
        TODO: Determine if a writer can acquire the lock.

        Writers need exclusive access (no readers, no other writers).

        Returns:
            True if writer can acquire, False otherwise
        """
        pass  # TODO: Implement this

    def read(self):
        """
        TODO: Acquire a read lock.

        The behavior depends on the policy:
        - ReadersPreference: Acquire if no writers
        - WritersPreference: Acquire if no writers and no waiting writers
        - Fair: Use a queue-like mechanism

        Returns:
            ReadGuard context manager
        """
        pass  # TODO: Implement this

    def write(self):
        """
        TODO: Acquire a write lock.

        Must wait until no readers and no other writers.

        Returns:
            WriteGuard context manager
        """
        pass  # TODO: Implement this

    def reader_count(self) -> int:
        """Get the number of active readers."""
        with self.lock:
            return self.readers

    def writer_count(self) -> int:
        """Get the number of active writers."""
        with self.lock:
            return self.writers

    def waiting_readers_count(self) -> int:
        """Get the number of waiting readers."""
        with self.lock:
            return self.waiting_readers

    def waiting_writers_count(self) -> int:
        """Get the number of waiting writers."""
        with self.lock:
            return self.waiting_writers


class ReadGuard(Generic[T]):
    """RAII-style guard for read access."""

    def __init__(self, rwlock: RwLock[T]):
        """
        TODO: Create a read guard.

        This should increment the reader count.

        Args:
            rwlock: The RwLock to guard
        """
        pass  # TODO: Implement this

    def __enter__(self):
        """Enter the context manager."""
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        TODO: Release the read lock.

        Decrement reader count and notify waiting writers.
        """
        pass  # TODO: Implement this


class WriteGuard(Generic[T]):
    """RAII-style guard for write access."""

    def __init__(self, rwlock: RwLock[T]):
        """
        TODO: Create a write guard.

        This should increment the writer count.

        Args:
            rwlock: The RwLock to guard
        """
        pass  # TODO: Implement this

    def __enter__(self):
        """Enter the context manager."""
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        TODO: Release the write lock.

        Decrement writer count and notify waiting readers/writers.
        """
        pass  # TODO: Implement this


class TestReaderWriter(unittest.TestCase):
    """Test cases for Reader-Writer Lock."""

    def test_single_reader(self):
        """Test single reader access."""
        lock = RwLock[int](42, LockPolicy.FAIR)
        guard = lock.read()
        with guard as data:
            self.assertEqual(data, 42)

    def test_single_writer(self):
        """Test single writer access."""
        lock = RwLock[int](42, LockPolicy.FAIR)
        guard = lock.write()
        with guard as data:
            data = 100  # Modify (in real implementation)
            self.assertEqual(data, 100)

    def test_multiple_readers(self):
        """Test multiple concurrent readers."""
        lock = RwLock[int](0, LockPolicy.READERS_PREFERENCE)
        results = []

        def reader():
            guard = lock.read()
            with guard as data:
                time.sleep(0.01)
                results.append(data)

        threads = []
        for _ in range(5):
            t = threading.Thread(target=reader)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # All readers should have run
        self.assertEqual(len(results), 5)

    def test_reader_writer_exclusion(self):
        """Test readers and writers are mutually exclusive."""
        lock = RwLock[int](0, LockPolicy.FAIR)
        results = []

        def writer():
            guard = lock.write()
            with guard as data:
                data = 1
                time.sleep(0.05)
                data = 2
                results.append(data)

        def reader():
            time.sleep(0.01)
            guard = lock.read()
            with guard as data:
                results.append(data)

        writer_thread = threading.Thread(target=writer)
        reader_thread = threading.Thread(target=reader)

        writer_thread.start()
        reader_thread.start()

        writer_thread.join()
        reader_thread.join()

        # Reader should see the final value after writer completes
        self.assertIn(2, results)

    def test_writers_preference(self):
        """Test writers preference policy."""
        lock = RwLock[int](0, LockPolicy.WRITERS_PREFERENCE)

        guard = lock.read()
        with guard:
            self.assertEqual(lock.reader_count(), 1)

        guard = lock.write()
        with guard:
            self.assertEqual(lock.writer_count(), 1)

        guard = lock.read()
        with guard:
            pass  # Should complete

    def test_readers_preference(self):
        """Test readers preference policy."""
        lock = RwLock[int](0, LockPolicy.READERS_PREFERENCE)

        def reader1():
            guard = lock.read()
            with guard:
                time.sleep(0.02)

        def writer():
            time.sleep(0.02)
            guard = lock.write()
            with guard:
                pass

        def reader2():
            time.sleep(0.01)
            guard = lock.read()
            with guard:
                pass

        r1 = threading.Thread(target=reader1)
        w = threading.Thread(target=writer)
        r2 = threading.Thread(target=reader2)

        r1.start()
        w.start()
        r2.start()

        r1.join()
        r2.join()
        w.join()

    def test_concurrent_readers(self):
        """Test multiple concurrent readers can access simultaneously."""
        lock = RwLock[list](list(range(5)), LockPolicy.FAIR)
        results = []

        def reader():
            guard = lock.read()
            with guard as data:
                total = sum(data)
                results.append(total)

        threads = []
        for _ in range(10):
            t = threading.Thread(target=reader)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # All readers should have seen the same data
        self.assertTrue(all(r == 10 for r in results))

    def test_sequential_writers(self):
        """Test writers execute sequentially."""
        lock = RwLock[int](0, LockPolicy.FAIR)
        results = []

        def writer(value):
            guard = lock.write()
            with guard:
                results.append(value)

        threads = []
        for i in range(5):
            t = threading.Thread(target=writer, args=(i,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # All writers should have executed
        self.assertEqual(len(results), 5)
        self.assertEqual(set(results), {0, 1, 2, 3, 4})

    def test_alternating_read_write(self):
        """Test alternating read and write operations."""
        lock = RwLock[int](0, LockPolicy.FAIR)

        for i in range(10):
            if i % 2 == 0:
                guard = lock.write()
                with guard:
                    pass  # Write operation
            else:
                guard = lock.read()
                with guard:
                    pass  # Read operation

    def test_fair_policy(self):
        """Test fair policy prevents starvation."""
        lock = RwLock[int](0, LockPolicy.FAIR)

        def reader():
            guard = lock.read()
            with guard:
                time.sleep(0.01)

        def writer():
            time.sleep(0.01)
            guard = lock.write()
            with guard:
                pass

        # Hold read lock
        r = threading.Thread(target=reader)
        r.start()

        # Writer waits
        w = threading.Thread(target=writer)
        w.start()

        time.sleep(0.02)

        r.join()
        w.join()

    def test_no_writer_starvation(self):
        """Test writers eventually execute with writers preference."""
        lock = RwLock[int](0, LockPolicy.WRITERS_PREFERENCE)
        results = []

        def writer():
            time.sleep(0.01)
            guard = lock.write()
            with guard:
                results.append(999)

        def reader():
            guard = lock.read()
            with guard:
                time.sleep(0.005)

        threads = []

        # Spawn a writer that should eventually execute
        w = threading.Thread(target=writer)
        w.start()
        threads.append(w)

        # Spawn many readers
        for _ in range(5):
            r = threading.Thread(target=reader)
            r.start()
            threads.append(r)

        for t in threads:
            t.join()

        # Writer should have executed
        self.assertIn(999, results)

    def test_reader_count(self):
        """Test reader count tracking."""
        lock = RwLock[int](42, LockPolicy.FAIR)

        self.assertEqual(lock.reader_count(), 0)

        guard1 = lock.read()
        with guard1:
            self.assertEqual(lock.reader_count(), 1)

            guard2 = lock.read()
            with guard2:
                self.assertEqual(lock.reader_count(), 2)

            self.assertEqual(lock.reader_count(), 1)

        self.assertEqual(lock.reader_count(), 0)

    def test_writer_count(self):
        """Test writer count tracking."""
        lock = RwLock[int](42, LockPolicy.FAIR)

        self.assertEqual(lock.writer_count(), 0)

        guard = lock.write()
        with guard:
            self.assertEqual(lock.writer_count(), 1)

        self.assertEqual(lock.writer_count(), 0)

    def test_stress_test(self):
        """Test with many concurrent readers and writers."""
        lock = RwLock[int](0, LockPolicy.FAIR)
        num_iterations = 100

        def reader():
            for _ in range(num_iterations):
                guard = lock.read()
                with guard:
                    time.sleep(0.00001)

        def writer():
            for _ in range(num_iterations):
                guard = lock.write()
                with guard:
                    time.sleep(0.00001)

        threads = []

        # Spawn readers
        for _ in range(10):
            t = threading.Thread(target=reader)
            t.start()
            threads.append(t)

        # Spawn writers
        for _ in range(5):
            t = threading.Thread(target=writer)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


if __name__ == '__main__':
    unittest.main()
