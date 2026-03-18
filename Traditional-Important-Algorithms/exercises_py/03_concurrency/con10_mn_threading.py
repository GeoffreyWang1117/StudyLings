# I AM NOT DONE

"""
con10_mn_threading.py

M:N Threading (hybrid threading) maps M user-level threads to N kernel threads.
This combines the efficiency of user-level threads with the parallelism of
kernel threads. The scheduler multiplexes many lightweight threads onto fewer
OS threads.

Your task: Implement an M:N thread scheduler.

Key concepts:
- User threads: Lightweight, managed by the runtime
- Kernel threads (workers): Heavy, managed by the OS
- Multiplexing: Many user threads share kernel threads
- Work stealing: Balance load across kernel threads
"""

from collections import deque
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
import unittest


ThreadId = int
WorkerId = int


class ThreadState(Enum):
    """User thread states."""
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"


@dataclass
class UserThread:
    """Represents a user-level thread."""
    id: ThreadId
    state: ThreadState
    remaining_work: int
    assigned_worker: Optional[WorkerId] = None

    def is_complete(self) -> bool:
        """Check if thread has completed."""
        return self.state == ThreadState.COMPLETED


class Worker:
    """Represents a kernel-level worker thread."""

    def __init__(self, worker_id: WorkerId):
        self.id = worker_id
        self.local_queue = deque()
        self.current_thread: Optional[ThreadId] = None
        self.total_execution_time = 0
        self.threads_completed = 0

    def enqueue(self, thread_id: ThreadId) -> None:
        """
        TODO: Add a thread to this worker's local queue.

        Args:
            thread_id: Thread to enqueue
        """
        pass  # TODO: Implement this

    def dequeue(self) -> Optional[ThreadId]:
        """
        TODO: Remove and return a thread from the local queue (LIFO).

        Returns:
            The thread ID, or None if empty
        """
        pass  # TODO: Implement this

    def steal(self) -> Optional[ThreadId]:
        """
        TODO: Steal a thread from the front of the queue (FIFO).

        Returns:
            The thread ID, or None if empty
        """
        pass  # TODO: Implement this

    def queue_len(self) -> int:
        """Get the queue length."""
        return len(self.local_queue)

    def is_idle(self) -> bool:
        """Check if worker is idle."""
        return self.current_thread is None and len(self.local_queue) == 0


class EventType(Enum):
    """Scheduler event types."""
    THREAD_STARTED = "thread_started"
    THREAD_COMPLETED = "thread_completed"
    THREAD_BLOCKED = "thread_blocked"
    THREAD_RESUMED = "thread_resumed"
    THREAD_STOLEN = "thread_stolen"


@dataclass
class SchedulerEvent:
    """Records scheduler events."""
    time: int
    event_type: EventType
    thread_id: Optional[ThreadId] = None
    worker_id: Optional[WorkerId] = None
    from_worker: Optional[WorkerId] = None
    to_worker: Optional[WorkerId] = None


class MNScheduler:
    """M:N threading scheduler."""

    def __init__(self, num_workers: int, quantum: int):
        self.threads: List[UserThread] = []
        self.workers = [Worker(i) for i in range(num_workers)]
        self.global_queue = deque()
        self.quantum = quantum
        self.current_time = 0
        self.events: List[SchedulerEvent] = []

    def spawn_thread(self, work_amount: int) -> ThreadId:
        """
        TODO: Create a new user thread.

        Steps:
        1. Create thread with unique ID
        2. Add to threads list
        3. Add to global queue
        4. Return thread ID

        Args:
            work_amount: Amount of work for the thread

        Returns:
            The thread ID
        """
        pass  # TODO: Implement this

    def _log_event(self, event_type: EventType, thread_id: Optional[ThreadId] = None,
                   worker_id: Optional[WorkerId] = None,
                   from_worker: Optional[WorkerId] = None,
                   to_worker: Optional[WorkerId] = None) -> None:
        """Log a scheduler event."""
        self.events.append(SchedulerEvent(self.current_time, event_type,
                                          thread_id, worker_id, from_worker, to_worker))

    def _find_steal_victim(self, thief_id: WorkerId) -> Optional[WorkerId]:
        """
        TODO: Find the best worker to steal from.

        Choose the worker with the most queued threads (excluding thief).

        Args:
            thief_id: ID of the worker trying to steal

        Returns:
            ID of victim worker, or None
        """
        pass  # TODO: Implement this

    def _try_steal(self, thief_id: WorkerId) -> Optional[ThreadId]:
        """
        TODO: Try to steal work for a worker.

        Steps:
        1. Find a victim worker
        2. Steal a thread from the victim
        3. Log the theft event
        4. Return the stolen thread ID

        Args:
            thief_id: ID of the worker trying to steal

        Returns:
            The stolen thread ID, or None
        """
        pass  # TODO: Implement this

    def _assign_work(self, worker_id: WorkerId) -> Optional[ThreadId]:
        """
        TODO: Assign work to a worker.

        Try in order:
        1. Worker's local queue
        2. Global queue
        3. Steal from another worker

        Args:
            worker_id: Worker to assign work to

        Returns:
            The thread ID assigned, or None
        """
        pass  # TODO: Implement this

    def execute_step(self, worker_id: WorkerId) -> bool:
        """
        TODO: Execute one step for a worker.

        Steps:
        1. If worker has no current thread, assign work
        2. If still no thread, return False (idle)
        3. Execute current thread for min(quantum, remaining_work)
        4. Update thread state and time
        5. Log events
        6. If thread completes or blocks, clear current_thread
        7. Return True if work was done

        Args:
            worker_id: Worker to execute step for

        Returns:
            True if work was done, False otherwise
        """
        pass  # TODO: Implement this

    def run_all(self) -> None:
        """Run all workers until all threads complete."""
        while True:
            any_work = False
            for worker_id in range(len(self.workers)):
                if self.execute_step(worker_id):
                    any_work = True
            if not any_work:
                break

    def get_thread(self, thread_id: ThreadId) -> Optional[UserThread]:
        """Get a thread by ID."""
        for thread in self.threads:
            if thread.id == thread_id:
                return thread
        return None

    def get_worker_stats(self, worker_id: WorkerId) -> dict:
        """Get statistics for a worker."""
        worker = self.workers[worker_id]
        return {
            'worker_id': worker.id,
            'threads_completed': worker.threads_completed,
            'total_execution_time': worker.total_execution_time,
            'current_queue_length': worker.queue_len(),
        }

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def get_events(self) -> List[SchedulerEvent]:
        """Get all logged events."""
        return self.events

    def all_complete(self) -> bool:
        """Check if all threads have completed."""
        return all(t.is_complete() for t in self.threads)


class TestMNScheduler(unittest.TestCase):
    """Test cases for M:N Scheduler."""

    def test_single_worker_single_thread(self):
        """Test single worker with single thread."""
        scheduler = MNScheduler(1, 10)
        scheduler.spawn_thread(20)

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())
        stats = scheduler.get_worker_stats(0)
        self.assertEqual(stats['threads_completed'], 1)

    def test_multiple_threads_single_worker(self):
        """Test multiple threads on single worker."""
        scheduler = MNScheduler(1, 5)
        scheduler.spawn_thread(10)
        scheduler.spawn_thread(10)
        scheduler.spawn_thread(10)

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())
        stats = scheduler.get_worker_stats(0)
        self.assertEqual(stats['threads_completed'], 3)

    def test_multiple_workers_load_balancing(self):
        """Test load balancing across multiple workers."""
        scheduler = MNScheduler(3, 10)

        # Spawn many threads
        for _ in range(9):
            scheduler.spawn_thread(10)

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())

        # Work should be distributed across workers
        stats0 = scheduler.get_worker_stats(0)
        stats1 = scheduler.get_worker_stats(1)
        stats2 = scheduler.get_worker_stats(2)

        self.assertGreater(stats0['threads_completed'], 0)
        self.assertGreater(stats1['threads_completed'], 0)
        self.assertGreater(stats2['threads_completed'], 0)

        total = (stats0['threads_completed'] + stats1['threads_completed'] +
                stats2['threads_completed'])
        self.assertEqual(total, 9)

    def test_work_stealing(self):
        """Test work stealing between workers."""
        scheduler = MNScheduler(2, 5)

        # Add all work to worker 0's queue
        for i in range(6):
            thread_id = scheduler.spawn_thread(10)
            # Manually assign to worker 0
            scheduler.workers[0].enqueue(thread_id)
        scheduler.global_queue.clear()  # Clear global queue

        scheduler.run_all()

        # Worker 1 should have stolen work
        events = scheduler.get_events()
        steals = [e for e in events if e.event_type == EventType.THREAD_STOLEN]

        self.assertGreater(len(steals), 0, "Work stealing should have occurred")

    def test_quantum_enforcement(self):
        """Test quantum is enforced."""
        scheduler = MNScheduler(1, 5)
        scheduler.spawn_thread(20)

        # Execute one step
        scheduler.execute_step(0)

        thread = scheduler.get_thread(0)
        # Should have executed for quantum (5) time units
        self.assertEqual(thread.remaining_work, 15)

    def test_thread_completion(self):
        """Test thread completion."""
        scheduler = MNScheduler(1, 10)
        thread_id = scheduler.spawn_thread(5)

        scheduler.run_all()

        thread = scheduler.get_thread(thread_id)
        self.assertEqual(thread.state, ThreadState.COMPLETED)
        self.assertEqual(thread.remaining_work, 0)

    def test_event_logging(self):
        """Test events are logged."""
        scheduler = MNScheduler(1, 10)
        scheduler.spawn_thread(5)

        scheduler.run_all()

        events = scheduler.get_events()
        self.assertTrue(any(e.event_type == EventType.THREAD_STARTED for e in events))
        self.assertTrue(any(e.event_type == EventType.THREAD_COMPLETED for e in events))

    def test_worker_utilization(self):
        """Test worker utilization."""
        scheduler = MNScheduler(2, 10)

        for _ in range(4):
            scheduler.spawn_thread(20)

        scheduler.run_all()

        stats0 = scheduler.get_worker_stats(0)
        stats1 = scheduler.get_worker_stats(1)

        # Both workers should have done work
        self.assertGreater(stats0['total_execution_time'], 0)
        self.assertGreater(stats1['total_execution_time'], 0)

    def test_varying_work_amounts(self):
        """Test with varying work amounts."""
        scheduler = MNScheduler(2, 10)

        scheduler.spawn_thread(5)
        scheduler.spawn_thread(50)
        scheduler.spawn_thread(15)
        scheduler.spawn_thread(30)

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())

        total_completed = sum(w.threads_completed for w in scheduler.workers)
        self.assertEqual(total_completed, 4)

    def test_empty_scheduler(self):
        """Test empty scheduler."""
        scheduler = MNScheduler(2, 10)

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())
        self.assertEqual(scheduler.current_time_value(), 0)


if __name__ == '__main__':
    unittest.main()
