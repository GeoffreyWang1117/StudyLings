"""
练习 19: KV 缓存 (Key-Value Cache)

KV 缓存是加速自回归生成的关键技术。
在生成过程中，之前 token 的 K 和 V 不需要重新计算，可以缓存复用。

不使用 KV 缓存：每次生成新 token 都要重新计算所有位置的 K 和 V
使用 KV 缓存：只需计算新 token 的 K 和 V，然后与缓存拼接

计算量对比（生成 n 个 token）：
- 无缓存: O(n^2) - 每步都计算整个序列
- 有缓存: O(n) - 每步只计算一个 token

在这个练习中，你将学习：
- KV 缓存的原理
- 如何实现 KV 缓存
- 缓存对内存和速度的影响
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import time


class CausalSelfAttentionWithKVCache(nn.Module):
    """
    带 KV 缓存的因果自注意力

    在推理时：
    1. 第一次调用：计算完整序列的 K、V，缓存它们
    2. 后续调用：只计算新 token 的 K、V，与缓存拼接
    """

    def __init__(self, d_model, num_heads, max_seq_len):
        super().__init__()

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, kv_cache=None, use_cache=False):
        """
        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)
               在使用缓存时，seq_len 可能只有 1（新 token）
            kv_cache: 之前的 K、V 缓存，元组 (cached_k, cached_v)
                      每个形状 (batch_size, num_heads, cached_len, d_k)
            use_cache: 是否返回更新后的缓存

        Returns:
            output: 注意力输出
            new_kv_cache: 更新后的 KV 缓存（如果 use_cache=True）
        """
        batch_size, seq_len, _ = x.shape

        # 计算 Q, K, V
        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # TODO: 如果有 KV 缓存，拼接之前的 K 和 V
        if kv_cache is not None:
            cached_k, cached_v = kv_cache
            # 在序列维度上拼接
            K = torch.cat([cached_k, K], dim=___)  # 填入正确的维度
            V = torch.cat([___, V], dim=2)  # 填入 cached_v

        # 保存新的缓存
        new_kv_cache = (K, V) if use_cache else None

        # 缩放点积注意力
        # 注意：Q 的长度可能只有 1，但 K、V 的长度是累积的
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # 因果掩码：只需要掩盖 Q 能看到的位置
        total_len = K.size(2)
        query_len = Q.size(2)

        # TODO: 创建适当大小的因果掩码
        # 如果是增量生成（query_len=1），新 token 可以看到所有之前的 token
        if query_len == 1:
            # 单个新 token 可以看到所有之前的位置，不需要掩码
            mask = None
        else:
            # 完整序列，使用标准因果掩码
            mask = torch.triu(
                torch.ones(query_len, total_len, device=x.device),
                diagonal=total_len - query_len + ___  # 填入正确的偏移
            ).bool()

        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)

        # 合并头
        output = output.transpose(1, 2).contiguous().view(batch_size, query_len, self.d_model)
        output = self.W_o(output)

        return output, new_kv_cache


class SimpleTransformerWithKVCache(nn.Module):
    """带 KV 缓存的简单 Transformer"""

    def __init__(self, vocab_size, d_model, num_heads, num_layers, max_seq_len):
        super().__init__()

        self.d_model = d_model
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Embedding(max_seq_len, d_model)

        self.layers = nn.ModuleList([
            CausalSelfAttentionWithKVCache(d_model, num_heads, max_seq_len)
            for _ in range(num_layers)
        ])

        self.ln = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, input_ids, past_kv_caches=None, use_cache=False):
        """
        Args:
            input_ids: (batch_size, seq_len)
            past_kv_caches: 列表，每层的 KV 缓存
            use_cache: 是否返回新缓存

        Returns:
            logits: (batch_size, seq_len, vocab_size)
            new_kv_caches: 更新后的缓存列表
        """
        batch_size, seq_len = input_ids.shape

        # 计算位置索引
        if past_kv_caches is not None and past_kv_caches[0] is not None:
            # 增量生成：位置从缓存长度开始
            past_length = past_kv_caches[0][0].size(2)
            positions = torch.arange(past_length, past_length + seq_len, device=input_ids.device)
        else:
            positions = torch.arange(seq_len, device=input_ids.device)

        # 嵌入
        x = self.embedding(input_ids) + self.pos_embedding(positions)

        # 初始化缓存列表
        if past_kv_caches is None:
            past_kv_caches = [None] * self.num_layers

        new_kv_caches = []

        # TODO: 通过每一层
        for i, layer in enumerate(self.layers):
            x, new_cache = layer(x, past_kv_caches[___], use_cache)  # 填入层索引
            new_kv_caches.append(new_cache)

        x = self.ln(x)
        logits = self.head(x)

        return logits, new_kv_caches if use_cache else None


def generate_without_cache(model, input_ids, max_new_tokens):
    """不使用 KV 缓存的生成（慢）"""
    for _ in range(max_new_tokens):
        logits, _ = model(input_ids)
        next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
        input_ids = torch.cat([input_ids, next_token], dim=1)
    return input_ids


def generate_with_cache(model, input_ids, max_new_tokens):
    """使用 KV 缓存的生成（快）"""
    # 第一次调用：处理完整的 prompt
    logits, kv_caches = model(input_ids, use_cache=True)
    next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)

    generated = [next_token]

    # TODO: 后续只处理新 token
    for _ in range(max_new_tokens - 1):
        # 只输入新 token
        logits, kv_caches = model(___, kv_caches, use_cache=True)  # 填入新 token
        next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
        generated.append(next_token)

    # 拼接所有生成的 token
    return torch.cat([input_ids] + generated, dim=1)


def benchmark_kv_cache():
    """对比有无 KV 缓存的速度"""
    vocab_size = 1000
    d_model = 128
    num_heads = 4
    num_layers = 4
    max_seq_len = 512

    model = SimpleTransformerWithKVCache(
        vocab_size, d_model, num_heads, num_layers, max_seq_len
    )
    model.eval()

    prompt = torch.randint(0, vocab_size, (1, 10))
    max_new_tokens = 50

    # 预热
    with torch.no_grad():
        _ = generate_without_cache(model, prompt.clone(), 5)
        _ = generate_with_cache(model, prompt.clone(), 5)

    # 测试无缓存
    with torch.no_grad():
        start = time.time()
        result1 = generate_without_cache(model, prompt.clone(), max_new_tokens)
        time_no_cache = time.time() - start

    # 测试有缓存
    with torch.no_grad():
        start = time.time()
        result2 = generate_with_cache(model, prompt.clone(), max_new_tokens)
        time_with_cache = time.time() - start

    return time_no_cache, time_with_cache


def main():
    print("测试 CausalSelfAttentionWithKVCache...")
    attn = CausalSelfAttentionWithKVCache(d_model=64, num_heads=4, max_seq_len=128)

    # 完整序列
    x_full = torch.randn(2, 10, 64)
    output, kv_cache = attn(x_full, use_cache=True)
    assert output.shape == (2, 10, 64)
    assert kv_cache[0].shape == (2, 4, 10, 16)  # K 缓存
    print("✓ 完整序列通过!")

    # 增量生成（使用缓存）
    x_new = torch.randn(2, 1, 64)  # 只有一个新 token
    output_new, new_cache = attn(x_new, kv_cache, use_cache=True)
    assert output_new.shape == (2, 1, 64)
    assert new_cache[0].shape == (2, 4, 11, 16)  # 缓存增加了 1
    print("✓ 增量生成通过!")

    print("\n测试 SimpleTransformerWithKVCache...")
    model = SimpleTransformerWithKVCache(
        vocab_size=100, d_model=64, num_heads=4, num_layers=2, max_seq_len=128
    )

    # 完整前向
    input_ids = torch.randint(0, 100, (2, 10))
    logits, caches = model(input_ids, use_cache=True)
    assert logits.shape == (2, 10, 100)
    print("✓ 模型前向通过!")

    # 增量前向
    new_ids = torch.randint(0, 100, (2, 1))
    logits_new, new_caches = model(new_ids, caches, use_cache=True)
    assert logits_new.shape == (2, 1, 100)
    print("✓ 增量前向通过!")

    print("\n测试生成函数...")
    prompt = torch.randint(0, 100, (1, 5))
    result1 = generate_without_cache(model, prompt.clone(), 10)
    result2 = generate_with_cache(model, prompt.clone(), 10)
    assert result1.shape == result2.shape == (1, 15)
    print("✓ 生成函数通过!")

    print("\n速度对比（生成 50 个 token）...")
    time_no_cache, time_with_cache = benchmark_kv_cache()
    speedup = time_no_cache / time_with_cache
    print(f"  无 KV 缓存: {time_no_cache:.3f}s")
    print(f"  有 KV 缓存: {time_with_cache:.3f}s")
    print(f"  加速比: {speedup:.2f}x")

    print("\n🎉 所有测试通过！KV 缓存掌握完成！")


if __name__ == "__main__":
    main()
