"""
Tree Traversal Methods
=======================

Different ways to traverse a binary tree:

1. Inorder (Left, Root, Right)
   - For BST: gives sorted order
   - Use: Expression trees (infix notation)

2. Preorder (Root, Left, Right)
   - Use: Creating a copy of tree
   - Use: Prefix notation

3. Postorder (Left, Right, Root)
   - Use: Deleting tree
   - Use: Postfix notation

4. Level-order (Breadth-first)
   - Use: Finding shortest path
   - Use: Level-by-level processing

Time Complexity: All are O(n)
"""


class Node:
    """A node in a binary tree"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def inorder_traversal(root: Node) -> list:
    """
    Inorder traversal: Left, Root, Right

    Args:
        root: Root of the tree

    Returns:
        List of values in inorder

    Time Complexity: O(n)
    """
    # TODO: Implement inorder traversal (recursive)
    pass


def preorder_traversal(root: Node) -> list:
    """
    Preorder traversal: Root, Left, Right

    Args:
        root: Root of the tree

    Returns:
        List of values in preorder

    Time Complexity: O(n)
    """
    # TODO: Implement preorder traversal (recursive)
    pass


def postorder_traversal(root: Node) -> list:
    """
    Postorder traversal: Left, Right, Root

    Args:
        root: Root of the tree

    Returns:
        List of values in postorder

    Time Complexity: O(n)
    """
    # TODO: Implement postorder traversal (recursive)
    pass


def levelorder_traversal(root: Node) -> list:
    """
    Level-order traversal (breadth-first).

    Args:
        root: Root of the tree

    Returns:
        List of values level by level

    Time Complexity: O(n)
    """
    # TODO: Implement level-order traversal
    # Hint: Use a queue
    pass


def tree_height(root: Node) -> int:
    """
    Calculate the height of a tree.

    Height = longest path from root to leaf.

    Args:
        root: Root of the tree

    Returns:
        Height (0 for single node, -1 for empty tree)

    Time Complexity: O(n)
    """
    # TODO: Implement height calculation (recursive)
    pass


def count_nodes(root: Node) -> int:
    """
    Count the number of nodes in the tree.

    Args:
        root: Root of the tree

    Returns:
        Number of nodes

    Time Complexity: O(n)
    """
    # TODO: Implement node counting (recursive)
    pass


def is_bst(root: Node, min_val=float('-inf'), max_val=float('inf')) -> bool:
    """
    Check if a binary tree is a valid BST.

    Args:
        root: Root of the tree
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid BST, False otherwise

    Time Complexity: O(n)
    """
    # TODO: Implement BST validation
    # Each node must be: min_val < node.data < max_val
    # Recursively check left and right subtrees
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def build_tree():
    """
    Build a sample tree:
           4
          / \
         2   6
        / \ / \
       1  3 5  7
    """
    root = Node(4)
    root.left = Node(2)
    root.right = Node(6)
    root.left.left = Node(1)
    root.left.right = Node(3)
    root.right.left = Node(5)
    root.right.right = Node(7)
    return root


def test_inorder():
    """Test inorder traversal"""
    root = build_tree()
    assert inorder_traversal(root) == [1, 2, 3, 4, 5, 6, 7]


def test_preorder():
    """Test preorder traversal"""
    root = build_tree()
    assert preorder_traversal(root) == [4, 2, 1, 3, 6, 5, 7]


def test_postorder():
    """Test postorder traversal"""
    root = build_tree()
    assert postorder_traversal(root) == [1, 3, 2, 5, 7, 6, 4]


def test_levelorder():
    """Test level-order traversal"""
    root = build_tree()
    assert levelorder_traversal(root) == [4, 2, 6, 1, 3, 5, 7]


def test_height():
    """Test tree height calculation"""
    root = build_tree()
    assert tree_height(root) == 2

    single = Node(1)
    assert tree_height(single) == 0

    assert tree_height(None) == -1


def test_count_nodes():
    """Test node counting"""
    root = build_tree()
    assert count_nodes(root) == 7

    single = Node(1)
    assert count_nodes(single) == 1

    assert count_nodes(None) == 0


def test_is_bst():
    """Test BST validation"""
    # Valid BST
    root = build_tree()
    assert is_bst(root) == True

    # Invalid BST
    invalid = Node(4)
    invalid.left = Node(2)
    invalid.right = Node(6)
    invalid.left.right = Node(5)  # Violates BST property!

    assert is_bst(invalid) == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
