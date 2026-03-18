"""
Exercise: Array Reshaping
==========================

Learn to manipulate array shapes - a crucial skill for deep learning!

Reshaping is essential when working with neural networks.
"""

# I AM NOT DONE

import jax.numpy as jnp


def reshape_1d_to_2d():
    """
    Reshape array [1, 2, 3, 4, 5, 6] to shape (2, 3).
    Should return:
    [[1, 2, 3],
     [4, 5, 6]]
    """
    arr = jnp.array([1, 2, 3, 4, 5, 6])
    # TODO: Reshape to (2, 3)
    return None


def reshape_2d_to_1d():
    """
    Flatten a 2D array to 1D:
    [[1, 2],
     [3, 4],
     [5, 6]]
    Should return: [1, 2, 3, 4, 5, 6]

    Hint: Use jnp.flatten() or reshape to (-1,)
    """
    arr = jnp.array([[1, 2], [3, 4], [5, 6]])
    # TODO: Flatten to 1D
    return None


def transpose_matrix():
    """
    Transpose the matrix:
    [[1, 2, 3],
     [4, 5, 6]]
    Should return:
    [[1, 4],
     [2, 5],
     [3, 6]]

    Hint: Use jnp.transpose() or .T
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6]])
    # TODO: Transpose the matrix
    return None


def add_dimension():
    """
    Add a new axis at position 1 to array [1, 2, 3].
    Shape should change from (3,) to (3, 1).

    Hint: Use jnp.expand_dims() or indexing with jnp.newaxis
    """
    arr = jnp.array([1, 2, 3])
    # TODO: Add new axis
    return None


def squeeze_dimensions():
    """
    Remove dimensions of size 1 from array with shape (1, 3, 1).
    Should result in shape (3,).

    Hint: Use jnp.squeeze()
    """
    arr = jnp.ones((1, 3, 1))
    # TODO: Squeeze the array
    return None


def reshape_3d():
    """
    Reshape array of shape (12,) to (2, 3, 2).

    Hint: Total elements must remain the same (12 = 2*3*2)
    """
    arr = jnp.arange(12)
    # TODO: Reshape to (2, 3, 2)
    return None


# ===== Tests - Don't modify below this line =====

def test_reshape_1d_to_2d():
    result = reshape_1d_to_2d()
    expected = jnp.array([[1, 2, 3], [4, 5, 6]])
    assert jnp.array_equal(result, expected), f"Expected shape {expected.shape}, got {result.shape}"
    print("✓ reshape_1d_to_2d test passed")


def test_reshape_2d_to_1d():
    result = reshape_2d_to_1d()
    expected = jnp.array([1, 2, 3, 4, 5, 6])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ reshape_2d_to_1d test passed")


def test_transpose_matrix():
    result = transpose_matrix()
    expected = jnp.array([[1, 4], [2, 5], [3, 6]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ transpose_matrix test passed")


def test_add_dimension():
    result = add_dimension()
    assert result.shape == (3, 1), f"Expected shape (3, 1), got {result.shape}"
    print("✓ add_dimension test passed")


def test_squeeze_dimensions():
    result = squeeze_dimensions()
    assert result.shape == (3,), f"Expected shape (3,), got {result.shape}"
    print("✓ squeeze_dimensions test passed")


def test_reshape_3d():
    result = reshape_3d()
    assert result.shape == (2, 3, 2), f"Expected shape (2, 3, 2), got {result.shape}"
    print("✓ reshape_3d test passed")


if __name__ == "__main__":
    test_reshape_1d_to_2d()
    test_reshape_2d_to_1d()
    test_transpose_matrix()
    test_add_dimension()
    test_squeeze_dimensions()
    test_reshape_3d()
    print("\n🎉 All tests passed!")
