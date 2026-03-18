"""
练习 36: 前向扩散 (Forward Diffusion)

前向扩散过程逐步向数据添加高斯噪声，直到变成纯噪声。

数学公式：
q(x_t|x_0) = N(x_t; √ᾱ_t * x_0, (1-ᾱ_t) * I)

可以一步计算任意时间步：
x_t = √ᾱ_t * x_0 + √(1-ᾱ_t) * ε, 其中 ε ~ N(0, I)

在这个练习中，你将学习：
- 前向扩散的实现
- 一步采样 x_t
- 理解噪声如何逐步累积
"""

import torch
import torch.nn as nn


def forward_diffusion_sample(x_0, t, sqrt_alpha_bar, sqrt_one_minus_alpha_bar):
    """
    从 x_0 直接采样任意时间步 t 的 x_t

    x_t = √ᾱ_t * x_0 + √(1-ᾱ_t) * ε

    Args:
        x_0: 原始数据，形状 (batch_size, ...)
        t: 时间步索引，形状 (batch_size,)
        sqrt_alpha_bar: √ᾱ 序列
        sqrt_one_minus_alpha_bar: √(1-ᾱ) 序列

    Returns:
        x_t: 加噪后的数据
        noise: 添加的噪声
    """
    # TODO: 采样噪声
    noise = torch.___(x_0)  # 使用 randn_like

    # 获取对应时间步的系数
    # 需要调整形状以便广播
    sqrt_alpha_bar_t = sqrt_alpha_bar[t]
    sqrt_one_minus_alpha_bar_t = sqrt_one_minus_alpha_bar[t]

    # 调整形状: (batch,) -> (batch, 1, 1, 1) for images
    while sqrt_alpha_bar_t.dim() < x_0.dim():
        sqrt_alpha_bar_t = sqrt_alpha_bar_t.unsqueeze(-1)
        sqrt_one_minus_alpha_bar_t = sqrt_one_minus_alpha_bar_t.unsqueeze(-1)

    # TODO: 计算 x_t
    x_t = sqrt_alpha_bar_t * ___ + sqrt_one_minus_alpha_bar_t * noise  # 填入 x_0

    return x_t, noise


def sequential_diffusion(x_0, betas, num_steps=None):
    """
    演示逐步扩散过程

    q(x_t|x_{t-1}) = N(x_t; √(1-β_t)*x_{t-1}, β_t*I)
    """
    if num_steps is None:
        num_steps = len(betas)

    x = x_0.clone()
    trajectory = [x.clone()]

    for t in range(num_steps):
        beta_t = betas[t]

        # TODO: 采样噪声
        noise = torch.randn_like(x)

        # TODO: 一步扩散
        # x_t = √(1-β_t) * x_{t-1} + √β_t * ε
        x = torch.sqrt(1 - beta_t) * x + torch.___(beta_t) * noise  # 使用 sqrt

        trajectory.append(x.clone())

    return trajectory


def compute_schedule(timesteps, beta_start=0.0001, beta_end=0.02):
    """计算扩散调度参数"""
    betas = torch.linspace(beta_start, beta_end, timesteps)
    alphas = 1 - betas
    alpha_bar = torch.cumprod(alphas, dim=0)
    sqrt_alpha_bar = torch.sqrt(alpha_bar)
    sqrt_one_minus_alpha_bar = torch.sqrt(1 - alpha_bar)

    return {
        'betas': betas,
        'alphas': alphas,
        'alpha_bar': alpha_bar,
        'sqrt_alpha_bar': sqrt_alpha_bar,
        'sqrt_one_minus_alpha_bar': sqrt_one_minus_alpha_bar
    }


def visualize_diffusion():
    """可视化扩散过程中信噪比的变化"""
    schedule = compute_schedule(timesteps=1000)

    alpha_bar = schedule['alpha_bar']

    # 信噪比 (SNR) = ᾱ / (1 - ᾱ)
    snr = alpha_bar / (1 - alpha_bar)
    snr_db = 10 * torch.log10(snr + 1e-8)

    print("不同时间步的信噪比 (dB):")
    for t in [0, 100, 250, 500, 750, 999]:
        print(f"  t={t}: SNR = {snr_db[t]:.2f} dB")

    return snr_db


class DiffusionForward:
    """前向扩散过程封装"""

    def __init__(self, timesteps=1000, beta_start=0.0001, beta_end=0.02):
        self.timesteps = timesteps

        # 计算调度参数
        schedule = compute_schedule(timesteps, beta_start, beta_end)
        self.betas = schedule['betas']
        self.sqrt_alpha_bar = schedule['sqrt_alpha_bar']
        self.sqrt_one_minus_alpha_bar = schedule['sqrt_one_minus_alpha_bar']

    def q_sample(self, x_0, t):
        """采样 q(x_t|x_0)"""
        return forward_diffusion_sample(
            x_0, t,
            self.sqrt_alpha_bar,
            self.sqrt_one_minus_alpha_bar
        )

    def get_noisy_image(self, x_0, t):
        """获取加噪图像（不返回噪声）"""
        x_t, _ = self.q_sample(x_0, t)
        return x_t


def main():
    print("测试前向扩散...")
    schedule = compute_schedule(timesteps=1000)

    x_0 = torch.randn(4, 1, 28, 28)  # 原始图像
    t = torch.randint(0, 1000, (4,))  # 随机时间步

    x_t, noise = forward_diffusion_sample(
        x_0, t,
        schedule['sqrt_alpha_bar'],
        schedule['sqrt_one_minus_alpha_bar']
    )

    assert x_t.shape == x_0.shape
    assert noise.shape == x_0.shape
    print("✓ forward_diffusion_sample 通过!")

    print("\n测试逐步扩散...")
    x_0_single = torch.randn(1, 1, 28, 28)
    trajectory = sequential_diffusion(x_0_single, schedule['betas'], num_steps=10)
    assert len(trajectory) == 11  # 包含初始状态
    print(f"✓ 生成 {len(trajectory)} 步轨迹")

    print("\n测试 DiffusionForward 类...")
    diffusion = DiffusionForward(timesteps=1000)
    x_t, noise = diffusion.q_sample(x_0, t)
    assert x_t.shape == x_0.shape
    print("✓ DiffusionForward 通过!")

    print("\n可视化信噪比变化...")
    visualize_diffusion()

    # 验证：t=0 时 x_t ≈ x_0, t=T-1 时 x_t ≈ noise
    print("\n验证端点行为...")
    t_start = torch.zeros(4, dtype=torch.long)
    t_end = torch.full((4,), 999, dtype=torch.long)

    x_t_start, _ = diffusion.q_sample(x_0, t_start)
    x_t_end, _ = diffusion.q_sample(x_0, t_end)

    # t=0 时应该几乎是原图
    diff_start = (x_t_start - x_0).abs().mean()
    # t=999 时应该几乎是纯噪声
    diff_end = (x_t_end).abs().mean()  # 应该接近标准正态的期望

    print(f"  t=0 与原图差异: {diff_start:.4f}")
    print(f"  t=999 均值: {diff_end:.4f} (应接近 0.8)")

    print("\n🎉 所有测试通过！前向扩散掌握完成！")


if __name__ == "__main__":
    main()
