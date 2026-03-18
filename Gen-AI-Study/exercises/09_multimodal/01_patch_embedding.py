"""
练习 43: 图像块嵌入 (Patch Embedding)

ViT 将图像分割成小块并嵌入，让 Transformer 能够处理图像。

流程：
1. 将图像分成 P×P 的小块
2. 展平每个块
3. 通过线性层映射到嵌入维度

例如 224x224 图像，patch_size=16:
- 分成 14x14=196 个块
- 每块是 16x16x3=768 维
- 映射到 d_model 维
"""

import torch
import torch.nn as nn


class PatchEmbedding(nn.Module):
    """图像块嵌入"""
    
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        
        # 使用卷积实现 patch 嵌入（等价于展平+线性）
        self.proj = nn.Conv2d(
            in_channels, embed_dim,
            kernel_size=patch_size, stride=patch_size
        )
    
    def forward(self, x):
        """
        Args:
            x: (batch, channels, height, width)
        Returns:
            (batch, num_patches, embed_dim)
        """
        # Conv2d: (B, C, H, W) -> (B, E, H/P, W/P)
        x = self.proj(x)
        
        # 展平空间维度: (B, E, H', W') -> (B, E, N) -> (B, N, E)
        x = x.flatten(2).transpose(1, 2)
        
        return x


def main():
    print("测试 PatchEmbedding...")
    patch_emb = PatchEmbedding(img_size=224, patch_size=16, embed_dim=768)
    
    x = torch.randn(4, 3, 224, 224)
    patches = patch_emb(x)
    
    expected_num_patches = (224 // 16) ** 2  # 196
    assert patches.shape == (4, expected_num_patches, 768)
    print(f"✓ 输出形状: {patches.shape}")
    print(f"✓ 图像块数量: {expected_num_patches}")
    
    print("\n🎉 Patch Embedding 测试通过！")

if __name__ == "__main__":
    main()
