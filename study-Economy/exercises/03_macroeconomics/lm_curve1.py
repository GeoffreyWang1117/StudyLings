# EXERCISE: lm_curve1
# DIFFICULTY: ★★★☆☆
# TOPIC: LM曲线
#
# 说明：
# LM曲线表示货币市场均衡时，利率与产出的组合。
#
# 货币市场均衡：货币供给 = 货币需求
# M/P = L(Y, r)
#
# 货币需求函数：
# L = kY - hr
#
# 其中：
# - k: 货币需求的收入敏感度
# - h: 货币需求的利率敏感度
# - M: 名义货币供给
# - P: 价格水平
#
# LM曲线推导：
# M/P = kY - hr
# hr = kY - M/P
# r = (k/h)Y - (1/h)(M/P)
#
# LM曲线是向右上方倾斜的（利率与产出正相关）
#
# 任务：
# 1. 推导LM曲线
# 2. 计算LM曲线的斜率
# 3. 分析货币政策如何移动LM曲线
#
# HINT1: LM曲线斜率 = k/h
# HINT2: 扩张性货币政策（增加M）使LM曲线右移


def lm_curve_interest_rate(
    y: float,
    m: float,
    p: float,
    k: float,
    h: float
) -> float:
    """
    给定产出，计算LM曲线上的利率水平。

    r = (k/h)Y - (1/h)(M/P)

    参数:
        y: 产出水平
        m: 名义货币供给
        p: 价格水平
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        利率 r
    """
    # TODO: 计算LM曲线上的利率
    pass


def lm_curve_output(
    r: float,
    m: float,
    p: float,
    k: float,
    h: float
) -> float:
    """
    给定利率，计算LM曲线上的产出水平。

    Y = (h/k)r + (1/k)(M/P)

    参数:
        r: 利率
        m: 名义货币供给
        p: 价格水平
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        产出水平 Y
    """
    # TODO: 计算LM曲线上的产出
    pass


def lm_curve_slope(k: float, h: float) -> float:
    """
    计算LM曲线的斜率（dr/dY）。

    斜率 = k / h

    参数:
        k: 货币需求收入敏感度
        h: 货币需求利率敏感度

    返回:
        LM曲线斜率（正数）
    """
    # TODO: 计算LM曲线斜率
    pass


def money_demand(y: float, r: float, k: float, h: float) -> float:
    """
    计算货币需求。

    L = kY - hr

    参数:
        y: 产出水平
        r: 利率
        k: 收入敏感度
        h: 利率敏感度

    返回:
        货币需求
    """
    # TODO: 计算货币需求
    pass


def real_money_supply(m: float, p: float) -> float:
    """
    计算实际货币供给。

    M/P

    参数:
        m: 名义货币供给
        p: 价格水平

    返回:
        实际货币供给
    """
    # TODO: 计算实际货币供给
    pass


def lm_shift_from_money_supply(delta_m: float, p: float, k: float) -> float:
    """
    计算货币供给变化导致的LM曲线水平移动距离。

    水平移动 = ΔM / (P × k)

    参数:
        delta_m: 名义货币供给变化
        p: 价格水平
        k: 货币需求收入敏感度

    返回:
        LM曲线水平移动距离
    """
    # TODO: 计算LM曲线移动
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
