"""
练习 51: Stable Diffusion U-Net

SD 的 U-Net 包含自注意力和交叉注意力，处理图像和文本。
"""

import torch
import torch.nn as nn


class SDBlock(nn.Module):
    """Stable Diffusion 风格的块"""
    
    def __init__(self, channels, context_dim=768):
        super().__init__()
        
        # ResNet 块
        self.resnet = nn.Sequential(
            nn.GroupNorm(32, channels),
            nn.SiLU(),
            nn.Conv2d(channels, channels, 3, padding=1)
        )
        
        # 自注意力
        self.self_attn = nn.MultiheadAttention(channels, num_heads=8, batch_first=True)
        
        # 交叉注意力 (条件)
        self.cross_attn = nn.MultiheadAttention(channels, num_heads=8, 
                                                 kdim=context_dim, vdim=context_dim,
                                                 batch_first=True)
        
        # FFN
        self.ffn = nn.Sequential(
            nn.Linear(channels, channels * 4),
            nn.GELU(),
            nn.Linear(channels * 4, channels)
        )
    
    def forward(self, x, context):
        B, C, H, W = x.shape
        
        # ResNet
        x = x + self.resnet(x)
        
        # 展平为序列
        x_flat = x.flatten(2).transpose(1, 2)  # (B, H*W, C)
        
        # 自注意力
        x_flat = x_flat + self.self_attn(x_flat, x_flat, x_flat)[0]
        
        # 交叉注意力
        x_flat = x_flat + self.cross_attn(x_flat, context, context)[0]
        
        # FFN
        x_flat = x_flat + self.ffn(x_flat)
        
        # 重塑回特征图
        x = x_flat.transpose(1, 2).view(B, C, H, W)
        
        return x


def main():
    print("测试 SD U-Net 块...")
    
    block = SDBlock(channels=256, context_dim=768)
    
    x = torch.randn(2, 256, 32, 32)
    context = torch.randn(2, 77, 768)  # 文本嵌入
    
    out = block(x, context)
    
    assert out.shape == x.shape
    print(f"✓ 输出形状: {out.shape}")
    
    print("\n🎉 SD U-Net 块测试通过！")

if __name__ == "__main__":
    main()
