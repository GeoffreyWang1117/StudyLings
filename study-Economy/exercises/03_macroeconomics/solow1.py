# EXERCISE: solow1
# DIFFICULTY: ★★★★☆
# TOPIC: 索洛增长模型
#
# 说明：
# 索洛模型是新古典经济增长理论的基础。
#
# 生产函数（柯布-道格拉斯）：
# Y = A * K^α * L^(1-α)
#
# 人均形式（令 k = K/L, y = Y/L）：
# y = A * k^α
#
# 资本积累方程：
# ΔK = sY - δK
# s: 储蓄率
# δ: 折旧率
#
# 人均资本变化（假设劳动力增长率为n）：
# Δk = sy - (δ + n)k
#    = sA*k^α - (δ + n)k
#
# 稳态条件：Δk = 0
# sA*k*^α = (δ + n)k*
# k* = [sA / (δ + n)]^(1/(1-α))
#
# 任务：
# 1. 计算人均产出
# 2. 计算稳态资本存量
# 3. 计算资本动态变化
#
# HINT1: 人均变量用小写字母表示
# HINT2: 稳态时投资恰好弥补折旧和人口稀释


def per_capita_output(k: float, a: float, alpha: float) -> float:
    """
    计算人均产出。

    y = A * k^α

    参数:
        k: 人均资本
        a: 全要素生产率
        alpha: 资本份额

    返回:
        人均产出 y
    """
    # TODO: 计算人均产出
    pass


def steady_state_capital(
    s: float,
    a: float,
    delta: float,
    n: float,
    alpha: float
) -> float:
    """
    计算稳态人均资本。

    k* = [sA / (δ + n)]^(1/(1-α))

    参数:
        s: 储蓄率
        a: 全要素生产率
        delta: 折旧率
        n: 人口增长率
        alpha: 资本份额

    返回:
        稳态人均资本 k*
    """
    # TODO: 计算稳态资本
    pass


def steady_state_output(
    s: float,
    a: float,
    delta: float,
    n: float,
    alpha: float
) -> float:
    """
    计算稳态人均产出。

    y* = A * (k*)^α

    参数:
        s, a, delta, n, alpha: 模型参数

    返回:
        稳态人均产出 y*
    """
    # TODO: 计算稳态产出
    pass


def capital_change(
    k: float,
    s: float,
    a: float,
    delta: float,
    n: float,
    alpha: float
) -> float:
    """
    计算人均资本的变化。

    Δk = sA*k^α - (δ + n)k

    参数:
        k: 当前人均资本
        s, a, delta, n, alpha: 模型参数

    返回:
        人均资本变化 Δk
    """
    # TODO: 计算资本变化
    pass


def investment_per_capita(k: float, s: float, a: float, alpha: float) -> float:
    """
    计算人均投资。

    i = sy = sA*k^α

    参数:
        k: 人均资本
        s: 储蓄率
        a: 全要素生产率
        alpha: 资本份额

    返回:
        人均投资
    """
    # TODO: 计算人均投资
    pass


def break_even_investment(k: float, delta: float, n: float) -> float:
    """
    计算维持人均资本不变所需的投资（持平投资）。

    持平投资 = (δ + n)k

    参数:
        k: 人均资本
        delta: 折旧率
        n: 人口增长率

    返回:
        持平投资
    """
    # TODO: 计算持平投资
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
