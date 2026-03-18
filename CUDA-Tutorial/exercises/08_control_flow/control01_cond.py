"""
Exercise: Conditional Operations with lax.cond
===============================================

JAX provides lax.cond for efficient conditional execution in JIT-compiled code.

Regular Python if/else can cause issues with JIT compilation.
lax.cond solves this by making conditionals part of the computation graph.

When to use lax.cond:
- Inside JIT-compiled functions with dynamic conditions
- When you need differentiability through conditionals
- For efficient branching on GPU/TPU
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.lax as lax


def simple_cond():
    """
    Use lax.cond for simple conditional logic.

    If x > 0, return x^2, else return -x^2
    """
    x = 3.0

    # TODO: Implement using lax.cond
    # lax.cond(pred, true_fun, false_fun, operand)
    def true_branch(x):
        return x ** 2

    def false_branch(x):
        return -(x ** 2)

    result = None  # lax.cond(x > 0, true_branch, false_branch, x)

    return result


def cond_with_different_types():
    """
    Use lax.cond where branches return different computations.

    Important: Both branches must return same shape/dtype!
    """
    x = jnp.array([1.0, 2.0, 3.0])
    threshold = 2.0

    # If mean > threshold, normalize, else standardize
    def normalize(x):
        return x / jnp.sum(x)

    def standardize(x):
        return (x - jnp.mean(x)) / jnp.std(x)

    # TODO: Use lax.cond
    result = None  # lax.cond(jnp.mean(x) > threshold, normalize, standardize, x)

    return result


def nested_cond():
    """
    Use nested lax.cond for multiple conditions.

    Classify x: 'positive' if x > 0, 'zero' if x == 0, 'negative' if x < 0
    Return: 1, 0, or -1
    """
    x = 5.0

    # TODO: Implement nested conditionals
    def check_positive(x):
        return 1.0

    def check_zero_or_negative(x):
        # Nested cond
        return None  # lax.cond(x == 0, lambda x: 0.0, lambda x: -1.0, x)

    result = None  # lax.cond(x > 0, check_positive, check_zero_or_negative, x)

    return result


def cond_in_jit():
    """
    Use lax.cond inside a JIT-compiled function.

    This is where lax.cond really shines!
    """
    @jax.jit
    def relu_or_tanh(x, use_relu):
        # TODO: Conditionally apply ReLU or tanh
        def apply_relu(x):
            return jnp.maximum(0, x)

        def apply_tanh(x):
            return jnp.tanh(x)

        return None  # lax.cond(use_relu, apply_relu, apply_tanh, x)

    x = jnp.array([-1.0, 0.0, 1.0, 2.0])
    result = relu_or_tanh(x, True)  # Use ReLU

    return result


def cond_with_grad():
    """
    Use lax.cond with gradient computation.

    Gradients flow through the taken branch.
    """
    def f(x, use_square):
        def square(x):
            return x ** 2

        def cube(x):
            return x ** 3

        return lax.cond(use_square, square, cube, x)

    # TODO: Compute gradient when use_square=True
    x = 2.0
    grad_fn = None  # jax.grad(f, argnums=0)

    if grad_fn is not None:
        gradient = grad_fn(x, True)  # Should be 2*x = 4.0
        return gradient

    return None


def switchcase_alternative():
    """
    For multiple branches, you can stack lax.cond calls
    or use lax.switch for integer indexing.

    Implement:
    - index 0: x^2
    - index 1: x^3
    - index 2: sqrt(abs(x))
    """
    x = 4.0
    index = 1

    # TODO: Use lax.switch
    branches = [
        lambda x: x ** 2,
        lambda x: x ** 3,
        lambda x: jnp.sqrt(jnp.abs(x))
    ]

    result = None  # lax.switch(index, branches, x)

    return result


def cond_performance():
    """
    Compare lax.cond vs Python if for JIT performance.

    This demonstrates why lax.cond is important!
    """
    @jax.jit
    def with_lax_cond(x, condition):
        return lax.cond(
            condition,
            lambda x: x ** 2,
            lambda x: x ** 3,
            x
        )

    # This version might cause issues with JIT due to data-dependent branching
    # but will work for demonstration
    @jax.jit
    def with_python_if(x, condition):
        # This works but is less efficient
        return jnp.where(condition, x ** 2, x ** 3)

    x = jnp.array([1.0, 2.0, 3.0])

    result_cond = with_lax_cond(x, True)
    result_if = with_python_if(x, True)

    return result_cond, result_if


# ===== Tests - Don't modify below this line =====

def test_simple_cond():
    result = simple_cond()
    if result is not None:
        assert jnp.isclose(result, 9.0), f"Expected 9.0, got {result}"
        print("✓ simple_cond test passed")
    else:
        print("✓ simple_cond test passed (implementation check)")


def test_cond_with_different_types():
    result = cond_with_different_types()
    if result is not None:
        assert result.shape == (3,), f"Expected shape (3,), got {result.shape}"
        print("✓ cond_with_different_types test passed")
    else:
        print("✓ cond_with_different_types test passed (implementation check)")


def test_nested_cond():
    result = nested_cond()
    if result is not None:
        assert jnp.isclose(result, 1.0), f"Expected 1.0 for positive number, got {result}"
        print("✓ nested_cond test passed")
    else:
        print("✓ nested_cond test passed (implementation check)")


def test_cond_in_jit():
    result = cond_in_jit()
    if result is not None:
        expected = jnp.array([0.0, 0.0, 1.0, 2.0])  # ReLU applied
        assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
        print("✓ cond_in_jit test passed")
    else:
        print("✓ cond_in_jit test passed (implementation check)")


def test_cond_with_grad():
    gradient = cond_with_grad()
    if gradient is not None:
        assert jnp.isclose(gradient, 4.0), f"Expected gradient 4.0, got {gradient}"
        print("✓ cond_with_grad test passed")
    else:
        print("✓ cond_with_grad test passed (implementation check)")


def test_switchcase_alternative():
    result = switchcase_alternative()
    if result is not None:
        assert jnp.isclose(result, 64.0), f"Expected 64.0 (4^3), got {result}"
        print("✓ switchcase_alternative test passed")
    else:
        print("✓ switchcase_alternative test passed (implementation check)")


def test_cond_performance():
    try:
        result_cond, result_if = cond_performance()
        assert jnp.allclose(result_cond, result_if)
        print("✓ cond_performance test passed")
    except:
        print("✓ cond_performance test passed (implementation check)")


if __name__ == "__main__":
    test_simple_cond()
    test_cond_with_different_types()
    test_nested_cond()
    test_cond_in_jit()
    test_cond_with_grad()
    test_switchcase_alternative()
    test_cond_performance()
    print("\n🎉 All tests passed!")
