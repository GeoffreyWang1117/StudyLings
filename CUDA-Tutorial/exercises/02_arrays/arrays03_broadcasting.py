"""
Exercise: Broadcasting
=======================

Broadcasting is a powerful mechanism that allows JAX to work with arrays
of different shapes during arithmetic operations.

Understanding broadcasting is essential for efficient array operations!
"""

# I AM NOT DONE

import jax.numpy as jnp


def broadcast_scalar():
    """
    Add scalar 10 to array [1, 2, 3, 4].
    Should return: [11, 12, 13, 14]

    Broadcasting automatically expands the scalar to match the array shape.
    """
    arr = jnp.array([1, 2, 3, 4])
    scalar = 10
    # TODO: Add scalar to array
    return None


def broadcast_1d_to_2d():
    """
    Add 1D array [1, 2, 3] to each row of 2D array:
    [[10, 20, 30],
     [40, 50, 60]]

    Should return:
    [[11, 22, 33],
     [41, 52, 63]]
    """
    arr_2d = jnp.array([[10, 20, 30], [40, 50, 60]])
    arr_1d = jnp.array([1, 2, 3])
    # TODO: Add 1D array to 2D array
    return None


def broadcast_column():
    """
    Add column vector [[1], [2]] to matrix:
    [[10, 20, 30],
     [40, 50, 60]]

    Should return:
    [[11, 21, 31],
     [42, 52, 62]]

    The column vector broadcasts across columns.
    """
    matrix = jnp.array([[10, 20, 30], [40, 50, 60]])
    column = jnp.array([[1], [2]])
    # TODO: Add column vector to matrix
    return None


def broadcast_outer_product():
    """
    Compute outer product of [1, 2, 3] and [10, 20].
    Should return:
    [[10, 20],
     [20, 40],
     [30, 60]]

    Hint: Reshape arrays to (3, 1) and (1, 2), then multiply
    """
    a = jnp.array([1, 2, 3])
    b = jnp.array([10, 20])
    # TODO: Compute outer product using broadcasting
    # Reshape a to (3, 1) and b to (1, 2), then multiply
    return None


def broadcast_multiple():
    """
    Multiply three arrays with compatible shapes:
    - a: shape (4, 1, 1) with values [1, 2, 3, 4]
    - b: shape (1, 3, 1) with values [10, 20, 30]
    - c: shape (1, 1, 2) with values [100, 200]

    Result should have shape (4, 3, 2).
    """
    a = jnp.array([1, 2, 3, 4]).reshape(4, 1, 1)
    b = jnp.array([10, 20, 30]).reshape(1, 3, 1)
    c = jnp.array([100, 200]).reshape(1, 1, 2)
    # TODO: Multiply the three arrays
    return None


# ===== Tests - Don't modify below this line =====

def test_broadcast_scalar():
    result = broadcast_scalar()
    expected = jnp.array([11, 12, 13, 14])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ broadcast_scalar test passed")


def test_broadcast_1d_to_2d():
    result = broadcast_1d_to_2d()
    expected = jnp.array([[11, 22, 33], [41, 52, 63]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ broadcast_1d_to_2d test passed")


def test_broadcast_column():
    result = broadcast_column()
    expected = jnp.array([[11, 21, 31], [42, 52, 62]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ broadcast_column test passed")


def test_broadcast_outer_product():
    result = broadcast_outer_product()
    expected = jnp.array([[10, 20], [20, 40], [30, 60]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ broadcast_outer_product test passed")


def test_broadcast_multiple():
    result = broadcast_multiple()
    assert result.shape == (4, 3, 2), f"Expected shape (4, 3, 2), got {result.shape}"
    # Check a few values
    assert result[0, 0, 0] == 1 * 10 * 100, "Incorrect value at [0,0,0]"
    assert result[1, 1, 1] == 2 * 20 * 200, "Incorrect value at [1,1,1]"
    print("✓ broadcast_multiple test passed")


if __name__ == "__main__":
    test_broadcast_scalar()
    test_broadcast_1d_to_2d()
    test_broadcast_column()
    test_broadcast_outer_product()
    test_broadcast_multiple()
    print("\n🎉 All tests passed!")
