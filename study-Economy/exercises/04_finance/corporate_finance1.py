# EXERCISE: corporate_finance1
# DIFFICULTY: ★★★★☆
# TOPIC: 公司金融与资本结构
#
# 说明：
# 公司金融（Corporate Finance）是金融学的核心分支，研究企业如何进行融资和投资决策，
# 以最大化股东价值。本模块聚焦于资本结构理论和资本成本计算。
#
# 【理论背景】
# 资本结构（Capital Structure）指企业融资中债务与股权的比例组合。
# 核心问题：是否存在"最优"资本结构能最大化企业价值？
#
# 【MM定理（Modigliani-Miller Theorem）】
# 1958年，Franco Modigliani和Merton Miller提出了现代资本结构理论的基石。
#
# MM定理的假设前提（完美资本市场）：
# 1. 无税收
# 2. 无交易成本和破产成本
# 3. 信息对称
# 4. 个人和公司借贷利率相同
# 5. 无代理成本
#
# MM定理 I（无税）：
#   企业价值与资本结构无关
#   V_L = V_U（有杠杆企业价值 = 无杠杆企业价值）
#   直觉：企业价值由资产创造的现金流决定，融资方式只是切蛋糕，不改变蛋糕大小
#
# MM定理 II（无税）：
#   股权成本随杠杆线性增加
#   r_E = r_U + (r_U - r_D) × (D/E)
#   其中：r_E = 股权成本，r_U = 无杠杆资本成本，r_D = 债务成本，D/E = 债务股权比
#   直觉：杠杆放大了股东的风险，因此要求更高回报
#
# MM定理（有税）：
#   考虑公司所得税后，债务利息可以抵税：
#   V_L = V_U + T × D（有杠杆价值 = 无杠杆价值 + 税盾价值）
#   含义：全部债务融资可最大化企业价值（但忽略了破产成本）
#
# 【加权平均资本成本（WACC）】
# WACC = (E/V) × r_E + (D/V) × r_D × (1-T)
# 其中：
# - E = 股权市值，D = 债务市值，V = E + D = 企业总价值
# - r_E = 股权成本（通常用CAPM估算）
# - r_D = 债务成本（税前）
# - T = 公司税率
# - (1-T) 反映了债务利息的税盾效应
#
# WACC的用途：
# - 作为投资项目的折现率
# - 评估企业价值（DCF估值）
# - 资本预算决策
#
# 【权衡理论（Trade-off Theory）】
# 最优资本结构是在债务的税盾收益与财务困境成本之间取得平衡：
# V = V_U + PV(税盾) - PV(财务困境成本)
#
# 财务困境成本包括：
# - 直接成本：法律费用、行政费用
# - 间接成本：客户/供应商流失、管理层分心、投资不足
#
# 【代理问题】
# 1. 股东-经理冲突：
#    - 经理可能追求个人利益（帝国建造、过度消费）
#    - 解决：激励机制、监督、债务约束
#
# 2. 股东-债权人冲突：
#    - 资产替代：股东倾向高风险项目
#    - 投资不足：当收益主要归债权人时
#    - 解决：债务契约、可转债
#
# 任务：
# 1. 计算加权平均资本成本（WACC）
# 2. 验证MM定理的各种推论
# 3. 分析税盾效应
# 4. 理解杠杆对股权成本的影响
#
# HINT1: 税盾价值 = T × D（假设永续债务且无违约风险）
# HINT2: 杠杆增加股权风险，体现在股权成本的上升
# HINT3: WACC随杠杆先降后升（权衡理论）

import numpy as np


def wacc(
    equity_value: float,
    debt_value: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float
) -> float:
    """
    计算加权平均资本成本（Weighted Average Cost of Capital）。

    【公式推导】
    企业的资本来源有两种：股权E和债务D。
    企业总价值 V = E + D

    各资本来源的成本加权平均：
    WACC = (E/V) × r_E + (D/V) × r_D × (1-T)

    其中 (1-T) 反映债务利息的税盾效应：
    - 债务利息在税前扣除，实际成本为 r_D × (1-T)
    - 例：债务成本5%，税率25%，实际成本 = 5% × 0.75 = 3.75%

    【经济含义】
    WACC代表企业的平均融资成本，也是新投资项目的最低要求回报率。
    - WACC越低，企业价值越高（用更低的折现率折现未来现金流）
    - 最优资本结构是使WACC最小化的债务比例

    参数:
        equity_value: 股权市值（E），通常为流通股数 × 股价
        debt_value: 债务市值（D），包括长期债务和有息短期债务
        cost_of_equity: 股权成本（r_E），通常用CAPM计算：r_E = r_f + β×(r_m - r_f)
        cost_of_debt: 债务成本（r_D），通常用债券收益率或贷款利率
        tax_rate: 边际公司所得税率（T）

    返回:
        WACC（加权平均资本成本）

    示例:
        股权价值800亿，债务200亿，股权成本12%，债务成本6%，税率25%
        >>> wacc(800, 200, 0.12, 0.06, 0.25)
        0.105  # WACC = 80% × 12% + 20% × 6% × 75% = 10.5%

    注意:
        - 股权和债务应使用市值而非账面价值
        - 税率应使用边际税率而非有效税率
        - 成本应与资本来源的风险匹配
    """
    # TODO: 计算WACC
    # 步骤1: 计算总价值 V = E + D
    # 步骤2: 计算股权权重 w_E = E / V
    # 步骤3: 计算债务权重 w_D = D / V
    # 步骤4: WACC = w_E × r_E + w_D × r_D × (1-T)
    pass


def levered_cost_of_equity(
    unlevered_cost: float,
    cost_of_debt: float,
    debt_equity_ratio: float,
    tax_rate: float
) -> float:
    """
    MM定理 II：计算有杠杆的股权成本。

    【公式推导】
    从MM定理出发，企业的加权资本成本不变（无税情况下）：
    r_U = (E/V) × r_E + (D/V) × r_D

    解出 r_E：
    r_E = r_U + (r_U - r_D) × (D/E)

    有税情况下，考虑税盾效应：
    r_E = r_U + (r_U - r_D) × (D/E) × (1-T)

    【经济直觉】
    - (r_U - r_D)：股权相对于债务的风险溢价
    - D/E：杠杆倍数
    - 杠杆放大了股东的风险敞口，因此要求更高回报
    - 税盾效应部分抵消了杠杆的风险增加

    【Hamada方程的联系】
    β_L = β_U × [1 + (1-T) × D/E]
    有杠杆的Beta是无杠杆Beta的放大版

    参数:
        unlevered_cost: 无杠杆资本成本（r_U），即全股权融资的资本成本
        cost_of_debt: 债务成本（r_D）
        debt_equity_ratio: 债务股权比（D/E），也称杠杆比率
        tax_rate: 公司所得税率（T）

    返回:
        有杠杆股权成本（r_E）

    示例:
        无杠杆成本10%，债务成本5%，D/E=0.5，税率25%
        >>> levered_cost_of_equity(0.10, 0.05, 0.5, 0.25)
        0.11875  # r_E = 10% + (10%-5%) × 0.5 × 0.75 = 11.875%

    应用场景:
        - 比较不同资本结构下的股权成本
        - 为可比公司法估值调整Beta
        - 评估杠杆收购（LBO）的可行性
    """
    # TODO: 计算有杠杆股权成本
    # 提示：r_E = r_U + (r_U - r_D) × (D/E) × (1-T)
    pass


def firm_value_with_tax_shield(
    unlevered_value: float,
    debt_value: float,
    tax_rate: float
) -> float:
    """
    有税情况下的企业价值（MM定理的税收修正）。

    【公式推导】
    无税MM定理：V_L = V_U

    有税时，债务利息可在税前扣除，产生税盾（Tax Shield）：
    每年税盾 = 利息支付 × 税率 = r_D × D × T

    假设永续债务，税盾的现值：
    PV(税盾) = (r_D × D × T) / r_D = T × D

    因此：V_L = V_U + T × D

    【含义与局限】
    - 根据此公式，企业应100%债务融资以最大化价值
    - 这与现实不符，因为忽略了：
      1. 财务困境成本
      2. 代理成本
      3. 债务能力限制
      4. 个人所得税
    - 权衡理论平衡了税盾收益与困境成本

    参数:
        unlevered_value: 无杠杆企业价值（V_U），即全股权融资时的企业价值
        debt_value: 债务价值（D），假设为永续债务
        tax_rate: 公司所得税率（T）

    返回:
        有杠杆企业价值（V_L）

    示例:
        无杠杆价值1000亿，债务200亿，税率25%
        >>> firm_value_with_tax_shield(1000, 200, 0.25)
        1050  # V_L = 1000 + 0.25 × 200 = 1050亿

    推论:
        - 股权价值 E = V_L - D = V_U + T×D - D = V_U - D×(1-T)
        - 债务每增加1元，企业价值增加T元
    """
    # TODO: 计算企业价值
    # 提示：V_L = V_U + T × D
    pass


def tax_shield_value(debt: float, tax_rate: float) -> float:
    """
    计算税盾价值（假设永续债务）。

    【税盾效应详解】
    债务利息是税前费用，减少了应税所得：

    无债务时税后利润 = EBIT × (1-T)
    有债务时税后利润 = (EBIT - 利息) × (1-T) = EBIT×(1-T) - 利息×(1-T)

    但总的现金流给投资者（股东+债权人）：
    = EBIT×(1-T) - 利息×(1-T) + 利息
    = EBIT×(1-T) + 利息×T

    比无债务多出 利息×T = r_D×D×T（每年的税盾）

    永续税盾的现值：PV = (r_D×D×T) / r_D = T×D

    【注意事项】
    实际中税盾可能不确定：
    - 公司可能亏损，无法使用税盾
    - 税法可能变化
    - 债务可能违约
    因此，有时用更高的折现率

    参数:
        debt: 债务金额（D）
        tax_rate: 公司所得税率（T）

    返回:
        税盾现值

    示例:
        债务500亿，税率30%
        >>> tax_shield_value(500, 0.30)
        150  # 税盾价值 = 0.30 × 500 = 150亿
    """
    # TODO: 计算税盾
    # 提示：Tax Shield = T × D
    pass


def debt_equity_ratio_from_wacc(
    wacc: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float
) -> float:
    """
    从已知WACC反推债务股权比。

    【公式推导】
    从WACC公式出发：
    WACC = (E/V) × r_E + (D/V) × r_D × (1-T)

    令 w = D/V（债务比率），则 E/V = 1-w：
    WACC = (1-w) × r_E + w × r_D × (1-T)
    WACC = r_E - w × r_E + w × r_D × (1-T)
    WACC = r_E - w × [r_E - r_D × (1-T)]

    解出 w：
    w = (r_E - WACC) / [r_E - r_D × (1-T)]

    债务股权比：
    D/E = w / (1-w) = (r_E - WACC) / (WACC - r_D × (1-T))

    【应用场景】
    - 目标WACC下的资本结构规划
    - 竞争对手分析（从估算的WACC推断资本结构）
    - 资本结构优化

    参数:
        wacc: 目标或已知的WACC
        cost_of_equity: 股权成本（r_E）
        cost_of_debt: 债务成本（r_D）
        tax_rate: 公司所得税率（T）

    返回:
        债务股权比（D/E）

    示例:
        WACC=10%，股权成本12%，债务成本6%，税率25%
        >>> debt_equity_ratio_from_wacc(0.10, 0.12, 0.06, 0.25)
        0.364  # D/E ≈ 0.364

    注意:
        - 如果计算结果为负，说明参数组合不合理
        - 假设股权成本固定（实际上会随杠杆变化）
    """
    # TODO: 计算D/E
    # 步骤1: 计算税后债务成本 r_D_aftertax = r_D × (1-T)
    # 步骤2: 计算债务比率 w = (r_E - WACC) / (r_E - r_D_aftertax)
    # 步骤3: D/E = w / (1-w)
    pass


def optimal_debt_ratio_tradeoff(
    tax_rate: float,
    bankruptcy_cost_rate: float,
    default_probability_func: callable
) -> float:
    """
    权衡理论下的最优债务比率。

    【权衡理论模型】
    企业价值 = V_U + PV(税盾) - PV(财务困境成本)
    V(D) = V_U + T×D - p(D)×BC

    其中：
    - T×D：税盾价值
    - p(D)：违约概率，随债务增加而上升
    - BC：破产成本（通常为资产的一定比例）

    最优条件（边际分析）：
    dV/dD = T - BC × dp/dD = 0
    即：边际税盾收益 = 边际财务困境成本

    【实践考量】
    最优债务比率取决于：
    - 税率：税率越高，债务越有吸引力
    - 资产有形性：有形资产多，破产成本低
    - 盈利稳定性：稳定的公司可承担更多债务
    - 行业特征：成长性行业通常债务较少

    参数:
        tax_rate: 公司所得税率（T）
        bankruptcy_cost_rate: 破产成本占资产比例（如0.20表示20%）
        default_probability_func: 违约概率函数，输入债务比率，输出违约概率
                                  例如：lambda d: 0.5 * d**2

    返回:
        最优债务比率（D/V）

    示例:
        税率25%，破产成本20%，违约概率 = 0.5 × (D/V)²
        >>> prob_func = lambda d: 0.5 * d**2
        >>> optimal_debt_ratio_tradeoff(0.25, 0.20, prob_func)
        0.56  # 最优债务比率约56%

    算法提示:
        可使用数值优化方法（如网格搜索或scipy.optimize）
        找到使企业价值最大化的债务比率
    """
    # TODO: 计算最优债务比率
    # 方法1: 网格搜索
    # for d in np.linspace(0, 1, 100):
    #     value = tax_shield(d) - expected_bankruptcy_cost(d)
    #     找到value最大的d
    # 方法2: 解一阶条件 T = BC × dp/dD
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
