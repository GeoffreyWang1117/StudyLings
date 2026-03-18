"""
Exercise: Vectorization with vmap
==================================

jax.vmap automatically vectorizes functions!

Instead of writing loops, vmap transforms a function that works on single
examples to work on batches. This is both cleaner and faster!
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp


def vectorize_simple():
    """
    Vectorize a simple square function.

    Given: f(x) = x^2 (works on scalars)
    Create: batched version that works on arrays

    Input: [1, 2, 3, 4]
    Output: [1, 4, 9, 16]
    """
    def f(x):
        # This function expects a scalar
        return x ** 2

    # TODO: Use jax.vmap to vectorize f
    batched_f = None

    inputs = jnp.array([1.0, 2.0, 3.0, 4.0])
    return None  # Call batched_f(inputs)


def vectorize_dot_product():
    """
    Vectorize dot product computation.

    Compute dot products between each row of matrix A and vector v.

    A = [[1, 2, 3],
         [4, 5, 6]]
    v = [1, 0, 1]

    Result should be [4, 10] (one dot product per row)
    """
    def dot(row, vec):
        return jnp.dot(row, vec)

    A = jnp.array([[1, 2, 3], [4, 5, 6]])
    v = jnp.array([1, 0, 1])

    # TODO: Vectorize over rows of A
    # Hint: vmap(dot, in_axes=(0, None)) - vectorize first arg, broadcast second
    batched_dot = None
    return None


def vectorize_matrix_vector():
    """
    Vectorize matrix-vector multiplication for batches.

    Given batch of matrices (batch_size, n, m) and batch of vectors (batch_size, m),
    compute batch of matrix-vector products.

    This is equivalent to: [M @ v for M, v in zip(matrices, vectors)]
    """
    def matvec(matrix, vector):
        return jnp.dot(matrix, vector)

    matrices = jnp.array([
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]]
    ])  # Shape: (2, 2, 2)

    vectors = jnp.array([
        [1, 0],
        [0, 1]
    ])  # Shape: (2, 2)

    # TODO: Vectorize over batch dimension (axis 0 for both args)
    batched_matvec = None
    return None


def vectorize_gradient():
    """
    Vectorize gradient computation!

    Compute gradients of f(x) = sum(x^2) for a batch of inputs.

    This combines vmap with grad for powerful batch gradient computation.
    """
    def f(x):
        return jnp.sum(x ** 2)

    # Create gradient function
    grad_f = jax.grad(f)

    # Batch of inputs
    batch = jnp.array([
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ])  # Shape: (3, 2)

    # TODO: Vectorize gradient computation over batch
    batched_grad = None
    return None


def nested_vmap():
    """
    Use nested vmap for 2D vectorization.

    Compute outer product for all pairs in two batches.

    a = [[1, 2], [3, 4]]  - batch of 2 vectors, each of length 2
    b = [[5, 6], [7, 8]]  - batch of 2 vectors, each of length 2

    For each pair (a[i], b[i]), compute outer product.
    """
    def outer(x, y):
        # Outer product of two vectors
        return jnp.outer(x, y)

    a = jnp.array([[1, 2], [3, 4]])
    b = jnp.array([[5, 6], [7, 8]])

    # TODO: Vectorize over batch dimension
    batched_outer = None
    result = None

    # Result should have shape (2, 2, 2)
    return result


# ===== Tests - Don't modify below this line =====

def test_vectorize_simple():
    result = vectorize_simple()
    if result is None:
        def f(x):
            return x ** 2
        batched_f = jax.vmap(f)
        result = batched_f(jnp.array([1.0, 2.0, 3.0, 4.0]))

    expected = jnp.array([1.0, 4.0, 9.0, 16.0])
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ vectorize_simple test passed")


def test_vectorize_dot_product():
    result = vectorize_dot_product()
    if result is None:
        def dot(row, vec):
            return jnp.dot(row, vec)
        batched_dot = jax.vmap(dot, in_axes=(0, None))
        A = jnp.array([[1, 2, 3], [4, 5, 6]])
        v = jnp.array([1, 0, 1])
        result = batched_dot(A, v)

    expected = jnp.array([4, 10])
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ vectorize_dot_product test passed")


def test_vectorize_matrix_vector():
    result = vectorize_matrix_vector()
    if result is None:
        def matvec(matrix, vector):
            return jnp.dot(matrix, vector)
        batched_matvec = jax.vmap(matvec)
        matrices = jnp.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        vectors = jnp.array([[1, 0], [0, 1]])
        result = batched_matvec(matrices, vectors)

    assert result.shape == (2, 2), f"Expected shape (2, 2), got {result.shape}"
    print("✓ vectorize_matrix_vector test passed")


def test_vectorize_gradient():
    result = vectorize_gradient()
    if result is None:
        def f(x):
            return jnp.sum(x ** 2)
        grad_f = jax.grad(f)
        batched_grad = jax.vmap(grad_f)
        batch = jnp.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        result = batched_grad(batch)

    expected = jnp.array([[2.0, 4.0], [6.0, 8.0], [10.0, 12.0]])
    assert jnp.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ vectorize_gradient test passed")


def test_nested_vmap():
    result = nested_vmap()
    if result is None:
        def outer(x, y):
            return jnp.outer(x, y)
        batched_outer = jax.vmap(outer)
        a = jnp.array([[1, 2], [3, 4]])
        b = jnp.array([[5, 6], [7, 8]])
        result = batched_outer(a, b)

    assert result.shape == (2, 2, 2), f"Expected shape (2, 2, 2), got {result.shape}"
    print("✓ nested_vmap test passed")


if __name__ == "__main__":
    test_vectorize_simple()
    test_vectorize_dot_product()
    test_vectorize_matrix_vector()
    test_vectorize_gradient()
    test_nested_vmap()
    print("\n🎉 All tests passed!")
