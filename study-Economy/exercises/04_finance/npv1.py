# EXERCISE: npv1
# DIFFICULTY: ★★★☆☆
# TOPIC: 净现值
#
# 说明：
# 净现值（NPV）是投资决策的核心工具。
# NPV衡量一项投资创造的价值。
#
# NPV = Σ [CFt / (1 + r)^t] - 初始投资
#
# 决策规则：
# - NPV > 0: 接受项目
# - NPV < 0: 拒绝项目
# - NPV = 0: 项目刚好达到要求回报率
#
# 当比较互斥项目时，选择NPV最高的项目。
#
# 任务：
# 1. 计算项目的NPV
# 2. 根据NPV做投资决策
# 3. 比较不同项目
#
# HINT1: NPV考虑了货币时间价值
# HINT2: 折现率反映了投资的机会成本

import numpy as np
from typing import Optional


def npv(cash_flows: list[float], discount_rate: float) -> float:
    """
    计算净现值。

    NPV = Σ [CFt / (1 + r)^t]

    参数:
        cash_flows: 现金流列表，第一个元素是初始投资（通常为负）
        discount_rate: 折现率

    返回:
        净现值
    """
    # TODO: 计算NPV
    pass


def npv_decision(npv_value: float) -> str:
    """
    根据NPV做投资决策。

    参数:
        npv_value: 净现值

    返回:
        "accept" 或 "reject"
    """
    # TODO: 做投资决策
    pass


def profitability_index(cash_flows: list[float], discount_rate: float) -> float:
    """
    计算盈利指数（PI）。

    PI = 未来现金流现值 / 初始投资
       = (NPV + |初始投资|) / |初始投资|

    参数:
        cash_flows: 现金流列表
        discount_rate: 折现率

    返回:
        盈利指数
    """
    # TODO: 计算盈利指数
    pass


def payback_period(cash_flows: list[float]) -> Optional[float]:
    """
    计算回收期（不考虑时间价值）。

    参数:
        cash_flows: 现金流列表

    返回:
        回收期（年），如果无法回收返回 None
    """
    # TODO: 计算回收期
    pass


def discounted_payback_period(cash_flows: list[float], discount_rate: float) -> Optional[float]:
    """
    计算折现回收期。

    参数:
        cash_flows: 现金流列表
        discount_rate: 折现率

    返回:
        折现回收期（年），如果无法回收返回 None
    """
    # TODO: 计算折现回收期
    pass


def compare_projects(
    project_a_flows: list[float],
    project_b_flows: list[float],
    discount_rate: float
) -> str:
    """
    比较两个互斥项目。

    参数:
        project_a_flows: 项目A的现金流
        project_b_flows: 项目B的现金流
        discount_rate: 折现率

    返回:
        "A" 或 "B"（NPV更高的项目）
    """
    # TODO: 比较项目
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
