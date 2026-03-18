"""
练习 46: CLIP 编码器

CLIP 使用独立的图像和文本编码器，将两种模态映射到共享空间。
"""

import torch
import torch.nn as nn


class ImageEncoder(nn.Module):
    """CLIP 图像编码器 (简化版)"""
    
    def __init__(self, embed_dim=512):
        super().__init__()
        
        # 简化的 ResNet 风格编码器
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 7, stride=2, padding=3),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2, padding=1),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, embed_dim)
        )
    
    def forward(self, x):
        return self.features(x)


class TextEncoder(nn.Module):
    """CLIP 文本编码器 (简化版)"""
    
    def __init__(self, vocab_size=10000, embed_dim=512, max_len=77):
        super().__init__()
        
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_len, embed_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=8, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)
        
        self.projection = nn.Linear(embed_dim, embed_dim)
    
    def forward(self, text_ids):
        B, L = text_ids.shape
        positions = torch.arange(L, device=text_ids.device)
        
        x = self.token_embedding(text_ids) + self.position_embedding(positions)
        x = self.transformer(x)
        
        # 使用 EOS token 的表示
        x = x[:, -1]
        return self.projection(x)


def main():
    print("测试 CLIP 编码器...")
    
    image_encoder = ImageEncoder(embed_dim=256)
    text_encoder = TextEncoder(vocab_size=1000, embed_dim=256)
    
    images = torch.randn(4, 3, 224, 224)
    text_ids = torch.randint(0, 1000, (4, 20))
    
    image_features = image_encoder(images)
    text_features = text_encoder(text_ids)
    
    assert image_features.shape == (4, 256)
    assert text_features.shape == (4, 256)
    
    print(f"✓ 图像特征形状: {image_features.shape}")
    print(f"✓ 文本特征形状: {text_features.shape}")
    
    print("\n🎉 CLIP 编码器测试通过！")

if __name__ == "__main__":
    main()
