"""
练习 38: 时间步嵌入

时间步嵌入让去噪网络知道当前处于扩散过程的哪个阶段。
这对于预测正确的噪声量至关重要。

实现方式类似于 Transformer 的位置编码。

在这个练习中，你将学习：
- 时间嵌入的作用
- 正弦时间编码
- 时间嵌入的注入方式
"""

import torch
import torch.nn as nn
import math


def get_timestep_embedding(timesteps, embedding_dim):
    """
    正弦时间步嵌入

    Args:
        timesteps: 时间步，形状 (batch_size,)
        embedding_dim: 嵌入维度

    Returns:
        嵌入向量，形状 (batch_size, embedding_dim)
    """
    half_dim = embedding_dim // 2
    emb = math.log(10000) / (half_dim - 1)
    emb = torch.exp(torch.arange(half_dim, device=timesteps.device) * -emb)
    
    # TODO: 计算时间步嵌入
    emb = timesteps[:, None].float() * emb[None, :]
    emb = torch.cat([emb.sin(), emb.cos()], dim=-1)
    
    return emb


class TimeEmbedding(nn.Module):
    """可学习的时间嵌入模块"""
    
    def __init__(self, time_dim, embed_dim):
        super().__init__()
        
        self.time_embed = nn.Sequential(
            nn.Linear(time_dim, embed_dim),
            nn.SiLU(),
            nn.Linear(embed_dim, embed_dim),
        )
    
    def forward(self, t):
        """
        Args:
            t: 时间步，形状 (batch_size,)
        Returns:
            时间嵌入，形状 (batch_size, embed_dim)
        """
        # 先用正弦编码，再通过 MLP
        t_emb = get_timestep_embedding(t, self.time_embed[0].in_features)
        return self.time_embed(t_emb)


def main():
    print("测试时间步嵌入...")
    t = torch.tensor([0, 100, 500, 999])
    emb = get_timestep_embedding(t, embedding_dim=64)
    
    assert emb.shape == (4, 64)
    print(f"✓ 嵌入形状: {emb.shape}")
    
    # 不同时间步应该有不同的嵌入
    assert not torch.allclose(emb[0], emb[1])
    print("✓ 不同时间步有不同的嵌入")
    
    print("\n测试 TimeEmbedding 模块...")
    time_embed = TimeEmbedding(time_dim=64, embed_dim=128)
    out = time_embed(t)
    assert out.shape == (4, 128)
    print(f"✓ TimeEmbedding 输出形状: {out.shape}")
    
    print("\n🎉 时间步嵌入测试通过！")

if __name__ == "__main__":
    main()
