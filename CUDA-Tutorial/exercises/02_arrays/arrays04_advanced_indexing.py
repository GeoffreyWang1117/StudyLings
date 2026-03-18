"""
Exercise: Advanced Indexing and Functional Updates
===================================================

JAX arrays are immutable, so we can't modify them in-place.
Instead, JAX provides the .at[] syntax for functional updates.

This returns a NEW array with the modifications applied.
"""

# I AM NOT DONE

import jax.numpy as jnp


def functional_update():
    """
    Update element at index 2 to value 100 in array [1, 2, 3, 4, 5].
    Should return: [1, 2, 100, 4, 5]

    Remember: Use .at[].set() for functional updates!
    """
    arr = jnp.array([1, 2, 3, 4, 5])
    # TODO: Update index 2 to 100 using .at[].set()
    return None


def update_multiple():
    """
    Update indices [1, 3] to values [20, 40] in array [1, 2, 3, 4, 5].
    Should return: [1, 20, 3, 40, 5]

    Hint: arr.at[[1, 3]].set([20, 40])
    """
    arr = jnp.array([1, 2, 3, 4, 5])
    # TODO: Update multiple indices
    return None


def update_2d():
    """
    Update element at row 1, column 2 to value 99:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    Should return:
    [[1, 2, 3],
     [4, 5, 99],
     [7, 8, 9]]
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # TODO: Update element at [1, 2]
    return None


def add_to_index():
    """
    Add 10 to the element at index 2 in array [1, 2, 3, 4, 5].
    Should return: [1, 2, 13, 4, 5]

    Hint: Use .at[].add() instead of .set()
    """
    arr = jnp.array([1, 2, 3, 4, 5])
    # TODO: Add 10 to index 2
    return None


def boolean_indexing():
    """
    Select all elements greater than 3 from array [1, 2, 3, 4, 5, 6].
    Should return: [4, 5, 6]

    Hint: Use arr[arr > 3]
    """
    arr = jnp.array([1, 2, 3, 4, 5, 6])
    # TODO: Select elements > 3
    return None


def where_update():
    """
    Replace all elements > 5 with 0 in array [1, 3, 6, 8, 2, 9].
    Should return: [1, 3, 0, 0, 2, 0]

    Hint: Use jnp.where(condition, true_value, false_value)
    """
    arr = jnp.array([1, 3, 6, 8, 2, 9])
    # TODO: Replace elements > 5 with 0
    return None


# ===== Tests - Don't modify below this line =====

def test_functional_update():
    result = functional_update()
    expected = jnp.array([1, 2, 100, 4, 5])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ functional_update test passed")


def test_update_multiple():
    result = update_multiple()
    expected = jnp.array([1, 20, 3, 40, 5])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ update_multiple test passed")


def test_update_2d():
    result = update_2d()
    expected = jnp.array([[1, 2, 3], [4, 5, 99], [7, 8, 9]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ update_2d test passed")


def test_add_to_index():
    result = add_to_index()
    expected = jnp.array([1, 2, 13, 4, 5])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ add_to_index test passed")


def test_boolean_indexing():
    result = boolean_indexing()
    expected = jnp.array([4, 5, 6])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ boolean_indexing test passed")


def test_where_update():
    result = where_update()
    expected = jnp.array([1, 3, 0, 0, 2, 0])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ where_update test passed")


if __name__ == "__main__":
    test_functional_update()
    test_update_multiple()
    test_update_2d()
    test_add_to_index()
    test_boolean_indexing()
    test_where_update()
    print("\n🎉 All tests passed!")
