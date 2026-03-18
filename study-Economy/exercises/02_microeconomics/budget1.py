# EXERCISE: budget1
# DIFFICULTY: ★★☆☆☆
# TOPIC: 预算约束
#
# 说明：
# 预算约束 (Budget Constraint) 描述了消费者在给定收入和价格下能够购买的商品组合。
#
# 预算约束方程：
# Px * x + Py * y = M
#
# 其中：
# - Px: 商品X的价格
# - Py: 商品Y的价格
# - M: 消费者收入（预算）
# - x, y: 商品数量
#
# 预算线：
# y = (M - Px * x) / Py = M/Py - (Px/Py) * x
# 斜率 = -Px/Py
# y轴截距 = M/Py
# x轴截距 = M/Px
#
# 任务：
# 1. 计算预算线上的点
# 2. 计算预算线的斜率
# 3. 判断一个消费组合是否在预算内
#
# HINT1: 预算线斜率反映了两种商品的相对价格
# HINT2: 可行消费组合满足 Px*x + Py*y ≤ M

def budget_line_y(x: float, px: float, py: float, income: float) -> float:
    """
    计算预算线上给定x对应的y值。

    y = (M - Px * x) / Py

    参数:
        x: 商品X的数量
        px: 商品X的价格
        py: 商品Y的价格
        income: 消费者收入

    返回:
        商品Y的数量
    """
    # TODO: 计算预算线上的y值
    pass


def budget_line_slope(px: float, py: float) -> float:
    """
    计算预算线的斜率。

    斜率 = -Px / Py

    参数:
        px: 商品X的价格
        py: 商品Y的价格

    返回:
        预算线斜率
    """
    # TODO: 计算预算线斜率
    pass


def is_affordable(x: float, y: float, px: float, py: float, income: float) -> bool:
    """
    判断消费组合是否在预算内。

    参数:
        x, y: 消费组合
        px, py: 价格
        income: 收入

    返回:
        如果可负担返回 True
    """
    # TODO: 判断是否可负担
    pass


def max_x(px: float, income: float) -> float:
    """
    计算只购买商品X时的最大数量（x轴截距）。

    参数:
        px: 商品X的价格
        income: 收入

    返回:
        最大X数量
    """
    # TODO: 计算x轴截距
    pass


def max_y(py: float, income: float) -> float:
    """
    计算只购买商品Y时的最大数量（y轴截距）。

    参数:
        py: 商品Y的价格
        income: 收入

    返回:
        最大Y数量
    """
    # TODO: 计算y轴截距
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
