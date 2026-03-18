# I AM NOT DONE

"""
dist08_vector_clock.py

Vector Clocks track causality in distributed systems without synchronized clocks.
Each node maintains a vector of logical timestamps - one for each node in the system.

Key properties:
- Happens-before relationship: If event A → event B, then VC(A) < VC(B)
- Concurrent events: Events are concurrent if neither VC(A) < VC(B) nor VC(B) < VC(A)
- Causal ordering: Can determine if events are causally related or concurrent

Your task: Implement vector clocks for tracking causality.

Key concepts:
- Local event: Increment own clock
- Send event: Increment own clock, send vector with message
- Receive event: Merge received vector (take max of each element), increment own clock
- Comparison: Less than, greater than, concurrent, or equal
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import unittest


class ClockOrdering(Enum):
    """Clock ordering relationship."""
    HAPPENS_BEFORE = auto()  # self < other
    HAPPENS_AFTER = auto()   # self > other
    CONCURRENT = auto()      # self || other (concurrent)
    EQUAL = auto()          # self == other


@dataclass
class VectorClock:
    """A vector clock."""
    clock: Dict[int, int]  # node_id -> timestamp
    node_id: int

    @staticmethod
    def new(node_id: int, num_nodes: int) -> 'VectorClock':
        """Create a new vector clock."""
        clock = {i: 0 for i in range(num_nodes)}
        return VectorClock(clock=clock, node_id=node_id)

    def increment(self):
        """
        TODO: Increment this node's timestamp.

        - Increment the counter for node_id
        """
        pass  # TODO: Implement this

    def get(self, node_id: int) -> int:
        """Get the timestamp for a node."""
        return self.clock.get(node_id, 0)

    def set(self, node_id: int, value: int):
        """Set the timestamp for a node."""
        self.clock[node_id] = value

    def merge(self, other: 'VectorClock'):
        """
        TODO: Merge another vector clock into this one.

        - For each node in other's clock, take the maximum of the two values
        - Don't forget to increment own clock after merging!
        """
        pass  # TODO: Implement this

    def compare(self, other: 'VectorClock') -> ClockOrdering:
        """
        TODO: Compare two vector clocks.

        - If all entries in self <= other and at least one is <, return HAPPENS_BEFORE
        - If all entries in self >= other and at least one is >, return HAPPENS_AFTER
        - If all entries are equal, return EQUAL
        - Otherwise, return CONCURRENT
        """
        pass  # TODO: Implement this

    def happens_before(self, other: 'VectorClock') -> bool:
        """Check if this clock happens before another."""
        return self.compare(other) == ClockOrdering.HAPPENS_BEFORE

    def happens_after(self, other: 'VectorClock') -> bool:
        """Check if this clock happens after another."""
        return self.compare(other) == ClockOrdering.HAPPENS_AFTER

    def is_concurrent(self, other: 'VectorClock') -> bool:
        """Check if this clock is concurrent with another."""
        return self.compare(other) == ClockOrdering.CONCURRENT

    def clone_clock(self) -> 'VectorClock':
        """Clone this vector clock."""
        return VectorClock(clock=self.clock.copy(), node_id=self.node_id)


class EventType(Enum):
    """Event types."""
    LOCAL = auto()
    SEND = auto()
    RECEIVE = auto()


@dataclass
class Event:
    """An event in the distributed system."""
    id: int
    node_id: int
    event_type: EventType
    description: str
    clock: VectorClock
    related_node: Optional[int] = None  # For send/receive events


class DistributedSystem:
    """A distributed system with vector clocks."""

    def __init__(self, num_nodes: int):
        """Initialize the system."""
        self.nodes: Dict[int, VectorClock] = {
            i: VectorClock.new(i, num_nodes) for i in range(num_nodes)
        }
        self.events: List[Event] = []
        self.next_event_id = 0

    def local_event(self, node_id: int, description: str) -> int:
        """
        TODO: Process a local event on a node.

        - Get the node's vector clock
        - Increment it
        - Create an Event with the current clock state
        - Add event to events list
        - Return event ID
        """
        pass  # TODO: Implement this

    def send_message(self, from_node: int, to_node: int, message: str) -> Tuple[int, VectorClock]:
        """
        TODO: Process a send event.

        - Get sender's vector clock
        - Increment it
        - Create a Send event
        - Return (event_id, copy of sender's clock to include with message)
        """
        pass  # TODO: Implement this

    def receive_message(self, node_id: int, sender: int, message: str,
                       sender_clock: VectorClock) -> int:
        """
        TODO: Process a receive event.

        - Get receiver's vector clock
        - Merge with sender's clock (this updates receiver's clock)
        - Create a Receive event
        - Return event ID
        """
        pass  # TODO: Implement this

    def get_event(self, event_id: int) -> Optional[Event]:
        """Get an event by ID."""
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def get_node_clock(self, node_id: int) -> Optional[VectorClock]:
        """Get a node's current clock."""
        return self.nodes.get(node_id)

    def compare_events(self, event_id1: int, event_id2: int) -> Optional[ClockOrdering]:
        """Compare two events."""
        e1 = self.get_event(event_id1)
        e2 = self.get_event(event_id2)
        if not e1 or not e2:
            return None
        return e1.clock.compare(e2.clock)

    def get_concurrent_events(self) -> List[Tuple[int, int]]:
        """
        TODO: Find all pairs of concurrent events.

        - Compare all pairs of events
        - Return pairs where events are concurrent
        - Only include each pair once (i.e., (a, b) not both (a, b) and (b, a))
        """
        pass  # TODO: Implement this

    def get_causal_history(self, event_id: int) -> List[int]:
        """
        TODO: Get all events that happened before this event.

        - Find all events e where e.clock < target_event.clock
        - Return their event IDs
        """
        pass  # TODO: Implement this


# Unit Tests
class TestVectorClock(unittest.TestCase):

    def test_vector_clock_creation(self):
        vc = VectorClock.new(0, 3)
        self.assertEqual(vc.get(0), 0)
        self.assertEqual(vc.get(1), 0)
        self.assertEqual(vc.get(2), 0)

    def test_increment(self):
        vc = VectorClock.new(0, 3)
        vc.increment()
        self.assertEqual(vc.get(0), 1)
        self.assertEqual(vc.get(1), 0)

        vc.increment()
        self.assertEqual(vc.get(0), 2)

    def test_merge(self):
        vc1 = VectorClock.new(0, 3)
        vc2 = VectorClock.new(1, 3)

        vc1.set(0, 5)
        vc1.set(1, 2)
        vc1.set(2, 3)

        vc2.set(0, 3)
        vc2.set(1, 6)
        vc2.set(2, 4)

        vc1.merge(vc2)

        # After merge, vc1 should have max of each + its own increment
        self.assertEqual(vc1.get(0), 6)  # max(5, 3) + 1
        self.assertEqual(vc1.get(1), 6)  # max(2, 6)
        self.assertEqual(vc1.get(2), 4)  # max(3, 4)

    def test_happens_before(self):
        vc1 = VectorClock.new(0, 2)
        vc2 = VectorClock.new(0, 2)

        vc1.set(0, 1)
        vc1.set(1, 2)

        vc2.set(0, 2)
        vc2.set(1, 3)

        self.assertEqual(vc1.compare(vc2), ClockOrdering.HAPPENS_BEFORE)
        self.assertTrue(vc1.happens_before(vc2))

    def test_happens_after(self):
        vc1 = VectorClock.new(0, 2)
        vc2 = VectorClock.new(0, 2)

        vc1.set(0, 5)
        vc1.set(1, 4)

        vc2.set(0, 2)
        vc2.set(1, 3)

        self.assertEqual(vc1.compare(vc2), ClockOrdering.HAPPENS_AFTER)
        self.assertTrue(vc1.happens_after(vc2))

    def test_concurrent(self):
        vc1 = VectorClock.new(0, 2)
        vc2 = VectorClock.new(1, 2)

        vc1.set(0, 3)
        vc1.set(1, 1)

        vc2.set(0, 1)
        vc2.set(1, 3)

        self.assertEqual(vc1.compare(vc2), ClockOrdering.CONCURRENT)
        self.assertTrue(vc1.is_concurrent(vc2))
        self.assertTrue(vc2.is_concurrent(vc1))  # Symmetry

    def test_equal(self):
        vc1 = VectorClock.new(0, 2)
        vc2 = VectorClock.new(1, 2)

        vc1.set(0, 3)
        vc1.set(1, 2)

        vc2.set(0, 3)
        vc2.set(1, 2)

        self.assertEqual(vc1.compare(vc2), ClockOrdering.EQUAL)

    def test_local_event(self):
        system = DistributedSystem(3)

        event_id = system.local_event(0, "process data")

        clock = system.get_node_clock(0)
        self.assertEqual(clock.get(0), 1)

        event = system.get_event(event_id)
        self.assertEqual(event.node_id, 0)

    def test_send_receive(self):
        system = DistributedSystem(2)

        event_id, sender_clock = system.send_message(0, 1, "hello")
        system.receive_message(1, 0, "hello", sender_clock)

        clock0 = system.get_node_clock(0)
        clock1 = system.get_node_clock(1)

        # Node 0 sent, so its clock[0] = 1
        self.assertEqual(clock0.get(0), 1)

        # Node 1 received, so it merged and incremented
        self.assertGreaterEqual(clock1.get(0), 1)
        self.assertGreaterEqual(clock1.get(1), 1)

    def test_causal_ordering(self):
        system = DistributedSystem(2)

        e1 = system.local_event(0, "event1")
        event_id, clock = system.send_message(0, 1, "msg")
        e3 = system.receive_message(1, 0, "msg", clock)

        ordering = system.compare_events(e1, e3)
        self.assertEqual(ordering, ClockOrdering.HAPPENS_BEFORE)

    def test_concurrent_events_detection(self):
        system = DistributedSystem(2)

        # Two independent events on different nodes
        e1 = system.local_event(0, "event_a")
        e2 = system.local_event(1, "event_b")

        ordering = system.compare_events(e1, e2)
        self.assertEqual(ordering, ClockOrdering.CONCURRENT)

    def test_multiple_messages(self):
        system = DistributedSystem(3)

        # Node 0 sends to node 1
        _, clock1 = system.send_message(0, 1, "msg1")
        system.receive_message(1, 0, "msg1", clock1)

        # Node 1 sends to node 2
        _, clock2 = system.send_message(1, 2, "msg2")
        system.receive_message(2, 1, "msg2", clock2)

        # Node 2 should have causal information from node 0
        clock2 = system.get_node_clock(2)
        self.assertGreater(clock2.get(0), 0)  # Knows about node 0's event

    def test_causal_history(self):
        system = DistributedSystem(2)

        e1 = system.local_event(0, "a")
        e2 = system.local_event(0, "b")
        _, clock = system.send_message(0, 1, "msg")
        e4 = system.receive_message(1, 0, "msg", clock)

        history = system.get_causal_history(e4)

        # e4's causal history should include e1, e2, and the send event
        self.assertGreaterEqual(len(history), 2)
        self.assertIn(e1, history)
        self.assertIn(e2, history)


if __name__ == '__main__':
    unittest.main()
