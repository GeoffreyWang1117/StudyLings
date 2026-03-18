"""
Exercise: Array Indexing
=========================

Learn to access and slice JAX arrays, just like NumPy!

Indexing and slicing are fundamental operations for working with arrays.
"""

# I AM NOT DONE

import jax.numpy as jnp


def get_element():
    """
    Get the element at index 2 from array [10, 20, 30, 40, 50].
    Should return: 30
    """
    arr = jnp.array([10, 20, 30, 40, 50])
    # TODO: Return the element at index 2
    return None


def get_slice():
    """
    Get elements from index 1 to 3 (inclusive of 1, exclusive of 4)
    from array [1, 2, 3, 4, 5, 6].
    Should return: [2, 3, 4]
    """
    arr = jnp.array([1, 2, 3, 4, 5, 6])
    # TODO: Return slice from index 1 to 4
    return None


def get_2d_element():
    """
    Get the element at row 1, column 2 from:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    Should return: 6
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # TODO: Get element at row 1, column 2
    return None


def get_row():
    """
    Get the second row (index 1) from:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    Should return: [4, 5, 6]
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # TODO: Get the second row
    return None


def get_column():
    """
    Get the first column from:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    Should return: [1, 4, 7]
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # TODO: Get the first column
    return None


def negative_indexing():
    """
    Get the last element from array [1, 2, 3, 4, 5].
    Should return: 5

    Hint: Use negative indexing
    """
    arr = jnp.array([1, 2, 3, 4, 5])
    # TODO: Get the last element
    return None


# ===== Tests - Don't modify below this line =====

def test_get_element():
    result = get_element()
    assert result == 30, f"Expected 30, got {result}"
    print("✓ get_element test passed")


def test_get_slice():
    result = get_slice()
    expected = jnp.array([2, 3, 4])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ get_slice test passed")


def test_get_2d_element():
    result = get_2d_element()
    assert result == 6, f"Expected 6, got {result}"
    print("✓ get_2d_element test passed")


def test_get_row():
    result = get_row()
    expected = jnp.array([4, 5, 6])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ get_row test passed")


def test_get_column():
    result = get_column()
    expected = jnp.array([1, 4, 7])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ get_column test passed")


def test_negative_indexing():
    result = negative_indexing()
    assert result == 5, f"Expected 5, got {result}"
    print("✓ negative_indexing test passed")


if __name__ == "__main__":
    test_get_element()
    test_get_slice()
    test_get_2d_element()
    test_get_row()
    test_get_column()
    test_negative_indexing()
    print("\n🎉 All tests passed!")
