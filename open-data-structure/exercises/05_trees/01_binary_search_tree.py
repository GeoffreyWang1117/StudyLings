"""
Binary Search Tree (BST)
=========================

A BST maintains the property: left < parent < right

Operations (average case for balanced tree):
- insert(x): O(log n)
- search(x): O(log n)
- delete(x): O(log n)
- min/max: O(log n)

Worst case (degenerate tree): O(n)

Applications:
- Maintaining sorted data
- Range queries
- Ordered iteration
"""


class Node:
    """A node in the BST"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    """Binary Search Tree implementation"""

    def __init__(self):
        """Initialize empty BST"""
        # TODO: Initialize root
        pass

    def insert(self, data):
        """
        Insert a value into the BST.

        Args:
            data: The value to insert

        Time Complexity: O(log n) average, O(n) worst
        """
        # TODO: Implement insert (recursive or iterative)
        pass

    def search(self, data) -> bool:
        """
        Search for a value.

        Args:
            data: The value to search for

        Returns:
            True if found, False otherwise

        Time Complexity: O(log n) average
        """
        # TODO: Implement search
        pass

    def delete(self, data):
        """
        Delete a value from the BST.

        Args:
            data: The value to delete

        Time Complexity: O(log n) average
        """
        # TODO: Implement delete
        # Cases: no children, one child, two children
        # For two children: replace with inorder successor
        pass

    def find_min(self):
        """
        Find the minimum value.

        Returns:
            The minimum value

        Raises:
            ValueError: If tree is empty

        Time Complexity: O(log n)
        """
        # TODO: Go left until you can't
        pass

    def find_max(self):
        """
        Find the maximum value.

        Returns:
            The maximum value

        Raises:
            ValueError: If tree is empty

        Time Complexity: O(log n)
        """
        # TODO: Go right until you can't
        pass

    def inorder(self) -> list:
        """
        Inorder traversal (left, root, right).

        Returns:
            List of values in sorted order

        Time Complexity: O(n)
        """
        # TODO: Implement inorder traversal
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test insert and search"""
    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)

    assert bst.search(5) == True
    assert bst.search(3) == True
    assert bst.search(7) == True
    assert bst.search(10) == False


def test_inorder():
    """Test inorder traversal gives sorted order"""
    bst = BST()
    values = [5, 3, 7, 1, 9, 4, 6]

    for val in values:
        bst.insert(val)

    assert bst.inorder() == sorted(values)


def test_find_min_max():
    """Test finding min and max"""
    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(9)

    assert bst.find_min() == 1
    assert bst.find_max() == 9


def test_delete_leaf():
    """Test deleting a leaf node"""
    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)

    bst.delete(3)
    assert bst.search(3) == False
    assert bst.inorder() == [5, 7]


def test_delete_one_child():
    """Test deleting node with one child"""
    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(1)

    bst.delete(3)
    assert bst.search(3) == False
    assert bst.inorder() == [1, 5]


def test_delete_two_children():
    """Test deleting node with two children"""
    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)

    bst.delete(3)
    assert bst.search(3) == False
    assert bst.inorder() == [1, 4, 5, 7]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
