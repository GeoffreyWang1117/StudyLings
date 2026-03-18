"""
练习 30: GAN 判别器

判别器的任务是区分真实样本和生成样本。它是一个二分类器。

判别器输出：
- 接近 1: 输入可能是真实样本
- 接近 0: 输入可能是假样本

在这个练习中，你将学习：
- 判别器的架构
- 卷积判别器的设计
- 输出层的选择
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleDiscriminator(nn.Module):
    """简单的 MLP 判别器"""

    def __init__(self, input_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            # TODO: 输出层
            nn.Linear(128, ___),  # 填入 1
            nn.___()  # 使用 Sigmoid
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.net(x)


class ConvDiscriminator(nn.Module):
    """卷积判别器（用于图像）"""

    def __init__(self, in_channels=1, ndf=64):
        """
        Args:
            in_channels: 输入通道数
            ndf: 判别器特征图基数
        """
        super().__init__()

        self.main = nn.Sequential(
            # 输入: (in_channels, 28, 28) for MNIST
            # TODO: 第一层不用 BatchNorm
            nn.Conv2d(in_channels, ndf, 4, 2, 1, bias=False),
            nn.___(0.2, inplace=True),  # 使用 LeakyReLU

            # TODO: 第二层
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.___(ndf * 2),  # 使用 BatchNorm2d
            nn.LeakyReLU(0.2, inplace=True),

            # 第三层
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # TODO: 输出层
            nn.Conv2d(ndf * 4, 1, 3, 1, 0, bias=False),
            nn.___()  # 使用 Sigmoid
        )

    def forward(self, x):
        return self.main(x).view(-1, 1)


class PatchDiscriminator(nn.Module):
    """
    PatchGAN 判别器

    不是对整个图像输出一个值，而是输出一个特征图，
    每个位置判断对应的图像区域是否真实。
    """

    def __init__(self, in_channels=1, ndf=64):
        super().__init__()

        self.main = nn.Sequential(
            nn.Conv2d(in_channels, ndf, 4, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(ndf, ndf * 2, 4, 2, 1),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # TODO: 输出层 - 1x1 卷积
            nn.___(ndf * 4, 1, 1, 1, 0),  # 使用 Conv2d
        )

    def forward(self, x):
        # 返回 patch 级别的判别结果
        return self.main(x)


def discriminator_loss(real_output, fake_output):
    """
    判别器损失

    目标：
    - 真实样本 -> 1
    - 假样本 -> 0
    """
    # TODO: 真实样本的损失
    real_loss = F.binary_cross_entropy_with_logits(
        real_output, torch.___(real_output)  # 使用 ones_like
    )

    # TODO: 假样本的损失
    fake_loss = F.binary_cross_entropy_with_logits(
        fake_output, torch.___(fake_output)  # 使用 zeros_like
    )

    return real_loss + fake_loss


def main():
    print("测试 SimpleDiscriminator...")
    disc = SimpleDiscriminator(input_dim=784)
    x = torch.randn(4, 1, 28, 28)
    out = disc(x)
    assert out.shape == (4, 1)
    assert (out >= 0).all() and (out <= 1).all()
    print("✓ SimpleDiscriminator 通过!")

    print("\n测试 ConvDiscriminator...")
    conv_disc = ConvDiscriminator(in_channels=1, ndf=64)
    out = conv_disc(x)
    assert out.shape == (4, 1)
    print("✓ ConvDiscriminator 通过!")

    print("\n测试 PatchDiscriminator...")
    patch_disc = PatchDiscriminator(in_channels=1, ndf=64)
    out = patch_disc(x)
    print(f"  Patch 输出形状: {out.shape}")
    print("✓ PatchDiscriminator 通过!")

    print("\n测试 discriminator_loss...")
    real_out = torch.randn(4, 1)
    fake_out = torch.randn(4, 1)
    loss = discriminator_loss(real_out, fake_out)
    assert loss.dim() == 0
    print(f"✓ discriminator_loss: {loss.item():.4f}")

    print("\n🎉 所有测试通过！GAN 判别器掌握完成！")


if __name__ == "__main__":
    main()
