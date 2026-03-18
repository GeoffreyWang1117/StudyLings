# EXERCISE: social_insurance1
# DIFFICULTY: ★★★★☆
# TOPIC: 社会保险
#
# 说明：
# 社会保险是政府应对人生风险的制度安排，包括养老、失业、医疗、工伤等保险。
# 它既是风险共担机制，也涉及收入再分配。
#
# 【理论背景】
# 社会保险的经济学分析始于福利经济学和信息经济学。
# 核心问题：为什么需要政府强制参与？私人市场为何无法有效提供？
#
# 【为什么需要政府介入保险市场？】
#
# 1. 逆向选择（Adverse Selection）
#    - 高风险者比低风险者更可能购买保险
#    - 保险公司无法完美区分风险类型
#    - 按平均风险定价 → 低风险者退出 → 价格上升 → 更多人退出
#    - 极端情况下市场崩溃（Akerlof, 1970）
#
#    政府解决方案：强制参保
#    - 所有人必须参加，打破自选择
#    - 形成真正的风险池
#
# 2. 道德风险（Moral Hazard）
#    - 有保险后行为改变，增加风险发生概率或损失
#    - 例：有失业保险后求职努力下降
#    - 例：有医疗保险后过度就医
#
#    解决方案：部分保险（非全额赔付）
#    - 自付比例（Co-payment）
#    - 免赔额（Deductible）
#    - 有限期限
#
# 3. 信贷约束（Credit Constraints）
#    - 个人可能无法在需要时借贷
#    - 收入波动时无法跨期平滑消费
#    - 特别影响低收入群体
#
# 4. 行为偏差（Behavioral Biases）
#    - 过度贴现：低估未来需求
#    - 过度乐观：低估风险发生概率
#    - 拖延症：总想"明天开始存钱"
#
#    解决方案：强制性储蓄/参保
#    - 家长主义（Paternalism）的正当性
#    - 帮助个人克服自控问题
#
# 【主要社会保险项目】
#
# 1. 养老保险（Pension/Social Security）
#    两种模式：
#
#    a) 现收现付制（Pay-As-You-Go, PAYG）
#       - 当期工人缴费直接支付给当期退休者
#       - 代际转移
#       - 收益率 ≈ 人口增长率 + 工资增长率 (n + g)
#       - 问题：人口老龄化时不可持续
#
#    b) 基金积累制（Fully Funded）
#       - 个人账户积累，退休时领取
#       - 资本市场投资
#       - 收益率 = 资本回报率 (r)
#       - 问题：投资风险、转轨成本
#
#    Aaron条件：
#    当 n + g > r 时，PAYG更优
#    当 n + g < r 时，基金制更优
#
# 2. 失业保险（Unemployment Insurance）
#    - 失业期间提供收入替代
#    - 替代率（Replacement Rate）：保险金/原工资
#    - 核心权衡：保障 vs 激励
#
#    道德风险问题：
#    - 高替代率降低求职努力
#    - 可能延长失业期
#
#    最优设计：
#    - 初期较高替代率，逐步递减
#    - 鼓励尽快再就业
#
# 3. 医疗保险（Health Insurance）
#    - 疾病的不确定性和高成本
#    - 严重的逆向选择和道德风险
#    - 不同国家模式：
#      * 单一支付者（如英国NHS）
#      * 社会保险（如德国）
#      * 混合制度（如美国）
#
# 4. 工伤保险（Workers' Compensation）
#    - 工作相关伤害和职业病
#    - 雇主强制投保
#    - 无过错责任
#
# 【关键概念】
#
# 1. 替代率（Replacement Rate）
#    RR = 保险金 / 原收入
#    衡量保障水平
#
# 2. 缴费率（Contribution Rate）
#    τ = 缴费 / 工资
#    影响劳动成本和供给
#
# 3. 抚养比（Dependency Ratio）
#    DR = 受益者人数 / 缴费者人数
#    决定PAYG系统的可持续性
#
# 4. 精算公平（Actuarial Fairness）
#    期望缴费现值 = 期望收益现值
#    纯保险原则，无再分配
#
# 【设计权衡】
#
# 核心权衡：保障（Insurance）vs 激励（Incentives）
#
# 保障功能：
# - 消费平滑（Consumption Smoothing）
# - 风险共担（Risk Pooling）
# - 减轻不确定性带来的焦虑
#
# 激励扭曲：
# - 劳动供给减少
# - 储蓄减少
# - 求职努力减少
# - 退休年龄提前
#
# 最优保险水平：边际保障收益 = 边际激励成本
#
# 任务：
# 1. 理解社会保险的经济学原理
# 2. 分析养老保险的两种模式
# 3. 计算替代率和缴费率
# 4. 理解道德风险和逆向选择问题
#
# HINT1: 替代率越高，保障越好，但激励扭曲越大
# HINT2: 现收现付制的可持续性依赖于人口结构
# HINT3: 逆向选择需要强制参保来解决

import numpy as np


def replacement_rate(
    benefit: float,
    previous_wage: float
) -> float:
    """
    计算替代率。

    【定义】
    替代率是社会保险金与之前收入的比率，衡量保险的保障水平。

    【公式】
    RR = B / W

    其中：
    - B: 保险金（Benefits）
    - W: 之前的工资收入

    【不同保险的替代率】
    失业保险：
    - 欧洲国家：60-80%
    - 美国：40-50%
    - 中国：60-70%

    养老保险：
    - 发达国家：50-70%
    - 中国目标：55-60%

    【替代率的含义】
    - RR = 1 (100%): 完全替代，收入无变化
    - RR = 0.5 (50%): 收入减半
    - 更高替代率 → 更好保障，但更多激励扭曲

    【政策考量】
    1. 太低：保障不足，贫困风险
    2. 太高：工作激励受损
    3. 最优替代率取决于风险厌恶程度和激励弹性

    参数:
        benefit: 保险金金额
                例：每月领取3000元失业保险金
        previous_wage: 失业/退休前的工资
                      例：之前月工资5000元

    返回:
        替代率（通常在0到1之间，但可能超过1）

    示例:
        失业保险
        >>> replacement_rate(3000, 5000)
        0.6   # 替代率60%，收入降至之前的60%

        养老金
        >>> replacement_rate(4000, 6000)
        0.667  # 替代率约67%

        低保障情况
        >>> replacement_rate(1500, 5000)
        0.3   # 替代率仅30%，保障较低

    注意:
        替代率可能因收入水平而变化
        累进制度下，低收入者替代率更高
    """
    # TODO: 计算替代率
    # 提示：RR = benefit / previous_wage
    pass


def payg_pension_benefit(
    contribution_rate: float,
    wage: float,
    workers_per_retiree: float
) -> float:
    """
    计算现收现付制养老金收益。

    【现收现付制原理】
    当期工人的缴费直接支付给当期退休者。

    收入端：所有工人的缴费
    Total Contributions = τ × W × L
    其中 L = 工人数量

    支出端：所有退休者的养老金
    Total Benefits = B × R
    其中 R = 退休者数量

    预算平衡条件：
    τ × W × L = B × R

    解得每个退休者的养老金：
    B = τ × W × (L/R)

    【制度参数】
    - τ: 缴费率
    - W: 平均工资
    - L/R: 劳动者/退休者比率（抚养比的倒数）

    【隐含收益率】
    长期看，PAYG的收益率约等于：n + g
    其中 n = 人口增长率，g = 生产率增长率

    【可持续性问题】
    当人口老龄化（L/R下降）时：
    - 要么降低B（养老金）
    - 要么提高τ（缴费率）
    - 要么延迟退休（改变L和R）

    参数:
        contribution_rate: 缴费率τ（工资的比例）
                          例：0.20表示工资的20%
        wage: 平均工资
             例：6000元/月
        workers_per_retiree: 劳动者/退休者比率（L/R）
                            例：3.0表示3个工人养1个退休者

    返回:
        每个退休者的养老金

    示例:
        正常人口结构
        >>> payg_pension_benefit(0.20, 6000, 3.0)
        3600  # 养老金3600元/月

        老龄化社会（L/R下降）
        >>> payg_pension_benefit(0.20, 6000, 2.0)
        2400  # 同样缴费率，养老金减少

        年轻社会
        >>> payg_pension_benefit(0.20, 6000, 5.0)
        6000  # 替代率可达100%

    政策应对老龄化：
        提高缴费率
        >>> payg_pension_benefit(0.25, 6000, 2.0)
        3000  # 提高缴费率维持养老金
    """
    # TODO: 计算PAYG养老金
    # 提示：B = τ × W × (L/R)
    pass


def funded_pension_benefit(
    contribution_rate: float,
    wage: float,
    years_working: int,
    years_retired: int,
    interest_rate: float
) -> float:
    """
    计算基金积累制养老金的年收益。

    【基金积累制原理】
    工作期间缴费积累在个人账户，投资增值，退休后领取。

    【简化模型】
    假设：
    - 工资恒定（不考虑工资增长）
    - 利率恒定
    - 退休时一次性年金化

    工作期积累（储蓄终值）：
    如果每年缴费 C = τ × W，工作 T_w 年，利率 r
    退休时账户价值（年金终值）：
    FV = C × [(1+r)^T_w - 1] / r

    退休期领取（年金化）：
    如果退休后每年领取 B，领 T_r 年，利率 r
    需要初始资金（年金现值）：
    PV = B × [1 - (1+r)^(-T_r)] / r

    令 FV = PV，解出 B：
    B = FV × r / [1 - (1+r)^(-T_r)]

    【与PAYG比较】
    基金制收益率 = 资本回报率 r
    PAYG收益率 = n + g（人口增长 + 生产率增长）

    Aaron条件：
    r > n + g → 基金制更优
    r < n + g → PAYG更优

    参数:
        contribution_rate: 缴费率
                          例：0.15表示工资的15%
        wage: 年工资（假设恒定）
             例：72000元/年
        years_working: 工作年限
                      例：40年（25-65岁）
        years_retired: 退休年限（预期）
                      例：20年（65-85岁）
        interest_rate: 投资收益率（实际利率）
                      例：0.03表示3%年回报

    返回:
        每年可领取的养老金

    示例:
        标准情况
        >>> funded_pension_benefit(0.15, 72000, 40, 20, 0.03)
        29_500  # 每年约2.95万元养老金

        更高回报率
        >>> funded_pension_benefit(0.15, 72000, 40, 20, 0.05)
        45_000  # 回报率提高，养老金大增

        更长工作期
        >>> funded_pension_benefit(0.15, 72000, 45, 15, 0.03)
        52_000  # 多工作少领取，养老金提高

    注意:
        实际计算需要考虑工资增长、通胀、投资风险等
    """
    # TODO: 计算基金制养老金
    # 提示：
    # 1. 年缴费：annual_contribution = contribution_rate * wage
    # 2. 退休时账户价值（年金终值）：
    #    FV = annual_contribution * ((1+r)^T_w - 1) / r
    # 3. 年金化（年金支付）：
    #    B = FV * r / (1 - (1+r)^(-T_r))
    pass


def aaron_condition(
    population_growth: float,
    wage_growth: float,
    interest_rate: float
) -> str:
    """
    评估Aaron条件，判断哪种养老金制度更优。

    【Aaron条件】
    Henry Aaron（1966）提出的比较PAYG和基金制的条件。

    PAYG的隐含收益率：n + g
    - n: 人口（劳动力）增长率
    - g: 实际工资增长率

    基金制的收益率：r
    - r: 资本市场实际回报率

    Aaron条件：
    - 如果 n + g > r：PAYG更优
    - 如果 n + g < r：基金制更优
    - 如果 n + g = r：两者等价

    【经济直觉】
    PAYG是代际转移：
    - 高人口增长 → 更多年轻人养老人 → 替代率更高
    - 高工资增长 → 税基扩大 → 可支付更多养老金

    基金制是资本积累：
    - 高资本回报 → 积累更多财富 → 退休更富裕

    【历史背景】
    二战后（n + g高）：PAYG更优
    现代老龄化社会（n + g低）：基金制可能更优

    【实践考量】
    1. 转轨成本：从PAYG转向基金制需要"双重负担"
    2. 风险差异：PAYG是政治风险，基金制是市场风险
    3. 再分配：PAYG便于代内再分配

    参数:
        population_growth: 劳动力人口增长率
                          例：0.01表示1%年增长
        wage_growth: 实际工资增长率
                    例：0.02表示2%年增长
        interest_rate: 资本市场实际回报率
                      例：0.04表示4%年回报

    返回:
        "payg"（现收现付更优）或 "funded"（基金制更优）

    示例:
        高增长时期（如中国1980-2000）
        >>> aaron_condition(0.02, 0.06, 0.05)
        "payg"  # n + g = 8% > r = 5%

        老龄化社会（如日本）
        >>> aaron_condition(-0.01, 0.01, 0.03)
        "funded"  # n + g = 0% < r = 3%

        边界情况
        >>> aaron_condition(0.01, 0.02, 0.03)
        "funded"  # n + g = 3% = r = 3%，实际应返回哪个取决于定义
    """
    # TODO: 评估Aaron条件
    # 提示：
    # 计算 payg_return = population_growth + wage_growth
    # 比较 payg_return 和 interest_rate
    # 返回 "payg" 或 "funded"
    pass


def unemployment_insurance_moral_hazard(
    base_search_effort: float,
    replacement_rate: float,
    effort_elasticity: float
) -> float:
    """
    计算失业保险道德风险下的实际求职努力。

    【道德风险问题】
    失业保险可能降低失业者的求职努力。

    经济逻辑：
    - 有保险 → 失业成本降低 → 找工作不那么紧迫
    - 替代率越高 → 道德风险越严重

    【模型】
    假设求职努力随替代率下降：
    Effort = Base_Effort × (1 - RR)^ε

    其中：
    - Base_Effort: 无保险时的努力水平（最大努力）
    - RR: 替代率
    - ε: 努力弹性（衡量道德风险严重程度）

    【含义】
    - RR = 0（无保险）：Effort = Base_Effort（全力求职）
    - RR = 1（全额保险）：Effort = 0（不求职）
    - 0 < RR < 1：Effort介于两者之间

    【实证研究】
    大量研究证实失业保险延长失业期：
    - 替代率提高10% → 失业期延长1-2周
    - 保险期限延长 → 失业期也延长

    【政策启示】
    1. 替代率不宜太高
    2. 可考虑时间递减的替代率
    3. 加强求职监督和激励

    参数:
        base_search_effort: 无保险时的基础求职努力（标准化为1）
                           例：1.0表示最大努力
        replacement_rate: 失业保险替代率
                         例：0.6表示60%替代率
        effort_elasticity: 努力对替代率的弹性
                          例：0.5表示中等道德风险

    返回:
        实际求职努力水平

    示例:
        低替代率（道德风险小）
        >>> unemployment_insurance_moral_hazard(1.0, 0.3, 0.5)
        0.84  # 努力下降约16%

        高替代率（道德风险大）
        >>> unemployment_insurance_moral_hazard(1.0, 0.7, 0.5)
        0.55  # 努力下降约45%

        高弹性（道德风险严重）
        >>> unemployment_insurance_moral_hazard(1.0, 0.5, 1.0)
        0.50  # 努力下降50%
    """
    # TODO: 计算道德风险下的求职努力
    # 提示：Effort = base_search_effort × (1 - replacement_rate)^effort_elasticity
    pass


def optimal_unemployment_benefit(
    consumption_smoothing_gain: float,
    moral_hazard_cost: float
) -> float:
    """
    计算最优失业保险替代率的简化模型。

    【最优保险理论】
    Baily（1978）和 Chetty（2006）的最优失业保险公式。

    【权衡】
    保障收益（Consumption Smoothing）：
    - 失业保险平滑消费，减少福利损失
    - 边际收益与风险厌恶程度相关
    - 边际收益随替代率递减

    激励成本（Moral Hazard）：
    - 保险降低求职努力，延长失业
    - 边际成本与行为弹性相关
    - 边际成本随替代率递增

    【最优条件】
    边际保障收益 = 边际激励成本
    MC_smoothing = MC_moral_hazard

    【简化模型】
    假设线性近似：
    最优替代率 RR* = 保障收益系数 / (保障收益系数 + 激励成本系数)

    或更简单地：
    RR* = Gain / (Gain + Cost)

    【Baily-Chetty公式的含义】
    最优替代率取决于：
    1. 风险厌恶系数（越厌恶风险，替代率越高）
    2. 消费下降程度（下降越多，替代率越高）
    3. 失业期弹性（越弹性，替代率越低）

    参数:
        consumption_smoothing_gain: 消费平滑的边际收益
                                   衡量保险的福利价值
                                   例：0.6表示较高保障需求
        moral_hazard_cost: 道德风险的边际成本
                          衡量激励扭曲程度
                          例：0.4表示中等激励成本

    返回:
        最优替代率

    示例:
        平衡情况
        >>> optimal_unemployment_benefit(0.5, 0.5)
        0.5   # 最优替代率50%

        高保障需求
        >>> optimal_unemployment_benefit(0.7, 0.3)
        0.7   # 最优替代率70%

        高道德风险
        >>> optimal_unemployment_benefit(0.4, 0.6)
        0.4   # 最优替代率40%
    """
    # TODO: 计算最优替代率
    # 提示：RR* = gain / (gain + cost)
    pass


def adverse_selection_premium(
    low_risk_prob: float,
    high_risk_prob: float,
    high_risk_share: float
) -> float:
    """
    计算逆向选择下的保险市场均衡保费。

    【逆向选择问题】
    George Akerlof（1970）"柠檬市场"

    保险市场的信息不对称：
    - 投保人知道自己的风险类型
    - 保险公司不知道（或难以区分）

    【市场失灵过程】
    1. 保险公司按平均风险定价
    2. 低风险者觉得保费太贵，不投保
    3. 投保池平均风险上升
    4. 保费继续上升
    5. 更多低风险者退出
    6. 恶性循环，可能导致市场崩溃

    【模型】
    两类人：低风险（概率p_L）和高风险（概率p_H）
    高风险者占比：s

    平均风险概率：
    p_avg = s × p_H + (1-s) × p_L

    如果按平均风险定价且低风险者不参保：
    保费 = p_H（只有高风险者投保）

    【政府干预理由】
    强制参保可以：
    1. 打破逆向选择循环
    2. 形成包含所有风险类型的池
    3. 实现更低的平均保费

    参数:
        low_risk_prob: 低风险者的风险概率
                      例：0.01表示1%的风险发生概率
        high_risk_prob: 高风险者的风险概率
                       例：0.10表示10%的风险概率
        high_risk_share: 高风险者在人口中的比例
                        例：0.3表示30%是高风险者

    返回:
        市场均衡保费（作为风险概率）

    示例:
        理想市场（信息完全，按平均定价）
        >>> adverse_selection_premium(0.01, 0.10, 0.3)
        0.037  # 平均风险 = 0.3×0.10 + 0.7×0.01 = 3.7%

        如果低风险者全部退出
        >>> adverse_selection_premium(0.01, 0.10, 1.0)
        0.10   # 只剩高风险者，保费=10%

    注意:
        这是简化模型，实际逆向选择涉及动态调整过程
    """
    # TODO: 计算平均风险保费
    # 提示：p_avg = high_risk_share × high_risk_prob + (1-high_risk_share) × low_risk_prob
    pass


def dependency_ratio_impact(
    old_dependency_ratio: float,
    contribution_rate: float
) -> float:
    """
    计算老年抚养比对PAYG养老金替代率的影响。

    【抚养比与替代率的关系】
    老年抚养比（Old-Age Dependency Ratio）：
    ODR = 老年人口 / 劳动年龄人口 = R / L

    在PAYG系统中：
    总缴费 = τ × W × L
    总支出 = B × R

    预算平衡：τ × W × L = B × R
    替代率：RR = B / W = τ × L / R = τ / ODR

    【可持续替代率】
    给定缴费率τ和抚养比ODR：
    Sustainable RR = τ / ODR

    【老龄化的影响】
    抚养比上升（老龄化）→ 可持续替代率下降

    例：
    - ODR = 0.2（5个工人养1个老人）：RR = τ/0.2 = 5τ
    - ODR = 0.5（2个工人养1个老人）：RR = τ/0.5 = 2τ

    如果τ = 20%：
    - ODR = 0.2时：RR = 100%
    - ODR = 0.5时：RR = 40%

    【政策选择】
    面对老龄化，可以：
    1. 降低替代率（削减福利）
    2. 提高缴费率（增加税负）
    3. 延迟退休年龄（改变ODR）
    4. 增加移民（增加劳动力）

    参数:
        old_dependency_ratio: 老年抚养比（退休人口/劳动人口）
                             例：0.25表示4个工人养1个老人
        contribution_rate: 养老保险缴费率
                          例：0.20表示工资的20%

    返回:
        可持续的替代率

    示例:
        年轻社会
        >>> dependency_ratio_impact(0.20, 0.20)
        1.0   # 可以实现100%替代率

        适度老龄化
        >>> dependency_ratio_impact(0.33, 0.20)
        0.6   # 替代率降至60%

        严重老龄化
        >>> dependency_ratio_impact(0.50, 0.20)
        0.4   # 替代率仅40%

        日本式超级老龄化
        >>> dependency_ratio_impact(0.70, 0.20)
        0.29  # 替代率不到30%
    """
    # TODO: 计算可持续替代率
    # 提示：Sustainable_RR = contribution_rate / old_dependency_ratio
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
