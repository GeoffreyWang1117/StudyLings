# I AM NOT DONE

"""
con02_priority_scheduling.py

Priority Scheduling assigns a priority to each task and always executes
the highest-priority task that's ready. This can be preemptive (where a
higher-priority task can interrupt a lower-priority one) or non-preemptive.

Your task: Implement a priority-based scheduler.

Key concepts:
- Priority levels: Higher number = higher priority
- Starvation: Low-priority tasks may never execute
- Aging: Can be used to prevent starvation
"""

import heapq
from typing import List, Tuple, Optional
import unittest


class Task:
    """Represents a task with priority and aging support."""

    def __init__(self, task_id: int, priority: int, execution_time: int):
        self.id = task_id
        self.priority = priority
        self.remaining_time = execution_time
        self.age = 0

    def is_complete(self) -> bool:
        """Check if task has completed execution."""
        return self.remaining_time == 0

    def effective_priority(self) -> int:
        """
        TODO: Calculate effective priority with aging.

        Hint: Add age to base priority to prevent starvation.

        Returns:
            The effective priority value
        """
        pass  # TODO: Implement this

    def __lt__(self, other):
        """
        TODO: Compare tasks by effective priority (higher priority comes first).

        Break ties by task ID (lower ID first).
        Note: Python's heapq is a min-heap, so we need to negate for max behavior.
        """
        pass  # TODO: Implement this


class PriorityScheduler:
    """Priority-based task scheduler with optional aging."""

    def __init__(self, enable_aging: bool = False):
        self.ready_queue = []  # Will use as a heap
        self.current_time = 0
        self.enable_aging = enable_aging

    def add_task(self, task: Task) -> None:
        """
        TODO: Add a task to the ready queue.

        Args:
            task: The task to add to the queue
        """
        pass  # TODO: Implement this

    def _age_tasks(self) -> None:
        """
        TODO: Increment age for all waiting tasks (if aging is enabled).

        Hint: You may need to rebuild the heap after modifying priorities.
        """
        pass  # TODO: Implement this

    def run_next(self, quantum: int) -> Optional[int]:
        """
        TODO: Run the highest priority task for the given quantum.

        Steps:
        1. Age all waiting tasks if aging is enabled
        2. Pop the highest priority task
        3. Execute it for min(quantum, remaining_time)
        4. Update current_time
        5. If not complete, reset age to 0 and add back to queue
        6. Return the task ID (or None if no tasks)

        Args:
            quantum: Time slice to run the task

        Returns:
            The task ID that ran, or None if no tasks
        """
        pass  # TODO: Implement this

    def run_to_completion(self) -> List[Tuple[int, int]]:
        """
        TODO: Run all tasks to completion (non-preemptive).

        Returns:
            A list of tuples (task_id, execution_time) pairs
        """
        pass  # TODO: Implement this

    def is_empty(self) -> bool:
        """Check if the ready queue is empty."""
        return len(self.ready_queue) == 0

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time


class TestPriorityScheduler(unittest.TestCase):
    """Test cases for Priority Scheduler."""

    def test_priority_order(self):
        """Test that tasks execute in priority order."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 1, 5))
        scheduler.add_task(Task(2, 3, 5))
        scheduler.add_task(Task(3, 2, 5))

        # Should run in order: 2 (priority 3), 3 (priority 2), 1 (priority 1)
        self.assertEqual(scheduler.run_next(10), 2)
        self.assertEqual(scheduler.run_next(10), 3)
        self.assertEqual(scheduler.run_next(10), 1)

    def test_equal_priority(self):
        """Test tie-breaking with equal priority."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 5, 5))
        scheduler.add_task(Task(2, 5, 5))
        scheduler.add_task(Task(3, 5, 5))

        # Should break ties by task ID
        self.assertEqual(scheduler.run_next(10), 1)
        self.assertEqual(scheduler.run_next(10), 2)
        self.assertEqual(scheduler.run_next(10), 3)

    def test_preemptive_scheduling(self):
        """Test preemptive behavior with higher priority arrival."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 1, 10))

        scheduler.run_next(3)  # Run task 1 for 3 units

        scheduler.add_task(Task(2, 5, 5))  # Higher priority arrives

        # Task 2 should run next (preemption)
        self.assertEqual(scheduler.run_next(10), 2)
        self.assertEqual(scheduler.run_next(10), 1)

    def test_aging_prevents_starvation(self):
        """Test that aging prevents starvation."""
        scheduler = PriorityScheduler(enable_aging=True)
        scheduler.add_task(Task(1, 1, 5))
        scheduler.add_task(Task(2, 10, 5))

        # Run several quanta
        task_ids_run = []
        for _ in range(20):
            task_id = scheduler.run_next(1)
            if task_id is not None:
                task_ids_run.append(task_id)

        # Task 1 should eventually run due to aging
        self.assertIn(1, task_ids_run, "Task 1 should eventually run with aging")

    def test_run_to_completion(self):
        """Test running all tasks to completion."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 2, 5))
        scheduler.add_task(Task(2, 3, 8))
        scheduler.add_task(Task(3, 1, 3))

        execution_log = scheduler.run_to_completion()

        self.assertEqual(len(execution_log), 3)
        self.assertEqual(execution_log[0][0], 2)  # Highest priority
        self.assertEqual(execution_log[1][0], 1)  # Medium priority
        self.assertEqual(execution_log[2][0], 3)  # Lowest priority

    def test_mixed_execution_times(self):
        """Test with varying execution times."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 10, 1))
        scheduler.add_task(Task(2, 5, 10))
        scheduler.add_task(Task(3, 8, 3))

        self.assertEqual(scheduler.run_next(5), 1)  # Priority 10
        self.assertEqual(scheduler.run_next(5), 3)  # Priority 8
        self.assertEqual(scheduler.run_next(5), 2)  # Priority 5 (partial)
        self.assertEqual(scheduler.run_next(5), 2)  # Priority 5 (complete)

    def test_single_task(self):
        """Test with a single task."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 5, 10))

        result = scheduler.run_next(20)
        self.assertEqual(result, 1)
        self.assertTrue(scheduler.is_empty())

    def test_empty_scheduler(self):
        """Test running empty scheduler."""
        scheduler = PriorityScheduler(enable_aging=False)

        result = scheduler.run_next(10)
        self.assertIsNone(result)

    def test_quantum_smaller_than_task(self):
        """Test task that needs multiple quanta."""
        scheduler = PriorityScheduler(enable_aging=False)
        scheduler.add_task(Task(1, 5, 20))

        for _ in range(4):
            result = scheduler.run_next(5)
            self.assertEqual(result, 1)

        self.assertTrue(scheduler.is_empty())

    def test_priority_levels(self):
        """Test with many priority levels."""
        scheduler = PriorityScheduler(enable_aging=False)
        for i in range(10):
            scheduler.add_task(Task(i, i, 2))

        results = []
        while not scheduler.is_empty():
            results.append(scheduler.run_next(5))

        # Should execute in descending priority order (9, 8, 7, ...)
        self.assertEqual(results[0], 9)
        self.assertEqual(results[-1], 0)

    def test_aging_mechanism(self):
        """Test aging increases effective priority."""
        scheduler = PriorityScheduler(enable_aging=True)
        task1 = Task(1, 1, 10)
        task2 = Task(2, 5, 10)

        scheduler.add_task(task1)
        scheduler.add_task(task2)

        # Run task 2 several times, aging task 1
        for _ in range(5):
            scheduler.run_next(2)

        # Task 1's age should have increased
        self.assertGreater(task1.age, 0)


if __name__ == '__main__':
    unittest.main()
