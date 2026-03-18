"""
练习 55: 量化 (Quantization)

量化是将模型从高精度 (FP32/FP16) 转换为低精度 (INT8/INT4) 的技术。

优势：
- 减少模型大小 (4x for INT8, 8x for INT4)
- 加速推理
- 减少显存占用

类型：
1. 动态量化: 推理时即时量化
2. 静态量化: 使用校准数据预先计算缩放因子
3. 量化感知训练 (QAT): 训练时模拟量化

在这个练习中，你将学习：
- 量化的基本原理
- 对称/非对称量化
- INT8 和 INT4 量化实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def symmetric_quantize(x, num_bits=8):
    """
    对称量化

    将浮点数映射到 [-2^(n-1)+1, 2^(n-1)-1]

    scale = max(|x|) / (2^(n-1) - 1)
    x_q = round(x / scale)
    """
    qmin = -(2 ** (num_bits - 1)) + 1
    qmax = 2 ** (num_bits - 1) - 1

    # TODO: 计算缩放因子
    max_val = x.abs().max()
    scale = max_val / ___  # 填入 qmax

    # TODO: 量化
    x_q = torch.round(x / scale).clamp(qmin, qmax).to(torch.int8)

    return x_q, scale


def symmetric_dequantize(x_q, scale):
    """
    对称反量化

    x = x_q * scale
    """
    # TODO: 反量化
    return x_q.float() * ___  # 填入 scale


def asymmetric_quantize(x, num_bits=8):
    """
    非对称量化

    将浮点数映射到 [0, 2^n - 1]
    更适合非对称分布的数据 (如 ReLU 输出)

    scale = (max - min) / (2^n - 1)
    zero_point = round(-min / scale)
    x_q = round(x / scale) + zero_point
    """
    qmin = 0
    qmax = 2 ** num_bits - 1

    x_min = x.min()
    x_max = x.max()

    # TODO: 计算 scale 和 zero_point
    scale = (x_max - x_min) / (qmax - ___)  # 填入 qmin
    zero_point = torch.round(-x_min / scale).clamp(qmin, qmax)

    # TODO: 量化
    x_q = torch.round(x / scale + zero_point).clamp(qmin, qmax).to(torch.uint8)

    return x_q, scale, zero_point


def asymmetric_dequantize(x_q, scale, zero_point):
    """非对称反量化"""
    # TODO: 反量化
    return (x_q.float() - zero_point) * ___  # 填入 scale


class QuantizedLinear(nn.Module):
    """
    INT8 量化线性层

    权重静态量化，激活动态量化
    """

    def __init__(self, in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        # 原始权重 (用于初始化)
        weight = torch.randn(out_features, in_features) / in_features ** 0.5

        # 量化权重
        self.weight_q, self.weight_scale = symmetric_quantize(weight, num_bits=8)
        self.register_buffer('_weight_q', self.weight_q)
        self.register_buffer('_weight_scale', torch.tensor([self.weight_scale]))

    def forward(self, x):
        # 动态量化输入
        x_q, x_scale = symmetric_quantize(x, num_bits=8)

        # TODO: 反量化并计算
        # 实际实现会使用整数矩阵乘法，这里简化为反量化后计算
        weight = symmetric_dequantize(self._weight_q, self._weight_scale.item())
        x_dq = symmetric_dequantize(x_q, ___)  # 填入 x_scale

        return F.linear(x_dq, weight)

    @classmethod
    def from_float(cls, linear_module):
        """从 float 线性层转换"""
        quantized = cls(linear_module.in_features, linear_module.out_features)
        weight_q, weight_scale = symmetric_quantize(linear_module.weight.data)
        quantized._weight_q = weight_q
        quantized._weight_scale = torch.tensor([weight_scale])
        return quantized


def int4_quantize(x, group_size=128):
    """
    INT4 分组量化

    将权重分组，每组单独量化到 [-8, 7]
    使用分组可以提高精度
    """
    orig_shape = x.shape
    x = x.view(-1, group_size)

    # TODO: 对每组计算 scale
    max_vals = x.abs().max(dim=1, keepdim=True).values
    scale = max_vals / ___  # 填入 7 (INT4 的最大值)

    # 量化到 INT4 范围 [-8, 7]
    x_q = torch.round(x / (scale + 1e-8)).clamp(-8, 7).to(torch.int8)

    return x_q.view(orig_shape), scale.view(-1)


def int4_dequantize(x_q, scale, group_size=128):
    """INT4 反量化"""
    orig_shape = x_q.shape
    x_q = x_q.view(-1, group_size)
    scale = scale.view(-1, 1)

    x = x_q.float() * scale
    return x.view(orig_shape)


class FakeQuantize(torch.autograd.Function):
    """
    伪量化 (用于量化感知训练 QAT)

    前向: 模拟量化效果
    反向: 直通估计器 (STE)
    """

    @staticmethod
    def forward(ctx, x, num_bits=8):
        # TODO: 量化再反量化，模拟精度损失
        x_q, scale = symmetric_quantize(x, num_bits)
        x_fake = symmetric_dequantize(x_q, ___)  # 填入 scale
        return x_fake

    @staticmethod
    def backward(ctx, grad_output):
        # 直通估计器: 梯度直接传递
        return grad_output, None


def compute_quantization_error(x, num_bits=8):
    """计算量化误差"""
    x_q, scale = symmetric_quantize(x, num_bits)
    x_dq = symmetric_dequantize(x_q, scale)

    mse = F.mse_loss(x, x_dq)
    max_error = (x - x_dq).abs().max()

    return mse, max_error


def main():
    torch.manual_seed(42)

    print("测试对称量化...")
    x = torch.randn(4, 4) * 2
    x_q, scale = symmetric_quantize(x, num_bits=8)
    x_dq = symmetric_dequantize(x_q, scale)

    mse = F.mse_loss(x, x_dq)
    print(f"✓ 对称量化 MSE: {mse:.6f}")
    assert x_q.dtype == torch.int8

    print("\n测试非对称量化...")
    x_relu = F.relu(torch.randn(4, 4))  # ReLU 输出非负
    x_q, scale, zp = asymmetric_quantize(x_relu)
    x_dq = asymmetric_dequantize(x_q, scale, zp)

    mse = F.mse_loss(x_relu, x_dq)
    print(f"✓ 非对称量化 MSE: {mse:.6f}")
    assert x_q.dtype == torch.uint8

    print("\n测试 INT4 量化...")
    weight = torch.randn(256, 256)
    w_q, scale = int4_quantize(weight, group_size=64)
    w_dq = int4_dequantize(w_q, scale, group_size=64)

    mse = F.mse_loss(weight, w_dq)
    print(f"✓ INT4 量化 MSE: {mse:.6f}")

    print("\n测试 QuantizedLinear...")
    linear = nn.Linear(128, 64, bias=False)
    quantized_linear = QuantizedLinear(128, 64)

    x = torch.randn(2, 10, 128)
    out = quantized_linear(x)
    assert out.shape == (2, 10, 64)
    print(f"✓ 量化线性层输出: {out.shape}")

    print("\n量化误差分析:")
    for bits in [8, 4, 2]:
        weight = torch.randn(512, 512)
        mse, max_err = compute_quantization_error(weight, num_bits=bits)
        print(f"  INT{bits}: MSE = {mse:.6f}, Max Error = {max_err:.4f}")

    print("\n模型大小对比:")
    num_params = 1_000_000_000  # 1B 参数
    print(f"  FP32: {num_params * 4 / 1024**3:.2f} GB")
    print(f"  FP16: {num_params * 2 / 1024**3:.2f} GB")
    print(f"  INT8: {num_params * 1 / 1024**3:.2f} GB")
    print(f"  INT4: {num_params * 0.5 / 1024**3:.2f} GB")

    print("\n🎉 所有测试通过！量化掌握完成！")


if __name__ == "__main__":
    main()
