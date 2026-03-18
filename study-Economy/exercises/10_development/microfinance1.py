# EXERCISE: microfinance1
# DIFFICULTY: ★★★★☆
# TOPIC: 小额信贷
#
# 说明：
# 小额信贷（Microfinance）是为传统金融体系排斥的穷人提供金融服务的创新模式。
# 2006年，孟加拉国格莱珉银行及其创始人Muhammad Yunus获得诺贝尔和平奖。
#
# 【为什么穷人被金融排斥？】
#
# 1. 缺乏抵押品
#    - 传统银行要求抵押物
#    - 穷人往往只有少量非正规资产
#    - 土地确权不完善
#
# 2. 信息不对称
#    - 逆向选择：银行无法区分好借款人和坏借款人
#    - 道德风险：借款后可能不努力还款
#    - 结果：高利率或拒绝贷款
#
# 3. 高交易成本
#    - 小额贷款的单位管理成本高
#    - 穷人分散在农村地区
#    - 缺乏信用记录
#
# 【传统信贷市场失灵】
# Stiglitz & Weiss (1981)：即使有信贷需求，银行可能选择信贷配给
# - 提高利率 → 吸引更高风险借款人 → 违约增加
# - 银行可能设定利率上限，拒绝部分借款人
#
# 【小额信贷的创新机制】
#
# 1. 团体贷款（Group Lending）
#    核心：连带责任（Joint Liability）
#    - 小组成员互相担保
#    - 一人违约，全组受影响
#
#    作用机制：
#    a) 同伴筛选（Peer Selection）
#       - 安全类型倾向与安全类型组队
#       - 自我选择解决逆向选择
#    b) 同伴监督（Peer Monitoring）
#       - 成员互相监督，确保努力
#       - 解决道德风险
#    c) 社会制裁（Social Sanctions）
#       - 违约者受到社区排斥
#       - 利用社会资本
#
# 2. 渐进式贷款（Progressive Lending）
#    - 从小额开始
#    - 按时还款后增加额度
#    - 创造动态激励
#
# 3. 频繁还款
#    - 每周/每两周还款
#    - 早期识别问题
#    - 培养还款习惯
#
# 4. 强制储蓄
#    - 贷款时要求存款
#    - 建立缓冲资金
#    - 培养储蓄习惯
#
# 【小额信贷的争议】
#
# 1. 利率过高？
#    - 年化利率通常30-100%
#    - 但仍低于非正式借贷（高利贷）
#    - 高运营成本是主因
#
# 2. 过度负债危机
#    - 印度安德拉邦危机（2010）
#    - 多头借贷
#    - 强制催收引发社会问题
#
# 3. 对最穷的人效果有限
#    - 贫困线以下人群参与率低
#    - 可能需要补助而非贷款
#    - 毕业式项目（Graduation Programs）
#
# 【发展中国家的小额信贷】
# - 孟加拉国格莱珉银行：900万借款人
# - 印度自助小组（SHG）：数千万成员
# - 肯尼亚M-Pesa：移动金融革命
# - 中国：农村信用社、小额贷款公司
#
# 任务：
# 1. 理解信贷约束的本质
# 2. 分析团体贷款的激励机制
# 3. 评估小额信贷的影响
#
# HINT1: 团体贷款利用社会资本替代物质抵押
# HINT2: 贫困陷阱可能需要补助（grants）而非贷款
# HINT3: 小额信贷不是万能药，需要结合其他干预

import numpy as np


def credit_rationing(
    collateral: float,
    loan_amount: float,
    interest_rate: float,
    default_probability: float
) -> bool:
    """
    信贷配给。

    【理论背景】
    Stiglitz & Weiss (1981) 证明了信贷配给的理论基础。
    银行在信息不对称下，可能选择拒绝部分借款人，即使他们愿意支付更高利率。

    【银行的贷款决策】
    银行批准贷款的条件：预期收益 ≥ 预期成本

    预期收益 = (1 - p) × (L × (1 + r)) + p × min(C, L × (1 + r))
    预期成本 = L

    其中：
    - L: 贷款金额
    - r: 利率
    - p: 违约概率
    - C: 抵押品价值

    简化条件：
    (1 - p) × L × (1 + r) + p × C ≥ L

    整理：C ≥ L × [1 - (1 - p) × (1 + r)] / p

    【信贷配给的后果】
    - 穷人无法投资高回报项目
    - 资源配置无效率
    - 贫困陷阱

    参数:
        collateral: 抵押品价值
            - 穷人通常很少
            - 例：土地、牲畜、设备
            - 例值：500美元
        loan_amount: 贷款金额
            - 小额信贷典型：$50-$500
            - 例值：1000美元
        interest_rate: 利率（年化）
            - 小额信贷：0.20-0.50
            - 例值：0.30
        default_probability: 违约概率
            - 优质借款人：0.01-0.05
            - 高风险借款人：0.10-0.30
            - 例值：0.10

    返回:
        是否获得贷款（True=批准，False=拒绝）

    示例:
        低风险借款人，充足抵押品
        >>> credit_rationing(1000, 1000, 0.30, 0.05)
        True  # 批准贷款

        高风险借款人，抵押品不足
        >>> credit_rationing(200, 1000, 0.30, 0.20)
        False  # 拒绝贷款

        典型穷人情况
        >>> credit_rationing(100, 500, 0.25, 0.10)
        False  # 抵押品不足，被拒

        计算过程：
        银行预期收益 = 0.9 × 500 × 1.25 + 0.1 × 100 = 562.5 + 10 = 572.5
        贷款成本 = 500
        572.5 > 500，应批准？

        但如果违约概率更高...
        >>> credit_rationing(100, 500, 0.25, 0.30)
        False  # 预期收益不足

    注意:
        1. 这是简化模型，实际银行决策更复杂
        2. 利率本身影响借款人类型（逆向选择）
        3. 信用评分等技术可改善信息问题
    """
    # TODO: 实现信贷配给模型
    # 提示：
    # 1. 计算银行预期收益
    #    = (1-p) × L × (1+r) + p × min(C, L×(1+r))
    # 2. 与贷款成本L比较
    # 3. 如果预期收益 >= L，返回True
    pass


def group_lending_payoff(
    own_success: bool,
    partner_success: bool,
    loan_amount: float,
    interest_rate: float,
    project_return: float
) -> float:
    """
    团体贷款支付。

    【理论背景】
    团体贷款（Group Lending）是格莱珉银行的核心创新。
    通过连带责任（Joint Liability），将违约成本分散给小组成员。

    【连带责任机制】
    假设两人小组（可推广到更多人）：
    - 如果都成功：各自还款，保留利润
    - 如果一人失败：成功者需要帮助还款
    - 如果都失败：可能无法还款

    【收益计算】
    设 R = 项目回报，L = 贷款额，r = 利率

    1. 自己成功，伙伴成功
       净收益 = R - L(1+r)

    2. 自己成功，伙伴失败
       净收益 = R - L(1+r) - L(1+r) = R - 2L(1+r)
       （需要帮伙伴还款）

    3. 自己失败
       净收益 = 0（无论伙伴如何）
       （违约，失去项目回报）

    参数:
        own_success: 自己的项目是否成功
            - True: 项目成功，获得回报
            - False: 项目失败，无回报
        partner_success: 伙伴的项目是否成功
            - True: 伙伴成功
            - False: 伙伴失败，可能需要帮还
        loan_amount: 贷款金额
            - 每人贷款额
            - 例：100美元
        interest_rate: 利率
            - 例：0.30
        project_return: 项目总回报（成功时）
            - 例：180美元

    返回:
        净收益（可能为负）

    示例:
        理想情况：都成功
        >>> group_lending_payoff(True, True, 100, 0.30, 180)
        50.0  # 净收益 = 180 - 100×1.3 = 50

        伙伴失败：需要帮还
        >>> group_lending_payoff(True, False, 100, 0.30, 180)
        -80.0  # 净收益 = 180 - 2×100×1.3 = -80

        自己失败
        >>> group_lending_payoff(False, True, 100, 0.30, 180)
        0.0  # 无回报

        都失败
        >>> group_lending_payoff(False, False, 100, 0.30, 180)
        0.0  # 无回报，可能违约

    注意:
        1. 这是简化的两人模型
        2. 实际中可能有更复杂的责任分担规则
        3. 社会制裁在模型外
    """
    # TODO: 计算团体贷款的净收益
    # 提示：
    # 如果自己失败：返回0
    # 如果自己成功且伙伴成功：返回 project_return - loan_amount * (1 + interest_rate)
    # 如果自己成功但伙伴失败：返回 project_return - 2 * loan_amount * (1 + interest_rate)
    pass


def peer_selection_effect(
    safe_type_probability: float,
    risky_type_probability: float,
    assortative_matching: float
) -> float:
    """
    同伴筛选效应。

    【理论背景】
    同伴筛选（Peer Selection）是团体贷款解决逆向选择的机制。

    在团体贷款中：
    - 借款人比银行更了解彼此
    - 他们会选择与自己类似的伙伴
    - 安全类型倾向于与安全类型组队

    【模型设定】
    假设有两类借款人：
    - 安全类型：成功概率高 p_s
    - 风险类型：成功概率低 p_r

    在个人贷款下：
    - 无法区分类型
    - 平均还款率 = 人口比例加权平均

    在团体贷款下：
    - 正向匹配（Assortative Matching）
    - 安全类型组成安全小组
    - 风险类型组成风险小组

    【计算团体还款率】
    假设两人小组，只要一人成功就还款：
    - 安全小组还款率 = 1 - (1 - p_s)²
    - 风险小组还款率 = 1 - (1 - p_r)²

    正向匹配程度影响混合小组的比例

    参数:
        safe_type_probability: 安全类型的成功概率
            - 例：0.95（95%成功率）
        risky_type_probability: 风险类型的成功概率
            - 例：0.60（60%成功率）
        assortative_matching: 正向匹配程度（0-1）
            - 0: 完全随机匹配
            - 1: 完全正向匹配（同类配对）
            - 例：0.8

    返回:
        团体贷款的平均还款率

    示例:
        完全正向匹配
        假设人口50%安全类型、50%风险类型
        >>> peer_selection_effect(0.95, 0.60, 1.0)
        0.91

        计算：
        安全小组（50%）：1-(1-0.95)² = 0.9975
        风险小组（50%）：1-(1-0.60)² = 0.84
        平均：0.5×0.9975 + 0.5×0.84 = 0.919

        随机匹配
        >>> peer_selection_effect(0.95, 0.60, 0.0)
        较低的还款率（更多混合小组）

        部分正向匹配
        >>> peer_selection_effect(0.95, 0.60, 0.5)
        中等还款率

    注意:
        1. 假设人口中安全和风险类型各占50%
        2. 实际中匹配程度取决于社区信息质量
        3. 连带责任增强了正向匹配激励
    """
    # TODO: 计算同伴筛选效应
    # 提示：
    # 1. 计算安全小组还款率：1 - (1 - p_s)²
    # 2. 计算风险小组还款率：1 - (1 - p_r)²
    # 3. 计算混合小组还款率（一人安全一人风险）：1 - (1-p_s)×(1-p_r)
    # 4. 根据正向匹配程度加权平均
    #    完全正向：50%安全小组 + 50%风险小组
    #    完全随机：50%混合小组 + 25%安全小组 + 25%风险小组
    pass


def peer_monitoring(
    monitoring_cost: float,
    detection_probability: float,
    social_sanction: float,
    shirking_benefit: float
) -> bool:
    """
    同伴监督。

    【理论背景】
    同伴监督（Peer Monitoring）解决道德风险问题。

    道德风险：借款后可能不努力工作
    - 银行难以监督
    - 但同村人可以观察

    【监督博弈】
    借款人决定是否努力（vs 偷懒）
    同伴决定是否监督

    偷懒的净收益 = 偷懒收益 - 被发现概率 × 惩罚
    B_shirk - p × S

    如果 B_shirk < p × S，偷懒不划算

    监督有效条件：
    detection_probability × social_sanction > shirking_benefit

    参数:
        monitoring_cost: 监督成本
            - 监督需要时间和精力
            - 例：5美元等值
        detection_probability: 发现偷懒的概率
            - 同村人相互了解程度
            - 例：0.8
        social_sanction: 社会制裁（违约者的惩罚）
            - 包括：声誉损失、排斥、无法获得未来贷款
            - 例：100美元等值
        shirking_benefit: 偷懒收益
            - 不努力工作节省的成本或获得的闲暇
            - 例：30美元等值

    返回:
        监督是否有效阻止偷懒（True=有效）

    示例:
        有效监督
        >>> peer_monitoring(5, 0.8, 100, 30)
        True
        # 偷懒的预期成本 = 0.8 × 100 = 80
        # 偷懒收益 = 30
        # 80 > 30，偷懒不划算

        无效监督
        >>> peer_monitoring(5, 0.3, 50, 30)
        False
        # 偷懒的预期成本 = 0.3 × 50 = 15
        # 偷懒收益 = 30
        # 15 < 30，偷懒划算

        城市vs农村
        农村社区（高检测概率、高社会制裁）
        >>> peer_monitoring(5, 0.9, 150, 40)
        True

        城市匿名社区（低检测概率、低社会制裁）
        >>> peer_monitoring(5, 0.4, 30, 40)
        False

    注意:
        1. 监督成本在此模型中未直接使用
        2. 实际中监督成本影响是否选择监督
        3. 社会资本是团体贷款的关键要素
    """
    # TODO: 判断同伴监督是否有效
    # 提示：
    # 如果 detection_probability × social_sanction > shirking_benefit，返回True
    # 否则返回False
    pass


def progressive_lending(
    initial_loan: float,
    success_multiplier: float,
    periods: int,
    success_rate: float
) -> np.ndarray:
    """
    渐进式贷款。

    【理论背景】
    渐进式贷款（Progressive Lending）创造动态激励。

    机制：
    - 初始贷款很小
    - 成功还款后，下次贷款额增加
    - 违约后，失去未来更大贷款的机会

    【动态激励】
    借款人面临跨期选择：
    - 今天违约：获得当期收益，但失去未来机会
    - 今天还款：牺牲部分当期收益，但保持未来机会

    当未来贷款足够大时，还款成为最优选择

    【数学模型】
    L_t = L_0 × m^(t-1)

    其中：
    - L_t: 第t期贷款
    - L_0: 初始贷款
    - m: 成功乘数

    预期贷款路径考虑成功概率：
    E[L_t] = L_0 × m^(t-1) × p^(t-1)

    参数:
        initial_loan: 初始贷款额
            - 小额信贷起步很小
            - 例：50美元
        success_multiplier: 成功后的贷款乘数
            - 典型值：1.2-2.0
            - 例：1.5（贷款增加50%）
        periods: 期数
            - 例：5期
        success_rate: 每期成功概率
            - 例：0.90（90%成功率）

    返回:
        预期贷款路径（数组）

    示例:
        典型渐进式贷款
        >>> progressive_lending(50, 1.5, 5, 0.90)
        array([50.0, 67.5, 91.1, 123.0, 166.1])

        计算：
        第1期：50
        第2期：50 × 1.5 × 0.9 = 67.5（期望值）
        第3期：67.5 × 1.5 × 0.9 = 91.1
        ...

        高风险借款人
        >>> progressive_lending(50, 1.5, 5, 0.70)
        array([50.0, 52.5, 55.1, 57.9, 60.8])
        # 低成功率导致贷款增长慢

        保守政策（低乘数）
        >>> progressive_lending(50, 1.2, 5, 0.90)
        array([50.0, 54.0, 58.3, 63.0, 68.0])

    注意:
        1. 这是预期值，实际路径取决于是否成功
        2. 渐进式贷款也用于发现借款人类型
        3. 乘数过高可能导致过度负债
    """
    # TODO: 计算预期贷款路径
    # 提示：
    # 1. 创建长度为periods的数组
    # 2. 第1期 = initial_loan
    # 3. 第t期 = 第(t-1)期 × success_multiplier × success_rate
    # 或直接用公式：L_t = initial_loan × (success_multiplier × success_rate)^(t-1)
    pass


def effective_interest_rate(
    nominal_rate: float,
    compounding_frequency: int,
    fees: float,
    forced_savings_rate: float
) -> float:
    """
    有效利率。

    【理论背景】
    小额信贷的名义利率往往低估实际成本。
    有效利率（Effective Interest Rate）考虑所有隐藏成本。

    【隐藏成本】
    1. 手续费：贷款时收取的固定费用
    2. 强制储蓄：要求存入一定比例资金
    3. 复利频率：频繁还款增加有效利率
    4. 保险费：强制保险

    【有效利率计算】
    考虑费用后的有效本金：
    Effective_principal = Loan × (1 - fees) × (1 - forced_savings)

    年化利率（考虑复利频率）：
    EAR = (1 + r/n)^n - 1

    总有效利率 ≈ EAR / (1 - fees - forced_savings)

    【小额信贷利率争议】
    - 名义年利率：15-30%
    - 有效年利率：50-100%+
    - 仍低于非正规借贷（100-500%+）

    参数:
        nominal_rate: 名义年利率
            - 小额信贷机构公布的利率
            - 例：0.25（25%）
        compounding_frequency: 年复利频率
            - 每周还款：52
            - 每月还款：12
            - 例：52
        fees: 手续费率（占贷款比例）
            - 例：0.05（5%手续费）
        forced_savings_rate: 强制储蓄率
            - 例：0.10（10%强制储蓄）

    返回:
        真实年化利率

    示例:
        典型小额信贷产品
        >>> effective_interest_rate(0.25, 52, 0.05, 0.10)
        0.388  # 有效利率约39%！

        名义利率25%，但：
        - 每周复利使EAR = (1+0.25/52)^52 - 1 = 0.284
        - 只能使用85%的本金（15%用于费用和储蓄）
        - 有效利率 ≈ 0.284 / 0.85 = 0.334

        更极端案例
        >>> effective_interest_rate(0.30, 52, 0.10, 0.15)
        0.578  # 有效利率近58%

        透明产品（无隐藏费用）
        >>> effective_interest_rate(0.25, 12, 0.0, 0.0)
        0.281  # 接近名义利率

    注意:
        1. 不同计算方法可能给出不同结果
        2. 强制储蓄如果有利息，影响会减小
        3. 应比较替代融资渠道的成本
    """
    # TODO: 计算有效利率
    # 提示：
    # 1. 计算复利后的年化利率：EAR = (1 + nominal_rate/frequency)^frequency - 1
    # 2. 计算可用本金比例：usable = 1 - fees - forced_savings_rate
    # 3. 有效利率 = EAR / usable
    pass


def credit_constraint_cost(
    optimal_investment: float,
    actual_investment: float,
    marginal_return: float
) -> float:
    """
    信贷约束的福利成本。

    【理论背景】
    当借款人面临信贷约束时，无法投资最优水平。
    这导致福利损失（Welfare Loss）。

    【模型】
    假设投资回报递减：
    Return(I) = R × I - 0.5 × I²/K

    最优投资 I* 使边际收益等于资金成本（假设为0简化）：
    R - I*/K = 0
    I* = R × K

    如果受约束只能投资 I < I*：
    损失 ≈ (I* - I) × 平均边际回报

    简化计算：
    Loss = (optimal - actual) × marginal_return / 2

    【发展中国家的信贷约束】
    - 农户无法购买足够肥料、种子
    - 微型企业无法扩大规模
    - 高回报投资机会被放弃

    参数:
        optimal_investment: 最优投资水平
            - 无约束时的理想投资
            - 例：1000美元
        actual_investment: 实际投资水平
            - 受信贷约束的实际投资
            - 例：300美元
        marginal_return: 边际回报率
            - 额外投资的回报
            - 发展中国家往往很高（0.50-2.00）
            - 例：0.80（80%回报）

    返回:
        福利损失（金额）

    示例:
        典型信贷约束农户
        >>> credit_constraint_cost(1000, 300, 0.80)
        280.0

        计算：
        未投资额 = 1000 - 300 = 700
        平均边际回报 ≈ 0.80 / 2 = 0.40（因递减）
        福利损失 = 700 × 0.40 = 280

        微型企业
        >>> credit_constraint_cost(5000, 1000, 1.20)
        2400.0

        # 信贷约束使企业损失2400美元潜在收益

        轻微约束
        >>> credit_constraint_cost(1000, 800, 0.50)
        50.0

    注意:
        1. 这是简化的三角形近似
        2. 实际边际回报可能非线性
        3. 信贷约束可能有长期动态效应
    """
    # TODO: 计算信贷约束福利成本
    # 提示：
    # Loss = (optimal_investment - actual_investment) × marginal_return / 2
    # 使用三角形面积近似（因边际回报递减）
    pass


def poverty_trap_threshold(
    initial_wealth: float,
    returns_below: float,
    returns_above: float,
    threshold: float
) -> str:
    """
    贫困陷阱。

    【理论背景】
    贫困陷阱（Poverty Trap）假说认为存在财富阈值：
    - 低于阈值：回报率低，无法积累
    - 高于阈值：回报率高，可以增长

    【机制】
    1. 规模不经济
       - 小规模生产成本高
       - 无法享受规模优势

    2. 信贷约束
       - 穷人无法借款投资高回报项目
       - 只能投资低回报项目

    3. 营养效率工资
       - 穷人营养不足，生产力低
       - 低收入→低营养→低生产力→低收入

    【数学模型】
    W_t+1 = W_t × (1 + r(W_t))

    其中 r(W) = { r_low  if W < threshold
                { r_high if W >= threshold

    如果 W_0 < threshold 且 r_low < 0：
    财富持续下降，陷入贫困

    参数:
        initial_wealth: 初始财富
            - 例：500美元
        returns_below: 阈值以下的回报率
            - 可能为负（净消耗）
            - 例：-0.05（-5%）
        returns_above: 阈值以上的回报率
            - 通常为正
            - 例：0.10（10%）
        threshold: 财富阈值
            - 跨越后进入增长轨道
            - 例：1000美元

    返回:
        "trapped"（陷入贫困）或 "escaping"（正在脱贫）

    示例:
        贫困陷阱
        >>> poverty_trap_threshold(500, -0.05, 0.10, 1000)
        "trapped"
        # 初始财富500 < 阈值1000，且回报率-5%
        # 财富将持续下降

        正在脱贫
        >>> poverty_trap_threshold(1200, -0.05, 0.10, 1000)
        "escaping"
        # 初始财富1200 > 阈值1000，回报率10%
        # 财富将持续增长

        边界情况
        >>> poverty_trap_threshold(1000, -0.05, 0.10, 1000)
        "escaping"  # 刚好达到阈值

    注意:
        1. 贫困陷阱假说有争议
        2. 实证证据不一致
        3. 如果存在贫困陷阱，需要"大推动"政策
    """
    # TODO: 判断是否陷入贫困陷阱
    # 提示：
    # 如果 initial_wealth < threshold，使用 returns_below
    # 如果 returns_below 使财富下降（< 0），返回 "trapped"
    # 否则返回 "escaping"
    # 如果 initial_wealth >= threshold，返回 "escaping"
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
