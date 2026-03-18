"""
Exercise: Automatic Differentiation with grad
==============================================

JAX's automatic differentiation is one of its most powerful features!

jax.grad computes the gradient of a function.
This is essential for training machine learning models.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def simple_gradient():
    """
    Compute the gradient of f(x) = x^2 at x = 3.0.
    The derivative is f'(x) = 2x, so at x=3, it should be 6.0.

    Hint: Use jax.grad() to create a gradient function
    """
    def f(x):
        return x ** 2

    # TODO: Create gradient function and evaluate at 3.0
    grad_f = None  # Use jax.grad(f)
    return None  # Evaluate grad_f(3.0)


def polynomial_gradient():
    """
    Compute the gradient of f(x) = 3x^3 + 2x^2 - 5x + 1 at x = 2.0.
    Derivative: f'(x) = 9x^2 + 4x - 5
    At x=2: f'(2) = 9(4) + 4(2) - 5 = 36 + 8 - 5 = 39
    """
    def f(x):
        return 3 * x**3 + 2 * x**2 - 5 * x + 1

    # TODO: Compute gradient at x = 2.0
    return None


def multivariate_gradient():
    """
    Compute the gradient of f(x, y) = x^2 + 3*y^2 at (x=1.0, y=2.0).

    For multivariate functions, we need to specify which argument
    to differentiate with respect to using 'argnums'.

    Gradient w.r.t. x: df/dx = 2x = 2(1) = 2.0
    """
    def f(x, y):
        return x**2 + 3 * y**2

    # TODO: Compute gradient w.r.t. first argument (x) at (1.0, 2.0)
    # Hint: jax.grad(f, argnums=0)
    grad_f = None
    return None


def array_gradient():
    """
    Compute the gradient of f(x) = sum(x^2) where x is an array.

    For x = [1.0, 2.0, 3.0], gradient should be 2*x = [2.0, 4.0, 6.0]
    """
    def f(x):
        return jnp.sum(x ** 2)

    x = jnp.array([1.0, 2.0, 3.0])
    # TODO: Compute gradient
    grad_f = None
    return None


def nested_gradient():
    """
    Compute the second derivative of f(x) = x^3 at x = 2.0.

    f(x) = x^3
    f'(x) = 3x^2
    f''(x) = 6x
    At x=2: f''(2) = 12
    """
    def f(x):
        return x ** 3

    # TODO: Apply jax.grad twice to get second derivative
    # Hint: jax.grad(jax.grad(f))
    second_grad_f = None
    return None


# ===== Tests - Don't modify below this line =====

def test_simple_gradient():
    result = simple_gradient()
    expected = 6.0
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ simple_gradient test passed")


def test_polynomial_gradient():
    result = polynomial_gradient()
    expected = 39.0
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ polynomial_gradient test passed")


def test_multivariate_gradient():
    result = multivariate_gradient()
    expected = 2.0
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ multivariate_gradient test passed")


def test_array_gradient():
    result = array_gradient()
    expected = jnp.array([2.0, 4.0, 6.0])
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ array_gradient test passed")


def test_nested_gradient():
    result = nested_gradient()
    expected = 12.0
    assert jnp.isclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ nested_gradient test passed")


if __name__ == "__main__":
    test_simple_gradient()
    test_polynomial_gradient()
    test_multivariate_gradient()
    test_array_gradient()
    test_nested_gradient()
    print("\n🎉 All tests passed!")
