"""
练习 32: GAN 损失函数

GAN 的训练是一个极小极大博弈 (minimax game)。

原始 GAN 目标:
min_G max_D V(D,G) = E[log D(x)] + E[log(1-D(G(z)))]

判别器目标：最大化 V
- 真实样本得分高 (D(x) -> 1)
- 假样本得分低 (D(G(z)) -> 0)

生成器目标：最小化 V（或最大化 E[log D(G(z))]）
- 让判别器无法区分假样本

在这个练习中，你将学习：
- 原始 GAN 损失
- 非饱和 GAN 损失
- Wasserstein GAN 损失
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def discriminator_loss_original(real_scores, fake_scores):
    """
    原始 GAN 判别器损失

    L_D = -E[log D(x)] - E[log(1 - D(G(z)))]
        = BCE(D(x), 1) + BCE(D(G(z)), 0)
    """
    # TODO: 真实样本损失
    real_loss = F.binary_cross_entropy_with_logits(
        real_scores, torch.___(real_scores)  # 使用 ones_like
    )

    # TODO: 假样本损失
    fake_loss = F.binary_cross_entropy_with_logits(
        fake_scores, torch.___(fake_scores)  # 使用 zeros_like
    )

    return real_loss + fake_loss


def generator_loss_original(fake_scores):
    """
    原始 GAN 生成器损失

    L_G = E[log(1 - D(G(z)))]

    但这个损失在 D 很强时梯度很小，导致训练不稳定
    """
    return F.binary_cross_entropy_with_logits(
        fake_scores, torch.zeros_like(fake_scores)
    )


def generator_loss_nonsaturating(fake_scores):
    """
    非饱和 GAN 生成器损失（常用）

    L_G = -E[log D(G(z))]
        = BCE(D(G(z)), 1)

    这个损失在 D 很强时仍有较大梯度
    """
    # TODO: 让假样本被判为真
    return F.___(
        fake_scores, torch.ones_like(fake_scores)
    )  # 使用 binary_cross_entropy_with_logits


def discriminator_loss_wgan(real_scores, fake_scores):
    """
    Wasserstein GAN 判别器（critic）损失

    L_D = E[D(G(z))] - E[D(x)]

    最大化真假样本得分之差
    """
    # TODO: WGAN 判别器损失
    # 注意：WGAN 中判别器输出不需要 sigmoid
    return fake_scores.___ - real_scores.mean()  # 使用 mean()


def generator_loss_wgan(fake_scores):
    """
    Wasserstein GAN 生成器损失

    L_G = -E[D(G(z))]

    最大化假样本的得分
    """
    # TODO: WGAN 生成器损失
    return -fake_scores.___()  # 使用 mean()


def gradient_penalty(discriminator, real, fake, device='cpu'):
    """
    WGAN-GP 梯度惩罚

    确保判别器满足 1-Lipschitz 约束
    penalty = E[(||∇D(x̂)||_2 - 1)^2]
    """
    batch_size = real.size(0)

    # TODO: 随机插值系数
    alpha = torch.rand(batch_size, 1, 1, 1, device=device)

    # TODO: 插值样本
    interpolated = alpha * real + (1 - ___) * fake  # 填入 alpha
    interpolated.requires_grad_(True)

    # 判别器输出
    d_interpolated = discriminator(interpolated)

    # TODO: 计算梯度
    gradients = torch.autograd.grad(
        outputs=d_interpolated,
        inputs=interpolated,
        grad_outputs=torch.ones_like(d_interpolated),
        create_graph=True,
        retain_graph=True
    )[0]

    # TODO: 计算梯度范数
    gradients = gradients.view(batch_size, -1)
    gradient_norm = gradients.norm(2, dim=___)  # 填入 1

    # 惩罚：(||∇D|| - 1)^2
    penalty = ((gradient_norm - 1) ** 2).mean()

    return penalty


class GANLoss:
    """GAN 损失类"""

    def __init__(self, loss_type='nonsaturating'):
        self.loss_type = loss_type

    def discriminator_loss(self, real_scores, fake_scores):
        if self.loss_type == 'wgan':
            return discriminator_loss_wgan(real_scores, fake_scores)
        else:
            return discriminator_loss_original(real_scores, fake_scores)

    def generator_loss(self, fake_scores):
        if self.loss_type == 'wgan':
            return generator_loss_wgan(fake_scores)
        elif self.loss_type == 'nonsaturating':
            return generator_loss_nonsaturating(fake_scores)
        else:
            return generator_loss_original(fake_scores)


def main():
    print("测试 discriminator_loss_original...")
    real = torch.randn(4, 1)
    fake = torch.randn(4, 1)
    loss = discriminator_loss_original(real, fake)
    assert loss.dim() == 0
    print(f"✓ D 损失: {loss.item():.4f}")

    print("\n测试 generator_loss_nonsaturating...")
    loss = generator_loss_nonsaturating(fake)
    print(f"✓ G 损失: {loss.item():.4f}")

    print("\n测试 WGAN 损失...")
    d_loss = discriminator_loss_wgan(real, fake)
    g_loss = generator_loss_wgan(fake)
    print(f"✓ WGAN D 损失: {d_loss.item():.4f}")
    print(f"✓ WGAN G 损失: {g_loss.item():.4f}")

    print("\n测试 gradient_penalty...")
    disc = nn.Sequential(
        nn.Conv2d(1, 16, 3, 1, 1),
        nn.LeakyReLU(0.2),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(16, 1)
    )
    real_imgs = torch.randn(4, 1, 28, 28)
    fake_imgs = torch.randn(4, 1, 28, 28)
    gp = gradient_penalty(disc, real_imgs, fake_imgs)
    print(f"✓ 梯度惩罚: {gp.item():.4f}")

    print("\n🎉 所有测试通过！GAN 损失函数掌握完成！")


if __name__ == "__main__":
    main()
