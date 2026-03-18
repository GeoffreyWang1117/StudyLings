"""
练习 10: 自注意力 (Self-Attention)

自注意力是 Transformer 的核心，让序列中的每个位置都能关注其他所有位置。
与普通注意力不同，自注意力的 Q、K、V 都来自同一个输入。

自注意力流程：
1. 输入 X 通过三个线性变换得到 Q, K, V
2. 计算注意力分数和权重
3. 加权求和得到输出

在这个练习中，你将学习：
- Q、K、V 投影矩阵的作用
- 自注意力的完整实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class SelfAttention(nn.Module):
    """
    单头自注意力实现
    """

    def __init__(self, d_model):
        """
        Args:
            d_model: 模型维度/嵌入维度
        """
        super().__init__()

        self.d_model = d_model

        # TODO: 定义 Q, K, V 的投影矩阵
        # 每个都是从 d_model 映射到 d_model
        self.W_q = nn.___(d_model, d_model)  # 使用 nn.Linear
        self.W_k = nn.___(d_model, d_model)  # 使用 nn.Linear
        self.W_v = nn.___(d_model, d_model)  # 使用 nn.Linear

    def forward(self, x, mask=None):
        """
        自注意力前向传播

        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)
            mask: 可选的注意力掩码

        Returns:
            output: 输出，形状 (batch_size, seq_len, d_model)
            attention_weights: 注意力权重
        """
        # TODO: 计算 Q, K, V
        # 都是对同一个输入 x 进行线性变换
        Q = self.___(x)  # Query
        K = self.___(x)  # Key
        V = self.___(x)  # Value

        # 计算注意力分数
        d_k = self.d_model
        # TODO: Q @ K^T / sqrt(d_k)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.___(d_k)

        # 应用掩码（如果有）
        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        # TODO: Softmax 得到注意力权重
        attention_weights = F.___(scores, dim=-1)

        # TODO: 加权求和
        output = torch.___(attention_weights, V)

        return output, attention_weights


class SelfAttentionWithProjection(nn.Module):
    """
    带输出投影的自注意力

    标准 Transformer 在注意力输出后还有一个投影层
    """

    def __init__(self, d_model):
        super().__init__()

        self.d_model = d_model

        # Q, K, V 投影
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)

        # TODO: 输出投影
        self.W_o = nn.___(d_model, d_model)  # 使用 nn.Linear

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape

        # 计算 Q, K, V
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        # 缩放点积注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_model)

        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        attention_weights = F.softmax(scores, dim=-1)
        attention_output = torch.matmul(attention_weights, V)

        # TODO: 应用输出投影
        output = self.___(attention_output)  # 调用 W_o

        return output, attention_weights


def understand_qkv():
    """
    理解 Q, K, V 的作用

    - Query (Q): "我在找什么？" - 表示当前位置要查询的信息
    - Key (K): "我是什么？" - 表示每个位置的标识符，用于匹配
    - Value (V): "我包含什么？" - 表示每个位置的内容

    相似的 Q 和 K 会产生高注意力分数，
    然后用这个分数对 V 进行加权求和
    """
    d_model = 4
    seq_len = 3

    # 假设输入是三个词的嵌入
    x = torch.tensor([[[1.0, 0.0, 0.0, 0.0],    # 词 1
                       [0.0, 1.0, 0.0, 0.0],     # 词 2
                       [0.0, 0.0, 1.0, 0.0]]])   # 词 3

    # 简单的自注意力（无投影，Q=K=V=x）
    Q = x
    K = x
    V = x

    # TODO: 计算注意力分数
    scores = torch.matmul(Q, K.___(-2, -1))  # 转置 K

    # 因为每个词的嵌入是正交的，所以只有相同位置会有高分数
    # scores 应该接近单位矩阵

    # TODO: 计算注意力权重
    weights = F.softmax(scores, dim=___)  # 填入正确的维度

    return scores, weights


def compare_with_without_projection():
    """
    对比有无投影的区别

    投影矩阵让模型能够学习：
    - W_q: 如何构造查询
    - W_k: 如何构造键
    - W_v: 如何构造值
    - W_o: 如何组合注意力输出

    没有投影时，模型的表达能力有限
    """
    d_model = 64
    seq_len = 10
    batch_size = 2

    x = torch.randn(batch_size, seq_len, d_model)

    # 创建两种自注意力
    attn_simple = SelfAttention(d_model)
    attn_proj = SelfAttentionWithProjection(d_model)

    # TODO: 计算参数数量
    simple_params = sum(p.numel() for p in attn_simple.___())  # 使用 parameters()
    proj_params = sum(p.numel() for p in attn_proj.parameters())

    # 带输出投影的版本有更多参数
    # simple: 3 * (d_model * d_model) = 3 * 64 * 64
    # proj: 4 * (d_model * d_model) = 4 * 64 * 64

    return simple_params, proj_params


def main():
    print("测试 SelfAttention...")
    attn = SelfAttention(d_model=64)
    x = torch.randn(2, 10, 64)  # (batch=2, seq_len=10, d_model=64)
    output, weights = attn(x)
    assert output.shape == (2, 10, 64), f"期望形状 (2, 10, 64)，得到 {output.shape}"
    assert weights.shape == (2, 10, 10), f"期望权重形状 (2, 10, 10)，得到 {weights.shape}"
    # 验证权重和为 1
    assert torch.allclose(weights.sum(dim=-1), torch.ones(2, 10))
    print("✓ SelfAttention 通过!")

    print("\n测试带掩码的 SelfAttention...")
    mask = torch.zeros(2, 10, 10).bool()
    mask[:, :, 5:] = True  # 掩盖后半部分
    output, weights = attn(x, mask)
    # 被掩盖的位置权重应该接近 0
    assert torch.all(weights[:, :, 5:] < 1e-6)
    print("✓ 带掩码的 SelfAttention 通过!")

    print("\n测试 SelfAttentionWithProjection...")
    attn_proj = SelfAttentionWithProjection(d_model=64)
    output, weights = attn_proj(x)
    assert output.shape == (2, 10, 64)
    print("✓ SelfAttentionWithProjection 通过!")

    print("\n测试 understand_qkv...")
    scores, weights = understand_qkv()
    # 对角线应该有最高分数
    for i in range(3):
        assert scores[0, i, i] >= scores[0, i].max() - 0.01
    print("✓ understand_qkv 通过!")

    print("\n测试 compare_with_without_projection...")
    simple_params, proj_params = compare_with_without_projection()
    assert proj_params > simple_params, "带投影的版本应该有更多参数"
    print(f"✓ 参数对比通过! Simple: {simple_params}, With Projection: {proj_params}")

    print("\n🎉 所有测试通过！自注意力掌握完成！")


if __name__ == "__main__":
    main()
