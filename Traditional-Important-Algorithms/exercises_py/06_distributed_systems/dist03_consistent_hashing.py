# I AM NOT DONE

"""
dist03_consistent_hashing.py

Consistent Hashing is a distributed hashing scheme that minimizes key
redistribution when nodes are added or removed. It's crucial for distributed
caches, databases, and load balancers.

Key properties:
- When a node is added/removed, only K/n keys need to be remapped (K=total keys, n=nodes)
- Contrast with traditional hashing where almost all keys need remapping
- Virtual nodes improve load distribution

Your task: Implement a consistent hash ring with virtual nodes.

Key concepts:
- Hash ring: Circular space of hash values (0 to 2^32-1)
- Virtual nodes: Multiple positions per physical node for better distribution
- Key lookup: Find the first node clockwise from the key's hash
- Minimal disruption on topology changes
"""

from typing import Dict, List, Optional, Set
import hashlib
import unittest


def hash_value(data: str) -> int:
    """Hash a string to a 64-bit integer."""
    return int(hashlib.md5(data.encode()).hexdigest(), 16)


class Node:
    """A physical node in the hash ring."""

    def __init__(self, node_id: str):
        """Initialize a node."""
        self.id = node_id
        self.keys: Set[str] = set()


class ConsistentHashRing:
    """Consistent hash ring with virtual nodes."""

    def __init__(self, virtual_nodes: int):
        """Initialize the hash ring."""
        self.ring: Dict[int, str] = {}  # hash -> node_id (virtual nodes)
        self.nodes: Dict[str, Node] = {}  # node_id -> node
        self.virtual_nodes = virtual_nodes
        self.key_mapping: Dict[str, str] = {}  # key -> node_id for quick lookup

    def add_node(self, node_id: str):
        """
        TODO: Add a physical node with its virtual nodes.

        - Create virtual_nodes number of entries in the ring
        - Virtual node hash: hash(node_id + "#" + str(replica_number))
        - Add to nodes dict
        - Redistribute keys that now belong to this node
        """
        pass  # TODO: Implement this

    def remove_node(self, node_id: str):
        """
        TODO: Remove a physical node and all its virtual nodes.

        - Remove all virtual nodes from the ring
        - Redistribute keys to successor nodes
        - Remove from nodes dict
        """
        pass  # TODO: Implement this

    def get_node(self, key: str) -> Optional[str]:
        """
        TODO: Find which node should store this key.

        - Hash the key
        - Find the first virtual node at or after this hash (clockwise)
        - If no node found after hash, wrap around to first node
        - Return the physical node ID (not virtual node)
        - Return None if no nodes in ring
        """
        pass  # TODO: Implement this

    def add_key(self, key: str) -> Optional[str]:
        """
        TODO: Add a key to the appropriate node.

        - Determine which node should store the key
        - Add key to that node's key set
        - Update key_mapping
        - Return the node_id where key was added
        """
        pass  # TODO: Implement this

    def remove_key(self, key: str) -> bool:
        """
        TODO: Remove a key from its node.

        - Find which node has the key
        - Remove from node's key set
        - Remove from key_mapping
        - Return True if key was found and removed
        """
        pass  # TODO: Implement this

    def get_key_location(self, key: str) -> Optional[str]:
        """Get the node ID where a key is stored."""
        return self.key_mapping.get(key)

    def get_node_info(self, node_id: str) -> Optional[Node]:
        """Get information about a node."""
        return self.nodes.get(node_id)

    def get_node_count(self) -> int:
        """Get the number of physical nodes."""
        return len(self.nodes)

    def get_virtual_node_count(self) -> int:
        """Get the number of virtual nodes."""
        return len(self.ring)

    def get_all_nodes(self) -> List[str]:
        """Get all node IDs."""
        return list(self.nodes.keys())

    def get_distribution(self) -> Dict[str, int]:
        """Return how many keys each node has."""
        return {node_id: len(node.keys) for node_id, node in self.nodes.items()}


# Unit Tests
class TestConsistentHashing(unittest.TestCase):

    def test_add_single_node(self):
        ring = ConsistentHashRing(3)
        ring.add_node("node1")

        self.assertEqual(ring.get_node_count(), 1)
        self.assertEqual(ring.get_virtual_node_count(), 3)

    def test_add_multiple_nodes(self):
        ring = ConsistentHashRing(5)
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")

        self.assertEqual(ring.get_node_count(), 3)
        self.assertEqual(ring.get_virtual_node_count(), 15)  # 3 nodes * 5 virtual nodes

    def test_get_node_for_key(self):
        ring = ConsistentHashRing(100)
        ring.add_node("node1")
        ring.add_node("node2")

        node = ring.get_node("my_key")
        self.assertIsNotNone(node)
        self.assertIn(node, ["node1", "node2"])

    def test_consistent_key_mapping(self):
        ring = ConsistentHashRing(100)
        ring.add_node("node1")
        ring.add_node("node2")

        # Same key should always map to same node
        node1 = ring.get_node("test_key")
        node2 = ring.get_node("test_key")
        self.assertEqual(node1, node2)

    def test_add_and_retrieve_keys(self):
        ring = ConsistentHashRing(50)
        ring.add_node("node1")
        ring.add_node("node2")

        ring.add_key("key1")
        ring.add_key("key2")
        ring.add_key("key3")

        self.assertIsNotNone(ring.get_key_location("key1"))
        self.assertIsNotNone(ring.get_key_location("key2"))
        self.assertIsNotNone(ring.get_key_location("key3"))

    def test_minimal_redistribution_on_add(self):
        ring = ConsistentHashRing(100)
        ring.add_node("node1")
        ring.add_node("node2")

        # Add 100 keys
        for i in range(100):
            ring.add_key(f"key{i}")

        # Track original distribution
        dist_before = ring.get_distribution()

        # Add a new node
        ring.add_node("node3")

        # Track new distribution
        dist_after = ring.get_distribution()

        # Most keys should stay on their original nodes
        node1_before = dist_before.get("node1", 0)
        node2_before = dist_before.get("node2", 0)
        node1_after = dist_after.get("node1", 0)
        node2_after = dist_after.get("node2", 0)

        # Each original node should have lost some keys but not all
        self.assertLess(node1_after, node1_before)
        self.assertLess(node2_after, node2_before)
        self.assertGreater(node1_after, 0)
        self.assertGreater(node2_after, 0)

        # New node should have some keys
        node3_after = dist_after.get("node3", 0)
        self.assertGreater(node3_after, 0)

    def test_remove_node_redistribution(self):
        ring = ConsistentHashRing(100)
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")

        # Add keys
        for i in range(90):
            ring.add_key(f"key{i}")

        # Remove a node
        ring.remove_node("node2")

        self.assertEqual(ring.get_node_count(), 2)

        # All keys should still be accessible
        for i in range(90):
            self.assertIsNotNone(ring.get_key_location(f"key{i}"))

        # Keys should only be on node1 and node3
        dist = ring.get_distribution()
        self.assertNotIn("node2", dist)
        self.assertGreater(dist.get("node1", 0), 0)
        self.assertGreater(dist.get("node3", 0), 0)

    def test_load_distribution_with_virtual_nodes(self):
        ring = ConsistentHashRing(150)
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")

        # Add many keys
        for i in range(300):
            ring.add_key(f"key{i}")

        dist = ring.get_distribution()

        # With enough virtual nodes, distribution should be relatively balanced
        # Each node should have roughly 100 keys (±30%)
        for count in dist.values():
            self.assertGreater(count, 70)
            self.assertLess(count, 130)

    def test_remove_key(self):
        ring = ConsistentHashRing(50)
        ring.add_node("node1")
        ring.add_key("test_key")

        self.assertIsNotNone(ring.get_key_location("test_key"))

        self.assertTrue(ring.remove_key("test_key"))
        self.assertIsNone(ring.get_key_location("test_key"))

        self.assertFalse(ring.remove_key("test_key"))  # Already removed

    def test_no_nodes(self):
        ring = ConsistentHashRing(100)
        self.assertIsNone(ring.get_node("any_key"))

    def test_virtual_nodes_improve_distribution(self):
        # Test with few virtual nodes
        ring_few = ConsistentHashRing(1)
        ring_few.add_node("node1")
        ring_few.add_node("node2")
        ring_few.add_node("node3")

        for i in range(300):
            ring_few.add_key(f"key{i}")

        dist_few = ring_few.get_distribution()
        counts_few = list(dist_few.values())
        max_few = max(counts_few)
        min_few = min(counts_few)
        variance_few = max_few - min_few

        # Test with many virtual nodes
        ring_many = ConsistentHashRing(150)
        ring_many.add_node("node1")
        ring_many.add_node("node2")
        ring_many.add_node("node3")

        for i in range(300):
            ring_many.add_key(f"key{i}")

        dist_many = ring_many.get_distribution()
        counts_many = list(dist_many.values())
        max_many = max(counts_many)
        min_many = min(counts_many)
        variance_many = max_many - min_many

        # More virtual nodes should reduce variance
        self.assertLess(variance_many, variance_few)

    def test_single_node_gets_all_keys(self):
        ring = ConsistentHashRing(50)
        ring.add_node("node1")

        for i in range(100):
            ring.add_key(f"key{i}")

        dist = ring.get_distribution()
        self.assertEqual(dist.get("node1"), 100)


if __name__ == '__main__':
    unittest.main()
