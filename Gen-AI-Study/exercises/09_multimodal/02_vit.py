"""
练习 44: Vision Transformer (ViT)

ViT 将 Transformer 直接应用于图像分类任务。

架构:
Patch Embedding + [CLS] Token + Position Embedding
    ↓
N × Transformer Encoder Block
    ↓
[CLS] Token -> MLP Head -> Classification
"""

import torch
import torch.nn as nn


class ViT(nn.Module):
    """简化版 Vision Transformer"""
    
    def __init__(self, img_size=224, patch_size=16, in_channels=3,
                 num_classes=1000, embed_dim=768, depth=12, num_heads=12):
        super().__init__()
        
        num_patches = (img_size // patch_size) ** 2
        
        # Patch 嵌入
        self.patch_embed = nn.Conv2d(in_channels, embed_dim, patch_size, patch_size)
        
        # [CLS] token
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        
        # 位置嵌入
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        
        # Transformer 编码器
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        # 分类头
        self.head = nn.Linear(embed_dim, num_classes)
        
        self._init_weights()
    
    def _init_weights(self):
        nn.init.normal_(self.cls_token, std=0.02)
        nn.init.normal_(self.pos_embed, std=0.02)
    
    def forward(self, x):
        B = x.shape[0]
        
        # Patch 嵌入
        x = self.patch_embed(x).flatten(2).transpose(1, 2)  # (B, N, E)
        
        # 添加 [CLS] token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)  # (B, N+1, E)
        
        # 添加位置嵌入
        x = x + self.pos_embed
        
        # Transformer
        x = self.transformer(x)
        
        # 分类 (使用 [CLS] token)
        cls_output = x[:, 0]
        return self.head(cls_output)


def main():
    print("测试 ViT...")
    model = ViT(img_size=224, patch_size=16, num_classes=10, 
                embed_dim=192, depth=2, num_heads=4)
    
    x = torch.randn(4, 3, 224, 224)
    out = model(x)
    
    assert out.shape == (4, 10)
    print(f"✓ 输出形状: {out.shape}")
    
    params = sum(p.numel() for p in model.parameters())
    print(f"✓ 参数数量: {params:,}")
    
    print("\n🎉 ViT 测试通过！")

if __name__ == "__main__":
    main()
