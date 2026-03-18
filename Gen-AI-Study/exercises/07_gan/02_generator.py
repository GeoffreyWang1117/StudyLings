"""
练习 31: GAN 生成器

生成器从随机噪声生成假样本，试图欺骗判别器。

生成器架构要点：
- 输入: 低维随机噪声 z
- 输出: 与真实数据同维度的生成样本

在这个练习中，你将学习：
- 生成器的架构设计
- 转置卷积上采样
- 批归一化的使用
"""

import torch
import torch.nn as nn


class SimpleGenerator(nn.Module):
    """简单的 MLP 生成器"""

    def __init__(self, latent_dim, output_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            # TODO: 输出层
            nn.Linear(512, ___),  # 填入 output_dim
            nn.___()  # 使用 Tanh，输出范围 [-1, 1]
        )

    def forward(self, z):
        return self.net(z)


class ConvGenerator(nn.Module):
    """卷积生成器（用于图像）"""

    def __init__(self, latent_dim=100, out_channels=1, ngf=64):
        """
        Args:
            latent_dim: 潜在向量维度
            out_channels: 输出通道数
            ngf: 生成器特征图基数
        """
        super().__init__()

        self.latent_dim = latent_dim

        # TODO: 从潜在向量到初始特征图
        self.fc = nn.Linear(latent_dim, ngf * 8 * 4 * 4)

        self.main = nn.Sequential(
            # 4x4 -> 7x7
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.___(ngf * 4),  # 使用 BatchNorm2d
            nn.ReLU(True),

            # 7x7 -> 14x14
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.___(),  # 使用 ReLU

            # TODO: 14x14 -> 28x28
            nn.ConvTranspose2d(ngf * 2, out_channels, 4, 2, 1, bias=False),
            nn.___()  # 使用 Tanh
        )

    def forward(self, z):
        # TODO: 从潜在向量生成初始特征图
        x = self.___(z)  # 调用 fc
        x = x.view(x.size(0), -1, 4, 4)
        return self.main(x)


class CondGenerator(nn.Module):
    """条件生成器（Conditional Generator）"""

    def __init__(self, latent_dim=100, num_classes=10, out_channels=1, ngf=64):
        super().__init__()

        self.latent_dim = latent_dim
        self.num_classes = num_classes

        # TODO: 类别嵌入
        self.label_emb = nn.___(num_classes, num_classes)  # 使用 Embedding

        # 输入维度 = latent_dim + num_classes
        self.fc = nn.Linear(latent_dim + num_classes, ngf * 8 * 4 * 4)

        self.main = nn.Sequential(
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf * 2, out_channels, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, z, labels):
        # TODO: 获取类别嵌入
        c = self.___(labels)  # 调用 label_emb

        # TODO: 拼接噪声和类别
        x = torch.cat([z, c], dim=___)  # 填入 1 或 -1

        x = self.fc(x)
        x = x.view(x.size(0), -1, 4, 4)
        return self.main(x)


def sample_noise(batch_size, latent_dim, device='cpu'):
    """采样噪声向量"""
    # TODO: 从标准正态分布采样
    return torch.___(batch_size, latent_dim, device=device)  # 使用 randn


def main():
    print("测试 SimpleGenerator...")
    gen = SimpleGenerator(latent_dim=100, output_dim=784)
    z = torch.randn(4, 100)
    out = gen(z)
    assert out.shape == (4, 784)
    assert (out >= -1).all() and (out <= 1).all()
    print("✓ SimpleGenerator 通过!")

    print("\n测试 ConvGenerator...")
    conv_gen = ConvGenerator(latent_dim=100, out_channels=1, ngf=64)
    z = torch.randn(4, 100)
    out = conv_gen(z)
    assert out.shape == (4, 1, 28, 28), f"期望 (4, 1, 28, 28)，得到 {out.shape}"
    print("✓ ConvGenerator 通过!")

    print("\n测试 CondGenerator...")
    cond_gen = CondGenerator(latent_dim=100, num_classes=10)
    z = torch.randn(4, 100)
    labels = torch.randint(0, 10, (4,))
    out = cond_gen(z, labels)
    assert out.shape == (4, 1, 28, 28)
    print("✓ CondGenerator 通过!")

    print("\n测试 sample_noise...")
    noise = sample_noise(8, 100)
    assert noise.shape == (8, 100)
    print("✓ sample_noise 通过!")

    print("\n🎉 所有测试通过！GAN 生成器掌握完成！")


if __name__ == "__main__":
    main()
