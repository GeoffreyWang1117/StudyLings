"""
Exercise: Loss Functions
=========================

Loss functions measure how well the model's predictions match the targets.

Implement common loss functions used in machine learning!
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def mse_loss(predictions, targets):
    """
    Mean Squared Error Loss.

    MSE = mean((predictions - targets)^2)

    Used for regression tasks.
    """
    # TODO: Implement MSE loss
    return None


def mae_loss(predictions, targets):
    """
    Mean Absolute Error Loss.

    MAE = mean(|predictions - targets|)

    Less sensitive to outliers than MSE.
    """
    # TODO: Implement MAE loss
    return None


def binary_cross_entropy(predictions, targets):
    """
    Binary Cross-Entropy Loss.

    BCE = -mean(targets * log(predictions) + (1 - targets) * log(1 - predictions))

    Used for binary classification.

    Hint: Add small epsilon to avoid log(0)
    """
    epsilon = 1e-7
    # TODO: Implement BCE loss
    # Clip predictions to avoid log(0)
    predictions = jnp.clip(predictions, epsilon, 1 - epsilon)
    return None


def categorical_cross_entropy(predictions, targets):
    """
    Categorical Cross-Entropy Loss.

    CCE = -mean(sum(targets * log(predictions)))

    Used for multi-class classification.
    predictions and targets are one-hot encoded.
    """
    epsilon = 1e-7
    predictions = jnp.clip(predictions, epsilon, 1.0)
    # TODO: Implement categorical cross-entropy
    return None


def sparse_categorical_cross_entropy(logits, labels):
    """
    Sparse Categorical Cross-Entropy.

    Takes logits (before softmax) and integer labels.
    More efficient than one-hot encoding.

    Hint: Use jax.nn.log_softmax and jnp.take_along_axis
    """
    # TODO: Implement sparse categorical cross-entropy
    # 1. Apply log_softmax to logits
    # 2. Select the log probability of the true class
    # 3. Return negative mean

    return None


def huber_loss(predictions, targets, delta=1.0):
    """
    Huber Loss (smooth L1 loss).

    Combines MSE for small errors and MAE for large errors.

    Huber(x) = 0.5 * x^2 if |x| <= delta
               delta * (|x| - 0.5 * delta) otherwise

    where x = predictions - targets
    """
    diff = predictions - targets
    # TODO: Implement Huber loss
    return None


def loss_with_regularization():
    """
    Implement loss with L2 regularization.

    Total loss = MSE loss + lambda * L2 regularization

    L2 reg = sum(W^2)  (sum of squared weights)
    """
    predictions = jnp.array([1.0, 2.0, 3.0])
    targets = jnp.array([1.5, 2.5, 3.5])
    weights = jnp.array([[1.0, 2.0], [3.0, 4.0]])
    lambda_reg = 0.01

    # TODO: Compute MSE loss
    mse = None

    # TODO: Compute L2 regularization
    l2_reg = None

    # TODO: Return total loss
    return None


# ===== Tests - Don't modify below this line =====

def test_mse_loss():
    predictions = jnp.array([1.0, 2.0, 3.0])
    targets = jnp.array([1.0, 2.0, 3.0])
    result = mse_loss(predictions, targets)

    assert result is not None, "Result should not be None"
    assert jnp.isclose(result, 0.0), f"MSE of perfect predictions should be 0, got {result}"
    print("✓ mse_loss test passed")


def test_mae_loss():
    predictions = jnp.array([1.0, 2.0, 3.0])
    targets = jnp.array([2.0, 3.0, 4.0])
    result = mae_loss(predictions, targets)

    assert result is not None, "Result should not be None"
    assert jnp.isclose(result, 1.0), f"MAE should be 1.0, got {result}"
    print("✓ mae_loss test passed")


def test_binary_cross_entropy():
    predictions = jnp.array([0.9, 0.1, 0.8])
    targets = jnp.array([1.0, 0.0, 1.0])
    result = binary_cross_entropy(predictions, targets)

    assert result is not None, "Result should not be None"
    assert result > 0, "BCE should be positive"
    print("✓ binary_cross_entropy test passed")


def test_categorical_cross_entropy():
    predictions = jnp.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]])
    targets = jnp.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    result = categorical_cross_entropy(predictions, targets)

    assert result is not None, "Result should not be None"
    assert result > 0, "CCE should be positive"
    print("✓ categorical_cross_entropy test passed")


def test_sparse_categorical_cross_entropy():
    logits = jnp.array([[2.0, 1.0, 0.1], [0.5, 2.5, 0.3]])
    labels = jnp.array([0, 1])
    result = sparse_categorical_cross_entropy(logits, labels)

    assert result is not None, "Result should not be None"
    assert result > 0, "Loss should be positive"
    print("✓ sparse_categorical_cross_entropy test passed")


def test_huber_loss():
    predictions = jnp.array([1.0, 5.0, 10.0])
    targets = jnp.array([1.0, 2.0, 3.0])
    result = huber_loss(predictions, targets, delta=1.0)

    assert result is not None, "Result should not be None"
    assert result > 0, "Huber loss should be positive"
    print("✓ huber_loss test passed")


def test_loss_with_regularization():
    result = loss_with_regularization()

    assert result is not None, "Result should not be None"
    assert result > 0, "Total loss should be positive"
    print("✓ loss_with_regularization test passed")


if __name__ == "__main__":
    test_mse_loss()
    test_mae_loss()
    test_binary_cross_entropy()
    test_categorical_cross_entropy()
    test_sparse_categorical_cross_entropy()
    test_huber_loss()
    test_loss_with_regularization()
    print("\n🎉 All tests passed!")
