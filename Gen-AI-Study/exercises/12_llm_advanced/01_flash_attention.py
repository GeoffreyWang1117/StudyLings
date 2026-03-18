"""
练习 54: Flash Attention (概念版)

Flash Attention 是一种 IO 感知的精确注意力算法，
通过分块计算和在线 softmax 显著减少显存占用。

核心思想：
1. 分块 (Tiling): 将 Q, K, V 分成小块
2. 在线 Softmax: 边计算边更新 softmax
3. 重计算 (Recomputation): 反向传播时重新计算中间结果

复杂度改进：
- 标准注意力显存: O(N^2)
- Flash Attention 显存: O(N)

注意：这是教学版本，展示核心思想。
实际使用请用 flash_attn 库或 PyTorch 2.0+ 的 SDPA。

在这个练习中，你将学习：
- 分块注意力的实现
- 在线 Softmax 算法
- IO 优化的重要性
"""

import torch
import torch.nn.functional as F
import math


def standard_attention(Q, K, V, mask=None):
    """
    标准注意力实现

    需要存储完整的 N×N 注意力矩阵
    """
    d_k = Q.shape[-1]

    # TODO: 计算注意力分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.___(d_k)  # 使用 sqrt

    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))

    attn = F.softmax(scores, dim=-1)
    output = torch.matmul(attn, V)

    return output


def online_softmax(x, block_size=64):
    """
    在线 Softmax 算法

    传统 softmax: softmax(x)_i = exp(x_i) / Σ exp(x_j)
    需要两次遍历: 1) 计算 max 和 sum  2) 归一化

    在线版本: 单次遍历，边读边更新
    """
    N = x.shape[-1]
    num_blocks = (N + block_size - 1) // block_size

    # 初始化
    m = torch.full(x.shape[:-1] + (1,), float('-inf'), device=x.device)  # 当前最大值
    l = torch.zeros(x.shape[:-1] + (1,), device=x.device)  # 当前 exp 和
    result = torch.zeros_like(x)

    for i in range(num_blocks):
        start = i * block_size
        end = min(start + block_size, N)
        x_block = x[..., start:end]

        # 当前块的最大值
        m_block = x_block.max(dim=-1, keepdim=True).values

        # TODO: 更新全局最大值
        m_new = torch.maximum(m, m_block)  # 使用 maximum

        # 修正之前的 exp 和
        # l_new = l * exp(m - m_new) + exp(x_block - m_new).sum()
        l_new = l * torch.exp(m - m_new) + torch.exp(x_block - ___).sum(dim=-1, keepdim=True)  # 填入 m_new

        # 更新结果（修正之前块的缩放）
        scale = torch.exp(m - m_new)
        result = result * scale

        # 添加当前块的贡献
        result[..., start:end] = torch.exp(x_block - m_new)

        # 更新状态
        m = m_new
        l = l_new

    # 最终归一化
    result = result / l

    return result


def tiled_attention(Q, K, V, block_size_q=64, block_size_kv=64):
    """
    分块注意力 (Flash Attention 简化版)

    将 Q, K, V 分成小块，逐块计算
    避免存储完整的 N×N 注意力矩阵
    """
    batch_size, num_heads, seq_len, head_dim = Q.shape
    scale = 1.0 / math.sqrt(head_dim)

    # 输出和中间状态
    O = torch.zeros_like(Q)
    L = torch.zeros(batch_size, num_heads, seq_len, 1, device=Q.device)  # log-sum-exp
    M = torch.full((batch_size, num_heads, seq_len, 1), float('-inf'), device=Q.device)  # max

    num_blocks_q = (seq_len + block_size_q - 1) // block_size_q
    num_blocks_kv = (seq_len + block_size_kv - 1) // block_size_kv

    for i in range(num_blocks_q):
        q_start = i * block_size_q
        q_end = min(q_start + block_size_q, seq_len)
        Q_block = Q[:, :, q_start:q_end, :]

        # 当前块的状态
        O_block = torch.zeros_like(Q_block)
        L_block = torch.zeros(batch_size, num_heads, q_end - q_start, 1, device=Q.device)
        M_block = torch.full((batch_size, num_heads, q_end - q_start, 1), float('-inf'), device=Q.device)

        for j in range(num_blocks_kv):
            kv_start = j * block_size_kv
            kv_end = min(kv_start + block_size_kv, seq_len)

            K_block = K[:, :, kv_start:kv_end, :]
            V_block = V[:, :, kv_start:kv_end, :]

            # TODO: 计算注意力分数
            S_block = torch.matmul(Q_block, K_block.transpose(-2, -1)) * ___  # 填入 scale

            # 在线 softmax 更新
            M_block_new = torch.maximum(M_block, S_block.max(dim=-1, keepdim=True).values)

            # 修正之前的结果
            exp_old = torch.exp(M_block - M_block_new)
            exp_new = torch.exp(S_block - M_block_new)

            L_block_new = L_block * exp_old + exp_new.sum(dim=-1, keepdim=True)
            O_block = O_block * exp_old + torch.matmul(exp_new, V_block)

            M_block = M_block_new
            L_block = L_block_new

        # TODO: 归一化输出
        O[:, :, q_start:q_end, :] = O_block / ___  # 填入 L_block

    return O


def memory_efficient_attention(Q, K, V, chunk_size=1024):
    """
    显存高效的注意力

    通过分块减少峰值显存使用
    """
    batch_size, num_heads, seq_len, head_dim = Q.shape
    scale = 1.0 / math.sqrt(head_dim)

    # 对 Q 分块
    num_chunks = (seq_len + chunk_size - 1) // chunk_size
    outputs = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, seq_len)

        Q_chunk = Q[:, :, start:end, :]

        # 计算这个 chunk 与所有 K 的注意力
        # TODO: 计算注意力分数
        scores = torch.matmul(Q_chunk, K.transpose(-2, -1)) * scale

        # Softmax 和加权
        attn = F.softmax(scores, dim=___)  # 填入 -1
        out_chunk = torch.matmul(attn, V)

        outputs.append(out_chunk)

    return torch.cat(outputs, dim=2)


def compare_implementations():
    """比较不同实现的结果"""
    torch.manual_seed(42)

    batch_size, num_heads, seq_len, head_dim = 2, 8, 256, 64
    Q = torch.randn(batch_size, num_heads, seq_len, head_dim)
    K = torch.randn(batch_size, num_heads, seq_len, head_dim)
    V = torch.randn(batch_size, num_heads, seq_len, head_dim)

    # 标准实现
    out_standard = standard_attention(Q, K, V)

    # 分块实现
    out_tiled = tiled_attention(Q, K, V, block_size_q=64, block_size_kv=64)

    # 显存高效实现
    out_memory = memory_efficient_attention(Q, K, V, chunk_size=64)

    print("实现比较:")
    print(f"  标准 vs 分块: 最大差异 = {(out_standard - out_tiled).abs().max():.6f}")
    print(f"  标准 vs 显存高效: 最大差异 = {(out_standard - out_memory).abs().max():.6f}")

    return out_standard, out_tiled, out_memory


def main():
    print("测试标准注意力...")
    Q = torch.randn(2, 8, 128, 64)
    K = torch.randn(2, 8, 128, 64)
    V = torch.randn(2, 8, 128, 64)

    out = standard_attention(Q, K, V)
    assert out.shape == Q.shape
    print(f"✓ 标准注意力输出: {out.shape}")

    print("\n测试在线 Softmax...")
    x = torch.randn(2, 8, 256)
    online_result = online_softmax(x, block_size=32)
    standard_result = F.softmax(x, dim=-1)
    diff = (online_result - standard_result).abs().max()
    print(f"✓ 与标准 Softmax 差异: {diff:.6f}")
    assert diff < 1e-5

    print("\n测试分块注意力...")
    out_tiled = tiled_attention(Q, K, V, block_size_q=32, block_size_kv=32)
    out_standard = standard_attention(Q, K, V)
    diff = (out_tiled - out_standard).abs().max()
    print(f"✓ 与标准注意力差异: {diff:.6f}")
    assert diff < 1e-4

    print("\n测试显存高效注意力...")
    out_memory = memory_efficient_attention(Q, K, V, chunk_size=32)
    diff = (out_memory - out_standard).abs().max()
    print(f"✓ 与标准注意力差异: {diff:.6f}")
    assert diff < 1e-5

    print("\n比较所有实现...")
    compare_implementations()

    print("\n显存分析 (概念性):")
    seq_len = 4096
    head_dim = 64
    print(f"  序列长度: {seq_len}, 头维度: {head_dim}")
    standard_mem = seq_len * seq_len * 4  # float32
    flash_mem = seq_len * head_dim * 4
    print(f"  标准注意力: ~{standard_mem / 1024 / 1024:.2f} MB (N²)")
    print(f"  Flash Attention: ~{flash_mem / 1024:.2f} KB (N)")
    print(f"  节省: {standard_mem / flash_mem:.0f}x")

    print("\n🎉 所有测试通过！Flash Attention 概念掌握完成！")


if __name__ == "__main__":
    main()
