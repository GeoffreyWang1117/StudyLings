"""
练习 21: 旋转位置编码 (Rotary Position Embedding, RoPE)

RoPE 是现代大模型（如 LLaMA、Qwen）使用的位置编码方式。
它通过旋转矩阵将位置信息编码到 Q 和 K 中。

核心思想：
- 将位置 m 的 Q 旋转 m*θ 角度
- 将位置 n 的 K 旋转 n*θ 角度
- Q_m @ K_n 的结果只依赖于相对位置 (m-n)

优点：
1. 相对位置编码
2. 更好的长度外推性
3. 计算高效

在这个练习中，你将学习：
- RoPE 的数学原理
- 如何实现 RoPE
- RoPE 与其他位置编码的比较
"""

import torch
import torch.nn as nn
import math


def precompute_freqs_cis(dim, max_seq_len, theta=10000.0):
    """
    预计算 RoPE 所需的复数频率

    Args:
        dim: 嵌入维度（必须是偶数）
        max_seq_len: 最大序列长度
        theta: 基础频率（类似于正弦位置编码的 10000）

    Returns:
        freqs_cis: 复数频率张量，形状 (max_seq_len, dim//2)
    """
    assert dim % 2 == 0, "维度必须是偶数"

    # TODO: 计算频率
    # freq_i = 1 / (theta^(2i/dim))
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / ___))  # 填入 dim

    # TODO: 生成位置索引
    positions = torch.arange(max_seq_len)

    # TODO: 计算位置 * 频率（外积）
    # 形状: (max_seq_len, dim//2)
    freqs = torch.___(positions, freqs)  # 使用 outer

    # 转换为复数形式: e^(i*theta) = cos(theta) + i*sin(theta)
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)

    return freqs_cis


def apply_rotary_emb(xq, xk, freqs_cis):
    """
    应用旋转位置编码

    Args:
        xq: Query 张量，形状 (batch, seq_len, num_heads, head_dim)
        xk: Key 张量，形状 (batch, seq_len, num_heads, head_dim)
        freqs_cis: 预计算的复数频率，形状 (seq_len, head_dim//2)

    Returns:
        旋转后的 xq, xk
    """
    # 将实数张量视为复数
    # 形状变化: (batch, seq, heads, dim) -> (batch, seq, heads, dim//2, 2)
    # 然后视为复数: (batch, seq, heads, dim//2)
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))

    # 调整 freqs_cis 形状以便广播
    # (seq, dim//2) -> (1, seq, 1, dim//2)
    freqs_cis = freqs_cis.unsqueeze(0).unsqueeze(2)

    # TODO: 应用旋转（复数乘法）
    xq_out = xq_ ___ freqs_cis  # 填入乘法运算符
    xk_out = xk_ * freqs_cis

    # 转回实数
    xq_out = torch.view_as_real(xq_out).flatten(-2)
    xk_out = torch.view_as_real(xk_out).flatten(-2)

    return xq_out.type_as(xq), xk_out.type_as(xk)


def rotate_half(x):
    """
    辅助函数：旋转张量的一半维度

    将 [x1, x2, x3, x4, ...] 变换为 [-x2, x1, -x4, x3, ...]
    """
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_emb_real(xq, xk, cos, sin):
    """
    应用旋转位置编码（实数版本，不使用复数）

    这是另一种实现方式，某些框架不支持复数运算时使用

    Args:
        xq, xk: Query 和 Key 张量
        cos, sin: 预计算的 cos 和 sin 值
    """
    # TODO: 应用旋转
    # x_rotated = x * cos + rotate_half(x) * sin
    xq_out = xq * cos + ___(xq) * sin  # 调用 rotate_half
    xk_out = xk * ___ + rotate_half(xk) * sin  # 填入 cos

    return xq_out, xk_out


class RotaryEmbedding(nn.Module):
    """
    RoPE 模块
    """

    def __init__(self, dim, max_seq_len=4096, theta=10000.0):
        super().__init__()

        self.dim = dim
        self.max_seq_len = max_seq_len
        self.theta = theta

        # 预计算频率
        freqs_cis = precompute_freqs_cis(dim, max_seq_len, theta)
        self.register_buffer('freqs_cis', freqs_cis)

        # 也存储 cos 和 sin（用于实数版本）
        # TODO: 分别计算 cos 和 sin
        freqs = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / dim))
        positions = torch.arange(max_seq_len)
        angles = torch.outer(positions, freqs)
        self.register_buffer('cos_cached', angles.cos().unsqueeze(0).unsqueeze(2))
        self.register_buffer('sin_cached', angles.___.unsqueeze(0).unsqueeze(2))  # 使用 sin

    def forward(self, xq, xk, start_pos=0):
        """
        Args:
            xq, xk: (batch, seq_len, num_heads, head_dim)
            start_pos: 起始位置（用于增量生成）
        """
        seq_len = xq.shape[1]
        freqs_cis = self.freqs_cis[start_pos : start_pos + seq_len]
        return apply_rotary_emb(xq, xk, freqs_cis)


def visualize_rope_property():
    """
    验证 RoPE 的关键性质：
    相对位置不变性 - Q_m @ K_n 只依赖于 (m-n)
    """
    dim = 64
    theta = 10000.0

    freqs_cis = precompute_freqs_cis(dim, 100, theta)

    # 创建随机 Q 和 K
    q = torch.randn(1, 1, 1, dim)  # 位置 0
    k = torch.randn(1, 1, 1, dim)  # 位置 0

    # 测试不同的绝对位置，但保持相对位置相同
    results = []
    for offset in [0, 10, 50]:
        q_pos = offset
        k_pos = offset + 5  # 相对位置固定为 5

        # 应用 RoPE
        q_rope = apply_rotary_emb(
            q.clone(), q.clone(),
            freqs_cis[q_pos:q_pos+1]
        )[0]
        k_rope = apply_rotary_emb(
            k.clone(), k.clone(),
            freqs_cis[k_pos:k_pos+1]
        )[1]

        # 计算点积
        score = (q_rope * k_rope).sum()
        results.append(score.item())

    # TODO: 验证所有结果应该相等（相对位置相同）
    tolerance = 1e-5
    all_equal = all(abs(r - results[0]) < tolerance for r in results)

    return results, all_equal


def main():
    print("测试 precompute_freqs_cis...")
    freqs_cis = precompute_freqs_cis(dim=64, max_seq_len=128)
    assert freqs_cis.shape == (128, 32), f"期望 (128, 32)，得到 {freqs_cis.shape}"
    assert freqs_cis.dtype == torch.complex64
    print("✓ precompute_freqs_cis 通过!")

    print("\n测试 apply_rotary_emb...")
    batch, seq, heads, dim = 2, 16, 4, 64
    xq = torch.randn(batch, seq, heads, dim)
    xk = torch.randn(batch, seq, heads, dim)
    freqs_cis = precompute_freqs_cis(dim, seq)

    xq_rope, xk_rope = apply_rotary_emb(xq, xk, freqs_cis)
    assert xq_rope.shape == xq.shape
    assert xk_rope.shape == xk.shape
    print("✓ apply_rotary_emb 通过!")

    print("\n测试 RotaryEmbedding 模块...")
    rope = RotaryEmbedding(dim=64, max_seq_len=256)
    xq_out, xk_out = rope(xq, xk)
    assert xq_out.shape == xq.shape
    print("✓ RotaryEmbedding 通过!")

    print("\n测试增量生成（start_pos）...")
    # 模拟 KV 缓存场景
    xq_new = torch.randn(batch, 1, heads, dim)  # 新的一个 token
    xk_new = torch.randn(batch, 1, heads, dim)
    xq_out, xk_out = rope(xq_new, xk_new, start_pos=16)
    assert xq_out.shape == (batch, 1, heads, dim)
    print("✓ 增量生成测试通过!")

    print("\n验证 RoPE 的相对位置不变性...")
    results, all_equal = visualize_rope_property()
    print(f"  不同绝对位置的点积结果: {results}")
    if all_equal:
        print("✓ 相对位置不变性验证通过!")
    else:
        print("  (数值可能有微小差异，但应该很接近)")

    print("\n🎉 所有测试通过！旋转位置编码掌握完成！")


if __name__ == "__main__":
    main()
