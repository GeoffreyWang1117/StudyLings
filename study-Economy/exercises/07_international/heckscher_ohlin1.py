# EXERCISE: heckscher_ohlin1
# DIFFICULTY: ★★★☆☆
# TOPIC: 赫克歇尔-俄林模型
#
# 说明：
# H-O模型（又称要素禀赋理论）解释为什么不同国家生产不同商品。
# 由瑞典经济学家赫克歇尔（1919）和俄林（1933）提出。
#
# 【核心思想】
# 一国应出口密集使用其丰裕要素的商品，
# 进口密集使用其稀缺要素的商品。
#
# 【模型假设】（2×2×2模型）
# - 两个国家（本国与外国）
# - 两种商品（X和Y）
# - 两种生产要素（资本K和劳动L）
# - 两国技术相同（生产函数相同）
# - 两国要素禀赋不同
# - 规模报酬不变
# - 完全竞争
# - 要素国内流动，国际不流动
#
# 【四大定理】
# 1. H-O定理：资本丰裕国出口资本密集品
# 2. 要素价格均等化定理：自由贸易使两国要素价格趋同
# 3. Stolper-Samuelson定理：商品价格上涨提高密集使用要素的回报
# 4. Rybczynski定理：要素增加扩大密集使用该要素的产品产出
#
# 【关键概念】
# - 要素丰裕度：比较K/L比率（物理定义）或比较要素价格（价格定义）
# - 要素密集度：生产中K/L的比率
#
# 任务：
# 1. 判断要素丰裕度
# 2. 确定贸易模式
# 3. 分析要素价格变化
#
# HINT1: 要素丰裕度比较K/L
# HINT2: 商品密集度由生产技术决定
# HINT3: 贸易惠及丰裕要素所有者

import numpy as np


def factor_abundance(
    k_home: float,
    l_home: float,
    k_foreign: float,
    l_foreign: float
) -> str:
    """
    判断本国的要素丰裕度（物理定义）。

    物理定义：比较两国的资本-劳动比率
    - 若 K_home/L_home > K_foreign/L_foreign，本国资本丰裕
    - 若 K_home/L_home < K_foreign/L_foreign，本国劳动丰裕

    参数:
        k_home: 本国资本存量
        l_home: 本国劳动力数量
        k_foreign: 外国资本存量
        l_foreign: 外国劳动力数量

    返回:
        "capital"（本国资本丰裕）
        "labor"（本国劳动丰裕）

    示例:
        本国：K=100, L=50 → K/L=2
        外国：K=80, L=80 → K/L=1
        本国K/L更高，资本丰裕
    """
    # TODO: 判断要素丰裕度
    # 提示：比较K/L比率
    pass


def factor_intensity(
    k_x: float,
    l_x: float,
    k_y: float,
    l_y: float
) -> tuple[str, str]:
    """
    判断商品的要素密集度。

    比较生产X和Y时使用的K/L比率：
    - 若 K_X/L_X > K_Y/L_Y，则X是资本密集品
    - 若 K_X/L_X < K_Y/L_Y，则X是劳动密集品

    参数:
        k_x: 生产X的资本投入
        l_x: 生产X的劳动投入
        k_y: 生产Y的资本投入
        l_y: 生产Y的劳动投入

    返回:
        (资本密集品, 劳动密集品)

    示例:
        X：K=10, L=5 → K/L=2
        Y：K=6, L=6 → K/L=1
        X是资本密集品，Y是劳动密集品
    """
    # TODO: 判断要素密集度
    # 提示：比较两种商品的K/L比率
    pass


def ho_trade_pattern(
    k_home: float,
    l_home: float,
    k_foreign: float,
    l_foreign: float,
    k_x: float,
    l_x: float,
    k_y: float,
    l_y: float
) -> tuple[str, str]:
    """
    根据H-O定理确定贸易模式。

    H-O定理核心结论：
    - 资本丰裕国出口资本密集品
    - 劳动丰裕国出口劳动密集品

    步骤：
    1. 判断本国要素丰裕度
    2. 判断各商品要素密集度
    3. 匹配确定出口品

    参数:
        k_home, l_home: 本国要素禀赋
        k_foreign, l_foreign: 外国要素禀赋
        k_x, l_x: X的要素需求
        k_y, l_y: Y的要素需求

    返回:
        (本国出口品, 本国进口品)

    示例:
        本国资本丰裕，X是资本密集品
        → 本国出口X，进口Y
    """
    # TODO: 确定贸易模式
    # 提示：结合要素丰裕度和商品密集度
    pass


def unit_cost(
    a_k: float,
    a_l: float,
    r: float,
    w: float
) -> float:
    """
    计算单位成本。

    在完全竞争和规模报酬不变下，价格等于单位成本。

    单位成本 = 资本成本 + 劳动成本
    c = a_K × r + a_L × w

    其中：
    - a_K: 单位产出的资本需求（资本系数）
    - a_L: 单位产出的劳动需求（劳动系数）
    - r: 资本回报率（租金率）
    - w: 工资率

    参数:
        a_k: 资本系数（如：每单位产出需0.5单位资本）
        a_l: 劳动系数（如：每单位产出需2单位劳动）
        r: 资本回报率（如：10%）
        w: 工资率（如：每小时20元）

    返回:
        单位成本

    示例:
        >>> unit_cost(0.5, 2, 0.1, 20)
        40.05  # 0.5×0.1 + 2×20
    """
    # TODO: 计算单位成本
    # 提示：c = a_K × r + a_L × w
    pass


def factor_prices_from_goods_prices(
    p_x: float,
    p_y: float,
    a_kx: float,
    a_lx: float,
    a_ky: float,
    a_ly: float
) -> tuple[float, float]:
    """
    从商品价格求解要素价格（要素价格均等化定理的基础）。

    零利润条件（完全竞争下价格=成本）：
    p_X = a_KX × r + a_LX × w  ... (1)
    p_Y = a_KY × r + a_LY × w  ... (2)

    两个方程两个未知数，可求解r和w。

    矩阵形式：
    [p_X]   [a_KX  a_LX] [r]
    [p_Y] = [a_KY  a_LY] [w]

    这说明：给定技术(a)和商品价格(p)，要素价格(r,w)被唯一确定！
    这是要素价格均等化定理的数学基础。

    参数:
        p_x, p_y: 商品价格
        a_kx, a_lx: X的要素系数
        a_ky, a_ly: Y的要素系数

    返回:
        (资本回报率r, 工资率w)
    """
    # TODO: 求解要素价格
    # 提示：解二元一次方程组
    pass


def stolper_samuelson(
    price_change_x: float,
    theta_kx: float,
    theta_lx: float
) -> tuple[float, float]:
    """
    Stolper-Samuelson定理：商品价格变化对要素回报的影响。

    SS定理内容：
    商品价格上涨将提高密集使用要素的实际回报，
    降低另一要素的实际回报（放大效应）。

    设X是资本密集品，当X价格上涨时：
    - 资本回报率上涨幅度 > X价格上涨幅度
    - 工资率下降

    近似公式（对数微分）：
    θ_KX × r̂ + θ_LX × ŵ = p̂_X
    其中θ是成本份额，ˆ表示变化率

    参数:
        price_change_x: X价格变化率（如0.1表示10%）
        theta_kx: X中资本成本份额（如0.6）
        theta_lx: X中劳动成本份额（如0.4）

    返回:
        (资本回报变化率, 工资变化率)

    注意:
        需要额外假设或简化才能唯一确定两个变化率
        这里假设两种商品都在生产
    """
    # TODO: 计算SS效应
    # 提示：利用成本份额分解价格变化
    pass


def rybczynski(
    labor_increase: float,
    lambda_lx: float,
    lambda_ly: float
) -> tuple[float, float]:
    """
    Rybczynski定理：要素禀赋变化对产出的影响。

    Rybczynski定理内容：
    在商品价格不变（小国假设）下，一种要素增加会：
    - 扩大密集使用该要素的产品产出
    - 减少另一产品的产出

    这解释了要素增长的"荷兰病"效应。

    近似公式：
    X̂ > L̂ > 0 > Ŷ（若X是劳动密集品）

    参数:
        labor_increase: 劳动增加率
        lambda_lx: X部门劳动占总劳动的份额
        lambda_ly: Y部门劳动占总劳动的份额

    返回:
        (X产量变化率, Y产量变化率)

    示例:
        劳动增加10%，X是劳动密集品
        → X产出增加>10%，Y产出减少
    """
    # TODO: 计算Rybczynski效应
    # 提示：劳动密集品产出增加超过要素增加幅度
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
