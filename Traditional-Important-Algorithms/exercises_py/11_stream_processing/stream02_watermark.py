# I AM NOT DONE

"""
Exercise: Watermark-based Event Processing

Watermarks are a core concept in stream processing for handling out-of-order
events. A watermark is a timestamp that indicates that no events with a
timestamp earlier than the watermark will arrive.

How watermarks work:
- Watermark(t) means "all events with timestamp < t have been seen"
- Used to determine when to close windows and emit results
- Handle late-arriving data (events that arrive after watermark)
- Balance latency vs completeness trade-off

Your task: Implement a watermark-based event processor that handles
out-of-order events and triggers computations when watermarks advance.

Key concepts:
- Watermark generation and propagation
- Event time vs processing time
- Late event handling (drop, side-output, or update)
- Allowed lateness configuration
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class LateEventStrategy(Enum):
    """Strategy for handling late events"""
    DROP = "drop"
    SIDE_OUTPUT = "side_output"
    UPDATE_WINDOW = "update_window"


@dataclass
class Event:
    """Stream event"""
    timestamp: int  # milliseconds
    data: str


@dataclass
class WindowResult:
    """Completed window result"""
    window_end: int
    events: List[Event]
    count: int


class WatermarkProcessor:
    """Watermark-based event processor"""

    def __init__(self, window_size: int, allowed_lateness: int, late_strategy: LateEventStrategy):
        """
        Initialize watermark processor

        Args:
            window_size: Window size in milliseconds
            allowed_lateness: How late can events arrive (milliseconds)
            late_strategy: Strategy for handling late events
        """
        # TODO: Initialize the watermark processor
        # - Set current_watermark to 0
        # - Initialize empty collections
        pass

    def add_event(self, event: Event):
        """Add an event to the processor"""
        # TODO: Add an event to the processor
        # - Check if event is late (timestamp < current_watermark - allowed_lateness)
        # - Handle based on late_strategy
        # - If not late, add to pending_events
        # Hint: Group events by window
        pass

    def advance_watermark(self, new_watermark: int) -> List[WindowResult]:
        """Advance the watermark and trigger window computations"""
        # TODO: Advance the watermark and trigger window computations
        # - Ensure new_watermark >= current_watermark (monotonic)
        # - Close all windows where window_end <= new_watermark
        # - Move completed windows to completed_windows
        # - Return newly completed windows
        # - Evict very old completed windows (outside allowed_lateness)
        pass

    def get_current_watermark(self) -> int:
        """Return the current watermark value"""
        # TODO: Return the current watermark value
        pass

    def get_late_events(self) -> List[Event]:
        """Return late events (for SIDE_OUTPUT strategy)"""
        # TODO: Return late events (for SIDE_OUTPUT strategy)
        pass


import unittest


class TestWatermarkProcessor(unittest.TestCase):
    def test_watermark_advancement(self):
        processor = WatermarkProcessor(5000, 1000, LateEventStrategy.DROP)

        self.assertEqual(processor.get_current_watermark(), 0)

        processor.advance_watermark(5000)
        self.assertEqual(processor.get_current_watermark(), 5000)

    def test_in_order_events(self):
        processor = WatermarkProcessor(5000, 1000, LateEventStrategy.DROP)

        processor.add_event(Event(timestamp=1000, data="event1"))
        processor.add_event(Event(timestamp=2000, data="event2"))

        results = processor.advance_watermark(6000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].count, 2)

    def test_out_of_order_events(self):
        processor = WatermarkProcessor(5000, 1000, LateEventStrategy.DROP)

        processor.add_event(Event(timestamp=3000, data="event1"))
        processor.add_event(Event(timestamp=1000, data="event2"))
        processor.add_event(Event(timestamp=2000, data="event3"))

        results = processor.advance_watermark(6000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].count, 3)

    def test_late_event_side_output_strategy(self):
        processor = WatermarkProcessor(5000, 1000, LateEventStrategy.SIDE_OUTPUT)

        processor.advance_watermark(6000)

        processor.add_event(Event(timestamp=1000, data="late_event"))

        late_events = processor.get_late_events()
        self.assertEqual(len(late_events), 1)
        self.assertEqual(late_events[0].data, "late_event")


if __name__ == '__main__':
    unittest.main()
