"""
Exercise: Hello JAX!
====================

Welcome to JAXlings! This is your first exercise.

JAX is a Python library for high-performance numerical computing and
automatic differentiation. It provides a NumPy-like API with added
features like automatic differentiation, JIT compilation, and GPU/TPU support.

Your task: Fix the code below to make all tests pass.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def create_array():
    """
    Create a JAX array containing the numbers [1, 2, 3, 4, 5].

    Hint: Use jax.numpy (jnp) instead of regular numpy!
    """
    # TODO: Replace None with the correct array
    return None


def get_array_shape():
    """
    Create a 2D array with shape (3, 4) filled with zeros.

    Hint: Use jnp.zeros()
    """
    # TODO: Replace None with a (3, 4) array of zeros
    return None


def array_from_list():
    """
    Convert a Python list [[1, 2], [3, 4], [5, 6]] to a JAX array.

    Hint: Use jnp.array()
    """
    data = [[1, 2], [3, 4], [5, 6]]
    # TODO: Convert data to a JAX array
    return None


# ===== Tests - Don't modify below this line =====

def test_create_array():
    """Test array creation."""
    arr = create_array()
    assert arr is not None, "Array should not be None"
    assert isinstance(arr, jax.Array), "Should return a JAX array"
    assert arr.shape == (5,), f"Expected shape (5,), got {arr.shape}"
    assert jnp.array_equal(arr, jnp.array([1, 2, 3, 4, 5])), "Array values are incorrect"
    print("✓ create_array test passed")


def test_get_array_shape():
    """Test array shape creation."""
    arr = get_array_shape()
    assert arr is not None, "Array should not be None"
    assert isinstance(arr, jax.Array), "Should return a JAX array"
    assert arr.shape == (3, 4), f"Expected shape (3, 4), got {arr.shape}"
    assert jnp.all(arr == 0), "Array should be filled with zeros"
    print("✓ get_array_shape test passed")


def test_array_from_list():
    """Test list to array conversion."""
    arr = array_from_list()
    assert arr is not None, "Array should not be None"
    assert isinstance(arr, jax.Array), "Should return a JAX array"
    expected = jnp.array([[1, 2], [3, 4], [5, 6]])
    assert arr.shape == (3, 2), f"Expected shape (3, 2), got {arr.shape}"
    assert jnp.array_equal(arr, expected), "Array values are incorrect"
    print("✓ array_from_list test passed")


if __name__ == "__main__":
    test_create_array()
    test_get_array_shape()
    test_array_from_list()
    print("\n🎉 All tests passed! Remove the 'I AM NOT DONE' comment and run 'jaxlings verify'")
