"""
练习 06: 位置编码 (Positional Encoding)

Transformer 本身不包含位置信息，因此需要通过位置编码来注入。
位置编码让模型能够理解序列中词语的位置关系。

在这个练习中，你将学习：
- 为什么需要位置编码
- 正弦位置编码的公式
- 如何实现位置编码
"""

import torch
import torch.nn as nn
import math


def sinusoidal_position_encoding(seq_len, d_model):
    """
    创建正弦位置编码

    位置编码公式：
    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    其中 pos 是位置，i 是维度索引

    Args:
        seq_len: 序列长度
        d_model: 模型维度

    Returns:
        位置编码矩阵，形状 (seq_len, d_model)
    """
    # 创建位置索引 [0, 1, 2, ..., seq_len-1]
    position = torch.arange(seq_len).unsqueeze(1)  # (seq_len, 1)

    # 创建维度索引的除数
    # div_term = 10000^(2i/d_model) = exp(2i * log(10000) / d_model)
    # TODO: 计算除数项
    # 创建 [0, 2, 4, ..., d_model-2] 的序列
    two_i = torch.arange(0, d_model, 2).float()  # (d_model/2,)

    # TODO: 计算 10000^(2i/d_model)
    # 使用 exp(2i * log(10000) / d_model) 更数值稳定
    div_term = torch.exp(two_i * (-math.log(___) / d_model))  # 填入 10000.0

    # 创建位置编码矩阵
    pe = torch.zeros(seq_len, d_model)

    # TODO: 偶数维度使用 sin
    pe[:, 0::2] = torch.___(position * div_term)  # 使用 sin

    # TODO: 奇数维度使用 cos
    pe[:, 1::2] = torch.___(position * div_term)  # 使用 cos

    return pe


class PositionalEncoding(nn.Module):
    """
    可学习或固定的位置编码模块

    在 Transformer 中，位置编码会加到词嵌入上：
    output = embedding + positional_encoding
    """

    def __init__(self, d_model, max_len=5000, dropout=0.1):
        """
        Args:
            d_model: 模型维度
            max_len: 最大序列长度
            dropout: dropout 概率
        """
        super().__init__()

        # TODO: 创建 dropout 层
        self.dropout = nn.___(p=dropout)  # 使用 nn.Dropout

        # 生成位置编码
        pe = sinusoidal_position_encoding(max_len, d_model)

        # 添加 batch 维度: (max_len, d_model) -> (1, max_len, d_model)
        pe = pe.unsqueeze(0)

        # TODO: 将位置编码注册为 buffer（不是参数，但会保存到模型中）
        # 使用 self.register_buffer() 方法
        self.___("pe", pe)  # 注册 buffer

    def forward(self, x):
        """
        Args:
            x: 输入张量，形状 (batch_size, seq_len, d_model)

        Returns:
            添加位置编码后的张量，形状不变
        """
        seq_len = x.size(1)

        # TODO: 将位置编码加到输入上
        # 只取需要的长度 self.pe[:, :seq_len, :]
        x = x + self.pe[:, :___, :]  # 填入正确的切片

        # TODO: 应用 dropout
        return self.___(x)  # 调用 dropout


class LearnedPositionalEncoding(nn.Module):
    """
    可学习的位置编码

    与固定的正弦位置编码不同，可学习的位置编码将位置嵌入作为参数学习
    GPT 系列模型使用这种方式
    """

    def __init__(self, d_model, max_len=512):
        super().__init__()

        # TODO: 创建可学习的位置嵌入
        # 使用 nn.Embedding，将位置索引映射到向量
        self.pos_embedding = nn.___(max_len, d_model)  # 使用 nn.Embedding

    def forward(self, x):
        """
        Args:
            x: 输入张量，形状 (batch_size, seq_len, d_model)

        Returns:
            添加位置编码后的张量
        """
        batch_size, seq_len, _ = x.shape

        # 创建位置索引 [0, 1, 2, ..., seq_len-1]
        positions = torch.arange(seq_len, device=x.device)

        # TODO: 获取位置嵌入并加到输入上
        pos_emb = self.___(positions)  # 调用 pos_embedding

        return x + pos_emb


def main():
    print("测试 sinusoidal_position_encoding...")
    pe = sinusoidal_position_encoding(seq_len=100, d_model=512)
    assert pe.shape == (100, 512), f"期望形状 (100, 512)，得到 {pe.shape}"
    # 验证数值范围在 [-1, 1] 之间（sin 和 cos 的范围）
    assert pe.min() >= -1.0 and pe.max() <= 1.0
    print("✓ sinusoidal_position_encoding 通过!")

    print("\n测试 PositionalEncoding...")
    pos_enc = PositionalEncoding(d_model=256, max_len=1000, dropout=0.0)
    x = torch.zeros(4, 50, 256)  # (batch=4, seq_len=50, d_model=256)
    output = pos_enc(x)
    assert output.shape == (4, 50, 256)
    # 由于输入是零，输出应该就是位置编码
    # 检查不同位置的编码是否不同
    assert not torch.allclose(output[0, 0], output[0, 1])
    print("✓ PositionalEncoding 通过!")

    print("\n测试 LearnedPositionalEncoding...")
    learned_pe = LearnedPositionalEncoding(d_model=256, max_len=512)
    x = torch.randn(4, 50, 256)
    output = learned_pe(x)
    assert output.shape == (4, 50, 256)
    # 验证是可学习的（参数数量）
    num_params = sum(p.numel() for p in learned_pe.parameters())
    assert num_params == 512 * 256, f"期望 {512*256} 个参数，得到 {num_params}"
    print("✓ LearnedPositionalEncoding 通过!")

    print("\n🎉 所有测试通过！位置编码掌握完成！")


if __name__ == "__main__":
    main()
