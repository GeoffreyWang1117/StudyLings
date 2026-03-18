# EXERCISE: production1
# DIFFICULTY: ★★★☆☆
# TOPIC: 生产函数（柯布-道格拉斯）
#
# 说明：
# 生产函数描述了投入要素与产出之间的技术关系。
#
# 柯布-道格拉斯生产函数：
# Q = A * L^α * K^β
#
# 其中：
# - Q: 产出
# - A: 全要素生产率 (TFP)
# - L: 劳动投入
# - K: 资本投入
# - α: 劳动的产出弹性
# - β: 资本的产出弹性
#
# 规模报酬：
# - α + β > 1: 规模报酬递增
# - α + β = 1: 规模报酬不变
# - α + β < 1: 规模报酬递减
#
# 边际产出：
# MPL = ∂Q/∂L = α * A * L^(α-1) * K^β = α * Q / L
# MPK = ∂Q/∂K = β * A * L^α * K^(β-1) = β * Q / K
#
# 任务：
# 1. 实现柯布-道格拉斯生产函数
# 2. 计算边际产出
# 3. 判断规模报酬类型
#
# HINT1: 规模报酬看 α + β 与 1 的关系
# HINT2: 边际产出 = 产出弹性 × 平均产出

import numpy as np


def cobb_douglas_production(
    labor: float,
    capital: float,
    a: float,
    alpha: float,
    beta: float
) -> float:
    """
    柯布-道格拉斯生产函数。

    Q = A * L^α * K^β

    参数:
        labor: 劳动投入 L
        capital: 资本投入 K
        a: 全要素生产率 A
        alpha: 劳动的产出弹性
        beta: 资本的产出弹性

    返回:
        产出 Q
    """
    # TODO: 实现生产函数
    pass


def marginal_product_labor(
    labor: float,
    capital: float,
    a: float,
    alpha: float,
    beta: float
) -> float:
    """
    计算劳动的边际产出 (MPL)。

    MPL = α * A * L^(α-1) * K^β

    参数:
        labor, capital: 要素投入
        a, alpha, beta: 生产函数参数

    返回:
        劳动的边际产出
    """
    # TODO: 计算MPL
    pass


def marginal_product_capital(
    labor: float,
    capital: float,
    a: float,
    alpha: float,
    beta: float
) -> float:
    """
    计算资本的边际产出 (MPK)。

    MPK = β * A * L^α * K^(β-1)

    参数:
        labor, capital: 要素投入
        a, alpha, beta: 生产函数参数

    返回:
        资本的边际产出
    """
    # TODO: 计算MPK
    pass


def returns_to_scale(alpha: float, beta: float) -> str:
    """
    判断规模报酬类型。

    参数:
        alpha: 劳动的产出弹性
        beta: 资本的产出弹性

    返回:
        "increasing" (递增), "constant" (不变), 或 "decreasing" (递减)
    """
    # TODO: 判断规模报酬
    pass


def technical_rate_of_substitution(
    labor: float,
    capital: float,
    alpha: float,
    beta: float
) -> float:
    """
    计算技术替代率 (MRTS)。

    MRTS = MPL / MPK = (α/β) * (K/L)

    表示保持产出不变，用多少资本替代一单位劳动。

    参数:
        labor, capital: 要素投入
        alpha, beta: 产出弹性

    返回:
        技术替代率
    """
    # TODO: 计算MRTS
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
