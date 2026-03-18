# EXERCISE: monopoly1
# DIFFICULTY: ★★★★☆
# TOPIC: 垄断定价
#
# 说明：
# 垄断者是市场上唯一的卖家，可以选择价格或产量。
#
# 垄断者面临向下倾斜的需求曲线：
# P = a - b*Q (反需求函数)
#
# 总收益：TR = P*Q = (a - b*Q)*Q = a*Q - b*Q²
# 边际收益：MR = dTR/dQ = a - 2b*Q
#
# 注意：MR 曲线斜率是需求曲线斜率的两倍！
#
# 利润最大化：MR = MC
# a - 2b*Q = MC
# Q* = (a - MC) / (2b)
# P* = a - b*Q*
#
# 垄断导致：
# - 产量低于竞争水平
# - 价格高于竞争水平
# - 产生无谓损失
#
# 任务：
# 1. 计算垄断者的MR
# 2. 找到利润最大化价格和产量
# 3. 计算垄断利润和无谓损失
#
# HINT1: 反需求函数 P = a - bQ 对应的 MR = a - 2bQ
# HINT2: 无谓损失是垄断导致的社会福利损失

import numpy as np


def inverse_demand(q: float, a: float, b: float) -> float:
    """
    反需求函数：给定数量，返回价格。

    P = a - b*Q

    参数:
        q: 数量
        a: 截距
        b: 斜率

    返回:
        价格
    """
    # TODO: 实现反需求函数
    pass


def marginal_revenue_monopoly(q: float, a: float, b: float) -> float:
    """
    计算垄断者的边际收益。

    MR = a - 2b*Q

    参数:
        q: 产量
        a, b: 需求函数参数 (P = a - bQ)

    返回:
        边际收益
    """
    # TODO: 计算MR
    pass


def monopoly_quantity(a: float, b: float, mc: float) -> float:
    """
    计算垄断者的最优产量。

    MR = MC
    a - 2b*Q = MC
    Q* = (a - MC) / (2b)

    参数:
        a, b: 需求函数参数
        mc: 边际成本（假设为常数）

    返回:
        最优产量
    """
    # TODO: 计算最优产量
    pass


def monopoly_price(a: float, b: float, mc: float) -> float:
    """
    计算垄断者的最优价格。

    P* = a - b*Q*

    参数:
        a, b: 需求函数参数
        mc: 边际成本

    返回:
        最优价格
    """
    # TODO: 计算最优价格
    pass


def monopoly_profit(a: float, b: float, mc: float, fc: float = 0) -> float:
    """
    计算垄断利润。

    π = (P* - MC) * Q* - FC

    参数:
        a, b: 需求函数参数
        mc: 边际成本
        fc: 固定成本

    返回:
        垄断利润
    """
    # TODO: 计算垄断利润
    pass


def deadweight_loss(a: float, b: float, mc: float) -> float:
    """
    计算垄断造成的无谓损失。

    无谓损失 = 竞争产量与垄断产量之间的三角形面积
    竞争产量 Qc: P = MC, 即 a - bQ = MC, Qc = (a - MC) / b
    垄断产量 Qm = (a - MC) / (2b)

    DWL = 0.5 * (Qc - Qm) * (Pm - MC)

    参数:
        a, b: 需求函数参数
        mc: 边际成本

    返回:
        无谓损失
    """
    # TODO: 计算无谓损失
    pass


def lerner_index(price: float, mc: float) -> float:
    """
    计算勒纳指数（衡量垄断势力）。

    L = (P - MC) / P

    L = 0: 完全竞争
    L = 1: 完全垄断
    0 < L < 1: 中间状态

    参数:
        price: 价格
        mc: 边际成本

    返回:
        勒纳指数
    """
    # TODO: 计算勒纳指数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
