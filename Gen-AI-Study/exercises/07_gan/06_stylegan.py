"""
练习 36: StyleGAN 核心组件

StyleGAN 引入了风格映射和自适应实例归一化，
实现了高质量、可控的图像生成。

核心创新：
1. Mapping Network: z -> w (中间潜在空间)
2. AdaIN (Adaptive Instance Normalization): 风格注入
3. 逐层风格控制
4. 噪声注入增加细节

在这个练习中，你将学习：
- Mapping Network
- AdaIN 机制
- 风格混合
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MappingNetwork(nn.Module):
    """
    映射网络

    将噪声 z 映射到中间潜在空间 w
    w 空间更加解耦，便于控制
    """

    def __init__(self, z_dim, w_dim, num_layers=8):
        super().__init__()

        layers = []
        for i in range(num_layers):
            in_dim = z_dim if i == 0 else w_dim
            layers.extend([
                nn.Linear(in_dim, w_dim),
                nn.LeakyReLU(0.2)
            ])

        self.mapping = nn.Sequential(*layers)

    def forward(self, z):
        """
        Args:
            z: 噪声向量 (batch, z_dim)

        Returns:
            w: 风格向量 (batch, w_dim)
        """
        # TODO: 可选的潜在空间归一化
        z = z / (z.norm(dim=-1, keepdim=True) + 1e-8)

        # TODO: 映射
        w = self.___(z)  # 填入 mapping

        return w


class AdaIN(nn.Module):
    """
    自适应实例归一化 (Adaptive Instance Normalization)

    AdaIN(x, y) = y_s * (x - μ(x)) / σ(x) + y_b

    用风格向量调制特征图
    """

    def __init__(self, num_features, w_dim):
        super().__init__()

        # 从 w 生成风格参数
        self.fc = nn.Linear(w_dim, num_features * 2)
        self.num_features = num_features

    def forward(self, x, w):
        """
        Args:
            x: 特征图 (batch, channels, H, W)
            w: 风格向量 (batch, w_dim)

        Returns:
            调制后的特征图
        """
        batch_size = x.shape[0]

        # 生成 scale 和 bias
        style = self.fc(w)  # (batch, num_features * 2)
        scale, bias = style.chunk(2, dim=1)  # 各 (batch, num_features)

        # 调整形状用于广播
        scale = scale.view(batch_size, self.num_features, 1, 1)
        bias = bias.view(batch_size, self.num_features, 1, 1)

        # TODO: 实例归一化
        # 计算每个实例、每个通道的均值和标准差
        mean = x.mean(dim=[2, 3], keepdim=True)
        std = x.std(dim=[2, 3], keepdim=True) + 1e-8

        # TODO: 归一化并应用风格
        x_norm = (x - mean) / ___  # 填入 std
        out = scale * x_norm + bias

        return out


class ModulatedConv2d(nn.Module):
    """
    调制卷积 (StyleGAN2)

    通过风格向量调制卷积核权重
    """

    def __init__(self, in_channels, out_channels, kernel_size, w_dim, demodulate=True):
        super().__init__()

        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.demodulate = demodulate

        # 卷积权重
        self.weight = nn.Parameter(
            torch.randn(out_channels, in_channels, kernel_size, kernel_size)
        )
        nn.init.kaiming_normal_(self.weight)

        # 风格调制
        self.style = nn.Linear(w_dim, in_channels)

    def forward(self, x, w):
        """
        Args:
            x: 输入特征 (batch, in_channels, H, W)
            w: 风格向量 (batch, w_dim)
        """
        batch_size = x.shape[0]

        # 获取风格调制因子
        style = self.style(w)  # (batch, in_channels)
        style = style.view(batch_size, 1, -1, 1, 1)

        # 调制权重
        # weight: (out, in, k, k) -> (batch, out, in, k, k)
        weight = self.weight.unsqueeze(0) * style

        if self.demodulate:
            # TODO: 解调 (归一化权重)
            sigma = weight.pow(2).sum(dim=[2, 3, 4], keepdim=True).sqrt() + 1e-8
            weight = weight / ___  # 填入 sigma

        # 分组卷积
        x = x.view(1, batch_size * x.shape[1], x.shape[2], x.shape[3])
        weight = weight.view(batch_size * self.out_channels, -1, self.kernel_size, self.kernel_size)

        out = F.conv2d(x, weight, padding=self.kernel_size // 2, groups=batch_size)
        out = out.view(batch_size, self.out_channels, out.shape[2], out.shape[3])

        return out


class NoiseInjection(nn.Module):
    """
    噪声注入

    为每个像素添加缩放的随机噪声，增加细节
    """

    def __init__(self, channels):
        super().__init__()
        # 可学习的噪声缩放因子
        self.weight = nn.Parameter(torch.zeros(1, channels, 1, 1))

    def forward(self, x, noise=None):
        """
        Args:
            x: 特征图 (batch, channels, H, W)
            noise: 可选的噪声 (batch, 1, H, W)
        """
        if noise is None:
            batch, _, height, width = x.shape
            noise = torch.randn(batch, 1, height, width, device=x.device)

        # TODO: 注入缩放的噪声
        return x + self.___ * noise  # 填入 weight


class StyleBlock(nn.Module):
    """
    StyleGAN 基本块

    结合风格调制、噪声注入和卷积
    """

    def __init__(self, in_channels, out_channels, w_dim):
        super().__init__()

        self.conv = ModulatedConv2d(in_channels, out_channels, 3, w_dim)
        self.noise = NoiseInjection(out_channels)
        self.activation = nn.LeakyReLU(0.2)

    def forward(self, x, w, noise=None):
        x = self.conv(x, w)
        x = self.noise(x, noise)
        x = self.activation(x)
        return x


class StyleMixing:
    """
    风格混合

    在不同层使用不同的 w 向量，
    实现粗/细特征的独立控制
    """

    @staticmethod
    def mix(w1, w2, mixing_layer, total_layers):
        """
        Args:
            w1: 第一个风格向量 (batch, w_dim)
            w2: 第二个风格向量 (batch, w_dim)
            mixing_layer: 从哪层开始使用 w2
            total_layers: 总层数

        Returns:
            混合后的风格向量 (total_layers, batch, w_dim)
        """
        # TODO: 前 mixing_layer 层使用 w1，之后使用 w2
        w_mixed = []
        for i in range(total_layers):
            if i < mixing_layer:
                w_mixed.append(___)  # 填入 w1
            else:
                w_mixed.append(w2)

        return torch.stack(w_mixed, dim=0)


def truncation_trick(w, w_avg, psi=0.7):
    """
    截断技巧

    将 w 向平均 w 收缩，提高图像质量
    但会降低多样性

    w' = w_avg + psi * (w - w_avg)
    """
    # TODO: 应用截断
    return w_avg + ___ * (w - w_avg)  # 填入 psi


def main():
    torch.manual_seed(42)

    z_dim = 512
    w_dim = 512
    batch_size = 4

    print("测试 MappingNetwork...")
    mapping = MappingNetwork(z_dim, w_dim, num_layers=8)
    z = torch.randn(batch_size, z_dim)
    w = mapping(z)
    assert w.shape == (batch_size, w_dim)
    print(f"✓ z: {z.shape} -> w: {w.shape}")

    print("\n测试 AdaIN...")
    adain = AdaIN(num_features=128, w_dim=w_dim)
    x = torch.randn(batch_size, 128, 16, 16)
    out = adain(x, w)
    assert out.shape == x.shape
    print(f"✓ AdaIN 输出: {out.shape}")

    print("\n测试 ModulatedConv2d...")
    mod_conv = ModulatedConv2d(64, 128, 3, w_dim)
    x = torch.randn(batch_size, 64, 32, 32)
    out = mod_conv(x, w)
    assert out.shape == (batch_size, 128, 32, 32)
    print(f"✓ ModulatedConv2d: {x.shape} -> {out.shape}")

    print("\n测试 NoiseInjection...")
    noise_layer = NoiseInjection(128)
    x = torch.randn(batch_size, 128, 16, 16)
    out = noise_layer(x)
    assert out.shape == x.shape
    # 验证噪声确实被添加了
    diff = (out - x).abs().mean()
    print(f"✓ NoiseInjection: 平均差异 = {diff:.4f}")

    print("\n测试 StyleBlock...")
    block = StyleBlock(64, 128, w_dim)
    x = torch.randn(batch_size, 64, 32, 32)
    out = block(x, w)
    assert out.shape == (batch_size, 128, 32, 32)
    print(f"✓ StyleBlock: {x.shape} -> {out.shape}")

    print("\n测试风格混合...")
    w1 = mapping(torch.randn(batch_size, z_dim))
    w2 = mapping(torch.randn(batch_size, z_dim))
    w_mixed = StyleMixing.mix(w1, w2, mixing_layer=4, total_layers=8)
    assert w_mixed.shape == (8, batch_size, w_dim)
    print(f"✓ 风格混合: {w_mixed.shape}")

    # 验证混合正确
    assert torch.allclose(w_mixed[0], w1)  # 前几层是 w1
    assert torch.allclose(w_mixed[7], w2)  # 后几层是 w2
    print("✓ 混合层验证通过")

    print("\n测试截断技巧...")
    w_avg = torch.zeros(w_dim)  # 假设平均 w
    w_truncated = truncation_trick(w, w_avg, psi=0.7)
    assert w_truncated.shape == w.shape

    # 验证截断后更接近平均
    dist_original = (w - w_avg).norm()
    dist_truncated = (w_truncated - w_avg).norm()
    assert dist_truncated < dist_original
    print(f"✓ 截断后距离: {dist_original:.4f} -> {dist_truncated:.4f}")

    print("\n🎉 所有测试通过！StyleGAN 核心组件掌握完成！")


if __name__ == "__main__":
    main()
