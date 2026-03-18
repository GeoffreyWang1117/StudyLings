# EXERCISE: hypothesis1
# DIFFICULTY: ★★★☆☆
# TOPIC: 假设检验
#
# 说明：
# 假设检验用于判断统计结论的可信度。
#
# 步骤：
# 1. 设立零假设H₀和备择假设H₁
# 2. 选择显著性水平α（常用0.05）
# 3. 计算检验统计量
# 4. 比较临界值或p值
# 5. 做出决策
#
# 常见检验：
# - t检验：单个系数的显著性
# - F检验：联合假设/模型整体显著性
# - 卡方检验：分类变量
#
# 任务：
# 1. 进行t检验
# 2. 进行F检验
# 3. 解释p值
#
# HINT1: p值是在H₀为真时观察到更极端结果的概率
# HINT2: p < α 则拒绝H₀

import numpy as np
from scipy import stats


def t_test_coefficient(beta: float, se: float, null_value: float = 0) -> tuple[float, float]:
    """
    对回归系数进行t检验。

    t = (β̂ - β₀) / SE(β̂)

    参数:
        beta: 系数估计值
        se: 标准误差
        null_value: 零假设值（默认为0）

    返回:
        (t统计量, p值)
    """
    # TODO: 进行t检验
    pass


def is_significant(p_value: float, alpha: float = 0.05) -> bool:
    """
    判断结果是否统计显著。

    参数:
        p_value: p值
        alpha: 显著性水平

    返回:
        是否显著
    """
    # TODO: 判断显著性
    pass


def f_test_model(r_squared: float, n: int, k: int) -> tuple[float, float]:
    """
    模型整体F检验。

    H₀: 所有斜率系数为0
    F = (R² / k) / [(1 - R²) / (n - k - 1)]

    参数:
        r_squared: R²
        n: 样本量
        k: 自变量数量

    返回:
        (F统计量, p值)
    """
    # TODO: 进行F检验
    pass


def f_test_restricted(ssr_r: float, ssr_ur: float, q: int, n: int, k: int) -> tuple[float, float]:
    """
    约束F检验。

    比较约束模型和非约束模型。
    F = [(SSR_r - SSR_ur) / q] / [SSR_ur / (n - k - 1)]

    参数:
        ssr_r: 约束模型的SSR
        ssr_ur: 非约束模型的SSR
        q: 约束数量
        n: 样本量
        k: 非约束模型的变量数

    返回:
        (F统计量, p值)
    """
    # TODO: 进行约束F检验
    pass


def confidence_interval(beta: float, se: float, alpha: float = 0.05, df: int = 100) -> tuple[float, float]:
    """
    计算系数的置信区间。

    CI = β̂ ± t_{α/2} × SE(β̂)

    参数:
        beta: 系数估计
        se: 标准误差
        alpha: 显著性水平
        df: 自由度

    返回:
        (下界, 上界)
    """
    # TODO: 计算置信区间
    pass


def power_of_test(effect_size: float, se: float, alpha: float = 0.05) -> float:
    """
    计算检验的功效（检验力）。

    功效 = 1 - P(Type II Error)
         = P(拒绝H₀ | H₁为真)

    参数:
        effect_size: 效应量（真实效应）
        se: 标准误差
        alpha: 显著性水平

    返回:
        功效
    """
    # TODO: 计算检验功效
    pass


def required_sample_size(effect_size: float, sd: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """
    计算达到指定功效所需的样本量。

    参数:
        effect_size: 期望检测的效应量
        sd: 标准差
        alpha: 显著性水平
        power: 目标功效

    返回:
        所需样本量
    """
    # TODO: 计算所需样本量
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
