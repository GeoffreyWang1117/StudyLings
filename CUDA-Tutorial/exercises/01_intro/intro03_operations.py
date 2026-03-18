"""
Exercise: Array Operations
===========================

JAX provides all the standard array operations you'd expect from NumPy.
Remember: operations return new arrays since JAX arrays are immutable!

Your task: Implement basic array operations.
"""

# I AM NOT DONE

import jax.numpy as jnp


def add_arrays():
    """
    Add two arrays: [1, 2, 3] and [4, 5, 6].
    Should return: [5, 7, 9]
    """
    a = jnp.array([1, 2, 3])
    b = jnp.array([4, 5, 6])
    # TODO: Add the arrays
    return None


def multiply_arrays():
    """
    Element-wise multiply: [2, 3, 4] * [5, 6, 7]
    Should return: [10, 18, 28]
    """
    a = jnp.array([2, 3, 4])
    b = jnp.array([5, 6, 7])
    # TODO: Multiply the arrays element-wise
    return None


def matrix_multiply():
    """
    Matrix multiplication of:
    [[1, 2],     [[5, 6],
     [3, 4]]  @   [7, 8]]

    Hint: Use jnp.dot() or @ operator
    """
    a = jnp.array([[1, 2], [3, 4]])
    b = jnp.array([[5, 6], [7, 8]])
    # TODO: Perform matrix multiplication
    return None


def compute_mean():
    """
    Compute the mean of array [1, 2, 3, 4, 5].
    Should return: 3.0
    """
    arr = jnp.array([1, 2, 3, 4, 5])
    # TODO: Compute mean
    return None


def compute_sum():
    """
    Compute the sum along axis 0 of:
    [[1, 2, 3],
     [4, 5, 6]]
    Should return: [5, 7, 9]
    """
    arr = jnp.array([[1, 2, 3], [4, 5, 6]])
    # TODO: Sum along axis 0
    return None


def apply_function():
    """
    Apply exponential function to array [0, 1, 2].

    Hint: Use jnp.exp()
    """
    arr = jnp.array([0, 1, 2])
    # TODO: Apply exp function
    return None


# ===== Tests - Don't modify below this line =====

def test_add_arrays():
    result = add_arrays()
    expected = jnp.array([5, 7, 9])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ add_arrays test passed")


def test_multiply_arrays():
    result = multiply_arrays()
    expected = jnp.array([10, 18, 28])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ multiply_arrays test passed")


def test_matrix_multiply():
    result = matrix_multiply()
    expected = jnp.array([[19, 22], [43, 50]])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ matrix_multiply test passed")


def test_compute_mean():
    result = compute_mean()
    assert jnp.isclose(result, 3.0), f"Expected 3.0, got {result}"
    print("✓ compute_mean test passed")


def test_compute_sum():
    result = compute_sum()
    expected = jnp.array([5, 7, 9])
    assert jnp.array_equal(result, expected), f"Expected {expected}, got {result}"
    print("✓ compute_sum test passed")


def test_apply_function():
    result = apply_function()
    expected = jnp.exp(jnp.array([0, 1, 2]))
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ apply_function test passed")


if __name__ == "__main__":
    test_add_arrays()
    test_multiply_arrays()
    test_matrix_multiply()
    test_compute_mean()
    test_compute_sum()
    test_apply_function()
    print("\n🎉 All tests passed!")
