"""
Trie (Prefix Tree)
==================

A trie stores strings efficiently for fast prefix-based operations.

Structure:
- Each node represents a character
- Root is empty
- Edges represent characters
- Special marker for end of word

Operations:
- insert(word): O(m) where m = word length
- search(word): O(m)
- startsWith(prefix): O(m)
- delete(word): O(m)

Applications:
- Autocomplete
- Spell checker
- IP routing (longest prefix match)
- Dictionary implementation
- T9 predictive text
"""


class TrieNode:
    """A node in the trie"""

    def __init__(self):
        # TODO: Initialize node
        # Hint: Use a dictionary for children
        # Track if this is end of a word
        pass


class Trie:
    """
    Trie (Prefix Tree) implementation.
    """

    def __init__(self):
        """Initialize empty trie"""
        # TODO: Create root node
        pass

    def insert(self, word: str):
        """
        Insert a word into the trie.

        Args:
            word: The word to insert

        Time Complexity: O(m) where m = len(word)
        """
        # TODO: Implement insert
        # Start from root
        # For each character:
        #   - Create node if doesn't exist
        #   - Move to that node
        # Mark last node as end of word
        pass

    def search(self, word: str) -> bool:
        """
        Search for a complete word.

        Args:
            word: The word to search for

        Returns:
            True if word exists in trie

        Time Complexity: O(m)
        """
        # TODO: Implement search
        # Traverse trie following characters
        # Check if last node is marked as end of word
        pass

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with given prefix.

        Args:
            prefix: The prefix to check

        Returns:
            True if prefix exists

        Time Complexity: O(m)
        """
        # TODO: Implement startsWith
        # Similar to search but don't check end of word marker
        pass

    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.

        Args:
            word: The word to delete

        Returns:
            True if word was deleted, False if not found

        Time Complexity: O(m)
        """
        # TODO: Implement delete (challenging!)
        # Remove nodes that are no longer needed
        # Don't remove if they're part of another word
        pass

    def find_all_with_prefix(self, prefix: str) -> list:
        """
        Find all words with given prefix.

        Args:
            prefix: The prefix

        Returns:
            List of words with that prefix

        Time Complexity: O(n) where n = total characters in matching words
        """
        # TODO: Implement autocomplete
        # 1. Navigate to prefix
        # 2. DFS to collect all words from that point
        pass

    def count_words(self) -> int:
        """
        Count total number of words in trie.

        Returns:
            Number of words

        Time Complexity: O(n) where n = total nodes
        """
        # TODO: Count nodes marked as end of word
        pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_insert_and_search():
    """Test basic insert and search"""
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")

    assert trie.search("apple") == True
    assert trie.search("app") == True
    assert trie.search("appl") == False  # Prefix but not word
    assert trie.search("orange") == False


def test_starts_with():
    """Test prefix checking"""
    trie = Trie()
    trie.insert("apple")
    trie.insert("application")

    assert trie.starts_with("app") == True
    assert trie.starts_with("appl") == True
    assert trie.starts_with("apple") == True
    assert trie.starts_with("ora") == False


def test_delete():
    """Test word deletion"""
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")

    assert trie.delete("app") == True
    assert trie.search("app") == False
    assert trie.search("apple") == True  # Should still exist
    assert trie.search("application") == True

    assert trie.delete("notfound") == False


def test_autocomplete():
    """Test finding all words with prefix"""
    trie = Trie()
    words = ["apple", "app", "application", "apply", "orange", "oregano"]

    for word in words:
        trie.insert(word)

    results = trie.find_all_with_prefix("app")
    assert set(results) == {"apple", "app", "application", "apply"}

    results = trie.find_all_with_prefix("or")
    assert set(results) == {"orange", "oregano"}


def test_count_words():
    """Test counting words"""
    trie = Trie()
    trie.insert("hello")
    trie.insert("world")
    trie.insert("help")

    assert trie.count_words() == 3


def test_empty_string():
    """Test empty string handling"""
    trie = Trie()
    trie.insert("")

    assert trie.search("") == True
    assert trie.starts_with("") == True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
