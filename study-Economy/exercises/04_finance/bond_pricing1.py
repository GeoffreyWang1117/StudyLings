# EXERCISE: bond_pricing1
# DIFFICULTY: ★★★☆☆
# TOPIC: 债券定价
#
# 说明：
# 债券价格是未来现金流的现值。
#
# 债券价格：
# P = Σ [C / (1+r)^t] + [F / (1+r)^n]
#
# 其中：
# - C: 每期票息（= 面值 × 票息率 / 付息频率）
# - F: 面值
# - r: 每期收益率
# - n: 期数
#
# 到期收益率（YTM）：
# 使债券价格等于现值的折现率
#
# 久期（Duration）：
# 衡量债券价格对利率变化的敏感度
# Macaulay Duration = Σ [t × PV(CFt)] / P
#
# 任务：
# 1. 计算债券价格
# 2. 计算到期收益率
# 3. 计算久期和凸性
#
# HINT1: 债券价格与收益率反向变动
# HINT2: 久期越长，利率风险越大

import numpy as np
from typing import Optional


def bond_price(face_value: float, coupon_rate: float, ytm: float, years: int, frequency: int = 2) -> float:
    """
    计算债券价格。

    P = Σ [C / (1+r)^t] + [F / (1+r)^n]

    参数:
        face_value: 面值
        coupon_rate: 年票息率
        ytm: 年化到期收益率
        years: 到期年限
        frequency: 每年付息次数（默认半年付息）

    返回:
        债券价格
    """
    # TODO: 计算债券价格
    pass


def zero_coupon_bond_price(face_value: float, ytm: float, years: int) -> float:
    """
    计算零息债券价格。

    P = F / (1 + r)^n

    参数:
        face_value: 面值
        ytm: 到期收益率
        years: 到期年限

    返回:
        债券价格
    """
    # TODO: 计算零息债券价格
    pass


def current_yield(coupon_rate: float, face_value: float, price: float) -> float:
    """
    计算当期收益率。

    Current Yield = 年票息 / 价格

    参数:
        coupon_rate: 票息率
        face_value: 面值
        price: 当前价格

    返回:
        当期收益率
    """
    # TODO: 计算当期收益率
    pass


def ytm_approximation(
    face_value: float,
    coupon_rate: float,
    price: float,
    years: int
) -> float:
    """
    估算到期收益率（近似公式）。

    YTM ≈ [C + (F - P) / n] / [(F + P) / 2]

    参数:
        face_value: 面值
        coupon_rate: 票息率
        price: 当前价格
        years: 到期年限

    返回:
        估算的YTM
    """
    # TODO: 估算YTM
    pass


def macaulay_duration(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years: int,
    frequency: int = 2
) -> float:
    """
    计算麦考利久期。

    D = Σ [t × PV(CFt)] / P

    参数:
        face_value: 面值
        coupon_rate: 票息率
        ytm: 到期收益率
        years: 到期年限
        frequency: 付息频率

    返回:
        麦考利久期（年）
    """
    # TODO: 计算麦考利久期
    pass


def modified_duration(macaulay_dur: float, ytm: float, frequency: int = 2) -> float:
    """
    计算修正久期。

    D* = D / (1 + r/m)

    参数:
        macaulay_dur: 麦考利久期
        ytm: 年化到期收益率
        frequency: 付息频率

    返回:
        修正久期
    """
    # TODO: 计算修正久期
    pass


def price_change_from_duration(
    modified_dur: float,
    price: float,
    yield_change: float
) -> float:
    """
    使用久期估算价格变化。

    ΔP ≈ -D* × P × Δy

    参数:
        modified_dur: 修正久期
        price: 当前价格
        yield_change: 收益率变化

    返回:
        价格变化
    """
    # TODO: 计算价格变化
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
