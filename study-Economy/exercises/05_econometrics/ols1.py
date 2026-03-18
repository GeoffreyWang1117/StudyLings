# EXERCISE: ols1
# DIFFICULTY: ★★★★☆
# TOPIC: 最小二乘法
#
# 说明：
# 最小二乘法（OLS）是回归分析的核心方法。
#
# OLS的目标：
# 最小化残差平方和 Σei² = Σ(Yi - Ŷi)²
#
# OLS的假设（高斯-马尔科夫条件）：
# 1. 线性关系
# 2. E(ε|X) = 0（外生性）
# 3. Var(ε|X) = σ²（同方差）
# 4. Cov(εi, εj) = 0（无自相关）
# 5. X满秩（无完全多重共线性）
#
# 在这些假设下，OLS是BLUE（最佳线性无偏估计量）
#
# 任务：
# 1. 验证OLS假设
# 2. 处理异方差问题
# 3. 理解估计量的性质
#
# HINT1: 残差图可以检验假设
# HINT2: 怀特标准误差可以处理异方差

import numpy as np
from scipy import stats


def residual_sum_of_squares(y: np.ndarray, y_pred: np.ndarray) -> float:
    """
    计算残差平方和（SSR）。

    SSR = Σ(Yi - Ŷi)²

    参数:
        y: 实际值
        y_pred: 预测值

    返回:
        SSR
    """
    # TODO: 计算SSR
    pass


def total_sum_of_squares(y: np.ndarray) -> float:
    """
    计算总平方和（SST）。

    SST = Σ(Yi - Ȳ)²

    参数:
        y: 因变量数组

    返回:
        SST
    """
    # TODO: 计算SST
    pass


def explained_sum_of_squares(y_pred: np.ndarray, y_mean: float) -> float:
    """
    计算回归平方和（SSE）。

    SSE = Σ(Ŷi - Ȳ)²

    参数:
        y_pred: 预测值
        y_mean: Y的均值

    返回:
        SSE
    """
    # TODO: 计算SSE
    pass


def durbin_watson(residuals: np.ndarray) -> float:
    """
    计算Durbin-Watson统计量（检验自相关）。

    DW = Σ(et - et-1)² / Σet²

    DW ≈ 2: 无自相关
    DW < 2: 正自相关
    DW > 2: 负自相关

    参数:
        residuals: 残差数组

    返回:
        DW统计量
    """
    # TODO: 计算DW统计量
    pass


def breusch_pagan_test(x: np.ndarray, residuals: np.ndarray) -> tuple[float, float]:
    """
    Breusch-Pagan检验（检验异方差）。

    回归残差平方对X，检验系数显著性。

    参数:
        x: 自变量矩阵
        residuals: 残差

    返回:
        (检验统计量, p值)
    """
    # TODO: 实现BP检验
    pass


def white_standard_errors(x: np.ndarray, residuals: np.ndarray) -> np.ndarray:
    """
    计算怀特稳健标准误差。

    异方差稳健的标准误差估计。

    参数:
        x: 自变量矩阵
        residuals: 残差

    返回:
        稳健标准误差
    """
    # TODO: 计算稳健标准误差
    pass


def variance_inflation_factor(x: np.ndarray, j: int) -> float:
    """
    计算第j个变量的方差膨胀因子（VIF）。

    VIF_j = 1 / (1 - R²_j)
    其中R²_j是将Xj对其他X回归的R²

    VIF > 10 表示严重多重共线性

    参数:
        x: 自变量矩阵（不包括常数列）
        j: 变量索引

    返回:
        VIF值
    """
    # TODO: 计算VIF
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
