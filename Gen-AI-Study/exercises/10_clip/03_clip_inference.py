"""
练习 48: CLIP 推理

CLIP 可以进行零样本图像分类，无需额外训练即可识别新类别。
"""

import torch
import torch.nn.functional as F


def zero_shot_classify(image_features, text_features, temperature=0.07):
    """
    零样本分类
    
    Args:
        image_features: (batch, dim) 图像特征
        text_features: (num_classes, dim) 各类别的文本特征
    
    Returns:
        predictions: (batch,) 预测的类别
        probs: (batch, num_classes) 概率分布
    """
    # 归一化
    image_features = F.normalize(image_features, dim=-1)
    text_features = F.normalize(text_features, dim=-1)
    
    # 计算相似度
    similarity = image_features @ text_features.T / temperature
    
    # 转为概率
    probs = F.softmax(similarity, dim=-1)
    
    # 预测
    predictions = probs.argmax(dim=-1)
    
    return predictions, probs


def main():
    print("测试 CLIP 零样本分类...")
    
    # 模拟特征
    image_features = torch.randn(4, 512)
    
    # 假设有 3 个类别的文本模板特征
    class_names = ["a photo of a cat", "a photo of a dog", "a photo of a bird"]
    text_features = torch.randn(3, 512)
    
    predictions, probs = zero_shot_classify(image_features, text_features)
    
    print(f"✓ 预测类别: {predictions.tolist()}")
    print(f"✓ 概率分布:\n{probs}")
    
    print("\n🎉 CLIP 推理测试通过！")

if __name__ == "__main__":
    main()
