# EXERCISE: okun1
# DIFFICULTY: ★★★☆☆
# TOPIC: 奥肯定律
#
# 说明：
# 奥肯定律描述产出缺口与失业缺口之间的经验关系。
#
# 奥肯定律的版本：
#
# 1. 差分版本（最常用）：
#    ΔY/Y = 3% - 2(Δu)
#    即GDP增长1%，失业率下降约0.5个百分点
#
# 2. 缺口版本：
#    (Y - Y*)/Y* = -β(u - u*)
#    其中 β ≈ 2（奥肯系数）
#
# 奥肯系数反映了：
# - 劳动力参与率的周期性变化
# - 工时的周期性变化
# - 劳动生产率的周期性变化
#
# 任务：
# 1. 实现奥肯定律的不同版本
# 2. 计算奥肯系数
# 3. 分析产出与失业的关系
#
# HINT1: 奥肯系数通常在2-3之间
# HINT2: 产出每低于潜在产出2-3%，失业率高出1个百分点


def okun_gdp_growth(unemployment_change: float, trend_growth: float = 3.0, okun_coef: float = 2.0) -> float:
    """
    差分版本奥肯定律：根据失业率变化计算GDP增长。

    ΔY/Y = 趋势增长率 - β × Δu

    参数:
        unemployment_change: 失业率变化（百分点）
        trend_growth: 趋势增长率（百分比，默认3%）
        okun_coef: 奥肯系数（默认2）

    返回:
        GDP增长率（百分比）
    """
    # TODO: 计算GDP增长
    pass


def okun_unemployment_change(gdp_growth: float, trend_growth: float = 3.0, okun_coef: float = 2.0) -> float:
    """
    差分版本奥肯定律：根据GDP增长计算失业率变化。

    Δu = (趋势增长率 - ΔY/Y) / β

    参数:
        gdp_growth: GDP增长率（百分比）
        trend_growth: 趋势增长率（百分比）
        okun_coef: 奥肯系数

    返回:
        失业率变化（百分点）
    """
    # TODO: 计算失业率变化
    pass


def output_gap_from_unemployment(
    u: float,
    u_natural: float,
    okun_coef: float = 2.0
) -> float:
    """
    缺口版本奥肯定律：根据失业率计算产出缺口。

    (Y - Y*)/Y* = -β(u - u*)

    参数:
        u: 实际失业率
        u_natural: 自然失业率
        okun_coef: 奥肯系数

    返回:
        产出缺口（百分比）
    """
    # TODO: 计算产出缺口
    pass


def unemployment_from_output_gap(
    output_gap: float,
    u_natural: float,
    okun_coef: float = 2.0
) -> float:
    """
    缺口版本奥肯定律：根据产出缺口计算失业率。

    u = u* - (Y - Y*) / (β × Y*)

    参数:
        output_gap: 产出缺口（百分比）
        u_natural: 自然失业率
        okun_coef: 奥肯系数

    返回:
        失业率
    """
    # TODO: 计算失业率
    pass


def estimate_okun_coefficient(
    gdp_growth_list: list[float],
    unemployment_change_list: list[float]
) -> float:
    """
    估计奥肯系数。

    使用简单线性回归：Δu = α - (1/β)ΔY
    β = -1 / slope

    参数:
        gdp_growth_list: GDP增长率序列
        unemployment_change_list: 失业率变化序列

    返回:
        估计的奥肯系数
    """
    # TODO: 估计奥肯系数
    # 提示：使用最小二乘法或简单的斜率计算
    pass


def required_growth_for_unemployment_reduction(
    target_reduction: float,
    trend_growth: float = 3.0,
    okun_coef: float = 2.0
) -> float:
    """
    计算使失业率下降所需的GDP增长率。

    参数:
        target_reduction: 目标失业率下降幅度（百分点）
        trend_growth: 趋势增长率
        okun_coef: 奥肯系数

    返回:
        所需GDP增长率
    """
    # TODO: 计算所需增长率
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
