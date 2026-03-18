# EXERCISE: multiplier1
# DIFFICULTY: ★★★☆☆
# TOPIC: 乘数效应
#
# 说明：
# 乘数效应描述了自主支出变化如何引起GDP成倍变化。
#
# 凯恩斯乘数模型：
# Y = C + I + G
# C = C₀ + c(Y - T)
#
# 其中：
# - c: 边际消费倾向 (MPC)，0 < c < 1
# - C₀: 自主消费
# - T: 税收
#
# 支出乘数：
# k = 1 / (1 - MPC) = 1 / MPS
#
# 当政府支出增加 ΔG 时：
# ΔY = k × ΔG
#
# 税收乘数：
# k_T = -MPC / (1 - MPC)
#
# 平衡预算乘数 = 1（政府支出和税收同时增加相同数量）
#
# 任务：
# 1. 计算支出乘数
# 2. 计算政府支出变化对GDP的影响
# 3. 计算税收乘数
#
# HINT1: MPC + MPS = 1（边际消费倾向 + 边际储蓄倾向 = 1）
# HINT2: 乘数越大，财政政策效果越强


def spending_multiplier(mpc: float) -> float:
    """
    计算支出乘数。

    k = 1 / (1 - MPC)

    参数:
        mpc: 边际消费倾向 (0 < mpc < 1)

    返回:
        支出乘数
    """
    # TODO: 计算支出乘数
    pass


def tax_multiplier(mpc: float) -> float:
    """
    计算税收乘数。

    k_T = -MPC / (1 - MPC)

    参数:
        mpc: 边际消费倾向

    返回:
        税收乘数（负数）
    """
    # TODO: 计算税收乘数
    pass


def gdp_change_from_spending(delta_g: float, mpc: float) -> float:
    """
    计算政府支出变化导致的GDP变化。

    ΔY = k × ΔG

    参数:
        delta_g: 政府支出变化
        mpc: 边际消费倾向

    返回:
        GDP变化
    """
    # TODO: 计算GDP变化
    pass


def gdp_change_from_tax(delta_t: float, mpc: float) -> float:
    """
    计算税收变化导致的GDP变化。

    ΔY = k_T × ΔT

    参数:
        delta_t: 税收变化
        mpc: 边际消费倾向

    返回:
        GDP变化
    """
    # TODO: 计算GDP变化
    pass


def balanced_budget_multiplier() -> float:
    """
    返回平衡预算乘数。

    当政府支出和税收同时增加相同数量时，
    ΔY = ΔG（平衡预算乘数为1）

    返回:
        平衡预算乘数
    """
    # TODO: 返回平衡预算乘数
    pass


def marginal_propensity_to_save(mpc: float) -> float:
    """
    计算边际储蓄倾向。

    MPS = 1 - MPC

    参数:
        mpc: 边际消费倾向

    返回:
        边际储蓄倾向
    """
    # TODO: 计算MPS
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
