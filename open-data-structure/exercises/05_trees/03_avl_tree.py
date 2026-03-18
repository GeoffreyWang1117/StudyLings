"""
AVL Tree (Balanced BST)
========================

An AVL tree is a self-balancing BST where the heights of left and right
subtrees differ by at most 1.

Balance factor = height(left) - height(right)
Must be in {-1, 0, 1}

Rotations:
- Left rotation (RR case)
- Right rotation (LL case)
- Left-Right rotation (LR case)
- Right-Left rotation (RL case)

Operations (all O(log n)):
- insert(x)
- delete(x)
- search(x)

Applications:
- When you need guaranteed O(log n) operations
- In-memory databases
- File systems
"""


class Node:
    """A node in an AVL tree"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 0


class AVLTree:
    """AVL Tree implementation"""

    def __init__(self):
        """Initialize empty AVL tree"""
        self.root = None

    def _height(self, node: Node) -> int:
        """Get height of node"""
        return node.height if node else -1

    def _update_height(self, node: Node):
        """Update height of node"""
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Node) -> int:
        """Get balance factor of node"""
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: Node) -> Node:
        """
        Right rotation:
            y              x
           / \            / \
          x   C   =>     A   y
         / \                / \
        A   B              B   C
        """
        # TODO: Implement right rotation
        pass

    def _rotate_left(self, x: Node) -> Node:
        """
        Left rotation:
          x                y
         / \              / \
        A   y     =>     x   C
           / \          / \
          B   C        A   B
        """
        # TODO: Implement left rotation
        pass

    def _rebalance(self, node: Node) -> Node:
        """
        Rebalance node if needed.

        Returns:
            The new root of this subtree
        """
        # TODO: Implement rebalancing
        # 1. Update height
        # 2. Check balance factor
        # 3. Perform rotations if needed:
        #    - LL case (bf > 1, left.bf >= 0): rotate right
        #    - RR case (bf < -1, right.bf <= 0): rotate left
        #    - LR case (bf > 1, left.bf < 0): rotate left then right
        #    - RL case (bf < -1, right.bf > 0): rotate right then left
        pass

    def insert(self, data):
        """
        Insert a value.

        Args:
            data: The value to insert

        Time Complexity: O(log n)
        """
        self.root = self._insert(self.root, data)

    def _insert(self, node: Node, data) -> Node:
        """
        Recursive insert helper.

        Returns:
            The new root of this subtree
        """
        # TODO: Implement insert
        # 1. Standard BST insert
        # 2. Update height
        # 3. Rebalance
        pass

    def search(self, data) -> bool:
        """Search for a value"""
        # TODO: Standard BST search
        pass

    def inorder(self) -> list:
        """Inorder traversal"""
        # TODO: Standard inorder traversal
        pass

    def is_balanced(self) -> bool:
        """Check if tree is balanced"""
        def check(node):
            if not node:
                return True
            bf = self._balance_factor(node)
            if abs(bf) > 1:
                return False
            return check(node.left) and check(node.right)

        return check(self.root)


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test insert and search"""
    avl = AVLTree()
    avl.insert(10)
    avl.insert(20)
    avl.insert(30)  # Should trigger rotation

    assert avl.search(10) == True
    assert avl.search(20) == True
    assert avl.search(30) == True
    assert avl.search(40) == False


def test_balance_after_inserts():
    """Test that tree remains balanced"""
    avl = AVLTree()

    # Insert in ascending order (would create degenerate BST)
    for i in range(10):
        avl.insert(i)

    # Tree should still be balanced
    assert avl.is_balanced() == True


def test_sorted_order():
    """Test inorder gives sorted result"""
    avl = AVLTree()
    values = [50, 25, 75, 10, 30, 60, 80, 5, 15]

    for val in values:
        avl.insert(val)

    assert avl.inorder() == sorted(values)


def test_rotations():
    """Test different rotation cases"""
    # LL case
    avl1 = AVLTree()
    avl1.insert(3)
    avl1.insert(2)
    avl1.insert(1)  # Triggers right rotation
    assert avl1.is_balanced() == True

    # RR case
    avl2 = AVLTree()
    avl2.insert(1)
    avl2.insert(2)
    avl2.insert(3)  # Triggers left rotation
    assert avl2.is_balanced() == True

    # LR case
    avl3 = AVLTree()
    avl3.insert(3)
    avl3.insert(1)
    avl3.insert(2)  # Triggers left-right rotation
    assert avl3.is_balanced() == True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
