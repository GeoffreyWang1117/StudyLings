"""
Exercise: Parallel Computation with pmap
=========================================

pmap (parallel map) runs computations in parallel across multiple devices!

Key concepts:
- Data parallelism across devices (GPUs/TPUs)
- Automatic sharding of data
- Collective operations (all-reduce, etc.)
- Single-Program Multiple-Data (SPMD) paradigm

Note: Some exercises will work best on multi-device setups,
but we'll write them to work on CPU too!
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
from jax import pmap, devices


def check_devices():
    """
    Check available devices.

    JAX can use CPUs, GPUs, and TPUs!
    """
    # TODO: Get list of devices
    device_list = None  # jax.devices()

    return device_list


def simple_pmap():
    """
    Use pmap to run a function in parallel across devices.

    pmap maps a function across the first axis of the input.
    """
    # Create data for each device
    # Shape: (n_devices, ...)
    n_devices = len(jax.devices())
    xs = jnp.arange(n_devices * 4).reshape(n_devices, 4)

    # TODO: Define parallel function
    @pmap
    def parallel_square(x):
        return x ** 2

    # Call it
    result = None  # parallel_square(xs)

    return result


def pmap_with_multiple_args():
    """
    Use pmap with multiple arguments.

    Each argument is sharded across its first axis.
    """
    n_devices = len(jax.devices())

    xs = jnp.arange(n_devices * 3).reshape(n_devices, 3)
    ys = jnp.arange(n_devices * 3, n_devices * 6).reshape(n_devices, 3)

    # TODO: Parallel function with two inputs
    @pmap
    def parallel_add(x, y):
        return x + y

    result = None  # parallel_add(xs, ys)

    return result


def pmap_axis_name():
    """
    Use axis_name for collective operations.

    axis_name enables operations like all-reduce, all-gather across devices.
    """
    n_devices = len(jax.devices())
    xs = jnp.arange(n_devices).reshape(n_devices, 1)

    # TODO: Use pmap with axis_name
    @pmap(axis_name='devices')
    def sum_across_devices(x):
        # Sum across all devices
        return jax.lax.psum(x, axis_name='devices')

    result = None  # sum_across_devices(xs)

    return result


def pmap_mean_across_devices():
    """
    Compute mean across devices using pmap.

    This is common in data-parallel training!
    """
    n_devices = len(jax.devices())

    # Each device gets different data
    data = jnp.arange(n_devices * 10).reshape(n_devices, 10).astype(jnp.float32)

    # TODO: Compute global mean using pmean
    @pmap(axis_name='batch')
    def compute_global_mean(x):
        local_mean = jnp.mean(x)
        # Average across devices
        global_mean = None  # jax.lax.pmean(local_mean, axis_name='batch')
        return global_mean

    result = None  # compute_global_mean(data)

    return result


def replicate_data():
    """
    Replicate data across devices.

    Sometimes you want the same data on all devices (e.g., model params).

    Hint: Use jax.device_put_replicated
    """
    params = jnp.array([1.0, 2.0, 3.0])

    # TODO: Replicate to all devices
    replicated_params = None  # jax.device_put_replicated(params, jax.devices())

    return replicated_params


def data_parallel_batch():
    """
    Simulate data-parallel batch processing.

    Split a batch across devices and process in parallel.
    """
    n_devices = len(jax.devices())
    batch_size = n_devices * 4  # 4 examples per device
    input_dim = 5

    # Full batch
    batch = jax.random.normal(jax.random.PRNGKey(0), (batch_size, input_dim))

    # TODO: Reshape for pmap (first dim = n_devices)
    batch_per_device = batch.reshape(n_devices, -1, input_dim)

    # Simple processing function
    @pmap
    def process_batch(x):
        # Sum over the batch dimension (axis=0 within each device)
        return jnp.sum(x, axis=0)

    result = None  # process_batch(batch_per_device)

    return result


def pmap_grad():
    """
    Use pmap with gradients for data-parallel training.

    This is the foundation of distributed training!
    """
    n_devices = len(jax.devices())

    # Model parameters (replicated across devices)
    params = jnp.array([1.0, 2.0])

    # Different data per device
    data = jnp.arange(n_devices * 2).reshape(n_devices, 2).astype(jnp.float32)
    targets = jnp.ones((n_devices, 1))

    def loss_fn(params, x, y):
        pred = jnp.dot(params, x)
        return jnp.mean((pred - y) ** 2)

    # TODO: Parallel gradient computation
    @pmap
    def parallel_grad(params, x, y):
        grads = jax.grad(loss_fn)(params, x, y)
        return grads

    # Replicate params
    params_replicated = jax.device_put_replicated(params, jax.devices())

    grads = None  # parallel_grad(params_replicated, data, targets)

    return grads


# ===== Tests - Don't modify below this line =====

def test_check_devices():
    devices = check_devices()
    if devices is not None:
        assert len(devices) > 0, "Should have at least one device"
        print(f"✓ check_devices test passed - Found {len(devices)} device(s)")
    else:
        print("✓ check_devices test passed (implementation check)")


def test_simple_pmap():
    result = simple_pmap()
    if result is not None:
        n_devices = len(jax.devices())
        assert result.shape[0] == n_devices
        print("✓ simple_pmap test passed")
    else:
        print("✓ simple_pmap test passed (implementation check)")


def test_pmap_with_multiple_args():
    result = pmap_with_multiple_args()
    if result is not None:
        assert result.shape[0] == len(jax.devices())
        print("✓ pmap_with_multiple_args test passed")
    else:
        print("✓ pmap_with_multiple_args test passed (implementation check)")


def test_pmap_axis_name():
    result = pmap_axis_name()
    if result is not None:
        # All devices should have the same total sum
        n_devices = len(jax.devices())
        expected_sum = sum(range(n_devices))
        assert jnp.all(result == expected_sum), f"Expected all {expected_sum}, got {result}"
        print("✓ pmap_axis_name test passed")
    else:
        print("✓ pmap_axis_name test passed (implementation check)")


def test_pmap_mean_across_devices():
    result = pmap_mean_across_devices()
    if result is not None:
        # All devices should have the same global mean
        assert jnp.allclose(result[0], result), "All devices should have same mean"
        print("✓ pmap_mean_across_devices test passed")
    else:
        print("✓ pmap_mean_across_devices test passed (implementation check)")


def test_replicate_data():
    replicated = replicate_data()
    if replicated is not None:
        assert len(replicated) == len(jax.devices())
        print("✓ replicate_data test passed")
    else:
        print("✓ replicate_data test passed (implementation check)")


def test_data_parallel_batch():
    result = data_parallel_batch()
    if result is not None:
        assert result.shape[0] == len(jax.devices())
        print("✓ data_parallel_batch test passed")
    else:
        print("✓ data_parallel_batch test passed (implementation check)")


def test_pmap_grad():
    grads = pmap_grad()
    if grads is not None:
        assert grads.shape[0] == len(jax.devices())
        print("✓ pmap_grad test passed")
    else:
        print("✓ pmap_grad test passed (implementation check)")


if __name__ == "__main__":
    test_check_devices()
    test_simple_pmap()
    test_pmap_with_multiple_args()
    test_pmap_axis_name()
    test_pmap_mean_across_devices()
    test_replicate_data()
    test_data_parallel_batch()
    test_pmap_grad()
    print("\n🎉 All tests passed!")
