"""
Welcome to ODS-Python!
======================

This is your first exercise. It's a simple warm-up to get you familiar
with the system.

Your task: Complete the function below to make the tests pass.
"""


def greet(name: str) -> str:
    """
    Return a greeting message for the given name.

    Example:
        >>> greet("Alice")
        'Hello, Alice! Welcome to ODS-Python!'

    Args:
        name: The name to greet

    Returns:
        A greeting message
    """
    # TODO: Return a greeting message in the format:
    # "Hello, {name}! Welcome to ODS-Python!"
    pass


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    # TODO: Return the sum of a and b
    pass


# ========================================
# Tests - Do not modify below this line
# ========================================

def test_greet():
    """Test the greet function"""
    assert greet("Alice") == "Hello, Alice! Welcome to ODS-Python!"
    assert greet("Bob") == "Hello, Bob! Welcome to ODS-Python!"
    assert greet("World") == "Hello, World! Welcome to ODS-Python!"


def test_add_numbers():
    """Test the add_numbers function"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
    assert add_numbers(100, 200) == 300


if __name__ == "__main__":
    # You can run this file directly to test your solution
    import pytest
    pytest.main([__file__, "-v"])
