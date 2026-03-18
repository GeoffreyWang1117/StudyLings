"""
练习 26: 自编码器 (Autoencoder)

自编码器学习数据的压缩表示，由编码器和解码器组成。
- 编码器：将输入压缩到低维潜在空间
- 解码器：从潜在空间重建输入

训练目标：最小化输入和重建之间的差异

应用：
- 特征学习
- 降维
- 去噪
- 图像压缩

在这个练习中，你将学习：
- 自编码器的结构
- 编码器和解码器的对称设计
- 瓶颈层的作用
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    """
    编码器：将图像压缩到潜在空间
    """

    def __init__(self, in_channels=1, latent_dim=128):
        """
        Args:
            in_channels: 输入图像通道数
            latent_dim: 潜在空间维度
        """
        super().__init__()

        # 卷积层逐步下采样
        # 输入: (B, in_channels, 28, 28)

        # TODO: 第一个卷积块
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 32, 3, stride=2, padding=1),  # -> 14x14
            nn.BatchNorm2d(32),
            nn.___()  # 使用 ReLU
        )

        # TODO: 第二个卷积块
        self.conv2 = nn.Sequential(
            nn.___(32, 64, 3, stride=2, padding=1),  # -> 7x7，使用 Conv2d
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        # 展平并映射到潜在空间
        # 7 * 7 * 64 = 3136
        self.fc = nn.Linear(7 * 7 * 64, latent_dim)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)

        # TODO: 展平
        x = x.view(x.size(0), ___)  # 填入 -1

        # TODO: 映射到潜在空间
        z = self.___(x)  # 调用 fc

        return z


class Decoder(nn.Module):
    """
    解码器：从潜在空间重建图像
    """

    def __init__(self, out_channels=1, latent_dim=128):
        super().__init__()

        # 从潜在空间映射回特征图
        self.fc = nn.Linear(latent_dim, 7 * 7 * 64)

        # 转置卷积逐步上采样
        # TODO: 第一个转置卷积块
        self.deconv1 = nn.Sequential(
            nn.___(64, 32, 4, stride=2, padding=1),  # -> 14x14，使用 ConvTranspose2d
            nn.BatchNorm2d(32),
            nn.ReLU()
        )

        # TODO: 第二个转置卷积块（输出层）
        self.deconv2 = nn.Sequential(
            nn.ConvTranspose2d(32, out_channels, 4, stride=2, padding=1),  # -> 28x28
            nn.___()  # 使用 Sigmoid，将输出归一化到 [0, 1]
        )

    def forward(self, z):
        # TODO: 从潜在空间映射
        x = self.fc(z)

        # TODO: 重塑为特征图
        x = x.view(x.size(0), 64, ___, ___)  # 填入 7, 7

        # 上采样重建
        x = self.deconv1(x)
        x = self.deconv2(x)

        return x


class Autoencoder(nn.Module):
    """
    完整的自编码器
    """

    def __init__(self, in_channels=1, latent_dim=128):
        super().__init__()

        # TODO: 创建编码器和解码器
        self.encoder = ___(in_channels, latent_dim)  # 使用 Encoder
        self.decoder = ___(in_channels, latent_dim)  # 使用 Decoder

    def forward(self, x):
        # TODO: 编码
        z = self.___(x)

        # TODO: 解码
        x_recon = self.___(z)

        return x_recon, z

    def encode(self, x):
        """只进行编码"""
        return self.encoder(x)

    def decode(self, z):
        """只进行解码"""
        return self.decoder(z)


def reconstruction_loss(x_recon, x):
    """
    计算重建损失

    常用选择：
    - MSE (Mean Squared Error): 适合一般图像
    - BCE (Binary Cross Entropy): 适合二值图像或像素值在 [0,1] 的图像
    """
    # TODO: 使用 MSE 损失
    loss = F.___(x_recon, x)  # 使用 mse_loss

    return loss


class DenoisingAutoencoder(nn.Module):
    """
    去噪自编码器

    训练时在输入上添加噪声，目标是重建干净的输入。
    这迫使模型学习更鲁棒的特征。
    """

    def __init__(self, in_channels=1, latent_dim=128, noise_factor=0.3):
        super().__init__()

        self.noise_factor = noise_factor
        self.encoder = Encoder(in_channels, latent_dim)
        self.decoder = Decoder(in_channels, latent_dim)

    def add_noise(self, x):
        """添加高斯噪声"""
        if self.training:
            # TODO: 添加噪声
            noise = torch.___(x)  # 使用 randn_like
            noisy_x = x + self.noise_factor * noise
            # 裁剪到 [0, 1]
            noisy_x = torch.clamp(noisy_x, 0, 1)
            return noisy_x
        return x

    def forward(self, x):
        # 训练时添加噪声
        x_noisy = self.add_noise(x)

        # 编码噪声输入
        z = self.encoder(x_noisy)

        # 解码重建
        x_recon = self.decoder(z)

        # 返回重建结果（目标是原始干净图像）
        return x_recon, z


def visualize_latent_space():
    """
    可视化潜在空间

    好的自编码器应该学到有意义的潜在表示：
    - 相似的输入应该有相似的潜在向量
    - 潜在空间应该是连续的
    """
    # 创建模型
    ae = Autoencoder(in_channels=1, latent_dim=2)  # 2D 潜在空间便于可视化

    # 模拟一些不同类别的输入
    # 在实际应用中，应该用真实数据
    class_0 = torch.randn(10, 1, 28, 28) * 0.5
    class_1 = torch.randn(10, 1, 28, 28) * 0.5 + 1

    # 编码
    with torch.no_grad():
        z_0 = ae.encode(class_0)
        z_1 = ae.encode(class_1)

    # 潜在向量的统计
    mean_0 = z_0.mean(dim=0)
    mean_1 = z_1.mean(dim=0)

    # TODO: 计算两类之间的距离
    distance = torch.sqrt(((mean_0 - mean_1) ** ___).sum())  # 填入 2

    return distance.item()


def main():
    print("测试 Encoder...")
    encoder = Encoder(in_channels=1, latent_dim=128)
    x = torch.randn(4, 1, 28, 28)
    z = encoder(x)
    assert z.shape == (4, 128), f"期望 (4, 128)，得到 {z.shape}"
    print("✓ Encoder 通过!")

    print("\n测试 Decoder...")
    decoder = Decoder(out_channels=1, latent_dim=128)
    x_recon = decoder(z)
    assert x_recon.shape == (4, 1, 28, 28), f"期望 (4, 1, 28, 28)，得到 {x_recon.shape}"
    print("✓ Decoder 通过!")

    print("\n测试 Autoencoder...")
    ae = Autoencoder(in_channels=1, latent_dim=128)
    x_recon, z = ae(x)
    assert x_recon.shape == x.shape
    assert z.shape == (4, 128)
    print("✓ Autoencoder 通过!")

    print("\n测试 reconstruction_loss...")
    loss = reconstruction_loss(x_recon, (x + 1) / 2)  # 归一化到 [0,1]
    assert loss.dim() == 0, "损失应该是标量"
    assert loss.item() > 0, "损失应该是正数"
    print(f"✓ reconstruction_loss 通过! 损失: {loss.item():.4f}")

    print("\n测试 DenoisingAutoencoder...")
    dae = DenoisingAutoencoder(in_channels=1, latent_dim=128, noise_factor=0.3)
    dae.train()
    x_normalized = (x + 1) / 2  # 归一化到 [0,1]
    x_recon, z = dae(x_normalized)
    assert x_recon.shape == x.shape
    print("✓ DenoisingAutoencoder 通过!")

    print("\n测试潜在空间...")
    distance = visualize_latent_space()
    print(f"✓ 两类潜在向量之间的距离: {distance:.4f}")

    print("\n参数统计...")
    num_params = sum(p.numel() for p in ae.parameters())
    print(f"  Autoencoder 参数: {num_params:,}")

    print("\n🎉 所有测试通过！自编码器掌握完成！")


if __name__ == "__main__":
    main()
