# EXERCISE: is_curve1
# DIFFICULTY: ★★★☆☆
# TOPIC: IS曲线
#
# 说明：
# IS曲线表示产品市场均衡时，利率与产出的组合。
#
# 产品市场均衡：Y = C + I + G
#
# 消费函数: C = C₀ + c(Y - T)
# 投资函数: I = I₀ - d*r
#
# 其中：
# - c: 边际消费倾向
# - d: 投资对利率的敏感度
# - r: 利率
#
# IS曲线推导：
# Y = C₀ + c(Y - T) + I₀ - d*r + G
# Y - cY = C₀ - cT + I₀ - d*r + G
# Y(1 - c) = C₀ - cT + I₀ + G - d*r
# Y = (C₀ - cT + I₀ + G) / (1-c) - (d/(1-c)) * r
#
# IS曲线是向右下方倾斜的（利率与产出负相关）
#
# 任务：
# 1. 推导IS曲线
# 2. 计算IS曲线的斜率
# 3. 分析财政政策如何移动IS曲线
#
# HINT1: IS曲线斜率 = -(1-c)/d
# HINT2: 扩张性财政政策使IS曲线右移


def is_curve_output(
    r: float,
    c0: float,
    c: float,
    t: float,
    i0: float,
    d: float,
    g: float
) -> float:
    """
    给定利率，计算IS曲线上的产出水平。

    Y = (C₀ - cT + I₀ + G) / (1-c) - (d/(1-c)) * r

    参数:
        r: 利率
        c0: 自主消费
        c: 边际消费倾向
        t: 税收
        i0: 自主投资
        d: 投资利率敏感度
        g: 政府支出

    返回:
        产出水平 Y
    """
    # TODO: 计算IS曲线上的产出
    pass


def is_curve_interest_rate(
    y: float,
    c0: float,
    c: float,
    t: float,
    i0: float,
    d: float,
    g: float
) -> float:
    """
    给定产出，计算IS曲线上的利率水平。

    r = (C₀ - cT + I₀ + G - (1-c)Y) / d

    参数:
        y: 产出水平
        c0, c, t, i0, d, g: 模型参数

    返回:
        利率 r
    """
    # TODO: 计算IS曲线上的利率
    pass


def is_curve_slope(c: float, d: float) -> float:
    """
    计算IS曲线的斜率（dr/dY）。

    斜率 = -(1-c) / d

    参数:
        c: 边际消费倾向
        d: 投资利率敏感度

    返回:
        IS曲线斜率（负数）
    """
    # TODO: 计算IS曲线斜率
    pass


def is_shift_from_government_spending(delta_g: float, c: float) -> float:
    """
    计算政府支出变化导致的IS曲线水平移动距离。

    水平移动 = ΔG / (1-c) = k × ΔG

    参数:
        delta_g: 政府支出变化
        c: 边际消费倾向

    返回:
        IS曲线水平移动距离
    """
    # TODO: 计算IS曲线移动
    pass


def investment(i0: float, d: float, r: float) -> float:
    """
    计算投资水平。

    I = I₀ - d*r

    参数:
        i0: 自主投资
        d: 投资利率敏感度
        r: 利率

    返回:
        投资水平
    """
    # TODO: 计算投资
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
