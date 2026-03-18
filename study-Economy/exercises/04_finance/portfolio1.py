# EXERCISE: portfolio1
# DIFFICULTY: ★★★★☆
# TOPIC: 投资组合理论
#
# 说明：
# 马科维茨投资组合理论是现代金融学的基石。
#
# 组合收益：
# E(Rp) = Σ wi × E(Ri)
#
# 组合方差（两资产情况）：
# σp² = w1²σ1² + w2²σ2² + 2w1w2ρ12σ1σ2
#
# 其中：
# - wi: 资产i的权重
# - E(Ri): 资产i的期望收益
# - σi: 资产i的标准差
# - ρ12: 两资产的相关系数
#
# 分散化效应：
# 当ρ < 1时，组合风险低于单个资产风险的加权平均
#
# 任务：
# 1. 计算投资组合的收益和风险
# 2. 理解分散化的效果
# 3. 找到最小方差组合
#
# HINT1: 权重之和等于1
# HINT2: 相关系数越低，分散化效果越好

import numpy as np


def portfolio_return(weights: np.ndarray, returns: np.ndarray) -> float:
    """
    计算投资组合期望收益。

    E(Rp) = Σ wi × E(Ri)

    参数:
        weights: 权重数组
        returns: 各资产期望收益数组

    返回:
        组合期望收益
    """
    # TODO: 计算组合收益
    pass


def portfolio_variance_two_assets(
    w1: float,
    sigma1: float,
    sigma2: float,
    rho: float
) -> float:
    """
    计算两资产组合的方差。

    σp² = w1²σ1² + w2²σ2² + 2w1w2ρσ1σ2
    其中 w2 = 1 - w1

    参数:
        w1: 资产1的权重
        sigma1: 资产1的标准差
        sigma2: 资产2的标准差
        rho: 两资产的相关系数

    返回:
        组合方差
    """
    # TODO: 计算组合方差
    pass


def portfolio_std(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    """
    计算投资组合标准差（通用情况）。

    σp = sqrt(w' × Σ × w)

    参数:
        weights: 权重数组
        cov_matrix: 协方差矩阵

    返回:
        组合标准差
    """
    # TODO: 计算组合标准差
    pass


def minimum_variance_weight_two_assets(
    sigma1: float,
    sigma2: float,
    rho: float
) -> float:
    """
    计算两资产情况下的最小方差组合权重。

    w1* = (σ2² - ρσ1σ2) / (σ1² + σ2² - 2ρσ1σ2)

    参数:
        sigma1: 资产1的标准差
        sigma2: 资产2的标准差
        rho: 相关系数

    返回:
        资产1的最优权重
    """
    # TODO: 计算最小方差权重
    pass


def diversification_benefit(
    sigma1: float,
    sigma2: float,
    rho: float,
    w1: float = 0.5
) -> float:
    """
    计算分散化收益。

    分散化收益 = 加权平均标准差 - 组合标准差

    参数:
        sigma1, sigma2: 各资产标准差
        rho: 相关系数
        w1: 资产1权重

    返回:
        分散化收益（标准差的减少）
    """
    # TODO: 计算分散化收益
    pass


def correlation_from_covariance(cov: float, sigma1: float, sigma2: float) -> float:
    """
    从协方差计算相关系数。

    ρ = Cov(R1, R2) / (σ1 × σ2)

    参数:
        cov: 协方差
        sigma1, sigma2: 标准差

    返回:
        相关系数
    """
    # TODO: 计算相关系数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
