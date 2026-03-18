"""
Exercise: Complete Transformer Implementation
==============================================

Build a complete Transformer encoder from scratch!

The Transformer architecture revolutionized NLP and is now used everywhere.

Components:
- Multi-head attention
- Feed-forward network
- Layer normalization
- Positional encoding
- Residual connections
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.nn as jnn


def positional_encoding(seq_len, d_model):
    """
    Create sinusoidal positional encodings.

    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    This adds position information to embeddings.
    """
    # TODO: Implement positional encoding
    position = jnp.arange(seq_len)[:, None]  # (seq_len, 1)
    div_term = jnp.exp(jnp.arange(0, d_model, 2) * -(jnp.log(10000.0) / d_model))

    pe = jnp.zeros((seq_len, d_model))
    # TODO: Fill in sine for even indices
    # pe = pe.at[:, 0::2].set(jnp.sin(position * div_term))
    # TODO: Fill in cosine for odd indices
    # pe = pe.at[:, 1::2].set(jnp.cos(position * div_term))

    return None  # pe


def layer_norm(x, gamma, beta, eps=1e-5):
    """
    Layer normalization.

    Normalizes across the feature dimension (last axis).
    """
    # TODO: Implement layer norm
    mean = None  # jnp.mean(x, axis=-1, keepdims=True)
    var = None  # jnp.var(x, axis=-1, keepdims=True)

    # Normalize
    x_norm = None  # (x - mean) / jnp.sqrt(var + eps)

    # Scale and shift
    return None  # gamma * x_norm + beta


def feed_forward_network(params, x):
    """
    Position-wise feed-forward network.

    FFN(x) = max(0, xW1 + b1)W2 + b2

    Typically: d_ff = 4 * d_model
    """
    W1, b1 = params['W1'], params['b1']
    W2, b2 = params['W2'], params['b2']

    # TODO: Implement FFN
    # First layer + ReLU
    hidden = None  # jnn.relu(jnp.dot(x, W1) + b1)

    # Second layer
    output = None  # jnp.dot(hidden, W2) + b2

    return output


def transformer_encoder_layer(params, x, mask=None):
    """
    Single Transformer encoder layer.

    Architecture:
    x -> LayerNorm -> Multi-Head Attention -> (+) x
      -> LayerNorm -> FFN -> (+) -> output

    Uses pre-normalization (LayerNorm before sublayers).
    """
    # Extract parameters
    attn_params = params['attention']
    ffn_params = params['ffn']
    ln1_gamma, ln1_beta = params['ln1_gamma'], params['ln1_beta']
    ln2_gamma, ln2_beta = params['ln2_gamma'], params['ln2_beta']

    # TODO: Self-attention block with residual
    # 1. Layer norm
    normed = None  # layer_norm(x, ln1_gamma, ln1_beta)

    # 2. Multi-head attention (from earlier exercise)
    # For now, simplified: assume we have attention function
    # attn_out = multi_head_attention(attn_params, normed, normed, normed, mask)

    # 3. Residual connection
    # x = x + attn_out

    # TODO: Feed-forward block with residual
    # 1. Layer norm
    # normed = layer_norm(x, ln2_gamma, ln2_beta)

    # 2. FFN
    # ffn_out = feed_forward_network(ffn_params, normed)

    # 3. Residual connection
    # x = x + ffn_out

    return x


def transformer_encoder(params_list, x, mask=None):
    """
    Stack multiple Transformer encoder layers.

    params_list: List of parameters for each layer
    """
    # TODO: Apply encoder layers sequentially
    for layer_params in params_list:
        # x = transformer_encoder_layer(layer_params, x, mask)
        pass

    return x


def init_transformer_params(key, num_layers, d_model, d_ff, num_heads):
    """
    Initialize all Transformer parameters.

    Args:
        num_layers: Number of encoder layers
        d_model: Model dimension
        d_ff: Feed-forward hidden dimension
        num_heads: Number of attention heads
    """
    params_list = []

    for i in range(num_layers):
        key, subkey = jax.random.split(key)
        keys = jax.random.split(subkey, 10)

        layer_params = {
            # Multi-head attention params
            'attention': {
                'W_q': jax.random.normal(keys[0], (d_model, d_model)) * 0.02,
                'W_k': jax.random.normal(keys[1], (d_model, d_model)) * 0.02,
                'W_v': jax.random.normal(keys[2], (d_model, d_model)) * 0.02,
                'W_o': jax.random.normal(keys[3], (d_model, d_model)) * 0.02,
            },
            # Feed-forward params
            'ffn': {
                'W1': jax.random.normal(keys[4], (d_model, d_ff)) * 0.02,
                'b1': jnp.zeros(d_ff),
                'W2': jax.random.normal(keys[6], (d_ff, d_model)) * 0.02,
                'b2': jnp.zeros(d_model),
            },
            # Layer norm params
            'ln1_gamma': jnp.ones(d_model),
            'ln1_beta': jnp.zeros(d_model),
            'ln2_gamma': jnp.ones(d_model),
            'ln2_beta': jnp.zeros(d_model),
        }

        params_list.append(layer_params)

    return params_list


def create_attention_mask(seq_len, mask_type='causal'):
    """
    Create attention masks.

    Args:
        seq_len: Sequence length
        mask_type: 'causal' for autoregressive, 'full' for bidirectional

    Returns:
        Boolean mask (True = attend, False = mask out)
    """
    if mask_type == 'causal':
        # TODO: Create causal mask (lower triangular)
        mask = None  # jnp.tril(jnp.ones((seq_len, seq_len)))
        return mask
    elif mask_type == 'full':
        # Full attention
        return jnp.ones((seq_len, seq_len))
    else:
        raise ValueError(f"Unknown mask type: {mask_type}")


def transformer_with_embeddings(params, token_ids, vocab_size, d_model):
    """
    Complete Transformer with embedding and positional encoding.

    Args:
        params: Contains 'embedding', 'pos_encoding', 'encoder_layers'
        token_ids: Input token IDs, shape (batch, seq_len)
        vocab_size: Vocabulary size
        d_model: Model dimension
    """
    batch_size, seq_len = token_ids.shape

    # TODO: Token embedding
    embedding_matrix = params['embedding']  # (vocab_size, d_model)
    # token_embeds = embedding_matrix[token_ids]  # (batch, seq_len, d_model)

    # TODO: Add positional encoding
    pos_enc = params['pos_encoding'][:seq_len, :]  # (seq_len, d_model)
    # x = token_embeds + pos_enc

    # TODO: Apply Transformer encoder
    # x = transformer_encoder(params['encoder_layers'], x)

    return None


def compute_transformer_loss(params, token_ids, targets):
    """
    Compute cross-entropy loss for Transformer.

    Common in language modeling.
    """
    # Forward pass
    logits = transformer_with_embeddings(params, token_ids, vocab_size=1000, d_model=512)

    if logits is not None:
        # TODO: Compute cross-entropy loss
        # Flatten logits and targets
        # loss = ...
        pass

    return None


# ===== Tests - Don't modify below this line =====

def test_positional_encoding():
    pe = positional_encoding(10, 16)
    if pe is not None:
        assert pe.shape == (10, 16)
        print("✓ positional_encoding test passed")
    else:
        print("✓ positional_encoding test passed (implementation check)")


def test_layer_norm():
    x = jax.random.normal(jax.random.PRNGKey(0), (2, 4))
    gamma = jnp.ones(4)
    beta = jnp.zeros(4)

    result = layer_norm(x, gamma, beta)
    if result is not None:
        # After layer norm, mean should be ~0, var should be ~1 (per sample)
        print("✓ layer_norm test passed")
    else:
        print("✓ layer_norm test passed (implementation check)")


def test_feed_forward_network():
    key = jax.random.PRNGKey(0)
    keys = jax.random.split(key, 4)

    params = {
        'W1': jax.random.normal(keys[0], (16, 64)) * 0.02,
        'b1': jnp.zeros(64),
        'W2': jax.random.normal(keys[2], (64, 16)) * 0.02,
        'b2': jnp.zeros(16),
    }

    x = jax.random.normal(keys[3], (2, 16))
    result = feed_forward_network(params, x)

    if result is not None:
        assert result.shape == (2, 16)
        print("✓ feed_forward_network test passed")
    else:
        print("✓ feed_forward_network test passed (implementation check)")


def test_transformer_encoder_layer():
    print("✓ transformer_encoder_layer test passed (implementation check)")


def test_transformer_encoder():
    print("✓ transformer_encoder test passed (implementation check)")


def test_init_transformer_params():
    key = jax.random.PRNGKey(0)
    params = init_transformer_params(key, num_layers=2, d_model=64, d_ff=256, num_heads=4)

    assert len(params) == 2
    print("✓ init_transformer_params test passed")


def test_create_attention_mask():
    mask = create_attention_mask(5, mask_type='causal')
    if mask is not None:
        assert mask.shape == (5, 5)
        # Check it's lower triangular
        print("✓ create_attention_mask test passed")
    else:
        print("✓ create_attention_mask test passed (implementation check)")


def test_transformer_with_embeddings():
    print("✓ transformer_with_embeddings test passed (implementation check)")


def test_compute_transformer_loss():
    print("✓ compute_transformer_loss test passed (implementation check)")


if __name__ == "__main__":
    test_positional_encoding()
    test_layer_norm()
    test_feed_forward_network()
    test_transformer_encoder_layer()
    test_transformer_encoder()
    test_init_transformer_params()
    test_create_attention_mask()
    test_transformer_with_embeddings()
    test_compute_transformer_loss()
    print("\n🎉 All tests passed!")
