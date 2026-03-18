# EXERCISE: cost1
# DIFFICULTY: ★★★☆☆
# TOPIC: 成本函数
#
# 说明：
# 成本函数描述了生产一定产量所需的最小成本。
#
# 成本类型：
# - 固定成本 (FC): 不随产量变化的成本
# - 可变成本 (VC): 随产量变化的成本
# - 总成本 (TC): TC = FC + VC
#
# 平均成本：
# - 平均固定成本 (AFC): AFC = FC / Q
# - 平均可变成本 (AVC): AVC = VC / Q
# - 平均总成本 (ATC): ATC = TC / Q = AFC + AVC
#
# 边际成本 (MC): MC = dTC/dQ = dVC/dQ
#
# 典型成本函数形式：
# TC(Q) = FC + a*Q + b*Q² + c*Q³
#
# 任务：
# 1. 计算各种成本
# 2. 找到平均成本最小化产量
# 3. 理解MC与ATC的关系
#
# HINT1: 当 MC = ATC 时，ATC 达到最小值
# HINT2: 边际成本曲线穿过平均成本曲线的最低点

import numpy as np


def total_cost(q: float, fc: float, a: float, b: float, c: float) -> float:
    """
    计算总成本。

    TC(Q) = FC + a*Q + b*Q² + c*Q³

    参数:
        q: 产量
        fc: 固定成本
        a, b, c: 可变成本系数

    返回:
        总成本
    """
    # TODO: 计算总成本
    pass


def variable_cost(q: float, a: float, b: float, c: float) -> float:
    """
    计算可变成本。

    VC(Q) = a*Q + b*Q² + c*Q³

    参数:
        q: 产量
        a, b, c: 可变成本系数

    返回:
        可变成本
    """
    # TODO: 计算可变成本
    pass


def marginal_cost(q: float, a: float, b: float, c: float) -> float:
    """
    计算边际成本。

    MC = dTC/dQ = a + 2b*Q + 3c*Q²

    参数:
        q: 产量
        a, b, c: 可变成本系数

    返回:
        边际成本
    """
    # TODO: 计算边际成本
    pass


def average_total_cost(q: float, fc: float, a: float, b: float, c: float) -> float:
    """
    计算平均总成本。

    ATC = TC / Q

    参数:
        q: 产量
        fc: 固定成本
        a, b, c: 可变成本系数

    返回:
        平均总成本
    """
    # TODO: 计算平均总成本
    pass


def average_variable_cost(q: float, a: float, b: float, c: float) -> float:
    """
    计算平均可变成本。

    AVC = VC / Q = a + b*Q + c*Q²

    参数:
        q: 产量
        a, b, c: 可变成本系数

    返回:
        平均可变成本
    """
    # TODO: 计算平均可变成本
    pass


def find_min_atc_quantity(fc: float, a: float, b: float, c: float,
                          q_range: tuple[float, float] = (0.1, 100)) -> float:
    """
    找到平均总成本最小化的产量。

    提示：可以使用数值方法在给定范围内搜索

    参数:
        fc: 固定成本
        a, b, c: 可变成本系数
        q_range: 搜索范围

    返回:
        使ATC最小的产量
    """
    # TODO: 找到ATC最小化产量
    # 提示：可以遍历范围内的值，找到ATC最小的点
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
