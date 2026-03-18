# EXERCISE: human_capital_dev1
# DIFFICULTY: ★★★★☆
# TOPIC: 人力资本与发展
#
# 说明：
# 人力资本（Human Capital）是发展的关键驱动力。
# Gary Becker（1964）将教育、健康和技能培训视为对人的投资，与物质资本投资类似。
#
# 【人力资本的定义】
# 人力资本 = 体现在人身上的知识、技能、健康和能力
# 它提高个人的生产力，并可以通过教育、培训、医疗等投资来积累。
#
# 【人力资本的组成】
#
# 1. 教育（Education）
#    - 正规教育：学校教育（小学、中学、大学）
#    - 非正规教育：职业培训、在职学习
#    - 认知技能：读写算、批判性思维
#    - 非认知技能：毅力、自律、社交能力
#
# 2. 健康（Health）
#    - 身体健康：营养、疾病控制
#    - 心理健康：压力管理、心理韧性
#    - 健康影响生产力和学习能力
#
# 3. 技能与经验
#    - 在职培训（On-the-job training）
#    - 干中学（Learning by doing）
#    - 经验积累
#
# 【教育回报】
#
# 私人回报：
# - 每多一年教育带来的工资增长
# - 发展中国家通常10-15%（高于发达国家5-10%）
# - 初等教育回报最高
#
# 社会回报：
# - 外部性：公民参与、犯罪减少、健康知识传播
# - 社会回报可能高于私人回报
#
# 【明瑟收入方程】
# Jacob Mincer (1974) 提出的经典模型：
# ln(w) = ln(w₀) + r×S + β₁×X + β₂×X²
#
# 其中：
# - w: 工资
# - S: 受教育年限
# - X: 工作经验
# - r: 教育回报率
#
# 【健康-财富关系】
# 健康 ↔ 财富 是双向因果关系：
# - 健康 → 生产力 → 收入
# - 收入 → 医疗投资 → 健康
# - 可能形成贫困-疾病陷阱
#
# 【发展中国家的人力资本挑战】
# 1. 教育质量差：出勤不等于学习
# 2. 辍学率高：童工、早婚
# 3. 营养不良：影响认知发展
# 4. 疾病负担：疟疾、寄生虫
# 5. 女孩教育差距
#
# 【发展政策干预】
#
# 1. 条件现金转移（CCT）
#    - 墨西哥Progresa/Oportunidades
#    - 巴西Bolsa Familia
#    - 以入学为条件发放现金
#
# 2. 学校供餐计划
#    - 解决营养不足
#    - 提高出勤率
#
# 3. 去虫项目（Deworming）
#    - Miguel & Kremer (2004)
#    - 低成本高收益
#
# 4. 信息干预
#    - 告知教育回报
#    - 改变预期
#
# 任务：
# 1. 计算教育回报
# 2. 分析健康投资效果
# 3. 评估人力资本政策
#
# HINT1: 教育回报率在发展中国家通常更高（稀缺性）
# HINT2: 儿童早期投资回报最高（关键期）
# HINT3: 教育质量比数量更重要

import numpy as np


def mincer_earnings(
    years_of_schooling: int,
    experience: int,
    base_wage: float,
    schooling_return: float = 0.1,
    experience_return: float = 0.03,
    experience_squared_return: float = -0.0005
) -> float:
    """
    明瑟收入方程。

    【理论背景】
    Jacob Mincer (1974) 提出的人力资本收入方程是劳动经济学的基础模型。
    该方程将工资与教育和经验联系起来。

    【方程推导】
    ln(w) = ln(w₀) + r×S + β₁×X + β₂×X²

    其中：
    - w: 观察到的工资
    - w₀: 基础工资（无教育无经验）
    - S: 受教育年限
    - X: 潜在工作经验 = 年龄 - 教育年限 - 6
    - r: 教育回报率（每年教育的工资增长率）
    - β₁: 经验的线性回报
    - β₂: 经验的二次项（通常为负，反映递减回报）

    【教育回报的含义】
    r = 0.10 意味着每多一年教育，工资提高约10%

    【经验的倒U型效应】
    经验增加工资（学习、技能积累）
    但速度递减（技能过时、体力下降）
    工资峰值年龄 ≈ -β₁/(2×β₂)

    【发展中国家特点】
    - 教育回报更高（10-15%）
    - 初等教育回报最高
    - 女性回报常高于男性

    参数:
        years_of_schooling: 受教育年限
            - 例：小学6年，初中9年，高中12年，大学16年
            - 发展中国家平均：5-10年
        experience: 工作经验（年）
            - 潜在经验 = 年龄 - 教育年限 - 6
            - 例：10年
        base_wage: 基础工资（无教育无经验时）
            - 当地最低工资或非技术工工资
            - 例：1000元/月
        schooling_return: 教育回报率（默认0.1）
            - 发展中国家：0.08-0.15
            - 发达国家：0.05-0.10
        experience_return: 经验线性回报（默认0.03）
            - 经验每年增加3%工资
        experience_squared_return: 经验二次项（默认-0.0005）
            - 负值反映递减回报

    返回:
        预测工资

    示例:
        大学毕业，5年经验
        >>> mincer_earnings(16, 5, 1000, 0.10, 0.03, -0.0005)
        5412.4

        计算过程：
        ln(w) = ln(1000) + 0.10×16 + 0.03×5 - 0.0005×25
              = 6.908 + 1.6 + 0.15 - 0.0125
              = 8.596
        w = exp(8.596) = 5412.4

        初中毕业，20年经验（工厂工人）
        >>> mincer_earnings(9, 20, 1000, 0.10, 0.03, -0.0005)
        4097.8

        高中毕业 vs 大学毕业
        >>> mincer_earnings(12, 5, 1000)
        3643.1  # 高中
        >>> mincer_earnings(16, 5, 1000)
        5412.4  # 大学
        # 大学溢价约49%

    注意:
        1. 这是简化模型，未考虑能力偏误
        2. 教育质量差异可能使回报率变化
        3. 行业、地区差异未考虑
    """
    # TODO: 实现明瑟收入方程
    # 提示：
    # 1. 计算对数工资
    #    ln_wage = ln(base_wage) + r×S + β₁×X + β₂×X²
    # 2. 转换回实际工资
    #    wage = exp(ln_wage)
    # 使用 np.log() 和 np.exp()
    pass


def private_return_to_education(
    wage_with_education: float,
    wage_without: float,
    education_cost: float,
    years: int
) -> float:
    """
    教育私人回报率（内部收益率）。

    【理论背景】
    私人回报率是个人教育投资决策的关键指标。
    它衡量教育投资的"利息"——使收益现值等于成本现值的折现率。

    【计算方法】
    简化公式（假设工作年限长，忽略后期）：

    IRR ≈ (w_edu - w_no_edu) / (direct_cost + foregone_earnings)

    更精确的方法需要求解NPV = 0的r

    【成本组成】
    1. 直接成本：学费、书本、交通
    2. 机会成本：上学期间放弃的收入（foregone earnings）

    【私人回报 vs 社会回报】
    私人回报：只考虑个人工资增加
    社会回报：还包括外部性（犯罪减少、公民参与等）

    如果社会回报 > 私人回报，应补贴教育

    参数:
        wage_with_education: 有教育后的年工资
            - 接受额外教育后的预期工资
            - 例：80000元/年（大学毕业）
        wage_without: 无教育的年工资
            - 不接受该教育的预期工资
            - 例：40000元/年（高中毕业）
        education_cost: 每年教育成本
            - 直接成本（学费等）
            - 例：10000元/年
        years: 教育年限
            - 例：4年（大学）

    返回:
        内部收益率（近似值）

    示例:
        大学教育决策
        >>> private_return_to_education(80000, 40000, 10000, 4)
        0.20  # 约20%回报率

        计算：
        年收益 = 80000 - 40000 = 40000
        总成本 = 4 × (10000 + 40000) = 200000（直接成本 + 机会成本）
        近似回报率 ≈ 40000 / (200000/4) = 40000 / 50000 = 0.80?

        简化公式：回报率 ≈ (w_diff) / (years × cost + years × w_without / 2)

        职业培训（短期）
        >>> private_return_to_education(50000, 40000, 5000, 1)
        0.22  # 约22%回报率

    注意:
        1. 这是简化计算，精确IRR需要迭代求解
        2. 未考虑失业风险
        3. 工资增长和贴现率会影响结果
    """
    # TODO: 计算教育私人回报率
    # 简化公式：
    # IRR ≈ (wage_with - wage_without) / (education_cost + wage_without)
    # 这是一个近似值，实际IRR需要迭代求解NPV=0
    pass


def social_return_to_education(
    private_return: float,
    external_benefits: float,
    public_subsidy_rate: float
) -> float:
    """
    教育社会回报率。

    【理论背景】
    教育具有正外部性（Positive Externalities）：
    个人教育投资会给社会带来额外收益。

    社会回报 = 私人回报 + 外部收益 - 公共补贴调整

    【外部收益的类型】
    1. 生产力外溢
       - 受教育者提高周围同事的生产力
       - 知识分享

    2. 犯罪减少
       - 教育降低犯罪率
       - 节省司法和监狱成本

    3. 公民参与
       - 投票、志愿服务
       - 民主质量

    4. 健康外部性
       - 健康知识传播
       - 疫苗接种配合

    5. 代际效应
       - 母亲教育提高子女发展

    【公共补贴的考虑】
    如果政府补贴教育，私人成本低于社会成本
    社会回报需要调整补贴

    参数:
        private_return: 私人回报率
            - 来自 private_return_to_education
            - 例：0.12（12%）
        external_benefits: 外部收益率
            - 外部性相对于私人收益的比例
            - 例：0.05（5个百分点）
            - 初等教育外部性更高
        public_subsidy_rate: 公共补贴率
            - 政府承担的教育成本比例
            - 例：0.70（70%由政府支付）

    返回:
        社会回报率

    示例:
        初等教育（高外部性，高补贴）
        >>> social_return_to_education(0.12, 0.08, 0.90)
        0.22  # 社会回报22%，远高于私人回报

        计算：
        简化：社会回报 ≈ 私人回报 + 外部收益 + 补贴调整
        = 0.12 + 0.08 + 补贴效应
        补贴使私人成本低，私人回报被高估，社会回报需调整

        更简单的近似：
        社会回报 ≈ (私人回报 + 外部收益) / (1 - 补贴率)
        如果补贴率高，社会成本（分母）低，社会回报高

        高等教育（低外部性，中等补贴）
        >>> social_return_to_education(0.10, 0.03, 0.50)
        0.26

    注意:
        1. 外部收益难以精确测量
        2. 不同教育水平外部性差异大
        3. 如果社会回报 > 私人回报，应增加教育补贴
    """
    # TODO: 计算社会回报率
    # 简化公式：
    # 社会回报 ≈ (private_return + external_benefits) / (1 - public_subsidy_rate)
    # 或更简单：social = private + external + 补贴调整
    # 使用第一个公式
    pass


def health_productivity_effect(
    health_status: float,
    base_productivity: float,
    elasticity: float = 0.5
) -> float:
    """
    健康对生产力的影响。

    【理论背景】
    健康是人力资本的重要组成部分。
    健康状况直接影响工作能力和生产效率。

    【作用机制】
    1. 体力工作能力
       - 健康工人可以工作更长时间
       - 力量和耐力

    2. 认知能力
       - 营养不良影响大脑发育
       - 疾病影响注意力和记忆

    3. 出勤率
       - 患病缺勤
       - 照顾生病家人

    4. 学习效率
       - 儿童健康影响学习吸收
       - 疾病期间教育中断

    【生产力函数】
    Productivity = Base × (Health)^ε

    其中ε是健康弹性，通常0.3-0.7

    【发展中国家的健康挑战】
    - 疟疾：非洲每年GDP损失约1%
    - 寄生虫：儿童认知发育受损
    - 营养不良：早期发育受阻（难以逆转）
    - HIV/AIDS：劳动年龄人口损失

    参数:
        health_status: 健康状况（0-1）
            - 0: 极差健康（无法工作）
            - 1: 完美健康
            - 发展中国家工人可能：0.6-0.8
            - 例：0.7
        base_productivity: 基础生产力
            - 完美健康时的生产力
            - 例：100（产出单位/天）
        elasticity: 健康弹性（默认0.5）
            - 健康提高1%，生产力提高ε%
            - 体力劳动弹性更高

    返回:
        实际生产力

    示例:
        典型发展中国家工人
        >>> health_productivity_effect(0.7, 100, 0.5)
        83.7

        计算：100 × (0.7)^0.5 = 100 × 0.837 = 83.7
        健康不佳使生产力损失16.3%

        健康改善的效果
        >>> health_productivity_effect(0.7, 100, 0.5)
        83.7
        >>> health_productivity_effect(0.9, 100, 0.5)
        94.9
        # 健康从0.7提高到0.9，生产力提高13.4%

        体力劳动者（高弹性）
        >>> health_productivity_effect(0.6, 100, 0.7)
        71.1

        办公室工作（低弹性）
        >>> health_productivity_effect(0.6, 100, 0.3)
        85.1

    注意:
        1. 这是简化模型
        2. 弹性因职业类型差异大
        3. 存在健康阈值效应（严重疾病无法工作）
    """
    # TODO: 计算健康对生产力的影响
    # 公式：Productivity = base_productivity × (health_status)^elasticity
    pass


def nutrition_cognitive_effect(
    calorie_intake: float,
    recommended_intake: float,
    cognitive_score: float
) -> float:
    """
    营养对认知能力的影响。

    【理论背景】
    充足营养对儿童大脑发育至关重要。
    生命早期1000天（孕期至2岁）是关键窗口期。

    【营养不良的类型】
    1. 热量不足（Undernutrition）
       - 总能量摄入不足
       - 导致发育迟缓

    2. 微量营养素缺乏
       - 铁：贫血、认知损伤
       - 碘：甲状腺功能、智力损伤
       - 锌：免疫、生长

    3. 蛋白质-能量营养不良
       - Kwashiorkor（夸希奥科病）
       - Marasmus（消瘦症）

    【认知影响模型】
    当摄入 < 推荐量：
    Cognitive_adjusted = Cognitive × (intake/recommended)^α

    当摄入 >= 推荐量：
    Cognitive_adjusted = Cognitive（无额外收益）

    α反映营养不足的敏感性

    【经验证据】
    - Hoddinott et al. (2008)：危地马拉营养干预增加成年收入46%
    - 去虫使儿童学习成绩提高
    - 学校供餐提高测试分数

    参数:
        calorie_intake: 实际卡路里摄入
            - 每日摄入热量
            - 例：1500千卡
        recommended_intake: 推荐摄入量
            - 年龄、性别、活动水平相关
            - 成人约2000千卡
            - 儿童约1500-1800千卡
        cognitive_score: 基础认知分数
            - 营养充足时的潜在分数
            - 例：100（标准化）

    返回:
        调整后认知分数

    示例:
        营养不足儿童
        >>> nutrition_cognitive_effect(1200, 1800, 100)
        81.6

        计算（假设α=0.5）：
        比例 = 1200/1800 = 0.667
        调整分数 = 100 × (0.667)^0.5 = 81.6
        营养不足使认知能力下降18.4%

        严重营养不良
        >>> nutrition_cognitive_effect(800, 1800, 100)
        66.7

        营养充足
        >>> nutrition_cognitive_effect(2000, 1800, 100)
        100.0  # 不超过满分

    注意:
        1. 效应在幼年期最强，早期损伤难以完全恢复
        2. 蛋白质和微量营养素同样重要
        3. 慢性vs急性营养不良有不同影响
    """
    # TODO: 计算营养对认知的影响
    # 提示：
    # 1. 如果 intake >= recommended，返回 cognitive_score
    # 2. 如果 intake < recommended：
    #    ratio = intake / recommended
    #    adjusted = cognitive_score × ratio^0.5（假设弹性0.5）
    pass


def conditional_cash_transfer(
    base_enrollment: float,
    transfer_amount: float,
    income: float,
    schooling_cost: float
) -> float:
    """
    条件现金转移对入学率的影响。

    【理论背景】
    条件现金转移（CCT）是发展政策的重要工具。
    政府向贫困家庭发放现金，条件是子女必须上学/接种疫苗等。

    【著名项目】
    - 墨西哥 PROGRESA/Oportunidades（1997年起）
    - 巴西 Bolsa Familia
    - 菲律宾 Pantawid
    - 印度尼西亚 PKH

    【作用机制】
    1. 收入效应
       - 增加家庭收入
       - 减少童工需求

    2. 价格效应
       - 降低上学的净成本
       - 补偿机会成本

    3. 行为改变
       - 条件性改变家庭优先级
       - 长期习惯形成

    【简化模型】
    假设家庭决策基于净成本：
    Net_cost = Schooling_cost - Transfer

    入学弹性模型：
    Enrollment = Base + β × (Transfer / Income)

    Transfer越高相对于收入，入学率提高越多

    参数:
        base_enrollment: 基础入学率（无CCT时）
            - 贫困地区初等教育：0.70-0.85
            - 中等教育：0.40-0.60
            - 例：0.75
        transfer_amount: 转移金额（每月或每年）
            - 通常为收入的10-30%
            - 例：500元/月
        income: 家庭月收入
            - 贫困线附近家庭
            - 例：3000元/月
        schooling_cost: 上学成本（每月或每年）
            - 包括学费、书本、交通、校服
            - 机会成本另算
            - 例：200元/月

    返回:
        新入学率（0-1之间，不超过1）

    示例:
        典型CCT项目
        >>> conditional_cash_transfer(0.75, 500, 3000, 200)
        0.88

        计算：
        净成本降低 = 500 - 200 = 300
        相对收入 = 500 / 3000 = 0.167
        假设弹性β = 0.8
        新入学率 = 0.75 + 0.8 × 0.167 = 0.884

        较慷慨的转移
        >>> conditional_cash_transfer(0.60, 800, 2000, 300)
        0.92

        转移金额小
        >>> conditional_cash_transfer(0.80, 100, 5000, 200)
        0.82  # 影响有限

    注意:
        1. 这是简化模型，实际效果因项目设计而异
        2. 入学率有上限（1.0）
        3. CCT也影响出勤率和学习成绩
        4. 长期效果（代际）可能更大
    """
    # TODO: 计算CCT对入学率的影响
    # 简化模型：
    # new_enrollment = base + β × (transfer / income)
    # 假设 β = 0.8
    # 确保结果不超过1.0
    pass


def quality_quantity_tradeoff(
    income: float,
    cost_per_child: float,
    quality_elasticity: float
) -> tuple[int, float]:
    """
    数量-质量权衡。

    【理论背景】
    Becker & Lewis (1973) 提出家庭面临子女数量和质量的权衡。
    收入约束下，多生孩子意味着每个孩子获得的资源减少。

    【模型】
    家庭效用 U = U(n, q)
    其中 n = 子女数量，q = 每个孩子的质量（教育、营养等）

    预算约束：Income = n × c(q)

    c(q) = 每个孩子的成本，随质量增加

    最优化条件给出 n* 和 q*

    【发展中国家观察】
    - 收入提高 → 少生优生
    - 女孩教育 → 生育率下降
    - 生育率下降 → 人口红利

    【数量-质量互动】
    Quality = Base × (Income / (n × cost))^ε

    随着n增加，每个孩子获得的资源减少，质量下降

    参数:
        income: 家庭年收入
            - 可用于子女的预算
            - 例：60000元/年
        cost_per_child: 每个孩子基本成本
            - 包括食物、住房、基本教育
            - 例：15000元/年
        quality_elasticity: 质量弹性
            - 资源增加对质量的影响
            - 例：0.4

    返回:
        (最优子女数量, 每个孩子的投资)

    示例:
        中等收入家庭
        >>> quality_quantity_tradeoff(60000, 15000, 0.4)
        (2, 30000)

        计算：
        最大可养孩子数 = 60000 / 15000 = 4
        最优化可能在2-3个孩子
        简化：n* = sqrt(income / cost)（假设效用函数形式）

        高收入家庭
        >>> quality_quantity_tradeoff(120000, 15000, 0.4)
        (3, 40000)  # 可以多生但也提高质量

        贫困家庭
        >>> quality_quantity_tradeoff(30000, 15000, 0.4)
        (1, 30000)  # 只能负担一个孩子

    注意:
        1. 这是高度简化的模型
        2. 偏好因文化差异很大
        3. 社会保障也影响生育决策
        4. 孩子数量取整
    """
    # TODO: 计算数量-质量权衡
    # 简化模型：
    # n* = max(1, int(sqrt(income / cost_per_child)))
    # investment = income / n*
    # 确保至少1个孩子
    pass


def intergenerational_mobility(
    parent_education: np.ndarray,
    child_education: np.ndarray
) -> float:
    """
    代际流动性。

    【理论背景】
    代际流动性衡量父母特征对子女结果的影响程度。
    高流动性意味着家庭背景影响小，机会更平等。

    【测量方法】
    回归子女教育于父母教育：
    Child_edu = α + β × Parent_edu + ε

    代际相关/弹性 β：
    - β = 1：完全不流动（子女完全继承父母地位）
    - β = 0：完全流动（家庭背景无影响）

    发达国家β约0.3-0.5
    发展中国家β可能更高

    【影响代际流动的因素】
    1. 教育可及性
       - 公共教育普及提高流动性

    2. 信贷约束
       - 穷人无法借款投资教育

    3. 社会网络
       - 职业机会依赖关系

    4. 歧视
       - 基于家庭背景的歧视

    【政策含义】
    低流动性说明机会不平等，需要：
    - 普及公共教育
    - 针对贫困生的财务援助
    - 早期儿童发展项目

    参数:
        parent_education: 父母教育年限数组
            - 形状：(n,)
            - 例：np.array([6, 8, 12, 4, 10, ...])
        child_education: 子女教育年限数组
            - 形状：(n,)
            - 例：np.array([9, 10, 14, 8, 12, ...])

    返回:
        代际相关系数（β，0-1之间）

    示例:
        高流动性社会
        父母教育差异大，但子女教育趋同
        >>> parent = np.array([4, 6, 8, 10, 12, 14, 16])
        >>> child = np.array([10, 11, 12, 12, 13, 13, 14])
        >>> intergenerational_mobility(parent, child)
        0.28  # 低相关，高流动

        低流动性社会
        子女教育高度依赖父母
        >>> parent = np.array([4, 6, 8, 10, 12, 14, 16])
        >>> child = np.array([5, 7, 9, 11, 13, 15, 17])
        >>> intergenerational_mobility(parent, child)
        0.95  # 高相关，低流动

        中等流动性
        >>> parent = np.array([5, 7, 9, 11, 13])
        >>> child = np.array([8, 10, 11, 13, 14])
        >>> intergenerational_mobility(parent, child)
        0.55

    注意:
        1. 这测量的是线性相关，实际关系可能非线性
        2. 应控制其他因素（如智力遗传）
        3. 收入流动性可能与教育流动性不同
    """
    # TODO: 计算代际相关系数
    # 使用简单线性回归的斜率 β
    # β = Cov(parent, child) / Var(parent)
    # 或使用相关系数作为近似
    # 提示：
    # cov = np.cov(parent_education, child_education)[0,1]
    # var = np.var(parent_education)
    # beta = cov / var
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
