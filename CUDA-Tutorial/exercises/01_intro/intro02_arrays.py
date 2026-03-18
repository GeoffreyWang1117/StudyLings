"""
Exercise: JAX Arrays
=====================

JAX arrays are immutable! Unlike NumPy arrays, you cannot modify them in-place.
Operations on JAX arrays return new arrays.

This immutability is crucial for JAX's transformation system (like jit and grad).

Your task: Complete the functions to work with JAX arrays.
"""

# I AM NOT DONE

import jax.numpy as jnp


def create_range():
    """
    Create an array with values from 0 to 9 (inclusive of 0, exclusive of 10).

    Hint: Use jnp.arange()
    """
    # TODO: Create array [0, 1, 2, ..., 9]
    return None


def create_ones():
    """
    Create a 3x3 array filled with ones.

    Hint: Use jnp.ones()
    """
    # TODO: Create a 3x3 array of ones
    return None


def create_identity():
    """
    Create a 4x4 identity matrix.

    Hint: Use jnp.eye()
    """
    # TODO: Create a 4x4 identity matrix
    return None


def create_linspace():
    """
    Create an array of 5 evenly spaced values between 0 and 1 (inclusive).

    Hint: Use jnp.linspace()
    """
    # TODO: Create array with 5 values from 0 to 1
    return None


def get_dtype():
    """
    Create an array [1, 2, 3] with float32 data type.

    Hint: Specify dtype parameter
    """
    # TODO: Create array with float32 dtype
    return None


# ===== Tests - Don't modify below this line =====

def test_create_range():
    arr = create_range()
    assert arr is not None
    expected = jnp.arange(10)
    assert jnp.array_equal(arr, expected), f"Expected {expected}, got {arr}"
    print("✓ create_range test passed")


def test_create_ones():
    arr = create_ones()
    assert arr is not None
    assert arr.shape == (3, 3), f"Expected shape (3, 3), got {arr.shape}"
    assert jnp.all(arr == 1), "All elements should be 1"
    print("✓ create_ones test passed")


def test_create_identity():
    arr = create_identity()
    assert arr is not None
    expected = jnp.eye(4)
    assert jnp.array_equal(arr, expected), "Should be a 4x4 identity matrix"
    print("✓ create_identity test passed")


def test_create_linspace():
    arr = create_linspace()
    assert arr is not None
    assert len(arr) == 5, f"Expected 5 elements, got {len(arr)}"
    expected = jnp.linspace(0, 1, 5)
    assert jnp.allclose(arr, expected), f"Expected {expected}, got {arr}"
    print("✓ create_linspace test passed")


def test_get_dtype():
    arr = get_dtype()
    assert arr is not None
    assert arr.dtype == jnp.float32, f"Expected dtype float32, got {arr.dtype}"
    assert jnp.array_equal(arr, jnp.array([1, 2, 3], dtype=jnp.float32))
    print("✓ get_dtype test passed")


if __name__ == "__main__":
    test_create_range()
    test_create_ones()
    test_create_identity()
    test_create_linspace()
    test_get_dtype()
    print("\n🎉 All tests passed! Remove the 'I AM NOT DONE' comment.")
