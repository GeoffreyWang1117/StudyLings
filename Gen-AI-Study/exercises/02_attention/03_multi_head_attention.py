"""
练习 11: 多头注意力 (Multi-Head Attention)

多头注意力让模型能够同时关注来自不同表示子空间的信息。
每个"头"独立计算注意力，最后拼接并投影。

公式：
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W_o
其中 head_i = Attention(Q @ W_q^i, K @ W_k^i, V @ W_v^i)

在这个练习中，你将学习：
- 多头注意力的动机
- 如何分割和合并头
- 高效的多头实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MultiHeadAttention(nn.Module):
    """
    多头注意力实现
    """

    def __init__(self, d_model, num_heads):
        """
        Args:
            d_model: 模型维度
            num_heads: 注意力头的数量
        """
        super().__init__()

        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"

        self.d_model = d_model
        self.num_heads = num_heads
        # TODO: 计算每个头的维度
        self.d_k = d_model // ___  # 填入正确的除数

        # Q, K, V 投影（处理所有头）
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)

        # 输出投影
        self.W_o = nn.Linear(d_model, d_model)

    def split_heads(self, x):
        """
        将最后一个维度分割成多个头

        Args:
            x: 形状 (batch_size, seq_len, d_model)

        Returns:
            形状 (batch_size, num_heads, seq_len, d_k)
        """
        batch_size, seq_len, _ = x.shape

        # TODO: 重塑张量
        # (batch, seq, d_model) -> (batch, seq, num_heads, d_k)
        x = x.view(batch_size, seq_len, self.___, self.___)

        # TODO: 转置得到 (batch, num_heads, seq, d_k)
        x = x.___  # 使用 transpose(1, 2) 或 permute

        return x

    def combine_heads(self, x):
        """
        将多个头合并回去

        Args:
            x: 形状 (batch_size, num_heads, seq_len, d_k)

        Returns:
            形状 (batch_size, seq_len, d_model)
        """
        batch_size, _, seq_len, _ = x.shape

        # TODO: 转置回 (batch, seq, num_heads, d_k)
        x = x.transpose(1, 2)

        # TODO: 合并最后两个维度
        # (batch, seq, num_heads, d_k) -> (batch, seq, d_model)
        x = x.___(batch_size, seq_len, self.___)  # 使用 contiguous().view() 或 reshape()

        return x

    def forward(self, query, key, value, mask=None):
        """
        多头注意力前向传播

        Args:
            query: (batch_size, seq_len_q, d_model)
            key: (batch_size, seq_len_k, d_model)
            value: (batch_size, seq_len_k, d_model)
            mask: 可选掩码

        Returns:
            output: (batch_size, seq_len_q, d_model)
            attention_weights: (batch_size, num_heads, seq_len_q, seq_len_k)
        """
        batch_size = query.size(0)

        # 步骤 1: 线性投影
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)

        # 步骤 2: 分割成多个头
        Q = self.split_heads(Q)  # (batch, num_heads, seq_q, d_k)
        K = self.split_heads(K)  # (batch, num_heads, seq_k, d_k)
        V = self.split_heads(V)  # (batch, num_heads, seq_k, d_k)

        # 步骤 3: 缩放点积注意力
        # TODO: 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.___)

        if mask is not None:
            # 扩展 mask 以匹配头的维度
            if mask.dim() == 3:
                mask = mask.unsqueeze(1)  # (batch, 1, seq_q, seq_k)
            scores = scores.masked_fill(mask, float('-inf'))

        # TODO: 计算注意力权重
        attention_weights = F.___(scores, dim=-1)

        # TODO: 加权求和
        attention_output = torch.___(attention_weights, V)

        # 步骤 4: 合并头
        attention_output = self.combine_heads(attention_output)

        # 步骤 5: 输出投影
        output = self.W_o(attention_output)

        return output, attention_weights


def understand_multi_head():
    """
    理解多头注意力的优势

    单头注意力只能学习一种注意力模式
    多头注意力可以同时学习多种模式：
    - 头 1 可能关注语法结构
    - 头 2 可能关注语义相似
    - 头 3 可能关注位置关系
    等等
    """
    d_model = 64
    num_heads = 8
    d_k = d_model // num_heads  # 每个头 8 维

    # TODO: 验证维度分割
    assert d_k == ___, f"每个头应该是 {d_model // num_heads} 维"

    # 创建多头注意力
    mha = MultiHeadAttention(d_model, num_heads)

    # 测试输入
    x = torch.randn(2, 10, d_model)
    output, weights = mha(x, x, x)

    # TODO: 验证权重形状
    # weights 应该是 (batch, num_heads, seq, seq)
    expected_shape = (2, ___, 10, 10)  # 填入 num_heads

    return weights.shape == expected_shape


def efficient_multi_head():
    """
    理解高效多头实现的技巧

    技巧：将所有头的 Q, K, V 投影合并成一个大矩阵乘法
    然后通过 reshape 和 transpose 分割成多个头

    这比为每个头分别计算要高效得多
    """
    d_model = 512
    num_heads = 8
    d_k = d_model // num_heads
    batch_size = 32
    seq_len = 100

    # 方法 1: 分别为每个头计算（低效）
    # 需要 8 次矩阵乘法

    # 方法 2: 合并计算（高效）
    # 只需要 1 次大矩阵乘法，然后 reshape

    # TODO: 理解这行代码为什么高效
    W_qkv = nn.Linear(d_model, 3 * d_model)  # Q, K, V 合并
    x = torch.randn(batch_size, seq_len, d_model)

    # 一次计算得到所有 Q, K, V
    qkv = W_qkv(x)  # (batch, seq, 3 * d_model)

    # TODO: 分割成 Q, K, V
    Q, K, V = qkv.chunk(___, dim=-1)  # 填入分块数

    return Q.shape == K.shape == V.shape == (batch_size, seq_len, d_model)


def main():
    print("测试 MultiHeadAttention...")
    mha = MultiHeadAttention(d_model=64, num_heads=8)
    x = torch.randn(2, 10, 64)
    output, weights = mha(x, x, x)  # 自注意力
    assert output.shape == (2, 10, 64), f"期望形状 (2, 10, 64)，得到 {output.shape}"
    assert weights.shape == (2, 8, 10, 10), f"期望权重形状 (2, 8, 10, 10)，得到 {weights.shape}"
    print("✓ MultiHeadAttention 通过!")

    print("\n测试 split_heads 和 combine_heads...")
    x = torch.randn(2, 10, 64)
    split = mha.split_heads(x)
    assert split.shape == (2, 8, 10, 8), f"分割后形状应为 (2, 8, 10, 8)，得到 {split.shape}"
    combined = mha.combine_heads(split)
    assert combined.shape == (2, 10, 64), f"合并后形状应为 (2, 10, 64)，得到 {combined.shape}"
    print("✓ split_heads 和 combine_heads 通过!")

    print("\n测试交叉注意力...")
    query = torch.randn(2, 10, 64)
    key = torch.randn(2, 20, 64)  # seq_len 不同
    value = torch.randn(2, 20, 64)
    output, weights = mha(query, key, value)
    assert output.shape == (2, 10, 64)
    assert weights.shape == (2, 8, 10, 20)
    print("✓ 交叉注意力通过!")

    print("\n测试 understand_multi_head...")
    result = understand_multi_head()
    assert result
    print("✓ understand_multi_head 通过!")

    print("\n测试 efficient_multi_head...")
    result = efficient_multi_head()
    assert result
    print("✓ efficient_multi_head 通过!")

    print("\n🎉 所有测试通过！多头注意力掌握完成！")


if __name__ == "__main__":
    main()
