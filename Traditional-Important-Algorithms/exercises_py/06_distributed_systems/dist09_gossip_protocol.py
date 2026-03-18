# I AM NOT DONE

"""
dist09_gossip_protocol.py

Gossip Protocol (also called epidemic protocol) spreads information through
a distributed system similar to how gossip or diseases spread in a population.
Nodes periodically exchange information with random peers.

Key properties:
- Eventual consistency: All nodes eventually receive all updates
- Fault tolerance: Works even if some nodes fail or messages are lost
- Scalability: Communication overhead grows logarithmically with cluster size
- No central coordination required

Your task: Implement a gossip protocol for information dissemination.

Key concepts:
- Push gossip: Sender pushes updates to random nodes
- Pull gossip: Receiver pulls updates from random nodes
- Push-Pull: Combination of both (most efficient)
- Fanout: Number of nodes to gossip with per round
- Round: One iteration of gossip exchange
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import unittest


@dataclass
class GossipMessage:
    """A gossip message with versioning."""
    key: str
    value: str
    version: int
    timestamp: int


class GossipNode:
    """A node in the gossip cluster."""

    def __init__(self, node_id: int):
        """Initialize a gossip node."""
        self.id = node_id
        self.data: Dict[str, GossipMessage] = {}
        self.peers: Set[int] = set()
        self.rounds_participated = 0
        self.messages_sent = 0
        self.messages_received = 0

    def add_peer(self, peer_id: int):
        """Add a peer to this node."""
        if peer_id != self.id:
            self.peers.add(peer_id)

    def update(self, key: str, value: str, version: int, timestamp: int) -> bool:
        """
        TODO: Update local data.

        - Only update if version is newer than current version
        - If key doesn't exist, add it
        - Return True if updated, False if ignored (older version)
        """
        pass  # TODO: Implement this

    def get(self, key: str) -> Optional[GossipMessage]:
        """Get a message by key."""
        return self.data.get(key)

    def get_all_data(self) -> List[GossipMessage]:
        """Get all data as a list."""
        return list(self.data.values())


class GossipCluster:
    """A cluster of nodes using gossip protocol."""

    def __init__(self, fanout: int):
        """Initialize the cluster."""
        self.nodes: Dict[int, GossipNode] = {}
        self.current_time = 0
        self.fanout = fanout  # How many random nodes to gossip with
        self.rng_seed = 12345  # For deterministic randomness in tests

    def add_node(self, node_id: int):
        """Add a node to the cluster."""
        self.nodes[node_id] = GossipNode(node_id)

    def connect_all(self):
        """
        TODO: Create a fully connected network.

        - Each node should have all other nodes as peers
        """
        pass  # TODO: Implement this

    def update_node_data(self, node_id: int, key: str, value: str, version: int):
        """
        TODO: Update data on a specific node.

        - Use current_time as timestamp
        - Update the node's local data
        """
        pass  # TODO: Implement this

    def _select_random_peers(self, node_id: int, count: int) -> List[int]:
        """
        TODO: Select random peers for gossip.

        - Get the node's peer list
        - Return up to 'count' random peers
        - Use simple deterministic selection for testing:
          Take first 'count' peers when sorted by ID
        - In real implementation, this would be truly random
        """
        pass  # TODO: Implement this

    def gossip_round_push(self, node_id: int):
        """
        TODO: Perform one round of push-based gossip.

        - Select fanout random peers
        - For each peer, send all of this node's data
        - Peer updates its data based on versions
        - Update statistics (messages_sent, messages_received, rounds_participated)
        """
        pass  # TODO: Implement this

    def gossip_round_pull(self, node_id: int):
        """
        TODO: Perform one round of pull-based gossip.

        - Select fanout random peers
        - For each peer, request all their data
        - Update this node's data based on versions
        - Update statistics
        """
        pass  # TODO: Implement this

    def gossip_round_push_pull(self, node_id: int):
        """
        TODO: Perform one round of push-pull gossip (most efficient).

        - Select fanout random peers
        - For each peer:
          1. Send all this node's data (push)
          2. Receive all peer's data (pull)
          3. Both nodes update their data
        - Update statistics
        """
        pass  # TODO: Implement this

    def run_gossip_round_all(self):
        """
        TODO: Run one gossip round for all nodes.

        - Each node performs push-pull gossip
        - Process nodes in sorted order for deterministic testing
        """
        pass  # TODO: Implement this

    def run_until_convergence(self, max_rounds: int) -> int:
        """
        TODO: Run gossip until all nodes have the same data.

        - Run rounds until convergence or max_rounds reached
        - Return number of rounds needed
        - Convergence: all nodes have same data (same keys with same versions)
        """
        pass  # TODO: Implement this

    def is_converged(self) -> bool:
        """
        TODO: Check if all nodes have converged.

        - All nodes should have the same set of keys
        - For each key, all nodes should have the same version
        """
        pass  # TODO: Implement this

    def get_node(self, node_id: int) -> Optional[GossipNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_convergence_percentage(self) -> float:
        """
        TODO: Calculate what percentage of data has converged.

        - Find all unique keys across all nodes
        - For each key, find the highest version number
        - Count how many nodes have that version
        - Return average percentage across all keys
        """
        pass  # TODO: Implement this

    def advance_time(self, delta: int):
        """Advance time."""
        self.current_time += delta

    def get_time(self) -> int:
        """Get current time."""
        return self.current_time


# Unit Tests
class TestGossipProtocol(unittest.TestCase):

    def test_create_node(self):
        node = GossipNode(1)
        self.assertEqual(node.id, 1)
        self.assertEqual(len(node.data), 0)

    def test_update_local_data(self):
        node = GossipNode(1)

        node.update("key1", "value1", 1, 100)

        msg = node.get("key1")
        self.assertEqual(msg.value, "value1")
        self.assertEqual(msg.version, 1)

    def test_update_with_newer_version(self):
        node = GossipNode(1)

        node.update("key1", "value1", 1, 100)
        node.update("key1", "value2", 2, 200)

        msg = node.get("key1")
        self.assertEqual(msg.value, "value2")
        self.assertEqual(msg.version, 2)

    def test_ignore_older_version(self):
        node = GossipNode(1)

        node.update("key1", "value2", 2, 200)
        node.update("key1", "value1", 1, 100)

        msg = node.get("key1")
        self.assertEqual(msg.value, "value2")  # Should keep newer version
        self.assertEqual(msg.version, 2)

    def test_connect_all(self):
        cluster = GossipCluster(2)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.add_node(2)

        cluster.connect_all()

        node0 = cluster.get_node(0)
        self.assertEqual(len(node0.peers), 2)  # Connected to nodes 1 and 2

    def test_gossip_push(self):
        cluster = GossipCluster(1)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.connect_all()

        cluster.update_node_data(0, "key1", "value1", 1)

        cluster.gossip_round_push(0)

        # Node 1 should have received the data
        node1 = cluster.get_node(1)
        self.assertIsNotNone(node1.get("key1"))

    def test_gossip_pull(self):
        cluster = GossipCluster(1)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.connect_all()

        cluster.update_node_data(1, "key1", "value1", 1)

        cluster.gossip_round_pull(0)

        # Node 0 should have pulled the data
        node0 = cluster.get_node(0)
        self.assertIsNotNone(node0.get("key1"))

    def test_push_pull_bidirectional(self):
        cluster = GossipCluster(1)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.connect_all()

        cluster.update_node_data(0, "key1", "value1", 1)
        cluster.update_node_data(1, "key2", "value2", 1)

        cluster.gossip_round_push_pull(0)

        # Both nodes should have both keys
        node0 = cluster.get_node(0)
        node1 = cluster.get_node(1)

        self.assertIsNotNone(node0.get("key1"))
        self.assertIsNotNone(node0.get("key2"))
        self.assertIsNotNone(node1.get("key1"))
        self.assertIsNotNone(node1.get("key2"))

    def test_convergence(self):
        cluster = GossipCluster(2)

        for i in range(5):
            cluster.add_node(i)
        cluster.connect_all()

        # Add different data to different nodes
        cluster.update_node_data(0, "key1", "value1", 1)
        cluster.update_node_data(1, "key2", "value2", 1)
        cluster.update_node_data(2, "key3", "value3", 1)

        rounds = cluster.run_until_convergence(20)

        self.assertGreater(rounds, 0)
        self.assertTrue(cluster.is_converged())

        # All nodes should have all keys
        for i in range(5):
            node = cluster.get_node(i)
            self.assertIsNotNone(node.get("key1"))
            self.assertIsNotNone(node.get("key2"))
            self.assertIsNotNone(node.get("key3"))

    def test_version_conflict_resolution(self):
        cluster = GossipCluster(2)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.connect_all()

        # Node 0 has older version
        cluster.update_node_data(0, "key1", "old", 1)

        # Node 1 has newer version
        cluster.update_node_data(1, "key1", "new", 2)

        cluster.run_until_convergence(10)

        # Both should have the newer version
        node0 = cluster.get_node(0)
        node1 = cluster.get_node(1)

        self.assertEqual(node0.get("key1").value, "new")
        self.assertEqual(node1.get("key1").value, "new")
        self.assertEqual(node0.get("key1").version, 2)
        self.assertEqual(node1.get("key1").version, 2)

    def test_fanout_limits_connections(self):
        cluster = GossipCluster(2)

        for i in range(10):
            cluster.add_node(i)
        cluster.connect_all()

        cluster.update_node_data(0, "key1", "value1", 1)

        node0 = cluster.get_node(0)
        initial_sent = node0.messages_sent

        cluster.gossip_round_push(0)

        node0 = cluster.get_node(0)
        # Should have gossiped to fanout (2) nodes, not all 9 peers
        self.assertLessEqual(node0.messages_sent - initial_sent, 2 * 10)  # 2 peers * some messages

    def test_statistics_tracking(self):
        cluster = GossipCluster(1)
        cluster.add_node(0)
        cluster.add_node(1)
        cluster.connect_all()

        cluster.update_node_data(0, "key1", "value1", 1)

        cluster.gossip_round_push_pull(0)

        node0 = cluster.get_node(0)
        self.assertGreater(node0.rounds_participated, 0)
        self.assertTrue(node0.messages_sent > 0 or node0.messages_received > 0)

    def test_large_cluster_convergence(self):
        cluster = GossipCluster(3)

        for i in range(20):
            cluster.add_node(i)
        cluster.connect_all()

        # Each node starts with unique data
        for i in range(20):
            cluster.update_node_data(i, f"key{i}", f"value{i}", 1)

        rounds = cluster.run_until_convergence(50)

        # Should converge in logarithmic rounds
        self.assertLess(rounds, 20)  # Should be much less than 50
        self.assertTrue(cluster.is_converged())


if __name__ == '__main__':
    unittest.main()
