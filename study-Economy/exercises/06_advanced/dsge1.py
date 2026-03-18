# EXERCISE: dsge1
# DIFFICULTY: ★★★★★
# TOPIC: 动态随机一般均衡入门
#
# 说明：
# DSGE模型是现代宏观经济学的标准分析框架。
#
# 简化的新凯恩斯DSGE模型包含：
# 1. 消费者优化问题
# 2. 企业定价决策
# 3. 货币政策规则
#
# 核心方程：
# - 新凯恩斯菲利普斯曲线（NKPC）：
#   πt = βEt[πt+1] + κxt
#
# - 动态IS曲线：
#   xt = Et[xt+1] - σ(it - Et[πt+1] - rⁿ)
#
# - 泰勒规则：
#   it = rⁿ + φπ×πt + φx×xt
#
# 其中：
# - π: 通胀
# - x: 产出缺口
# - i: 名义利率
# - rⁿ: 自然利率
#
# 任务：
# 1. 理解DSGE的基本结构
# 2. 实现简单的求解
# 3. 分析政策冲击
#
# HINT1: DSGE通常需要线性化后求解
# HINT2: 可以使用CUDA加速迭代求解

import numpy as np


def nkpc(pi_future: float, output_gap: float, beta: float, kappa: float) -> float:
    """
    新凯恩斯菲利普斯曲线。

    πt = βEt[πt+1] + κxt

    参数:
        pi_future: 预期未来通胀
        output_gap: 产出缺口
        beta: 折现因子
        kappa: 菲利普斯曲线斜率

    返回:
        当期通胀
    """
    # TODO: 计算NKPC
    pass


def dynamic_is(
    output_gap_future: float,
    nominal_rate: float,
    inflation_future: float,
    natural_rate: float,
    sigma: float
) -> float:
    """
    动态IS曲线。

    xt = Et[xt+1] - σ(it - Et[πt+1] - rⁿ)

    参数:
        output_gap_future: 预期未来产出缺口
        nominal_rate: 名义利率
        inflation_future: 预期未来通胀
        natural_rate: 自然利率
        sigma: 跨期替代弹性

    返回:
        当期产出缺口
    """
    # TODO: 计算动态IS
    pass


def taylor_rule(
    natural_rate: float,
    inflation: float,
    output_gap: float,
    phi_pi: float = 1.5,
    phi_x: float = 0.5
) -> float:
    """
    泰勒规则。

    it = rⁿ + φπ×πt + φx×xt

    参数:
        natural_rate: 自然利率
        inflation: 通胀率
        output_gap: 产出缺口
        phi_pi: 通胀反应系数（>1保证稳定性）
        phi_x: 产出缺口反应系数

    返回:
        名义利率
    """
    # TODO: 计算泰勒规则
    pass


def check_taylor_principle(phi_pi: float) -> bool:
    """
    检验泰勒原则。

    泰勒原则：φπ > 1，确保政策对通胀的反应足够强。

    参数:
        phi_pi: 通胀反应系数

    返回:
        是否满足泰勒原则
    """
    # TODO: 检验泰勒原则
    pass


def solve_steady_state(natural_rate: float) -> dict:
    """
    求解稳态。

    在稳态：πss = 0, xss = 0, iss = rⁿ

    参数:
        natural_rate: 自然利率

    返回:
        {'inflation': πss, 'output_gap': xss, 'interest_rate': iss}
    """
    # TODO: 求解稳态
    pass


def monetary_policy_shock(
    shock_size: float,
    beta: float,
    kappa: float,
    sigma: float,
    phi_pi: float,
    phi_x: float,
    periods: int = 20
) -> dict:
    """
    模拟货币政策冲击的影响（简化版）。

    参数:
        shock_size: 冲击大小（利率变化）
        beta, kappa, sigma: 模型参数
        phi_pi, phi_x: 泰勒规则参数
        periods: 模拟期数

    返回:
        {'inflation': [], 'output_gap': [], 'interest_rate': []}
    """
    # TODO: 模拟政策冲击
    pass


def discount_factor_from_interest_rate(annual_rate: float) -> float:
    """
    从年利率计算季度折现因子。

    β = 1 / (1 + r/4)

    参数:
        annual_rate: 年利率

    返回:
        季度折现因子
    """
    # TODO: 计算折现因子
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
