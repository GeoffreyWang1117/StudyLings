# I AM NOT DONE

"""
Exercise: Streaming Join

Join two data streams based on a common key within a time window.
Similar to database joins but for unbounded streams.

Types:
- Inner join: Emit when matching events from both streams within window
- Outer join: Emit even without match
- Temporal join: Join based on event time proximity

Your task: Implement streaming join with time windows.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LeftEvent:
    key: str
    value: int
    timestamp: int


@dataclass
class RightEvent:
    key: str
    value: str
    timestamp: int


@dataclass
class JoinResult:
    key: str
    left_value: int
    right_value: str
    timestamp: int


class StreamingJoin:
    """Join two data streams"""

    def __init__(self, window_ms: int):
        self.window_ms = window_ms
        self.left_buffer = {}
        self.right_buffer = {}

    def add_left(self, event: LeftEvent) -> List[JoinResult]:
        """Add event from left stream and return join results"""
        # TODO: Add left event and join with right events in window
        pass

    def add_right(self, event: RightEvent) -> List[JoinResult]:
        """Add event from right stream and return join results"""
        # TODO: Add right event and join with left events in window
        pass

    def evict_old_events(self, watermark: int):
        """Remove events outside join window"""
        # TODO: Clean up old events
        pass


import unittest


class TestStreamingJoin(unittest.TestCase):
    def test_simple_join(self):
        join = StreamingJoin(window_ms=5000)

        left = LeftEvent(key="user1", value=100, timestamp=1000)
        right = RightEvent(key="user1", value="data", timestamp=1500)

        join.add_left(left)
        results = join.add_right(right)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].key, "user1")
        self.assertEqual(results[0].left_value, 100)
        self.assertEqual(results[0].right_value, "data")


if __name__ == '__main__':
    unittest.main()
