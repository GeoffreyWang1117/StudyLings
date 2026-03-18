# I AM NOT DONE

"""
os08_producer_consumer.py

The Producer-Consumer problem is a classic synchronization problem where producers
generate data and place it in a buffer, while consumers remove data from the buffer.
The challenge is to ensure that producers don't add data to a full buffer and
consumers don't remove data from an empty buffer.

Your task: Implement a thread-safe bounded buffer for the producer-consumer problem.
"""

import threading
from collections import deque
from typing import Generic, TypeVar, Optional
import unittest
import time


T = TypeVar('T')


class BoundedBuffer(Generic[T]):
    """Thread-safe bounded buffer for producer-consumer problem."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = deque()
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def produce(self, item: T) -> None:
        """
        TODO: Add an item to the buffer.

        Steps:
        1. Acquire the lock
        2. Wait while buffer is full (use not_full condition)
        3. Add item to buffer
        4. Notify waiting consumers (use not_empty condition)

        Args:
            item: Item to add to buffer
        """
        pass  # TODO: Implement this

    def consume(self) -> T:
        """
        TODO: Remove and return an item from the buffer.

        Steps:
        1. Acquire the lock
        2. Wait while buffer is empty (use not_empty condition)
        3. Remove item from buffer
        4. Notify waiting producers (use not_full condition)

        Returns:
            The consumed item
        """
        pass  # TODO: Implement this

    def try_produce(self, item: T) -> bool:
        """
        TODO: Try to add an item without blocking.

        Args:
            item: Item to add

        Returns:
            True if successful, False if buffer is full
        """
        pass  # TODO: Implement this

    def try_consume(self) -> Optional[T]:
        """
        TODO: Try to remove an item without blocking.

        Returns:
            The consumed item, or None if buffer is empty
        """
        pass  # TODO: Implement this

    def __len__(self) -> int:
        """
        TODO: Return current number of items in buffer.

        Returns:
            Number of items in buffer
        """
        pass  # TODO: Implement this

    def is_empty(self) -> bool:
        """
        TODO: Check if buffer is empty.

        Returns:
            True if empty, False otherwise
        """
        pass  # TODO: Implement this

    def is_full(self) -> bool:
        """
        TODO: Check if buffer is full.

        Returns:
            True if full, False otherwise
        """
        pass  # TODO: Implement this

    def get_capacity(self) -> int:
        """Get the buffer capacity."""
        return self.capacity


class MPMCQueue(Generic[T]):
    """Multi-producer, multi-consumer queue."""

    def __init__(self, capacity: int):
        self.buffer = BoundedBuffer[T](capacity)

    def send(self, item: T) -> None:
        """Send an item to the queue."""
        self.buffer.produce(item)

    def recv(self) -> T:
        """Receive an item from the queue."""
        return self.buffer.consume()

    def try_send(self, item: T) -> bool:
        """Try to send an item without blocking."""
        return self.buffer.try_produce(item)

    def try_recv(self) -> Optional[T]:
        """Try to receive an item without blocking."""
        return self.buffer.try_consume()

    def __len__(self) -> int:
        """Get the number of items in queue."""
        return len(self.buffer)

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.buffer.is_empty()


class TestProducerConsumer(unittest.TestCase):
    """Test cases for Producer-Consumer."""

    def test_basic_produce_consume(self):
        """Test basic produce and consume operations."""
        buffer = BoundedBuffer[int](5)

        buffer.produce(1)
        buffer.produce(2)
        buffer.produce(3)

        self.assertEqual(buffer.consume(), 1)
        self.assertEqual(buffer.consume(), 2)
        self.assertEqual(buffer.consume(), 3)

    def test_fifo_order(self):
        """Test FIFO ordering."""
        buffer = BoundedBuffer[str](3)

        buffer.produce("first")
        buffer.produce("second")
        buffer.produce("third")

        self.assertEqual(buffer.consume(), "first")
        self.assertEqual(buffer.consume(), "second")
        self.assertEqual(buffer.consume(), "third")

    def test_buffer_capacity(self):
        """Test buffer capacity limits."""
        buffer = BoundedBuffer[int](2)

        buffer.produce(1)
        buffer.produce(2)

        self.assertEqual(len(buffer), 2)
        self.assertTrue(buffer.is_full())

    def test_try_produce_full(self):
        """Test try_produce on full buffer."""
        buffer = BoundedBuffer[int](1)

        self.assertTrue(buffer.try_produce(1))
        self.assertFalse(buffer.try_produce(2))

    def test_try_consume_empty(self):
        """Test try_consume on empty buffer."""
        buffer = BoundedBuffer[int](5)

        self.assertTrue(buffer.is_empty())
        self.assertIsNone(buffer.try_consume())

    def test_single_producer_single_consumer(self):
        """Test with single producer and consumer threads."""
        buffer = BoundedBuffer[int](10)
        results = []

        def producer():
            for i in range(20):
                buffer.produce(i)

        def consumer():
            for _ in range(20):
                results.append(buffer.consume())

        prod_thread = threading.Thread(target=producer)
        cons_thread = threading.Thread(target=consumer)

        prod_thread.start()
        cons_thread.start()

        prod_thread.join()
        cons_thread.join()

        self.assertEqual(sum(results), sum(range(20)))

    def test_multiple_producers(self):
        """Test with multiple producer threads."""
        buffer = BoundedBuffer[int](50)

        def producer(start_val):
            for j in range(10):
                buffer.produce(start_val * 10 + j)

        threads = []
        for i in range(3):
            t = threading.Thread(target=producer, args=(i,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEqual(len(buffer), 30)

    def test_multiple_consumers(self):
        """Test with multiple consumer threads."""
        buffer = BoundedBuffer[int](50)
        results = []
        lock = threading.Lock()

        # Fill buffer
        for i in range(30):
            buffer.produce(i)

        def consumer():
            local_results = []
            for _ in range(10):
                local_results.append(buffer.consume())
            with lock:
                results.extend(local_results)

        threads = []
        for _ in range(3):
            t = threading.Thread(target=consumer)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEqual(sum(results), sum(range(30)))

    def test_mpmc_queue(self):
        """Test MPMC queue wrapper."""
        queue = MPMCQueue[int](10)

        queue.send(1)
        queue.send(2)
        queue.send(3)

        self.assertEqual(queue.recv(), 1)
        self.assertEqual(queue.recv(), 2)
        self.assertEqual(queue.recv(), 3)

    def test_mpmc_concurrent(self):
        """Test MPMC with concurrent producers and consumers."""
        queue = MPMCQueue[int](20)
        num_items = 30

        def producer(start):
            for j in range(10):
                queue.send(start * 100 + j)
                time.sleep(0.0001)

        def consumer():
            count = 0
            for _ in range(10):
                queue.recv()
                count += 1
                time.sleep(0.0001)
            return count

        threads = []

        # Spawn producers
        for i in range(3):
            t = threading.Thread(target=producer, args=(i,))
            t.start()
            threads.append(t)

        # Spawn consumers
        for _ in range(3):
            t = threading.Thread(target=consumer)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertTrue(queue.is_empty())

    def test_producer_blocks_on_full(self):
        """Test producer blocks when buffer is full."""
        buffer = BoundedBuffer[int](2)

        buffer.produce(1)
        buffer.produce(2)

        def delayed_consumer():
            time.sleep(0.05)
            buffer.consume()

        consumer_thread = threading.Thread(target=delayed_consumer)
        consumer_thread.start()

        # This should block until consumer removes an item
        buffer.produce(3)

        consumer_thread.join()
        self.assertLessEqual(len(buffer), 2)

    def test_consumer_blocks_on_empty(self):
        """Test consumer blocks when buffer is empty."""
        buffer = BoundedBuffer[int](5)

        def delayed_producer():
            time.sleep(0.05)
            buffer.produce(42)

        producer_thread = threading.Thread(target=delayed_producer)
        producer_thread.start()

        # This should block until producer adds an item
        value = buffer.consume()

        producer_thread.join()
        self.assertEqual(value, 42)

    def test_stress_test(self):
        """Test with many items."""
        buffer = BoundedBuffer[int](10)
        num_items = 1000
        results = []
        lock = threading.Lock()

        def producer():
            for i in range(num_items):
                buffer.produce(i)

        def consumer():
            local_results = []
            for _ in range(num_items):
                local_results.append(buffer.consume())
            with lock:
                results.extend(local_results)

        prod_thread = threading.Thread(target=producer)
        cons_thread = threading.Thread(target=consumer)

        prod_thread.start()
        cons_thread.start()

        prod_thread.join()
        cons_thread.join()

        self.assertEqual(sum(results), sum(range(num_items)))


if __name__ == '__main__':
    unittest.main()
