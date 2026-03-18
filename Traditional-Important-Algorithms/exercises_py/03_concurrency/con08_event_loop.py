# I AM NOT DONE

"""
con08_event_loop.py

An Event Loop is a programming construct that waits for and dispatches events
or messages in a program. It's the foundation of asynchronous I/O frameworks
and is used in Node.js, browser JavaScript, and async Python runtimes.

Your task: Implement a simple event loop with timers and I/O events.

Key concepts:
- Event queue: Stores pending events
- Event handlers: Functions that process events
- Timers: Delayed execution
- Non-blocking I/O: Process events without waiting
"""

import heapq
from collections import deque
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import unittest


EventId = int
TimerId = int
HandlerId = int


class EventType(Enum):
    """Types of events."""
    TIMER = "timer"
    IO = "io"
    CUSTOM = "custom"


@dataclass
class Event:
    """Represents an event."""
    event_type: EventType
    data: str


@dataclass
class ScheduledEvent:
    """Event scheduled for a specific time."""
    id: EventId
    event: Event
    scheduled_time: int

    def __lt__(self, other):
        """Compare by scheduled time (earlier times come first)."""
        if self.scheduled_time != other.scheduled_time:
            return self.scheduled_time < other.scheduled_time
        return self.id < other.id


class EventLoop:
    """Simple event loop implementation."""

    def __init__(self):
        self.current_time = 0
        self.next_event_id = 0
        self.next_timer_id = 0
        self.immediate_queue = deque()
        self.timer_queue = []  # Min-heap
        self.handlers: List[Callable] = []
        self.event_log: List[Tuple[int, Event]] = []

    def schedule_immediate(self, event: Event) -> EventId:
        """
        TODO: Schedule an event to run immediately (in the next tick).

        Add to immediate_queue with current_time as scheduled_time.

        Args:
            event: The event to schedule

        Returns:
            The event ID
        """
        pass  # TODO: Implement this

    def schedule_timer(self, event: Event, delay: int) -> EventId:
        """
        TODO: Schedule an event to run after a delay.

        Add to timer_queue with current_time + delay as scheduled_time.

        Args:
            event: The event to schedule
            delay: Delay in time units

        Returns:
            The event ID
        """
        pass  # TODO: Implement this

    def set_timeout(self, delay: int) -> TimerId:
        """
        TODO: Create a timer that fires after delay.

        Similar to JavaScript's setTimeout.

        Args:
            delay: Delay in time units

        Returns:
            The timer ID
        """
        pass  # TODO: Implement this

    def add_handler(self, handler: Callable[[Event, 'EventLoop'], None]) -> HandlerId:
        """
        TODO: Add an event handler.

        Args:
            handler: Function that takes (event, event_loop)

        Returns:
            The handler ID (its index in the handlers list)
        """
        pass  # TODO: Implement this

    def _process_event(self, event: Event) -> None:
        """
        TODO: Process an event by calling all handlers.

        Steps:
        1. Log the event
        2. Call each handler with the event
        """
        pass  # TODO: Implement this

    def tick(self) -> bool:
        """
        TODO: Process one iteration of the event loop.

        Steps:
        1. Process all immediate events (in order)
        2. Check timer queue for events ready to fire
        3. Process the next ready timer event
        4. Increment current_time
        5. Return True if any event was processed

        Returns:
            True if any event was processed, False otherwise
        """
        pass  # TODO: Implement this

    def run(self) -> None:
        """Run the event loop until no more events."""
        while self.tick():
            pass

    def run_for(self, duration: int) -> None:
        """Run the event loop for a specific duration."""
        end_time = self.current_time + duration
        while self.current_time < end_time and self.tick():
            pass

    def current_time_value(self) -> int:
        """Get the current time."""
        return self.current_time

    def has_pending_events(self) -> bool:
        """Check if there are pending events."""
        return len(self.immediate_queue) > 0 or len(self.timer_queue) > 0

    def get_event_log(self) -> List[Tuple[int, Event]]:
        """Get all logged events."""
        return self.event_log


class TestEventLoop(unittest.TestCase):
    """Test cases for Event Loop."""

    def test_immediate_event(self):
        """Test immediate event execution."""
        event_loop = EventLoop()
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "test"))

        self.assertTrue(event_loop.has_pending_events())
        processed = event_loop.tick()
        self.assertTrue(processed)
        self.assertFalse(event_loop.has_pending_events())

    def test_timer_event(self):
        """Test timer event execution."""
        event_loop = EventLoop()
        event_loop.schedule_timer(Event(EventType.CUSTOM, "delayed"), 10)

        # Event should not fire immediately
        for _ in range(9):
            event_loop.tick()

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 0)

        # Should fire on or after the 10th tick
        event_loop.tick()
        log = event_loop.get_event_log()
        self.assertEqual(len(log), 1)

    def test_event_ordering(self):
        """Test immediate events process in order."""
        event_loop = EventLoop()

        event_loop.schedule_immediate(Event(EventType.CUSTOM, "first"))
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "second"))
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "third"))

        event_loop.run()

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 3)
        self.assertEqual(log[0][1].data, "first")
        self.assertEqual(log[1][1].data, "second")
        self.assertEqual(log[2][1].data, "third")

    def test_timer_ordering(self):
        """Test timers fire in correct order."""
        event_loop = EventLoop()

        event_loop.schedule_timer(Event(EventType.CUSTOM, "long"), 20)
        event_loop.schedule_timer(Event(EventType.CUSTOM, "short"), 5)
        event_loop.schedule_timer(Event(EventType.CUSTOM, "medium"), 10)

        event_loop.run()

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 3)

        # Should fire in order: short, medium, long
        self.assertEqual(log[0][1].data, "short")
        self.assertEqual(log[1][1].data, "medium")
        self.assertEqual(log[2][1].data, "long")

    def test_mixed_events(self):
        """Test mix of immediate and timer events."""
        event_loop = EventLoop()

        event_loop.schedule_timer(Event(EventType.CUSTOM, "timer"), 5)
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "immediate"))

        event_loop.tick()  # Process immediate

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0][1].data, "immediate")

        event_loop.run()  # Process timer

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 2)

    def test_event_handler(self):
        """Test event handlers are called."""
        event_loop = EventLoop()
        count = [0]  # Use list to allow modification in closure

        def handler(event: Event, _: EventLoop):
            if event.event_type == EventType.CUSTOM:
                count[0] += 1

        event_loop.add_handler(handler)
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "test1"))
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "test2"))

        event_loop.run()

        # Handler should have been called twice
        self.assertEqual(count[0], 2)
        self.assertEqual(len(event_loop.get_event_log()), 2)

    def test_recursive_scheduling(self):
        """Test handler that schedules another event."""
        event_loop = EventLoop()

        def handler(event: Event, ev_loop: EventLoop):
            if event.data == "spawn":
                ev_loop.schedule_immediate(Event(EventType.CUSTOM, "spawned"))

        event_loop.add_handler(handler)
        event_loop.schedule_immediate(Event(EventType.CUSTOM, "spawn"))
        event_loop.run()

        log = event_loop.get_event_log()
        self.assertGreaterEqual(len(log), 2)  # Original event + spawned event

    def test_run_for_duration(self):
        """Test running for a specific duration."""
        event_loop = EventLoop()

        event_loop.schedule_timer(Event(EventType.CUSTOM, "t1"), 5)
        event_loop.schedule_timer(Event(EventType.CUSTOM, "t2"), 15)
        event_loop.schedule_timer(Event(EventType.CUSTOM, "t3"), 25)

        event_loop.run_for(20)

        log = event_loop.get_event_log()
        # Should have processed t1 and t2, but not t3
        self.assertEqual(len(log), 2)
        self.assertTrue(event_loop.has_pending_events())  # t3 still pending

    def test_set_timeout(self):
        """Test set_timeout functionality."""
        event_loop = EventLoop()

        timer1 = event_loop.set_timeout(10)
        timer2 = event_loop.set_timeout(5)

        self.assertNotEqual(timer1, timer2)

        event_loop.run()

        log = event_loop.get_event_log()
        self.assertEqual(len(log), 2)

    def test_empty_event_loop(self):
        """Test running empty event loop."""
        event_loop = EventLoop()

        result = event_loop.tick()
        self.assertFalse(result)

    def test_multiple_handlers(self):
        """Test multiple handlers on same event."""
        event_loop = EventLoop()
        calls = [0, 0]

        def handler1(event: Event, _):
            calls[0] += 1

        def handler2(event: Event, _):
            calls[1] += 1

        event_loop.add_handler(handler1)
        event_loop.add_handler(handler2)

        event_loop.schedule_immediate(Event(EventType.CUSTOM, "test"))
        event_loop.run()

        # Both handlers should have been called
        self.assertEqual(calls[0], 1)
        self.assertEqual(calls[1], 1)


if __name__ == '__main__':
    unittest.main()
