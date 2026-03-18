"""
练习 45: 对比学习损失

对比学习通过拉近正样本对、推远负样本对来学习表示。

InfoNCE Loss:
L = -log(exp(sim(z_i, z_j)/τ) / Σ_k exp(sim(z_i, z_k)/τ))

在 CLIP 中，正样本对是匹配的图像-文本对。
"""

import torch
import torch.nn.functional as F


def contrastive_loss(image_features, text_features, temperature=0.07):
    """
    对比学习损失 (InfoNCE)
    
    Args:
        image_features: (batch, dim) 图像特征
        text_features: (batch, dim) 文本特征
        temperature: 温度参数
    
    Returns:
        loss: 对比损失
    """
    # 归一化
    image_features = F.normalize(image_features, dim=-1)
    text_features = F.normalize(text_features, dim=-1)
    
    # 计算相似度矩阵
    logits = image_features @ text_features.T / temperature
    
    # 对角线是正样本
    batch_size = image_features.shape[0]
    labels = torch.arange(batch_size, device=image_features.device)
    
    # 图像到文本方向的损失
    loss_i2t = F.cross_entropy(logits, labels)
    
    # 文本到图像方向的损失
    loss_t2i = F.cross_entropy(logits.T, labels)
    
    # 对称损失
    loss = (loss_i2t + loss_t2i) / 2
    
    return loss


def main():
    print("测试对比学习损失...")
    
    image_features = torch.randn(8, 512)
    text_features = torch.randn(8, 512)
    
    loss = contrastive_loss(image_features, text_features)
    print(f"✓ 对比损失: {loss.item():.4f}")
    
    # 当特征完全匹配时，损失应该更低
    text_features_matched = image_features.clone()
    loss_matched = contrastive_loss(image_features, text_features_matched)
    print(f"✓ 匹配时损失: {loss_matched.item():.4f}")
    
    assert loss_matched < loss
    print("✓ 验证通过：匹配特征的损失更低")
    
    print("\n🎉 对比学习损失测试通过！")

if __name__ == "__main__":
    main()
