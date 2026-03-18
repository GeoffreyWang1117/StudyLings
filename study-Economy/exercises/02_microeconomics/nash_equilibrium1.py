# EXERCISE: nash_equilibrium1
# DIFFICULTY: ★★★★☆
# TOPIC: 纳什均衡
#
# 说明：
# 纳什均衡是博弈论中最重要的解概念。
#
# 纳什均衡定义：
# 给定其他玩家的策略，每个玩家都在选择自己的最优策略。
# 换言之，没有任何玩家有动机单方面改变策略。
#
# 常见的2x2博弈：
#
# 1. 协调博弈（如选择开车靠左还是靠右）：
#    有多个纳什均衡，需要协调
#
# 2. 性别之战（如夫妻选择去看足球还是歌剧）：
#    存在两个纯策略纳什均衡
#
# 3. 匹配硬币（如零和博弈）：
#    可能没有纯策略纳什均衡，但存在混合策略均衡
#
# 任务：
# 1. 实现最优响应函数
# 2. 通过迭代找到纳什均衡
# 3. 分析不同类型的博弈
#
# HINT1: 最优响应是给定对手策略时的最佳策略
# HINT2: 纳什均衡是双方互为最优响应的策略组合

import numpy as np
from typing import Optional


def best_response(payoff_matrix: np.ndarray,
                  player: int,
                  opponent_strategy: int) -> int:
    """
    计算玩家对对手策略的最优响应。

    参数:
        payoff_matrix: 收益矩阵 (形状: 2x2x2)
        player: 玩家编号 (0 或 1)
        opponent_strategy: 对手的策略 (0 或 1)

    返回:
        最优响应策略 (0 或 1)
    """
    # TODO: 计算最优响应
    pass


def create_coordination_game() -> np.ndarray:
    """
    创建协调博弈的收益矩阵。

    协调博弈（开车靠左还是靠右）：
              玩家B
             左    右
    玩家A 左 (1,1) (0,0)
          右 (0,0) (1,1)

    返回:
        收益矩阵
    """
    # TODO: 创建协调博弈矩阵
    pass


def create_battle_of_sexes() -> np.ndarray:
    """
    创建性别之战的收益矩阵。

    性别之战（夫妻选择活动）：
                  妻子
                足球    歌剧
    丈夫  足球  (3,2)   (0,0)
          歌剧  (0,0)   (2,3)

    返回:
        收益矩阵
    """
    # TODO: 创建性别之战矩阵
    pass


def create_matching_pennies() -> np.ndarray:
    """
    创建匹配硬币博弈的收益矩阵。

    匹配硬币（零和博弈）：
              玩家B
             正面    反面
    玩家A 正面 (1,-1) (-1,1)
          反面 (-1,1) (1,-1)

    返回:
        收益矩阵
    """
    # TODO: 创建匹配硬币矩阵
    pass


def find_pure_nash_equilibria(payoff_matrix: np.ndarray) -> list[tuple[int, int]]:
    """
    找到所有纯策略纳什均衡。

    参数:
        payoff_matrix: 收益矩阵

    返回:
        纯策略纳什均衡列表
    """
    # TODO: 找到所有纯策略纳什均衡
    pass


def mixed_strategy_nash_2x2(payoff_matrix: np.ndarray) -> Optional[tuple[float, float]]:
    """
    计算2x2博弈的混合策略纳什均衡。

    对于2x2博弈，如果存在完全混合策略均衡，可以通过让对手无差异来求解。

    玩家A选择策略0的概率为p，使得玩家B对两种策略无差异：
    p * B(0,0) + (1-p) * B(1,0) = p * B(0,1) + (1-p) * B(1,1)

    参数:
        payoff_matrix: 收益矩阵

    返回:
        (玩家A选策略0的概率, 玩家B选策略0的概率)
        如果不存在完全混合策略均衡，返回 None
    """
    # TODO: 计算混合策略纳什均衡
    # 提示：通过让对手无差异来求解混合策略
    pass


def expected_payoff_mixed(payoff_matrix: np.ndarray,
                         p_a: float,
                         p_b: float) -> tuple[float, float]:
    """
    计算混合策略下的期望收益。

    参数:
        payoff_matrix: 收益矩阵
        p_a: 玩家A选策略0的概率
        p_b: 玩家B选策略0的概率

    返回:
        (玩家A的期望收益, 玩家B的期望收益)
    """
    # TODO: 计算期望收益
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
