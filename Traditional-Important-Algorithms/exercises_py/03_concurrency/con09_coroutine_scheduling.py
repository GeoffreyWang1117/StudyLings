# I AM NOT DONE

"""
con09_coroutine_scheduling.py

Coroutines are functions that can suspend execution and resume later,
allowing for cooperative multitasking. A coroutine scheduler manages
multiple coroutines, switching between them when they yield.

Your task: Implement a coroutine scheduler that can suspend and resume
coroutine execution.

Key concepts:
- Yield points: Where coroutines can suspend
- Resumption: Continuing from where a coroutine left off
- Cooperative scheduling: Coroutines control when they yield
- State preservation: Maintaining coroutine state across yields
"""

from collections import deque
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
import unittest


CoroutineId = int


class YieldType(Enum):
    """Types of yields."""
    YIELD = "yield"
    YIELD_VALUE = "yield_value"
    AWAIT = "await"


class CoroutineState(Enum):
    """Coroutine execution states."""
    READY = "ready"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"


@dataclass
class Instruction:
    """Instruction for coroutine execution."""
    execute_for: int  # Time units to execute
    action: str  # 'yield' or 'return'
    yield_type: Optional[YieldType] = None
    yield_value: Optional[int] = None
    await_coroutine: Optional[CoroutineId] = None
    return_value: Optional[int] = None


class Coroutine:
    """Represents a coroutine with instructions."""

    def __init__(self, coroutine_id: CoroutineId, instructions: List[Instruction]):
        self.id = coroutine_id
        self.state = CoroutineState.READY
        self.instructions = deque(instructions)
        self.execution_time = 0

    @staticmethod
    def simple_yielding(coroutine_id: CoroutineId, total_time: int, yield_interval: int):
        """
        TODO: Create a coroutine that yields every yield_interval units.

        Args:
            coroutine_id: Coroutine ID
            total_time: Total execution time
            yield_interval: Interval between yields

        Returns:
            A Coroutine that yields periodically
        """
        pass  # TODO: Implement this

    def is_complete(self) -> bool:
        """Check if coroutine has completed."""
        return self.state == CoroutineState.COMPLETED

    def can_run(self) -> bool:
        """Check if coroutine can run."""
        return self.state == CoroutineState.READY


class EventType(Enum):
    """Scheduler event types."""
    STARTED = "started"
    RESUMED = "resumed"
    YIELDED = "yielded"
    COMPLETED = "completed"


@dataclass
class SchedulerEvent:
    """Records scheduler events."""
    time: int
    coroutine_id: CoroutineId
    event: EventType
    yield_type: Optional[YieldType] = None
    return_value: Optional[int] = None


class CoroutineScheduler:
    """Scheduler for managing coroutines."""

    def __init__(self):
        self.coroutines: List[Coroutine] = []
        self.ready_queue = deque()
        self.waiting: List[Tuple[CoroutineId, CoroutineId]] = []  # (waiting_id, waiting_for_id)
        self.current_time = 0
        self.events: List[SchedulerEvent] = []

    def spawn(self, coroutine: Coroutine) -> CoroutineId:
        """
        TODO: Add a coroutine to the scheduler.

        Steps:
        1. Add to coroutines list
        2. Add to ready queue
        3. Return its ID

        Args:
            coroutine: The coroutine to add

        Returns:
            The coroutine ID
        """
        pass  # TODO: Implement this

    def _log_event(self, coroutine_id: CoroutineId, event: EventType,
                   yield_type: Optional[YieldType] = None,
                   return_value: Optional[int] = None) -> None:
        """Log a scheduler event."""
        self.events.append(SchedulerEvent(self.current_time, coroutine_id, event,
                                          yield_type, return_value))

    def _resume_waiting_coroutines(self, completed_id: CoroutineId) -> None:
        """
        TODO: Resume coroutines that were waiting for the completed coroutine.

        Steps:
        1. Find all coroutines waiting for completed_id
        2. Move them back to ready queue
        3. Update their state to Ready
        4. Remove them from waiting list

        Args:
            completed_id: ID of the completed coroutine
        """
        pass  # TODO: Implement this

    def run_next(self) -> Optional[CoroutineId]:
        """
        TODO: Run the next ready coroutine until it yields or completes.

        Steps:
        1. Get next coroutine from ready queue
        2. Update its state to Running
        3. Execute its next instruction
        4. Handle the action (Yield or Return)
        5. Update current_time
        6. Log appropriate events
        7. Return the coroutine ID that ran

        Returns:
            The coroutine ID that ran, or None
        """
        pass  # TODO: Implement this

    def run_all(self) -> None:
        """Run all coroutines until completion."""
        while len(self.ready_queue) > 0 or len(self.waiting) > 0:
            if len(self.ready_queue) == 0:
                # Deadlock detection
                if len(self.waiting) > 0:
                    break
            self.run_next()

    def get_coroutine(self, coroutine_id: CoroutineId) -> Optional[Coroutine]:
        """Get a coroutine by ID."""
        for coro in self.coroutines:
            if coro.id == coroutine_id:
                return coro
        return None

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def get_events(self) -> List[SchedulerEvent]:
        """Get all logged events."""
        return self.events

    def all_complete(self) -> bool:
        """Check if all coroutines have completed."""
        return all(c.is_complete() for c in self.coroutines)


class TestCoroutineScheduler(unittest.TestCase):
    """Test cases for Coroutine Scheduler."""

    def test_single_coroutine_no_yield(self):
        """Test single coroutine without yields."""
        scheduler = CoroutineScheduler()

        coroutine = Coroutine(0, [
            Instruction(10, 'return', return_value=42),
        ])

        scheduler.spawn(coroutine)
        scheduler.run_all()

        coro = scheduler.get_coroutine(0)
        self.assertEqual(coro.state, CoroutineState.COMPLETED)
        self.assertEqual(scheduler.current_time_value(), 10)

    def test_coroutine_with_yields(self):
        """Test coroutine with yields."""
        scheduler = CoroutineScheduler()

        coroutine = Coroutine(0, [
            Instruction(5, 'yield', yield_type=YieldType.YIELD),
            Instruction(5, 'return', return_value=100),
        ])

        scheduler.spawn(coroutine)
        scheduler.run_all()

        events = scheduler.get_events()
        self.assertTrue(any(e.event == EventType.YIELDED and
                           e.yield_type == YieldType.YIELD for e in events))
        self.assertTrue(any(e.event == EventType.COMPLETED and
                           e.return_value == 100 for e in events))

    def test_multiple_coroutines(self):
        """Test multiple coroutines executing."""
        scheduler = CoroutineScheduler()

        scheduler.spawn(Coroutine.simple_yielding(0, 10, 5))
        scheduler.spawn(Coroutine.simple_yielding(1, 10, 5))

        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())

        # Both should have run
        events = scheduler.get_events()
        self.assertTrue(any(e.coroutine_id == 0 for e in events))
        self.assertTrue(any(e.coroutine_id == 1 for e in events))

    def test_round_robin_execution(self):
        """Test round-robin execution of coroutines."""
        scheduler = CoroutineScheduler()

        scheduler.spawn(Coroutine.simple_yielding(0, 15, 5))
        scheduler.spawn(Coroutine.simple_yielding(1, 15, 5))

        scheduler.run_all()

        events = scheduler.get_events()

        # Events should alternate between coroutines
        last_id = None
        switches = 0

        for event in events:
            if event.event in (EventType.STARTED, EventType.RESUMED):
                if last_id is not None and last_id != event.coroutine_id:
                    switches += 1
                last_id = event.coroutine_id

        self.assertGreater(switches, 0, "Coroutines should interleave execution")

    def test_await_coroutine(self):
        """Test awaiting another coroutine."""
        scheduler = CoroutineScheduler()

        coroutine1 = Coroutine(0, [
            Instruction(10, 'return', return_value=42),
        ])

        coroutine2 = Coroutine(1, [
            Instruction(5, 'yield', yield_type=YieldType.AWAIT, await_coroutine=0),
            Instruction(5, 'return', return_value=100),
        ])

        scheduler.spawn(coroutine1)
        scheduler.spawn(coroutine2)
        scheduler.run_all()

        # Both should complete
        self.assertTrue(scheduler.all_complete())

        events = scheduler.get_events()
        # Coroutine 1 should complete before coroutine 2 resumes
        coro1_complete_events = [e for e in events
                                 if e.coroutine_id == 0 and e.event == EventType.COMPLETED]
        coro2_resume_events = [e for e in events
                              if e.coroutine_id == 1 and e.event == EventType.RESUMED]

        if coro1_complete_events and coro2_resume_events:
            complete_time = coro1_complete_events[0].time
            resume_time = coro2_resume_events[0].time
            self.assertLessEqual(complete_time, resume_time)

    def test_immediate_completion(self):
        """Test coroutine that completes immediately."""
        scheduler = CoroutineScheduler()

        coroutine = Coroutine(0, [
            Instruction(0, 'return', return_value=1),
        ])

        scheduler.spawn(coroutine)
        scheduler.run_all()

        self.assertTrue(scheduler.all_complete())
        self.assertEqual(scheduler.current_time_value(), 0)

    def test_multiple_yields(self):
        """Test coroutine with multiple yields."""
        scheduler = CoroutineScheduler()

        coroutine = Coroutine(0, [
            Instruction(1, 'yield', yield_type=YieldType.YIELD),
            Instruction(1, 'yield', yield_type=YieldType.YIELD),
            Instruction(1, 'yield', yield_type=YieldType.YIELD),
            Instruction(1, 'return', return_value=0),
        ])

        scheduler.spawn(coroutine)
        scheduler.run_all()

        events = scheduler.get_events()
        yield_count = sum(1 for e in events if e.event == EventType.YIELDED)

        self.assertEqual(yield_count, 3)

    def test_empty_scheduler(self):
        """Test running empty scheduler."""
        scheduler = CoroutineScheduler()

        result = scheduler.run_next()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
