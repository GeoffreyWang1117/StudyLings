# EXERCISE: monte_carlo1
# DIFFICULTY: ★★★★☆
# TOPIC: 蒙特卡洛模拟
#
# 说明：
# 蒙特卡洛方法使用随机抽样来解决数值问题。
#
# 应用场景：
# 1. 期权定价
# 2. 风险评估（VaR）
# 3. 积分计算
# 4. 贝叶斯推断
#
# 基本步骤：
# 1. 定义随机过程
# 2. 大量模拟路径
# 3. 计算统计量
# 4. 估计置信区间
#
# 几何布朗运动（股价模拟）：
# dS = μSdt + σSdW
# 离散化：St+Δt = St × exp[(μ - σ²/2)Δt + σ√Δt × Z]
#
# 任务：
# 1. 模拟几何布朗运动
# 2. Monte Carlo期权定价
# 3. 估计收敛误差
#
# HINT1: 模拟次数越多，结果越准确
# HINT2: CUDA可以显著加速大规模模拟

import numpy as np


def geometric_brownian_motion(
    s0: float,
    mu: float,
    sigma: float,
    t: float,
    n_steps: int,
    n_paths: int,
    seed: int = 42
) -> np.ndarray:
    """
    模拟几何布朗运动路径。

    St+Δt = St × exp[(μ - σ²/2)Δt + σ√Δt × Z]

    参数:
        s0: 初始价格
        mu: 漂移率（期望收益）
        sigma: 波动率
        t: 总时间
        n_steps: 时间步数
        n_paths: 模拟路径数
        seed: 随机种子

    返回:
        价格路径矩阵 (n_paths × n_steps+1)
    """
    # TODO: 模拟GBM
    pass


def monte_carlo_european_call(
    s0: float,
    k: float,
    r: float,
    sigma: float,
    t: float,
    n_simulations: int,
    seed: int = 42
) -> tuple[float, float]:
    """
    Monte Carlo欧式看涨期权定价。

    Call = e^(-rT) × E[max(ST - K, 0)]

    参数:
        s0: 当前股价
        k: 执行价格
        r: 无风险利率
        sigma: 波动率
        t: 到期时间
        n_simulations: 模拟次数
        seed: 随机种子

    返回:
        (期权价格, 标准误差)
    """
    # TODO: MC期权定价
    pass


def monte_carlo_standard_error(values: np.ndarray) -> float:
    """
    计算Monte Carlo标准误差。

    SE = σ / √n

    参数:
        values: 模拟得到的值

    返回:
        标准误差
    """
    # TODO: 计算标准误差
    pass


def confidence_interval_mc(
    mean: float,
    se: float,
    confidence: float = 0.95
) -> tuple[float, float]:
    """
    计算Monte Carlo估计的置信区间。

    参数:
        mean: 均值估计
        se: 标准误差
        confidence: 置信水平

    返回:
        (下界, 上界)
    """
    # TODO: 计算置信区间
    pass


def antithetic_variates(
    s0: float,
    k: float,
    r: float,
    sigma: float,
    t: float,
    n_simulations: int,
    seed: int = 42
) -> tuple[float, float]:
    """
    对偶变量法减少方差。

    使用 Z 和 -Z 生成两条对称路径。

    参数:
        s0, k, r, sigma, t: 期权参数
        n_simulations: 模拟次数
        seed: 随机种子

    返回:
        (期权价格, 标准误差)
    """
    # TODO: 对偶变量法
    pass


def simulate_portfolio_var(
    returns_mean: np.ndarray,
    returns_cov: np.ndarray,
    weights: np.ndarray,
    initial_value: float,
    horizon: int,
    n_simulations: int,
    confidence: float = 0.95,
    seed: int = 42
) -> float:
    """
    Monte Carlo模拟组合VaR。

    参数:
        returns_mean: 资产期望收益
        returns_cov: 收益协方差矩阵
        weights: 组合权重
        initial_value: 初始组合价值
        horizon: 持有期（天）
        n_simulations: 模拟次数
        confidence: 置信水平
        seed: 随机种子

    返回:
        VaR值
    """
    # TODO: 模拟VaR
    pass


def required_simulations_for_precision(
    target_se: float,
    estimated_std: float
) -> int:
    """
    计算达到目标精度所需的模拟次数。

    n = (σ / SE)²

    参数:
        target_se: 目标标准误差
        estimated_std: 估计的标准差

    返回:
        所需模拟次数
    """
    # TODO: 计算所需模拟次数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
