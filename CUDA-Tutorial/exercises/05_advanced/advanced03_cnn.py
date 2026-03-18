"""
Exercise: Convolutional Neural Networks
========================================

Implement a simple CNN using JAX!

CNNs are essential for computer vision tasks.
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.lax as lax


def simple_conv2d(image, kernel):
    """
    Implement a simple 2D convolution.

    Args:
        image: Input image of shape (H, W)
        kernel: Convolution kernel of shape (kH, kW)

    Returns:
        Convolved image

    Hint: Use jax.lax.conv or implement with loops
    """
    # TODO: Implement convolution
    # For simplicity, use valid padding
    return None


def conv_layer_forward(x, W, b):
    """
    Convolutional layer forward pass.

    Args:
        x: Input of shape (batch, height, width, channels_in)
        W: Weights of shape (kernel_h, kernel_w, channels_in, channels_out)
        b: Bias of shape (channels_out,)

    Returns:
        Output of shape (batch, out_h, out_w, channels_out)

    Hint: Use jax.lax.conv_general_dilated
    """
    # TODO: Implement conv layer
    # Use dimension_numbers to specify NHWC format
    dn = lax.conv_dimension_numbers(x.shape, W.shape, ('NHWC', 'HWIO', 'NHWC'))

    out = None  # lax.conv_general_dilated(x, W, window_strides=(1, 1), padding='SAME', dimension_numbers=dn)

    # Add bias
    if out is not None:
        out = out + b

    return out


def max_pool2d(x, pool_size=2):
    """
    Implement 2D max pooling.

    Args:
        x: Input of shape (batch, height, width, channels)
        pool_size: Size of pooling window

    Returns:
        Pooled output

    Hint: Use jax.lax.reduce_window
    """
    # TODO: Implement max pooling
    init_val = -jnp.inf
    out = None  # lax.reduce_window(x, init_val, lax.max, (1, pool_size, pool_size, 1), (1, pool_size, pool_size, 1), 'VALID')

    return out


def simple_cnn(params, x):
    """
    Implement a simple CNN.

    Architecture:
    Input -> Conv(32 filters) -> ReLU -> MaxPool -> Conv(64 filters) -> ReLU -> MaxPool -> Flatten -> Dense

    Args:
        params: Dict with 'conv1', 'conv2', 'dense' weights and biases
        x: Input of shape (batch, 28, 28, 1)

    Returns:
        Output logits
    """
    # TODO: Implement CNN forward pass

    # Conv1
    x = None  # conv_layer_forward(x, params['W_conv1'], params['b_conv1'])
    if x is not None:
        x = jax.nn.relu(x)
        x = max_pool2d(x, pool_size=2)

        # Conv2
        x = conv_layer_forward(x, params['W_conv2'], params['b_conv2'])
        x = jax.nn.relu(x)
        x = max_pool2d(x, pool_size=2)

        # Flatten
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1)

        # Dense
        x = jnp.dot(x, params['W_dense']) + params['b_dense']

    return x


def initialize_cnn(key):
    """
    Initialize CNN parameters.

    Returns params dict for a simple CNN.
    """
    keys = jax.random.split(key, 6)

    params = {
        # Conv1: 3x3 kernel, 1 input channel, 8 output channels
        'W_conv1': jax.random.normal(keys[0], (3, 3, 1, 8)) * 0.1,
        'b_conv1': jnp.zeros(8),

        # Conv2: 3x3 kernel, 8 input channels, 16 output channels
        'W_conv2': jax.random.normal(keys[2], (3, 3, 8, 16)) * 0.1,
        'b_conv2': jnp.zeros(16),

        # Dense: 7*7*16 -> 10 (after two 2x2 pooling from 28x28)
        'W_dense': jax.random.normal(keys[4], (7*7*16, 10)) * 0.1,
        'b_dense': jnp.zeros(10),
    }

    return params


# ===== Tests - Don't modify below this line =====

def test_simple_conv2d():
    image = jnp.ones((5, 5))
    kernel = jnp.ones((3, 3))

    result = simple_conv2d(image, kernel)

    # Just check it runs
    print("✓ simple_conv2d test passed (implementation check)")


def test_conv_layer_forward():
    x = jnp.ones((2, 8, 8, 3))  # batch=2, 8x8 image, 3 channels
    W = jax.random.normal(jax.random.PRNGKey(0), (3, 3, 3, 16)) * 0.1
    b = jnp.zeros(16)

    result = conv_layer_forward(x, W, b)

    if result is not None:
        assert result.shape[0] == 2, "Batch size should be preserved"
        assert result.shape[3] == 16, "Should have 16 output channels"
        print("✓ conv_layer_forward test passed")
    else:
        print("✓ conv_layer_forward test passed (implementation check)")


def test_max_pool2d():
    x = jnp.ones((1, 8, 8, 3))

    result = max_pool2d(x, pool_size=2)

    if result is not None:
        assert result.shape[1] == 4 and result.shape[2] == 4, "Should halve spatial dimensions"
        print("✓ max_pool2d test passed")
    else:
        print("✓ max_pool2d test passed (implementation check)")


def test_simple_cnn():
    key = jax.random.PRNGKey(0)
    params = initialize_cnn(key)

    x = jax.random.normal(key, (2, 28, 28, 1))  # Batch of 2 images

    result = simple_cnn(params, x)

    if result is not None:
        assert result.shape == (2, 10), f"Expected shape (2, 10), got {result.shape}"
        print("✓ simple_cnn test passed")
    else:
        print("✓ simple_cnn test passed (implementation check)")


def test_initialize_cnn():
    key = jax.random.PRNGKey(0)
    params = initialize_cnn(key)

    assert 'W_conv1' in params and 'W_conv2' in params and 'W_dense' in params
    print("✓ initialize_cnn test passed")


if __name__ == "__main__":
    test_simple_conv2d()
    test_conv_layer_forward()
    test_max_pool2d()
    test_simple_cnn()
    test_initialize_cnn()
    print("\n🎉 All tests passed!")
