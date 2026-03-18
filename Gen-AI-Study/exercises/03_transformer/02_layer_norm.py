"""
练习 14: 层归一化 (Layer Normalization)

层归一化对于稳定 Transformer 的训练至关重要。
与批归一化不同，层归一化沿着特征维度进行归一化。

公式：
LayerNorm(x) = γ * (x - μ) / √(σ² + ε) + β

其中 μ 和 σ² 是沿特征维度计算的均值和方差，
γ (gamma) 和 β (beta) 是可学习的参数。

在这个练习中，你将学习：
- 层归一化的计算过程
- 为什么用层归一化而不是批归一化
- Pre-LN vs Post-LN
"""

import torch
import torch.nn as nn


class LayerNorm(nn.Module):
    """
    手动实现层归一化
    """

    def __init__(self, normalized_shape, eps=1e-5):
        """
        Args:
            normalized_shape: 归一化的维度（通常是 d_model）
            eps: 数值稳定性的小常数
        """
        super().__init__()

        self.eps = eps

        # TODO: 创建可学习的缩放参数 gamma (初始化为 1)
        self.gamma = nn.Parameter(torch.___(normalized_shape))  # 使用 ones

        # TODO: 创建可学习的偏移参数 beta (初始化为 0)
        self.beta = nn.Parameter(torch.___(normalized_shape))  # 使用 zeros

    def forward(self, x):
        """
        Args:
            x: 输入张量，形状 (..., normalized_shape)

        Returns:
            归一化后的张量，形状不变
        """
        # TODO: 计算均值（沿最后一个维度）
        # keepdim=True 保持维度以便广播
        mean = x.___(dim=-1, keepdim=True)  # 使用 mean()

        # TODO: 计算方差（沿最后一个维度）
        var = x.___(dim=-1, keepdim=True)  # 使用 var()

        # TODO: 归一化
        # x_norm = (x - mean) / sqrt(var + eps)
        x_norm = (x - mean) / torch.___(var + self.eps)  # 使用 sqrt

        # TODO: 缩放和偏移
        output = self.___ * x_norm + self.___  # 使用 gamma 和 beta

        return output


class RMSNorm(nn.Module):
    """
    RMSNorm (Root Mean Square Normalization)

    RMSNorm 是 LayerNorm 的简化版本，不减去均值，被 LLaMA 采用。
    RMSNorm(x) = γ * x / √(mean(x²) + ε)

    优点：计算更简单，效果相近
    """

    def __init__(self, normalized_shape, eps=1e-6):
        super().__init__()

        self.eps = eps
        # TODO: 只有缩放参数，没有偏移参数
        self.weight = nn.Parameter(torch.___(normalized_shape))  # 使用 ones

    def forward(self, x):
        # TODO: 计算均方根 (RMS)
        # rms = sqrt(mean(x^2))
        rms = torch.sqrt(x.pow(2).mean(dim=-1, keepdim=___) + self.eps)  # 填入 True

        # TODO: 归一化并缩放
        output = self.___ * (x / rms)  # 使用 weight

        return output


def compare_layer_norm_batch_norm():
    """
    理解 LayerNorm 和 BatchNorm 的区别

    - BatchNorm: 沿 batch 维度归一化，对每个特征独立
      适合 CNN，但在 RNN/Transformer 中表现不佳
      因为序列长度可变，batch 统计不稳定

    - LayerNorm: 沿特征维度归一化，对每个样本独立
      不依赖 batch，适合 RNN/Transformer
    """
    batch_size = 4
    seq_len = 10
    d_model = 64

    x = torch.randn(batch_size, seq_len, d_model)

    # TODO: 使用 PyTorch 的 LayerNorm
    layer_norm = nn.___(d_model)  # 使用 nn.LayerNorm
    ln_output = layer_norm(x)

    # TODO: 使用 PyTorch 的 BatchNorm
    # 注意：BatchNorm1d 期望 (batch, features) 或 (batch, features, length)
    # 需要转置
    batch_norm = nn.___(d_model)  # 使用 nn.BatchNorm1d
    x_transposed = x.transpose(1, 2)  # (batch, d_model, seq_len)
    bn_output = batch_norm(x_transposed).transpose(1, 2)

    return ln_output.shape, bn_output.shape


def pre_ln_vs_post_ln():
    """
    Pre-LN vs Post-LN

    Post-LN (原始 Transformer):
    x = x + Attention(LayerNorm(x))
    x = x + FFN(LayerNorm(x))

    Pre-LN (GPT-2 开始采用):
    x = LayerNorm(x + Attention(x))
    x = LayerNorm(x + FFN(x))

    Pre-LN 训练更稳定，不需要 warmup
    """
    d_model = 64

    # 简化的 Post-LN 块
    class PostLNBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.attn = nn.Linear(d_model, d_model)  # 简化的注意力
            self.ffn = nn.Linear(d_model, d_model)   # 简化的 FFN

        def forward(self, x):
            # TODO: Post-LN: 先加残差，再归一化
            x = self.norm1(x + self.___(x))
            x = self.___(x + self.ffn(x))
            return x

    # 简化的 Pre-LN 块
    class PreLNBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.attn = nn.Linear(d_model, d_model)
            self.ffn = nn.Linear(d_model, d_model)

        def forward(self, x):
            # TODO: Pre-LN: 先归一化，再加残差
            x = x + self.attn(self.___(x))
            x = x + self.ffn(self.___(x))
            return x

    return PostLNBlock(), PreLNBlock()


def main():
    print("测试 LayerNorm...")
    ln = LayerNorm(normalized_shape=64)
    x = torch.randn(2, 10, 64)
    output = ln(x)
    assert output.shape == (2, 10, 64)

    # 验证归一化后的统计量
    # 每个样本的每个位置，均值应该接近 0，方差应该接近 1
    mean = output.mean(dim=-1)
    var = output.var(dim=-1)
    assert torch.allclose(mean, torch.zeros_like(mean), atol=1e-5)
    assert torch.allclose(var, torch.ones_like(var), atol=1e-1)
    print("✓ LayerNorm 通过!")

    print("\n测试与 PyTorch LayerNorm 对比...")
    pytorch_ln = nn.LayerNorm(64)
    # 复制参数
    with torch.no_grad():
        ln.gamma.copy_(pytorch_ln.weight)
        ln.beta.copy_(pytorch_ln.bias)
    our_output = ln(x)
    pytorch_output = pytorch_ln(x)
    assert torch.allclose(our_output, pytorch_output, atol=1e-5)
    print("✓ 与 PyTorch LayerNorm 一致!")

    print("\n测试 RMSNorm...")
    rms_norm = RMSNorm(normalized_shape=64)
    output = rms_norm(x)
    assert output.shape == (2, 10, 64)
    # RMSNorm 后的 RMS 应该接近 1
    rms = torch.sqrt(output.pow(2).mean(dim=-1))
    assert torch.allclose(rms, torch.ones_like(rms), atol=1e-1)
    print("✓ RMSNorm 通过!")

    print("\n测试 compare_layer_norm_batch_norm...")
    ln_shape, bn_shape = compare_layer_norm_batch_norm()
    assert ln_shape == bn_shape == (4, 10, 64)
    print("✓ compare_layer_norm_batch_norm 通过!")

    print("\n测试 pre_ln_vs_post_ln...")
    post_ln, pre_ln = pre_ln_vs_post_ln()
    x = torch.randn(2, 10, 64)
    post_out = post_ln(x)
    pre_out = pre_ln(x)
    assert post_out.shape == pre_out.shape == (2, 10, 64)
    print("✓ pre_ln_vs_post_ln 通过!")

    print("\n🎉 所有测试通过！层归一化掌握完成！")


if __name__ == "__main__":
    main()
