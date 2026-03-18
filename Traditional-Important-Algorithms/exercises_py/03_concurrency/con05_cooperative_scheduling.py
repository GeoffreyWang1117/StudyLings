# I AM NOT DONE

"""
con05_cooperative_scheduling.py

Cooperative Scheduling (non-preemptive scheduling) relies on tasks voluntarily
yielding control back to the scheduler. Tasks run until they explicitly yield
or complete. This is simpler than preemptive scheduling but can lead to
starvation if a task doesn't yield.

Your task: Implement a cooperative scheduler where tasks must yield control.

Key concepts:
- Voluntary yielding: Tasks control when they give up CPU
- No forced preemption: Scheduler cannot interrupt tasks
- Simpler context switching: Only happens at yield points
"""

from collections import deque
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
import unittest


class YieldReason(Enum):
    """Reasons for yielding."""
    VOLUNTARY = "voluntary"
    IO_WAIT = "io_wait"
    COMPLETED = "completed"


class Action(Enum):
    """Action types for task instructions."""
    YIELD = "yield"
    CONTINUE = "continue"


@dataclass
class TaskAction:
    """Represents an action a task will perform."""
    run_for: int  # Time units to run before action
    action: Action
    yield_reason: Optional[YieldReason] = None
    continue_time: Optional[int] = None  # For Continue action


class Task:
    """Represents a cooperative task."""

    def __init__(self, task_id: int, actions: List[TaskAction]):
        self.id = task_id
        self.actions = deque(actions)
        self.total_execution_time = sum(a.run_for for a in actions)

    @staticmethod
    def simple(task_id: int, execution_time: int, yield_interval: int):
        """
        TODO: Create a task that yields every yield_interval units.

        Calculate how many yields are needed and create TaskActions.

        Args:
            task_id: Task identifier
            execution_time: Total execution time
            yield_interval: Interval between yields

        Returns:
            A Task that yields periodically
        """
        pass  # TODO: Implement this

    def is_complete(self) -> bool:
        """Check if task has no more actions."""
        return len(self.actions) == 0

    def next_action(self) -> Optional[TaskAction]:
        """Get the next action to perform."""
        return self.actions.popleft() if self.actions else None


class EventType(Enum):
    """Scheduler event types."""
    STARTED = "started"
    YIELDED = "yielded"
    RESUMED = "resumed"


@dataclass
class SchedulerEvent:
    """Records scheduler events."""
    time: int
    task_id: int
    event: EventType
    yield_reason: Optional[YieldReason] = None


class CooperativeScheduler:
    """Cooperative scheduler implementation."""

    def __init__(self):
        self.ready_queue = deque()
        self.waiting_queue = deque()  # (task, time_to_wait)
        self.current_time = 0
        self.events = []

    def _log_event(self, task_id: int, event: EventType,
                   yield_reason: Optional[YieldReason] = None) -> None:
        """Log a scheduler event."""
        self.events.append(SchedulerEvent(self.current_time, task_id, event, yield_reason))

    def add_task(self, task: Task) -> None:
        """
        TODO: Add a task to the ready queue.

        Args:
            task: The task to add
        """
        pass  # TODO: Implement this

    def _update_waiting_tasks(self) -> None:
        """
        TODO: Check waiting tasks and move ready ones back to ready queue.

        Decrement wait time for all waiting tasks.
        Move tasks with wait_time == 0 back to ready queue.
        """
        pass  # TODO: Implement this

    def run_next(self) -> Optional[int]:
        """
        TODO: Run the next task until it yields or completes.

        Steps:
        1. Update waiting tasks
        2. Get next task from ready queue
        3. Log Started event
        4. Execute task actions until it yields or completes
        5. Handle the yield reason appropriately
        6. Return the task ID that ran (or None if no tasks)

        Returns:
            The task ID that ran, or None
        """
        pass  # TODO: Implement this

    def run_all(self) -> None:
        """Run all tasks until completion."""
        while not self.is_idle():
            self.run_next()

    def is_idle(self) -> bool:
        """Check if scheduler is idle."""
        return len(self.ready_queue) == 0 and len(self.waiting_queue) == 0

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def get_events(self) -> List[SchedulerEvent]:
        """Get all logged events."""
        return self.events


class TestCooperativeScheduler(unittest.TestCase):
    """Test cases for Cooperative Scheduler."""

    def test_single_task_no_yield(self):
        """Test single task without yielding."""
        scheduler = CooperativeScheduler()

        task = Task(1, [TaskAction(10, Action.YIELD, YieldReason.COMPLETED)])

        scheduler.add_task(task)
        scheduler.run_all()

        self.assertEqual(scheduler.current_time_value(), 10)
        self.assertTrue(scheduler.is_idle())

    def test_task_with_voluntary_yields(self):
        """Test task with multiple voluntary yields."""
        scheduler = CooperativeScheduler()

        task = Task(1, [
            TaskAction(3, Action.YIELD, YieldReason.VOLUNTARY),
            TaskAction(3, Action.YIELD, YieldReason.VOLUNTARY),
            TaskAction(4, Action.YIELD, YieldReason.COMPLETED),
        ])

        scheduler.add_task(task)
        scheduler.run_all()

        events = scheduler.get_events()
        yield_count = sum(1 for e in events
                         if e.event == EventType.YIELDED and
                         e.yield_reason == YieldReason.VOLUNTARY)
        self.assertEqual(yield_count, 2)
        self.assertEqual(scheduler.current_time_value(), 10)

    def test_multiple_tasks_round_robin(self):
        """Test multiple tasks interleaving execution."""
        scheduler = CooperativeScheduler()

        scheduler.add_task(Task.simple(1, 10, 5))
        scheduler.add_task(Task.simple(2, 10, 5))

        scheduler.run_all()

        events = scheduler.get_events()

        # Tasks should interleave
        task1_events = [e for e in events if e.task_id == 1]
        task2_events = [e for e in events if e.task_id == 2]

        self.assertGreater(len(task1_events), 1)
        self.assertGreater(len(task2_events), 1)

    def test_io_wait(self):
        """Test I/O wait behavior."""
        scheduler = CooperativeScheduler()

        task = Task(1, [
            TaskAction(5, Action.YIELD, YieldReason.IO_WAIT),
            TaskAction(5, Action.YIELD, YieldReason.COMPLETED),
        ])

        scheduler.add_task(task)

        # Add another task to run while first is waiting
        scheduler.add_task(Task.simple(2, 8, 8))

        scheduler.run_all()

        events = scheduler.get_events()
        self.assertTrue(any(e.task_id == 1 and e.yield_reason == YieldReason.IO_WAIT
                           for e in events))
        self.assertTrue(any(e.task_id == 2 for e in events))

    def test_task_hogging_cpu(self):
        """Test task that never yields causes starvation."""
        scheduler = CooperativeScheduler()

        # Task that never yields
        selfish_task = Task(1, [TaskAction(100, Action.YIELD, YieldReason.COMPLETED)])

        scheduler.add_task(selfish_task)
        scheduler.add_task(Task.simple(2, 10, 5))

        # Run just the first task
        scheduler.run_next()

        # Task 2 should not have run yet (starvation)
        events = scheduler.get_events()
        self.assertTrue(all(e.task_id == 1 for e in events))
        self.assertEqual(scheduler.current_time_value(), 100)

    def test_fair_yielding(self):
        """Test fair yielding between tasks."""
        scheduler = CooperativeScheduler()

        # Both tasks yield fairly
        scheduler.add_task(Task.simple(1, 20, 4))
        scheduler.add_task(Task.simple(2, 20, 4))

        scheduler.run_all()

        # Both should complete in reasonable time
        self.assertEqual(scheduler.current_time_value(), 40)

        events = scheduler.get_events()
        task1_starts = sum(1 for e in events if e.task_id == 1 and e.event == EventType.STARTED)
        task2_starts = sum(1 for e in events if e.task_id == 2 and e.event == EventType.STARTED)

        # Should get roughly equal scheduling opportunities
        self.assertGreater(task1_starts, 0)
        self.assertGreater(task2_starts, 0)

    def test_empty_scheduler(self):
        """Test running empty scheduler."""
        scheduler = CooperativeScheduler()

        result = scheduler.run_next()
        self.assertIsNone(result)

    def test_single_action_task(self):
        """Test task with single action."""
        scheduler = CooperativeScheduler()

        task = Task(1, [TaskAction(5, Action.YIELD, YieldReason.COMPLETED)])
        scheduler.add_task(task)

        result = scheduler.run_next()
        self.assertEqual(result, 1)
        self.assertTrue(scheduler.is_idle())

    def test_zero_time_action(self):
        """Test action with zero execution time."""
        scheduler = CooperativeScheduler()

        task = Task(1, [
            TaskAction(0, Action.YIELD, YieldReason.VOLUNTARY),
            TaskAction(5, Action.YIELD, YieldReason.COMPLETED),
        ])
        scheduler.add_task(task)

        scheduler.run_all()
        self.assertEqual(scheduler.current_time_value(), 5)


if __name__ == '__main__':
    unittest.main()
