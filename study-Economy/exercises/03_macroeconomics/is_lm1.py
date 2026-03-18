# EXERCISE: is_lm1
# DIFFICULTY: ★★★★☆
# TOPIC: IS-LM模型综合
#
# 说明：
# IS-LM模型是凯恩斯宏观经济学的核心模型。
# IS曲线和LM曲线的交点确定均衡产出和均衡利率。
#
# IS曲线: Y = A/(1-c) - (d/(1-c))r
# LM曲线: r = (k/h)Y - (1/h)(M/P)
#
# 其中 A = C₀ - cT + I₀ + G（自主支出）
#
# 联立求解：
# 将LM代入IS，或将IS代入LM
#
# 财政政策效果取决于LM曲线斜率
# 货币政策效果取决于IS曲线斜率
#
# 任务：
# 1. 求解IS-LM均衡
# 2. 分析财政政策效果
# 3. 分析货币政策效果
#
# HINT1: 将LM的r代入IS方程求Y*
# HINT2: 挤出效应：财政扩张提高利率，减少私人投资

import numpy as np


def solve_is_lm(
    c0: float, c: float, t: float, i0: float, d: float, g: float,
    m: float, p: float, k: float, h: float
) -> tuple[float, float]:
    """
    求解IS-LM均衡。

    参数:
        c0: 自主消费
        c: 边际消费倾向
        t: 税收
        i0: 自主投资
        d: 投资利率敏感度
        g: 政府支出
        m: 名义货币供给
        p: 价格水平
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        (均衡产出Y*, 均衡利率r*)
    """
    # TODO: 求解IS-LM均衡
    # 提示：
    # 1. 先计算自主支出 A = c0 - c*t + i0 + g
    # 2. 联立IS和LM方程求解
    pass


def fiscal_policy_effect(
    delta_g: float,
    c: float, d: float,
    k: float, h: float
) -> tuple[float, float]:
    """
    计算财政政策（政府支出变化）的效果。

    参数:
        delta_g: 政府支出变化
        c: 边际消费倾向
        d: 投资利率敏感度
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        (产出变化ΔY, 利率变化Δr)
    """
    # TODO: 计算财政政策效果
    # 财政政策乘数（考虑货币市场反馈）:
    # ΔY/ΔG = 1 / [(1-c) + dk/h]
    pass


def monetary_policy_effect(
    delta_m: float, p: float,
    c: float, d: float,
    k: float, h: float
) -> tuple[float, float]:
    """
    计算货币政策（货币供给变化）的效果。

    参数:
        delta_m: 货币供给变化
        p: 价格水平
        c: 边际消费倾向
        d: 投资利率敏感度
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        (产出变化ΔY, 利率变化Δr)
    """
    # TODO: 计算货币政策效果
    pass


def crowding_out(
    delta_g: float,
    c: float, d: float,
    k: float, h: float
) -> float:
    """
    计算挤出效应（财政扩张导致的私人投资减少）。

    挤出效应 = d × Δr

    参数:
        delta_g: 政府支出变化
        c, d, k, h: 模型参数

    返回:
        被挤出的投资量
    """
    # TODO: 计算挤出效应
    pass


def is_fiscal_more_effective(d: float, k: float, h: float) -> bool:
    """
    判断财政政策是否比货币政策更有效。

    当LM曲线较平坦（h较大或k较小）时，财政政策更有效
    当IS曲线较平坦（d较大）时，货币政策更有效

    参数:
        d: 投资利率敏感度
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        如果财政政策更有效返回True
    """
    # TODO: 比较政策有效性
    # 简化判断：比较 d*k/h 与 1 的关系
    # d*k/h < 1 时财政政策更有效
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
