# EXERCISE: currency_crisis1
# DIFFICULTY: ★★★★★
# TOPIC: 货币危机模型（三代模型）
#
# 说明：
# 货币危机（Currency Crisis）是指固定汇率制度的崩溃，
# 通常伴随着本币大幅贬值和外汇储备急剧下降。
#
# 【历史上的重大货币危机】
# - 1992年欧洲汇率机制危机（英镑、里拉）
# - 1994年墨西哥比索危机
# - 1997年亚洲金融危机（泰铢、韩元、印尼盾）
# - 1998年俄罗斯卢布危机
# - 2001年阿根廷比索危机
# - 2018年土耳其里拉危机
#
# 【三代货币危机模型】
#
# ═══════════════════════════════════════════════════════════
# 第一代模型（Krugman, 1979; Flood & Garber, 1984）
# ═══════════════════════════════════════════════════════════
#
# 核心思想：财政赤字货币化导致储备耗尽
#
# 基本设定：
# - 政府持续财政赤字，通过印钞弥补
# - 央行承诺维护固定汇率
# - 矛盾：货币扩张与固定汇率不可兼得
#
# 模型方程：
# 货币供给：M = D + R（国内信贷 + 外汇储备）
# 货币需求：M = P × L(Y, i) = P × L（固定汇率下P固定）
# 信贷增长：dD/dt = μ（持续扩张）
# 储备变化：dR/dt = -μ（储备被动减少）
#
# 影子汇率（Shadow Exchange Rate）：
# 无干预时的均衡汇率，由国内信贷决定：
# s̃ = D / L(Y, i*)
#
# 投机攻击时点：
# 当影子汇率超过固定汇率时，理性投机者发动攻击
# 攻击时点 T：s̃(T) = s̄（固定汇率）
#
# 关键结论：
# 1. 危机时点可以预测（取决于储备消耗速度）
# 2. 攻击发生在储备耗尽之前（投机者抢先行动）
# 3. 投机者获利，央行损失储备
#
# ═══════════════════════════════════════════════════════════
# 第二代模型（Obstfeld, 1994, 1996）
# ═══════════════════════════════════════════════════════════
#
# 核心思想：自我实现的预期与多重均衡
#
# 关键创新：
# - 政府不是被动的，而是权衡成本收益
# - 维护固定汇率有成本（高利率、失业）
# - 放弃固定汇率也有成本（信誉损失）
#
# 政府损失函数：
# L = α·u² + β·π² + γ·(放弃汇率的成本)
#
# 多重均衡：
# - 好均衡：无人预期贬值 → 无攻击 → 汇率稳定
# - 坏均衡：预期贬值 → 利率上升 → 政府放弃固定汇率
#
# 三个区域：
# 1. 基本面很好：无论预期如何，汇率稳定
# 2. 基本面很差：无论预期如何，危机发生
# 3. 中间区域：预期自我实现，可能稳定也可能危机
#
# 政策含义：
# - 危机可能"无端"发生（阳光黑子均衡）
# - 市场情绪和信心至关重要
# - 央行需要"足够"的储备来改变预期
#
# ═══════════════════════════════════════════════════════════
# 第三代模型（1997年后）
# ═══════════════════════════════════════════════════════════
#
# 核心思想：金融脆弱性与双重危机
#
# 背景：亚洲危机的新特征
# - 财政状况良好
# - 银行部门脆弱
# - 企业外币债务高
#
# 资产负债表效应（Krugman, 1999）：
# - 企业借外币债务，收入为本币
# - 本币贬值 → 债务负担加重 → 企业破产
# - 企业破产 → 经济收缩 → 进一步贬值
#
# 银行危机与货币危机的联系：
# - 银行资产质量恶化 → 存款外流 → 汇率压力
# - 汇率贬值 → 银行外币负债增加 → 银行危机加深
# - 双重危机相互强化
#
# 道德风险与过度借贷：
# - 政府隐性担保 → 银行过度冒险
# - 资本流入推高资产价格 → 泡沫
# - 泡沫破裂 → 危机
#
# 任务：
# 1. 理解第一代模型的储备动态和攻击时点
# 2. 分析第二代模型的多重均衡
# 3. 计算第三代模型的资产负债表效应
# 4. 构建危机预警指标
#
# HINT1: 影子汇率是无央行干预时的均衡汇率
# HINT2: 攻击发生在影子汇率等于固定汇率时
# HINT3: 第二代模型中预期可以自我实现

import numpy as np


def shadow_exchange_rate(
    money_supply: float,
    domestic_credit: float,
    money_demand_param: float
) -> float:
    """
    计算影子汇率（第一代模型）。

    影子汇率是假设央行不干预外汇市场时的均衡汇率。
    它反映了国内货币状况隐含的汇率水平。

    理论推导：
    在固定汇率下：
    M = D + R（货币供给 = 国内信贷 + 外汇储备）
    M/P = L(Y, i*)（实际货币需求）

    若央行放弃干预（R=0）：
    M = D（货币供给仅由国内信贷决定）
    均衡要求：D/s̃ = L（实际货币需求）

    解得影子汇率：
    s̃ = D / L

    经济学含义：
    - s̃ < s̄：国内信贷不足以支撑固定汇率，汇率高估
    - s̃ = s̄：均衡点，攻击临界
    - s̃ > s̄：国内信贷过多，固定汇率不可持续

    参数:
        money_supply: 当前货币供给M
                      例如：M = 100（亿美元）
        domestic_credit: 国内信贷D
                         例如：D = 80（亿美元）
                         随时间增长（财政赤字货币化）
        money_demand_param: 货币需求参数L
                            例如：L = 50（实际货币需求）

    返回:
        影子汇率s̃

    示例:
        国内信贷80，货币需求参数50
        >>> shadow_exchange_rate(100, 80, 50)
        1.6  # 影子汇率为1.6

    注意:
        当影子汇率超过固定汇率时，投机攻击将发生

    TODO提示：
    - 影子汇率 = 国内信贷 / 货币需求参数
    - s̃ = D / L
    """
    # TODO: 计算影子汇率
    # 提示：s̃ = D / L(Y, i*)
    # 简化为：s̃ = domestic_credit / money_demand_param
    pass


def reserve_dynamics(
    reserves: float,
    domestic_credit: float,
    credit_growth: float,
    fixed_rate: float,
    money_demand: float
) -> float:
    """
    计算储备变化率（第一代模型）。

    在固定汇率制度下，货币供给由货币需求决定：
    M = P × L = s̄ × L（固定汇率下）

    货币供给恒等式：
    M = D + R

    因此：
    s̄ × L = D + R
    R = s̄ × L - D

    对时间求导：
    dR/dt = -dD/dt = -μ

    含义：
    - 国内信贷每增加1单位，储备减少1单位
    - 央行通过卖出外汇吸收多余货币
    - 储备持续下降直至耗尽

    参数:
        reserves: 当前外汇储备R
                  例如：R = 50（亿美元）
        domestic_credit: 当前国内信贷D
                         例如：D = 50（亿美元）
        credit_growth: 国内信贷增长率μ（绝对值）
                       例如：μ = 5（每期增加5亿美元）
        fixed_rate: 固定汇率s̄
                    例如：s̄ = 2.0
        money_demand: 货币需求L
                      例如：L = 50

    返回:
        储备变化率dR/dt（负值表示减少）

    示例:
        信贷增长5亿/期
        >>> reserve_dynamics(50, 50, 5, 2.0, 50)
        -5.0  # 储备每期减少5亿

    TODO提示：
    - 储备变化率等于信贷增长率的负值
    - dR/dt = -credit_growth
    """
    # TODO: 计算储备动态
    # 提示：dR/dt = -dD/dt = -credit_growth
    # 在固定汇率下，信贷增加多少，储备就减少多少
    pass


def attack_time_first_gen(
    initial_reserves: float,
    credit_growth: float,
    money_demand: float,
    fixed_rate: float
) -> float:
    """
    计算第一代模型的投机攻击时点。

    攻击时点的确定（Flood-Garber条件）：

    攻击前一刻：
    - 储备 R(T⁻) > 0
    - 影子汇率 s̃(T⁻) < s̄

    攻击后一刻：
    - 储备 R(T⁺) = 0
    - 实际汇率 = 影子汇率 = s̄

    投机者在攻击时买走所有剩余储备。

    计算攻击时点：
    初始状态：R₀ + D₀ = s̄ × L
    信贷增长：D(t) = D₀ + μt

    攻击时刻 T：
    影子汇率 = 固定汇率
    D(T) / L = s̄
    D₀ + μT = s̄ × L
    T = (s̄ × L - D₀) / μ = R₀ / μ

    参数:
        initial_reserves: 初始外汇储备R₀
                          例如：R₀ = 100（亿美元）
        credit_growth: 国内信贷增长率μ
                       例如：μ = 10（每年增加10亿）
        money_demand: 货币需求L
        fixed_rate: 固定汇率s̄

    返回:
        攻击时点T（期数）

    示例:
        初始储备100亿，信贷每年增长10亿
        >>> attack_time_first_gen(100, 10, 50, 2.0)
        10.0  # 10年后发生攻击

    重要结论：
    - 攻击时点可预测
    - 投机者不需等到储备耗尽
    - 预期到危机会加速危机

    TODO提示：
    - T = R₀ / μ
    - 初始储备除以信贷增长率
    """
    # TODO: 计算攻击时点
    # 提示：T = R₀ / credit_growth
    pass


def speculative_attack_reserve_loss(
    money_demand: float,
    domestic_credit_at_attack: float
) -> float:
    """
    计算投机攻击时的储备损失。

    在攻击时刻，投机者用本币购买外汇储备。

    攻击前：
    M = D(T) + R(T)

    攻击后：
    M' = D(T)（储备归零）

    储备损失 = 攻击时的储备存量
    ΔR = R(T) = M - D(T) = s̄ × L - D(T)

    简化计算：
    ΔR = money_demand × s̄ - domestic_credit_at_attack

    但在攻击临界点，s̃ = s̄，所以：
    ΔR = L × s̃ - D = L × (D/L) - D...

    更简单的理解：
    攻击时剩余储备 = 货币需求 - 当时的国内信贷（假设已标准化）

    参数:
        money_demand: 货币需求（决定攻击时的货币供给）
                      例如：L = 50
        domestic_credit_at_attack: 攻击时刻的国内信贷D(T)
                                   例如：D(T) = 45

    返回:
        储备损失（正值）

    示例:
        货币需求50，攻击时信贷45
        >>> speculative_attack_reserve_loss(50, 45)
        5.0  # 损失5亿储备

    TODO提示：
    - 简化假设下，储备损失 = L - D(T)（标准化后）
    - 或者直接理解为攻击时的剩余储备
    """
    # TODO: 计算储备损失
    # 提示：储备损失 = money_demand - domestic_credit_at_attack
    # （这是一个简化版本，假设固定汇率=1）
    pass


def government_cost_benefit(
    unemployment: float,
    inflation: float,
    reserve_cost: float,
    weight_unemployment: float = 1.0,
    weight_inflation: float = 0.5
) -> float:
    """
    第二代模型：政府损失函数。

    在第二代模型中，政府是理性决策者，
    需要权衡维护固定汇率的成本与收益。

    政府损失函数：
    L = α × u² + β × π² + C(保卫汇率)

    维护固定汇率的成本：
    - 高利率抑制投资和消费
    - 失业增加
    - 动用储备

    放弃固定汇率的成本：
    - 通胀上升
    - 信誉损失
    - 外债负担加重

    决策规则：
    如果 L(维护) < L(放弃)，则维护汇率
    如果 L(维护) > L(放弃)，则放弃汇率

    参数:
        unemployment: 失业率（如0.08表示8%）
                      例如：u = 0.08
        inflation: 通胀率（如0.05表示5%）
                   例如：π = 0.05
        reserve_cost: 保卫汇率消耗的储备成本
                      例如：C = 0.1（占GDP的10%）
        weight_unemployment: 失业权重α，默认1.0
        weight_inflation: 通胀权重β，默认0.5

    返回:
        政府总损失

    示例:
        失业率8%，通胀5%，储备成本10%
        >>> government_cost_benefit(0.08, 0.05, 0.1)
        0.0089  # 政府总损失

        计算：1.0×0.08² + 0.5×0.05² + 0.1 = 0.0064 + 0.00125 + 0.1

    TODO提示：
    - 计算失业损失：α × u²
    - 计算通胀损失：β × π²
    - 加上储备成本
    - L = α × unemployment² + β × inflation² + reserve_cost
    """
    # TODO: 计算政府损失函数
    # 提示：L = α × u² + β × π² + C
    pass


def multiple_equilibria(
    fundamentals: float,
    expectations: float,
    threshold_low: float,
    threshold_high: float
) -> str:
    """
    第二代模型：判断多重均衡区域。

    第二代模型的核心洞见是存在三个区域：

    1. 基本面良好区（fundamentals < threshold_low）
       - 无论市场预期如何，汇率都稳定
       - 政府有足够实力应对攻击
       - 唯一均衡：稳定

    2. 基本面恶劣区（fundamentals > threshold_high）
       - 无论市场预期如何，危机都会发生
       - 政府无力维护汇率
       - 唯一均衡：危机

    3. 中间区域（threshold_low ≤ fundamentals ≤ threshold_high）
       - 两种均衡都可能
       - 如果预期稳定 → 稳定均衡
       - 如果预期贬值 → 危机均衡
       - 预期可以自我实现

    这解释了为什么危机有时"无端"发生：
    - 市场情绪转变
    - 投机者协调攻击
    - 传染效应（一国危机引发对邻国的担忧）

    参数:
        fundamentals: 基本面指标（如财政赤字/GDP）
                      例如：0.05表示5%的财政赤字
                      数值越高，基本面越差
        expectations: 贬值预期（0到1）
                      0表示完全相信固定汇率
                      1表示确信会贬值
        threshold_low: 安全区上限
                       例如：0.03（3%以下财政赤字是安全的）
        threshold_high: 危机区下限
                        例如：0.08（8%以上财政赤字必然危机）

    返回:
        "stable": 稳定均衡
        "crisis": 危机均衡
        "multiple": 多重均衡区域（取决于预期）

    示例:
        基本面良好
        >>> multiple_equilibria(0.02, 0.5, 0.03, 0.08)
        "stable"

        基本面恶劣
        >>> multiple_equilibria(0.10, 0.3, 0.03, 0.08)
        "crisis"

        中间区域
        >>> multiple_equilibria(0.05, 0.6, 0.03, 0.08)
        "multiple"  # 或根据预期判断

    TODO提示：
    - 如果 fundamentals < threshold_low，返回 "stable"
    - 如果 fundamentals > threshold_high，返回 "crisis"
    - 否则返回 "multiple"（或根据expectations判断）
    """
    # TODO: 判断多重均衡区域
    # 提示：
    # if fundamentals < threshold_low: return "stable"
    # elif fundamentals > threshold_high: return "crisis"
    # else: return "multiple"
    pass


def balance_sheet_effect(
    foreign_debt: float,
    depreciation: float,
    output_elasticity: float
) -> float:
    """
    第三代模型：资产负债表效应。

    这是1997年亚洲金融危机后发展的重要理论。

    机制说明：
    - 新兴市场企业常借外币债务（利率低）
    - 企业收入为本币
    - 货币错配（Currency Mismatch）

    贬值的影响：
    1. 外币债务本币价值上升
       ΔDebt = Debt × 贬值率
    2. 净资产减少
    3. 信用紧缩，投资下降
    4. 产出收缩

    恶性循环：
    贬值 → 企业资产负债恶化 → 投资下降 → 产出下降
    → 进一步贬值 → ...

    与传统观点的对比：
    - 传统：贬值有利于出口，促进增长
    - 第三代：贬值损害资产负债表，抑制增长
    - 净效果取决于两种力量的相对大小

    参数:
        foreign_debt: 外币债务（本币计价）
                      例如：1000（亿本币）
        depreciation: 贬值率（如0.3表示贬值30%）
                      例如：0.3
        output_elasticity: 产出对资产负债表的弹性
                           例如：0.5表示债务增加1%，产出下降0.5%

    返回:
        产出损失（占初始产出的比例，负值）

    示例:
        外债1000亿，贬值30%，产出弹性0.5
        >>> balance_sheet_effect(1000, 0.3, 0.5)
        -150.0  # 产出损失150亿

        计算：外债增加 = 1000 × 0.3 = 300
              产出损失 = 300 × 0.5 = 150

    TODO提示：
    - 债务增加 = foreign_debt × depreciation
    - 产出损失 = 债务增加 × output_elasticity
    - 返回负值表示损失
    """
    # TODO: 计算资产负债表效应
    # 提示：
    # 债务增加 = foreign_debt × depreciation
    # 产出损失 = 债务增加 × output_elasticity
    # 返回 -产出损失（负值）
    pass


def early_warning_indicator(
    reserve_coverage: float,
    current_account_gdp: float,
    credit_growth: float,
    real_appreciation: float
) -> float:
    """
    危机预警指标（综合评分）。

    危机预警系统旨在识别脆弱性，提前发出警告。

    常用预警指标：

    1. 储备覆盖率（Reserve Coverage）
       - 储备/月进口
       - 通常要求 > 3个月
       - 越低越危险

    2. 经常账户/GDP
       - 持续逆差是危险信号
       - 通常警戒线为 -5%
       - 越负越危险

    3. 信贷增长率
       - 快速信贷扩张预示泡沫
       - 通常警戒线为 20%/年
       - 越高越危险

    4. 实际汇率升值
       - 升值过多意味着竞争力下降
       - 通常警戒线为 20%
       - 升值越多越危险

    综合评分方法（简化）：
    对各指标标准化后加权平均

    参数:
        reserve_coverage: 储备覆盖率（月数）
                          例如：3.0表示可覆盖3个月进口
        current_account_gdp: 经常账户余额/GDP
                             例如：-0.05表示逆差占GDP的5%
        credit_growth: 年信贷增长率
                       例如：0.25表示25%增长
        real_appreciation: 实际汇率升值幅度（累计）
                           例如：0.15表示升值15%

    返回:
        危机概率（0到1之间）
        0表示安全，1表示极度危险

    示例:
        储备3个月，经常账户-5%，信贷增长25%，升值15%
        >>> early_warning_indicator(3.0, -0.05, 0.25, 0.15)
        0.55  # 中等风险

    评分逻辑（简化）：
    - 储备 < 3个月：加0.25分
    - 经常账户 < -5%：加0.25分
    - 信贷增长 > 20%：加0.25分
    - 升值 > 20%：加0.25分

    TODO提示：
    - 对每个指标设定阈值
    - 超过阈值则累加危机分数
    - 返回归一化的总分（0-1之间）
    """
    # TODO: 计算预警指标
    # 提示：
    # score = 0
    # if reserve_coverage < 3: score += 0.25
    # if current_account_gdp < -0.05: score += 0.25
    # if credit_growth > 0.20: score += 0.25
    # if real_appreciation > 0.20: score += 0.25
    # 可以使用更平滑的评分函数
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
