"""
练习 39: 反向扩散

反向扩散从噪声逐步去噪，生成清晰的样本。这是采样过程的核心。

公式：
x_{t-1} = (1/√α_t) * (x_t - (1-α_t)/√(1-ᾱ_t) * ε_θ(x_t, t)) + σ_t * z
"""

import torch
import math


def p_sample(model, x_t, t, betas, alphas, alpha_bar, sqrt_one_minus_alpha_bar):
    """单步反向采样"""
    with torch.no_grad():
        # 预测噪声
        predicted_noise = model(x_t, t)
        
        alpha_t = alphas[t]
        beta_t = betas[t]
        sqrt_one_minus_alpha_bar_t = sqrt_one_minus_alpha_bar[t]
        
        # 计算均值
        mean = (1 / torch.sqrt(alpha_t)) * (
            x_t - (beta_t / sqrt_one_minus_alpha_bar_t) * predicted_noise
        )
        
        # 添加噪声（除了 t=0）
        if t > 0:
            noise = torch.randn_like(x_t)
            std = torch.sqrt(beta_t)
            x_t_minus_1 = mean + std * noise
        else:
            x_t_minus_1 = mean
            
        return x_t_minus_1


def p_sample_loop(model, shape, timesteps, schedule_params):
    """完整的采样循环"""
    device = next(model.parameters()).device
    
    # 从纯噪声开始
    x = torch.randn(shape, device=device)
    
    for t in reversed(range(timesteps)):
        t_batch = torch.full((shape[0],), t, device=device, dtype=torch.long)
        x = p_sample(model, x, t_batch, **schedule_params)
        
    return x


def main():
    print("反向扩散需要训练好的模型。")
    print("这个练习主要是理解采样公式。")
    print("\n关键公式：")
    print("x_{t-1} = (1/√α_t) * (x_t - β_t/√(1-ᾱ_t) * ε_θ) + σ_t * z")
    print("\n✓ 反向扩散概念理解完成！")

if __name__ == "__main__":
    main()
