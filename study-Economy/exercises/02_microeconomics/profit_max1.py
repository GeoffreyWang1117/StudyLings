# EXERCISE: profit_max1
# DIFFICULTY: ★★★☆☆
# TOPIC: 利润最大化
#
# 说明：
# 厂商的目标是最大化利润。
#
# 利润 = 总收益 - 总成本
# π = TR - TC = P*Q - TC(Q)
#
# 利润最大化条件：
# dπ/dQ = 0
# MR = MC (边际收益 = 边际成本)
#
# 对于价格接受者（完全竞争市场）：
# P = MR = MC
#
# 对于价格制定者（垄断市场）：
# MR = P + Q*(dP/dQ) = MC
#
# 任务：
# 1. 计算利润
# 2. 找到利润最大化产量
# 3. 分析完全竞争下的最优决策
#
# HINT1: 完全竞争下，价格由市场决定，单个厂商是价格接受者
# HINT2: 利润最大化时 MR = MC

import numpy as np


def profit(price: float, quantity: float, total_cost: float) -> float:
    """
    计算利润。

    π = P*Q - TC

    参数:
        price: 市场价格
        quantity: 产量
        total_cost: 总成本

    返回:
        利润
    """
    # TODO: 计算利润
    pass


def total_revenue(price: float, quantity: float) -> float:
    """
    计算总收益。

    TR = P * Q

    参数:
        price: 价格
        quantity: 产量

    返回:
        总收益
    """
    # TODO: 计算总收益
    pass


def find_profit_max_quantity_competitive(
    price: float,
    fc: float,
    a: float,
    b: float,
    c: float,
    q_range: tuple[float, float] = (0.1, 100)
) -> float:
    """
    找到完全竞争市场下的利润最大化产量。

    在完全竞争市场中：MR = P = MC
    所以需要找到 P = a + 2b*Q + 3c*Q² 的解

    参数:
        price: 市场价格
        fc: 固定成本
        a, b, c: 成本函数系数 (TC = FC + aQ + bQ² + cQ³)
        q_range: 搜索范围

    返回:
        利润最大化产量
    """
    # TODO: 找到利润最大化产量
    # 提示：找到 P = MC 的产量
    pass


def should_produce(price: float, avc_min: float) -> bool:
    """
    判断厂商是否应该生产（短期决策）。

    短期停产条件：P < AVC_min
    如果价格低于最低平均可变成本，应该停产

    参数:
        price: 市场价格
        avc_min: 最低平均可变成本

    返回:
        如果应该生产返回 True
    """
    # TODO: 判断是否应该生产
    pass


def break_even_price(fc: float, a: float, b: float, c: float, q: float) -> float:
    """
    计算盈亏平衡价格。

    盈亏平衡：π = 0, 即 P = ATC

    参数:
        fc: 固定成本
        a, b, c: 成本函数系数
        q: 产量

    返回:
        盈亏平衡价格
    """
    # TODO: 计算盈亏平衡价格
    # 提示：P = TC / Q = ATC
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
