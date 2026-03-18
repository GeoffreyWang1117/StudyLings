"""
练习 13: 前馈网络 (Feed-Forward Network)

前馈网络(FFN)是 Transformer 块的重要组成部分。
它由两个线性层和一个激活函数组成。

公式：
FFN(x) = Linear2(Activation(Linear1(x)))
     = max(0, xW_1 + b_1)W_2 + b_2  (如果使用 ReLU)

中间维度（d_ff）通常是输入维度（d_model）的 4 倍。

在这个练习中，你将学习：
- FFN 的结构和作用
- 不同激活函数的选择
- GLU 变体
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FeedForward(nn.Module):
    """
    标准 Transformer 前馈网络
    """

    def __init__(self, d_model, d_ff=None, dropout=0.1):
        """
        Args:
            d_model: 模型维度
            d_ff: 前馈网络中间维度，默认为 4 * d_model
            dropout: dropout 概率
        """
        super().__init__()

        if d_ff is None:
            d_ff = 4 * d_model

        # TODO: 第一个线性层，将 d_model 扩展到 d_ff
        self.linear1 = nn.Linear(d_model, ___)  # 填入输出维度

        # TODO: 第二个线性层，将 d_ff 收缩回 d_model
        self.linear2 = nn.Linear(___, d_model)  # 填入输入维度

        # Dropout
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)

        Returns:
            输出，形状 (batch_size, seq_len, d_model)
        """
        # TODO: FFN(x) = Linear2(Dropout(ReLU(Linear1(x))))
        x = self.linear1(x)
        x = F.___(x)  # 使用 relu 激活
        x = self.dropout(x)
        x = self.___(x)  # 应用第二个线性层

        return x


class FeedForwardGELU(nn.Module):
    """
    使用 GELU 激活函数的前馈网络

    GELU (Gaussian Error Linear Unit) 是 BERT、GPT 等模型使用的激活函数
    GELU(x) = x * Φ(x)，其中 Φ 是标准正态分布的累积分布函数
    """

    def __init__(self, d_model, d_ff=None, dropout=0.1):
        super().__init__()

        if d_ff is None:
            d_ff = 4 * d_model

        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # TODO: 使用 GELU 代替 ReLU
        x = self.linear1(x)
        x = F.___(x)  # 使用 gelu 激活
        x = self.dropout(x)
        x = self.linear2(x)

        return x


class SwiGLU(nn.Module):
    """
    SwiGLU 前馈网络

    SwiGLU 是 GLU (Gated Linear Unit) 的变体，被 LLaMA 等模型采用
    SwiGLU(x) = (xW_1 * SiLU(xW_gate)) @ W_2

    它使用门控机制，让网络能够学习选择性地传递信息
    """

    def __init__(self, d_model, d_ff=None, dropout=0.1):
        super().__init__()

        if d_ff is None:
            # SwiGLU 通常使用 (2/3) * 4 * d_model 作为中间维度
            # 因为有两个投影，这样总参数量与标准 FFN 相近
            d_ff = int(4 * d_model * 2 / 3)

        # TODO: 值投影
        self.w1 = nn.Linear(d_model, d_ff, bias=False)

        # TODO: 门控投影
        self.w_gate = nn.Linear(d_model, ___, bias=False)  # 填入输出维度

        # TODO: 输出投影
        self.w2 = nn.Linear(___, d_model, bias=False)  # 填入输入维度

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        SwiGLU(x) = (x @ W_1 * SiLU(x @ W_gate)) @ W_2
        """
        # TODO: 计算门控值
        gate = F.___(self.w_gate(x))  # 使用 silu 激活 (也叫 swish)

        # TODO: 计算值并与门控相乘
        value = self.w1(x)
        x = value ___ gate  # 填入元素级乘法运算符

        x = self.dropout(x)
        x = self.w2(x)

        return x


def compare_activations():
    """
    比较不同激活函数的特性
    """
    x = torch.linspace(-3, 3, 100)

    # TODO: 计算各种激活函数的输出
    relu_out = F.___(x)   # ReLU
    gelu_out = F.___(x)   # GELU
    silu_out = F.___(x)   # SiLU/Swish

    # ReLU: max(0, x) - 硬截断
    # GELU: x * Φ(x) - 平滑版本
    # SiLU: x * sigmoid(x) - 另一种平滑版本

    return relu_out, gelu_out, silu_out


def main():
    print("测试 FeedForward...")
    ffn = FeedForward(d_model=64, d_ff=256, dropout=0.0)
    x = torch.randn(2, 10, 64)
    output = ffn(x)
    assert output.shape == (2, 10, 64), f"期望形状 (2, 10, 64)，得到 {output.shape}"
    print("✓ FeedForward 通过!")

    print("\n测试 FeedForwardGELU...")
    ffn_gelu = FeedForwardGELU(d_model=64, d_ff=256, dropout=0.0)
    output = ffn_gelu(x)
    assert output.shape == (2, 10, 64)
    print("✓ FeedForwardGELU 通过!")

    print("\n测试 SwiGLU...")
    swiglu = SwiGLU(d_model=64, dropout=0.0)
    output = swiglu(x)
    assert output.shape == (2, 10, 64)
    print("✓ SwiGLU 通过!")

    print("\n测试参数数量...")
    ffn_params = sum(p.numel() for p in ffn.parameters())
    swiglu_params = sum(p.numel() for p in swiglu.parameters())
    # SwiGLU 的参数量应该与标准 FFN 相近
    print(f"  标准 FFN 参数: {ffn_params}")
    print(f"  SwiGLU 参数: {swiglu_params}")
    print("✓ 参数量对比完成!")

    print("\n测试 compare_activations...")
    relu, gelu, silu = compare_activations()
    # 所有激活函数在正区域应该接近 y=x
    assert relu[-1] > 2.5  # ReLU(3) = 3
    assert gelu[-1] > 2.5  # GELU(3) ≈ 3
    assert silu[-1] > 2.5  # SiLU(3) ≈ 2.86
    print("✓ compare_activations 通过!")

    print("\n🎉 所有测试通过！前馈网络掌握完成！")


if __name__ == "__main__":
    main()
