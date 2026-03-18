"""
练习 25: 转置卷积 (Transposed Convolution)

转置卷积用于上采样，是图像生成中放大特征图的常用方法。
也称为反卷积或分数步长卷积。

转置卷积不是卷积的逆运算，而是：
- 卷积：减小空间尺寸
- 转置卷积：增大空间尺寸

输出尺寸公式：
out_size = (in_size - 1) * stride - 2 * padding + kernel_size + output_padding

在这个练习中，你将学习：
- 转置卷积的实现
- 上采样的不同方法
- 棋盘效应及其解决方案
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def create_transposed_conv():
    """创建基本的转置卷积层"""
    in_channels = 16
    out_channels = 8
    kernel_size = 4
    stride = 2
    padding = 1

    # TODO: 创建转置卷积层
    # nn.ConvTranspose2d 用于上采样
    conv_t = nn.___(  # 使用 ConvTranspose2d
        in_channels,
        out_channels,
        kernel_size,
        stride=stride,
        padding=padding
    )

    return conv_t


def calculate_transposed_output_size(in_size, kernel_size, stride=1, padding=0, output_padding=0):
    """
    计算转置卷积输出尺寸

    公式: out = (in - 1) * stride - 2 * padding + kernel + output_padding
    """
    # TODO: 实现输出尺寸公式
    out_size = (in_size - 1) * ___ - 2 * padding + kernel_size + output_padding

    return out_size


def upsample_2x():
    """
    使用转置卷积进行 2 倍上采样

    常用配置：kernel=4, stride=2, padding=1
    out = (in - 1) * 2 - 2 + 4 = 2 * in
    """
    in_channels = 16
    out_channels = 8

    # TODO: 创建 2 倍上采样的转置卷积
    # 目标：输入 HxW -> 输出 2H x 2W
    conv_t = nn.ConvTranspose2d(
        in_channels,
        out_channels,
        kernel_size=___,  # 填入 4
        stride=___,       # 填入 2
        padding=___       # 填入 1
    )

    return conv_t


class UpsampleBlock(nn.Module):
    """
    上采样块（解决棋盘效应）

    棋盘效应：转置卷积容易产生网格状伪影
    解决方案：先用插值上采样，再用普通卷积
    """

    def __init__(self, in_channels, out_channels, scale_factor=2):
        super().__init__()

        self.scale_factor = scale_factor

        # TODO: 普通卷积（上采样后使用）
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        # TODO: 先用双线性插值上采样
        x = F.___(x, scale_factor=self.scale_factor, mode='bilinear', align_corners=False)

        # 再用卷积处理
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)

        return x


class PixelShuffleUpsample(nn.Module):
    """
    PixelShuffle 上采样

    另一种上采样方法，将通道维度的数据重排到空间维度
    输入: (B, C*r^2, H, W) -> 输出: (B, C, H*r, W*r)

    优点：
    - 不会产生棋盘效应
    - 所有上采样的像素都由卷积产生
    """

    def __init__(self, in_channels, out_channels, scale_factor=2):
        super().__init__()

        self.scale_factor = scale_factor

        # TODO: 卷积到 out_channels * scale_factor^2 通道
        self.conv = nn.Conv2d(
            in_channels,
            out_channels * scale_factor * ___,  # 填入 scale_factor
            kernel_size=3,
            padding=1
        )

        # TODO: PixelShuffle 层
        self.pixel_shuffle = nn.___(scale_factor)  # 使用 PixelShuffle

    def forward(self, x):
        x = self.conv(x)
        x = self.___(x)  # 应用 pixel_shuffle
        return x


def compare_upsample_methods():
    """
    对比不同上采样方法的特点
    """
    in_channels = 16
    out_channels = 8

    methods = {
        'transposed_conv': nn.ConvTranspose2d(in_channels, out_channels, 4, 2, 1),
        'interpolate_conv': UpsampleBlock(in_channels, out_channels),
        'pixel_shuffle': PixelShuffleUpsample(in_channels, out_channels)
    }

    # 测试输入
    x = torch.randn(1, in_channels, 8, 8)

    results = {}
    for name, layer in methods.items():
        out = layer(x)
        params = sum(p.numel() for p in layer.parameters())
        results[name] = {'shape': out.shape, 'params': params}

    return results


def understand_checkerboard():
    """
    理解棋盘效应

    当 kernel_size 不能被 stride 整除时，
    转置卷积的输出像素会有不均匀的覆盖，
    导致周期性的亮暗条纹。

    解决方案：
    1. 使用 kernel_size 可被 stride 整除的配置
    2. 使用 resize + conv 代替转置卷积
    3. 使用 PixelShuffle
    """
    # 好的配置：kernel=4, stride=2 (4 % 2 == 0)
    good_conv = nn.ConvTranspose2d(1, 1, kernel_size=4, stride=2, padding=1)

    # 不好的配置：kernel=3, stride=2 (3 % 2 != 0)
    bad_conv = nn.ConvTranspose2d(1, 1, kernel_size=3, stride=2, padding=1)

    # 测试
    x = torch.ones(1, 1, 4, 4)

    # 设置均匀的权重
    with torch.no_grad():
        good_conv.weight.fill_(1.0)
        good_conv.bias.fill_(0.0)
        bad_conv.weight.fill_(1.0)
        bad_conv.bias.fill_(0.0)

    good_out = good_conv(x)
    bad_out = bad_conv(x)

    # TODO: 计算输出的方差（均匀输出方差应该为 0）
    good_var = good_out.___(dim=(-2, -1)).mean().item()  # 使用 var
    bad_var = bad_out.___(dim=(-2, -1)).mean().item()   # 使用 var

    return good_var, bad_var


def main():
    print("测试 create_transposed_conv...")
    conv_t = create_transposed_conv()
    x = torch.randn(1, 16, 8, 8)
    out = conv_t(x)
    expected = calculate_transposed_output_size(8, 4, 2, 1)
    assert out.shape == (1, 8, expected, expected)
    print(f"✓ 输入 8x8 -> 输出 {expected}x{expected}")

    print("\n测试 calculate_transposed_output_size...")
    assert calculate_transposed_output_size(8, 4, 2, 1) == 16
    assert calculate_transposed_output_size(8, 3, 2, 1) == 15
    print("✓ calculate_transposed_output_size 通过!")

    print("\n测试 upsample_2x...")
    upsample = upsample_2x()
    out = upsample(x)
    assert out.shape == (1, 8, 16, 16), f"期望 (1, 8, 16, 16)，得到 {out.shape}"
    print("✓ upsample_2x 通过!")

    print("\n测试 UpsampleBlock...")
    block = UpsampleBlock(16, 8)
    out = block(x)
    assert out.shape == (1, 8, 16, 16)
    print("✓ UpsampleBlock 通过!")

    print("\n测试 PixelShuffleUpsample...")
    ps_block = PixelShuffleUpsample(16, 8)
    out = ps_block(x)
    assert out.shape == (1, 8, 16, 16)
    print("✓ PixelShuffleUpsample 通过!")

    print("\n对比上采样方法...")
    results = compare_upsample_methods()
    for name, info in results.items():
        print(f"  {name}: shape={info['shape']}, params={info['params']}")

    print("\n理解棋盘效应...")
    good_var, bad_var = understand_checkerboard()
    print(f"  好的配置 (k=4, s=2) 输出方差: {good_var:.6f}")
    print(f"  差的配置 (k=3, s=2) 输出方差: {bad_var:.6f}")
    print("  方差越小说明输出越均匀")

    print("\n🎉 所有测试通过！转置卷积掌握完成！")


if __name__ == "__main__":
    main()
