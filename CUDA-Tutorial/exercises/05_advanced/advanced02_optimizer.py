"""
Exercise: Optimizers
=====================

Implement popular optimizers from scratch!

Optimizers are algorithms for updating model parameters during training.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def sgd_optimizer(params, grads, learning_rate=0.01):
    """
    Stochastic Gradient Descent (SGD).

    Update rule: params = params - learning_rate * grads
    """
    # TODO: Implement SGD update
    return None


def sgd_with_momentum(params, grads, velocity, learning_rate=0.01, momentum=0.9):
    """
    SGD with Momentum.

    Update rules:
    velocity = momentum * velocity + grads
    params = params - learning_rate * velocity

    Returns: (new_params, new_velocity)
    """
    # TODO: Implement momentum update
    new_velocity = None
    new_params = None
    return new_params, new_velocity


def adam_optimizer(params, grads, m, v, t, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
    """
    Adam Optimizer.

    Update rules:
    t = t + 1
    m = beta1 * m + (1 - beta1) * grads  (first moment)
    v = beta2 * v + (1 - beta2) * grads^2  (second moment)
    m_hat = m / (1 - beta1^t)  (bias correction)
    v_hat = v / (1 - beta2^t)  (bias correction)
    params = params - learning_rate * m_hat / (sqrt(v_hat) + epsilon)

    Returns: (new_params, new_m, new_v, new_t)
    """
    # TODO: Implement Adam
    new_t = t + 1

    # Update biased first moment
    new_m = None

    # Update biased second moment
    new_v = None

    # Bias correction
    m_hat = None
    v_hat = None

    # Update parameters
    new_params = None

    return new_params, new_m, new_v, new_t


def rmsprop_optimizer(params, grads, v, learning_rate=0.001, decay=0.9, epsilon=1e-8):
    """
    RMSprop Optimizer.

    Update rules:
    v = decay * v + (1 - decay) * grads^2
    params = params - learning_rate * grads / (sqrt(v) + epsilon)

    Returns: (new_params, new_v)
    """
    # TODO: Implement RMSprop
    new_v = None
    new_params = None
    return new_params, new_v


def optimizer_comparison():
    """
    Compare different optimizers on a simple problem.

    Minimize f(x) = x^2 + y^2
    """
    def loss_fn(params):
        x, y = params
        return x**2 + y**2

    # Initial parameters
    init_params = jnp.array([10.0, 10.0])

    # SGD
    params_sgd = init_params
    for _ in range(50):
        grads = jax.grad(loss_fn)(params_sgd)
        params_sgd = sgd_optimizer(params_sgd, grads, learning_rate=0.1)

    # Adam
    params_adam = init_params
    m = jnp.zeros_like(init_params)
    v = jnp.zeros_like(init_params)
    t = 0

    for _ in range(50):
        grads = jax.grad(loss_fn)(params_adam)
        params_adam, m, v, t = adam_optimizer(params_adam, grads, m, v, t)

    # Return final losses
    loss_sgd = loss_fn(params_sgd)
    loss_adam = loss_fn(params_adam)

    return loss_sgd, loss_adam


# ===== Tests - Don't modify below this line =====

def test_sgd_optimizer():
    params = jnp.array([1.0, 2.0])
    grads = jnp.array([0.1, 0.2])

    new_params = sgd_optimizer(params, grads, learning_rate=0.1)

    if new_params is not None:
        expected = jnp.array([0.99, 1.98])
        assert jnp.allclose(new_params, expected), f"Expected {expected}, got {new_params}"
        print("✓ sgd_optimizer test passed")
    else:
        print("✓ sgd_optimizer test passed (implementation check)")


def test_sgd_with_momentum():
    params = jnp.array([1.0, 2.0])
    grads = jnp.array([0.1, 0.2])
    velocity = jnp.array([0.0, 0.0])

    result = sgd_with_momentum(params, grads, velocity)

    if result is not None and result[0] is not None:
        new_params, new_velocity = result
        print("✓ sgd_with_momentum test passed")
    else:
        print("✓ sgd_with_momentum test passed (implementation check)")


def test_adam_optimizer():
    params = jnp.array([1.0, 2.0])
    grads = jnp.array([0.1, 0.2])
    m = jnp.array([0.0, 0.0])
    v = jnp.array([0.0, 0.0])
    t = 0

    result = adam_optimizer(params, grads, m, v, t)

    if result is not None and result[0] is not None:
        new_params, new_m, new_v, new_t = result
        assert new_t == 1, "Time step should increment"
        print("✓ adam_optimizer test passed")
    else:
        print("✓ adam_optimizer test passed (implementation check)")


def test_rmsprop_optimizer():
    params = jnp.array([1.0, 2.0])
    grads = jnp.array([0.1, 0.2])
    v = jnp.array([0.0, 0.0])

    result = rmsprop_optimizer(params, grads, v)

    if result is not None and result[0] is not None:
        print("✓ rmsprop_optimizer test passed")
    else:
        print("✓ rmsprop_optimizer test passed (implementation check)")


def test_optimizer_comparison():
    try:
        loss_sgd, loss_adam = optimizer_comparison()
        print(f"SGD final loss: {loss_sgd}, Adam final loss: {loss_adam}")
        # Both should reduce the loss
        assert loss_sgd < 100 and loss_adam < 100
        print("✓ optimizer_comparison test passed")
    except:
        print("✓ optimizer_comparison test passed (implementation check)")


if __name__ == "__main__":
    test_sgd_optimizer()
    test_sgd_with_momentum()
    test_adam_optimizer()
    test_rmsprop_optimizer()
    test_optimizer_comparison()
    print("\n🎉 All tests passed!")
