# I AM NOT DONE

"""
con01_round_robin.py

Round Robin Scheduling is a preemptive scheduling algorithm where each task
gets a fixed time slice (quantum) to execute. When a task's quantum expires,
it moves to the back of the queue, and the next task gets to run.

Your task: Implement a round robin scheduler that manages task execution.

Key concepts:
- Time quantum: Fixed time slice for each task
- Queue-based: Tasks wait in a FIFO queue
- Fair: Each task gets equal CPU time
"""

from collections import deque
from typing import List, Tuple, Optional
import unittest


class Task:
    """Represents a task with an ID and remaining execution time."""

    def __init__(self, task_id: int, execution_time: int):
        self.id = task_id
        self.remaining_time = execution_time

    def is_complete(self) -> bool:
        """Check if the task has completed execution."""
        return self.remaining_time == 0


class RoundRobinScheduler:
    """Round Robin Scheduler implementation."""

    def __init__(self, quantum: int):
        self.queue = deque()
        self.quantum = quantum
        self.current_time = 0

    def add_task(self, task: Task) -> None:
        """
        TODO: Add a task to the ready queue.

        Args:
            task: The task to add to the queue
        """
        pass  # TODO: Implement this

    def run_next(self) -> Optional[int]:
        """
        TODO: Run the next task for one quantum (or until completion).

        Steps:
        1. Remove the task from the front of the queue
        2. Execute it for min(quantum, remaining_time)
        3. Update current_time
        4. If the task isn't complete, add it back to the queue
        5. Return the ID of the task that just ran (or None if queue is empty)

        Returns:
            The task ID that ran, or None if no tasks in queue
        """
        pass  # TODO: Implement this

    def run_all(self) -> List[Tuple[int, int, int]]:
        """
        TODO: Run all tasks until completion.

        Returns:
            A list of tuples (task_id, start_time, end_time) for each execution slice
        """
        pass  # TODO: Implement this

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time


class TestRoundRobin(unittest.TestCase):
    """Test cases for Round Robin Scheduler."""

    def test_single_task(self):
        """Test with a single task that completes within quantum."""
        scheduler = RoundRobinScheduler(10)
        scheduler.add_task(Task(1, 5))

        task_id = scheduler.run_next()
        self.assertEqual(task_id, 1)
        self.assertEqual(scheduler.current_time_value(), 5)
        self.assertTrue(scheduler.is_empty())

    def test_multiple_tasks_within_quantum(self):
        """Test multiple tasks that complete within their quantum."""
        scheduler = RoundRobinScheduler(10)
        scheduler.add_task(Task(1, 5))
        scheduler.add_task(Task(2, 8))
        scheduler.add_task(Task(3, 3))

        scheduler.run_next()  # Task 1: 0-5
        scheduler.run_next()  # Task 2: 5-13
        scheduler.run_next()  # Task 3: 13-16

        self.assertEqual(scheduler.current_time_value(), 16)
        self.assertTrue(scheduler.is_empty())

    def test_task_exceeds_quantum(self):
        """Test a task that takes longer than the quantum."""
        scheduler = RoundRobinScheduler(5)
        scheduler.add_task(Task(1, 12))

        scheduler.run_next()  # 0-5, task goes back to queue
        self.assertFalse(scheduler.is_empty())
        self.assertEqual(scheduler.current_time_value(), 5)

        scheduler.run_next()  # 5-10, task goes back to queue
        self.assertFalse(scheduler.is_empty())
        self.assertEqual(scheduler.current_time_value(), 10)

        scheduler.run_next()  # 10-12, task completes
        self.assertTrue(scheduler.is_empty())
        self.assertEqual(scheduler.current_time_value(), 12)

    def test_interleaved_execution(self):
        """Test that tasks alternate execution."""
        scheduler = RoundRobinScheduler(4)
        scheduler.add_task(Task(1, 10))
        scheduler.add_task(Task(2, 10))

        execution_log = scheduler.run_all()

        # Should alternate between tasks
        self.assertEqual(len(execution_log), 6)  # 3 slices per task
        self.assertEqual(execution_log[0][0], 1)  # Task 1: 0-4
        self.assertEqual(execution_log[1][0], 2)  # Task 2: 4-8
        self.assertEqual(execution_log[2][0], 1)  # Task 1: 8-12
        self.assertEqual(execution_log[3][0], 2)  # Task 2: 12-16
        self.assertEqual(execution_log[4][0], 1)  # Task 1: 16-18
        self.assertEqual(execution_log[5][0], 2)  # Task 2: 18-20

    def test_varying_arrival_times(self):
        """Test tasks added at different times."""
        scheduler = RoundRobinScheduler(3)
        scheduler.add_task(Task(1, 7))

        scheduler.run_next()  # Task 1: 0-3

        scheduler.add_task(Task(2, 5))
        scheduler.run_next()  # Task 2: 3-6
        scheduler.run_next()  # Task 1: 6-9
        scheduler.run_next()  # Task 2: 9-11
        scheduler.run_next()  # Task 1: 11-12

        self.assertTrue(scheduler.is_empty())
        self.assertEqual(scheduler.current_time_value(), 12)

    def test_zero_execution_time(self):
        """Test edge case with zero execution time."""
        scheduler = RoundRobinScheduler(5)
        scheduler.add_task(Task(1, 0))

        task_id = scheduler.run_next()
        self.assertEqual(task_id, 1)
        self.assertEqual(scheduler.current_time_value(), 0)

    def test_large_quantum(self):
        """Test with quantum larger than all task times."""
        scheduler = RoundRobinScheduler(100)
        scheduler.add_task(Task(1, 10))
        scheduler.add_task(Task(2, 15))
        scheduler.add_task(Task(3, 8))

        execution_log = scheduler.run_all()

        # All tasks should complete in one quantum each
        self.assertEqual(len(execution_log), 3)

    def test_quantum_of_one(self):
        """Test with minimum quantum of 1."""
        scheduler = RoundRobinScheduler(1)
        scheduler.add_task(Task(1, 3))
        scheduler.add_task(Task(2, 3))

        execution_log = scheduler.run_all()

        # Should alternate every time unit
        self.assertEqual(len(execution_log), 6)

    def test_empty_scheduler(self):
        """Test running empty scheduler."""
        scheduler = RoundRobinScheduler(5)

        result = scheduler.run_next()
        self.assertIsNone(result)
        self.assertTrue(scheduler.is_empty())

    def test_many_tasks(self):
        """Test with many tasks."""
        scheduler = RoundRobinScheduler(5)
        for i in range(10):
            scheduler.add_task(Task(i, 15))

        execution_log = scheduler.run_all()

        # Each task needs 3 slices (15 / 5)
        self.assertEqual(len(execution_log), 30)
        self.assertTrue(scheduler.is_empty())

    def test_mixed_execution_times(self):
        """Test with tasks of varying execution times."""
        scheduler = RoundRobinScheduler(4)
        scheduler.add_task(Task(1, 2))   # Completes in 1 slice
        scheduler.add_task(Task(2, 10))  # Needs 3 slices
        scheduler.add_task(Task(3, 5))   # Needs 2 slices

        execution_log = scheduler.run_all()

        self.assertEqual(len(execution_log), 6)
        self.assertEqual(scheduler.current_time_value(), 17)


if __name__ == '__main__':
    unittest.main()
