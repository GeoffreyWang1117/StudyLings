# EXERCISE: time_value1
# DIFFICULTY: ★★☆☆☆
# TOPIC: 货币时间价值
#
# 说明：
# 货币时间价值是金融学的基础概念。
# 今天的一元钱比明天的一元钱更有价值。
#
# 终值（Future Value）：
# FV = PV × (1 + r)^n
#
# 现值（Present Value）：
# PV = FV / (1 + r)^n
#
# 年金终值：
# FV_annuity = PMT × [(1 + r)^n - 1] / r
#
# 年金现值：
# PV_annuity = PMT × [1 - (1 + r)^(-n)] / r
#
# 任务：
# 1. 计算终值和现值
# 2. 计算年金的终值和现值
# 3. 理解折现的概念
#
# HINT1: 复利计算使用指数函数
# HINT2: 年金是等额定期支付的现金流

import numpy as np


def future_value(pv: float, r: float, n: int) -> float:
    """
    计算终值。

    FV = PV × (1 + r)^n

    参数:
        pv: 现值
        r: 利率（每期）
        n: 期数

    返回:
        终值
    """
    # TODO: 计算终值
    pass


def present_value(fv: float, r: float, n: int) -> float:
    """
    计算现值。

    PV = FV / (1 + r)^n

    参数:
        fv: 终值
        r: 利率（每期）
        n: 期数

    返回:
        现值
    """
    # TODO: 计算现值
    pass


def annuity_future_value(pmt: float, r: float, n: int) -> float:
    """
    计算年金终值。

    FV = PMT × [(1 + r)^n - 1] / r

    参数:
        pmt: 每期支付金额
        r: 利率（每期）
        n: 期数

    返回:
        年金终值
    """
    # TODO: 计算年金终值
    pass


def annuity_present_value(pmt: float, r: float, n: int) -> float:
    """
    计算年金现值。

    PV = PMT × [1 - (1 + r)^(-n)] / r

    参数:
        pmt: 每期支付金额
        r: 利率（每期）
        n: 期数

    返回:
        年金现值
    """
    # TODO: 计算年金现值
    pass


def perpetuity_present_value(pmt: float, r: float) -> float:
    """
    计算永续年金现值。

    PV = PMT / r

    参数:
        pmt: 每期支付金额
        r: 利率

    返回:
        永续年金现值
    """
    # TODO: 计算永续年金现值
    pass


def effective_annual_rate(nominal_rate: float, m: int) -> float:
    """
    计算有效年利率。

    EAR = (1 + r_nominal/m)^m - 1

    参数:
        nominal_rate: 名义年利率
        m: 每年复利次数

    返回:
        有效年利率
    """
    # TODO: 计算有效年利率
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
