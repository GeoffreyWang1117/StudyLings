# I AM NOT DONE

"""
con06_work_stealing.py

Work Stealing is a scheduling strategy where idle workers steal work from
busy workers' queues. Each worker has its own deque (double-ended queue)
where it pushes/pops tasks from one end, while other workers can steal
from the other end.

Your task: Implement a work-stealing scheduler with multiple workers.

Key concepts:
- Per-worker work queues (deques)
- LIFO for local operations, FIFO for stealing
- Load balancing through theft
- Reduced contention compared to global queue
"""

from collections import deque
from typing import List, Tuple, Optional
from dataclasses import dataclass
import unittest


@dataclass
class Task:
    """Represents a task with execution time."""
    id: int
    execution_time: int


class WorkerQueue:
    """Worker's task queue with stealing support."""

    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.deque = deque()
        self.total_executed = 0
        self.tasks_completed = 0
        self.tasks_stolen = 0
        self.tasks_stolen_from_me = 0

    def push(self, task: Task) -> None:
        """
        TODO: Push task to the back of the deque (LIFO for local operations).

        Args:
            task: The task to push
        """
        pass  # TODO: Implement this

    def pop(self) -> Optional[Task]:
        """
        TODO: Pop task from the back of the deque (LIFO for local operations).

        Returns:
            The popped task, or None if empty
        """
        pass  # TODO: Implement this

    def steal(self) -> Optional[Task]:
        """
        TODO: Steal task from the front of the deque (FIFO for stealing).

        Increment tasks_stolen_from_me counter.

        Returns:
            The stolen task, or None if empty
        """
        pass  # TODO: Implement this

    def __len__(self) -> int:
        """Get the number of tasks in the queue."""
        return len(self.deque)

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.deque) == 0


class WorkStealingScheduler:
    """Work-stealing scheduler with multiple workers."""

    def __init__(self, num_workers: int):
        self.workers = [WorkerQueue(i) for i in range(num_workers)]
        self.current_time = 0

    def submit_task(self, worker_id: int, task: Task) -> None:
        """
        TODO: Submit a task to a specific worker's queue.

        Args:
            worker_id: Worker to submit to
            task: The task to submit
        """
        pass  # TODO: Implement this

    def submit_tasks(self, worker_id: int, tasks: List[Task]) -> None:
        """Submit multiple tasks to a worker."""
        for task in tasks:
            self.submit_task(worker_id, task)

    def _find_victim(self, thief_id: int) -> Optional[int]:
        """
        TODO: Find a worker to steal from.

        Strategy: Find the worker with the most tasks (excluding the thief).

        Args:
            thief_id: ID of the worker trying to steal

        Returns:
            ID of the victim worker, or None if no suitable victim
        """
        pass  # TODO: Implement this

    def _try_steal(self, thief_id: int) -> Optional[Task]:
        """
        TODO: Try to steal a task for the given worker.

        Steps:
        1. Find a victim using _find_victim
        2. Steal from the victim's queue
        3. Update thief's stolen counter
        4. Return the stolen task

        Args:
            thief_id: ID of the worker trying to steal

        Returns:
            The stolen task, or None if no task could be stolen
        """
        pass  # TODO: Implement this

    def execute_step(self, worker_id: int) -> Optional[int]:
        """
        TODO: Execute one step for a worker.

        Steps:
        1. Try to pop a task from worker's own queue
        2. If queue is empty, try to steal from another worker
        3. If got a task, "execute" it (update counters and time)
        4. Return the task ID that was executed (or None)

        Args:
            worker_id: ID of the worker

        Returns:
            The task ID executed, or None
        """
        pass  # TODO: Implement this

    def run_until_complete(self) -> List[Tuple[int, int]]:
        """
        TODO: Run all workers until all tasks are complete.

        Use round-robin among workers.

        Returns:
            A list of tuples (worker_id, task_id) showing execution
        """
        pass  # TODO: Implement this

    def get_worker_stats(self, worker_id: int) -> dict:
        """Get statistics for a worker."""
        worker = self.workers[worker_id]
        return {
            'worker_id': worker.worker_id,
            'tasks_completed': worker.tasks_completed,
            'total_execution_time': worker.total_executed,
            'tasks_stolen': worker.tasks_stolen,
            'tasks_stolen_from_me': worker.tasks_stolen_from_me,
        }

    def is_complete(self) -> bool:
        """Check if all workers are done."""
        return all(w.is_empty() for w in self.workers)

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time


class TestWorkStealingScheduler(unittest.TestCase):
    """Test cases for Work Stealing Scheduler."""

    def test_single_worker_single_task(self):
        """Test single worker with single task."""
        scheduler = WorkStealingScheduler(1)
        scheduler.submit_task(0, Task(1, 10))

        result = scheduler.execute_step(0)
        self.assertEqual(result, 1)
        self.assertTrue(scheduler.is_complete())

    def test_lifo_local_execution(self):
        """Test LIFO order for local execution."""
        scheduler = WorkStealingScheduler(1)
        scheduler.submit_task(0, Task(1, 5))
        scheduler.submit_task(0, Task(2, 5))
        scheduler.submit_task(0, Task(3, 5))

        # Should execute in LIFO order (3, 2, 1)
        self.assertEqual(scheduler.execute_step(0), 3)
        self.assertEqual(scheduler.execute_step(0), 2)
        self.assertEqual(scheduler.execute_step(0), 1)

    def test_work_stealing_basic(self):
        """Test basic work stealing."""
        scheduler = WorkStealingScheduler(2)

        # Load all tasks on worker 0
        scheduler.submit_task(0, Task(1, 5))
        scheduler.submit_task(0, Task(2, 5))
        scheduler.submit_task(0, Task(3, 5))

        # Worker 1 should steal from worker 0
        result = scheduler.execute_step(1)
        self.assertIsNotNone(result)

        stats = scheduler.get_worker_stats(1)
        self.assertEqual(stats['tasks_stolen'], 1)

        stats = scheduler.get_worker_stats(0)
        self.assertEqual(stats['tasks_stolen_from_me'], 1)

    def test_fifo_stealing(self):
        """Test FIFO order for stealing."""
        scheduler = WorkStealingScheduler(2)

        # Add tasks to worker 0 in order: 1, 2, 3
        scheduler.submit_task(0, Task(1, 5))
        scheduler.submit_task(0, Task(2, 5))
        scheduler.submit_task(0, Task(3, 5))

        # Worker 1 steals - should get task 1 (FIFO)
        stolen = scheduler.execute_step(1)
        self.assertEqual(stolen, 1)

        # Worker 0 executes - should get task 3 (LIFO)
        local = scheduler.execute_step(0)
        self.assertEqual(local, 3)

    def test_load_balancing(self):
        """Test load balancing across workers."""
        scheduler = WorkStealingScheduler(3)

        # Give worker 0 many tasks
        for i in range(10):
            scheduler.submit_task(0, Task(i, 5))

        scheduler.run_until_complete()

        # All workers should have done some work
        stats0 = scheduler.get_worker_stats(0)
        stats1 = scheduler.get_worker_stats(1)
        stats2 = scheduler.get_worker_stats(2)

        self.assertGreater(stats0['tasks_completed'], 0)
        self.assertGreater(stats1['tasks_completed'], 0)
        self.assertGreater(stats2['tasks_completed'], 0)

        # Total should be 10
        total = (stats0['tasks_completed'] + stats1['tasks_completed'] +
                stats2['tasks_completed'])
        self.assertEqual(total, 10)

    def test_no_stealing_when_balanced(self):
        """Test no stealing occurs when work is balanced."""
        scheduler = WorkStealingScheduler(2)

        scheduler.submit_task(0, Task(1, 5))
        scheduler.submit_task(1, Task(2, 5))

        scheduler.run_until_complete()

        # No stealing should occur since work is balanced
        stats0 = scheduler.get_worker_stats(0)
        stats1 = scheduler.get_worker_stats(1)

        self.assertEqual(stats0['tasks_stolen'], 0)
        self.assertEqual(stats1['tasks_stolen'], 0)

    def test_steal_from_busiest(self):
        """Test stealing from the busiest worker."""
        scheduler = WorkStealingScheduler(3)

        scheduler.submit_task(0, Task(1, 5))
        scheduler.submit_task(1, Task(2, 5))
        scheduler.submit_task(1, Task(3, 5))
        scheduler.submit_task(1, Task(4, 5))
        scheduler.submit_task(1, Task(5, 5))

        # Worker 2 should steal from worker 1 (busiest)
        scheduler.execute_step(2)

        stats1 = scheduler.get_worker_stats(1)
        self.assertEqual(stats1['tasks_stolen_from_me'], 1)

    def test_execution_time_tracking(self):
        """Test execution time is tracked correctly."""
        scheduler = WorkStealingScheduler(2)

        scheduler.submit_task(0, Task(1, 10))
        scheduler.submit_task(0, Task(2, 15))

        scheduler.run_until_complete()

        total_time = scheduler.current_time_value()
        self.assertGreaterEqual(total_time, 25)  # At least the sum of execution times

    def test_empty_worker(self):
        """Test worker with no tasks."""
        scheduler = WorkStealingScheduler(2)

        result = scheduler.execute_step(0)
        self.assertIsNone(result)

    def test_all_workers_empty(self):
        """Test when all workers are empty."""
        scheduler = WorkStealingScheduler(3)

        for i in range(3):
            result = scheduler.execute_step(i)
            self.assertIsNone(result)

        self.assertTrue(scheduler.is_complete())


if __name__ == '__main__':
    unittest.main()
