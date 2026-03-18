"""
Exercise: Combining Transformations
====================================

The real power of JAX comes from combining transformations!

You can compose jit, grad, and vmap in any order to create
highly optimized, vectorized, differentiable functions.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def jit_grad_combo():
    """
    Combine JIT and grad for fast gradient computation.

    f(x) = sum(x^3) + 2*sum(x^2)

    Create a JIT-compiled gradient function.
    """
    def f(x):
        return jnp.sum(x ** 3) + 2 * jnp.sum(x ** 2)

    # TODO: Combine jit and grad
    # Option 1: jax.jit(jax.grad(f))
    # Option 2: @jax.jit decorator on grad function
    fast_grad = None

    x = jnp.array([1.0, 2.0, 3.0])
    return None  # Evaluate fast_grad(x)


def vmap_grad_combo():
    """
    Combine vmap and grad to compute gradients for a batch.

    This is extremely useful in machine learning!

    f(x) = x^T @ x (dot product with itself)

    Compute gradients for a batch of inputs.
    """
    def f(x):
        return jnp.dot(x, x)

    # TODO: Combine vmap and grad
    # jax.vmap(jax.grad(f))
    batch_grad = None

    batch = jnp.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0]
    ])
    return None


def jit_vmap_grad():
    """
    Combine all three: JIT + vmap + grad!

    This is the pattern used in many ML frameworks.

    f(w, x) = sum((w * x)^2)

    Create a JIT-compiled, vectorized gradient function w.r.t. w.
    """
    def loss(w, x):
        return jnp.sum((w * x) ** 2)

    # TODO: Combine jit, vmap, and grad
    # We want: gradient w.r.t. w, vectorized over batches of x
    # jax.jit(jax.vmap(jax.grad(loss, argnums=0), in_axes=(None, 0)))

    w = jnp.array([1.0, 2.0, 3.0])
    x_batch = jnp.array([
        [1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0]
    ])

    optimized_grad = None
    return None  # Evaluate optimized_grad(w, x_batch)


def grad_of_grad():
    """
    Compute Hessian (second derivatives) using nested grad.

    For f(x) = x^T @ A @ x where A is a matrix,
    compute the Hessian (matrix of second derivatives).
    """
    A = jnp.array([[2.0, 1.0], [1.0, 2.0]])

    def f(x):
        return jnp.dot(x, jnp.dot(A, x))

    # TODO: Compute Hessian using jacfwd or nested grad
    # Hint: jax.jacfwd(jax.grad(f))
    hessian_fn = None

    x = jnp.array([1.0, 2.0])
    return None  # Evaluate hessian_fn(x)


def per_example_gradients():
    """
    Compute per-example gradients in a batch.

    This is useful for techniques like gradient clipping per example.

    loss(w, x, y) = (w @ x - y)^2

    Compute gradient w.r.t. w for each example in the batch separately.
    """
    def loss(w, x, y):
        pred = jnp.dot(w, x)
        return (pred - y) ** 2

    w = jnp.array([1.0, 2.0, 3.0])

    x_batch = jnp.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ])
    y_batch = jnp.array([2.0, 4.0, 6.0])

    # TODO: Create function that computes per-example gradients
    # Use vmap over examples, grad w.r.t. w
    # jax.vmap(jax.grad(loss, argnums=0), in_axes=(None, 0, 0))
    per_example_grad = None

    return None  # Evaluate per_example_grad(w, x_batch, y_batch)


# ===== Tests - Don't modify below this line =====

def test_jit_grad_combo():
    result = jit_grad_combo()
    if result is None:
        def f(x):
            return jnp.sum(x ** 3) + 2 * jnp.sum(x ** 2)
        fast_grad = jax.jit(jax.grad(f))
        result = fast_grad(jnp.array([1.0, 2.0, 3.0]))

    # Gradient: 3x^2 + 4x
    expected = jnp.array([7.0, 20.0, 39.0])  # [3+4, 12+8, 27+12]
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ jit_grad_combo test passed")


def test_vmap_grad_combo():
    result = vmap_grad_combo()
    if result is None:
        def f(x):
            return jnp.dot(x, x)
        batch_grad = jax.vmap(jax.grad(f))
        batch = jnp.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = batch_grad(batch)

    # Gradient of x^T x is 2x
    expected = jnp.array([[2.0, 4.0, 6.0], [8.0, 10.0, 12.0]])
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ vmap_grad_combo test passed")


def test_jit_vmap_grad():
    result = jit_vmap_grad()
    if result is None:
        def loss(w, x):
            return jnp.sum((w * x) ** 2)
        optimized_grad = jax.jit(jax.vmap(jax.grad(loss, argnums=0), in_axes=(None, 0)))
        w = jnp.array([1.0, 2.0, 3.0])
        x_batch = jnp.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])
        result = optimized_grad(w, x_batch)

    assert result.shape == (2, 3), f"Expected shape (2, 3), got {result.shape}"
    print("✓ jit_vmap_grad test passed")


def test_grad_of_grad():
    result = grad_of_grad()
    if result is None:
        A = jnp.array([[2.0, 1.0], [1.0, 2.0]])
        def f(x):
            return jnp.dot(x, jnp.dot(A, x))
        hessian_fn = jax.jacfwd(jax.grad(f))
        result = hessian_fn(jnp.array([1.0, 2.0]))

    # Hessian should be 2*A for quadratic forms
    assert result.shape == (2, 2), f"Expected shape (2, 2), got {result.shape}"
    print("✓ grad_of_grad test passed")


def test_per_example_gradients():
    result = per_example_gradients()
    if result is None:
        def loss(w, x, y):
            pred = jnp.dot(w, x)
            return (pred - y) ** 2
        per_example_grad = jax.vmap(jax.grad(loss, argnums=0), in_axes=(None, 0, 0))
        w = jnp.array([1.0, 2.0, 3.0])
        x_batch = jnp.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        y_batch = jnp.array([2.0, 4.0, 6.0])
        result = per_example_grad(w, x_batch, y_batch)

    assert result.shape == (3, 3), f"Expected shape (3, 3), got {result.shape}"
    print("✓ per_example_gradients test passed")


if __name__ == "__main__":
    test_jit_grad_combo()
    test_vmap_grad_combo()
    test_jit_vmap_grad()
    test_grad_of_grad()
    test_per_example_gradients()
    print("\n🎉 All tests passed!")
