# EXERCISE: regression2
# DIFFICULTY: ★★★★☆
# TOPIC: 多元回归
#
# 说明：
# 多元回归允许多个自变量解释因变量的变化。
#
# 多元回归模型：
# Y = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ + ε
#
# 矩阵形式：
# Y = Xβ + ε
#
# OLS估计：
# β̂ = (X'X)⁻¹X'Y
#
# 调整R²：
# R̄² = 1 - (1 - R²)(n - 1) / (n - k - 1)
#
# 任务：
# 1. 实现多元回归OLS估计
# 2. 计算调整R²
# 3. 理解变量选择的重要性
#
# HINT1: 需要在X矩阵第一列添加1（截距项）
# HINT2: 调整R²惩罚过多变量

import numpy as np


def add_constant(x: np.ndarray) -> np.ndarray:
    """
    在X矩阵第一列添加常数1。

    参数:
        x: 自变量矩阵 (n × k)

    返回:
        添加常数列后的矩阵 (n × (k+1))
    """
    # TODO: 添加常数列
    pass


def ols_multiple(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    多元回归OLS估计。

    β̂ = (X'X)⁻¹X'Y

    参数:
        x: 自变量矩阵（应包含常数列）
        y: 因变量向量

    返回:
        系数估计向量
    """
    # TODO: 计算多元回归系数
    pass


def predict_multiple(x: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    多元回归预测。

    Ŷ = Xβ

    参数:
        x: 自变量矩阵（应包含常数列）
        beta: 系数向量

    返回:
        预测值
    """
    # TODO: 多元回归预测
    pass


def adjusted_r_squared(r_squared: float, n: int, k: int) -> float:
    """
    计算调整R²。

    R̄² = 1 - (1 - R²)(n - 1) / (n - k - 1)

    参数:
        r_squared: R²
        n: 样本量
        k: 自变量数量（不包括常数项）

    返回:
        调整R²
    """
    # TODO: 计算调整R²
    pass


def f_statistic(r_squared: float, n: int, k: int) -> float:
    """
    计算F统计量。

    F = (R² / k) / [(1 - R²) / (n - k - 1)]

    参数:
        r_squared: R²
        n: 样本量
        k: 自变量数量

    返回:
        F统计量
    """
    # TODO: 计算F统计量
    pass


def standard_errors(x: np.ndarray, y: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    计算系数的标准误差。

    SE(β̂) = sqrt(s² × (X'X)⁻¹的对角元素)
    其中 s² = SSR / (n - k - 1)

    参数:
        x: 自变量矩阵（包含常数列）
        y: 因变量向量
        beta: 系数估计

    返回:
        标准误差向量
    """
    # TODO: 计算标准误差
    pass


def t_statistics(beta: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    计算t统计量。

    t = β̂ / SE(β̂)

    参数:
        beta: 系数估计
        se: 标准误差

    返回:
        t统计量向量
    """
    # TODO: 计算t统计量
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
