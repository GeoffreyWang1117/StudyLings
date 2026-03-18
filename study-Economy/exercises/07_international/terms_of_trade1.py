# EXERCISE: terms_of_trade1
# DIFFICULTY: ★★★☆☆
# TOPIC: 贸易条件
#
# 说明：
# 贸易条件（Terms of Trade, TOT）是衡量一国在国际贸易中
# 交换比率的重要指标，反映出口商品相对于进口商品的购买力。
#
# 【贸易条件的定义】
#
# 商品贸易条件（净易货贸易条件）：
# TOT = P_X / P_M = 出口价格指数 / 进口价格指数
#
# 解读：
# - TOT = 100：基期水平
# - TOT > 100：贸易条件改善（同样出口可换更多进口）
# - TOT < 100：贸易条件恶化（同样出口换更少进口）
#
# 【贸易条件的类型】
#
# 1. 商品贸易条件（最常用）
#    TOT = P_X / P_M
#
# 2. 收入贸易条件
#    收入TOT = (P_X / P_M) × 出口量
#    反映进口能力
#
# 3. 单要素贸易条件
#    考虑生产率变化
#
# 4. 双要素贸易条件
#    同时考虑进出口生产率
#
# 【贸易条件变化的福利效应】
#
# 贸易条件改善：
# - 相同出口量可获得更多进口
# - 实际收入增加
# - 福利提升
#
# 收入效应的计算：
# ΔY/Y ≈ (X/Y) × (ΔTOT/TOT)
#
# 其中 X/Y 是出口占GDP比重
#
# 【国内总收入（GDI）vs 国内生产总值（GDP）】
#
# GDP衡量国内生产
# GDI = GDP + 贸易条件变化带来的收益
#
# 贸易利得 = (TOT_new - TOT_old) / TOT_old × 出口价值
#
# 对于出口依赖型经济，GDI和GDP可能有显著差异
#
# 【普雷维什-辛格假说】
#
# Raul Prebisch和Hans Singer（1950年代）提出：
# 初级产品相对于制成品的贸易条件存在长期恶化趋势
#
# 理论解释：
# 1. 需求方面：
#    - 初级产品需求收入弹性低
#    - 恩格尔定律：收入增加，食品支出比例下降
#
# 2. 供给方面：
#    - 技术进步节约原材料
#    - 合成替代品出现
#
# 3. 市场结构：
#    - 初级产品市场接近完全竞争
#    - 制成品市场存在垄断
#    - 生产率提高在制成品国体现为工资上涨
#    - 在初级产品国体现为价格下降
#
# 政策含义（进口替代工业化的理论基础）：
# - 发展中国家应发展工业
# - 减少对初级产品出口的依赖
#
# 【贫困化增长（Immiserizing Growth）】
#
# Jagdish Bhagwati（1958）提出：
# 出口部门的增长可能导致福利下降
#
# 条件：
# - 大国（影响世界价格）
# - 出口偏向型增长
# - 外国需求弹性低
#
# 机制：
# 出口增长 → 世界价格下降 → 贸易条件恶化
# 如果贸易条件恶化程度 > 产出增长带来的福利
# 则总福利下降
#
# 【荷兰病（Dutch Disease）】
#
# 资源出口繁荣导致其他贸易部门萎缩的现象
#
# 机制：
# 1. 资源出口增加 → 外汇收入增加
# 2. 本币升值（实际汇率上升）
# 3. 其他贸易部门（制造业）竞争力下降
# 4. "去工业化"
#
# 案例：
# - 1960年代荷兰天然气出口
# - 产油国的制造业萎缩
#
# 任务：
# 1. 计算和分析贸易条件
# 2. 评估贸易条件变化的福利效应
# 3. 理解P-S假说和贫困化增长
# 4. 分析荷兰病现象
#
# HINT1: 贸易条件改善意味着出口购买力提高
# HINT2: 初级产品出口国面临贸易条件长期恶化风险
# HINT3: 资源繁荣可能带来荷兰病

import numpy as np


def terms_of_trade(
    export_price_index: float,
    import_price_index: float
) -> float:
    """
    计算贸易条件指数。

    贸易条件（净易货贸易条件）衡量出口品相对进口品的价格。

    公式：
    TOT = P_X / P_M × 100

    其中：
    - P_X: 出口价格指数
    - P_M: 进口价格指数

    经济学含义：
    - TOT上升：出口品相对升值，贸易条件改善
    - TOT下降：出口品相对贬值，贸易条件恶化

    与实际汇率的关系：
    TOT改善 ≈ 实际汇率升值（从贸易品角度）

    参数:
        export_price_index: 出口价格指数
                            例如：P_X = 110（相比基期上涨10%）
        import_price_index: 进口价格指数
                            例如：P_M = 105（相比基期上涨5%）

    返回:
        贸易条件指数（基期=100）

    示例:
        出口价格指数110，进口价格指数105
        >>> terms_of_trade(110, 105)
        104.76  # 贸易条件改善约5%

        计算：110 / 105 × 100 = 104.76

    TODO提示：
    - TOT = (P_X / P_M) × 100
    - 如果价格指数已经是以100为基期，则直接相除
    """
    # TODO: 计算贸易条件
    # 提示：TOT = export_price_index / import_price_index
    # 如果需要以100为基期，乘以100
    pass


def terms_of_trade_change(
    tot_new: float,
    tot_old: float
) -> float:
    """
    计算贸易条件变化率。

    贸易条件变化率反映一段时期内交换比率的改变。

    公式：
    ΔTOT/TOT = (TOT_new - TOT_old) / TOT_old

    解读：
    - 正值：贸易条件改善
    - 负值：贸易条件恶化

    重要性：
    - 对出口依赖型经济影响巨大
    - 石油价格波动对产油国TOT影响显著
    - 大宗商品价格周期影响发展中国家

    参数:
        tot_new: 新时期贸易条件指数
                 例如：105
        tot_old: 旧时期贸易条件指数
                 例如：100

    返回:
        贸易条件变化率（小数形式）

    示例:
        贸易条件从100变为105
        >>> terms_of_trade_change(105, 100)
        0.05  # 改善5%

        贸易条件从100变为90
        >>> terms_of_trade_change(90, 100)
        -0.10  # 恶化10%

    TODO提示：
    - ΔTOT/TOT = (tot_new - tot_old) / tot_old
    """
    # TODO: 计算贸易条件变化率
    # 提示：change = (tot_new - tot_old) / tot_old
    pass


def income_effect_of_tot_change(
    export_volume: float,
    import_volume: float,
    tot_change: float,
    gdp: float
) -> float:
    """
    计算贸易条件变化的收入效应。

    贸易条件变化会影响一国的实际收入（购买力）。

    基本思路：
    - 出口数量不变时，出口价格上升增加收入
    - 进口数量不变时，进口价格上升减少购买力

    收入效应估计（简化）：
    ΔY/Y ≈ (X/Y) × (ΔTOT/TOT)

    其中：
    - X/Y: 出口占GDP的比重
    - ΔTOT/TOT: 贸易条件变化率

    更精确的计算考虑贸易差额：
    实际收入变化 = 出口收入变化 - 进口成本变化

    参数:
        export_volume: 出口量（或出口值作为代理）
                       例如：500亿美元
        import_volume: 进口量（本函数中未直接使用）
        tot_change: 贸易条件变化率
                    例如：0.05（改善5%）
        gdp: 国内生产总值
             例如：2000亿美元

    返回:
        实际收入变化率（占GDP比例）

    示例:
        出口500亿，GDP 2000亿，贸易条件改善5%
        >>> income_effect_of_tot_change(500, 400, 0.05, 2000)
        0.0125  # 实际收入增加GDP的1.25%

        计算：(500/2000) × 0.05 = 0.0125

    TODO提示：
    - 收入效应 ≈ (export_volume / gdp) × tot_change
    """
    # TODO: 计算收入效应
    # 提示：income_effect = (export_volume / gdp) × tot_change
    pass


def gross_domestic_income(
    gdp: float,
    trading_gains: float
) -> float:
    """
    计算国内总收入（考虑贸易条件）。

    GDP衡量国内生产，但不反映贸易条件变化带来的购买力变化。

    国内总收入（GDI）调整了这一因素：
    GDI = GDP + 贸易利得

    贸易利得 = 贸易条件变化带来的实际收入变化

    区别：
    - GDP：生产角度衡量经济活动
    - GDI：收入角度衡量购买力

    案例：
    - 石油出口国：油价上涨时 GDI >> GDP
    - 石油进口国：油价上涨时 GDI << GDP

    参数:
        gdp: 国内生产总值
             例如：1000亿美元
        trading_gains: 贸易条件变化带来的收益（或损失）
                       例如：50亿美元（贸易条件改善）
                       例如：-30亿美元（贸易条件恶化）

    返回:
        国内总收入

    示例:
        GDP 1000亿，贸易利得50亿
        >>> gross_domestic_income(1000, 50)
        1050.0  # GDI = 1050亿

        GDP 1000亿，贸易损失30亿
        >>> gross_domestic_income(1000, -30)
        970.0  # GDI = 970亿

    TODO提示：
    - GDI = GDP + trading_gains
    """
    # TODO: 计算GDI
    # 提示：GDI = gdp + trading_gains
    pass


def immiserizing_growth_condition(
    export_growth: float,
    demand_elasticity: float,
    supply_share: float
) -> bool:
    """
    判断是否可能发生贫困化增长。

    贫困化增长（Immiserizing Growth）发生条件：
    出口增长导致的贸易条件恶化程度超过了产出增长的收益

    简化条件：
    当一个大的出口国（市场份额大）面临低弹性的外国需求时，
    出口扩张可能导致价格大幅下跌。

    关键判断：
    价格下跌幅度 ≈ (1/ε) × 出口增长 × 市场份额

    如果：
    价格下跌导致的收入损失 > 数量增加带来的收入
    则发生贫困化增长

    简化条件：
    (1/ε) × supply_share > (1 - 原有利润率)

    更简单的判断规则：
    如果 export_growth / demand_elasticity × supply_share > threshold
    则可能发生

    参数:
        export_growth: 出口增长率
                       例如：0.20（增长20%）
        demand_elasticity: 世界需求价格弹性（绝对值）
                           例如：0.5（低弹性）
        supply_share: 该国在世界市场的供给份额
                      例如：0.30（占30%）

    返回:
        是否可能发生贫困化增长（True/False）

    示例:
        出口增长20%，需求弹性0.5，市场份额30%
        >>> immiserizing_growth_condition(0.20, 0.5, 0.30)
        True  # 价格下跌幅度可能很大

        出口增长10%，需求弹性2.0，市场份额10%
        >>> immiserizing_growth_condition(0.10, 2.0, 0.10)
        False  # 影响较小

    TODO提示：
    - 估计价格下跌幅度：price_drop ≈ (export_growth × supply_share) / demand_elasticity
    - 如果 price_drop > export_growth，则可能发生贫困化增长
    - 或使用简化阈值判断
    """
    # TODO: 判断贫困化增长条件
    # 提示：
    # price_effect = (export_growth × supply_share) / demand_elasticity
    # return price_effect > 某个阈值（如 export_growth × 0.5）
    pass


def commodity_price_volatility(
    prices: np.ndarray
) -> float:
    """
    计算商品价格波动率。

    初级产品价格通常比制成品波动大，
    这给依赖商品出口的国家带来不确定性。

    波动率计算（变异系数）：
    CV = 标准差 / 均值

    或使用收益率的标准差。

    高波动率的影响：
    - 收入不稳定
    - 难以规划财政支出
    - 投资决策困难
    - 可能引发经济周期

    参数:
        prices: 价格时间序列
                例如：[100, 120, 90, 110, 105]（5年数据）

    返回:
        变异系数（标准差/均值）

    示例:
        价格序列 [100, 120, 90, 110, 105]
        >>> commodity_price_volatility(np.array([100, 120, 90, 110, 105]))
        0.10  # 变异系数约10%

    TODO提示：
    - 计算均值：np.mean(prices)
    - 计算标准差：np.std(prices)
    - CV = std / mean
    """
    # TODO: 计算价格波动率
    # 提示：
    # mean = np.mean(prices)
    # std = np.std(prices)
    # return std / mean
    pass


def prebisch_singer_trend(
    commodity_prices: np.ndarray,
    manufacture_prices: np.ndarray,
    years: np.ndarray
) -> float:
    """
    估计普雷维什-辛格趋势（贸易条件的长期趋势）。

    P-S假说：初级产品相对制成品的价格存在长期下降趋势

    检验方法：
    对贸易条件取对数，然后对时间做回归：
    ln(TOT) = α + β × t + ε

    其中：
    - β < 0: 支持P-S假说（贸易条件恶化）
    - β > 0: 反对P-S假说（贸易条件改善）

    趋势系数β的含义：
    每年贸易条件变化的百分比

    实证结果：
    - 1900-1980年：β ≈ -0.5%到-1%/年
    - 近年来结论不一

    参数:
        commodity_prices: 初级产品价格指数序列
                          例如：[100, 98, 95, 93, 90]
        manufacture_prices: 制成品价格指数序列
                            例如：[100, 102, 105, 108, 112]
        years: 年份序列
               例如：[2000, 2001, 2002, 2003, 2004]

    返回:
        趋势系数β（每年变化率）

    示例:
        >>> commodity = np.array([100, 98, 95, 93, 90])
        >>> manufacture = np.array([100, 102, 105, 108, 112])
        >>> years = np.array([0, 1, 2, 3, 4])
        >>> prebisch_singer_trend(commodity, manufacture, years)
        -0.05  # 每年贸易条件恶化约5%

    TODO提示：
    - 计算贸易条件：TOT = commodity / manufacture
    - 取对数：log_tot = np.log(TOT)
    - 线性回归求斜率：可用 np.polyfit(years, log_tot, 1)
    """
    # TODO: 估计P-S趋势
    # 提示：
    # tot = commodity_prices / manufacture_prices
    # log_tot = np.log(tot)
    # slope, intercept = np.polyfit(years, log_tot, 1)
    # return slope
    pass


def dutch_disease_effect(
    resource_boom: float,
    real_appreciation: float,
    manufacturing_elasticity: float
) -> float:
    """
    计算荷兰病效应对制造业的影响。

    荷兰病机制：
    1. 资源出口繁荣 → 外汇收入增加
    2. 本币升值（或非贸易品价格上涨）
    3. 制造业成本上升，竞争力下降
    4. 制造业产出下降（去工业化）

    简化模型：
    制造业产出变化 ≈ -实际升值幅度 × 制造业弹性

    弹性含义：
    - 高弹性：制造业对汇率敏感，受冲击大
    - 低弹性：制造业有定价能力或差异化

    长期影响：
    - 人力资本流向资源部门
    - 制造业学习曲线中断
    - 资源枯竭后难以恢复

    参数:
        resource_boom: 资源出口增长幅度
                       例如：0.50（增长50%）
        real_appreciation: 实际汇率升值幅度
                           例如：0.15（升值15%）
        manufacturing_elasticity: 制造业对汇率的弹性
                                  例如：0.8（汇率升值1%，产出下降0.8%）

    返回:
        制造业产出变化（负值表示下降）

    示例:
        资源繁荣50%，实际升值15%，制造业弹性0.8
        >>> dutch_disease_effect(0.50, 0.15, 0.8)
        -0.12  # 制造业产出下降12%

        计算：-0.15 × 0.8 = -0.12

    TODO提示：
    - manufacturing_change = -real_appreciation × manufacturing_elasticity
    """
    # TODO: 计算荷兰病效应
    # 提示：manufacturing_change = -real_appreciation × manufacturing_elasticity
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
