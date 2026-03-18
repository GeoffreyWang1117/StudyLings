# EXERCISE: arima1
# DIFFICULTY: ★★★★☆
# TOPIC: ARIMA模型
#
# 说明：
# ARIMA(p,d,q)是最常用的时间序列预测模型。
#
# 组成部分：
# - AR(p): 自回归，p阶
# - I(d): 积分，d阶差分
# - MA(q): 移动平均，q阶
#
# AR(p)模型：
# Yt = c + φ₁Yt-1 + φ₂Yt-2 + ... + φpYt-p + εt
#
# MA(q)模型：
# Yt = μ + εt + θ₁εt-1 + θ₂εt-2 + ... + θqεt-q
#
# ARMA(p,q)：
# Yt = c + Σφᵢ Yt-i + εt + Σθⱼ εt-j
#
# 模型选择：
# - ACF拖尾、PACF截尾 → AR
# - ACF截尾、PACF拖尾 → MA
# - 都拖尾 → ARMA
#
# 任务：
# 1. 实现AR模型
# 2. 实现MA模型
# 3. 模型识别和预测
#
# HINT1: 使用AIC/BIC选择最优阶数
# HINT2: 检验残差是否为白噪声

import numpy as np


def ar1_process(phi: float, c: float, sigma: float, n: int, seed: int = 42) -> np.ndarray:
    """
    生成AR(1)过程。

    Yt = c + φYt-1 + εt

    参数:
        phi: 自回归系数（|φ| < 1 保证平稳）
        c: 常数项
        sigma: 误差标准差
        n: 序列长度
        seed: 随机种子

    返回:
        AR(1)序列
    """
    # TODO: 生成AR(1)过程
    pass


def ma1_process(theta: float, mu: float, sigma: float, n: int, seed: int = 42) -> np.ndarray:
    """
    生成MA(1)过程。

    Yt = μ + εt + θεt-1

    参数:
        theta: 移动平均系数
        mu: 均值
        sigma: 误差标准差
        n: 序列长度
        seed: 随机种子

    返回:
        MA(1)序列
    """
    # TODO: 生成MA(1)过程
    pass


def ar1_forecast(y: np.ndarray, phi: float, c: float, h: int) -> np.ndarray:
    """
    AR(1)模型预测。

    参数:
        y: 历史序列
        phi: AR系数
        c: 常数
        h: 预测步数

    返回:
        预测值
    """
    # TODO: AR(1)预测
    pass


def estimate_ar1(y: np.ndarray) -> tuple[float, float]:
    """
    估计AR(1)参数。

    使用OLS估计 Yt = c + φYt-1

    参数:
        y: 时间序列

    返回:
        (φ估计, c估计)
    """
    # TODO: 估计AR(1)参数
    pass


def aic(n: int, k: int, log_likelihood: float) -> float:
    """
    计算AIC（赤池信息准则）。

    AIC = 2k - 2ln(L)

    参数:
        n: 样本量
        k: 参数数量
        log_likelihood: 对数似然

    返回:
        AIC值
    """
    # TODO: 计算AIC
    pass


def bic(n: int, k: int, log_likelihood: float) -> float:
    """
    计算BIC（贝叶斯信息准则）。

    BIC = k×ln(n) - 2ln(L)

    参数:
        n: 样本量
        k: 参数数量
        log_likelihood: 对数似然

    返回:
        BIC值
    """
    # TODO: 计算BIC
    pass


def ljung_box_test(residuals: np.ndarray, lags: int) -> tuple[float, float]:
    """
    Ljung-Box检验（检验残差自相关）。

    Q = n(n+2) Σ ρk² / (n-k)

    参数:
        residuals: 残差序列
        lags: 滞后阶数

    返回:
        (Q统计量, p值)
    """
    # TODO: 实现LB检验
    pass


def is_white_noise(residuals: np.ndarray, alpha: float = 0.05) -> bool:
    """
    检验残差是否为白噪声。

    参数:
        residuals: 残差序列
        alpha: 显著性水平

    返回:
        是否为白噪声
    """
    # TODO: 检验白噪声
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
