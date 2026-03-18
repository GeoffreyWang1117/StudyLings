"""
练习 27: 重参数化技巧 (Reparameterization Trick)

重参数化技巧使得我们能够通过随机采样反向传播梯度。

问题：VAE 需要从 q(z|x) = N(μ, σ²) 中采样 z
但采样操作是不可导的，无法反向传播梯度。

解决方案：重参数化
z = μ + σ * ε, 其中 ε ~ N(0, 1)

这样梯度可以流过 μ 和 σ，而 ε 作为输入（不需要梯度）

在这个练习中，你将学习：
- 为什么需要重参数化
- 如何实现重参数化
- 理解梯度流动
"""

import torch
import torch.nn as nn


def sample_without_reparameterization(mu, logvar):
    """
    不使用重参数化的采样（不可导）

    这种方式无法训练，因为采样过程阻断了梯度
    """
    std = torch.exp(0.5 * logvar)
    # 直接从 N(mu, std^2) 采样 - 梯度无法传播
    z = torch.normal(mu, std)
    return z


def reparameterize(mu, logvar):
    """
    重参数化采样

    z = μ + σ * ε, 其中 ε ~ N(0, 1)

    Args:
        mu: 均值，形状 (batch_size, latent_dim)
        logvar: 对数方差，形状 (batch_size, latent_dim)
               使用 log(σ²) 而不是 σ² 是为了数值稳定性

    Returns:
        z: 采样的潜在向量
    """
    # TODO: 计算标准差
    # std = exp(0.5 * logvar) = exp(log(σ)) = σ
    std = torch.exp(___ * logvar)  # 填入 0.5

    # TODO: 从标准正态分布采样 epsilon
    eps = torch.___(mu)  # 使用 randn_like

    # TODO: 重参数化
    # z = mu + std * eps
    z = mu + ___ * eps  # 填入 std

    return z


def verify_gradient_flow():
    """
    验证重参数化后梯度可以流动
    """
    # 创建需要梯度的参数
    mu = torch.randn(4, 10, requires_grad=True)
    logvar = torch.randn(4, 10, requires_grad=True)

    # 使用重参数化采样
    z = reparameterize(mu, logvar)

    # 计算一个简单的损失
    loss = z.sum()

    # TODO: 反向传播
    loss.___()  # 调用 backward()

    # 检查梯度是否存在
    has_mu_grad = mu.grad is not None and mu.grad.abs().sum() > 0
    has_logvar_grad = logvar.grad is not None and logvar.grad.abs().sum() > 0

    return has_mu_grad, has_logvar_grad


class ReparameterizedSampler(nn.Module):
    """
    可学习的重参数化采样器

    从输入特征预测 μ 和 log(σ²)
    """

    def __init__(self, input_dim, latent_dim):
        super().__init__()

        # TODO: 预测均值的网络
        self.fc_mu = nn.Linear(input_dim, ___)  # 填入 latent_dim

        # TODO: 预测对数方差的网络
        self.fc_logvar = nn.Linear(input_dim, ___)  # 填入 latent_dim

    def forward(self, x):
        """
        Args:
            x: 输入特征，形状 (batch_size, input_dim)

        Returns:
            z: 采样的潜在向量
            mu: 均值
            logvar: 对数方差
        """
        # TODO: 预测分布参数
        mu = self.___(x)  # 调用 fc_mu
        logvar = self.___(x)  # 调用 fc_logvar

        # TODO: 重参数化采样
        z = ___(mu, logvar)  # 调用 reparameterize

        return z, mu, logvar


def understand_logvar():
    """
    理解为什么使用 log(σ²) 而不是 σ 或 σ²

    1. σ² 必须非负，但网络输出可以是任意值
       使用 logvar 可以让网络自由输出，然后 exp() 保证非负

    2. 数值稳定性：当 σ 很小时，log(σ²) 可以表示很大的负数

    3. KL 散度的计算更简单
    """
    # 假设 logvar 在 [-10, 10] 范围内
    logvar = torch.linspace(-10, 10, 100)

    # TODO: 计算对应的标准差
    std = torch.___(0.5 * logvar)  # 使用 exp

    # std 的范围是 [exp(-5), exp(5)] ≈ [0.007, 148]

    return std.min().item(), std.max().item()


def sample_latent_space():
    """
    从潜在空间采样以生成新样本

    在生成时，直接从 N(0, 1) 采样
    """
    latent_dim = 10
    num_samples = 5

    # TODO: 从标准正态分布采样潜在向量
    z = torch.___(num_samples, latent_dim)  # 使用 randn

    return z


def main():
    print("测试 reparameterize...")
    mu = torch.zeros(4, 10)
    logvar = torch.zeros(4, 10)  # σ = 1

    # 多次采样检查统计量
    samples = [reparameterize(mu, logvar) for _ in range(1000)]
    samples = torch.stack(samples)

    mean_of_samples = samples.mean(dim=0).mean()
    std_of_samples = samples.std(dim=0).mean()

    assert abs(mean_of_samples.item()) < 0.1, f"均值应接近 0，得到 {mean_of_samples.item()}"
    assert abs(std_of_samples.item() - 1.0) < 0.1, f"标准差应接近 1，得到 {std_of_samples.item()}"
    print(f"✓ 采样均值: {mean_of_samples.item():.4f}, 标准差: {std_of_samples.item():.4f}")

    print("\n验证梯度流动...")
    has_mu_grad, has_logvar_grad = verify_gradient_flow()
    assert has_mu_grad, "μ 应该有梯度"
    assert has_logvar_grad, "logvar 应该有梯度"
    print("✓ 梯度可以正确流动!")

    print("\n测试 ReparameterizedSampler...")
    sampler = ReparameterizedSampler(input_dim=64, latent_dim=10)
    x = torch.randn(4, 64)
    z, mu, logvar = sampler(x)
    assert z.shape == (4, 10)
    assert mu.shape == (4, 10)
    assert logvar.shape == (4, 10)
    print("✓ ReparameterizedSampler 通过!")

    print("\n理解 logvar...")
    std_min, std_max = understand_logvar()
    print(f"  logvar ∈ [-10, 10] 对应 std ∈ [{std_min:.4f}, {std_max:.2f}]")

    print("\n测试潜在空间采样...")
    z = sample_latent_space()
    assert z.shape == (5, 10)
    print("✓ sample_latent_space 通过!")

    print("\n🎉 所有测试通过！重参数化技巧掌握完成！")


if __name__ == "__main__":
    main()
