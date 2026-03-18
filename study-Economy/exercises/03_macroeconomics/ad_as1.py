# EXERCISE: ad_as1
# DIFFICULTY: ★★★★☆
# TOPIC: 总需求-总供给模型
#
# 说明：
# AD-AS模型是分析价格水平与产出关系的宏观模型。
#
# 总需求（AD）曲线：
# 来源于IS-LM模型，价格水平P变化时的均衡产出轨迹
# P ↑ → 实际货币供给(M/P) ↓ → LM左移 → Y ↓
# 所以AD曲线向右下方倾斜
#
# 总供给（AS）曲线：
# 短期AS（SRAS）：向右上方倾斜
# 长期AS（LRAS）：垂直于自然产出水平
#
# 短期AS: P = Pᵉ + λ(Y - Yₙ)
# 其中 Pᵉ是预期价格，Yₙ是自然产出水平
#
# 任务：
# 1. 推导AD曲线
# 2. 实现短期AS曲线
# 3. 求解AD-AS均衡
#
# HINT1: AD曲线本质是IS-LM对不同P的解
# HINT2: 长期均衡时 P = Pᵉ，Y = Yₙ


def ad_curve_output(
    p: float,
    c0: float, c: float, t: float, i0: float, d: float, g: float,
    m: float, k: float, h: float
) -> float:
    """
    计算给定价格水平下的总需求。

    AD曲线来源于IS-LM均衡的Y*对P的关系。

    参数:
        p: 价格水平
        其他参数: IS-LM模型参数

    返回:
        总需求（产出）
    """
    # TODO: 计算AD曲线上的产出
    # 使用IS-LM的均衡解
    pass


def sras_price(y: float, y_natural: float, p_expected: float, lambda_: float) -> float:
    """
    短期总供给曲线：给定产出，计算价格水平。

    P = Pᵉ + λ(Y - Yₙ)

    参数:
        y: 产出水平
        y_natural: 自然产出水平
        p_expected: 预期价格水平
        lambda_: 价格对产出缺口的敏感度

    返回:
        价格水平
    """
    # TODO: 计算SRAS上的价格
    pass


def sras_output(p: float, y_natural: float, p_expected: float, lambda_: float) -> float:
    """
    短期总供给曲线：给定价格，计算产出。

    Y = Yₙ + (P - Pᵉ) / λ

    参数:
        p: 价格水平
        y_natural: 自然产出水平
        p_expected: 预期价格水平
        lambda_: 价格敏感度

    返回:
        产出水平
    """
    # TODO: 计算SRAS上的产出
    pass


def lras_output(y_natural: float) -> float:
    """
    长期总供给：返回自然产出水平。

    长期AS是垂直的，产出等于自然产出水平。

    参数:
        y_natural: 自然产出水平

    返回:
        长期产出（等于自然产出）
    """
    # TODO: 返回LRAS
    pass


def output_gap(y: float, y_natural: float) -> float:
    """
    计算产出缺口。

    产出缺口 = Y - Yₙ

    正值：经济过热
    负值：经济衰退

    参数:
        y: 实际产出
        y_natural: 自然产出

    返回:
        产出缺口
    """
    # TODO: 计算产出缺口
    pass


def inflation_from_output_gap(output_gap: float, lambda_: float) -> float:
    """
    根据产出缺口计算通胀压力。

    通胀 = λ × (Y - Yₙ)

    参数:
        output_gap: 产出缺口
        lambda_: 菲利普斯曲线斜率

    返回:
        通胀率变化
    """
    # TODO: 计算通胀压力
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
