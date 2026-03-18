"""
Radix Tree (Patricia Trie)
===========================

A space-optimized trie where nodes with single child are merged.
Also called Patricia Trie or Compact Prefix Tree.

Differences from Trie:
- Edges labeled with strings (not single characters)
- Fewer nodes (more space-efficient)
- Same time complexity but better constants

Operations:
- insert(key): O(k) where k = key length
- search(key): O(k)
- delete(key): O(k)
- Space: O(n) where n = total chars (vs O(n*k) for trie)

Applications:
- IP routing tables (longest prefix match)
- Inverted indexes
- Memory-efficient autocomplete
- Linux kernel (dcache for filesystem)
- Git's packfile index
"""


class RadixNode:
    """A node in the radix tree"""

    def __init__(self, edge_label=""):
        self.edge_label = edge_label  # String on edge to this node
        self.children = {}             # First char -> child node
        self.is_end = False           # Marks end of a key
        self.value = None             # Associated value


class RadixTree:
    """
    Radix Tree (Patricia Trie) implementation.
    """

    def __init__(self):
        """Initialize empty radix tree"""
        self.root = RadixNode()

    def insert(self, key: str, value=None):
        """
        Insert a key-value pair.

        Args:
            key: The key string
            value: Associated value

        Time Complexity: O(k) where k = len(key)
        """
        # TODO: Insert with edge compression
        # Start from root
        # Find matching child by first character
        # Determine common prefix with edge label
        # Split edge if needed
        pass

    def _find_common_prefix(self, s1: str, s2: str) -> str:
        """Find longest common prefix of two strings"""
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[:i]

    def search(self, key: str):
        """
        Search for a key.

        Args:
            key: The key to search for

        Returns:
            Associated value if found, None otherwise

        Time Complexity: O(k)
        """
        # TODO: Traverse tree following edge labels
        # Must match complete key and end at is_end=True node
        pass

    def delete(self, key: str) -> bool:
        """
        Delete a key.

        Args:
            key: The key to delete

        Returns:
            True if deleted, False if not found

        Time Complexity: O(k)
        """
        # TODO: Delete key and compress tree
        # After deletion, merge nodes if needed
        pass

    def starts_with(self, prefix: str) -> list:
        """
        Find all keys starting with prefix.

        Args:
            prefix: The prefix

        Returns:
            List of keys with that prefix

        Time Complexity: O(k + m) where m = total length of results
        """
        # TODO: Navigate to prefix node
        # Collect all keys in subtree
        pass

    def longest_prefix(self, text: str) -> str:
        """
        Find longest prefix of text that exists in tree.

        Args:
            text: The text

        Returns:
            Longest matching prefix

        Time Complexity: O(k)
        """
        # TODO: Follow tree as far as possible
        # Return longest valid prefix found
        pass

    def _collect_keys(self, node: RadixNode, prefix: str, results: list):
        """
        Recursively collect all keys from subtree.

        Args:
            node: Current node
            prefix: Current prefix
            results: List to append results to
        """
        if node.is_end:
            results.append(prefix)

        for char, child in node.children.items():
            self._collect_keys(child, prefix + child.edge_label, results)

    def keys(self) -> list:
        """
        Get all keys in tree.

        Returns:
            List of all keys
        """
        results = []
        self._collect_keys(self.root, "", results)
        return results


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic insert and search"""
    tree = RadixTree()
    tree.insert("test", 1)
    tree.insert("testing", 2)
    tree.insert("tester", 3)

    assert tree.search("test") == 1
    assert tree.search("testing") == 2
    assert tree.search("tester") == 3
    assert tree.search("tes") is None


def test_edge_splitting():
    """Test that edges are split correctly"""
    tree = RadixTree()
    tree.insert("test", 1)
    tree.insert("team", 2)

    assert tree.search("test") == 1
    assert tree.search("team") == 2
    # "te" is common prefix, edges should be split


def test_delete():
    """Test deletion"""
    tree = RadixTree()
    tree.insert("test", 1)
    tree.insert("testing", 2)

    assert tree.delete("test") == True
    assert tree.search("test") is None
    assert tree.search("testing") == 2  # Should still exist


def test_starts_with():
    """Test prefix search"""
    tree = RadixTree()
    tree.insert("apple", 1)
    tree.insert("application", 2)
    tree.insert("apply", 3)
    tree.insert("orange", 4)

    results = tree.starts_with("app")
    assert set(results) == {"apple", "application", "apply"}

    results = tree.starts_with("or")
    assert results == ["orange"]


def test_longest_prefix():
    """Test longest prefix matching"""
    tree = RadixTree()
    tree.insert("test", 1)
    tree.insert("testing", 2)

    assert tree.longest_prefix("testify") == "test"
    assert tree.longest_prefix("testing123") == "testing"
    assert tree.longest_prefix("xyz") == ""


def test_empty_string():
    """Test with empty string"""
    tree = RadixTree()
    tree.insert("", 0)
    tree.insert("test", 1)

    assert tree.search("") == 0
    assert tree.search("test") == 1


def test_ip_routing():
    """Test IP routing table use case"""
    # Simulate routing table
    tree = RadixTree()
    tree.insert("192.168", "local")
    tree.insert("192.168.1", "subnet1")
    tree.insert("10.0", "private")

    # Longest prefix match
    assert tree.longest_prefix("192.168.1.100") == "192.168.1"
    assert tree.longest_prefix("192.168.2.1") == "192.168"
    assert tree.longest_prefix("10.0.0.1") == "10.0"


def test_keys():
    """Test getting all keys"""
    tree = RadixTree()
    keys = ["apple", "app", "application", "banana"]

    for key in keys:
        tree.insert(key, 1)

    assert set(tree.keys()) == set(keys)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
