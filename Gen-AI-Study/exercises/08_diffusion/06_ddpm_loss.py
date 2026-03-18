"""
练习 40: DDPM 损失函数

DDPM 训练目标是让模型预测添加到数据中的噪声。

Loss = E[||ε - ε_θ(x_t, t)||²]

训练步骤：
1. 采样数据 x_0
2. 随机采样时间步 t
3. 采样噪声 ε
4. 计算 x_t = √ᾱ_t * x_0 + √(1-ᾱ_t) * ε
5. 预测噪声 ε_θ(x_t, t)
6. 计算损失 ||ε - ε_θ||²
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def ddpm_loss(model, x_0, t, sqrt_alpha_bar, sqrt_one_minus_alpha_bar):
    """
    计算 DDPM 损失
    
    Args:
        model: 噪声预测模型
        x_0: 原始数据
        t: 时间步
        sqrt_alpha_bar: √ᾱ 序列
        sqrt_one_minus_alpha_bar: √(1-ᾱ) 序列
    
    Returns:
        loss: MSE 损失
    """
    # 采样噪声
    noise = torch.randn_like(x_0)
    
    # 获取系数
    sqrt_alpha_bar_t = sqrt_alpha_bar[t].view(-1, 1, 1, 1)
    sqrt_one_minus_alpha_bar_t = sqrt_one_minus_alpha_bar[t].view(-1, 1, 1, 1)
    
    # 前向扩散
    x_t = sqrt_alpha_bar_t * x_0 + sqrt_one_minus_alpha_bar_t * noise
    
    # 预测噪声
    noise_pred = model(x_t, t)
    
    # MSE 损失
    loss = F.mse_loss(noise_pred, noise)
    
    return loss


class DDPMTrainer:
    """DDPM 训练器"""
    
    def __init__(self, model, timesteps=1000, beta_start=0.0001, beta_end=0.02):
        self.model = model
        self.timesteps = timesteps
        
        # 计算调度参数
        betas = torch.linspace(beta_start, beta_end, timesteps)
        alphas = 1 - betas
        alpha_bar = torch.cumprod(alphas, dim=0)
        
        self.sqrt_alpha_bar = torch.sqrt(alpha_bar)
        self.sqrt_one_minus_alpha_bar = torch.sqrt(1 - alpha_bar)
    
    def train_step(self, x_0):
        """单步训练"""
        batch_size = x_0.size(0)
        device = x_0.device
        
        # 随机时间步
        t = torch.randint(0, self.timesteps, (batch_size,), device=device)
        
        # 计算损失
        loss = ddpm_loss(
            self.model, x_0, t,
            self.sqrt_alpha_bar.to(device),
            self.sqrt_one_minus_alpha_bar.to(device)
        )
        
        return loss


def main():
    print("DDPM 损失函数:")
    print("L = E[||ε - ε_θ(x_t, t)||²]")
    print("\n训练目标: 预测添加到数据中的噪声")
    print("✓ DDPM 损失函数理解完成！")

if __name__ == "__main__":
    main()
