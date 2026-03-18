# I AM NOT DONE

"""
con04_preemptive_scheduling.py

Preemptive Scheduling allows the scheduler to interrupt a running task and
switch to another task. This is crucial for responsive systems where high-
priority tasks need to run immediately.

Your task: Implement a preemptive scheduler with priority and time slicing.

Key concepts:
- Context switching: Saving and restoring task state
- Preemption points: When scheduler can interrupt tasks
- Time slicing: Tasks are interrupted after their quantum expires
"""

from collections import deque
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
import unittest


class TaskState(Enum):
    """Task execution states."""
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"


class EventType(Enum):
    """Scheduler event types."""
    TASK_STARTED = "task_started"
    TASK_PREEMPTED = "task_preempted"
    TASK_COMPLETED = "task_completed"
    CONTEXT_SWITCH = "context_switch"


@dataclass
class Task:
    """Represents a task with state and priority."""
    id: int
    priority: int
    remaining_time: int
    state: TaskState = TaskState.READY
    time_slice_used: int = 0

    def is_complete(self) -> bool:
        """Check if task has completed execution."""
        return self.remaining_time == 0


@dataclass
class SchedulerEvent:
    """Records scheduler events for analysis."""
    time: int
    event_type: EventType
    task_id: int


class PreemptiveScheduler:
    """Preemptive scheduler with priority and quantum-based preemption."""

    def __init__(self, quantum: int, context_switch_cost: int):
        """
        Initialize the preemptive scheduler.

        Args:
            quantum: Time slice for each task
            context_switch_cost: Overhead of context switching
        """
        self.ready_queue = deque()
        self.running_task = None
        self.quantum = quantum
        self.current_time = 0
        self.context_switch_cost = context_switch_cost
        self.events = []

    def _log_event(self, event_type: EventType, task_id: int) -> None:
        """Log a scheduler event."""
        self.events.append(SchedulerEvent(self.current_time, event_type, task_id))

    def _context_switch(self) -> None:
        """
        TODO: Simulate context switch overhead.

        Increment current_time by context_switch_cost.
        """
        pass  # TODO: Implement this

    def _should_preempt(self, new_task: Task) -> bool:
        """
        TODO: Determine if the running task should be preempted.

        Preempt if:
        1. No task is running, OR
        2. New task has higher priority, OR
        3. Running task has used up its quantum

        Args:
            new_task: The task to potentially preempt for

        Returns:
            True if should preempt, False otherwise
        """
        pass  # TODO: Implement this

    def add_task(self, task: Task) -> None:
        """
        TODO: Add a task and potentially preempt the running task.

        Steps:
        1. Check if the new task should preempt the current one
        2. If yes, move running task back to ready queue and context switch
        3. Add the new task appropriately

        Args:
            task: The task to add
        """
        pass  # TODO: Implement this

    def tick(self) -> Optional[int]:
        """
        TODO: Execute one time unit.

        Steps:
        1. If no task is running, schedule the next one from ready queue
        2. Execute the running task for 1 time unit
        3. Check if quantum expired or task completed
        4. Handle preemption if needed
        5. Return the ID of the task that executed (or None)

        Returns:
            The task ID that executed, or None
        """
        pass  # TODO: Implement this

    def run_until_idle(self) -> None:
        """Run until all tasks are complete."""
        while self.running_task is not None or len(self.ready_queue) > 0:
            self.tick()

    def get_events(self) -> List[SchedulerEvent]:
        """Get all logged events."""
        return self.events

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def is_idle(self) -> bool:
        """Check if scheduler is idle."""
        return self.running_task is None and len(self.ready_queue) == 0


class TestPreemptiveScheduler(unittest.TestCase):
    """Test cases for Preemptive Scheduler."""

    def test_single_task_no_preemption(self):
        """Test single task executes without preemption."""
        scheduler = PreemptiveScheduler(10, 1)
        scheduler.add_task(Task(1, 5, 8))

        scheduler.run_until_idle()

        events = scheduler.get_events()
        self.assertTrue(any(e.event_type == EventType.TASK_STARTED for e in events))
        self.assertTrue(any(e.event_type == EventType.TASK_COMPLETED for e in events))
        self.assertEqual(sum(1 for e in events if e.event_type == EventType.TASK_PREEMPTED), 0)

    def test_quantum_expiration(self):
        """Test task is preempted after quantum expires."""
        scheduler = PreemptiveScheduler(5, 1)
        scheduler.add_task(Task(1, 5, 12))

        for _ in range(5):
            scheduler.tick()

        # Task should be preempted after quantum expires
        events = scheduler.get_events()
        self.assertTrue(any(e.event_type == EventType.TASK_PREEMPTED for e in events))

    def test_priority_preemption(self):
        """Test higher priority task preempts lower priority."""
        scheduler = PreemptiveScheduler(10, 1)
        scheduler.add_task(Task(1, 5, 20))

        # Let task 1 run for a bit
        for _ in range(3):
            scheduler.tick()

        # Add higher priority task
        scheduler.add_task(Task(2, 10, 5))

        # Task 1 should be preempted
        events = scheduler.get_events()
        self.assertTrue(any(e.event_type == EventType.TASK_PREEMPTED and e.task_id == 1
                           for e in events))
        self.assertTrue(any(e.event_type == EventType.CONTEXT_SWITCH for e in events))

    def test_context_switch_overhead(self):
        """Test context switch adds overhead time."""
        scheduler = PreemptiveScheduler(5, 2)
        scheduler.add_task(Task(1, 5, 10))
        scheduler.add_task(Task(2, 10, 5))  # Higher priority

        scheduler.run_until_idle()

        # Total time should include context switch overhead
        # Task 2: 5 units + switch (2) + Task 1: 10 units
        self.assertGreaterEqual(scheduler.current_time_value(), 15)

    def test_round_robin_with_preemption(self):
        """Test round-robin behavior with equal priority."""
        scheduler = PreemptiveScheduler(4, 0)
        scheduler.add_task(Task(1, 5, 10))
        scheduler.add_task(Task(2, 5, 10))

        scheduler.run_until_idle()

        events = scheduler.get_events()

        # Both tasks should be preempted and resumed multiple times
        task1_starts = sum(1 for e in events
                          if e.task_id == 1 and e.event_type == EventType.TASK_STARTED)
        task2_starts = sum(1 for e in events
                          if e.task_id == 2 and e.event_type == EventType.TASK_STARTED)

        self.assertGreater(task1_starts, 1)
        self.assertGreater(task2_starts, 1)

    def test_no_preemption_on_lower_priority(self):
        """Test lower priority task doesn't preempt higher priority."""
        scheduler = PreemptiveScheduler(10, 1)
        scheduler.add_task(Task(1, 10, 15))

        for _ in range(5):
            scheduler.tick()

        # Add lower priority task
        events_before = len(scheduler.get_events())
        scheduler.add_task(Task(2, 5, 5))

        # Should not cause immediate preemption
        events = scheduler.get_events()
        self.assertEqual(len(events), events_before)  # No new events

    def test_task_completion_during_quantum(self):
        """Test task completes before quantum expires."""
        scheduler = PreemptiveScheduler(10, 0)
        scheduler.add_task(Task(1, 5, 3))

        scheduler.run_until_idle()

        events = scheduler.get_events()
        self.assertTrue(any(e.event_type == EventType.TASK_COMPLETED for e in events))
        self.assertEqual(sum(1 for e in events if e.event_type == EventType.TASK_PREEMPTED), 0)
        self.assertEqual(scheduler.current_time_value(), 3)

    def test_empty_scheduler(self):
        """Test ticking empty scheduler."""
        scheduler = PreemptiveScheduler(5, 1)

        result = scheduler.tick()
        self.assertIsNone(result)

    def test_multiple_preemptions(self):
        """Test multiple preemptions with varying priorities."""
        scheduler = PreemptiveScheduler(3, 0)
        scheduler.add_task(Task(1, 1, 10))
        scheduler.add_task(Task(2, 3, 5))
        scheduler.add_task(Task(3, 2, 5))

        scheduler.run_until_idle()

        # Should execute in priority order with preemptions
        events = scheduler.get_events()
        self.assertGreater(len(events), 3)

    def test_all_tasks_complete(self):
        """Test all tasks eventually complete."""
        scheduler = PreemptiveScheduler(5, 1)
        for i in range(5):
            scheduler.add_task(Task(i, i % 3, 10))

        scheduler.run_until_idle()

        self.assertTrue(scheduler.is_idle())
        events = scheduler.get_events()
        completed = sum(1 for e in events if e.event_type == EventType.TASK_COMPLETED)
        self.assertEqual(completed, 5)


if __name__ == '__main__':
    unittest.main()
