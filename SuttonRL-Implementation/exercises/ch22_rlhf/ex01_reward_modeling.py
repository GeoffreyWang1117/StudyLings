"""
练习: Reward Modeling - RLHF第二阶段

算法描述:
从人类偏好对比中学习奖励模型，这是RLHF的核心创新。
将"对齐"问题转化为可优化的奖励函数。

核心思想:
- 人类比较两个输出: y_w (win) vs y_l (lose)
- 建模偏好概率: P(y_w > y_l | x)
- 使用Bradley-Terry模型

数学公式:
1. Bradley-Terry模型:
   P(y_w > y_l | x) = σ(r_θ(x, y_w) - r_θ(x, y_l))
   其中σ是sigmoid函数

2. 训练目标:
   L(θ) = -E_{(x,y_w,y_l)~D}[log σ(r_θ(x,y_w) - r_θ(x,y_l))]

3. 梯度:
   ∇_θ L = -E[σ(r_l - r_w) · (∇r_w - ∇r_l)]

RLHF三阶段:
1. SFT: 监督微调 (Behavioral Cloning)
2. RM: 奖励建模 (本练习)
3. RL: 强化学习优化 (PPO with KL penalty)

应用实例:
- ChatGPT: InstructGPT论文
- Claude: Constitutional AI
- GPT-4: RLHF对齐
- Llama 2: RLHF微调

参考: Christiano et al. (2017) "Deep RL from Human Preferences"
        Ouyang et al. (2022) "Training language models to follow instructions (InstructGPT)"
"""

import numpy as np

class RewardModel:
    """奖励模型: 从偏好对比学习奖励函数"""
    def __init__(self, state_dim, action_dim, lr=0.001):
        """
        初始化

        Args:
            state_dim: 状态/prompt维度
            action_dim: 动作/response维度
            lr: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr

        # 奖励网络: r_θ(x, y)
        self.weights = np.random.randn(state_dim + action_dim) * 0.01

    def compute_reward(self, state, action):
        """
        计算奖励 r(x, y)

        Args:
            state: 输入/prompt x
            action: 输出/response y

        Returns:
            reward: 标量奖励值
        """
        # TODO: 实现奖励计算
        # 提示: concat(x, y) @ weights
        pass  # TODO

    def predict_preference(self, state, action_w, action_l):
        """
        预测偏好概率 P(y_w > y_l | x)

        Args:
            state: prompt
            action_w: 获胜response
            action_l: 失败response

        Returns:
            prob: P(y_w > y_l)
        """
        # TODO: 实现偏好预测
        # 提示1: r_w = self.compute_reward(state, action_w)
        # 提示2: r_l = self.compute_reward(state, action_l)
        # 提示3: prob = sigmoid(r_w - r_l)
        pass  # TODO

    def train_step(self, state, action_w, action_l):
        """
        训练一步

        Args:
            state: prompt
            action_w: preferred response
            action_l: dispreferred response

        Returns:
            loss: 损失值
        """
        # TODO: 实现训练步骤
        # 提示1: 计算r_w和r_l
        # 提示2: 计算loss = -log σ(r_w - r_l)
        # 提示3: 计算梯度: σ(r_l - r_w) * (feature_w - feature_l)
        # 提示4: 更新参数
        pass  # TODO

    def train(self, preference_data, epochs=100, batch_size=32):
        """
        训练奖励模型

        Args:
            preference_data: [(x, y_w, y_l), ...] 偏好对比数据
            epochs: 训练轮数
            batch_size: 批大小

        Returns:
            history: 训练历史
        """
        # TODO: 实现完整训练
        # 提示1: 对每个epoch:
        # 提示2:   打乱数据
        # 提示3:   分批训练
        # 提示4:   记录loss和准确率
        pass  # TODO

    def evaluate(self, test_data):
        """
        评估奖励模型准确率

        Args:
            test_data: [(x, y_w, y_l), ...]

        Returns:
            accuracy: 预测准确率
        """
        # TODO: 实现评估
        # 提示: 计算P(y_w > y_l) > 0.5的比例
        pass  # TODO


def collect_human_preferences_simulation(env, policy1, policy2, n_comparisons=100):
    """
    模拟收集人类偏好数据

    在真实RLHF中:
    1. 模型生成多个响应
    2. 人类标注者比较并选择更好的
    3. 收集(prompt, better_response, worse_response)

    Args:
        env: 环境
        policy1, policy2: 两个策略
        n_comparisons: 比较次数

    Returns:
        preference_data: [(x, y_w, y_l), ...]
    """
    # TODO: 实现偏好数据收集模拟
    # 提示1: 生成prompt
    # 提示2: 两个策略分别生成response
    # 提示3: 模拟人类选择（用真实奖励或规则）
    # 提示4: 记录(x, y_better, y_worse)
    pass  # TODO


def visualize_reward_model():
    """可视化奖励模型的学习过程"""
    print("\n=== 奖励模型学习过程 ===")
    print("\n输入: 偏好对比")
    print("  Prompt: '写一首关于AI的诗'")
    print("  Response A: '...'  (人类选择)")
    print("  Response B: '...'")
    print("\n模型学习:")
    print("  初始: r(A) ≈ r(B) (随机)")
    print("  训练: max P(A > B) = σ(r(A) - r(B))")
    print("  结果: r(A) >> r(B)")
    print("\n泛化:")
    print("  新prompt: '写一首关于太空的诗'")
    print("  模型可以评分新response（未见过的）")
    print("  这就是奖励模型的价值！")


def rlhf_three_stages():
    """RLHF三阶段详解"""
    print("\n=== RLHF三阶段 ===")
    print("\n阶段1: Supervised Fine-Tuning (SFT)")
    print("  - 数据: 高质量人类演示 (prompt, ideal_response)")
    print("  - 方法: Behavioral Cloning (监督学习)")
    print("  - 目标: 让模型学会基本的回复能力")
    print("  - 输出: π_SFT (基础策略)")
    print("\n阶段2: Reward Modeling (RM)")
    print("  - 数据: 人类偏好对比 (prompt, better, worse)")
    print("  - 方法: Bradley-Terry模型")
    print("  - 目标: 学习人类偏好的奖励函数")
    print("  - 输出: r_θ(x, y) (奖励模型)")
    print("\n阶段3: RL Fine-Tuning")
    print("  - 初始策略: π_SFT")
    print("  - 奖励: r_θ(x, y) - β·KL(π||π_SFT)")
    print("  - 方法: PPO with KL penalty")
    print("  - 目标: 最大化奖励，不过度偏离SFT")
    print("  - 输出: π_RLHF (最终对齐策略)")
    print("\n为什么需要三阶段?")
    print("  - 直接RL难: 探索空间巨大")
    print("  - SFT初始化: 提供好的起点")
    print("  - RM分离评估: 人类不需要写reward code")
    print("  - RL优化: 超越演示数据")


def bradley_terry_model_explained():
    """详解Bradley-Terry模型"""
    print("\n=== Bradley-Terry模型 ===")
    print("\n起源: 1952年，用于体育比赛排名")
    print("\n假设: 每个选手有潜在实力r_i")
    print("  P(i胜j) = exp(r_i) / (exp(r_i) + exp(r_j))")
    print("         = σ(r_i - r_j)")
    print("\n在RLHF中:")
    print("  选手 -> 模型response")
    print("  实力 -> 奖励分数")
    print("  比赛 -> 人类偏好对比")
    print("\n优势:")
    print("  ✓ 简单高效")
    print("  ✓ 只需成对比较（比绝对评分容易）")
    print("  ✓ 理论基础坚实")
    print("  ✓ 可扩展到多选项 (Plackett-Luce)")


if __name__ == "__main__":
    print("练习: Reward Modeling - RLHF的核心创新")
    print("核心: 从人类偏好学习奖励函数")
    print("\n目标函数:")
    print("  L = -E[log σ(r(x,y_w) - r(x,y_l))]")
    print("  其中 y_w是preferred, y_l是dispreferred")

    visualize_reward_model()
    bradley_terry_model_explained()
    rlhf_three_stages()

    print("\n" + "="*50)
    print("训练示例...")
    # TODO: 实现示例

    print("\n应用: ChatGPT, Claude, GPT-4, Llama 2等所有对齐LLM")
