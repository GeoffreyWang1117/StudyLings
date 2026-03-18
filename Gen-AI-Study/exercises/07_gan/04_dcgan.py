"""
练习 33: DCGAN (Deep Convolutional GAN)

DCGAN 引入了卷积架构和训练技巧，大大提升了 GAN 的稳定性。

关键设计原则：
1. 使用步长卷积代替池化
2. 在生成器和判别器中使用批归一化
3. 生成器使用 ReLU，最后一层使用 Tanh
4. 判别器使用 LeakyReLU
5. 第一层判别器和最后一层生成器不用批归一化

在这个练习中，你将学习：
- DCGAN 的架构设计
- 训练技巧
- 完整的训练循环
"""

import torch
import torch.nn as nn


class DCGANGenerator(nn.Module):
    """DCGAN 生成器"""

    def __init__(self, latent_dim=100, ngf=64, nc=1):
        """
        Args:
            latent_dim: 潜在向量维度
            ngf: 生成器特征图基数
            nc: 输出通道数
        """
        super().__init__()

        self.main = nn.Sequential(
            # 输入: (latent_dim, 1, 1)
            # TODO: 第一层 - 4x4
            nn.ConvTranspose2d(latent_dim, ngf * 8, 4, 1, 0, bias=False),
            nn.___(ngf * 8),  # 使用 BatchNorm2d
            nn.ReLU(True),

            # 4x4 -> 8x8
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.___(),  # 使用 ReLU

            # 8x8 -> 16x16
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),

            # 16x16 -> 32x32
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),

            # TODO: 最后一层 - 不用 BatchNorm
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.___()  # 使用 Tanh
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, (nn.ConvTranspose2d, nn.Conv2d)):
                nn.init.normal_(m.weight, 0.0, 0.02)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.normal_(m.weight, 1.0, 0.02)
                nn.init.constant_(m.bias, 0)

    def forward(self, z):
        # z: (batch, latent_dim) -> (batch, latent_dim, 1, 1)
        z = z.view(z.size(0), -1, 1, 1)
        return self.main(z)


class DCGANDiscriminator(nn.Module):
    """DCGAN 判别器"""

    def __init__(self, nc=1, ndf=64):
        super().__init__()

        self.main = nn.Sequential(
            # TODO: 第一层 - 不用 BatchNorm
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.___(0.2, inplace=True),  # 使用 LeakyReLU

            # 32x32 -> 16x16
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),

            # 16x16 -> 8x8
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # 8x8 -> 4x4
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),

            # TODO: 输出层
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.___()  # 使用 Sigmoid
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, 0.0, 0.02)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.normal_(m.weight, 1.0, 0.02)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        return self.main(x).view(-1, 1)


def train_dcgan_step(G, D, g_optim, d_optim, real_imgs, latent_dim, device='cpu'):
    """DCGAN 单步训练"""
    batch_size = real_imgs.size(0)
    criterion = nn.BCELoss()

    real_label = torch.ones(batch_size, 1, device=device)
    fake_label = torch.zeros(batch_size, 1, device=device)

    # ========== 训练判别器 ==========
    D.zero_grad()

    # 真实样本
    real_output = D(real_imgs)
    d_loss_real = criterion(real_output, real_label)

    # 假样本
    z = torch.randn(batch_size, latent_dim, device=device)
    fake_imgs = G(z)
    fake_output = D(fake_imgs.detach())
    d_loss_fake = criterion(fake_output, fake_label)

    # TODO: 判别器总损失
    d_loss = d_loss_real + ___  # 填入 d_loss_fake
    d_loss.backward()
    d_optim.step()

    # ========== 训练生成器 ==========
    G.zero_grad()

    fake_output = D(fake_imgs)
    # TODO: 生成器损失 - 让假样本被判为真
    g_loss = criterion(fake_output, ___)  # 填入 real_label
    g_loss.backward()
    g_optim.step()

    return d_loss.item(), g_loss.item()


def main():
    print("测试 DCGANGenerator...")
    G = DCGANGenerator(latent_dim=100, ngf=64, nc=1)
    z = torch.randn(4, 100)
    fake_imgs = G(z)
    assert fake_imgs.shape == (4, 1, 64, 64)
    print(f"✓ 生成图像形状: {fake_imgs.shape}")

    print("\n测试 DCGANDiscriminator...")
    D = DCGANDiscriminator(nc=1, ndf=64)
    out = D(fake_imgs)
    assert out.shape == (4, 1)
    print(f"✓ 判别器输出形状: {out.shape}")

    print("\n测试训练步骤...")
    g_optim = torch.optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
    d_optim = torch.optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

    real_imgs = torch.randn(4, 1, 64, 64)
    d_loss, g_loss = train_dcgan_step(G, D, g_optim, d_optim, real_imgs, 100)
    print(f"✓ D 损失: {d_loss:.4f}, G 损失: {g_loss:.4f}")

    print("\n参数统计...")
    g_params = sum(p.numel() for p in G.parameters())
    d_params = sum(p.numel() for p in D.parameters())
    print(f"  生成器参数: {g_params:,}")
    print(f"  判别器参数: {d_params:,}")

    print("\n🎉 所有测试通过！DCGAN 掌握完成！")


if __name__ == "__main__":
    main()
