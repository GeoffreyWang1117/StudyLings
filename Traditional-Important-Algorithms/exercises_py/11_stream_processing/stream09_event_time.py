# I AM NOT DONE

"""
Exercise: Event Time Processing

Process events based on their event time rather than processing time.
Handle out-of-order events and late arrivals.

Key concepts:
- Event time vs processing time
- Timestamp extraction
- Time domain assignment
- Skew handling

Your task: Implement event time processing.
"""

from typing import List
from dataclasses import dataclass
import time


@dataclass
class TimestampedEvent:
    """Event with timestamp"""
    event_time: int  # milliseconds
    processing_time: int  # milliseconds
    data: str


class EventTimeProcessor:
    """Process events based on event time"""

    def __init__(self):
        self.events = []
        self.current_watermark = 0

    def add_event(self, data: str, event_time: int):
        """Add event with event time"""
        # TODO: Add event
        # - Record processing time
        # - Store event
        # - Update watermark based on event times
        pass

    def get_events_in_range(self, start_time: int, end_time: int) -> List[TimestampedEvent]:
        """Get events in event time range"""
        # TODO: Return events in time range
        pass

    def get_skew(self) -> int:
        """Calculate event time skew (difference between event and processing time)"""
        # TODO: Calculate average skew
        pass


import unittest


class TestEventTimeProcessor(unittest.TestCase):
    def test_event_time_processing(self):
        proc = EventTimeProcessor()

        proc.add_event("event1", 1000)
        proc.add_event("event2", 2000)
        proc.add_event("event3", 1500)  # Out of order

        events = proc.get_events_in_range(1000, 2000)
        self.assertEqual(len(events), 3)


if __name__ == '__main__':
    unittest.main()
