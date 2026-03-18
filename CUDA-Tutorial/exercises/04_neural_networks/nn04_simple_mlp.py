"""
Exercise: Multi-Layer Perceptron (MLP)
=======================================

Build a simple neural network by stacking linear layers with activations!

An MLP is a feedforward neural network with multiple layers.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.nn as jnn


def simple_mlp_forward(params, x):
    """
    Implement a 2-layer MLP forward pass.

    Architecture:
    Input -> Linear(W1, b1) -> ReLU -> Linear(W2, b2) -> Output

    Args:
        params: Dictionary with keys 'W1', 'b1', 'W2', 'b2'
        x: Input vector

    Returns:
        Output vector
    """
    W1, b1 = params['W1'], params['b1']
    W2, b2 = params['W2'], params['b2']

    # TODO: Implement forward pass
    # Layer 1: linear + ReLU
    hidden = None

    # Layer 2: linear (no activation)
    output = None

    return None


def mlp_with_multiple_hidden():
    """
    Implement a 3-layer MLP (2 hidden layers).

    Architecture:
    Input(2) -> Hidden(4) -> ReLU -> Hidden(4) -> ReLU -> Output(1)
    """
    # Initialize parameters
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 6)

    params = {
        'W1': jax.random.normal(keys[0], (4, 2)) * 0.1,
        'b1': jnp.zeros(4),
        'W2': jax.random.normal(keys[2], (4, 4)) * 0.1,
        'b2': jnp.zeros(4),
        'W3': jax.random.normal(keys[4], (1, 4)) * 0.1,
        'b3': jnp.zeros(1),
    }

    x = jnp.array([1.0, 2.0])

    # TODO: Implement 3-layer forward pass
    # Layer 1
    h1 = None

    # Layer 2
    h2 = None

    # Output layer
    output = None

    return output


def mlp_classifier():
    """
    Implement MLP for classification (with softmax output).

    Architecture:
    Input -> Hidden -> ReLU -> Output -> Softmax
    """
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    # Network: input_dim=3, hidden_dim=5, output_dim=3
    params = {
        'W1': jax.random.normal(keys[0], (5, 3)) * 0.1,
        'b1': jnp.zeros(5),
        'W2': jax.random.normal(keys[2], (3, 5)) * 0.1,
        'b2': jnp.zeros(3),
    }

    x = jnp.array([1.0, 0.5, 0.2])

    # TODO: Forward pass with softmax at the end
    # Hidden layer
    hidden = None

    # Output layer (logits)
    logits = None

    # Softmax
    probs = None

    return probs


def batched_mlp():
    """
    Implement batched MLP using vmap.

    Process multiple inputs at once efficiently.
    """
    def mlp_single(params, x):
        # Single example forward pass
        W1, b1 = params['W1'], params['b1']
        W2, b2 = params['W2'], params['b2']

        h = jnn.relu(jnp.dot(W1, x) + b1)
        output = jnp.dot(W2, h) + b2
        return output

    # Initialize params
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    params = {
        'W1': jax.random.normal(keys[0], (4, 2)) * 0.1,
        'b1': jnp.zeros(4),
        'W2': jax.random.normal(keys[2], (3, 4)) * 0.1,
        'b2': jnp.zeros(3),
    }

    # Batch of inputs
    X_batch = jnp.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

    # TODO: Use vmap to process batch
    # Hint: jax.vmap(mlp_single, in_axes=(None, 0))
    batched_forward = None

    return None  # Call batched_forward(params, X_batch)


def mlp_with_dropout():
    """
    Implement MLP with dropout for regularization.

    Dropout randomly sets some activations to zero during training.
    """
    def mlp_forward(params, x, key, training=True, dropout_rate=0.5):
        W1, b1 = params['W1'], params['b1']
        W2, b2 = params['W2'], params['b2']

        # Layer 1
        h = jnn.relu(jnp.dot(W1, x) + b1)

        # Apply dropout
        if training:
            # TODO: Implement dropout
            # Hint: Generate random mask and scale
            keep_prob = 1.0 - dropout_rate
            mask = jax.random.bernoulli(key, keep_prob, h.shape)
            h = jnp.where(mask, h / keep_prob, 0)

        # Layer 2
        output = jnp.dot(W2, h) + b2
        return output

    # Initialize
    key = jax.random.PRNGKey(42)
    keys = jax.random.split(key, 5)

    params = {
        'W1': jax.random.normal(keys[0], (4, 2)) * 0.1,
        'b1': jnp.zeros(4),
        'W2': jax.random.normal(keys[2], (3, 4)) * 0.1,
        'b2': jnp.zeros(3),
    }

    x = jnp.array([1.0, 2.0])

    # Training mode
    output_train = mlp_forward(params, x, keys[4], training=True)

    # Inference mode (no dropout)
    output_test = mlp_forward(params, x, keys[4], training=False)

    return output_train, output_test


# ===== Tests - Don't modify below this line =====

def test_simple_mlp_forward():
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    params = {
        'W1': jax.random.normal(keys[0], (4, 2)) * 0.1,
        'b1': jnp.zeros(4),
        'W2': jax.random.normal(keys[2], (3, 4)) * 0.1,
        'b2': jnp.zeros(3),
    }

    x = jnp.array([1.0, 2.0])
    result = simple_mlp_forward(params, x)

    assert result is not None, "Result should not be None"
    assert result.shape == (3,), f"Expected shape (3,), got {result.shape}"
    print("✓ simple_mlp_forward test passed")


def test_mlp_with_multiple_hidden():
    result = mlp_with_multiple_hidden()

    assert result is not None, "Result should not be None"
    assert result.shape == (1,), f"Expected shape (1,), got {result.shape}"
    print("✓ mlp_with_multiple_hidden test passed")


def test_mlp_classifier():
    result = mlp_classifier()

    assert result is not None, "Result should not be None"
    assert result.shape == (3,), f"Expected shape (3,), got {result.shape}"
    assert jnp.allclose(jnp.sum(result), 1.0), "Softmax should sum to 1"
    print("✓ mlp_classifier test passed")


def test_batched_mlp():
    result = batched_mlp()

    assert result is not None, "Result should not be None"
    assert result.shape == (3, 3), f"Expected shape (3, 3), got {result.shape}"
    print("✓ batched_mlp test passed")


def test_mlp_with_dropout():
    output_train, output_test = mlp_with_dropout()

    assert output_train is not None and output_test is not None
    assert output_train.shape == (3,) and output_test.shape == (3,)
    print("✓ mlp_with_dropout test passed")


if __name__ == "__main__":
    test_simple_mlp_forward()
    test_mlp_with_multiple_hidden()
    test_mlp_classifier()
    test_batched_mlp()
    test_mlp_with_dropout()
    print("\n🎉 All tests passed!")
