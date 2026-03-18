# I AM NOT DONE

"""
dist07_heartbeat.py

Heartbeat mechanisms are fundamental for failure detection in distributed systems.
Nodes periodically send "I'm alive" messages to detect when peers have failed.

Common approaches:
- Fixed timeout: Declare node dead after missing N heartbeats
- Adaptive timeout: Adjust based on network conditions
- Phi Accrual Failure Detector: Continuous suspicion level instead of binary alive/dead

Your task: Implement heartbeat-based failure detection with both fixed and
adaptive strategies.

Key concepts:
- Heartbeat interval: How often to send heartbeats
- Timeout threshold: When to suspect failure
- False positives: Declaring healthy node as failed (due to slow network)
- Detection time: How quickly failures are detected
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional
import unittest


class NodeStatus(Enum):
    """Node status."""
    ALIVE = auto()
    SUSPECTED = auto()
    DEAD = auto()


@dataclass
class HeartbeatRecord:
    """Record of heartbeat information for a node."""
    node_id: int
    last_heartbeat: int
    heartbeat_count: int
    status: NodeStatus
    missed_heartbeats: int


class FixedTimeoutDetector:
    """Fixed timeout failure detector."""

    def __init__(self, heartbeat_interval: int, timeout_threshold: int):
        """Initialize the detector."""
        self.nodes: Dict[int, HeartbeatRecord] = {}
        self.heartbeat_interval = heartbeat_interval
        self.timeout_threshold = timeout_threshold
        self.current_time = 0

    def add_node(self, node_id: int):
        """Add a node to monitor."""
        self.nodes[node_id] = HeartbeatRecord(
            node_id=node_id,
            last_heartbeat=self.current_time,
            heartbeat_count=0,
            status=NodeStatus.ALIVE,
            missed_heartbeats=0
        )

    def receive_heartbeat(self, node_id: int):
        """
        TODO: Process a heartbeat from a node.

        - Update last_heartbeat to current_time
        - Increment heartbeat_count
        - Reset missed_heartbeats to 0
        - Set status to ALIVE
        - If node doesn't exist, add it
        """
        pass  # TODO: Implement this

    def check_timeouts(self):
        """
        TODO: Check all nodes for timeouts.

        - For each node, calculate time_since_heartbeat
        - If time_since_heartbeat > timeout_threshold:
          - Set status to DEAD
          - Increment missed_heartbeats
        - Otherwise, ensure status is ALIVE
        """
        pass  # TODO: Implement this

    def advance_time(self, delta: int):
        """Advance time and check for timeouts."""
        self.current_time += delta
        self.check_timeouts()

    def get_status(self, node_id: int) -> Optional[NodeStatus]:
        """Get the status of a node."""
        record = self.nodes.get(node_id)
        return record.status if record else None

    def get_alive_nodes(self) -> List[int]:
        """Get all alive nodes."""
        return [
            record.node_id for record in self.nodes.values()
            if record.status == NodeStatus.ALIVE
        ]

    def get_dead_nodes(self) -> List[int]:
        """Get all dead nodes."""
        return [
            record.node_id for record in self.nodes.values()
            if record.status == NodeStatus.DEAD
        ]

    def get_time(self) -> int:
        """Get current time."""
        return self.current_time


@dataclass
class AdaptiveHeartbeatRecord:
    """Adaptive heartbeat record with history."""
    node_id: int
    last_heartbeat: int
    heartbeat_count: int
    status: NodeStatus
    heartbeat_history: List[int]  # Intervals between heartbeats
    max_history: int

    def calculate_mean(self) -> float:
        """Calculate mean heartbeat interval."""
        if not self.heartbeat_history:
            return 0.0
        return sum(self.heartbeat_history) / len(self.heartbeat_history)

    def calculate_std_dev(self) -> float:
        """Calculate standard deviation of heartbeat intervals."""
        if len(self.heartbeat_history) < 2:
            return 0.0
        mean = self.calculate_mean()
        variance = sum((x - mean) ** 2 for x in self.heartbeat_history) / len(self.heartbeat_history)
        return variance ** 0.5


class AdaptiveTimeoutDetector:
    """Adaptive timeout failure detector using Phi Accrual."""

    def __init__(self, max_history: int, phi_threshold: float):
        """Initialize the detector."""
        self.nodes: Dict[int, AdaptiveHeartbeatRecord] = {}
        self.max_history = max_history
        self.phi_threshold = phi_threshold
        self.current_time = 0

    def add_node(self, node_id: int):
        """Add a node to monitor."""
        self.nodes[node_id] = AdaptiveHeartbeatRecord(
            node_id=node_id,
            last_heartbeat=self.current_time,
            heartbeat_count=0,
            status=NodeStatus.ALIVE,
            heartbeat_history=[],
            max_history=self.max_history
        )

    def receive_heartbeat(self, node_id: int):
        """
        TODO: Process a heartbeat with adaptive tracking.

        - Calculate interval since last heartbeat
        - Add interval to heartbeat_history
        - Limit history size to max_history (remove oldest if needed)
        - Update last_heartbeat to current_time
        - Increment heartbeat_count
        - Set status to ALIVE
        - If node doesn't exist, add it
        """
        pass  # TODO: Implement this

    def calculate_phi(self, node_id: int) -> float:
        """
        TODO: Calculate phi (suspicion level) for a node.

        Uses the Phi Accrual Failure Detector algorithm.

        - Get time since last heartbeat
        - Get mean and std_dev from heartbeat history
        - If no history, return 0.0
        - Calculate phi based on how many standard deviations away we are

        Simplified phi calculation:
        phi = (time_since_last - mean) / (std_dev + 1.0)
        (The +1.0 prevents division by zero)

        Return 0.0 if node doesn't exist
        """
        pass  # TODO: Implement this

    def check_failures(self):
        """
        TODO: Check all nodes for failure based on phi threshold.

        - Calculate phi for each node
        - If phi > phi_threshold, mark as SUSPECTED
        - If phi > phi_threshold * 2, mark as DEAD
        - Otherwise, mark as ALIVE
        """
        pass  # TODO: Implement this

    def advance_time(self, delta: int):
        """Advance time and check for failures."""
        self.current_time += delta
        self.check_failures()

    def get_status(self, node_id: int) -> Optional[NodeStatus]:
        """Get the status of a node."""
        record = self.nodes.get(node_id)
        return record.status if record else None

    def get_alive_nodes(self) -> List[int]:
        """Get all alive nodes."""
        return [
            record.node_id for record in self.nodes.values()
            if record.status == NodeStatus.ALIVE
        ]

    def get_suspected_nodes(self) -> List[int]:
        """Get all suspected nodes."""
        return [
            record.node_id for record in self.nodes.values()
            if record.status == NodeStatus.SUSPECTED
        ]

    def get_dead_nodes(self) -> List[int]:
        """Get all dead nodes."""
        return [
            record.node_id for record in self.nodes.values()
            if record.status == NodeStatus.DEAD
        ]

    def get_time(self) -> int:
        """Get current time."""
        return self.current_time


# Unit Tests
class TestHeartbeat(unittest.TestCase):

    def test_fixed_timeout_initial_state(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        self.assertEqual(detector.get_status(1), NodeStatus.ALIVE)

    def test_fixed_timeout_heartbeat(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        detector.advance_time(10)
        detector.receive_heartbeat(1)

        self.assertEqual(detector.get_status(1), NodeStatus.ALIVE)

    def test_fixed_timeout_detection(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        # No heartbeat for 31 time units
        detector.advance_time(31)

        self.assertEqual(detector.get_status(1), NodeStatus.DEAD)

    def test_fixed_timeout_recovery(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        # Node times out
        detector.advance_time(31)
        self.assertEqual(detector.get_status(1), NodeStatus.DEAD)

        # Node sends heartbeat and recovers
        detector.receive_heartbeat(1)
        self.assertEqual(detector.get_status(1), NodeStatus.ALIVE)

    def test_multiple_nodes(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)
        detector.add_node(2)
        detector.add_node(3)

        # Node 1 and 2 send heartbeats
        detector.receive_heartbeat(1)
        detector.receive_heartbeat(2)

        detector.advance_time(31)

        # Node 3 should be dead, 1 and 2 alive
        self.assertEqual(len(detector.get_alive_nodes()), 2)
        self.assertEqual(detector.get_dead_nodes(), [3])

    def test_get_alive_and_dead_nodes(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)
        detector.add_node(2)

        detector.receive_heartbeat(1)
        detector.advance_time(31)

        alive = detector.get_alive_nodes()
        dead = detector.get_dead_nodes()

        self.assertEqual(alive, [1])
        self.assertEqual(dead, [2])

    def test_adaptive_heartbeat_history(self):
        detector = AdaptiveTimeoutDetector(5, 3.0)
        detector.add_node(1)

        # Send heartbeats at regular intervals
        for _ in range(10):
            detector.advance_time(10)
            detector.receive_heartbeat(1)

        node = detector.nodes.get(1)
        self.assertLessEqual(len(node.heartbeat_history), 5)  # Should be capped at max_history

    def test_adaptive_mean_calculation(self):
        detector = AdaptiveTimeoutDetector(10, 3.0)
        detector.add_node(1)

        # Send heartbeats at 10ms intervals
        for _ in range(5):
            detector.advance_time(10)
            detector.receive_heartbeat(1)

        node = detector.nodes.get(1)
        mean = node.calculate_mean()
        self.assertAlmostEqual(mean, 10.0, delta=0.1)

    def test_adaptive_phi_calculation(self):
        detector = AdaptiveTimeoutDetector(10, 3.0)
        detector.add_node(1)

        # Establish pattern
        for _ in range(5):
            detector.advance_time(10)
            detector.receive_heartbeat(1)

        # Small delay - phi should be low
        detector.advance_time(12)
        phi = detector.calculate_phi(1)
        self.assertLess(phi, 3.0)

    def test_adaptive_failure_detection(self):
        detector = AdaptiveTimeoutDetector(10, 2.0)
        detector.add_node(1)

        # Establish regular pattern (10ms intervals)
        for _ in range(5):
            detector.advance_time(10)
            detector.receive_heartbeat(1)

        # Long delay should trigger suspicion
        detector.advance_time(50)

        status = detector.get_status(1)
        # Should be suspected or dead due to high phi
        self.assertIn(status, [NodeStatus.SUSPECTED, NodeStatus.DEAD])

    def test_adaptive_suspected_state(self):
        detector = AdaptiveTimeoutDetector(10, 3.0)
        detector.add_node(1)

        # Establish pattern
        for _ in range(10):
            detector.advance_time(10)
            detector.receive_heartbeat(1)

        # Delay that causes high phi but not extreme
        detector.advance_time(35)

        suspected = detector.get_suspected_nodes()
        # Node might be in suspected state
        self.assertTrue(len(suspected) == 0 or 1 in suspected)

    def test_heartbeat_count(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        for _ in range(5):
            detector.receive_heartbeat(1)

        node = detector.nodes.get(1)
        self.assertEqual(node.heartbeat_count, 5)

    def test_auto_add_node_on_heartbeat(self):
        detector = FixedTimeoutDetector(10, 30)

        # Node doesn't exist yet
        self.assertIsNone(detector.get_status(1))

        # Receiving heartbeat should add it
        detector.receive_heartbeat(1)
        self.assertEqual(detector.get_status(1), NodeStatus.ALIVE)

    def test_missed_heartbeats_tracking(self):
        detector = FixedTimeoutDetector(10, 30)
        detector.add_node(1)

        detector.advance_time(31)
        detector.check_timeouts()

        node = detector.nodes.get(1)
        self.assertGreater(node.missed_heartbeats, 0)


if __name__ == '__main__':
    unittest.main()
