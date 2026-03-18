"""
Rope Data Structure
===================

A Rope is a tree structure for efficiently storing and manipulating
very large strings (like text documents).

Structure:
- Binary tree where leaves contain string fragments
- Internal nodes store total length of left subtree
- Allows O(log n) insert/delete vs O(n) for strings

Operations:
- concat(rope1, rope2): O(1) - just create parent node
- split(i): Split at position i - O(log n)
- insert(i, str): Insert string at position i - O(log n)
- delete(i, j): Delete range [i, j] - O(log n)
- char_at(i): Get character at position i - O(log n)
- substring(i, j): Extract substring - O(log n + k)

Applications:
- Text editors (Vim, Emacs use rope-like structures)
- Collaborative editing
- Undo/redo systems
- Large document processing
- Version control systems
"""


class RopeNode:
    """A node in the rope tree"""

    def __init__(self, text=None, left=None, right=None):
        self.text = text        # Text in leaf node
        self.left = left        # Left child
        self.right = right      # Right child
        self.weight = 0         # Length of left subtree

        if self.is_leaf():
            self.weight = len(text) if text else 0
        elif left:
            self.weight = left.total_length()

    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return self.left is None and self.right is None

    def total_length(self) -> int:
        """Get total length of text in this subtree"""
        if self.is_leaf():
            return len(self.text) if self.text else 0
        left_len = self.left.total_length() if self.left else 0
        right_len = self.right.total_length() if self.right else 0
        return left_len + right_len


class Rope:
    """
    Rope data structure for efficient string operations.
    """

    SPLIT_THRESHOLD = 10  # Min length for leaf node

    def __init__(self, text=""):
        """
        Initialize rope from string.

        Args:
            text: Initial text
        """
        # TODO: Create rope from text
        # For simple case, just create single leaf node
        # For optimization, split into balanced tree
        if text:
            self.root = RopeNode(text=text)
        else:
            self.root = RopeNode(text="")

    def concat(self, other) -> 'Rope':
        """
        Concatenate two ropes.

        Args:
            other: Another rope

        Returns:
            New rope (this and other are unchanged)

        Time Complexity: O(1)
        """
        # TODO: Create new parent node with this as left, other as right
        pass

    def char_at(self, index: int) -> str:
        """
        Get character at position.

        Args:
            index: Position (0-indexed)

        Returns:
            Character at position

        Raises:
            IndexError: If index out of bounds

        Time Complexity: O(log n)
        """
        # TODO: Traverse tree using weight to navigate
        return self._char_at(self.root, index)

    def _char_at(self, node: RopeNode, index: int) -> str:
        """Recursive helper for char_at"""
        # TODO:
        # If leaf: return text[index]
        # If index < node.weight: search left
        # Else: search right with adjusted index
        pass

    def substring(self, start: int, end: int) -> str:
        """
        Extract substring.

        Args:
            start: Start index (inclusive)
            end: End index (exclusive)

        Returns:
            Substring

        Time Complexity: O(log n + k) where k = substring length
        """
        # TODO: Collect characters from start to end
        result = []
        for i in range(start, end):
            result.append(self.char_at(i))
        return ''.join(result)

    def insert(self, index: int, text: str) -> 'Rope':
        """
        Insert text at position.

        Args:
            index: Position to insert at
            text: Text to insert

        Returns:
            New rope with insertion

        Time Complexity: O(log n)
        """
        # TODO: Split at index, concat three parts:
        # split(index) gives (left, right)
        # return left.concat(Rope(text)).concat(right)
        pass

    def delete(self, start: int, end: int) -> 'Rope':
        """
        Delete range of text.

        Args:
            start: Start index (inclusive)
            end: End index (exclusive)

        Returns:
            New rope with deletion

        Time Complexity: O(log n)
        """
        # TODO: Split at start and end, concat remaining parts
        pass

    def split(self, index: int) -> tuple:
        """
        Split rope at position.

        Args:
            index: Position to split at

        Returns:
            Tuple of (left_rope, right_rope)

        Time Complexity: O(log n)
        """
        # TODO: Recursively split tree at index
        pass

    def to_string(self) -> str:
        """
        Convert rope to string.

        Returns:
            String representation

        Time Complexity: O(n)
        """
        # TODO: In-order traversal collecting leaf text
        return self._to_string(self.root)

    def _to_string(self, node: RopeNode) -> str:
        """Recursive string conversion"""
        if node is None:
            return ""
        if node.is_leaf():
            return node.text or ""
        left = self._to_string(node.left)
        right = self._to_string(node.right)
        return left + right

    def __len__(self) -> int:
        """Get length of text"""
        return self.root.total_length() if self.root else 0


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_basic_rope():
    """Test basic rope creation"""
    rope = Rope("Hello, World!")
    assert rope.to_string() == "Hello, World!"
    assert len(rope) == 13


def test_concat():
    """Test concatenation"""
    rope1 = Rope("Hello")
    rope2 = Rope(", World!")
    rope3 = rope1.concat(rope2)

    assert rope3.to_string() == "Hello, World!"
    # Original ropes unchanged
    assert rope1.to_string() == "Hello"


def test_char_at():
    """Test character access"""
    rope = Rope("Hello")

    assert rope.char_at(0) == 'H'
    assert rope.char_at(1) == 'e'
    assert rope.char_at(4) == 'o'


def test_substring():
    """Test substring extraction"""
    rope = Rope("Hello, World!")

    assert rope.substring(0, 5) == "Hello"
    assert rope.substring(7, 12) == "World"
    assert rope.substring(0, 13) == "Hello, World!"


def test_insert():
    """Test insertion"""
    rope = Rope("Hello, World!")
    rope2 = rope.insert(7, "Beautiful ")

    assert rope2.to_string() == "Hello, Beautiful World!"
    assert rope.to_string() == "Hello, World!"  # Original unchanged


def test_delete():
    """Test deletion"""
    rope = Rope("Hello, Beautiful World!")
    rope2 = rope.delete(7, 17)  # Delete "Beautiful "

    assert rope2.to_string() == "Hello, World!"


def test_split():
    """Test splitting"""
    rope = Rope("Hello, World!")
    left, right = rope.split(7)

    assert left.to_string() == "Hello, "
    assert right.to_string() == "World!"


def test_large_text():
    """Test with larger text"""
    # Simulate text editor operations
    rope = Rope("a" * 1000)
    assert len(rope) == 1000

    rope = rope.insert(500, "INSERT")
    assert len(rope) == 1006
    assert rope.substring(498, 508) == "aaINSERTaa"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
