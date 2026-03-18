# EXERCISE: utility2
# DIFFICULTY: ★★☆☆☆
# TOPIC: 边际效用递减
#
# 说明：
# 边际效用 (Marginal Utility) 是消费额外一单位商品带来的效用增加。
# 边际效用递减法则：随着消费量增加，每额外一单位带来的效用增加会减少。
#
# 对于效用函数 U(x)：
# 边际效用 MU = dU/dx
#
# 对于柯布-道格拉斯效用 U(x,y) = x^α * y^β：
# MUx = α * x^(α-1) * y^β = α * U(x,y) / x
# MUy = β * x^α * y^(β-1) = β * U(x,y) / y
#
# 任务：
# 1. 计算边际效用
# 2. 验证边际效用递减
# 3. 计算边际替代率 MRS
#
# HINT1: MRS = MUx / MUy
# HINT2: MRS 表示为保持效用不变，愿意用多少Y换取1单位X

import numpy as np


def marginal_utility_x(x: float, y: float, alpha: float, beta: float) -> float:
    """
    计算商品X的边际效用（柯布-道格拉斯效用函数）。

    MUx = α * x^(α-1) * y^β

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        商品X的边际效用
    """
    # TODO: 计算商品X的边际效用
    pass


def marginal_utility_y(x: float, y: float, alpha: float, beta: float) -> float:
    """
    计算商品Y的边际效用（柯布-道格拉斯效用函数）。

    MUy = β * x^α * y^(β-1)

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        商品Y的边际效用
    """
    # TODO: 计算商品Y的边际效用
    pass


def marginal_rate_of_substitution(x: float, y: float, alpha: float, beta: float) -> float:
    """
    计算边际替代率 (MRS)。

    MRS = MUx / MUy = (α/β) * (y/x)

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        边际替代率
    """
    # TODO: 计算边际替代率
    pass


def is_diminishing_mu(utilities: list[float]) -> bool:
    """
    检验边际效用是否递减。

    参数:
        utilities: 随消费量增加的边际效用序列

    返回:
        如果边际效用严格递减返回 True
    """
    # TODO: 检验边际效用递减
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
