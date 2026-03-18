# I AM NOT DONE

"""
con03_mlfq.py

Multi-Level Feedback Queue (MLFQ) is an advanced scheduling algorithm that
uses multiple priority queues. Tasks start at the highest priority and move
to lower priorities if they use their full quantum. This favors I/O-bound
and interactive tasks while still completing CPU-bound tasks.

Your task: Implement a multi-level feedback queue scheduler.

Key concepts:
- Multiple queues with different priorities
- Dynamic priority adjustment based on behavior
- Quantum increases at lower priority levels
"""

from collections import deque
from typing import List, Tuple, Optional
import unittest


class Task:
    """Represents a task in the MLFQ system."""

    def __init__(self, task_id: int, execution_time: int):
        self.id = task_id
        self.remaining_time = execution_time
        self.priority_level = 0  # Start at highest priority

    def is_complete(self) -> bool:
        """Check if task has completed execution."""
        return self.remaining_time == 0


class MLFQ:
    """Multi-Level Feedback Queue Scheduler."""

    def __init__(self, num_levels: int, base_quantum: int, boost_interval: int):
        """
        Initialize MLFQ with multiple priority queues.

        Args:
            num_levels: Number of priority levels
            base_quantum: Base quantum for highest priority level
            boost_interval: Time interval for priority boosting
        """
        self.queues = [deque() for _ in range(num_levels)]
        self.quantums = [base_quantum * (2 ** i) for i in range(num_levels)]
        self.current_time = 0
        self.boost_interval = boost_interval
        self.time_since_boost = 0

    def add_task(self, task: Task) -> None:
        """
        TODO: Add a task to the appropriate queue based on its priority level.

        Args:
            task: The task to add
        """
        pass  # TODO: Implement this

    def _boost_all_tasks(self) -> None:
        """
        TODO: Move all tasks to the highest priority queue.

        This prevents starvation of long-running tasks.
        """
        pass  # TODO: Implement this

    def _find_next_task(self) -> Optional[Task]:
        """
        TODO: Find the next task to run from the highest non-empty queue.

        Returns:
            The next task to run, or None if all queues are empty
        """
        pass  # TODO: Implement this

    def run_next(self) -> Optional[Tuple[int, int, int]]:
        """
        TODO: Run the next task.

        Steps:
        1. Check if it's time for a priority boost
        2. Find the next task from the highest priority queue
        3. Get the quantum for that priority level
        4. Execute for min(quantum, remaining_time)
        5. If the task used its full quantum AND isn't complete, demote it
        6. If the task didn't use full quantum, keep it at same priority
        7. Update current_time and time_since_boost
        8. Return (task_id, priority_level, time_executed)

        Returns:
            Tuple of (task_id, priority_level, time_executed) or None
        """
        pass  # TODO: Implement this

    def run_all(self) -> List[Tuple[int, int, int]]:
        """
        TODO: Run all tasks until completion.

        Returns:
            A list of tuples (task_id, priority_level, time_slice) for each execution
        """
        pass  # TODO: Implement this

    def is_empty(self) -> bool:
        """Check if all queues are empty."""
        return all(len(q) == 0 for q in self.queues)

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def queue_lengths(self) -> List[int]:
        """Get the length of each queue."""
        return [len(q) for q in self.queues]


class TestMLFQ(unittest.TestCase):
    """Test cases for Multi-Level Feedback Queue."""

    def test_single_task(self):
        """Test with a single task."""
        mlfq = MLFQ(3, 4, 100)
        mlfq.add_task(Task(1, 10))

        result = mlfq.run_next()
        self.assertEqual(result, (1, 0, 4))  # Run for quantum at level 0

        result = mlfq.run_next()
        self.assertEqual(result, (1, 1, 6))  # Demoted to level 1, runs for remaining time

    def test_task_demotion(self):
        """Test that tasks are demoted after using full quantum."""
        mlfq = MLFQ(3, 2, 100)
        mlfq.add_task(Task(1, 20))

        # Task should be demoted after using full quantum
        mlfq.run_next()  # Level 0, quantum 2
        self.assertEqual(mlfq.queue_lengths(), [0, 1, 0])

        mlfq.run_next()  # Level 1, quantum 4
        self.assertEqual(mlfq.queue_lengths(), [0, 0, 1])

        mlfq.run_next()  # Level 2, quantum 8
        self.assertEqual(mlfq.queue_lengths(), [0, 0, 1])  # Stays at lowest level

    def test_io_bound_task(self):
        """Test I/O-bound task (short CPU bursts) stays at high priority."""
        mlfq = MLFQ(3, 10, 100)

        # Simulate I/O-bound task (short CPU burst)
        mlfq.add_task(Task(1, 3))

        result = mlfq.run_next()
        # Should complete in first quantum without demotion
        self.assertEqual(result, (1, 0, 3))
        self.assertTrue(mlfq.is_empty())

    def test_mixed_tasks(self):
        """Test mix of CPU-bound and I/O-bound tasks."""
        mlfq = MLFQ(3, 4, 100)

        mlfq.add_task(Task(1, 20))  # CPU-bound
        mlfq.add_task(Task(2, 3))   # I/O-bound

        # I/O-bound task should stay at high priority
        executions = []
        while not mlfq.is_empty():
            result = mlfq.run_next()
            if result:
                executions.append((result[0], result[1]))

        # Task 2 should appear at high priority levels
        task2_levels = [level for tid, level in executions if tid == 2]
        self.assertTrue(any(level == 0 for level in task2_levels))

    def test_priority_boost(self):
        """Test priority boost mechanism."""
        mlfq = MLFQ(3, 5, 20)

        mlfq.add_task(Task(1, 50))

        # Run for a while, task will be demoted
        for _ in range(3):
            mlfq.run_next()

        # Should be at low priority now
        self.assertTrue(mlfq.queue_lengths()[2] > 0 or mlfq.is_empty())

        # Continue running until boost
        if not mlfq.is_empty():
            initial_time = mlfq.current_time_value()
            while mlfq.current_time_value() - initial_time < 20 and not mlfq.is_empty():
                mlfq.run_next()

            # After boost, tasks should be at high priority
            if not mlfq.is_empty():
                self.assertTrue(mlfq.queue_lengths()[0] > 0)

    def test_round_robin_within_level(self):
        """Test round-robin behavior within a priority level."""
        mlfq = MLFQ(2, 3, 100)

        mlfq.add_task(Task(1, 3))
        mlfq.add_task(Task(2, 3))
        mlfq.add_task(Task(3, 3))

        executions = mlfq.run_all()

        # All tasks should complete at level 0 (I/O-bound behavior)
        self.assertEqual(len(executions), 3)
        self.assertTrue(all(level == 0 for _, level, _ in executions))

    def test_quantum_doubling(self):
        """Test that quantum doubles at each level."""
        mlfq = MLFQ(4, 2, 100)

        self.assertEqual(mlfq.quantums, [2, 4, 8, 16])

    def test_empty_mlfq(self):
        """Test running empty MLFQ."""
        mlfq = MLFQ(3, 5, 100)

        result = mlfq.run_next()
        self.assertIsNone(result)
        self.assertTrue(mlfq.is_empty())

    def test_single_level_mlfq(self):
        """Test MLFQ with single level (degrades to round-robin)."""
        mlfq = MLFQ(1, 5, 100)
        mlfq.add_task(Task(1, 10))
        mlfq.add_task(Task(2, 10))

        executions = mlfq.run_all()

        # Should behave like round-robin at level 0
        self.assertTrue(all(level == 0 for _, level, _ in executions))

    def test_large_boost_interval(self):
        """Test with very large boost interval (no boosting occurs)."""
        mlfq = MLFQ(3, 4, 10000)
        mlfq.add_task(Task(1, 30))

        executions = mlfq.run_all()

        # Task should go through all levels without boost
        levels_visited = set(level for _, level, _ in executions)
        self.assertIn(0, levels_visited)  # Started at level 0

    def test_zero_boost_interval(self):
        """Test with zero boost interval (constant boosting)."""
        mlfq = MLFQ(3, 4, 0)
        mlfq.add_task(Task(1, 20))

        executions = mlfq.run_all()

        # All executions should be at level 0 due to constant boosting
        self.assertTrue(all(level == 0 for _, level, _ in executions))


if __name__ == '__main__':
    unittest.main()
