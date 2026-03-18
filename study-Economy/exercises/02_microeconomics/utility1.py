# EXERCISE: utility1
# DIFFICULTY: ★★☆☆☆
# TOPIC: 效用函数
#
# 说明：
# 效用 (Utility) 是消费者从消费商品中获得的满足程度的度量。
# 效用函数 U(x, y) 表示消费 x 单位商品X 和 y 单位商品Y 获得的总效用。
#
# 常见效用函数类型：
# 1. 线性效用: U(x, y) = ax + by
# 2. 柯布-道格拉斯效用: U(x, y) = x^α * y^β
# 3. 完全互补: U(x, y) = min(ax, by)
# 4. 完全替代: U(x, y) = ax + by
#
# 任务：
# 1. 实现柯布-道格拉斯效用函数
# 2. 实现完全互补效用函数
# 3. 实现完全替代效用函数
#
# HINT1: 柯布-道格拉斯中，α和β通常满足α + β = 1
# HINT2: 完全互补品例如：左右脚鞋子

import numpy as np


def cobb_douglas_utility(x: float, y: float, alpha: float, beta: float) -> float:
    """
    柯布-道格拉斯效用函数。

    U(x, y) = x^α * y^β

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        效用值
    """
    # TODO: 实现柯布-道格拉斯效用函数
    pass


def perfect_complements_utility(x: float, y: float, a: float, b: float) -> float:
    """
    完全互补效用函数。

    U(x, y) = min(ax, by)

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        a: 商品X的系数
        b: 商品Y的系数

    返回:
        效用值
    """
    # TODO: 实现完全互补效用函数
    pass


def perfect_substitutes_utility(x: float, y: float, a: float, b: float) -> float:
    """
    完全替代效用函数。

    U(x, y) = ax + by

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        a: 商品X的边际效用
        b: 商品Y的边际效用

    返回:
        效用值
    """
    # TODO: 实现完全替代效用函数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
