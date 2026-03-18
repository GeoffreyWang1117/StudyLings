"""
练习 34: 谱归一化 (Spectral Normalization)

谱归一化通过约束权重的谱范数来稳定 GAN 训练。
确保判别器满足 Lipschitz 连续性约束。

谱范数是权重矩阵的最大奇异值。
谱归一化: W_norm = W / σ(W)

在这个练习中，你将学习：
- 谱归一化的原理
- 幂迭代法估计谱范数
- PyTorch 的谱归一化实现
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def power_iteration(W, u, num_iters=1):
    """
    幂迭代法估计最大奇异值

    σ(W) = max_u ||Wu|| / ||u||

    Args:
        W: 权重矩阵，形状 (out_features, in_features)
        u: 左奇异向量估计，形状 (out_features,)
        num_iters: 迭代次数

    Returns:
        sigma: 估计的谱范数
        u: 更新后的左奇异向量
    """
    for _ in range(num_iters):
        # v = W^T u / ||W^T u||
        # TODO: 计算 v
        v = torch.matmul(W.t(), u)
        v = v / v.norm()

        # u = W v / ||W v||
        # TODO: 计算 u
        u = torch.matmul(___, v)  # 填入 W
        u = u / u.___()  # 使用 norm()

    # TODO: 计算谱范数
    # σ = u^T W v
    sigma = torch.dot(u, torch.matmul(W, v))

    return sigma, u


class SpectralNorm(nn.Module):
    """谱归一化层"""

    def __init__(self, module, name='weight', num_iters=1):
        super().__init__()

        self.module = module
        self.name = name
        self.num_iters = num_iters

        # 获取权重形状
        weight = getattr(module, name)
        height = weight.shape[0]

        # TODO: 初始化左奇异向量
        u = torch.___(height)  # 使用 randn
        u = u / u.norm()

        # 注册为 buffer
        self.register_buffer('u', u)

    def forward(self, *args, **kwargs):
        # 获取权重
        weight = getattr(self.module, self.name)

        # 重塑为 2D
        W = weight.view(weight.shape[0], -1)

        # TODO: 幂迭代估计谱范数
        sigma, u = ___(W, self.u, self.num_iters)  # 调用 power_iteration

        # 更新 u
        self.u.copy_(u)

        # TODO: 归一化权重
        W_norm = weight / ___  # 填入 sigma

        # 临时替换权重
        setattr(self.module, self.name, W_norm)

        # 前向传播
        output = self.module(*args, **kwargs)

        # 恢复原始权重
        setattr(self.module, self.name, weight)

        return output


def apply_spectral_norm(module):
    """
    对模块应用 PyTorch 的谱归一化

    PyTorch 提供了 torch.nn.utils.spectral_norm
    """
    from torch.nn.utils import spectral_norm

    # TODO: 应用谱归一化
    return ___(module)  # 调用 spectral_norm


class SNDiscriminator(nn.Module):
    """使用谱归一化的判别器"""

    def __init__(self, nc=1, ndf=64):
        super().__init__()

        self.main = nn.Sequential(
            # TODO: 对每层应用谱归一化
            apply_spectral_norm(nn.Conv2d(nc, ndf, 4, 2, 1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),

            apply_spectral_norm(nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),

            apply_spectral_norm(nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),

            apply_spectral_norm(nn.Conv2d(ndf * 4, 1, 4, 1, 0, bias=False)),
        )

    def forward(self, x):
        return self.main(x).view(-1, 1)


def main():
    print("测试 power_iteration...")
    W = torch.randn(10, 5)
    u = torch.randn(10)
    u = u / u.norm()

    sigma, u_new = power_iteration(W, u, num_iters=10)

    # 与 SVD 结果对比
    _, s, _ = torch.svd(W)
    actual_sigma = s[0]

    print(f"  幂迭代估计: {sigma.item():.4f}")
    print(f"  SVD 真实值: {actual_sigma.item():.4f}")
    assert abs(sigma.item() - actual_sigma.item()) < 0.1
    print("✓ power_iteration 通过!")

    print("\n测试 apply_spectral_norm...")
    conv = nn.Conv2d(3, 16, 3, 1, 1)
    conv_sn = apply_spectral_norm(nn.Conv2d(3, 16, 3, 1, 1))
    x = torch.randn(1, 3, 28, 28)
    out = conv_sn(x)
    assert out.shape == (1, 16, 28, 28)
    print("✓ apply_spectral_norm 通过!")

    print("\n测试 SNDiscriminator...")
    disc = SNDiscriminator(nc=1, ndf=64)
    x = torch.randn(4, 1, 32, 32)
    out = disc(x)
    assert out.shape == (4, 1)
    print("✓ SNDiscriminator 通过!")

    print("\n🎉 所有测试通过！谱归一化掌握完成！")


if __name__ == "__main__":
    main()
