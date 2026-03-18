# EXERCISE: game_theory1
# DIFFICULTY: ★★★☆☆
# TOPIC: 博弈论基础（囚徒困境）
#
# 说明：
# 博弈论研究策略性互动，即一个人的最优决策取决于他人的决策。
#
# 囚徒困境是最著名的博弈之一：
# 两个嫌疑人被分开审讯，每人可以选择"合作"（保持沉默）或"背叛"（认罪）。
#
# 收益矩阵（以被告A的收益为例，年数越少越好，用负数表示）：
#                    被告B
#                合作      背叛
# 被告A  合作   (-1,-1)   (-3,0)
#        背叛   (0,-3)    (-2,-2)
#
# 特点：
# - 个体理性导致集体非理性
# - 存在唯一的纳什均衡（双方都背叛）
# - 但双方合作的结果更好
#
# 任务：
# 1. 实现收益矩阵
# 2. 找到占优策略
# 3. 分析囚徒困境的纳什均衡
#
# HINT1: 占优策略是无论对方选什么，自己的最优选择
# HINT2: 纳什均衡是没有人想单独改变策略的状态

import numpy as np
from typing import Optional


def create_prisoners_dilemma_payoff() -> np.ndarray:
    """
    创建囚徒困境的收益矩阵。

    返回形状为 (2, 2, 2) 的数组：
    - 第一维：玩家A的策略 (0=合作, 1=背叛)
    - 第二维：玩家B的策略 (0=合作, 1=背叛)
    - 第三维：(玩家A的收益, 玩家B的收益)

    收益矩阵（负数表示服刑年数）：
    (合作, 合作): (-1, -1)
    (合作, 背叛): (-3, 0)
    (背叛, 合作): (0, -3)
    (背叛, 背叛): (-2, -2)

    返回:
        收益矩阵
    """
    # TODO: 创建收益矩阵
    pass


def get_payoff(payoff_matrix: np.ndarray,
               strategy_a: int,
               strategy_b: int) -> tuple[float, float]:
    """
    获取给定策略组合下两位玩家的收益。

    参数:
        payoff_matrix: 收益矩阵
        strategy_a: 玩家A的策略 (0=合作, 1=背叛)
        strategy_b: 玩家B的策略 (0=合作, 1=背叛)

    返回:
        (玩家A的收益, 玩家B的收益)
    """
    # TODO: 获取收益
    pass


def find_dominant_strategy(payoff_matrix: np.ndarray, player: int) -> Optional[int]:
    """
    找到某玩家的占优策略。

    占优策略：无论对手选什么，这个策略总是最优的。

    参数:
        payoff_matrix: 收益矩阵
        player: 玩家编号 (0=A, 1=B)

    返回:
        占优策略 (0=合作, 1=背叛)，如果没有则返回 None
    """
    # TODO: 找到占优策略
    # 提示：比较每种策略在对手所有可能选择下的收益
    pass


def is_nash_equilibrium(payoff_matrix: np.ndarray,
                        strategy_a: int,
                        strategy_b: int) -> bool:
    """
    判断给定策略组合是否为纳什均衡。

    纳什均衡：给定对方策略，没有人想单独改变自己的策略。

    参数:
        payoff_matrix: 收益矩阵
        strategy_a: 玩家A的策略
        strategy_b: 玩家B的策略

    返回:
        是否为纳什均衡
    """
    # TODO: 判断纳什均衡
    pass


def find_all_nash_equilibria(payoff_matrix: np.ndarray) -> list[tuple[int, int]]:
    """
    找到所有纳什均衡。

    参数:
        payoff_matrix: 收益矩阵

    返回:
        所有纳什均衡的列表 [(策略A, 策略B), ...]
    """
    # TODO: 找到所有纳什均衡
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
