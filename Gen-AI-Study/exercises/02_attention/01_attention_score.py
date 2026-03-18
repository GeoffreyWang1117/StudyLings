"""
练习 09: 注意力分数 (Attention Score)

注意力机制是现代深度学习的核心，它让模型能够"关注"输入的不同部分。
注意力分数决定了每个位置应该获得多少关注。

缩放点积注意力公式：
Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

在这个练习中，你将学习：
- Query, Key, Value 的概念
- 如何计算注意力分数
- 缩放因子的作用
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


def compute_attention_scores(query, key):
    """
    计算注意力分数

    Args:
        query: 查询向量，形状 (batch_size, seq_len_q, d_k)
        key: 键向量，形状 (batch_size, seq_len_k, d_k)

    Returns:
        attention_scores: 注意力分数，形状 (batch_size, seq_len_q, seq_len_k)
    """
    d_k = query.size(-1)

    # TODO: 计算 Q @ K^T
    # query: (batch, seq_q, d_k)
    # key: (batch, seq_k, d_k)
    # key 需要转置最后两个维度
    scores = torch.matmul(query, key.___(___))  # 使用 transpose() 或 permute()

    # TODO: 缩放
    # 除以 sqrt(d_k) 防止点积值过大导致 softmax 梯度消失
    scores = scores / math.___(d_k)  # 使用 math.sqrt

    return scores


def compute_attention_weights(scores, mask=None):
    """
    将注意力分数转换为注意力权重

    Args:
        scores: 注意力分数，形状 (batch_size, seq_len_q, seq_len_k)
        mask: 可选的掩码，形状 (batch_size, 1, seq_len_k) 或 (batch_size, seq_len_q, seq_len_k)
              True 表示该位置应被掩盖（设为负无穷）

    Returns:
        attention_weights: 注意力权重，形状 (batch_size, seq_len_q, seq_len_k)
    """
    if mask is not None:
        # TODO: 将掩码位置设为负无穷
        # 这样 softmax 后这些位置的权重就会接近 0
        scores = scores.masked_fill(mask, float("___"))  # 填入负无穷表示

    # TODO: 对最后一个维度应用 softmax
    attention_weights = F.___(scores, dim=___)  # 使用 softmax，填入维度

    return attention_weights


def scaled_dot_product_attention(query, key, value, mask=None):
    """
    完整的缩放点积注意力

    Args:
        query: (batch_size, seq_len_q, d_k)
        key: (batch_size, seq_len_k, d_k)
        value: (batch_size, seq_len_k, d_v)
        mask: 可选掩码

    Returns:
        output: (batch_size, seq_len_q, d_v)
        attention_weights: (batch_size, seq_len_q, seq_len_k)
    """
    # 步骤 1: 计算注意力分数
    scores = compute_attention_scores(query, key)

    # 步骤 2: 转换为注意力权重
    attention_weights = compute_attention_weights(scores, mask)

    # TODO: 步骤 3: 加权求和 value
    # attention_weights: (batch, seq_q, seq_k)
    # value: (batch, seq_k, d_v)
    # output: (batch, seq_q, d_v)
    output = torch.___(attention_weights, value)  # 使用 matmul

    return output, attention_weights


def visualize_attention_concept():
    """
    用一个简单的例子理解注意力机制

    假设我们在做机器翻译，要将 "I love cats" 翻译成中文
    - Query: 当前要生成的目标词的表示
    - Key: 源语言每个词的表示（用于匹配）
    - Value: 源语言每个词的内容（用于提取信息）
    """
    # 简化的例子：3 个源词，2 维向量
    # "I", "love", "cats"
    batch_size = 1
    seq_len = 3
    d_k = 2

    # 假设的 Key（源词表示）
    key = torch.tensor([[[1.0, 0.0],    # "I"
                         [0.0, 1.0],     # "love"
                         [0.5, 0.5]]])   # "cats"

    # 假设的 Value（源词内容）
    value = torch.tensor([[[1.0, 0.0],   # "I" 的内容
                           [0.0, 1.0],    # "love" 的内容
                           [0.5, 0.5]]])  # "cats" 的内容

    # TODO: 创建一个与 "cats" 最相似的 Query
    # 如果我们想关注 "cats"，Query 应该接近 [0.5, 0.5]
    query = torch.tensor([[[___, ___]]])  # 填入合适的值使其关注 "cats"

    # 计算注意力
    output, weights = scaled_dot_product_attention(query, key, value)

    # weights 应该在 "cats" 位置有最高的权重
    return weights, output


def main():
    print("测试 compute_attention_scores...")
    query = torch.randn(2, 4, 64)  # (batch=2, seq_q=4, d_k=64)
    key = torch.randn(2, 6, 64)    # (batch=2, seq_k=6, d_k=64)
    scores = compute_attention_scores(query, key)
    assert scores.shape == (2, 4, 6), f"期望形状 (2, 4, 6)，得到 {scores.shape}"
    print("✓ compute_attention_scores 通过!")

    print("\n测试 compute_attention_weights...")
    scores = torch.randn(2, 4, 6)
    weights = compute_attention_weights(scores)
    # 权重应该在最后一个维度上和为 1
    sums = weights.sum(dim=-1)
    assert torch.allclose(sums, torch.ones_like(sums)), "权重应该和为 1"
    print("✓ compute_attention_weights 通过!")

    print("\n测试带掩码的 attention_weights...")
    mask = torch.zeros(2, 4, 6).bool()
    mask[:, :, -2:] = True  # 掩盖最后两个位置
    weights = compute_attention_weights(scores, mask)
    # 被掩盖的位置权重应该接近 0
    assert torch.all(weights[:, :, -2:] < 1e-6), "掩盖位置的权重应该接近 0"
    print("✓ 带掩码的 attention_weights 通过!")

    print("\n测试 scaled_dot_product_attention...")
    query = torch.randn(2, 4, 64)
    key = torch.randn(2, 6, 64)
    value = torch.randn(2, 6, 128)  # d_v 可以不等于 d_k
    output, weights = scaled_dot_product_attention(query, key, value)
    assert output.shape == (2, 4, 128), f"期望形状 (2, 4, 128)，得到 {output.shape}"
    assert weights.shape == (2, 4, 6)
    print("✓ scaled_dot_product_attention 通过!")

    print("\n测试 visualize_attention_concept...")
    weights, output = visualize_attention_concept()
    # "cats" 在位置 2，应该有最高权重
    cats_weight = weights[0, 0, 2]
    other_weights = torch.cat([weights[0, 0, :2], weights[0, 0, 3:]])
    if other_weights.numel() > 0:
        assert cats_weight > other_weights.max(), "cats 应该获得最高注意力"
    print(f"✓ visualize_attention_concept 通过! (cats 权重: {cats_weight:.4f})")

    print("\n🎉 所有测试通过！注意力分数掌握完成！")


if __name__ == "__main__":
    main()
