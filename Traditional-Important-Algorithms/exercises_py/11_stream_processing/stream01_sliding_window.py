# I AM NOT DONE

"""
Exercise: Sliding Window Aggregator

Sliding windows are fundamental building blocks in stream processing for
grouping events into finite sets for aggregation. There are three main types:

1. Tumbling Windows: Fixed-size, non-overlapping windows
   Example: [0-5s], [5-10s], [10-15s]

2. Hopping Windows: Fixed-size, overlapping windows with a hop interval
   Example: [0-5s], [2-7s], [4-9s] (window=5s, hop=2s)

3. Session Windows: Variable-size windows based on gaps in activity
   Example: Events grouped if gap < timeout

Your task: Implement a sliding window aggregator that supports all three
window types for real-time stream aggregation.

Key concepts:
- Window lifecycle (creation, updating, expiration)
- Event time vs processing time
- Window boundaries and alignment
- Efficient storage of window state
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass


class WindowType(Enum):
    """Window types"""
    TUMBLING = "tumbling"
    HOPPING = "hopping"
    SESSION = "session"


@dataclass
class Event:
    """Stream event"""
    timestamp: int  # milliseconds
    value: int


@dataclass
class Window:
    """Window aggregation result"""
    start: int
    end: int
    count: int
    sum: int
    min: int
    max: int


class SlidingWindowAggregator:
    """Sliding window aggregator for stream processing"""

    def __init__(self, window_type: WindowType, size_ms: int = 5000, hop_ms: Optional[int] = None):
        """
        Initialize window aggregator

        Args:
            window_type: Type of window
            size_ms: Window size in milliseconds
            hop_ms: Hop interval for hopping windows
        """
        # TODO: Initialize the aggregator with the specified window type
        pass

    def add_event(self, event: Event):
        """Add an event to the appropriate window(s)"""
        # TODO: Add an event to the appropriate window(s)
        # - For tumbling windows: assign to exactly one window
        # - For hopping windows: may belong to multiple overlapping windows
        # - For session windows: merge with existing session or create new one
        pass

    def get_windows(self) -> List[Window]:
        """Return all current windows"""
        # TODO: Return all current windows
        # - For session windows, use session_windows
        # - For tumbling/hopping, use windows
        pass

    def evict_old_windows(self, watermark: int):
        """Remove windows that have ended before the watermark"""
        # TODO: Remove windows that have ended before the watermark
        # - Only keep windows that might still receive events
        # - For session windows, consider gap timeout
        pass


import unittest


class TestSlidingWindowAggregator(unittest.TestCase):
    def test_tumbling_window_basic(self):
        agg = SlidingWindowAggregator(WindowType.TUMBLING, size_ms=5000)

        agg.add_event(Event(timestamp=1000, value=10))
        agg.add_event(Event(timestamp=2000, value=20))
        agg.add_event(Event(timestamp=6000, value=30))

        windows = agg.get_windows()
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0].count, 2)
        self.assertEqual(windows[0].sum, 30)

    def test_tumbling_window_alignment(self):
        agg = SlidingWindowAggregator(WindowType.TUMBLING, size_ms=10000)

        agg.add_event(Event(timestamp=0, value=1))
        agg.add_event(Event(timestamp=9999, value=2))
        agg.add_event(Event(timestamp=10000, value=3))

        windows = agg.get_windows()
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0].count, 2)
        self.assertEqual(windows[1].count, 1)

    def test_window_aggregates(self):
        agg = SlidingWindowAggregator(WindowType.TUMBLING, size_ms=5000)

        agg.add_event(Event(timestamp=1000, value=5))
        agg.add_event(Event(timestamp=2000, value=15))
        agg.add_event(Event(timestamp=3000, value=10))

        windows = agg.get_windows()
        self.assertEqual(len(windows), 1)

        w = windows[0]
        self.assertEqual(w.count, 3)
        self.assertEqual(w.sum, 30)
        self.assertEqual(w.min, 5)
        self.assertEqual(w.max, 15)

    def test_evict_old_windows(self):
        agg = SlidingWindowAggregator(WindowType.TUMBLING, size_ms=5000)

        agg.add_event(Event(timestamp=1000, value=10))
        agg.add_event(Event(timestamp=6000, value=20))
        agg.add_event(Event(timestamp=11000, value=30))

        self.assertEqual(len(agg.get_windows()), 3)

        agg.evict_old_windows(10000)
        windows = agg.get_windows()
        self.assertLessEqual(len(windows), 2)


if __name__ == '__main__':
    unittest.main()
