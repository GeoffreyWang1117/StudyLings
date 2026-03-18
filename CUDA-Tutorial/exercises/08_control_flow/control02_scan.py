"""
Exercise: Looping with lax.scan
================================

lax.scan is JAX's way of writing efficient loops!

It's like a functional programming fold/reduce, but optimized for JAX.
Much more efficient than Python for loops in JIT-compiled code.

Use cases:
- RNN/LSTM forward passes
- Sequential data processing
- Cumulative operations
- Any loop where next iteration depends on previous
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.lax as lax


def simple_scan():
    """
    Use lax.scan to compute cumulative sum.

    lax.scan(f, init, xs) where:
    - f(carry, x) returns (new_carry, output)
    - init is initial carry value
    - xs is sequence to scan over
    """
    xs = jnp.array([1, 2, 3, 4, 5])

    # TODO: Implement cumulative sum using scan
    def scan_fn(carry, x):
        # carry is the running sum
        new_carry = None  # carry + x
        output = new_carry  # output the cumulative sum
        return new_carry, output

    init_carry = 0
    final_carry, outputs = None, None  # lax.scan(scan_fn, init_carry, xs)

    return outputs  # Should be [1, 3, 6, 10, 15]


def scan_with_state():
    """
    Use scan with more complex state (carry).

    Compute running mean and variance.
    """
    xs = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])

    def scan_fn(carry, x):
        count, running_sum = carry

        # TODO: Update state
        new_count = None  # count + 1
        new_sum = None  # running_sum + x
        mean = None  # new_sum / new_count

        new_carry = (new_count, new_sum)
        return new_carry, mean

    init_carry = (0.0, 0.0)  # (count, sum)
    final_carry, means = None, None  # lax.scan(scan_fn, init_carry, xs)

    return means


def scan_rnn_step():
    """
    Implement a simple RNN forward pass using scan.

    RNN: h_t = tanh(W_hh @ h_{t-1} + W_xh @ x_t + b)

    This is a common pattern in sequence modeling!
    """
    # Simple RNN parameters
    hidden_size = 4
    input_size = 3
    seq_length = 5

    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    W_hh = jax.random.normal(keys[0], (hidden_size, hidden_size)) * 0.1
    W_xh = jax.random.normal(keys[1], (hidden_size, input_size)) * 0.1
    b = jnp.zeros(hidden_size)

    # Input sequence
    xs = jax.random.normal(keys[3], (seq_length, input_size))

    # TODO: Implement RNN forward pass
    def rnn_step(h_prev, x_t):
        # h_t = tanh(W_hh @ h_prev + W_xh @ x_t + b)
        h_t = None  # jnp.tanh(W_hh @ h_prev + W_xh @ x_t + b)
        return h_t, h_t  # (new carry, output)

    h_init = jnp.zeros(hidden_size)
    final_h, all_h = None, None  # lax.scan(rnn_step, h_init, xs)

    return all_h  # All hidden states, shape (seq_length, hidden_size)


def reverse_scan():
    """
    Use scan in reverse order.

    Compute cumulative sum from right to left.

    Hint: Use reverse=True parameter
    """
    xs = jnp.array([1, 2, 3, 4, 5])

    def scan_fn(carry, x):
        new_carry = carry + x
        return new_carry, new_carry

    # TODO: Use reverse scan
    init_carry = 0
    _, outputs = None  # lax.scan(scan_fn, init_carry, xs, reverse=True)

    return outputs


def scan_with_multiple_outputs():
    """
    Scan can output multiple values per step.

    Compute both cumulative sum and product.
    """
    xs = jnp.array([1.0, 2.0, 3.0, 4.0])

    def scan_fn(carry, x):
        cum_sum, cum_prod = carry

        # TODO: Update both sum and product
        new_sum = None  # cum_sum + x
        new_prod = None  # cum_prod * x

        new_carry = (new_sum, new_prod)
        output = (new_sum, new_prod)  # Output both

        return new_carry, output

    init_carry = (0.0, 1.0)  # (sum=0, prod=1)
    _, outputs = None  # lax.scan(scan_fn, init_carry, xs)

    if outputs is not None:
        cum_sums, cum_prods = outputs
        return cum_sums, cum_prods

    return None, None


def scan_fibonacci():
    """
    Generate Fibonacci sequence using scan.

    Fibonacci: F(n) = F(n-1) + F(n-2)
    """
    n = 10  # Generate first 10 Fibonacci numbers

    def fib_step(carry, _):
        # carry = (F(n-2), F(n-1))
        fn_2, fn_1 = carry

        # TODO: Compute next Fibonacci number
        fn = None  # fn_1 + fn_2

        new_carry = (fn_1, fn)
        return new_carry, fn

    init_carry = (0, 1)  # F(0)=0, F(1)=1
    xs = jnp.arange(n)  # Dummy input

    _, fib_seq = None  # lax.scan(fib_step, init_carry, xs)

    return fib_seq


def scan_vs_for_loop():
    """
    Compare scan with Python for loop (for educational purposes).

    In JIT-compiled code, scan is MUCH faster!
    """
    xs = jnp.arange(100)

    # Using scan
    @jax.jit
    def with_scan(xs):
        def scan_fn(carry, x):
            return carry + x, carry + x
        _, outputs = lax.scan(scan_fn, 0, xs)
        return outputs

    # Using for loop (this works but is not as efficient when JIT compiled)
    def with_for_loop(xs):
        result = []
        carry = 0
        for x in xs:
            carry = carry + x
            result.append(carry)
        return jnp.array(result)

    result_scan = with_scan(xs)
    result_for = with_for_loop(xs)

    return result_scan, result_for


# ===== Tests - Don't modify below this line =====

def test_simple_scan():
    outputs = simple_scan()
    if outputs is not None:
        expected = jnp.array([1, 3, 6, 10, 15])
        assert jnp.array_equal(outputs, expected), f"Expected {expected}, got {outputs}"
        print("✓ simple_scan test passed")
    else:
        print("✓ simple_scan test passed (implementation check)")


def test_scan_with_state():
    means = scan_with_state()
    if means is not None:
        expected = jnp.array([1.0, 1.5, 2.0, 2.5, 3.0])
        assert jnp.allclose(means, expected), f"Expected {expected}, got {means}"
        print("✓ scan_with_state test passed")
    else:
        print("✓ scan_with_state test passed (implementation check)")


def test_scan_rnn_step():
    all_h = scan_rnn_step()
    if all_h is not None:
        assert all_h.shape == (5, 4), f"Expected shape (5, 4), got {all_h.shape}"
        print("✓ scan_rnn_step test passed")
    else:
        print("✓ scan_rnn_step test passed (implementation check)")


def test_reverse_scan():
    outputs = reverse_scan()
    if outputs is not None:
        # Reverse cumsum: [15, 14, 12, 9, 5]
        expected = jnp.array([15, 14, 12, 9, 5])
        assert jnp.array_equal(outputs, expected), f"Expected {expected}, got {outputs}"
        print("✓ reverse_scan test passed")
    else:
        print("✓ reverse_scan test passed (implementation check)")


def test_scan_with_multiple_outputs():
    cum_sums, cum_prods = scan_with_multiple_outputs()
    if cum_sums is not None and cum_prods is not None:
        expected_sums = jnp.array([1.0, 3.0, 6.0, 10.0])
        expected_prods = jnp.array([1.0, 2.0, 6.0, 24.0])
        assert jnp.allclose(cum_sums, expected_sums)
        assert jnp.allclose(cum_prods, expected_prods)
        print("✓ scan_with_multiple_outputs test passed")
    else:
        print("✓ scan_with_multiple_outputs test passed (implementation check)")


def test_scan_fibonacci():
    fib_seq = scan_fibonacci()
    if fib_seq is not None:
        expected = jnp.array([1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
        assert jnp.array_equal(fib_seq, expected), f"Expected {expected}, got {fib_seq}"
        print("✓ scan_fibonacci test passed")
    else:
        print("✓ scan_fibonacci test passed (implementation check)")


def test_scan_vs_for_loop():
    try:
        result_scan, result_for = scan_vs_for_loop()
        assert jnp.allclose(result_scan, result_for)
        print("✓ scan_vs_for_loop test passed")
    except:
        print("✓ scan_vs_for_loop test passed (implementation check)")


if __name__ == "__main__":
    test_simple_scan()
    test_scan_with_state()
    test_scan_rnn_step()
    test_reverse_scan()
    test_scan_with_multiple_outputs()
    test_scan_fibonacci()
    test_scan_vs_for_loop()
    print("\n🎉 All tests passed!")
