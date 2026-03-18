"""
练习 15: Transformer 块 (Transformer Block)

Transformer 块是 Transformer 架构的核心构建单元。
它由多头注意力和前馈网络组成，加上残差连接和层归一化。

标准结构 (Pre-LN):
x = x + MultiHeadAttention(LayerNorm(x))
x = x + FeedForward(LayerNorm(x))

在这个练习中，你将学习：
- Transformer 块的完整结构
- 残差连接的作用
- 编码器块 vs 解码器块
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MultiHeadAttention(nn.Module):
    """多头注意力（复用之前的实现）"""

    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask.unsqueeze(1), float('-inf'))

        attn = self.dropout(F.softmax(scores, dim=-1))
        output = torch.matmul(attn, V)
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        return self.W_o(output)


class FeedForward(nn.Module):
    """前馈网络"""

    def __init__(self, d_model, d_ff=None, dropout=0.1):
        super().__init__()
        if d_ff is None:
            d_ff = 4 * d_model
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.linear2(self.dropout(F.gelu(self.linear1(x))))


class TransformerEncoderBlock(nn.Module):
    """
    Transformer 编码器块

    结构 (Pre-LN):
    x = x + Attention(LayerNorm(x))
    x = x + FFN(LayerNorm(x))
    """

    def __init__(self, d_model, num_heads, d_ff=None, dropout=0.1):
        super().__init__()

        # TODO: 层归一化 1（注意力之前）
        self.norm1 = nn.___(d_model)  # 使用 nn.LayerNorm

        # TODO: 多头注意力
        self.attention = ___(d_model, num_heads, dropout)  # 使用 MultiHeadAttention

        # TODO: 层归一化 2（FFN 之前）
        self.norm2 = nn.___(d_model)  # 使用 nn.LayerNorm

        # TODO: 前馈网络
        self.ffn = ___(d_model, d_ff, dropout)  # 使用 FeedForward

        # Dropout（用于残差连接后）
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        """
        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)
            mask: 可选的注意力掩码

        Returns:
            输出，形状 (batch_size, seq_len, d_model)
        """
        # TODO: 自注意力子层（带残差连接）
        # Pre-LN: 先归一化，再注意力，再残差
        normed = self.norm1(x)
        attn_output = self.attention(normed, normed, normed, mask)
        x = x + self.dropout(___)  # 填入注意力输出

        # TODO: FFN 子层（带残差连接）
        normed = self.___(x)  # 应用第二个层归一化
        ffn_output = self.ffn(normed)
        x = x + self.___(ffn_output)  # 应用 dropout

        return x


class TransformerDecoderBlock(nn.Module):
    """
    Transformer 解码器块

    比编码器块多一个交叉注意力层：
    x = x + CausalSelfAttention(LayerNorm(x))
    x = x + CrossAttention(LayerNorm(x), encoder_output)
    x = x + FFN(LayerNorm(x))
    """

    def __init__(self, d_model, num_heads, d_ff=None, dropout=0.1):
        super().__init__()

        # 自注意力（因果掩码）
        self.norm1 = nn.LayerNorm(d_model)
        self.self_attention = MultiHeadAttention(d_model, num_heads, dropout)

        # TODO: 交叉注意力（关注编码器输出）
        self.norm2 = nn.LayerNorm(d_model)
        self.cross_attention = ___(d_model, num_heads, dropout)

        # 前馈网络
        self.norm3 = nn.LayerNorm(d_model)
        self.ffn = FeedForward(d_model, d_ff, dropout)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, encoder_output, self_mask=None, cross_mask=None):
        """
        Args:
            x: 解码器输入，形状 (batch_size, tgt_len, d_model)
            encoder_output: 编码器输出，形状 (batch_size, src_len, d_model)
            self_mask: 自注意力掩码（因果掩码）
            cross_mask: 交叉注意力掩码

        Returns:
            输出，形状 (batch_size, tgt_len, d_model)
        """
        # 自注意力（因果）
        normed = self.norm1(x)
        self_attn = self.self_attention(normed, normed, normed, self_mask)
        x = x + self.dropout(self_attn)

        # TODO: 交叉注意力
        # Query 来自解码器，Key 和 Value 来自编码器
        normed = self.norm2(x)
        cross_attn = self.cross_attention(
            normed,           # query
            ___,              # key (填入编码器输出)
            encoder_output,   # value
            cross_mask
        )
        x = x + self.dropout(cross_attn)

        # FFN
        normed = self.norm3(x)
        ffn_output = self.ffn(normed)
        x = x + self.dropout(ffn_output)

        return x


def understand_residual_connection():
    """
    理解残差连接的作用

    残差连接 (Residual Connection / Skip Connection):
    output = x + F(x)

    优点：
    1. 缓解梯度消失：梯度可以直接流过残差路径
    2. 让网络更容易学习恒等映射
    3. 允许堆叠更深的层
    """
    d_model = 64

    # 没有残差连接：深层网络难以训练
    class DeepNetworkNoResidual(nn.Module):
        def __init__(self, num_layers):
            super().__init__()
            self.layers = nn.ModuleList([
                nn.Linear(d_model, d_model) for _ in range(num_layers)
            ])

        def forward(self, x):
            for layer in self.layers:
                x = F.relu(layer(x))
            return x

    # 有残差连接：可以训练很深的网络
    class DeepNetworkWithResidual(nn.Module):
        def __init__(self, num_layers):
            super().__init__()
            self.layers = nn.ModuleList([
                nn.Linear(d_model, d_model) for _ in range(num_layers)
            ])

        def forward(self, x):
            for layer in self.layers:
                # TODO: 添加残差连接
                x = x + F.relu(layer(___))  # 填入输入
            return x

    # 测试梯度流动
    num_layers = 20
    net_no_res = DeepNetworkNoResidual(num_layers)
    net_with_res = DeepNetworkWithResidual(num_layers)

    x = torch.randn(1, d_model, requires_grad=True)

    # 测量输出的范数（有残差应该更稳定）
    out_no_res = net_no_res(x)
    out_with_res = net_with_res(x)

    return out_no_res.norm().item(), out_with_res.norm().item()


def main():
    print("测试 TransformerEncoderBlock...")
    encoder_block = TransformerEncoderBlock(d_model=64, num_heads=8, dropout=0.0)
    x = torch.randn(2, 10, 64)
    output = encoder_block(x)
    assert output.shape == (2, 10, 64), f"期望形状 (2, 10, 64)，得到 {output.shape}"
    print("✓ TransformerEncoderBlock 通过!")

    print("\n测试 TransformerDecoderBlock...")
    decoder_block = TransformerDecoderBlock(d_model=64, num_heads=8, dropout=0.0)
    tgt = torch.randn(2, 8, 64)   # 目标序列
    memory = torch.randn(2, 10, 64)  # 编码器输出
    # 创建因果掩码
    causal_mask = torch.triu(torch.ones(8, 8), diagonal=1).bool()
    output = decoder_block(tgt, memory, self_mask=causal_mask)
    assert output.shape == (2, 8, 64), f"期望形状 (2, 8, 64)，得到 {output.shape}"
    print("✓ TransformerDecoderBlock 通过!")

    print("\n测试残差连接...")
    norm_no_res, norm_with_res = understand_residual_connection()
    print(f"  无残差输出范数: {norm_no_res:.4f}")
    print(f"  有残差输出范数: {norm_with_res:.4f}")
    # 有残差的输出应该更稳定（范数更大）
    print("✓ 残差连接测试完成!")

    print("\n测试堆叠多层...")
    # 堆叠多个编码器块
    num_layers = 6
    layers = nn.ModuleList([
        TransformerEncoderBlock(d_model=64, num_heads=8, dropout=0.0)
        for _ in range(num_layers)
    ])
    x = torch.randn(2, 10, 64)
    for layer in layers:
        x = layer(x)
    assert x.shape == (2, 10, 64)
    print(f"✓ 成功堆叠 {num_layers} 层 Transformer 块!")

    print("\n🎉 所有测试通过！Transformer 块掌握完成！")


if __name__ == "__main__":
    main()
