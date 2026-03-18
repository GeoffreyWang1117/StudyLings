# EXERCISE: capital_flows1
# DIFFICULTY: ★★★★☆
# TOPIC: 国际资本流动
#
# 说明：
# 国际资本流动是全球化金融体系的核心特征，
# 它连接了不同国家的储蓄者和投资者。
#
# 【资本流动的类型】
#
# 1. 外国直接投资（FDI）
#    - 定义：获得企业控制权的投资（通常≥10%股权）
#    - 特点：长期、稳定、伴随技术和管理转移
#    - 形式：绿地投资、跨国并购、利润再投资
#    - 例子：特斯拉在上海建厂
#
# 2. 证券投资（Portfolio Investment）
#    - 定义：股票和债券投资（<10%股权）
#    - 特点：流动性高、波动性大
#    - 形式：购买外国股票、政府债券、公司债
#    - 例子：外资通过沪港通买入A股
#
# 3. 其他投资
#    - 银行贷款和存款
#    - 贸易信贷
#    - 货币和存款
#
# 4. 储备资产
#    - 央行持有的外汇储备变动
#
# 【资本流动的决定因素】
#
# 1. 利率差（Interest Rate Differential）
#    资本从低利率国流向高利率国
#    受利率平价约束
#
# 2. 风险溢价（Risk Premium）
#    新兴市场需要更高收益补偿风险
#    包括：违约风险、政治风险、汇率风险
#
# 3. 增长预期
#    高增长国家吸引更多资本
#    "追逐收益"行为
#
# 4. 制度质量
#    产权保护、法治、透明度
#    影响长期投资决策
#
# 【资本账户开放的利弊分析】
#
# 潜在收益：
# - 资源配置效率：资本流向回报最高处
# - 风险分散：国际投资组合降低风险
# - 技术和管理转移（FDI）
# - 金融发展：竞争促进效率
#
# 潜在风险：
# - 资本外逃和突然停止
# - 货币危机
# - 金融传染
# - 丧失货币政策自主权
#
# 【突然停止（Sudden Stop）】
#
# 资本流入突然逆转的现象：
# - 触发因素：外部冲击、信心丧失、传染
# - 后果：汇率暴跌、经济衰退、金融危机
# - 例子：1997年亚洲金融危机、2008年新兴市场
#
# 脆弱性指标：
# - 经常账户赤字
# - 短期外债
# - 储备不足
# - 货币错配
#
# 【套息交易（Carry Trade）】
#
# 借低利率货币，投资高利率货币：
# 收益 = (i_高 - i_低) + 汇率变化
#
# 风险：
# - 汇率逆转时亏损放大
# - 流动性风险
# - 2008年日元套息交易平仓引发市场动荡
#
# 任务：
# 1. 理解资本流动的决定因素
# 2. 分析资本账户开放的效应
# 3. 计算FDI和组合投资决策
# 4. 评估外债可持续性
#
# HINT1: 利率平价条件驱动资本流动
# HINT2: 风险溢价反映国家风险
# HINT3: 突然停止可能引发危机

import numpy as np


def interest_parity_capital_flow(
    interest_home: float,
    interest_foreign: float,
    expected_depreciation: float,
    risk_premium: float,
    capital_mobility: float
) -> float:
    """
    计算利率平价驱动的资本流动。

    资本流动由跨国收益差驱动：

    无抛补利率平价条件（UIP）：
    i = i* + E[Δe] + ρ

    其中：
    - i: 国内利率
    - i*: 国外利率
    - E[Δe]: 预期贬值率
    - ρ: 风险溢价

    偏离UIP时产生资本流动：
    KF = κ × (i - i* - E[Δe] - ρ)

    其中κ是资本流动性参数

    含义：
    - 国内利率高于均衡水平 → 资本流入
    - 国内利率低于均衡水平 → 资本流出

    参数:
        interest_home: 国内利率
                       例如：i = 0.05（5%）
        interest_foreign: 国外（世界）利率
                          例如：i* = 0.02（2%）
        expected_depreciation: 预期本币贬值率
                               例如：E[Δe] = 0.02（预期贬值2%）
        risk_premium: 风险溢价（本国相对外国的额外风险补偿）
                      例如：ρ = 0.01（1%）
        capital_mobility: 资本流动性参数κ
                          例如：κ = 1000（高流动性）

    返回:
        资本流入量（正为流入，负为流出）

    示例:
        国内利率5%，国外2%，预期贬值2%，风险溢价1%，流动性1000
        >>> interest_parity_capital_flow(0.05, 0.02, 0.02, 0.01, 1000)
        0.0  # 均衡：5% = 2% + 2% + 1%，无资本流动

        国内利率6%（其他同上）
        >>> interest_parity_capital_flow(0.06, 0.02, 0.02, 0.01, 1000)
        10.0  # 资本流入：1000 × (6% - 2% - 2% - 1%) = 10

    TODO提示：
    - KF = κ × (i - i* - E[Δe] - ρ)
    """
    # TODO: 计算资本流动
    # 提示：KF = capital_mobility × (interest_home - interest_foreign - expected_depreciation - risk_premium)
    pass


def fdi_decision(
    host_return: float,
    home_return: float,
    setup_cost: float,
    years: int,
    discount_rate: float
) -> bool:
    """
    FDI投资决策（基于NPV）。

    外国直接投资决策考虑长期收益和初始成本。

    净现值（NPV）方法：
    NPV = -C₀ + Σ (R_host - R_home) / (1+r)^t

    其中：
    - C₀: 初始设立成本
    - R_host: 在东道国的年回报
    - R_home: 在母国的年回报（机会成本）
    - r: 折现率

    决策规则：NPV > 0 则投资

    考虑因素（除财务外）：
    - 市场准入
    - 技术保护
    - 政治风险
    - 税收优惠

    参数:
        host_return: 东道国年回报（如利润）
                     例如：150万美元/年
        home_return: 母国年回报（机会成本）
                     例如：100万美元/年
        setup_cost: FDI设立成本
                    例如：500万美元
        years: 投资年限
               例如：10年
        discount_rate: 折现率
                       例如：0.08（8%）

    返回:
        是否进行FDI投资（True/False）

    示例:
        东道国回报150万，母国回报100万，设立成本500万，10年，折现率8%
        >>> fdi_decision(150, 100, 500, 10, 0.08)
        False  # NPV = -500 + 50 × 年金因子(8%,10年) ≈ -500 + 335 < 0

    TODO提示：
    - 计算年度超额回报：host_return - home_return
    - 计算年金现值：Σ 超额回报 / (1+r)^t
    - NPV = -setup_cost + 年金现值
    - 返回 NPV > 0
    """
    # TODO: FDI决策
    # 提示：
    # annual_excess = host_return - home_return
    # pv = sum(annual_excess / (1 + discount_rate)**t for t in range(1, years+1))
    # npv = -setup_cost + pv
    # return npv > 0
    pass


def portfolio_allocation(
    expected_returns: np.ndarray,
    covariance_matrix: np.ndarray,
    risk_aversion: float
) -> np.ndarray:
    """
    国际投资组合最优配置（均值-方差优化）。

    基于马科维茨投资组合理论：
    max E[r_p] - (γ/2) × Var[r_p]

    其中：
    - E[r_p] = w'μ（组合预期收益）
    - Var[r_p] = w'Σw（组合方差）
    - γ: 风险厌恶系数

    最优权重（无约束）：
    w* = (1/γ) × Σ^(-1) × μ

    国际分散化的好处：
    - 不同国家股市相关性 < 1
    - 分散化降低组合风险
    - 新兴市场提供超额收益机会

    参数:
        expected_returns: 各国市场预期收益向量μ
                          例如：[0.08, 0.10, 0.12]（美、欧、亚）
        covariance_matrix: 收益协方差矩阵Σ
                           例如：3×3矩阵
        risk_aversion: 风险厌恶系数γ
                       例如：γ = 2

    返回:
        最优投资权重向量

    示例:
        三个市场，预期收益8%/10%/12%
        >>> expected_returns = np.array([0.08, 0.10, 0.12])
        >>> cov = np.array([[0.04, 0.01, 0.01],
                            [0.01, 0.05, 0.02],
                            [0.01, 0.02, 0.06]])
        >>> portfolio_allocation(expected_returns, cov, 2)
        array([0.3, 0.4, 0.3])  # 示意

    TODO提示：
    - w = (1/γ) × Σ^(-1) × μ
    - 使用 np.linalg.inv() 求逆矩阵
    """
    # TODO: 计算最优投资组合
    # 提示：
    # w = (1/risk_aversion) × np.linalg.inv(covariance_matrix) @ expected_returns
    pass


def home_bias_measure(
    domestic_weight: float,
    domestic_market_share: float
) -> float:
    """
    衡量本土偏好程度。

    本土偏好（Home Bias）是指投资者在国内资产上的配置
    超过了市场价值权重所隐含的比例。

    本土偏好指数：
    HB = (w_domestic - share_domestic) / (1 - share_domestic)

    其中：
    - w_domestic: 实际国内资产权重
    - share_domestic: 国内市场占全球市场份额

    解读：
    - HB = 0: 无本土偏好（与市场权重一致）
    - HB = 1: 完全本土偏好（只投国内）
    - HB < 0: 反向偏好（低配国内）

    本土偏好的原因：
    - 信息不对称
    - 交易成本
    - 汇率风险
    - 监管限制
    - 行为偏差

    实证发现：
    - 美国投资者约80%配置在国内（市场份额约50%）
    - 日本投资者本土偏好更严重
    - 近年来有下降趋势

    参数:
        domestic_weight: 投资者国内资产实际权重
                         例如：w = 0.80（80%）
        domestic_market_share: 国内市场占全球份额
                               例如：share = 0.50（50%）

    返回:
        本土偏好指数（0到1之间）

    示例:
        国内资产权重80%，国内市场份额50%
        >>> home_bias_measure(0.80, 0.50)
        0.60  # HB = (0.8 - 0.5) / (1 - 0.5) = 0.6

    TODO提示：
    - HB = (w_domestic - share) / (1 - share)
    """
    # TODO: 计算本土偏好指数
    # 提示：HB = (domestic_weight - domestic_market_share) / (1 - domestic_market_share)
    pass


def sudden_stop_impact(
    capital_inflow_gdp: float,
    reversal: float,
    output_elasticity: float
) -> dict:
    """
    评估资本流动突然停止的影响。

    突然停止（Sudden Stop）是资本流入急剧逆转的现象。

    冲击传导机制：
    1. 资本流入突然停止或逆转
    2. 汇率贬值压力
    3. 国内信贷紧缩
    4. 需求收缩
    5. 产出下降

    经常账户必须调整：
    CA = S - I = -资本流入
    资本流入减少 → 经常账户必须改善

    调整方式：
    - 减少进口（进口压缩）
    - 汇率贬值促进出口
    - 投资下降
    - 消费下降

    产出损失估计：
    ΔY/Y ≈ elasticity × 资本流入逆转幅度

    参数:
        capital_inflow_gdp: 危机前资本流入/GDP
                            例如：0.08（占GDP的8%）
        reversal: 资本流入逆转幅度（0到1）
                  例如：1.0表示完全停止
                  例如：1.5表示从流入变为流出
        output_elasticity: 产出对资本流动的弹性
                           例如：0.5表示资本减少1%GDP，产出下降0.5%

    返回:
        字典包含：
        - 'output_loss': 产出损失（占GDP比例）
        - 'current_account_adjustment': 经常账户调整幅度

    示例:
        资本流入8%GDP，完全逆转，产出弹性0.5
        >>> sudden_stop_impact(0.08, 1.0, 0.5)
        {'output_loss': -0.04, 'current_account_adjustment': 0.08}

    TODO提示：
    - output_loss = -output_elasticity × capital_inflow_gdp × reversal
    - current_account_adjustment = capital_inflow_gdp × reversal
    """
    # TODO: 计算突然停止影响
    # 提示：
    # ca_adjustment = capital_inflow_gdp × reversal
    # output_loss = -output_elasticity × ca_adjustment
    pass


def external_debt_sustainability(
    debt_gdp: float,
    interest_rate: float,
    growth_rate: float,
    primary_balance_gdp: float
) -> float:
    """
    外债可持续性分析。

    债务动态方程：
    Δd = (r - g)d - pb

    其中：
    - d: 债务/GDP比率
    - r: 实际利率
    - g: 实际GDP增长率
    - pb: 基本余额/GDP（基本余额 = 经常账户 + 利息支出）

    稳态条件（Δd = 0）：
    d* = pb / (r - g)

    可持续性条件：
    - 如果 r > g：需要基本盈余维持债务稳定
    - 如果 r < g：即使基本赤字也可能可持续

    风险因素：
    - 利率上升
    - 增长下降
    - 汇率贬值（外币债务）

    参数:
        debt_gdp: 当前外债/GDP比率
                  例如：d = 0.50（50%）
        interest_rate: 外债实际利率
                       例如：r = 0.05（5%）
        growth_rate: 实际GDP增长率
                     例如：g = 0.03（3%）
        primary_balance_gdp: 基本余额/GDP
                             例如：pb = 0.01（1%盈余）

    返回:
        债务/GDP比率的变化

    示例:
        债务50%GDP，利率5%，增长3%，基本盈余1%
        >>> external_debt_sustainability(0.50, 0.05, 0.03, 0.01)
        0.0  # Δd = (5%-3%)×50% - 1% = 1% - 1% = 0

    TODO提示：
    - Δd = (r - g) × d - pb
    """
    # TODO: 计算债务可持续性
    # 提示：delta_d = (interest_rate - growth_rate) × debt_gdp - primary_balance_gdp
    pass


def capital_control_effectiveness(
    target_flow_reduction: float,
    actual_flow_reduction: float,
    evasion_rate: float
) -> float:
    """
    评估资本管制的有效性。

    资本管制是限制跨境资本流动的政策工具。

    有效性指标：
    effectiveness = actual_reduction / target_reduction × (1 - evasion)

    管制类型：
    1. 价格型：对资本流动征税（托宾税）
    2. 数量型：审批、配额、禁止
    3. 宏观审慎：针对特定风险

    管制效果的影响因素：
    - 金融市场发达程度（越发达越易规避）
    - 执法能力
    - 管制范围
    - 激励强度

    规避渠道：
    - 贸易伪造
    - 地下钱庄
    - 加密货币
    - 跨国公司内部转移

    参数:
        target_flow_reduction: 目标资本流动减少量
                               例如：100亿美元
        actual_flow_reduction: 实际资本流动减少量
                               例如：60亿美元
        evasion_rate: 估计的规避率
                      例如：0.20（20%的管制被规避）

    返回:
        有效性指数（0到1之间，1为完全有效）

    示例:
        目标减少100亿，实际减少60亿，规避率20%
        >>> capital_control_effectiveness(100, 60, 0.20)
        0.48  # 0.6 × (1 - 0.2) = 0.48

    TODO提示：
    - effectiveness = (actual / target) × (1 - evasion)
    """
    # TODO: 计算资本管制有效性
    # 提示：effectiveness = (actual_flow_reduction / target_flow_reduction) × (1 - evasion_rate)
    pass


def carry_trade_return(
    interest_home: float,
    interest_foreign: float,
    exchange_rate_change: float,
    leverage: float = 1.0
) -> float:
    """
    计算套息交易收益率。

    套息交易（Carry Trade）：
    借入低利率货币，投资高利率货币。

    基本收益计算：
    总收益 = 利差收益 + 汇率变动收益
    R = (i_high - i_low) + Δe

    杠杆效应：
    R_杠杆 = leverage × R

    风险：
    - 汇率风险：高利率货币可能贬值
    - 流动性风险：危机时难以平仓
    - UIP谜题：高利率货币往往不贬值反而升值

    历史案例：
    - 日元套息交易：借日元，投澳元/纽元
    - 2008年：日元大幅升值，套息交易巨亏

    参数:
        interest_home: 高利率货币利率
                       例如：i_高 = 0.08（8%，如澳元）
        interest_foreign: 低利率货币利率
                          例如：i_低 = 0.01（1%，如日元）
        exchange_rate_change: 高利率货币汇率变化
                              正值为升值，负值为贬值
                              例如：0.02表示升值2%
        leverage: 杠杆倍数
                  例如：5倍杠杆

    返回:
        套息交易收益率

    示例:
        高利率8%，低利率1%，高利率货币升值2%，无杠杆
        >>> carry_trade_return(0.08, 0.01, 0.02, 1.0)
        0.09  # 7%利差 + 2%汇率收益 = 9%

        5倍杠杆
        >>> carry_trade_return(0.08, 0.01, 0.02, 5.0)
        0.45  # 5 × 9% = 45%

        高利率货币贬值10%
        >>> carry_trade_return(0.08, 0.01, -0.10, 5.0)
        -0.15  # 5 × (7% - 10%) = -15%

    TODO提示：
    - base_return = (interest_home - interest_foreign) + exchange_rate_change
    - total_return = leverage × base_return
    """
    # TODO: 计算套息交易收益
    # 提示：
    # base_return = (interest_home - interest_foreign) + exchange_rate_change
    # return leverage × base_return
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
