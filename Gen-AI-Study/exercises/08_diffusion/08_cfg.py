"""
练习 42: Classifier-Free Guidance (CFG)

CFG 在不需要额外分类器的情况下实现条件生成。

核心思想：
- 同时训练条件和无条件生成
- 推理时组合两者的预测
- 公式: ε_pred = ε_uncond + w * (ε_cond - ε_uncond)

w > 1 增强条件影响，生成更符合条件的样本
"""

import torch


def cfg_sample(model, x_t, t, condition, guidance_scale=7.5):
    """
    Classifier-Free Guidance 采样
    
    Args:
        model: 条件/无条件两用模型
        condition: 条件（如文本嵌入）
        guidance_scale: 引导强度 w
    """
    # 无条件预测 (condition=None 或空)
    noise_uncond = model(x_t, t, condition=None)
    
    # 条件预测
    noise_cond = model(x_t, t, condition=condition)
    
    # CFG 组合
    noise_pred = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
    
    return noise_pred


class CFGModel:
    """支持 CFG 的模型包装"""
    
    def __init__(self, model, uncond_prob=0.1):
        self.model = model
        self.uncond_prob = uncond_prob  # 训练时随机丢弃条件的概率
    
    def forward_train(self, x_t, t, condition):
        """训练时有一定概率丢弃条件"""
        if torch.rand(1) < self.uncond_prob:
            condition = None
        return self.model(x_t, t, condition)
    
    def forward_cfg(self, x_t, t, condition, guidance_scale):
        """推理时使用 CFG"""
        return cfg_sample(self.model, x_t, t, condition, guidance_scale)


def main():
    print("Classifier-Free Guidance:")
    print("ε_pred = ε_uncond + w * (ε_cond - ε_uncond)")
    print("\n参数 w (guidance_scale):")
    print("- w=1: 纯条件生成")
    print("- w>1: 增强条件影响")
    print("- 通常使用 w=7.5")
    print("\n✓ CFG 概念理解完成！")

if __name__ == "__main__":
    main()
