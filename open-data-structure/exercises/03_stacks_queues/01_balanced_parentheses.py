"""
Balanced Parentheses - Stack Application
=========================================

One classic application of stacks is checking if parentheses are balanced.

Examples:
- "()" -> True
- "(())" -> True
- "([{}])" -> True
- "([)]" -> False (wrong order)
- "(((" -> False (unclosed)

Algorithm:
1. Use a stack to track opening brackets
2. When you see a closing bracket, check if it matches the top
3. At the end, stack should be empty

Applications:
- Compiler syntax checking
- Expression validation
- HTML/XML tag matching
"""


def is_balanced(s: str) -> bool:
    """
    Check if parentheses/brackets are balanced.

    Args:
        s: String containing brackets: (), [], {}

    Returns:
        True if balanced, False otherwise

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # TODO: Implement using a stack
    # Hint: Use a dictionary to map closing to opening brackets
    pass


def is_valid_html(html: str) -> bool:
    """
    Check if HTML tags are properly nested.

    Simplified version - only checks tag structure.

    Example:
        "<div><p>text</p></div>" -> True
        "<div><p>text</div></p>" -> False

    Args:
        html: HTML string

    Returns:
        True if tags are properly nested

    Time Complexity: O(n)
    """
    # TODO: Implement HTML tag validation
    # Hint: Extract tags and use a stack to match opening/closing
    # You can use simple string operations to find tags
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_balanced_simple():
    """Test simple balanced cases"""
    assert is_balanced("()") == True
    assert is_balanced("[]") == True
    assert is_balanced("{}") == True
    assert is_balanced("") == True


def test_balanced_nested():
    """Test nested brackets"""
    assert is_balanced("(())") == True
    assert is_balanced("([{}])") == True
    assert is_balanced("{[()]}") == True


def test_balanced_multiple():
    """Test multiple brackets"""
    assert is_balanced("()[]{}") == True
    assert is_balanced("({})[]") == True


def test_unbalanced():
    """Test unbalanced cases"""
    assert is_balanced("(") == False
    assert is_balanced(")") == False
    assert is_balanced("(()") == False
    assert is_balanced("())") == False
    assert is_balanced("([)]") == False  # Wrong order
    assert is_balanced("{[(])}") == False


def test_html_valid():
    """Test valid HTML"""
    assert is_valid_html("<div></div>") == True
    assert is_valid_html("<div><p>text</p></div>") == True
    assert is_valid_html("<a><b><c></c></b></a>") == True


def test_html_invalid():
    """Test invalid HTML"""
    assert is_valid_html("<div><p></div></p>") == False
    assert is_valid_html("<div>") == False
    assert is_valid_html("</div>") == False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
