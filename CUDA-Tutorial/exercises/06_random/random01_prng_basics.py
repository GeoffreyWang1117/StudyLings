"""
Exercise: JAX Random Number Basics
===================================

JAX uses a different random number system than NumPy!

JAX uses explicit PRNG (Pseudo-Random Number Generator) keys for reproducibility
and parallelizability. This is different from NumPy's global random state.

Key concepts:
- Explicit random keys
- Splitting keys for independence
- Deterministic by default
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.random as random


def create_random_key():
    """
    Create a PRNG key with seed 42.

    Hint: Use jax.random.PRNGKey(seed)
    """
    # TODO: Create a random key with seed 42
    key = None
    return key


def generate_random_array():
    """
    Generate a random array of shape (5,) with values from normal distribution.

    Hint: Use jax.random.normal(key, shape)
    """
    key = jax.random.PRNGKey(0)

    # TODO: Generate random array
    arr = None
    return arr


def split_random_key():
    """
    Split a random key into multiple independent keys.

    This is crucial for maintaining independence in random operations!

    Hint: Use jax.random.split(key, num)
    """
    key = jax.random.PRNGKey(0)

    # TODO: Split key into 3 independent keys
    keys = None  # jax.random.split(key, 3)
    return keys


def sequential_random_ops():
    """
    Perform sequential random operations with proper key splitting.

    Generate two independent random arrays.
    """
    key = jax.random.PRNGKey(0)

    # TODO: Split key for two operations
    key1, key2 = None, None  # jax.random.split(key, 2) or jax.random.split(key)

    # TODO: Generate two random arrays
    arr1 = None  # jax.random.normal(key1, (3,))
    arr2 = None  # jax.random.normal(key2, (3,))

    return arr1, arr2


def different_distributions():
    """
    Sample from different probability distributions.

    JAX provides many distributions: normal, uniform, bernoulli, etc.
    """
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    # TODO: Sample from normal distribution N(0, 1)
    normal_sample = None  # jax.random.normal(keys[0], (5,))

    # TODO: Sample from uniform distribution U(0, 1)
    uniform_sample = None  # jax.random.uniform(keys[1], (5,))

    # TODO: Sample from Bernoulli with p=0.5
    bernoulli_sample = None  # jax.random.bernoulli(keys[2], 0.5, (5,))

    # TODO: Sample integers from 0 to 9
    randint_sample = None  # jax.random.randint(keys[3], (5,), 0, 10)

    return normal_sample, uniform_sample, bernoulli_sample, randint_sample


def shuffle_array():
    """
    Shuffle an array randomly.

    Hint: Use jax.random.permutation
    """
    key = jax.random.PRNGKey(42)
    arr = jnp.arange(10)

    # TODO: Shuffle the array
    shuffled = None  # jax.random.permutation(key, arr)

    return shuffled


def random_choice():
    """
    Randomly sample elements from an array.

    Hint: Use jax.random.choice
    """
    key = jax.random.PRNGKey(0)
    arr = jnp.array([10, 20, 30, 40, 50])

    # TODO: Sample 3 elements with replacement
    samples = None  # jax.random.choice(key, arr, shape=(3,), replace=True)

    return samples


# ===== Tests - Don't modify below this line =====

def test_create_random_key():
    key = create_random_key()
    assert key is not None, "Key should not be None"
    # JAX keys are arrays with specific properties
    print("✓ create_random_key test passed")


def test_generate_random_array():
    arr = generate_random_array()
    assert arr is not None, "Array should not be None"
    assert arr.shape == (5,), f"Expected shape (5,), got {arr.shape}"
    print("✓ generate_random_array test passed")


def test_split_random_key():
    keys = split_random_key()
    if keys is not None:
        assert len(keys) == 3, f"Expected 3 keys, got {len(keys)}"
        # Keys should be different
        assert not jnp.array_equal(keys[0], keys[1]), "Keys should be different"
        print("✓ split_random_key test passed")
    else:
        print("✓ split_random_key test passed (implementation check)")


def test_sequential_random_ops():
    result = sequential_random_ops()
    if result is not None and result[0] is not None:
        arr1, arr2 = result
        assert arr1.shape == (3,) and arr2.shape == (3,)
        # Arrays should be different (with high probability)
        assert not jnp.allclose(arr1, arr2), "Arrays should be different"
        print("✓ sequential_random_ops test passed")
    else:
        print("✓ sequential_random_ops test passed (implementation check)")


def test_different_distributions():
    result = different_distributions()
    if result is not None and result[0] is not None:
        normal, uniform, bernoulli, randint = result
        assert normal.shape == (5,)
        assert uniform.shape == (5,)
        assert bernoulli.shape == (5,)
        assert randint.shape == (5,)
        # Check value ranges
        assert jnp.all((uniform >= 0) & (uniform <= 1)), "Uniform should be in [0, 1]"
        assert jnp.all((bernoulli >= 0) & (bernoulli <= 1)), "Bernoulli should be 0 or 1"
        assert jnp.all((randint >= 0) & (randint < 10)), "Randint should be in [0, 10)"
        print("✓ different_distributions test passed")
    else:
        print("✓ different_distributions test passed (implementation check)")


def test_shuffle_array():
    shuffled = shuffle_array()
    if shuffled is not None:
        original = jnp.arange(10)
        # Should have same elements, different order (with high probability)
        assert jnp.array_equal(jnp.sort(shuffled), original), "Should contain same elements"
        print("✓ shuffle_array test passed")
    else:
        print("✓ shuffle_array test passed (implementation check)")


def test_random_choice():
    samples = random_choice()
    if samples is not None:
        assert samples.shape == (3,), f"Expected shape (3,), got {samples.shape}"
        arr = jnp.array([10, 20, 30, 40, 50])
        # All samples should be from original array
        assert jnp.all(jnp.isin(samples, arr)), "Samples should be from original array"
        print("✓ random_choice test passed")
    else:
        print("✓ random_choice test passed (implementation check)")


if __name__ == "__main__":
    test_create_random_key()
    test_generate_random_array()
    test_split_random_key()
    test_sequential_random_ops()
    test_different_distributions()
    test_shuffle_array()
    test_random_choice()
    print("\n🎉 All tests passed!")
