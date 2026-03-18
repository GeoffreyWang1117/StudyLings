"""
Exercise: Activation Functions
===============================

Activation functions introduce non-linearity into neural networks.

Learn to implement and use common activation functions!
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.nn as jnn


def relu_activation(x):
    """
    Implement ReLU: f(x) = max(0, x)

    Hint: Use jnp.maximum(0, x) or jnn.relu(x)
    """
    # TODO: Implement ReLU
    return None


def sigmoid_activation(x):
    """
    Implement Sigmoid: f(x) = 1 / (1 + exp(-x))

    Hint: Use jnn.sigmoid(x)
    """
    # TODO: Implement sigmoid
    return None


def tanh_activation(x):
    """
    Implement Tanh: f(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))

    Hint: Use jnp.tanh(x)
    """
    # TODO: Implement tanh
    return None


def softmax_activation(x):
    """
    Implement Softmax: softmax(x)_i = exp(x_i) / sum(exp(x_j))

    Used for multi-class classification.

    Hint: Use jnn.softmax(x)
    """
    # TODO: Implement softmax
    return None


def leaky_relu(x, alpha=0.01):
    """
    Implement Leaky ReLU: f(x) = x if x > 0 else alpha * x

    Hint: Use jnp.where(x > 0, x, alpha * x) or jnn.leaky_relu
    """
    # TODO: Implement leaky ReLU
    return None


def gelu_activation(x):
    """
    Implement GELU (Gaussian Error Linear Unit).

    GELU is used in modern transformers like BERT and GPT.

    Hint: Use jnn.gelu(x)
    """
    # TODO: Implement GELU
    return None


def activation_derivative():
    """
    Compute derivative of ReLU using JAX's autodiff.

    For x = 2.0, ReLU'(x) = 1.0
    For x = -1.0, ReLU'(x) = 0.0
    """
    def relu(x):
        return jnp.maximum(0, x)

    # TODO: Use jax.grad to compute derivative
    relu_grad = None

    # Test at x = 2.0
    return None  # Evaluate relu_grad(2.0)


# ===== Tests - Don't modify below this line =====

def test_relu_activation():
    x = jnp.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    result = relu_activation(x)

    expected = jnp.array([0.0, 0.0, 0.0, 1.0, 2.0])
    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ relu_activation test passed")


def test_sigmoid_activation():
    x = jnp.array([0.0])
    result = sigmoid_activation(x)

    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, 0.5), f"Sigmoid(0) should be 0.5, got {result}"
    print("✓ sigmoid_activation test passed")


def test_tanh_activation():
    x = jnp.array([0.0])
    result = tanh_activation(x)

    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, 0.0), f"Tanh(0) should be 0.0, got {result}"
    print("✓ tanh_activation test passed")


def test_softmax_activation():
    x = jnp.array([1.0, 2.0, 3.0])
    result = softmax_activation(x)

    assert result is not None, "Result should not be None"
    assert jnp.allclose(jnp.sum(result), 1.0), "Softmax should sum to 1"
    assert jnp.all(result >= 0) and jnp.all(result <= 1), "Softmax should be in [0, 1]"
    print("✓ softmax_activation test passed")


def test_leaky_relu():
    x = jnp.array([-2.0, 0.0, 2.0])
    result = leaky_relu(x, alpha=0.1)

    expected = jnp.array([-0.2, 0.0, 2.0])
    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ leaky_relu test passed")


def test_gelu_activation():
    x = jnp.array([0.0])
    result = gelu_activation(x)

    assert result is not None, "Result should not be None"
    assert jnp.allclose(result, 0.0, atol=1e-6), f"GELU(0) should be ~0, got {result}"
    print("✓ gelu_activation test passed")


def test_activation_derivative():
    result = activation_derivative()

    if result is None:
        def relu(x):
            return jnp.maximum(0, x)
        relu_grad = jax.grad(relu)
        result = relu_grad(2.0)

    assert jnp.isclose(result, 1.0), f"ReLU'(2.0) should be 1.0, got {result}"
    print("✓ activation_derivative test passed")


if __name__ == "__main__":
    test_relu_activation()
    test_sigmoid_activation()
    test_tanh_activation()
    test_softmax_activation()
    test_leaky_relu()
    test_gelu_activation()
    test_activation_derivative()
    print("\n🎉 All tests passed!")
