# EXERCISE: gdp1
# DIFFICULTY: ★★☆☆☆
# TOPIC: GDP计算
#
# 说明：
# GDP（国内生产总值）是衡量一国经济产出的核心指标。
#
# GDP 计算方法：
# 1. 支出法: GDP = C + I + G + (X - M)
#    - C: 消费支出
#    - I: 投资支出
#    - G: 政府支出
#    - X: 出口
#    - M: 进口
#
# 2. 收入法: GDP = 工资 + 利润 + 利息 + 租金 + 折旧 + 间接税
#
# 名义GDP vs 实际GDP：
# - 名义GDP: 用当期价格计算
# - 实际GDP: 用基期价格计算，剔除通胀影响
# - GDP平减指数 = 名义GDP / 实际GDP × 100
#
# 任务：
# 1. 用支出法计算GDP
# 2. 计算实际GDP
# 3. 计算GDP增长率
#
# HINT1: 净出口 = 出口 - 进口
# HINT2: 实际GDP = 名义GDP / (1 + 通胀率)


def gdp_expenditure_approach(
    consumption: float,
    investment: float,
    government: float,
    exports: float,
    imports: float
) -> float:
    """
    用支出法计算GDP。

    GDP = C + I + G + (X - M)

    参数:
        consumption: 消费支出 C
        investment: 投资支出 I
        government: 政府支出 G
        exports: 出口 X
        imports: 进口 M

    返回:
        GDP
    """
    # TODO: 计算GDP
    pass


def real_gdp(nominal_gdp: float, gdp_deflator: float) -> float:
    """
    计算实际GDP。

    实际GDP = 名义GDP / GDP平减指数 × 100

    参数:
        nominal_gdp: 名义GDP
        gdp_deflator: GDP平减指数（例如：110 表示相对基期上涨10%）

    返回:
        实际GDP
    """
    # TODO: 计算实际GDP
    pass


def gdp_growth_rate(gdp_current: float, gdp_previous: float) -> float:
    """
    计算GDP增长率。

    增长率 = (当期GDP - 上期GDP) / 上期GDP × 100

    参数:
        gdp_current: 当期GDP
        gdp_previous: 上期GDP

    返回:
        增长率（百分比）
    """
    # TODO: 计算GDP增长率
    pass


def gdp_per_capita(gdp: float, population: float) -> float:
    """
    计算人均GDP。

    参数:
        gdp: GDP总量
        population: 人口

    返回:
        人均GDP
    """
    # TODO: 计算人均GDP
    pass


def net_exports(exports: float, imports: float) -> float:
    """
    计算净出口。

    参数:
        exports: 出口
        imports: 进口

    返回:
        净出口
    """
    # TODO: 计算净出口
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
