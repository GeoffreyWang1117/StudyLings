# EXERCISE: capm1
# DIFFICULTY: ★★★★☆
# TOPIC: 资本资产定价模型
#
# 说明：
# CAPM（资本资产定价模型）描述了风险与期望收益的关系。
#
# CAPM公式：
# E(Ri) = Rf + βi × [E(Rm) - Rf]
#
# 其中：
# - E(Ri): 资产i的期望收益
# - Rf: 无风险利率
# - βi: 资产i的贝塔系数
# - E(Rm): 市场组合期望收益
# - E(Rm) - Rf: 市场风险溢价
#
# 贝塔系数：
# βi = Cov(Ri, Rm) / Var(Rm) = ρim × σi / σm
#
# 贝塔衡量系统性风险（市场风险），不可分散
# β > 1: 激进型资产
# β < 1: 防御型资产
# β = 1: 与市场同步
#
# 任务：
# 1. 使用CAPM计算期望收益
# 2. 计算贝塔系数
# 3. 评估资产定价是否合理
#
# HINT1: CAPM只考虑系统性风险
# HINT2: 阿尔法α衡量超额收益

import numpy as np


def capm_expected_return(rf: float, beta: float, market_return: float) -> float:
    """
    使用CAPM计算期望收益。

    E(Ri) = Rf + β × [E(Rm) - Rf]

    参数:
        rf: 无风险利率
        beta: 贝塔系数
        market_return: 市场期望收益

    返回:
        期望收益
    """
    # TODO: 计算CAPM期望收益
    pass


def calculate_beta(cov_with_market: float, market_variance: float) -> float:
    """
    计算贝塔系数。

    β = Cov(Ri, Rm) / Var(Rm)

    参数:
        cov_with_market: 资产收益与市场收益的协方差
        market_variance: 市场收益的方差

    返回:
        贝塔系数
    """
    # TODO: 计算贝塔
    pass


def beta_from_regression(asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
    """
    通过回归计算贝塔。

    使用 Ri = α + β × Rm + ε 的斜率作为贝塔。

    参数:
        asset_returns: 资产收益序列
        market_returns: 市场收益序列

    返回:
        贝塔系数
    """
    # TODO: 通过回归计算贝塔
    # 提示：使用最小二乘法或numpy的相关函数
    pass


def market_risk_premium(market_return: float, rf: float) -> float:
    """
    计算市场风险溢价。

    Market Risk Premium = E(Rm) - Rf

    参数:
        market_return: 市场期望收益
        rf: 无风险利率

    返回:
        市场风险溢价
    """
    # TODO: 计算市场风险溢价
    pass


def alpha(actual_return: float, rf: float, beta: float, market_return: float) -> float:
    """
    计算阿尔法（超额收益）。

    α = Ri - [Rf + β × (Rm - Rf)]

    参数:
        actual_return: 实际收益
        rf: 无风险利率
        beta: 贝塔系数
        market_return: 市场收益

    返回:
        阿尔法
    """
    # TODO: 计算阿尔法
    pass


def is_undervalued(actual_return: float, capm_return: float) -> bool:
    """
    判断资产是否被低估。

    如果实际收益 > CAPM期望收益，资产被低估（值得买入）

    参数:
        actual_return: 实际或预期收益
        capm_return: CAPM计算的应得收益

    返回:
        如果被低估返回 True
    """
    # TODO: 判断是否被低估
    pass


def portfolio_beta(weights: np.ndarray, betas: np.ndarray) -> float:
    """
    计算投资组合的贝塔。

    βp = Σ wi × βi

    参数:
        weights: 权重数组
        betas: 各资产贝塔数组

    返回:
        组合贝塔
    """
    # TODO: 计算组合贝塔
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
