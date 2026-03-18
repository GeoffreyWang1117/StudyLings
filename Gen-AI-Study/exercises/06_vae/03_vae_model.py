"""
练习 29: 完整 VAE 模型

实现完整的变分自编码器，能够生成新的图像样本。

VAE 架构:
编码器: x -> (μ, logσ²)
采样: z ~ N(μ, σ²) (使用重参数化)
解码器: z -> x_recon

在这个练习中，你将学习：
- 完整 VAE 的实现
- 训练循环
- 从潜在空间采样生成
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def reparameterize(mu, logvar):
    """重参数化采样"""
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)
    return mu + std * eps


class VAE(nn.Module):
    """完整的 VAE 模型"""

    def __init__(self, in_channels=1, latent_dim=20):
        super().__init__()

        self.latent_dim = latent_dim

        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 32, 4, 2, 1),  # 14x14
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2, 1),  # 7x7
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, 2, 1),  # 3x3 (向下取整)
            nn.ReLU(),
        )

        # TODO: μ 和 logvar 的投影层
        self.fc_mu = nn.Linear(128 * 3 * 3, ___)  # 填入 latent_dim
        self.fc_logvar = nn.Linear(128 * 3 * 3, ___)  # 填入 latent_dim

        # 解码器
        self.fc_decode = nn.Linear(latent_dim, 128 * 3 * 3)

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, 2, 1),  # 6x6
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, 2, 0),  # 14x14
            nn.ReLU(),
            nn.ConvTranspose2d(32, in_channels, 4, 2, 1),  # 28x28
            nn.___(),  # 使用 Sigmoid
        )

    def encode(self, x):
        """编码到潜在分布参数"""
        h = self.encoder(x)
        h = h.view(h.size(0), -1)

        # TODO: 预测 μ 和 logvar
        mu = self.___(h)  # 调用 fc_mu
        logvar = self.___(h)  # 调用 fc_logvar

        return mu, logvar

    def decode(self, z):
        """从潜在向量解码"""
        h = self.fc_decode(z)
        h = h.view(h.size(0), 128, 3, 3)
        return self.decoder(h)

    def forward(self, x):
        # TODO: 编码
        mu, logvar = self.___(x)

        # TODO: 重参数化采样
        z = ___(mu, logvar)  # 调用 reparameterize

        # TODO: 解码
        x_recon = self.___(z)

        return x_recon, mu, logvar

    @torch.no_grad()
    def sample(self, num_samples, device='cpu'):
        """从潜在空间采样生成新图像"""
        # TODO: 从标准正态分布采样
        z = torch.___(num_samples, self.latent_dim, device=device)

        # TODO: 解码
        samples = self.___(z)

        return samples


def vae_loss(x_recon, x, mu, logvar, beta=1.0):
    """VAE 损失"""
    # 重建损失
    recon_loss = F.binary_cross_entropy(x_recon, x, reduction='sum')

    # KL 散度
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return (recon_loss + beta * kl_loss) / x.size(0)


def train_step(model, optimizer, x, beta=1.0):
    """单步训练"""
    model.train()
    optimizer.zero_grad()

    # TODO: 前向传播
    x_recon, mu, logvar = ___(x)  # 调用 model

    # TODO: 计算损失
    loss = ___(x_recon, x, mu, logvar, beta)  # 调用 vae_loss

    # TODO: 反向传播
    loss.___()

    # TODO: 更新参数
    optimizer.___()

    return loss.item()


@torch.no_grad()
def interpolate_latent(model, x1, x2, steps=10):
    """在两个图像的潜在表示之间插值"""
    model.eval()

    # 编码
    mu1, _ = model.encode(x1)
    mu2, _ = model.encode(x2)

    # TODO: 线性插值
    interpolations = []
    for alpha in torch.linspace(0, 1, steps):
        z = (1 - ___) * mu1 + ___ * mu2  # 填入 alpha
        img = model.decode(z)
        interpolations.append(img)

    return torch.cat(interpolations, dim=0)


def main():
    print("测试 VAE 模型...")
    vae = VAE(in_channels=1, latent_dim=20)
    x = torch.rand(4, 1, 28, 28)

    x_recon, mu, logvar = vae(x)
    assert x_recon.shape == x.shape
    assert mu.shape == (4, 20)
    assert logvar.shape == (4, 20)
    print(f"✓ VAE 前向传播通过!")

    print("\n测试损失计算...")
    loss = vae_loss(x_recon, x, mu, logvar)
    assert loss.dim() == 0
    print(f"✓ VAE 损失: {loss.item():.4f}")

    print("\n测试训练步骤...")
    optimizer = torch.optim.Adam(vae.parameters(), lr=1e-3)
    loss = train_step(vae, optimizer, x)
    print(f"✓ 训练步骤完成，损失: {loss:.4f}")

    print("\n测试采样...")
    samples = vae.sample(8)
    assert samples.shape == (8, 1, 28, 28)
    assert samples.min() >= 0 and samples.max() <= 1
    print(f"✓ 成功生成 8 个样本!")

    print("\n测试潜在空间插值...")
    x1 = torch.rand(1, 1, 28, 28)
    x2 = torch.rand(1, 1, 28, 28)
    interp = interpolate_latent(vae, x1, x2, steps=5)
    assert interp.shape == (5, 1, 28, 28)
    print(f"✓ 潜在空间插值通过!")

    print("\n参数统计...")
    num_params = sum(p.numel() for p in vae.parameters())
    print(f"  VAE 参数: {num_params:,}")

    print("\n🎉 所有测试通过！VAE 模型掌握完成！")


if __name__ == "__main__":
    main()
