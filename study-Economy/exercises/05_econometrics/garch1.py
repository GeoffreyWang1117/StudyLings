# EXERCISE: garch1
# DIFFICULTY: ★★★★★
# TOPIC: GARCH波动率模型
#
# 说明：
# GARCH模型用于建模时变波动率，广泛应用于金融数据。
#
# 金融时间序列特征：
# - 波动聚集：大波动后往往跟随大波动
# - 厚尾分布：极端值出现频率高于正态分布
# - 杠杆效应：负收益对波动的影响大于正收益
#
# GARCH(1,1)模型：
# rt = μ + εt
# εt = σt × zt, zt ~ N(0,1)
# σt² = ω + α×εt-1² + β×σt-1²
#
# 其中：
# - ω > 0, α ≥ 0, β ≥ 0
# - α + β < 1 保证平稳性
#
# 任务：
# 1. 理解波动聚集
# 2. 实现GARCH(1,1)模拟
# 3. 计算条件波动率
#
# HINT1: α + β 越接近1，波动持续性越强
# HINT2: 可以使用CUDA加速大规模模拟

import numpy as np


def garch11_simulate(
    omega: float,
    alpha: float,
    beta: float,
    n: int,
    mu: float = 0,
    seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    模拟GARCH(1,1)过程。

    rt = μ + εt
    εt = σt × zt
    σt² = ω + α×εt-1² + β×σt-1²

    参数:
        omega: 常数项
        alpha: ARCH项系数
        beta: GARCH项系数
        n: 序列长度
        mu: 均值
        seed: 随机种子

    返回:
        (收益率序列, 波动率序列)
    """
    # TODO: 模拟GARCH(1,1)
    pass


def unconditional_variance(omega: float, alpha: float, beta: float) -> float:
    """
    计算GARCH(1,1)的无条件方差。

    σ² = ω / (1 - α - β)

    参数:
        omega, alpha, beta: GARCH参数

    返回:
        无条件方差
    """
    # TODO: 计算无条件方差
    pass


def volatility_persistence(alpha: float, beta: float) -> float:
    """
    计算波动率持续性。

    持续性 = α + β

    参数:
        alpha, beta: GARCH参数

    返回:
        持续性（接近1表示高持续性）
    """
    # TODO: 计算持续性
    pass


def half_life_volatility(alpha: float, beta: float) -> float:
    """
    计算波动率半衰期。

    波动率冲击衰减一半所需时间。
    半衰期 = ln(2) / ln(α + β)

    参数:
        alpha, beta: GARCH参数

    返回:
        半衰期（期数）
    """
    # TODO: 计算半衰期
    pass


def conditional_variance_forecast(
    omega: float,
    alpha: float,
    beta: float,
    last_epsilon_sq: float,
    last_sigma_sq: float,
    h: int
) -> np.ndarray:
    """
    条件方差预测。

    σt+h² = ω + (α + β)^(h-1) × [α×εt² + β×σt² - ω/(1-α-β)] + ω/(1-α-β)

    简化：一步预测 σt+1² = ω + α×εt² + β×σt²

    参数:
        omega, alpha, beta: GARCH参数
        last_epsilon_sq: 最后一个ε²
        last_sigma_sq: 最后一个σ²
        h: 预测步数

    返回:
        预测的条件方差序列
    """
    # TODO: 条件方差预测
    pass


def value_at_risk(mu: float, sigma: float, confidence: float = 0.95) -> float:
    """
    计算VaR（在险价值）。

    VaR = μ - σ × Φ^(-1)(1 - confidence)

    参数:
        mu: 期望收益
        sigma: 波动率
        confidence: 置信水平

    返回:
        VaR（损失为正）
    """
    # TODO: 计算VaR
    pass


def expected_shortfall(mu: float, sigma: float, confidence: float = 0.95) -> float:
    """
    计算ES（期望损失）/ CVaR。

    ES = E[Loss | Loss > VaR]
    对于正态分布：ES = μ - σ × φ(Φ^(-1)(1-c)) / (1-c)

    参数:
        mu: 期望收益
        sigma: 波动率
        confidence: 置信水平

    返回:
        期望损失
    """
    # TODO: 计算ES
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
