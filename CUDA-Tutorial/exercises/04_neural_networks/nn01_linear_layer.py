"""
Exercise: Linear Layer
=======================

Implement a simple linear layer (fully connected layer).

Linear layer: y = Wx + b
Where:
- W is the weight matrix
- x is the input vector
- b is the bias vector
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def linear_forward(W, b, x):
    """
    Implement forward pass of a linear layer.

    Args:
        W: Weight matrix of shape (output_dim, input_dim)
        b: Bias vector of shape (output_dim,)
        x: Input vector of shape (input_dim,)

    Returns:
        Output vector of shape (output_dim,)

    Hint: Use jnp.dot(W, x) + b
    """
    # TODO: Implement linear layer
    return None


def linear_batch(W, b, X):
    """
    Implement batched linear layer.

    Args:
        W: Weight matrix of shape (output_dim, input_dim)
        b: Bias vector of shape (output_dim,)
        X: Input batch of shape (batch_size, input_dim)

    Returns:
        Output batch of shape (batch_size, output_dim)

    Hint: Use jnp.dot(X, W.T) + b or vmap the single-example version
    """
    # TODO: Implement batched linear layer
    return None


def initialize_linear_layer(input_dim, output_dim, key):
    """
    Initialize weights and biases for a linear layer.

    Args:
        input_dim: Input dimension
        output_dim: Output dimension
        key: JAX random key

    Returns:
        (W, b) tuple

    Hint: Use jax.random.normal for weights, jnp.zeros for biases
    Common initialization: W ~ N(0, 1/sqrt(input_dim))
    """
    # TODO: Initialize W and b
    # Split key for W and b initialization
    key_w, key_b = jax.random.split(key)

    # Initialize W with small random values
    W = None  # Shape: (output_dim, input_dim)

    # Initialize b with zeros
    b = None  # Shape: (output_dim,)

    return W, b


def linear_with_gradient():
    """
    Compute gradient of loss w.r.t. weights.

    Loss = sum((Wx + b - target)^2)

    Returns gradient of loss w.r.t. W
    """
    def loss_fn(W, b, x, target):
        pred = jnp.dot(W, x) + b
        return jnp.sum((pred - target) ** 2)

    # Test data
    W = jnp.array([[1.0, 2.0], [3.0, 4.0]])
    b = jnp.array([0.1, 0.2])
    x = jnp.array([1.0, 1.0])
    target = jnp.array([2.0, 5.0])

    # TODO: Compute gradient w.r.t. W (argnums=0)
    grad_fn = None  # jax.grad(loss_fn, argnums=0)
    return None  # Evaluate grad_fn(W, b, x, target)


# ===== Tests - Don't modify below this line =====

def test_linear_forward():
    W = jnp.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = jnp.array([0.1, 0.2])
    x = jnp.array([1.0, 0.0, 1.0])

    result = linear_forward(W, b, x)
    expected = jnp.array([4.1, 10.2])  # [1*1 + 0*2 + 1*3 + 0.1, 1*4 + 0*5 + 1*6 + 0.2]

    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ linear_forward test passed")


def test_linear_batch():
    W = jnp.array([[1.0, 2.0], [3.0, 4.0]])
    b = jnp.array([0.1, 0.2])
    X = jnp.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])

    result = linear_batch(W, b, X)

    assert result is not None, "Result should not be None"
    assert result.shape == (3, 2), f"Expected shape (3, 2), got {result.shape}"
    print("✓ linear_batch test passed")


def test_initialize_linear_layer():
    key = jax.random.PRNGKey(0)
    W, b = initialize_linear_layer(3, 2, key)

    assert W is not None and b is not None, "W and b should not be None"
    assert W.shape == (2, 3), f"Expected W shape (2, 3), got {W.shape}"
    assert b.shape == (2,), f"Expected b shape (2,), got {b.shape}"
    print("✓ initialize_linear_layer test passed")


def test_linear_with_gradient():
    result = linear_with_gradient()

    if result is None:
        def loss_fn(W, b, x, target):
            pred = jnp.dot(W, x) + b
            return jnp.sum((pred - target) ** 2)
        W = jnp.array([[1.0, 2.0], [3.0, 4.0]])
        b = jnp.array([0.1, 0.2])
        x = jnp.array([1.0, 1.0])
        target = jnp.array([2.0, 5.0])
        grad_fn = jax.grad(loss_fn, argnums=0)
        result = grad_fn(W, b, x, target)

    assert result is not None, "Gradient should not be None"
    assert result.shape == (2, 2), f"Expected shape (2, 2), got {result.shape}"
    print("✓ linear_with_gradient test passed")


if __name__ == "__main__":
    test_linear_forward()
    test_linear_batch()
    test_initialize_linear_layer()
    test_linear_with_gradient()
    print("\n🎉 All tests passed!")
