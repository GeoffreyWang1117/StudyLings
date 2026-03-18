# EXERCISE: phillips1
# DIFFICULTY: ★★★☆☆
# TOPIC: 菲利普斯曲线
#
# 说明：
# 菲利普斯曲线描述通货膨胀与失业之间的关系。
#
# 原始菲利普斯曲线（1958）：
# 通胀率与失业率负相关
#
# 附加预期的菲利普斯曲线：
# π = πᵉ - β(u - uₙ)
#
# 其中：
# - π: 实际通胀率
# - πᵉ: 预期通胀率
# - u: 实际失业率
# - uₙ: 自然失业率（NAIRU）
# - β: 失业对通胀的敏感度
#
# 长期菲利普斯曲线：
# 当预期调整后，π = πᵉ，u = uₙ
# 长期菲利普斯曲线是垂直的
#
# 任务：
# 1. 实现菲利普斯曲线
# 2. 计算牺牲比率
# 3. 分析预期在通胀中的作用
#
# HINT1: 短期内可以用失业换取低通胀
# HINT2: 长期中失业率回归自然率


def phillips_curve_inflation(
    u: float,
    u_natural: float,
    pi_expected: float,
    beta: float
) -> float:
    """
    附加预期的菲利普斯曲线：计算通胀率。

    π = πᵉ - β(u - uₙ)

    参数:
        u: 实际失业率
        u_natural: 自然失业率
        pi_expected: 预期通胀率
        beta: 失业对通胀敏感度

    返回:
        实际通胀率
    """
    # TODO: 计算通胀率
    pass


def phillips_curve_unemployment(
    pi: float,
    u_natural: float,
    pi_expected: float,
    beta: float
) -> float:
    """
    菲利普斯曲线：给定通胀率，计算失业率。

    u = uₙ - (π - πᵉ) / β

    参数:
        pi: 实际通胀率
        u_natural: 自然失业率
        pi_expected: 预期通胀率
        beta: 失业敏感度

    返回:
        失业率
    """
    # TODO: 计算失业率
    pass


def sacrifice_ratio(delta_inflation: float, delta_unemployment: float) -> float:
    """
    计算牺牲比率。

    牺牲比率 = 累计产出损失 / 通胀降低幅度
    简化版本：失业率增加 / 通胀降低幅度

    参数:
        delta_inflation: 通胀变化（负值表示降低）
        delta_unemployment: 失业率变化（正值表示增加）

    返回:
        牺牲比率
    """
    # TODO: 计算牺牲比率
    pass


def adaptive_expectations(pi_last: float, pi_expected_last: float, theta: float) -> float:
    """
    适应性预期：根据过去的通胀调整预期。

    πᵉₜ = πᵉₜ₋₁ + θ(πₜ₋₁ - πᵉₜ₋₁)

    参数:
        pi_last: 上期实际通胀
        pi_expected_last: 上期预期通胀
        theta: 调整速度（0到1之间）

    返回:
        本期预期通胀
    """
    # TODO: 计算适应性预期
    pass


def unemployment_gap(u: float, u_natural: float) -> float:
    """
    计算失业缺口。

    失业缺口 = u - uₙ

    正值：周期性失业
    负值：经济过热

    参数:
        u: 实际失业率
        u_natural: 自然失业率

    返回:
        失业缺口
    """
    # TODO: 计算失业缺口
    pass


def is_stagflation(inflation: float, unemployment: float,
                   inflation_threshold: float, unemployment_threshold: float) -> bool:
    """
    判断是否处于滞胀。

    滞胀：高通胀与高失业并存

    参数:
        inflation: 通胀率
        unemployment: 失业率
        inflation_threshold: 高通胀门槛
        unemployment_threshold: 高失业门槛

    返回:
        是否滞胀
    """
    # TODO: 判断滞胀
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
