# EXERCISE: consumer_choice1
# DIFFICULTY: ★★★☆☆
# TOPIC: 消费者最优选择
#
# 说明：
# 消费者最优选择是在预算约束下最大化效用的商品组合。
#
# 对于柯布-道格拉斯效用 U(x,y) = x^α * y^β：
# 最优条件：MRS = Px/Py
# 即：(α/β) * (y/x) = Px/Py
#
# 结合预算约束 Px*x + Py*y = M：
# 最优解：
# x* = (α / (α + β)) * (M / Px)
# y* = (β / (α + β)) * (M / Py)
#
# 任务：
# 1. 计算最优消费组合
# 2. 计算最优效用水平
# 3. 分析价格变化对最优选择的影响
#
# HINT1: 在最优点，无差异曲线与预算线相切
# HINT2: 柯布-道格拉斯效用下，支出份额等于指数份额

import numpy as np


def optimal_consumption(
    alpha: float,
    beta: float,
    px: float,
    py: float,
    income: float
) -> tuple[float, float]:
    """
    计算最优消费组合。

    对于 U(x,y) = x^α * y^β：
    x* = (α / (α + β)) * (M / Px)
    y* = (β / (α + β)) * (M / Py)

    参数:
        alpha, beta: 效用函数参数
        px, py: 商品价格
        income: 收入

    返回:
        (最优x, 最优y)
    """
    # TODO: 计算最优消费组合
    pass


def optimal_utility(
    alpha: float,
    beta: float,
    px: float,
    py: float,
    income: float
) -> float:
    """
    计算最优效用水平。

    参数:
        alpha, beta: 效用函数参数
        px, py: 商品价格
        income: 收入

    返回:
        最优效用值
    """
    # TODO: 计算最优效用
    # 提示：先计算最优x和y，再代入效用函数
    pass


def expenditure_share(alpha: float, beta: float) -> tuple[float, float]:
    """
    计算各商品的支出份额。

    对于柯布-道格拉斯效用，支出份额等于指数份额：
    商品X支出份额 = α / (α + β)
    商品Y支出份额 = β / (α + β)

    参数:
        alpha, beta: 效用函数参数

    返回:
        (X支出份额, Y支出份额)
    """
    # TODO: 计算支出份额
    pass


def price_effect_on_x(
    alpha: float,
    beta: float,
    px_old: float,
    px_new: float,
    py: float,
    income: float
) -> float:
    """
    计算商品X价格变化导致的X消费量变化。

    参数:
        alpha, beta: 效用函数参数
        px_old, px_new: X的旧价格和新价格
        py: Y的价格
        income: 收入

    返回:
        X消费量的变化（新 - 旧）
    """
    # TODO: 计算价格效应
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
