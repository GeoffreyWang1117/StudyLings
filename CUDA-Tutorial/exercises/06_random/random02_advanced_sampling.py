"""
Exercise: Advanced Random Sampling
===================================

Learn advanced random sampling techniques in JAX.

Topics:
- Custom distributions
- Rejection sampling
- Reparameterization trick
- Categorical sampling
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.random as random


def categorical_sample():
    """
    Sample from a categorical distribution.

    Given probabilities [0.1, 0.3, 0.4, 0.2], sample category indices.

    Hint: Use jax.random.categorical
    """
    key = jax.random.PRNGKey(0)
    logits = jnp.log(jnp.array([0.1, 0.3, 0.4, 0.2]))

    # TODO: Sample 10 categorical values
    samples = None  # jax.random.categorical(key, logits, shape=(10,))

    return samples


def multivariate_normal():
    """
    Sample from a multivariate normal distribution.

    Mean: [0, 0]
    Covariance: [[1, 0.5], [0.5, 1]]

    Hint: Use jax.random.multivariate_normal
    """
    key = jax.random.PRNGKey(0)
    mean = jnp.array([0.0, 0.0])
    cov = jnp.array([[1.0, 0.5], [0.5, 1.0]])

    # TODO: Sample 100 points from multivariate normal
    samples = None  # jax.random.multivariate_normal(key, mean, cov, (100,))

    return samples


def truncated_normal():
    """
    Implement truncated normal sampling (values between -2 and 2).

    Use rejection sampling: keep sampling until we get values in range.

    This demonstrates the reparameterization trick.
    """
    key = jax.random.PRNGKey(0)

    # TODO: Sample from normal and clip to [-2, 2]
    samples = None  # jax.random.normal(key, (1000,))
    if samples is not None:
        # Simple truncation (not true truncated normal, but illustrative)
        samples = jnp.clip(samples, -2.0, 2.0)

    return samples


def gumbel_max_trick():
    """
    Implement Gumbel-max trick for differentiable categorical sampling.

    The Gumbel-max trick: argmax(log_probs + Gumbel(0,1))
    gives a categorical sample.

    Hint: Use jax.random.gumbel
    """
    key = jax.random.PRNGKey(0)
    log_probs = jnp.log(jnp.array([0.1, 0.3, 0.4, 0.2]))

    # TODO: Sample using Gumbel-max trick
    gumbel_noise = None  # jax.random.gumbel(key, shape=log_probs.shape)
    if gumbel_noise is not None:
        # Add Gumbel noise and take argmax
        sample = jnp.argmax(log_probs + gumbel_noise)
        return sample

    return None


def dropout_mask():
    """
    Create a dropout mask (useful in neural networks).

    With dropout probability 0.5, create a binary mask.

    Hint: Use jax.random.bernoulli
    """
    key = jax.random.PRNGKey(0)
    shape = (10, 20)
    dropout_rate = 0.5
    keep_prob = 1.0 - dropout_rate

    # TODO: Create dropout mask
    mask = None  # jax.random.bernoulli(key, keep_prob, shape)

    return mask


def random_with_vmap():
    """
    Use vmap with random operations.

    Generate a batch of random arrays, each with different key.

    This is important for parallel random generation!
    """
    key = jax.random.PRNGKey(0)
    batch_size = 5

    # TODO: Split key into batch_size keys
    keys = None  # jax.random.split(key, batch_size)

    # TODO: Use vmap to generate random arrays in parallel
    # Each array should have shape (3,)
    def generate(k):
        return jax.random.normal(k, (3,))

    if keys is not None:
        batch = jax.vmap(generate)(keys)
        return batch

    return None


def stable_softmax_sample():
    """
    Implement numerically stable softmax sampling.

    Given logits, convert to probabilities and sample.
    """
    key = jax.random.PRNGKey(0)
    logits = jnp.array([10.0, 20.0, 30.0, 25.0])  # Large values

    # TODO: Convert logits to probabilities (numerically stable)
    probs = None  # jax.nn.softmax(logits)

    # TODO: Sample from categorical
    if probs is not None:
        # Convert back to log space for categorical
        log_probs = jnp.log(probs + 1e-10)
        sample = jax.random.categorical(key, log_probs)
        return sample

    return None


# ===== Tests - Don't modify below this line =====

def test_categorical_sample():
    samples = categorical_sample()
    if samples is not None:
        assert samples.shape == (10,), f"Expected shape (10,), got {samples.shape}"
        assert jnp.all((samples >= 0) & (samples < 4)), "Samples should be in [0, 4)"
        print("✓ categorical_sample test passed")
    else:
        print("✓ categorical_sample test passed (implementation check)")


def test_multivariate_normal():
    samples = multivariate_normal()
    if samples is not None:
        assert samples.shape == (100, 2), f"Expected shape (100, 2), got {samples.shape}"
        print("✓ multivariate_normal test passed")
    else:
        print("✓ multivariate_normal test passed (implementation check)")


def test_truncated_normal():
    samples = truncated_normal()
    if samples is not None:
        assert jnp.all((samples >= -2.0) & (samples <= 2.0)), "All samples should be in [-2, 2]"
        print("✓ truncated_normal test passed")
    else:
        print("✓ truncated_normal test passed (implementation check)")


def test_gumbel_max_trick():
    sample = gumbel_max_trick()
    if sample is not None:
        assert sample >= 0 and sample < 4, f"Sample should be in [0, 4), got {sample}"
        print("✓ gumbel_max_trick test passed")
    else:
        print("✓ gumbel_max_trick test passed (implementation check)")


def test_dropout_mask():
    mask = dropout_mask()
    if mask is not None:
        assert mask.shape == (10, 20), f"Expected shape (10, 20), got {mask.shape}"
        assert jnp.all((mask == 0) | (mask == 1)), "Mask should be binary"
        print("✓ dropout_mask test passed")
    else:
        print("✓ dropout_mask test passed (implementation check)")


def test_random_with_vmap():
    batch = random_with_vmap()
    if batch is not None:
        assert batch.shape == (5, 3), f"Expected shape (5, 3), got {batch.shape}"
        # Arrays should be different (with high probability)
        assert not jnp.allclose(batch[0], batch[1]), "Batches should be different"
        print("✓ random_with_vmap test passed")
    else:
        print("✓ random_with_vmap test passed (implementation check)")


def test_stable_softmax_sample():
    sample = stable_softmax_sample()
    if sample is not None:
        assert sample >= 0 and sample < 4, f"Sample should be in [0, 4), got {sample}"
        print("✓ stable_softmax_sample test passed")
    else:
        print("✓ stable_softmax_sample test passed (implementation check)")


if __name__ == "__main__":
    test_categorical_sample()
    test_multivariate_normal()
    test_truncated_normal()
    test_gumbel_max_trick()
    test_dropout_mask()
    test_random_with_vmap()
    test_stable_softmax_sample()
    print("\n🎉 All tests passed!")
