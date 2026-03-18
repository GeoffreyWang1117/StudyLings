# EXERCISE: regression1
# DIFFICULTY: ★★★☆☆
# TOPIC: 简单线性回归
#
# 说明：
# 线性回归是计量经济学的基础工具。
#
# 简单线性回归模型：
# Y = α + βX + ε
#
# 其中：
# - Y: 因变量
# - X: 自变量
# - α: 截距
# - β: 斜率（X对Y的边际效应）
# - ε: 误差项
#
# 最小二乘估计（OLS）：
# β̂ = Σ(Xi - X̄)(Yi - Ȳ) / Σ(Xi - X̄)²
# α̂ = Ȳ - β̂X̄
#
# 任务：
# 1. 实现OLS估计
# 2. 计算拟合优度R²
# 3. 进行预测
#
# HINT1: OLS最小化残差平方和
# HINT2: R²衡量模型解释力度

import numpy as np


def ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    """
    计算OLS斜率估计。

    β̂ = Σ(Xi - X̄)(Yi - Ȳ) / Σ(Xi - X̄)²

    参数:
        x: 自变量数组
        y: 因变量数组

    返回:
        斜率估计值
    """
    # TODO: 计算斜率
    pass


def ols_intercept(x: np.ndarray, y: np.ndarray) -> float:
    """
    计算OLS截距估计。

    α̂ = Ȳ - β̂X̄

    参数:
        x: 自变量数组
        y: 因变量数组

    返回:
        截距估计值
    """
    # TODO: 计算截距
    pass


def predict(x: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """
    使用回归方程进行预测。

    Ŷ = α + βX

    参数:
        x: 自变量值
        alpha: 截距
        beta: 斜率

    返回:
        预测值
    """
    # TODO: 计算预测值
    pass


def residuals(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    计算残差。

    e = Y - Ŷ

    参数:
        y: 实际值
        y_pred: 预测值

    返回:
        残差数组
    """
    # TODO: 计算残差
    pass


def r_squared(y: np.ndarray, y_pred: np.ndarray) -> float:
    """
    计算决定系数R²。

    R² = 1 - SSR/SST
       = 1 - Σ(Yi - Ŷi)² / Σ(Yi - Ȳ)²

    参数:
        y: 实际值
        y_pred: 预测值

    返回:
        R²
    """
    # TODO: 计算R²
    pass


def standard_error_of_estimate(y: np.ndarray, y_pred: np.ndarray, k: int = 2) -> float:
    """
    计算估计标准误差。

    SEE = sqrt(SSR / (n - k))

    参数:
        y: 实际值
        y_pred: 预测值
        k: 参数数量（简单回归为2）

    返回:
        估计标准误差
    """
    # TODO: 计算估计标准误差
    pass


def correlation_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    """
    计算相关系数。

    r = Cov(X,Y) / (σx × σy)

    参数:
        x, y: 数据数组

    返回:
        相关系数
    """
    # TODO: 计算相关系数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
