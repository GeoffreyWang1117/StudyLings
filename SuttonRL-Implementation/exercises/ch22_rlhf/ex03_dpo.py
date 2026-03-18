"""
练习: DPO (Direct Preference Optimization) - 2023新方法

算法描述:
DPO直接从偏好数据优化策略，绕过奖励建模和RL阶段。
2023年提出，已成为RLHF的重要替代方案。

核心思想:
- 传统RLHF: Preference -> RM -> RL
- DPO: Preference -> Direct Policy Optimization
- 数学上等价，但更简单稳定

数学推导:
1. RLHF目标:
   π* = argmax E[r(x,y) - β·KL(π||π_ref)]

2. 最优策略闭式解:
   π*(y|x) = π_ref(y|x) · exp(r(x,y)/β) / Z(x)

3. 代入Bradley-Terry:
   P(y_w > y_l) = σ(r(y_w) - r(y_l))

4. DPO目标 (消除r):
   L = -E[log σ(β log(π(y_w)/π_ref(y_w)) - β log(π(y_l)/π_ref(y_l)))]

优势:
- 不需要训练奖励模型
- 不需要RL（更稳定）
- 计算效率高
- 理论上等价于RLHF

局限:
- 需要高质量偏好数据
- 可能不如RLHF灵活
- 较新方法（2023）

2025年状态:
- 快速流行
- Llama 2, Mistral等采用
- 与RLHF互补

参考: Rafailov et al. (2023) "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
"""

import numpy as np

class DPO:
    """Direct Preference Optimization"""
    def __init__(self, state_dim, action_dim, beta=0.1, lr=0.0003):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            beta: KL系数
            lr: 学习率
        """
        self.beta = beta
        self.lr = lr

        # 策略π
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.01
        # 参考策略π_ref (通常是SFT, 固定)
        self.ref_weights = self.policy_weights.copy()

    def get_action_probs(self, state, use_ref=False):
        """获取动作概率"""
        weights = self.ref_weights if use_ref else self.policy_weights
        logits = state @ weights
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def compute_log_ratio(self, state, action):
        """
        计算log(π(a|s) / π_ref(a|s))

        Returns:
            log_ratio: log比率
        """
        # TODO: 实现log ratio计算
        # 提示1: π = self.get_action_probs(state, use_ref=False)
        # 提示2: π_ref = self.get_action_probs(state, use_ref=True)
        # 提示3: log_ratio = log(π[action]) - log(π_ref[action])
        pass  # TODO

    def compute_dpo_loss(self, state, action_w, action_l):
        """
        计算DPO损失

        Args:
            state: prompt
            action_w: preferred action
            action_l: dispreferred action

        Returns:
            loss: DPO损失
        """
        # TODO: 实现DPO损失
        # 提示1: log_ratio_w = self.compute_log_ratio(state, action_w)
        # 提示2: log_ratio_l = self.compute_log_ratio(state, action_l)
        # 提示3: logits = β * (log_ratio_w - log_ratio_l)
        # 提示4: loss = -log σ(logits)
        # 提示5: σ(x) = 1 / (1 + exp(-x))
        pass  # TODO

    def train_step(self, state, action_w, action_l):
        """训练一步"""
        # TODO: 实现训练
        # 提示1: 计算DPO loss
        # 提示2: 计算梯度 (自动微分或手动)
        # 提示3: 更新策略参数
        pass  # TODO

    def train(self, preference_data, epochs=100, batch_size=32):
        """DPO训练"""
        # TODO: 实现完整训练
        # 提示1: 与reward modeling类似
        # 提示2: 但直接优化策略
        # 提示3: 不需要单独的reward model
        pass  # TODO


def compare_rlhf_and_dpo():
    """对比RLHF和DPO"""
    print("\n=== RLHF vs DPO ===")
    print("\nRLHF (Traditional):")
    print("  1. SFT: 监督微调")
    print("  2. RM: 训练奖励模型")
    print("     损失: -log σ(r(y_w) - r(y_l))")
    print("  3. RL: PPO优化策略")
    print("     目标: max E[r(y) - β·KL(π||π_SFT)]")
    print("  ✓ 灵活（可用奖励模型评估新数据）")
    print("  ✓ 理论成熟")
    print("  ✗ 复杂（三阶段）")
    print("  ✗ RL不稳定")
    print("\nDPO (Direct):")
    print("  1. SFT: 监督微调")
    print("  2. DPO: 直接优化策略")
    print("     损失: -log σ(β(log π(y_w)/π_ref - log π(y_l)/π_ref))")
    print("  ✓ 简单（一阶段）")
    print("  ✓ 稳定（无RL）")
    print("  ✓ 高效")
    print("  ✗ 不如RLHF灵活")
    print("  ✗ 较新（2023）")
    print("\n数学关系:")
    print("  DPO是RLHF的闭式解！")
    print("  理论等价，但实现更简单")


def dpo_derivation_intuition():
    """DPO推导直觉"""
    print("\n=== DPO推导直觉 ===")
    print("\n1. RLHF最优策略:")
    print("   π*(y|x) ∝ π_ref(y|x) · exp(r(x,y)/β)")
    print("\n2. 反解r:")
    print("   r(x,y) = β log(π*(y|x)/π_ref(y|x)) + const")
    print("\n3. 代入Bradley-Terry:")
    print("   P(y_w > y_l) = σ(r(y_w) - r(y_l))")
    print("                = σ(β[log π/π_ref]_w - β[log π/π_ref]_l)")
    print("\n4. DPO目标:")
    print("   max P(y_w > y_l) 直接优化π")
    print("\n关键insight:")
    print("  奖励模型r是中间变量，可以消除！")
    print("  直接从偏好到策略")


def when_to_use_dpo_vs_rlhf():
    """何时用DPO vs RLHF"""
    print("\n=== 选择DPO还是RLHF? ===")
    print("\n使用DPO当:")
    print("  ✓ 计算资源有限")
    print("  ✓ 需要快速迭代")
    print("  ✓ 有高质量成对偏好数据")
    print("  ✓ 追求训练稳定性")
    print("  例: 小团队，研究原型")
    print("\n使用RLHF当:")
    print("  ✓ 需要最大灵活性")
    print("  ✓ 可以在线收集数据")
    print("  ✓ 有充足计算资源")
    print("  ✓ 需要持续评估/迭代")
    print("  例: OpenAI, Anthropic规模的训练")
    print("\n2025年趋势:")
    print("  - 两者互补")
    print("  - 混合方法出现")
    print("  - DPO普及度快速上升")


if __name__ == "__main__":
    print("练习: DPO - 直接偏好优化")
    print("核心: 绕过RM和RL，直接从偏好优化策略")
    print("\n损失函数:")
    print("  L = -E[log σ(β·log(π(y_w)/π_ref(y_w)) - β·log(π(y_l)/π_ref(y_l)))]")

    compare_rlhf_and_dpo()
    dpo_derivation_intuition()
    when_to_use_dpo_vs_rlhf()

    print("\n" + "="*50)
    print("2023年突破，2025年已广泛应用")
    print("Llama 2, Mistral, Zephyr等模型使用DPO")
