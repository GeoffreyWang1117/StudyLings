# EXERCISE: black_scholes1
# DIFFICULTY: ★★★★★
# TOPIC: Black-Scholes期权定价
#
# 说明：
# Black-Scholes模型是期权定价的经典模型。
#
# 欧式看涨期权价格：
# C = S × N(d1) - K × e^(-rT) × N(d2)
#
# 欧式看跌期权价格：
# P = K × e^(-rT) × N(-d2) - S × N(-d1)
#
# 其中：
# d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
# d2 = d1 - σ√T
# N(x) = 标准正态分布累积分布函数
#
# 参数说明：
# - S: 标的资产当前价格
# - K: 执行价格
# - r: 无风险利率
# - T: 到期时间（年）
# - σ: 波动率
#
# 任务：
# 1. 实现Black-Scholes公式
# 2. 理解期权的希腊字母
# 3. 验证看涨-看跌平价关系
#
# HINT1: 使用scipy.stats.norm计算N(x)
# HINT2: 看涨-看跌平价: C - P = S - K×e^(-rT)

import numpy as np
from scipy import stats


def d1(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算 d1。

    d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)

    参数:
        s: 标的资产价格
        k: 执行价格
        r: 无风险利率
        t: 到期时间
        sigma: 波动率

    返回:
        d1值
    """
    # TODO: 计算d1
    pass


def d2(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算 d2。

    d2 = d1 - σ√T

    参数:
        s, k, r, t, sigma: 期权参数

    返回:
        d2值
    """
    # TODO: 计算d2
    pass


def black_scholes_call(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算欧式看涨期权价格。

    C = S × N(d1) - K × e^(-rT) × N(d2)

    参数:
        s: 标的资产价格
        k: 执行价格
        r: 无风险利率
        t: 到期时间
        sigma: 波动率

    返回:
        看涨期权价格
    """
    # TODO: 计算看涨期权价格
    pass


def black_scholes_put(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算欧式看跌期权价格。

    P = K × e^(-rT) × N(-d2) - S × N(-d1)

    参数:
        s, k, r, t, sigma: 期权参数

    返回:
        看跌期权价格
    """
    # TODO: 计算看跌期权价格
    pass


def put_call_parity(call_price: float, s: float, k: float, r: float, t: float) -> float:
    """
    使用看涨-看跌平价计算看跌期权价格。

    C - P = S - K×e^(-rT)
    P = C - S + K×e^(-rT)

    参数:
        call_price: 看涨期权价格
        s: 标的资产价格
        k: 执行价格
        r: 无风险利率
        t: 到期时间

    返回:
        看跌期权价格
    """
    # TODO: 使用平价关系计算
    pass


def option_delta_call(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算看涨期权的Delta。

    Delta_call = N(d1)

    参数:
        s, k, r, t, sigma: 期权参数

    返回:
        Delta值
    """
    # TODO: 计算Delta
    pass


def option_gamma(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算期权的Gamma（看涨看跌相同）。

    Gamma = N'(d1) / (S × σ × √T)

    参数:
        s, k, r, t, sigma: 期权参数

    返回:
        Gamma值
    """
    # TODO: 计算Gamma
    pass


def option_vega(s: float, k: float, r: float, t: float, sigma: float) -> float:
    """
    计算期权的Vega。

    Vega = S × √T × N'(d1)

    参数:
        s, k, r, t, sigma: 期权参数

    返回:
        Vega值
    """
    # TODO: 计算Vega
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
