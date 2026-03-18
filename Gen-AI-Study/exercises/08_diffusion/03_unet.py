"""
练习 37: U-Net 架构

U-Net 是扩散模型中常用的去噪网络架构，具有对称的编码器-解码器结构。

关键特点：
- 编码器逐步下采样
- 解码器逐步上采样
- 跳跃连接保留细节信息
- 时间步嵌入注入

在这个练习中，你将学习：
- U-Net 的结构
- 跳跃连接的作用
- 时间步嵌入的注入方式
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class SinusoidalPositionEmbeddings(nn.Module):
    """时间步的正弦位置编码"""
    
    def __init__(self, dim):
        super().__init__()
        self.dim = dim

    def forward(self, time):
        device = time.device
        half_dim = self.dim // 2
        embeddings = math.log(10000) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim, device=device) * -embeddings)
        embeddings = time[:, None] * embeddings[None, :]
        embeddings = torch.cat((embeddings.sin(), embeddings.cos()), dim=-1)
        return embeddings


class Block(nn.Module):
    """基本卷积块"""
    
    def __init__(self, in_ch, out_ch, time_emb_dim, up=False):
        super().__init__()
        
        self.time_mlp = nn.Linear(time_emb_dim, out_ch)
        
        if up:
            self.conv1 = nn.Conv2d(2*in_ch, out_ch, 3, padding=1)
            self.transform = nn.ConvTranspose2d(out_ch, out_ch, 4, 2, 1)
        else:
            self.conv1 = nn.Conv2d(in_ch, out_ch, 3, padding=1)
            self.transform = nn.Conv2d(out_ch, out_ch, 4, 2, 1)
            
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding=1)
        self.bnorm1 = nn.BatchNorm2d(out_ch)
        self.bnorm2 = nn.BatchNorm2d(out_ch)
        self.relu = nn.ReLU()
        
    def forward(self, x, t):
        h = self.bnorm1(self.relu(self.conv1(x)))
        time_emb = self.relu(self.time_mlp(t))
        time_emb = time_emb[(..., ) + (None, ) * 2]
        h = h + time_emb
        h = self.bnorm2(self.relu(self.conv2(h)))
        return self.transform(h)


class SimpleUNet(nn.Module):
    """简化的 U-Net 用于扩散模型"""
    
    def __init__(self, in_channels=1, out_channels=1, time_emb_dim=32):
        super().__init__()
        
        # 时间嵌入
        self.time_mlp = nn.Sequential(
            SinusoidalPositionEmbeddings(time_emb_dim),
            nn.Linear(time_emb_dim, time_emb_dim),
            nn.ReLU()
        )
        
        # 编码器（下采样）
        self.conv0 = nn.Conv2d(in_channels, 64, 3, padding=1)
        self.downs = nn.ModuleList([
            Block(64, 128, time_emb_dim),
            Block(128, 256, time_emb_dim),
        ])
        
        # 解码器（上采样）
        self.ups = nn.ModuleList([
            Block(256, 128, time_emb_dim, up=True),
            Block(128, 64, time_emb_dim, up=True),
        ])
        
        self.output = nn.Conv2d(64, out_channels, 1)

    def forward(self, x, t):
        t = self.time_mlp(t)
        x = self.conv0(x)
        
        # 下采样，保存跳跃连接
        residuals = []
        for down in self.downs:
            x = down(x, t)
            residuals.append(x)
        
        # 上采样，使用跳跃连接
        for up in self.ups:
            residual = residuals.pop()
            x = torch.cat((x, residual), dim=1)
            x = up(x, t)
            
        return self.output(x)


def main():
    print("测试 SimpleUNet...")
    model = SimpleUNet(in_channels=1, out_channels=1)
    x = torch.randn(4, 1, 28, 28)
    t = torch.randint(0, 1000, (4,)).float()
    
    out = model(x, t)
    assert out.shape == x.shape, f"期望 {x.shape}，得到 {out.shape}"
    print(f"✓ U-Net 输出形状: {out.shape}")
    
    params = sum(p.numel() for p in model.parameters())
    print(f"✓ 参数数量: {params:,}")
    
    print("\n🎉 U-Net 测试通过！")

if __name__ == "__main__":
    main()
