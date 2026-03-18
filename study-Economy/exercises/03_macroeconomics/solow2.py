# EXERCISE: solow2
# DIFFICULTY: ★★★★☆
# TOPIC: 稳态分析
#
# 说明：
# 稳态分析是索洛模型的核心。
#
# 稳态特征：
# 1. 人均资本 k 不再变化
# 2. 人均产出 y 不再变化
# 3. 总产出 Y 以人口增长率 n 增长
#
# 黄金律稳态（Golden Rule）：
# 使稳态消费最大化的储蓄率
# c* = y* - (δ + n)k*
#
# dc*/dk* = 0
# → dy*/dk* = δ + n
# → αA(k*)^(α-1) = δ + n
# → MPK = δ + n
#
# 黄金律储蓄率：s_gold = α
#
# 任务：
# 1. 分析储蓄率对稳态的影响
# 2. 计算黄金律稳态
# 3. 判断经济是否过度储蓄
#
# HINT1: 储蓄率越高，稳态资本越高，但消费不一定越高
# HINT2: 黄金律条件：MPK = δ + n

import numpy as np


def steady_state_consumption(
    s: float,
    a: float,
    delta: float,
    n: float,
    alpha: float
) -> float:
    """
    计算稳态人均消费。

    c* = (1 - s) * y*
       = (1 - s) * A * [sA / (δ + n)]^(α/(1-α))

    参数:
        s, a, delta, n, alpha: 模型参数

    返回:
        稳态人均消费
    """
    # TODO: 计算稳态消费
    pass


def golden_rule_savings_rate(alpha: float) -> float:
    """
    计算黄金律储蓄率。

    s_gold = α

    参数:
        alpha: 资本份额

    返回:
        黄金律储蓄率
    """
    # TODO: 返回黄金律储蓄率
    pass


def golden_rule_capital(
    a: float,
    delta: float,
    n: float,
    alpha: float
) -> float:
    """
    计算黄金律稳态资本。

    使用 s = α 计算稳态资本

    参数:
        a, delta, n, alpha: 模型参数

    返回:
        黄金律人均资本
    """
    # TODO: 计算黄金律资本
    pass


def marginal_product_of_capital(k: float, a: float, alpha: float) -> float:
    """
    计算资本边际产出。

    MPK = αA * k^(α-1)

    参数:
        k: 人均资本
        a: 全要素生产率
        alpha: 资本份额

    返回:
        资本边际产出
    """
    # TODO: 计算MPK
    pass


def is_dynamically_efficient(mpk: float, delta: float, n: float) -> bool:
    """
    判断经济是否动态有效。

    动态有效：MPK > δ + n（不过度储蓄）
    动态无效：MPK < δ + n（过度储蓄）

    参数:
        mpk: 资本边际产出
        delta: 折旧率
        n: 人口增长率

    返回:
        如果动态有效返回 True
    """
    # TODO: 判断动态效率
    pass


def convergence_speed(delta: float, n: float, alpha: float) -> float:
    """
    计算向稳态收敛的速度。

    收敛速度 λ = (1 - α)(δ + n)

    参数:
        delta: 折旧率
        n: 人口增长率
        alpha: 资本份额

    返回:
        收敛速度（每期缺口缩小的比例）
    """
    # TODO: 计算收敛速度
    pass


def years_to_half_convergence(lambda_: float) -> float:
    """
    计算半衰期（缺口缩小一半所需时间）。

    半衰期 = ln(2) / λ

    参数:
        lambda_: 收敛速度

    返回:
        半衰期（年）
    """
    # TODO: 计算半衰期
    pass


def simulate_transition(
    k0: float,
    s: float,
    a: float,
    delta: float,
    n: float,
    alpha: float,
    periods: int
) -> list[float]:
    """
    模拟向稳态的过渡过程。

    参数:
        k0: 初始人均资本
        s, a, delta, n, alpha: 模型参数
        periods: 模拟期数

    返回:
        各期人均资本的列表
    """
    # TODO: 模拟过渡过程
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
