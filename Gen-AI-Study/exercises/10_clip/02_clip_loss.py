"""
练习 47: CLIP 损失函数

CLIP 使用对称的对比损失，同时从图像和文本两个方向进行匹配。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CLIPLoss(nn.Module):
    """CLIP 对比损失"""
    
    def __init__(self, temperature=0.07):
        super().__init__()
        self.temperature = nn.Parameter(torch.tensor(temperature).log())
    
    def forward(self, image_features, text_features):
        # 获取温度
        temperature = self.temperature.exp()
        
        # 归一化
        image_features = F.normalize(image_features, dim=-1)
        text_features = F.normalize(text_features, dim=-1)
        
        # 相似度矩阵
        logits = image_features @ text_features.T / temperature
        
        # 标签 (对角线为正样本)
        batch_size = image_features.shape[0]
        labels = torch.arange(batch_size, device=logits.device)
        
        # 对称损失
        loss_i2t = F.cross_entropy(logits, labels)
        loss_t2i = F.cross_entropy(logits.T, labels)
        
        return (loss_i2t + loss_t2i) / 2


def main():
    print("测试 CLIP 损失...")
    
    criterion = CLIPLoss()
    
    image_features = torch.randn(8, 512)
    text_features = torch.randn(8, 512)
    
    loss = criterion(image_features, text_features)
    print(f"✓ CLIP 损失: {loss.item():.4f}")
    
    print("\n🎉 CLIP 损失测试通过！")

if __name__ == "__main__":
    main()
