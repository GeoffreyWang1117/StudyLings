# EXERCISE: efficient_frontier1
# DIFFICULTY: ★★★★☆
# TOPIC: 有效前沿
#
# 说明：
# 有效前沿是所有有效投资组合（给定风险下收益最高，或给定收益下风险最低）的集合。
#
# 有效前沿的特点：
# 1. 位于最小方差组合上方
# 2. 曲线向左上方凸出
# 3. 理性投资者只选择有效前沿上的组合
#
# 资本市场线（CML）：
# 当存在无风险资产时，最优组合是无风险资产与切点组合的组合
# E(Rp) = Rf + [(E(Rm) - Rf) / σm] × σp
#
# 夏普比率：
# Sharpe = [E(Rp) - Rf] / σp
# 切点组合具有最高的夏普比率
#
# 任务：
# 1. 生成有效前沿
# 2. 找到切点组合
# 3. 计算资本市场线
#
# HINT1: 有效前沿是一条抛物线（在均值-标准差空间）
# HINT2: 切点组合使夏普比率最大化

import numpy as np


def sharpe_ratio(expected_return: float, rf: float, std: float) -> float:
    """
    计算夏普比率。

    Sharpe = (E(R) - Rf) / σ

    参数:
        expected_return: 期望收益
        rf: 无风险利率
        std: 标准差

    返回:
        夏普比率
    """
    # TODO: 计算夏普比率
    pass


def capital_market_line_return(rf: float, market_return: float, market_std: float, portfolio_std: float) -> float:
    """
    计算资本市场线上给定风险的期望收益。

    E(Rp) = Rf + [(E(Rm) - Rf) / σm] × σp

    参数:
        rf: 无风险利率
        market_return: 市场（切点）组合收益
        market_std: 市场组合标准差
        portfolio_std: 目标组合标准差

    返回:
        期望收益
    """
    # TODO: 计算CML上的收益
    pass


def tangent_portfolio_weight(
    rf: float,
    returns: np.ndarray,
    cov_matrix: np.ndarray
) -> np.ndarray:
    """
    计算切点组合的权重。

    切点组合使夏普比率最大化。
    简化公式（两资产情况）见下方实现。

    参数:
        rf: 无风险利率
        returns: 各资产期望收益数组
        cov_matrix: 协方差矩阵

    返回:
        切点组合权重
    """
    # TODO: 计算切点组合权重
    # 使用公式：w* = (Σ^(-1) × (μ - rf)) / (1' × Σ^(-1) × (μ - rf))
    pass


def optimal_complete_portfolio(
    rf: float,
    market_return: float,
    market_std: float,
    risk_aversion: float
) -> tuple[float, float]:
    """
    计算最优完整组合（无风险资产 + 风险组合的配置）。

    风险资产比例：y* = (E(Rm) - Rf) / (A × σm²)

    参数:
        rf: 无风险利率
        market_return: 市场组合收益
        market_std: 市场组合标准差
        risk_aversion: 风险厌恶系数 A

    返回:
        (风险资产比例, 无风险资产比例)
    """
    # TODO: 计算最优配置
    pass


def is_efficient_portfolio(
    portfolio_return: float,
    portfolio_std: float,
    min_var_return: float,
    min_var_std: float
) -> bool:
    """
    判断组合是否在有效前沿上。

    有效前沿位于最小方差组合上方。

    参数:
        portfolio_return: 组合收益
        portfolio_std: 组合标准差
        min_var_return: 最小方差组合收益
        min_var_std: 最小方差组合标准差

    返回:
        如果在有效前沿上返回 True
    """
    # TODO: 判断是否有效
    # 简化判断：收益不低于最小方差组合，且风险合理
    pass


def treynor_ratio(expected_return: float, rf: float, beta: float) -> float:
    """
    计算特雷诺比率。

    Treynor = (E(R) - Rf) / β

    参数:
        expected_return: 期望收益
        rf: 无风险利率
        beta: 贝塔系数

    返回:
        特雷诺比率
    """
    # TODO: 计算特雷诺比率
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
