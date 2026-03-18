"""
练习 24: 卷积基础 (Convolution Basics)

卷积是处理图像数据的基础操作。
卷积层通过滑动窗口提取局部特征，具有平移不变性和参数共享的特点。

关键概念：
- 卷积核 (kernel): 用于提取特征的小矩阵
- 步幅 (stride): 卷积核滑动的步长
- 填充 (padding): 在边缘添加的像素
- 输入/输出通道: 颜色通道和特征图数量

输出尺寸公式：
out_size = (in_size + 2*padding - kernel_size) // stride + 1

在这个练习中，你将学习：
- 2D 卷积的实现
- 各参数对输出的影响
- 卷积在图像处理中的作用
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def create_conv_layer():
    """创建基本的卷积层"""
    in_channels = 3   # RGB 图像
    out_channels = 16  # 输出 16 个特征图
    kernel_size = 3    # 3x3 卷积核

    # TODO: 创建 2D 卷积层
    # nn.Conv2d(in_channels, out_channels, kernel_size)
    conv = nn.___(in_channels, out_channels, kernel_size)  # 使用 Conv2d

    return conv


def calculate_output_size(in_size, kernel_size, stride=1, padding=0):
    """
    计算卷积输出尺寸

    公式: out = (in + 2*padding - kernel) // stride + 1
    """
    # TODO: 实现输出尺寸计算公式
    out_size = (in_size + 2 * ___ - kernel_size) // stride + ___  # 填入 padding 和 1

    return out_size


def conv_with_padding():
    """
    使用填充保持特征图尺寸不变

    当 kernel_size=3, stride=1 时，padding=1 可以保持尺寸
    当 kernel_size=5, stride=1 时，padding=2 可以保持尺寸
    """
    in_channels = 3
    out_channels = 16
    kernel_size = 3

    # TODO: 设置正确的 padding 使输出尺寸等于输入尺寸
    # 对于 kernel_size=k, stride=1, padding=(k-1)//2 可以保持尺寸
    padding = (kernel_size - 1) // ___  # 填入 2

    conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding)

    return conv


def conv_with_stride():
    """
    使用步幅进行下采样

    stride=2 会使特征图尺寸减半
    """
    in_channels = 16
    out_channels = 32
    kernel_size = 3
    stride = 2
    padding = 1  # 保持整数输出尺寸

    # TODO: 创建步幅卷积
    conv = nn.Conv2d(
        in_channels,
        out_channels,
        kernel_size,
        stride=___,  # 填入 stride
        padding=padding
    )

    return conv


class ConvBlock(nn.Module):
    """
    标准卷积块：Conv -> BatchNorm -> ReLU
    """

    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super().__init__()

        # TODO: 创建卷积层
        self.conv = nn.___(in_channels, out_channels, kernel_size, stride, padding)

        # TODO: 创建批归一化层
        self.bn = nn.___(out_channels)  # 使用 BatchNorm2d

        # TODO: 创建激活函数
        self.relu = nn.___()  # 使用 ReLU

    def forward(self, x):
        # TODO: 实现前向传播
        x = self.conv(x)
        x = self.___(x)  # 应用批归一化
        x = self.___(x)  # 应用 ReLU

        return x


def understand_receptive_field():
    """
    理解感受野 (Receptive Field)

    感受野是输出特征图上一个点对应的输入图像区域。
    多层卷积会增大感受野。

    - 单层 3x3 卷积: 感受野 = 3x3
    - 两层 3x3 卷积: 感受野 = 5x5
    - 三层 3x3 卷积: 感受野 = 7x7

    这就是为什么使用多个小卷积核比一个大卷积核更好：
    - 参数更少
    - 非线性更多
    - 感受野相同
    """
    # 计算感受野
    # 公式：RF_l = RF_{l-1} + (k-1) * stride_product
    def calculate_rf(layers):
        """
        layers: [(kernel_size, stride), ...]
        """
        rf = 1
        stride_product = 1

        for k, s in layers:
            # TODO: 更新感受野
            rf = rf + (k - 1) * ___  # 填入 stride_product
            stride_product *= s

        return rf

    # 三层 3x3 卷积，stride=1
    layers_3x3 = [(3, 1), (3, 1), (3, 1)]
    rf_3x3 = calculate_rf(layers_3x3)

    # 一层 7x7 卷积
    layers_7x7 = [(7, 1)]
    rf_7x7 = calculate_rf(layers_7x7)

    return rf_3x3, rf_7x7


def pooling_operations():
    """
    池化操作：下采样同时保留重要特征
    """
    # 最大池化
    # TODO: 创建 2x2 最大池化层
    max_pool = nn.___(kernel_size=2, stride=2)  # 使用 MaxPool2d

    # 平均池化
    # TODO: 创建 2x2 平均池化层
    avg_pool = nn.___(kernel_size=2, stride=2)  # 使用 AvgPool2d

    # 全局平均池化（将整个特征图变成一个值）
    # TODO: 创建自适应平均池化，输出 1x1
    global_pool = nn.___(output_size=1)  # 使用 AdaptiveAvgPool2d

    return max_pool, avg_pool, global_pool


def main():
    print("测试 create_conv_layer...")
    conv = create_conv_layer()
    x = torch.randn(1, 3, 32, 32)  # (batch, channels, height, width)
    out = conv(x)
    expected_size = calculate_output_size(32, 3, 1, 0)  # 30
    assert out.shape == (1, 16, expected_size, expected_size)
    print(f"✓ 输入 32x32 -> 输出 {expected_size}x{expected_size}")

    print("\n测试 calculate_output_size...")
    assert calculate_output_size(32, 3, 1, 0) == 30
    assert calculate_output_size(32, 3, 1, 1) == 32  # 保持尺寸
    assert calculate_output_size(32, 3, 2, 1) == 16  # 减半
    print("✓ calculate_output_size 通过!")

    print("\n测试 conv_with_padding...")
    conv_pad = conv_with_padding()
    out = conv_pad(x)
    assert out.shape == (1, 16, 32, 32), "padding 应该保持尺寸"
    print("✓ conv_with_padding 通过!")

    print("\n测试 conv_with_stride...")
    conv_stride = conv_with_stride()
    x_16ch = torch.randn(1, 16, 32, 32)
    out = conv_stride(x_16ch)
    assert out.shape == (1, 32, 16, 16), "stride=2 应该减半尺寸"
    print("✓ conv_with_stride 通过!")

    print("\n测试 ConvBlock...")
    block = ConvBlock(3, 16)
    out = block(x)
    assert out.shape == (1, 16, 32, 32)
    print("✓ ConvBlock 通过!")

    print("\n测试 understand_receptive_field...")
    rf_3x3, rf_7x7 = understand_receptive_field()
    assert rf_3x3 == rf_7x7 == 7, "三层 3x3 应该等于 7x7"
    print(f"✓ 三层 3x3 感受野 = {rf_3x3}, 一层 7x7 感受野 = {rf_7x7}")

    # 参数对比
    params_3x3 = 3 * (3 * 3 * 16 * 16)  # 简化
    params_7x7 = 16 * 7 * 7 * 16
    print(f"  三层 3x3 参数约: {params_3x3}")
    print(f"  一层 7x7 参数约: {params_7x7}")

    print("\n测试 pooling_operations...")
    max_pool, avg_pool, global_pool = pooling_operations()
    x = torch.randn(1, 16, 32, 32)

    max_out = max_pool(x)
    assert max_out.shape == (1, 16, 16, 16)

    avg_out = avg_pool(x)
    assert avg_out.shape == (1, 16, 16, 16)

    global_out = global_pool(x)
    assert global_out.shape == (1, 16, 1, 1)

    print("✓ pooling_operations 通过!")

    print("\n🎉 所有测试通过！卷积基础掌握完成！")


if __name__ == "__main__":
    main()
