"""
练习 23: 分组查询注意力 (Grouped Query Attention, GQA)

GQA 是 MHA (Multi-Head Attention) 和 MQA (Multi-Query Attention) 的折中方案。
它让多个查询头共享同一组键值头，在效率和性能间取得平衡。

注意力变体对比：
- MHA: n_q_heads 个 Q 头，n_kv_heads = n_q_heads 个 K/V 头（完全独立）
- MQA: n_q_heads 个 Q 头，n_kv_heads = 1 个 K/V 头（全部共享）
- GQA: n_q_heads 个 Q 头，n_kv_heads 个 K/V 头（分组共享，1 < n_kv_heads < n_q_heads）

GQA 的优势：
1. 减少 KV 缓存的内存占用（对长序列很重要）
2. 推理速度更快
3. 性能接近 MHA

LLaMA 2/3 使用 GQA，n_q_heads=32, n_kv_heads=8

在这个练习中，你将学习：
- GQA 的实现
- KV 头到 Q 头的映射
- 内存节省的计算
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class GroupedQueryAttention(nn.Module):
    """
    分组查询注意力

    n_kv_heads 个 K/V 头被 n_heads 个 Q 头共享
    每 (n_heads // n_kv_heads) 个 Q 头共享一个 K/V 头
    """

    def __init__(self, d_model, n_heads, n_kv_heads, max_seq_len=4096):
        """
        Args:
            d_model: 模型维度
            n_heads: Q 头的数量
            n_kv_heads: K/V 头的数量（必须能整除 n_heads）
            max_seq_len: 最大序列长度
        """
        super().__init__()

        assert n_heads % n_kv_heads == 0, "n_heads 必须能被 n_kv_heads 整除"

        self.d_model = d_model
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.head_dim = d_model // n_heads

        # TODO: 计算每个 KV 头对应多少个 Q 头
        self.n_rep = n_heads // ___  # 填入 n_kv_heads

        # Q 投影：d_model -> n_heads * head_dim
        self.wq = nn.Linear(d_model, n_heads * self.head_dim, bias=False)

        # TODO: K 投影：d_model -> n_kv_heads * head_dim
        self.wk = nn.Linear(d_model, ___ * self.head_dim, bias=False)  # 填入 n_kv_heads

        # TODO: V 投影：d_model -> n_kv_heads * head_dim
        self.wv = nn.Linear(d_model, ___ * self.head_dim, bias=False)  # 填入 n_kv_heads

        # 输出投影
        self.wo = nn.Linear(n_heads * self.head_dim, d_model, bias=False)

        # 因果掩码
        mask = torch.triu(torch.ones(max_seq_len, max_seq_len), diagonal=1).bool()
        self.register_buffer('causal_mask', mask)

    def repeat_kv(self, x):
        """
        将 K/V 头重复以匹配 Q 头的数量

        Args:
            x: 形状 (batch, n_kv_heads, seq_len, head_dim)

        Returns:
            形状 (batch, n_heads, seq_len, head_dim)
        """
        if self.n_rep == 1:
            return x

        batch, n_kv_heads, seq_len, head_dim = x.shape

        # TODO: 扩展并重复 KV 头
        # 方法: 先 unsqueeze，然后 expand，最后 reshape
        # (batch, n_kv, seq, head) -> (batch, n_kv, 1, seq, head)
        # -> (batch, n_kv, n_rep, seq, head) -> (batch, n_heads, seq, head)
        x = x.unsqueeze(2)  # (batch, n_kv, 1, seq, head)
        x = x.expand(batch, n_kv_heads, self.___, seq_len, head_dim)  # 填入 n_rep
        x = x.reshape(batch, self.n_heads, seq_len, head_dim)

        return x

    def forward(self, x, kv_cache=None, use_cache=False):
        """
        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)
            kv_cache: KV 缓存
            use_cache: 是否返回缓存

        Returns:
            output, new_kv_cache
        """
        batch_size, seq_len, _ = x.shape

        # 计算 Q, K, V
        q = self.wq(x)
        k = self.wk(x)
        v = self.wv(x)

        # 重塑为多头形式
        q = q.view(batch_size, seq_len, self.n_heads, self.head_dim).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(1, 2)

        # 处理 KV 缓存
        if kv_cache is not None:
            cached_k, cached_v = kv_cache
            k = torch.cat([cached_k, k], dim=2)
            v = torch.cat([cached_v, v], dim=2)

        new_kv_cache = (k, v) if use_cache else None

        # TODO: 重复 K 和 V 以匹配 Q 头的数量
        k = self.___(k)  # 调用 repeat_kv
        v = self.___(v)  # 调用 repeat_kv

        # 注意力计算
        total_len = k.size(2)
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)

        # 应用因果掩码
        if seq_len == 1:
            mask = None
        else:
            mask = self.causal_mask[:seq_len, :total_len]

        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, v)

        # 合并头并投影
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, -1)
        output = self.wo(output)

        return output, new_kv_cache


def compare_attention_types():
    """
    对比 MHA, MQA, GQA 的内存占用
    """
    d_model = 4096
    n_heads = 32
    head_dim = d_model // n_heads
    seq_len = 2048
    batch_size = 1

    # 计算 KV 缓存大小
    def kv_cache_size(n_kv_heads):
        # 每层: 2 (K+V) * batch * n_kv_heads * seq_len * head_dim * bytes_per_element
        return 2 * batch_size * n_kv_heads * seq_len * head_dim * 2  # fp16

    # TODO: 计算各种配置的 KV 缓存大小
    mha_size = kv_cache_size(n_heads)          # MHA: n_kv_heads = n_heads
    gqa_size = kv_cache_size(8)                # GQA: n_kv_heads = 8
    mqa_size = kv_cache_size(___)              # MQA: n_kv_heads = 1，填入 1

    return {
        'MHA': mha_size / 1024 / 1024,  # MB
        'GQA (8 heads)': gqa_size / 1024 / 1024,
        'MQA': mqa_size / 1024 / 1024
    }


def test_equivalence_with_mha():
    """
    当 n_kv_heads = n_heads 时，GQA 应该等价于 MHA
    """
    d_model = 64
    n_heads = 4

    # GQA with n_kv_heads = n_heads 就是 MHA
    gqa_as_mha = GroupedQueryAttention(d_model, n_heads, n_kv_heads=n_heads)

    x = torch.randn(2, 10, d_model)
    output, _ = gqa_as_mha(x)

    # 验证 repeat_kv 在这种情况下不改变任何东西
    k = torch.randn(2, 4, 10, 16)
    k_repeated = gqa_as_mha.repeat_kv(k)
    assert torch.equal(k, k_repeated), "当 n_rep=1 时，repeat_kv 不应改变输入"

    return True


def main():
    print("测试 GroupedQueryAttention...")
    d_model = 64
    n_heads = 8
    n_kv_heads = 2  # 每 4 个 Q 头共享一个 KV 头

    gqa = GroupedQueryAttention(d_model, n_heads, n_kv_heads)
    x = torch.randn(2, 16, d_model)

    output, _ = gqa(x)
    assert output.shape == (2, 16, d_model)
    print(f"✓ GQA 前向传播通过! (n_heads={n_heads}, n_kv_heads={n_kv_heads})")

    print("\n测试 repeat_kv...")
    k = torch.randn(2, 2, 16, 8)  # (batch, n_kv_heads=2, seq, head_dim)
    k_repeated = gqa.repeat_kv(k)
    assert k_repeated.shape == (2, 8, 16, 8)  # (batch, n_heads=8, seq, head_dim)
    # 验证每组 4 个头是相同的
    assert torch.equal(k_repeated[:, 0], k_repeated[:, 1])
    assert torch.equal(k_repeated[:, 0], k_repeated[:, 2])
    assert torch.equal(k_repeated[:, 0], k_repeated[:, 3])
    print("✓ repeat_kv 通过!")

    print("\n测试 KV 缓存...")
    x_prompt = torch.randn(2, 10, d_model)
    _, kv_cache = gqa(x_prompt, use_cache=True)

    x_new = torch.randn(2, 1, d_model)
    output_new, new_cache = gqa(x_new, kv_cache, use_cache=True)
    assert output_new.shape == (2, 1, d_model)
    assert new_cache[0].shape == (2, n_kv_heads, 11, 8)  # 序列长度增加 1
    print("✓ KV 缓存通过!")

    print("\n对比内存占用...")
    sizes = compare_attention_types()
    for name, size in sizes.items():
        print(f"  {name}: {size:.2f} MB (per layer)")

    saving_gqa = (1 - sizes['GQA (8 heads)'] / sizes['MHA']) * 100
    saving_mqa = (1 - sizes['MQA'] / sizes['MHA']) * 100
    print(f"\n  GQA 节省: {saving_gqa:.1f}%")
    print(f"  MQA 节省: {saving_mqa:.1f}%")

    print("\n测试与 MHA 的等价性...")
    result = test_equivalence_with_mha()
    assert result
    print("✓ 当 n_kv_heads = n_heads 时等价于 MHA!")

    print("\n参数对比...")
    mha_params = (
        d_model * d_model +  # wq
        d_model * d_model +  # wk
        d_model * d_model +  # wv
        d_model * d_model    # wo
    )

    gqa_params = (
        d_model * d_model +  # wq (full)
        d_model * (d_model * n_kv_heads // n_heads) +  # wk (reduced)
        d_model * (d_model * n_kv_heads // n_heads) +  # wv (reduced)
        d_model * d_model    # wo
    )

    print(f"  MHA 参数: {mha_params:,}")
    print(f"  GQA 参数: {gqa_params:,}")
    print(f"  参数节省: {(1 - gqa_params/mha_params)*100:.1f}%")

    print("\n🎉 所有测试通过！分组查询注意力掌握完成！")


if __name__ == "__main__":
    main()
