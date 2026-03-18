"""
练习 22: RMSNorm (Root Mean Square Normalization)

RMSNorm 是 LayerNorm 的简化版本，被 LLaMA 等现代模型采用。
它不减去均值，只做缩放归一化。

公式：
RMSNorm(x) = x / RMS(x) * γ
其中 RMS(x) = √(mean(x²) + ε)

相比 LayerNorm 的优势：
1. 计算更简单（不需要计算均值）
2. 效果相近
3. 稍微减少计算量

在这个练习中，你将学习：
- RMSNorm 的实现
- 与 LayerNorm 的对比
- 为什么不减均值也能工作
"""

import torch
import torch.nn as nn


class RMSNorm(nn.Module):
    """
    RMS Normalization
    """

    def __init__(self, dim, eps=1e-6):
        """
        Args:
            dim: 归一化的维度
            eps: 数值稳定性的小常数
        """
        super().__init__()

        self.eps = eps

        # TODO: 创建可学习的缩放参数（初始化为 1）
        self.weight = nn.Parameter(torch.___(dim))  # 使用 ones

    def _norm(self, x):
        """
        计算 RMS 归一化
        x / RMS(x), 其中 RMS(x) = sqrt(mean(x^2) + eps)
        """
        # TODO: 计算 x^2 的均值
        mean_square = x.pow(2).mean(dim=-1, keepdim=___)  # 填入 True

        # TODO: 计算 RMS 并归一化
        rms = torch.sqrt(mean_square + self.___)  # 填入 eps
        return x / rms

    def forward(self, x):
        """
        Args:
            x: 输入张量，形状 (..., dim)

        Returns:
            归一化后的张量
        """
        # TODO: 归一化并缩放
        # 注意：在某些实现中，会先转为 float 计算再转回原精度
        output = self._norm(x.float()).type_as(x)
        return output * self.___  # 填入 weight


class LayerNorm(nn.Module):
    """
    标准 LayerNorm（用于对比）
    """

    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))
        self.bias = nn.Parameter(torch.zeros(dim))

    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        x_norm = (x - mean) / torch.sqrt(var + self.eps)
        return self.weight * x_norm + self.bias


def compare_norm_behaviors():
    """
    对比 RMSNorm 和 LayerNorm 的行为
    """
    dim = 64
    rms_norm = RMSNorm(dim)
    layer_norm = LayerNorm(dim)

    # 测试不同分布的输入
    results = {}

    # 1. 零均值输入
    x_zero_mean = torch.randn(4, 16, dim)
    x_zero_mean = x_zero_mean - x_zero_mean.mean(dim=-1, keepdim=True)

    results['zero_mean'] = {
        'rms': rms_norm(x_zero_mean),
        'layer': layer_norm(x_zero_mean)
    }

    # 2. 非零均值输入
    x_shifted = torch.randn(4, 16, dim) + 5.0

    results['shifted'] = {
        'rms': rms_norm(x_shifted),
        'layer': layer_norm(x_shifted)
    }

    return results


def analyze_norm_difference():
    """
    分析为什么 RMSNorm 不减均值也能工作

    在深度学习中：
    1. 网络通常会学习到接近零均值的表示
    2. 残差连接会自动调整均值
    3. 关键是保持特征的相对大小关系
    """
    dim = 64

    # 创建归一化层
    rms_norm = RMSNorm(dim)
    layer_norm = LayerNorm(dim)

    # 随机输入
    x = torch.randn(100, dim) * 3 + 2  # 非零均值，较大方差

    # 归一化
    x_rms = rms_norm(x)
    x_layer = layer_norm(x)

    # TODO: 计算归一化后的统计量
    # RMSNorm 后的均值不一定是 0
    rms_mean = x_rms.mean(dim=-1).mean().item()
    rms_std = x_rms.std(dim=-1).mean().item()

    # LayerNorm 后的均值接近 0，std 接近 1
    layer_mean = x_layer.mean(dim=-1).mean().item()
    layer_std = x_layer.___(dim=-1).mean().item()  # 使用 std

    return {
        'rms': {'mean': rms_mean, 'std': rms_std},
        'layer': {'mean': layer_mean, 'std': layer_std}
    }


def benchmark_norm():
    """
    简单的性能对比
    """
    import time

    dim = 4096  # 典型的 LLM 维度
    batch_size = 32
    seq_len = 512

    rms_norm = RMSNorm(dim)
    layer_norm = LayerNorm(dim)

    x = torch.randn(batch_size, seq_len, dim)

    # 预热
    for _ in range(10):
        _ = rms_norm(x)
        _ = layer_norm(x)

    # 测试 RMSNorm
    start = time.time()
    for _ in range(100):
        _ = rms_norm(x)
    rms_time = time.time() - start

    # 测试 LayerNorm
    start = time.time()
    for _ in range(100):
        _ = layer_norm(x)
    layer_time = time.time() - start

    return rms_time, layer_time


def main():
    print("测试 RMSNorm...")
    dim = 64
    rms_norm = RMSNorm(dim)
    x = torch.randn(2, 10, dim)
    output = rms_norm(x)
    assert output.shape == (2, 10, dim)

    # 验证 RMS 接近 1
    rms = torch.sqrt(output.pow(2).mean(dim=-1))
    assert torch.allclose(rms, torch.ones_like(rms), atol=0.1)
    print("✓ RMSNorm 通过!")

    print("\n测试参数数量...")
    rms_params = sum(p.numel() for p in rms_norm.parameters())
    layer_norm = LayerNorm(dim)
    layer_params = sum(p.numel() for p in layer_norm.parameters())
    print(f"  RMSNorm 参数: {rms_params}")  # 只有 weight
    print(f"  LayerNorm 参数: {layer_params}")  # weight + bias
    assert rms_params < layer_params
    print("✓ RMSNorm 参数更少!")

    print("\n对比归一化行为...")
    results = compare_norm_behaviors()
    print("  零均值输入:")
    print(f"    RMS 输出范数: {results['zero_mean']['rms'].norm().item():.4f}")
    print(f"    Layer 输出范数: {results['zero_mean']['layer'].norm().item():.4f}")
    print("  偏移均值输入:")
    print(f"    RMS 输出范数: {results['shifted']['rms'].norm().item():.4f}")
    print(f"    Layer 输出范数: {results['shifted']['layer'].norm().item():.4f}")
    print("✓ 行为对比完成!")

    print("\n分析归一化差异...")
    stats = analyze_norm_difference()
    print(f"  RMSNorm - 均值: {stats['rms']['mean']:.4f}, 标准差: {stats['rms']['std']:.4f}")
    print(f"  LayerNorm - 均值: {stats['layer']['mean']:.4f}, 标准差: {stats['layer']['std']:.4f}")
    print("✓ 差异分析完成!")

    print("\n性能对比 (100 次前向传播)...")
    rms_time, layer_time = benchmark_norm()
    print(f"  RMSNorm: {rms_time:.4f}s")
    print(f"  LayerNorm: {layer_time:.4f}s")
    speedup = layer_time / rms_time
    print(f"  RMSNorm 相对速度: {speedup:.2f}x")

    print("\n🎉 所有测试通过！RMSNorm 掌握完成！")


if __name__ == "__main__":
    main()
