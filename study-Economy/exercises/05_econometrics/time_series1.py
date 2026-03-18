# EXERCISE: time_series1
# DIFFICULTY: ★★★★☆
# TOPIC: 时间序列基础
#
# 说明：
# 时间序列分析处理按时间顺序排列的数据。
#
# 关键概念：
# - 平稳性：统计性质不随时间变化
# - 自相关：当前值与过去值的相关性
# - 趋势：长期增长或下降
# - 季节性：周期性波动
#
# 自相关函数（ACF）：
# ρk = Cov(Yt, Yt-k) / Var(Yt)
#
# 偏自相关函数（PACF）：
# 控制中间滞后后的相关性
#
# 任务：
# 1. 计算自相关
# 2. 检验平稳性
# 3. 进行差分
#
# HINT1: 非平稳序列需要先差分
# HINT2: ACF和PACF有助于识别模型

import numpy as np
from typing import Optional


def autocorrelation(y: np.ndarray, lag: int) -> float:
    """
    计算滞后k阶的自相关系数。

    ρk = Cov(Yt, Yt-k) / Var(Yt)

    参数:
        y: 时间序列
        lag: 滞后阶数

    返回:
        自相关系数
    """
    # TODO: 计算自相关
    pass


def acf(y: np.ndarray, max_lag: int) -> np.ndarray:
    """
    计算自相关函数。

    参数:
        y: 时间序列
        max_lag: 最大滞后阶数

    返回:
        自相关系数数组（从lag=0到lag=max_lag）
    """
    # TODO: 计算ACF
    pass


def difference(y: np.ndarray, d: int = 1) -> np.ndarray:
    """
    计算差分。

    ΔYt = Yt - Yt-1
    Δ²Yt = ΔYt - ΔYt-1

    参数:
        y: 时间序列
        d: 差分阶数

    返回:
        差分后的序列
    """
    # TODO: 计算差分
    pass


def moving_average(y: np.ndarray, window: int) -> np.ndarray:
    """
    计算移动平均。

    参数:
        y: 时间序列
        window: 窗口大小

    返回:
        移动平均序列
    """
    # TODO: 计算移动平均
    pass


def exponential_smoothing(y: np.ndarray, alpha: float) -> np.ndarray:
    """
    指数平滑。

    St = αYt + (1-α)St-1

    参数:
        y: 时间序列
        alpha: 平滑参数（0到1之间）

    返回:
        平滑后的序列
    """
    # TODO: 实现指数平滑
    pass


def adf_statistic(y: np.ndarray) -> float:
    """
    计算ADF检验统计量（简化版）。

    检验单位根（非平稳性）
    H₀: 存在单位根（非平稳）

    参数:
        y: 时间序列

    返回:
        ADF统计量
    """
    # TODO: 计算ADF统计量
    # 简化实现：回归 ΔYt = α + ρYt-1 + εt，返回ρ的t统计量
    pass


def is_stationary(adf_stat: float, critical_value: float = -2.86) -> bool:
    """
    基于ADF检验判断是否平稳。

    参数:
        adf_stat: ADF统计量
        critical_value: 临界值（5%水平）

    返回:
        是否平稳
    """
    # TODO: 判断平稳性
    pass


def detrend(y: np.ndarray) -> np.ndarray:
    """
    去除线性趋势。

    参数:
        y: 时间序列

    返回:
        去趋势后的序列
    """
    # TODO: 去趋势
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
