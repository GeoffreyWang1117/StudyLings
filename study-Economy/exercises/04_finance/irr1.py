# EXERCISE: irr1
# DIFFICULTY: ★★★☆☆
# TOPIC: 内部收益率
#
# 说明：
# 内部收益率（IRR）是使NPV等于零的折现率。
#
# 0 = Σ [CFt / (1 + IRR)^t]
#
# 决策规则：
# - IRR > 要求回报率: 接受项目
# - IRR < 要求回报率: 拒绝项目
#
# IRR的问题：
# 1. 可能存在多个IRR（现金流符号多次变化时）
# 2. 互斥项目比较时可能给出错误决策
# 3. 融资型项目需要反转决策规则
#
# 任务：
# 1. 计算IRR
# 2. 使用IRR做决策
# 3. 理解IRR的局限性
#
# HINT1: IRR需要用数值方法求解
# HINT2: 可以使用二分法或牛顿法

import numpy as np
from typing import Optional


def irr(cash_flows: list[float], guess: float = 0.1, tolerance: float = 1e-6, max_iterations: int = 1000) -> Optional[float]:
    """
    计算内部收益率。

    使用数值方法找到使NPV=0的利率。

    参数:
        cash_flows: 现金流列表
        guess: 初始猜测值
        tolerance: 收敛容差
        max_iterations: 最大迭代次数

    返回:
        内部收益率，如果无法收敛返回 None
    """
    # TODO: 计算IRR
    # 提示：可以使用二分法或牛顿法
    pass


def irr_decision(irr_value: float, required_return: float) -> str:
    """
    根据IRR做投资决策。

    参数:
        irr_value: 内部收益率
        required_return: 要求回报率

    返回:
        "accept" 或 "reject"
    """
    # TODO: 做投资决策
    pass


def modified_irr(cash_flows: list[float], finance_rate: float, reinvest_rate: float) -> float:
    """
    计算修正内部收益率（MIRR）。

    MIRR假设：
    - 负现金流按融资利率折现到0期
    - 正现金流按再投资利率复利到终期

    MIRR = (终值FV / 现值PV)^(1/n) - 1

    参数:
        cash_flows: 现金流列表
        finance_rate: 融资利率（用于负现金流）
        reinvest_rate: 再投资利率（用于正现金流）

    返回:
        修正内部收益率
    """
    # TODO: 计算MIRR
    pass


def npv_at_rate(cash_flows: list[float], rate: float) -> float:
    """
    计算给定折现率下的NPV。

    参数:
        cash_flows: 现金流列表
        rate: 折现率

    返回:
        NPV
    """
    # TODO: 计算NPV
    pass


def has_multiple_irrs(cash_flows: list[float]) -> bool:
    """
    判断现金流是否可能有多个IRR。

    当现金流符号变化超过一次时，可能存在多个IRR。

    参数:
        cash_flows: 现金流列表

    返回:
        如果可能有多个IRR返回 True
    """
    # TODO: 检查是否可能有多个IRR
    pass


def crossover_rate(
    project_a_flows: list[float],
    project_b_flows: list[float]
) -> Optional[float]:
    """
    计算两个项目的交叉利率。

    交叉利率是使两个项目NPV相等的折现率。

    参数:
        project_a_flows: 项目A的现金流
        project_b_flows: 项目B的现金流

    返回:
        交叉利率
    """
    # TODO: 计算交叉利率
    # 提示：计算差额现金流的IRR
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
