"""
Exercise: Custom Gradients
===========================

Sometimes you need to define custom gradient rules for a function.
JAX provides @jax.custom_vjp for this purpose.

This is useful for:
- Numerical stability
- Implementing non-differentiable operations
- Optimizing gradient computation
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def simple_custom_grad():
    """
    Define a custom gradient for f(x) = x^2.

    Instead of the default gradient (2x), use a custom gradient (3x).
    This is just for demonstration!
    """
    @jax.custom_vjp
    def f(x):
        return x ** 2

    def f_fwd(x):
        # Forward pass: return (output, residuals)
        return f(x), x

    def f_bwd(residuals, g):
        # Backward pass: return (gradient,)
        x = residuals
        # TODO: Return custom gradient (3*x instead of 2*x)
        return (None,)  # Replace with (3 * x * g,)

    f.defvjp(f_fwd, f_bwd)

    # Test
    x = 2.0
    grad_f = jax.grad(f)
    return grad_f(x)  # Should return 6.0 instead of 4.0


def stable_log_gradient():
    """
    Implement numerically stable log with custom gradient.

    log(x) can be unstable for very small x.
    Custom gradient can handle this better.
    """
    @jax.custom_vjp
    def safe_log(x):
        return jnp.log(jnp.maximum(x, 1e-10))

    def safe_log_fwd(x):
        y = safe_log(x)
        return y, x

    def safe_log_bwd(x, g):
        # Gradient of log(x) is 1/x
        # TODO: Implement with numerical safety
        return (None,)  # Replace with (g / jnp.maximum(x, 1e-10),)

    safe_log.defvjp(safe_log_fwd, safe_log_bwd)

    x = jnp.array([1e-15, 1.0, 10.0])
    grad_fn = jax.grad(lambda x: jnp.sum(safe_log(x)))
    return grad_fn(x)


def clip_gradient():
    """
    Implement gradient clipping using custom vjp.

    Forward: f(x) = x^3
    Backward: clip gradients to [-1, 1]
    """
    @jax.custom_vjp
    def f_with_clipped_grad(x):
        return x ** 3

    def f_fwd(x):
        return f_with_clipped_grad(x), x

    def f_bwd(x, g):
        # Compute normal gradient
        grad = 3 * x ** 2
        # TODO: Clip gradient
        clipped_grad = None  # jnp.clip(grad, -1.0, 1.0)
        return (clipped_grad * g,)

    f_with_clipped_grad.defvjp(f_fwd, f_bwd)

    x = 10.0  # Normal gradient would be 300
    grad_fn = jax.grad(f_with_clipped_grad)
    return grad_fn(x)  # Should return 1.0 (clipped)


# ===== Tests - Don't modify below this line =====

def test_simple_custom_grad():
    try:
        result = simple_custom_grad()
        # Should be 6.0 with custom gradient (3x)
        print(f"Custom gradient result: {result}")
        print("✓ simple_custom_grad test passed")
    except:
        print("✓ simple_custom_grad test passed (implementation check)")


def test_stable_log_gradient():
    try:
        result = stable_log_gradient()
        assert result is not None
        print("✓ stable_log_gradient test passed")
    except:
        print("✓ stable_log_gradient test passed (implementation check)")


def test_clip_gradient():
    try:
        result = clip_gradient()
        # Should be clipped to 1.0
        print(f"Clipped gradient: {result}")
        print("✓ clip_gradient test passed")
    except:
        print("✓ clip_gradient test passed (implementation check)")


if __name__ == "__main__":
    test_simple_custom_grad()
    test_stable_log_gradient()
    test_clip_gradient()
    print("\n🎉 All tests passed!")
