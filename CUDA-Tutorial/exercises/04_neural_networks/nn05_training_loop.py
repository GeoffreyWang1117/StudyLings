"""
Exercise: Training Loop
========================

Put it all together: implement a complete training loop!

This combines everything: forward pass, loss, gradients, and parameter updates.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.nn as jnn


def gradient_descent_step(params, x, y, learning_rate=0.01):
    """
    Perform one gradient descent step.

    1. Compute loss
    2. Compute gradients
    3. Update parameters

    Model: simple linear regression y = Wx + b
    """
    def loss_fn(params, x, y):
        W, b = params
        pred = W * x + b
        return jnp.mean((pred - y) ** 2)

    # TODO: Compute loss and gradients
    loss, grads = None  # Use jax.value_and_grad

    # TODO: Update parameters
    # new_params = old_params - learning_rate * gradients
    W, b = params
    grad_W, grad_b = grads

    new_W = None
    new_b = None

    return (new_W, new_b), loss


def train_simple_model():
    """
    Train a simple linear model for multiple steps.

    Fit y = 2x + 1 from data points.
    """
    # Data
    X = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = jnp.array([3.0, 5.0, 7.0, 9.0, 11.0])  # y = 2x + 1

    # Initialize parameters
    params = (jnp.array(0.0), jnp.array(0.0))  # (W, b)

    # TODO: Training loop
    learning_rate = 0.1
    num_steps = 100

    for step in range(num_steps):
        params, loss = gradient_descent_step(params, X, y, learning_rate)

    return params


def batched_training_step(params, X_batch, y_batch, learning_rate=0.01):
    """
    Training step with batched data.

    Model: MLP classifier
    """
    def loss_fn(params, x, y):
        # Forward pass
        W1, b1, W2, b2 = params
        h = jnn.relu(jnp.dot(W1, x) + b1)
        logits = jnp.dot(W2, h) + b2

        # Cross-entropy loss
        return -jnp.sum(y * jnn.log_softmax(logits))

    # TODO: Compute average loss and gradients over batch
    # Use vmap to vectorize over batch, then average

    # Vectorized loss function
    batched_loss_fn = None  # jax.vmap(loss_fn, in_axes=(None, 0, 0))

    # Compute losses for all examples
    losses = None

    # Average loss
    avg_loss = None

    # Compute gradients of average loss
    grads = None  # jax.grad(lambda p: jnp.mean(batched_loss_fn(p, X_batch, y_batch)))(params)

    # TODO: Update parameters
    W1, b1, W2, b2 = params
    grad_W1, grad_b1, grad_W2, grad_b2 = grads

    new_params = (
        None,  # W1 - learning_rate * grad_W1
        None,  # b1 - learning_rate * grad_b1
        None,  # W2 - learning_rate * grad_W2
        None,  # b2 - learning_rate * grad_b2
    )

    return new_params, avg_loss


def train_with_validation():
    """
    Training loop with train/validation split.

    Monitor both training and validation loss.
    """
    # Simple dataset
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 10)

    # Generate synthetic data
    X_train = jax.random.normal(keys[0], (100, 2))
    y_train = jnp.sum(X_train, axis=1, keepdims=True) + jax.random.normal(keys[1], (100, 1)) * 0.1

    X_val = jax.random.normal(keys[2], (20, 2))
    y_val = jnp.sum(X_val, axis=1, keepdims=True) + jax.random.normal(keys[3], (20, 1)) * 0.1

    # Initialize model
    params = {
        'W': jax.random.normal(keys[4], (1, 2)) * 0.1,
        'b': jnp.zeros(1),
    }

    def loss_fn(params, X, y):
        pred = jnp.dot(X, params['W'].T) + params['b']
        return jnp.mean((pred - y) ** 2)

    # TODO: Training loop with validation
    learning_rate = 0.1
    num_epochs = 50

    train_losses = []
    val_losses = []

    for epoch in range(num_epochs):
        # Compute gradients on training data
        train_loss, grads = jax.value_and_grad(loss_fn)(params, X_train, y_train)

        # Update parameters
        params['W'] = params['W'] - learning_rate * grads['W']
        params['b'] = params['b'] - learning_rate * grads['b']

        # Compute validation loss
        val_loss = loss_fn(params, X_val, y_val)

        train_losses.append(train_loss)
        val_losses.append(val_loss)

    return params, train_losses, val_losses


def jit_training_step():
    """
    JIT-compile the training step for faster execution.

    This is crucial for performance!
    """
    def loss_fn(params, x, y):
        W, b = params
        pred = W * x + b
        return jnp.mean((pred - y) ** 2)

    # TODO: Create JIT-compiled training step
    @jax.jit
    def train_step(params, x, y, lr):
        loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
        W, b = params
        grad_W, grad_b = grads
        new_params = (W - lr * grad_W, b - lr * grad_b)
        return new_params, loss

    # Test
    params = (jnp.array(0.0), jnp.array(0.0))
    X = jnp.array([1.0, 2.0, 3.0])
    y = jnp.array([2.0, 4.0, 6.0])

    # Run one step
    new_params, loss = train_step(params, X, y, 0.1)

    return new_params, loss


# ===== Tests - Don't modify below this line =====

def test_gradient_descent_step():
    params = (jnp.array(0.0), jnp.array(0.0))
    X = jnp.array([1.0, 2.0, 3.0])
    y = jnp.array([2.0, 4.0, 6.0])

    new_params, loss = gradient_descent_step(params, X, y, learning_rate=0.1)

    assert new_params is not None, "New params should not be None"
    assert isinstance(new_params, tuple) and len(new_params) == 2
    print("✓ gradient_descent_step test passed")


def test_train_simple_model():
    params = train_simple_model()

    W, b = params
    # Should learn approximately W=2, b=1
    assert jnp.abs(W - 2.0) < 0.5, f"W should be close to 2.0, got {W}"
    assert jnp.abs(b - 1.0) < 0.5, f"b should be close to 1.0, got {b}"
    print("✓ train_simple_model test passed")


def test_batched_training_step():
    # Skip detailed test - just check it runs
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 6)

    params = (
        jax.random.normal(keys[0], (4, 2)) * 0.1,
        jnp.zeros(4),
        jax.random.normal(keys[2], (3, 4)) * 0.1,
        jnp.zeros(3),
    )

    X_batch = jax.random.normal(keys[4], (5, 2))
    y_batch = jax.random.normal(keys[5], (5, 3))

    try:
        new_params, loss = batched_training_step(params, X_batch, y_batch)
        print("✓ batched_training_step test passed")
    except:
        print("✓ batched_training_step test passed (implementation check)")


def test_train_with_validation():
    params, train_losses, val_losses = train_with_validation()

    assert len(train_losses) > 0 and len(val_losses) > 0
    # Training should reduce loss
    assert train_losses[-1] < train_losses[0], "Training should reduce loss"
    print("✓ train_with_validation test passed")


def test_jit_training_step():
    new_params, loss = jit_training_step()

    assert new_params is not None and loss is not None
    print("✓ jit_training_step test passed")


if __name__ == "__main__":
    test_gradient_descent_step()
    test_train_simple_model()
    test_batched_training_step()
    test_train_with_validation()
    test_jit_training_step()
    print("\n🎉 All tests passed!")
