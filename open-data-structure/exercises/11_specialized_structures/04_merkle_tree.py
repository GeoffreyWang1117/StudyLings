"""
Merkle Tree (Hash Tree)
=======================

A Merkle Tree is a tree where each node is labeled with a cryptographic
hash. Leaf nodes contain data hashes, internal nodes contain hashes of
their children.

Structure:
- Binary tree
- Leaves: hash(data)
- Internal nodes: hash(left_hash + right_hash)
- Root: Merkle root (represents entire dataset)

Operations:
- Build tree: O(n)
- Verify element: O(log n) - requires log n hashes (Merkle proof)
- Update element: O(log n)

Properties:
- Any change in data changes the root hash
- Can verify subset of data without full dataset
- Efficient data integrity verification

Applications:
- Blockchain (Bitcoin, Ethereum)
- Git version control
- Distributed databases (Cassandra, DynamoDB)
- IPFS file system
- Certificate transparency
- Peer-to-peer networks
"""


import hashlib


class MerkleNode:
    """A node in the Merkle tree"""

    def __init__(self, data=None, left=None, right=None):
        self.data = data        # Original data (for leaves)
        self.hash = None        # Hash value
        self.left = left        # Left child
        self.right = right      # Right child

    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return self.left is None and self.right is None


class MerkleTree:
    """
    Merkle Tree for cryptographic verification.
    """

    def __init__(self, data_blocks: list):
        """
        Build Merkle tree from data blocks.

        Args:
            data_blocks: List of data items (strings or bytes)
        """
        # TODO: Build tree from data
        self.leaves = []
        self.root = self._build_tree(data_blocks)

    def _hash(self, data) -> str:
        """
        Compute SHA-256 hash of data.

        Args:
            data: Data to hash (string or bytes)

        Returns:
            Hex digest of hash
        """
        # TODO: Compute hash
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def _build_tree(self, data_blocks: list) -> MerkleNode:
        """
        Recursively build Merkle tree.

        Args:
            data_blocks: List of data blocks

        Returns:
            Root node of tree
        """
        # TODO: Build tree bottom-up
        # Base case: empty data
        if not data_blocks:
            return None

        # Create leaf nodes
        # If odd number of nodes, duplicate last one
        # Build parent level by hashing pairs
        # Repeat until only root remains
        pass

    def get_root_hash(self) -> str:
        """
        Get the Merkle root hash.

        Returns:
            Root hash (hex string)

        Time Complexity: O(1)
        """
        # TODO: Return root hash
        return self.root.hash if self.root else None

    def get_proof(self, index: int) -> list:
        """
        Get Merkle proof for element at index.

        Proof is list of hashes needed to verify element.

        Args:
            index: Index of element

        Returns:
            List of (hash, direction) tuples
            direction is 'left' or 'right'

        Time Complexity: O(log n)
        """
        # TODO: Collect sibling hashes on path to root
        # Track whether sibling is on left or right
        pass

    @staticmethod
    def verify_proof(data, index: int, proof: list, root_hash: str) -> bool:
        """
        Verify that data at index produces root_hash with given proof.

        Args:
            data: The data element
            index: Index of element
            proof: Merkle proof (from get_proof)
            root_hash: Expected root hash

        Returns:
            True if proof is valid

        Time Complexity: O(log n)
        """
        # TODO: Recompute hash using proof
        # Start with hash(data)
        # For each (hash, direction) in proof:
        #   If direction == 'left': current = hash(hash + current)
        #   Else: current = hash(current + hash)
        # Check if final hash equals root_hash
        pass

    def update(self, index: int, new_data):
        """
        Update data at index and recompute affected hashes.

        Args:
            index: Index to update
            new_data: New data value

        Time Complexity: O(log n)
        """
        # TODO: Update leaf and recompute hashes up to root
        pass

    def verify_tree(self) -> bool:
        """
        Verify integrity of entire tree.

        Returns:
            True if all hashes are correct

        Time Complexity: O(n)
        """
        # TODO: Recursively verify all nodes
        return self._verify_node(self.root)

    def _verify_node(self, node: MerkleNode) -> bool:
        """Verify a single node's hash"""
        # TODO: Check if node's hash matches computed hash
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_build_merkle_tree():
    """Test building Merkle tree"""
    data = ["block1", "block2", "block3", "block4"]
    tree = MerkleTree(data)

    assert tree.get_root_hash() is not None
    assert len(tree.get_root_hash()) == 64  # SHA-256 produces 64 hex chars


def test_merkle_proof():
    """Test generating and verifying Merkle proof"""
    data = ["tx1", "tx2", "tx3", "tx4"]
    tree = MerkleTree(data)

    # Get proof for index 1
    proof = tree.get_proof(1)
    root_hash = tree.get_root_hash()

    # Verify proof
    assert MerkleTree.verify_proof("tx2", 1, proof, root_hash) == True

    # Wrong data should fail
    assert MerkleTree.verify_proof("tx_wrong", 1, proof, root_hash) == False


def test_update():
    """Test updating data"""
    data = ["a", "b", "c", "d"]
    tree = MerkleTree(data)
    old_root = tree.get_root_hash()

    # Update element
    tree.update(1, "b_modified")
    new_root = tree.get_root_hash()

    # Root should change
    assert old_root != new_root

    # Proof for updated element should verify
    proof = tree.get_proof(1)
    assert MerkleTree.verify_proof("b_modified", 1, proof, new_root) == True


def test_tamper_detection():
    """Test that tampering is detected"""
    data = ["block1", "block2", "block3", "block4"]
    tree = MerkleTree(data)

    proof = tree.get_proof(2)
    root_hash = tree.get_root_hash()

    # Tampered data should fail verification
    tampered_data = "block2_tampered"
    assert MerkleTree.verify_proof(tampered_data, 2, proof, root_hash) == False


def test_odd_number_of_blocks():
    """Test with odd number of data blocks"""
    data = ["a", "b", "c"]  # Odd number
    tree = MerkleTree(data)

    assert tree.get_root_hash() is not None

    # Should be able to verify all blocks
    for i in range(len(data)):
        proof = tree.get_proof(i)
        assert MerkleTree.verify_proof(data[i], i, proof, tree.get_root_hash()) == True


def test_single_block():
    """Test with single data block"""
    data = ["only_block"]
    tree = MerkleTree(data)

    root_hash = tree.get_root_hash()
    proof = tree.get_proof(0)

    assert MerkleTree.verify_proof("only_block", 0, proof, root_hash) == True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
