"""
Splay Tree
==========

A self-adjusting binary search tree where recently accessed
elements are quick to access again.

Key operation: SPLAY
- Move accessed node to root via rotations
- Frequently accessed items stay near top
- Amortized O(log n) per operation

Rotations:
- Zig: Single rotation (when parent is root)
- Zig-Zig: Double rotation (same direction)
- Zig-Zag: Double rotation (different directions)

Operations (all amortized O(log n)):
- insert(x)
- search(x)
- delete(x)
- find_min/max()

Applications:
- Caching (LRU-like behavior)
- Network routing
- Garbage collection
- When access patterns are non-uniform
"""


class Node:
    """A node in the splay tree"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    """
    Splay Tree implementation with amortized O(log n) operations.
    """

    def __init__(self):
        """Initialize empty splay tree"""
        self.root = None

    def _rotate_right(self, node: Node):
        """
        Right rotation (zig when node is left child).

              y                x
             / \              / \
            x   C    =>      A   y
           / \                  / \
          A   B                B   C
        """
        # TODO: Implement right rotation
        # Update parent pointers
        pass

    def _rotate_left(self, node: Node):
        """
        Left rotation (zig when node is right child).

            x                  y
           / \                / \
          A   y      =>      x   C
             / \            / \
            B   C          A   B
        """
        # TODO: Implement left rotation
        # Update parent pointers
        pass

    def _splay(self, node: Node):
        """
        Splay node to root using rotations.

        Three cases:
        1. Zig: parent is root (single rotation)
        2. Zig-Zig: parent and grandparent in same direction
        3. Zig-Zag: parent and grandparent in different directions
        """
        # TODO: Implement splay operation
        # While node is not root:
        #   If parent is root: Zig
        #   Elif same direction: Zig-Zig
        #   Else: Zig-Zag
        pass

    def search(self, data) -> bool:
        """
        Search for a value and splay it to root.

        Args:
            data: The value to search for

        Returns:
            True if found, False otherwise

        Time Complexity: O(log n) amortized
        """
        # TODO: Standard BST search
        # If found, splay that node to root
        # If not found, splay last accessed node
        pass

    def insert(self, data):
        """
        Insert a value and splay it to root.

        Args:
            data: The value to insert

        Time Complexity: O(log n) amortized
        """
        # TODO: Standard BST insert
        # Splay the new node to root
        pass

    def delete(self, data) -> bool:
        """
        Delete a value.

        Args:
            data: The value to delete

        Returns:
            True if deleted, False if not found

        Time Complexity: O(log n) amortized
        """
        # TODO: Splay node to root
        # If found:
        #   Split into left and right subtrees
        #   Join them (splay max of left subtree, attach right)
        pass

    def find_min(self):
        """
        Find minimum value and splay it to root.

        Returns:
            Minimum value

        Time Complexity: O(log n) amortized
        """
        # TODO: Go left until can't
        # Splay to root
        pass

    def find_max(self):
        """
        Find maximum value and splay it to root.

        Returns:
            Maximum value

        Time Complexity: O(log n) amortized
        """
        # TODO: Go right until can't
        # Splay to root
        pass

    def inorder(self) -> list:
        """Inorder traversal (for testing)"""
        # TODO: Standard inorder traversal
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic insert and search"""
    tree = SplayTree()
    tree.insert(50)
    tree.insert(30)
    tree.insert(70)
    tree.insert(20)
    tree.insert(40)

    assert tree.search(30) == True
    assert tree.search(100) == False

    # After search, 30 should be at root
    assert tree.root.data == 30


def test_splay_on_access():
    """Test that accessed nodes move to root"""
    tree = SplayTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(val)

    # Access 20 (deep in tree)
    tree.search(20)

    # 20 should now be at root
    assert tree.root.data == 20


def test_delete():
    """Test deletion"""
    tree = SplayTree()
    tree.insert(50)
    tree.insert(30)
    tree.insert(70)
    tree.insert(20)
    tree.insert(40)

    assert tree.delete(30) == True
    assert tree.search(30) == False

    # Other elements should still exist
    assert tree.search(50) == True
    assert tree.search(70) == True


def test_find_min_max():
    """Test finding min and max"""
    tree = SplayTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for val in values:
        tree.insert(val)

    assert tree.find_min() == 20
    assert tree.root.data == 20  # Min should be splayed to root

    assert tree.find_max() == 80
    assert tree.root.data == 80  # Max should be splayed to root


def test_repeated_access():
    """Test that repeated access keeps elements near top"""
    tree = SplayTree()
    for i in range(100):
        tree.insert(i)

    # Access elements 10-15 repeatedly
    for _ in range(5):
        for i in range(10, 16):
            tree.search(i)

    # These elements should be near root (fast access)
    # Let's verify by counting rotations needed
    # (In a balanced tree, would need ~log(100) ≈ 7 rotations)


def test_sorted_order():
    """Test that inorder gives sorted result"""
    tree = SplayTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for val in values:
        tree.insert(val)

    assert tree.inorder() == sorted(values)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
