# EXERCISE: reinforcement1
# DIFFICULTY: ★★★★★
# TOPIC: 强化学习与经济决策
#
# 说明：
# 强化学习可以用于建模序贯决策问题。
#
# 经济学应用：
# 1. 最优消费-储蓄决策
# 2. 动态定价
# 3. 最优投资组合
# 4. 博弈论中的学习
#
# 基本概念：
# - 状态 (State): 经济状态（如财富水平）
# - 动作 (Action): 决策（如消费量）
# - 奖励 (Reward): 效用或利润
# - 策略 (Policy): 状态到动作的映射
#
# 贝尔曼方程：
# V(s) = max_a [R(s,a) + β × E[V(s')]]
#
# Q-learning更新：
# Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]
#
# 任务：
# 1. 理解动态规划与RL的关系
# 2. 实现简单的Q-learning
# 3. 应用于经济决策问题
#
# HINT1: 贝尔曼方程是RL的理论基础
# HINT2: ε-greedy平衡探索与利用

import numpy as np
from typing import Tuple


def bellman_equation(
    value_next: np.ndarray,
    rewards: np.ndarray,
    transition_prob: np.ndarray,
    beta: float
) -> np.ndarray:
    """
    贝尔曼方程迭代。

    V(s) = max_a [R(s,a) + β × Σ P(s'|s,a) V(s')]

    参数:
        value_next: 下期价值函数
        rewards: 奖励矩阵 R(s,a)
        transition_prob: 转移概率 P(s'|s,a)
        beta: 折现因子

    返回:
        更新后的价值函数
    """
    # TODO: 贝尔曼更新
    pass


def value_iteration(
    rewards: np.ndarray,
    transition_prob: np.ndarray,
    beta: float,
    tolerance: float = 1e-6,
    max_iterations: int = 1000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    价值迭代算法求解最优策略。

    参数:
        rewards: 奖励矩阵 (n_states × n_actions)
        transition_prob: 转移概率 (n_states × n_actions × n_states)
        beta: 折现因子
        tolerance: 收敛容差
        max_iterations: 最大迭代次数

    返回:
        (最优价值函数, 最优策略)
    """
    # TODO: 价值迭代
    pass


def q_learning_update(
    q_value: float,
    reward: float,
    next_max_q: float,
    alpha: float,
    gamma: float
) -> float:
    """
    Q-learning单步更新。

    Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]

    参数:
        q_value: 当前Q值
        reward: 获得的奖励
        next_max_q: 下一状态的最大Q值
        alpha: 学习率
        gamma: 折现因子

    返回:
        更新后的Q值
    """
    # TODO: Q-learning更新
    pass


def epsilon_greedy_action(
    q_values: np.ndarray,
    epsilon: float,
    seed: int = None
) -> int:
    """
    ε-贪婪策略选择动作。

    以概率ε随机探索，以概率1-ε选择最优动作。

    参数:
        q_values: 各动作的Q值
        epsilon: 探索概率
        seed: 随机种子

    返回:
        选择的动作索引
    """
    # TODO: ε-贪婪
    pass


def consumption_savings_reward(
    consumption: float,
    gamma: float = 2.0
) -> float:
    """
    CRRA效用函数作为奖励。

    u(c) = c^(1-γ) / (1-γ), γ ≠ 1
    u(c) = ln(c), γ = 1

    参数:
        consumption: 消费量
        gamma: 风险厌恶系数

    返回:
        效用值
    """
    # TODO: CRRA效用
    pass


def optimal_savings_rate(
    wealth: float,
    income: float,
    interest_rate: float,
    beta: float,
    gamma: float
) -> float:
    """
    欧拉方程隐含的最优储蓄率（简化版）。

    在CRRA效用下的最优储蓄决策。

    参数:
        wealth: 当前财富
        income: 收入
        interest_rate: 利率
        beta: 折现因子
        gamma: 风险厌恶系数

    返回:
        最优储蓄率
    """
    # TODO: 计算最优储蓄率
    pass


def temporal_difference_error(
    reward: float,
    value_current: float,
    value_next: float,
    gamma: float
) -> float:
    """
    计算时序差分误差（TD error）。

    δ = r + γV(s') - V(s)

    参数:
        reward: 奖励
        value_current: 当前状态价值
        value_next: 下一状态价值
        gamma: 折现因子

    返回:
        TD误差
    """
    # TODO: 计算TD误差
    pass


def discount_sum(rewards: np.ndarray, gamma: float) -> float:
    """
    计算折现奖励总和。

    G = Σ γ^t × r_t

    参数:
        rewards: 奖励序列
        gamma: 折现因子

    返回:
        折现总和
    """
    # TODO: 计算折现和
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
