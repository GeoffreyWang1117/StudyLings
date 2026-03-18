"""
练习 35: 噪声调度 (Noise Schedule)

扩散模型通过逐步添加噪声来破坏数据。
噪声调度定义了每个时间步添加多少噪声。

关键参数：
- β_t: 每步添加的噪声方差
- α_t = 1 - β_t
- ᾱ_t = ∏(α_i) 从 i=1 到 t: 累积的信号保留量

常用调度：
- 线性调度: β 从 β_1 线性增加到 β_T
- 余弦调度: 更平滑的退化

在这个练习中，你将学习：
- 噪声调度的定义
- 不同调度的特点
- 相关参数的计算
"""

import torch
import math


def linear_beta_schedule(timesteps, beta_start=0.0001, beta_end=0.02):
    """
    线性噪声调度

    β_t 从 beta_start 线性增加到 beta_end

    Args:
        timesteps: 总时间步数 T
        beta_start: 初始 β 值
        beta_end: 最终 β 值

    Returns:
        betas: 形状 (timesteps,) 的 β 序列
    """
    # TODO: 创建线性空间
    betas = torch.___(beta_start, beta_end, timesteps)  # 使用 linspace

    return betas


def cosine_beta_schedule(timesteps, s=0.008):
    """
    余弦噪声调度

    改进的调度方式，避免早期破坏太快

    f(t) = cos((t/T + s) / (1+s) * π/2)^2
    ᾱ_t = f(t) / f(0)
    β_t = 1 - ᾱ_t / ᾱ_{t-1}
    """
    steps = timesteps + 1
    t = torch.linspace(0, timesteps, steps)

    # TODO: 计算 f(t)
    f_t = torch.cos((t / timesteps + s) / (1 + s) * math.pi / 2) ** ___  # 填入 2

    # 计算 ᾱ_t
    alpha_bar = f_t / f_t[0]

    # TODO: 计算 β_t = 1 - ᾱ_t / ᾱ_{t-1}
    betas = 1 - alpha_bar[1:] / alpha_bar[:-1]

    # 裁剪到合理范围
    betas = torch.clamp(betas, 0.0001, 0.9999)

    return betas


def compute_alpha_bar(betas):
    """
    计算累积 alpha

    α_t = 1 - β_t
    ᾱ_t = ∏(α_i) for i=1 to t
    """
    # TODO: 计算 α_t
    alphas = 1 - ___  # 填入 betas

    # TODO: 计算累积乘积 ᾱ_t
    alpha_bar = torch.___(alphas, dim=0)  # 使用 cumprod

    return alpha_bar


def compute_schedule_params(betas):
    """
    计算扩散过程所需的所有参数

    Returns:
        dict: 包含以下参数
        - betas
        - alphas
        - alpha_bar
        - sqrt_alpha_bar
        - sqrt_one_minus_alpha_bar
        - posterior_variance
    """
    alphas = 1 - betas
    alpha_bar = torch.cumprod(alphas, dim=0)

    # 用于前向扩散 q(x_t|x_0)
    # x_t = sqrt(ᾱ_t) * x_0 + sqrt(1-ᾱ_t) * ε
    # TODO: 计算 sqrt(ᾱ_t)
    sqrt_alpha_bar = torch.___(alpha_bar)  # 使用 sqrt

    # TODO: 计算 sqrt(1 - ᾱ_t)
    sqrt_one_minus_alpha_bar = torch.sqrt(1 - ___)  # 填入 alpha_bar

    # 后验方差 (用于反向过程)
    # β̃_t = β_t * (1 - ᾱ_{t-1}) / (1 - ᾱ_t)
    alpha_bar_prev = F_pad_alpha_bar(alpha_bar)
    posterior_variance = betas * (1 - alpha_bar_prev) / (1 - alpha_bar)

    return {
        'betas': betas,
        'alphas': alphas,
        'alpha_bar': alpha_bar,
        'sqrt_alpha_bar': sqrt_alpha_bar,
        'sqrt_one_minus_alpha_bar': sqrt_one_minus_alpha_bar,
        'posterior_variance': posterior_variance
    }


def F_pad_alpha_bar(alpha_bar):
    """在 alpha_bar 前面填充 1.0（对应 t=0）"""
    return torch.cat([torch.tensor([1.0]), alpha_bar[:-1]])


def visualize_schedule():
    """可视化不同调度的区别"""
    timesteps = 1000

    linear_betas = linear_beta_schedule(timesteps)
    cosine_betas = cosine_beta_schedule(timesteps)

    linear_alpha_bar = compute_alpha_bar(linear_betas)
    cosine_alpha_bar = compute_alpha_bar(cosine_betas)

    # 打印关键时间点的 ᾱ 值
    print("不同时间点的 ᾱ 值:")
    print("时间步\t线性\t余弦")
    for t in [0, 100, 500, 800, 999]:
        print(f"{t}\t{linear_alpha_bar[t]:.4f}\t{cosine_alpha_bar[t]:.4f}")

    return linear_alpha_bar, cosine_alpha_bar


def main():
    timesteps = 1000

    print("测试 linear_beta_schedule...")
    linear_betas = linear_beta_schedule(timesteps)
    assert linear_betas.shape == (timesteps,)
    assert linear_betas[0] < linear_betas[-1]  # 递增
    print(f"✓ β 范围: [{linear_betas[0]:.6f}, {linear_betas[-1]:.6f}]")

    print("\n测试 cosine_beta_schedule...")
    cosine_betas = cosine_beta_schedule(timesteps)
    assert cosine_betas.shape == (timesteps,)
    print(f"✓ β 范围: [{cosine_betas.min():.6f}, {cosine_betas.max():.6f}]")

    print("\n测试 compute_alpha_bar...")
    alpha_bar = compute_alpha_bar(linear_betas)
    assert alpha_bar.shape == (timesteps,)
    # ᾱ 应该递减
    assert (alpha_bar[:-1] >= alpha_bar[1:]).all()
    print(f"✓ ᾱ 范围: [{alpha_bar[-1]:.6f}, {alpha_bar[0]:.6f}]")

    print("\n测试 compute_schedule_params...")
    params = compute_schedule_params(linear_betas)
    assert all(k in params for k in ['betas', 'alphas', 'alpha_bar', 'sqrt_alpha_bar'])
    print("✓ 所有参数计算完成!")

    print("\n可视化不同调度...")
    visualize_schedule()

    print("\n🎉 所有测试通过！噪声调度掌握完成！")


if __name__ == "__main__":
    main()
