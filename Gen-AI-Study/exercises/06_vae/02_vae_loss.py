"""
练习 28: VAE 损失函数

VAE 的损失函数由两部分组成：
1. 重建损失：衡量重建质量
2. KL 散度：将潜在分布正则化到标准正态分布

总损失 = 重建损失 + β * KL 散度

ELBO (Evidence Lower Bound):
L = E_q[log p(x|z)] - KL(q(z|x) || p(z))
  = -重建损失 - KL散度

在这个练习中，你将学习：
- KL 散度的推导和实现
- β-VAE 的概念
- 损失的各部分作用
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def kl_divergence(mu, logvar):
    """
    计算 KL 散度: KL(q(z|x) || p(z))

    其中 q(z|x) = N(μ, σ²), p(z) = N(0, 1)

    公式推导：
    KL(N(μ,σ²) || N(0,1))
    = -0.5 * Σ(1 + log(σ²) - μ² - σ²)
    = -0.5 * Σ(1 + logvar - μ² - exp(logvar))

    Args:
        mu: 均值，形状 (batch_size, latent_dim)
        logvar: 对数方差

    Returns:
        kl: KL 散度，形状 (batch_size,)
    """
    # TODO: 实现 KL 散度
    # KL = -0.5 * sum(1 + logvar - mu^2 - exp(logvar))
    kl = -0.5 * torch.sum(
        1 + logvar - mu.___(2) - logvar.___(),  # 填入 pow 和 exp
        dim=-1
    )

    return kl


def reconstruction_loss_bce(x_recon, x):
    """
    二元交叉熵重建损失

    适用于像素值在 [0, 1] 范围的图像
    """
    # TODO: 计算 BCE 损失
    # reduction='none' 保留每个像素的损失，然后手动求和
    loss = F.___(x_recon, x, reduction='none')  # 使用 binary_cross_entropy

    # 对空间维度求和，对 batch 求平均
    loss = loss.sum(dim=[1, 2, 3])  # 对 C, H, W 求和

    return loss


def reconstruction_loss_mse(x_recon, x):
    """
    MSE 重建损失

    适用于一般图像
    """
    # TODO: 计算 MSE 损失
    loss = F.___(x_recon, x, reduction='none')  # 使用 mse_loss

    # 对空间维度求和
    loss = loss.sum(dim=[1, 2, 3])

    return loss


def vae_loss(x_recon, x, mu, logvar, beta=1.0, recon_type='bce'):
    """
    完整的 VAE 损失

    Args:
        x_recon: 重建图像
        x: 原始图像
        mu: 潜在分布均值
        logvar: 潜在分布对数方差
        beta: KL 散度的权重（β-VAE）
        recon_type: 重建损失类型 ('bce' 或 'mse')

    Returns:
        total_loss: 总损失
        recon_loss: 重建损失
        kl_loss: KL 散度
    """
    # 重建损失
    if recon_type == 'bce':
        recon_loss = reconstruction_loss_bce(x_recon, x)
    else:
        recon_loss = reconstruction_loss_mse(x_recon, x)

    # TODO: 计算 KL 散度
    kl_loss = ___(mu, logvar)  # 调用 kl_divergence

    # TODO: 总损失
    total_loss = recon_loss + ___ * kl_loss  # 填入 beta

    # 对 batch 求平均
    return total_loss.mean(), recon_loss.mean(), kl_loss.mean()


def understand_beta_vae():
    """
    理解 β-VAE

    β > 1: 更强的正则化，潜在空间更连续但重建质量可能下降
    β < 1: 更好的重建质量但潜在空间可能不够规则
    β = 1: 标准 VAE

    β-VAE 可以学到更解纠缠的表示
    """
    # 模拟不同 β 的效果
    mu = torch.randn(32, 10)
    logvar = torch.randn(32, 10)

    kl = kl_divergence(mu, logvar).mean()

    results = {}
    for beta in [0.1, 1.0, 5.0, 10.0]:
        # TODO: 计算带权重的 KL
        weighted_kl = beta * ___  # 填入 kl
        results[beta] = weighted_kl.item()

    return results


class VAELoss(nn.Module):
    """
    VAE 损失模块
    """

    def __init__(self, beta=1.0, recon_type='bce'):
        super().__init__()

        self.beta = beta
        self.recon_type = recon_type

    def forward(self, x_recon, x, mu, logvar):
        return vae_loss(x_recon, x, mu, logvar, self.beta, self.recon_type)


def kl_annealing_schedule(epoch, warmup_epochs=10, method='linear'):
    """
    KL 退火策略

    在训练初期使用较小的 β，逐渐增加到目标值
    这有助于稳定训练

    Args:
        epoch: 当前 epoch
        warmup_epochs: 预热 epoch 数
        method: 退火方法 ('linear', 'cyclical')
    """
    if method == 'linear':
        # TODO: 线性增加 β
        beta = min(1.0, epoch / ___)  # 填入 warmup_epochs
    elif method == 'cyclical':
        # 周期性增加和重置
        cycle = epoch % warmup_epochs
        beta = cycle / warmup_epochs
    else:
        beta = 1.0

    return beta


def main():
    print("测试 kl_divergence...")
    # 当 q = p = N(0,1) 时，KL 应该为 0
    mu_zero = torch.zeros(4, 10)
    logvar_zero = torch.zeros(4, 10)
    kl = kl_divergence(mu_zero, logvar_zero)
    assert kl.abs().mean() < 1e-5, f"KL(N(0,1)||N(0,1)) 应该接近 0，得到 {kl.mean()}"
    print("✓ kl_divergence 基本测试通过!")

    # 当 q 偏离 p 时，KL 应该为正
    mu_shifted = torch.ones(4, 10) * 2
    kl_shifted = kl_divergence(mu_shifted, logvar_zero)
    assert kl_shifted.mean() > 0, "KL 应该为正"
    print(f"✓ 偏移后 KL = {kl_shifted.mean():.4f}")

    print("\n测试重建损失...")
    x = torch.rand(4, 1, 28, 28)  # [0, 1] 范围
    x_recon = torch.rand(4, 1, 28, 28)

    bce_loss = reconstruction_loss_bce(x_recon, x)
    assert bce_loss.shape == (4,)
    print(f"✓ BCE 重建损失: {bce_loss.mean().item():.4f}")

    mse_loss = reconstruction_loss_mse(x_recon, x)
    assert mse_loss.shape == (4,)
    print(f"✓ MSE 重建损失: {mse_loss.mean().item():.4f}")

    print("\n测试 vae_loss...")
    mu = torch.randn(4, 10)
    logvar = torch.randn(4, 10)
    total, recon, kl = vae_loss(x_recon, x, mu, logvar, beta=1.0)
    print(f"✓ 总损失: {total.item():.4f}, 重建: {recon.item():.4f}, KL: {kl.item():.4f}")

    print("\n测试 β-VAE...")
    beta_results = understand_beta_vae()
    for beta, weighted_kl in beta_results.items():
        print(f"  β={beta}: 加权 KL = {weighted_kl:.4f}")

    print("\n测试 KL 退火...")
    for epoch in [0, 5, 10, 15]:
        beta = kl_annealing_schedule(epoch, warmup_epochs=10)
        print(f"  Epoch {epoch}: β = {beta:.2f}")

    print("\n🎉 所有测试通过！VAE 损失函数掌握完成！")


if __name__ == "__main__":
    main()
