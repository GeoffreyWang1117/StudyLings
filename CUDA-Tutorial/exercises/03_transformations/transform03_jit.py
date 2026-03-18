"""
Exercise: JIT Compilation
==========================

jax.jit compiles functions using XLA for faster execution.

JIT compilation can provide significant speedups, especially for
functions that are called multiple times.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import time


def create_jit_function():
    """
    Create a JIT-compiled version of a simple function.

    f(x) = x^2 + 2*x + 1

    Apply @jax.jit decorator or use jax.jit(f)
    """
    # TODO: Add @jax.jit decorator
    def f(x):
        return x**2 + 2*x + 1

    # Return the JIT-compiled function
    # TODO: Either use @jax.jit above or return jax.jit(f) here
    return None


def jit_with_arrays():
    """
    JIT compile a function that works with arrays.

    Normalize an array: (x - mean) / std
    """
    # TODO: JIT compile this function
    def normalize(x):
        mean = jnp.mean(x)
        std = jnp.std(x)
        return (x - mean) / std

    arr = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])
    # TODO: Create JIT version and call it
    jit_normalize = None
    return None


def jit_matrix_multiply():
    """
    JIT compile matrix multiplication for better performance.

    Multiply two 3x3 matrices.
    """
    @jax.jit
    def matmul(a, b):
        return jnp.dot(a, b)

    # TODO: Call the JIT-compiled function
    a = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=jnp.float32)
    b = jnp.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]], dtype=jnp.float32)

    return None  # Call matmul(a, b)


def jit_grad_combination():
    """
    Combine JIT with grad for maximum performance!

    Compute gradient of f(x) = sum(x^3) efficiently.
    """
    def f(x):
        return jnp.sum(x ** 3)

    # TODO: Create JIT-compiled gradient function
    # Hint: jax.jit(jax.grad(f)) or @jax.jit on grad function
    grad_f = None

    x = jnp.array([1.0, 2.0, 3.0])
    return None  # Evaluate grad_f(x)


def static_vs_dynamic():
    """
    Understand static vs dynamic arguments in JIT.

    JIT functions are recompiled when array shapes change.
    Use static_argnums for arguments that should trigger recompilation.
    """
    @jax.jit
    def sum_first_n(arr, n):
        # This will be slow if n changes - it triggers recompilation
        return jnp.sum(arr[:n])

    # Better: make n static
    # TODO: Modify to use static_argnums for 'n'
    # @jax.jit(static_argnums=(1,))
    def sum_first_n_static(arr, n):
        return jnp.sum(arr[:n])

    arr = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # TODO: Create static version and call it
    result = None  # Call sum_first_n_static(arr, 5)
    return result


# ===== Tests - Don't modify below this line =====

def test_create_jit_function():
    f = create_jit_function()
    if f is None:
        # Try to create it ourselves for testing
        def f_impl(x):
            return x**2 + 2*x + 1
        f = jax.jit(f_impl)

    result = f(3.0)
    expected = 16.0  # 9 + 6 + 1
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ create_jit_function test passed")


def test_jit_with_arrays():
    result = jit_with_arrays()
    if result is None:
        @jax.jit
        def normalize(x):
            mean = jnp.mean(x)
            std = jnp.std(x)
            return (x - mean) / std
        result = normalize(jnp.array([1.0, 2.0, 3.0, 4.0, 5.0]))

    # For [1,2,3,4,5], mean=3, std≈1.414, so normalized values center at 0
    assert result.shape == (5,), f"Expected shape (5,), got {result.shape}"
    assert jnp.isclose(jnp.mean(result), 0.0, atol=1e-6), "Mean should be ~0"
    print("✓ jit_with_arrays test passed")


def test_jit_matrix_multiply():
    result = jit_matrix_multiply()
    assert result is not None, "Result should not be None"
    assert result.shape == (3, 3), f"Expected shape (3, 3), got {result.shape}"
    print("✓ jit_matrix_multiply test passed")


def test_jit_grad_combination():
    result = jit_grad_combination()
    if result is None:
        def f(x):
            return jnp.sum(x ** 3)
        grad_f = jax.jit(jax.grad(f))
        result = grad_f(jnp.array([1.0, 2.0, 3.0]))

    expected = jnp.array([3.0, 12.0, 27.0])  # 3*x^2 for each element
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ jit_grad_combination test passed")


def test_static_vs_dynamic():
    result = static_vs_dynamic()
    if result is None:
        @jax.jit(static_argnums=(1,))
        def sum_first_n_static(arr, n):
            return jnp.sum(arr[:n])
        result = sum_first_n_static(jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 5)

    expected = 15  # 1+2+3+4+5
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ static_vs_dynamic test passed")


if __name__ == "__main__":
    test_create_jit_function()
    test_jit_with_arrays()
    test_jit_matrix_multiply()
    test_jit_grad_combination()
    test_static_vs_dynamic()
    print("\n🎉 All tests passed!")
