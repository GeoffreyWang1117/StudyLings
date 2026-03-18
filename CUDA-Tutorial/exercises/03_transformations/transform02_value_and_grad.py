"""
Exercise: Value and Gradient
=============================

Often we need both the function value AND its gradient.
jax.value_and_grad provides both efficiently!

This is very useful in optimization where you need the loss and its gradient.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def compute_value_and_grad():
    """
    Compute both f(x) and f'(x) for f(x) = x^2 at x = 4.0.

    Should return: (value=16.0, grad=8.0)
    """
    def f(x):
        return x ** 2

    # TODO: Use jax.value_and_grad
    value_and_grad_f = None
    value, grad = None, None  # Call value_and_grad_f(4.0)
    return value, grad


def loss_and_gradient():
    """
    Compute MSE loss and its gradient.

    MSE = mean((predictions - targets)^2)

    Given predictions = [2.0, 4.0, 6.0] and targets = [1.0, 3.0, 5.0],
    compute both the loss value and gradient w.r.t. predictions.
    """
    def mse_loss(predictions, targets):
        return jnp.mean((predictions - targets) ** 2)

    predictions = jnp.array([2.0, 4.0, 6.0])
    targets = jnp.array([1.0, 3.0, 5.0])

    # TODO: Compute loss and gradient w.r.t. predictions
    # Hint: jax.value_and_grad(mse_loss, argnums=0)
    value_and_grad_fn = None
    loss, grad = None, None
    return loss, grad


def multi_output_grad():
    """
    For functions with multiple outputs, we can get gradients of each.

    f(x) = x^2 + 2*x
    Returns (value, gradient) at x = 3.0

    value = 3^2 + 2*3 = 15
    grad = 2*3 + 2 = 8
    """
    def f(x):
        return x**2 + 2*x

    # TODO: Compute value and gradient at x = 3.0
    value_and_grad_f = None
    return None


def gradient_with_aux():
    """
    Sometimes we want to return auxiliary data along with the loss.
    Use has_aux=True for this.

    Function returns (loss, aux_data).
    value_and_grad with has_aux=True returns ((loss, aux), grad).
    """
    def f_with_aux(x):
        loss = x ** 2
        aux = {"squared": loss, "doubled": 2 * x}
        return loss, aux

    # TODO: Use jax.value_and_grad with has_aux=True
    # Evaluate at x = 5.0
    value_and_grad_f = None  # jax.value_and_grad(f_with_aux, has_aux=True)
    (value, aux), grad = None, None
    return value, aux, grad


# ===== Tests - Don't modify below this line =====

def test_compute_value_and_grad():
    value, grad = compute_value_and_grad()
    assert jnp.isclose(value, 16.0), f"Expected value 16.0, got {value}"
    assert jnp.isclose(grad, 8.0), f"Expected grad 8.0, got {grad}"
    print("✓ compute_value_and_grad test passed")


def test_loss_and_gradient():
    loss, grad = loss_and_gradient()
    expected_loss = 1.0  # mean([1, 1, 1]) = 1
    expected_grad = jnp.array([2/3, 2/3, 2/3])  # 2*(pred - target) / 3
    assert jnp.isclose(loss, expected_loss), f"Expected loss {expected_loss}, got {loss}"
    assert jnp.allclose(grad, expected_grad), f"Expected grad {expected_grad}, got {grad}"
    print("✓ loss_and_gradient test passed")


def test_multi_output_grad():
    result = multi_output_grad()
    if isinstance(result, tuple):
        value, grad = result
    else:
        value_and_grad_f = jax.value_and_grad(lambda x: x**2 + 2*x)
        value, grad = value_and_grad_f(3.0)

    assert jnp.isclose(value, 15.0), f"Expected value 15.0, got {value}"
    assert jnp.isclose(grad, 8.0), f"Expected grad 8.0, got {grad}"
    print("✓ multi_output_grad test passed")


def test_gradient_with_aux():
    value, aux, grad = gradient_with_aux()
    assert jnp.isclose(value, 25.0), f"Expected value 25.0, got {value}"
    assert jnp.isclose(grad, 10.0), f"Expected grad 10.0, got {grad}"
    assert "squared" in aux, "Auxiliary data should contain 'squared'"
    assert "doubled" in aux, "Auxiliary data should contain 'doubled'"
    print("✓ gradient_with_aux test passed")


if __name__ == "__main__":
    test_compute_value_and_grad()
    test_loss_and_gradient()
    test_multi_output_grad()
    test_gradient_with_aux()
    print("\n🎉 All tests passed!")
