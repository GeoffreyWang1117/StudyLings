# EXERCISE: rct1
# DIFFICULTY: ★★★★★
# TOPIC: 随机对照试验
#
# 说明：
# 随机对照试验（Randomized Controlled Trials, RCT）是发展经济学的革命性方法。
# 2019年诺贝尔经济学奖授予Abhijit Banerjee、Esther Duflo和Michael Kremer，
# 表彰他们在全球贫困研究中使用实验方法的贡献。
#
# 【为什么需要RCT？】
#
# 发展政策评估面临根本性挑战：
# - 选择偏误：参与项目的人可能本来就不同
# - 反向因果：结果可能影响"原因"
# - 遗漏变量：未观察到的因素同时影响处理和结果
#
# 例如：小额信贷借款人收入提高，是因为小额信贷，还是因为他们本来就更有进取心？
#
# 【RCT的核心思想】
# 通过随机分配处理，使处理组和对照组在所有特征上（包括未观察到的）平均相同。
# 因此，两组结果的差异可以归因于处理本身。
#
# 【RCT的优势】
# 1. 因果识别清晰：随机化消除选择偏误
# 2. 简单透明：不需要复杂计量假设
# 3. 可测量具体政策效果
# 4. 为政策制定提供证据
#
# 【RCT的局限】
# 1. 外部有效性：结果能否推广到其他情境？
# 2. 霍桑效应：被观察可能改变行为
# 3. 溢出效应：对照组可能间接受影响
# 4. 实施成本：设计和实施昂贵
# 5. 伦理考量：是否可以拒绝给某些人提供可能有益的干预？
#
# 【RCT设计要素】
#
# 1. 随机分配（Randomization）
#    - 简单随机：每个单位独立随机分配
#    - 分层随机：在每个层（如地区、性别）内分别随机
#    - 聚类随机：以群组（如村庄、学校）为单位随机
#
# 2. 样本量计算（Power Analysis）
#    - 确保能检测到有意义的效应
#    - 考虑预期效应大小、变异程度、显著性水平
#
# 3. 对照组选择
#    - 纯对照：不接受任何干预
#    - 安慰剂对照：接受"假"干预
#    - 比较对照：接受替代干预
#
# 4. 意向处理分析（ITT）
#    - 按分配分析，不管实际是否接受处理
#    - 保持随机化的好处
#
# 【发展中国家的著名RCT】
#
# 1. 条件现金转移（墨西哥 PROGRESA）
#    - 评估CCT对入学、健康的影响
#
# 2. 学校去虫（肯尼亚）
#    - Miguel & Kremer (2004)
#    - 发现强大的正外溢效应
#
# 3. 小额信贷（多国）
#    - Banerjee et al. (2015)
#    - 发现效果不如预期
#
# 4. 蚊帐（肯尼亚）
#    - Cohen & Dupas (2010)
#    - 免费发放 vs 收费发放
#
# 【伦理考量】
# 1. 知情同意：参与者了解试验性质
# 2. 最小伤害：不造成不必要伤害
# 3. 公平分配：考虑对照组的福利
# 4. 审查委员会批准
#
# 任务：
# 1. 设计RCT的随机化方案
# 2. 计算所需样本量
# 3. 分析RCT结果（ITT、TOT）
#
# HINT1: 功效分析决定样本量——太小会错过真实效应
# HINT2: ITT分析保持随机化好处，即使有不服从
# HINT3: 聚类随机需要更大样本（设计效应）

import numpy as np
from typing import Optional


def simple_randomization(
    n_subjects: int,
    treatment_probability: float = 0.5
) -> np.ndarray:
    """
    简单随机分配。

    【理论背景】
    简单随机化是最基本的随机分配方法。
    每个研究对象独立地以固定概率被分配到处理组。

    【方法】
    对每个受试者 i：
    T_i = 1 如果 U_i < p，否则 T_i = 0

    其中 U_i ~ Uniform(0,1)，p是处理概率

    【优缺点】
    优点：
    - 实施简单
    - 不需要关于受试者的信息

    缺点：
    - 处理组和对照组大小可能不平衡
    - 小样本时可能产生协变量不平衡

    【何时使用】
    - 样本量大（>100）
    - 不担心组间不平衡
    - 没有明确的分层变量

    参数:
        n_subjects: 受试者数量
            - 例：1000个农户
            - 应足够大以保证统计功效
        treatment_probability: 处理概率（默认0.5）
            - 0.5：处理组和对照组大小相等
            - 可以不等，如0.7表示70%进入处理组
            - 例：0.5

    返回:
        处理分配向量（1=处理组，0=对照组）
        形状：(n_subjects,)

    示例:
        1000人试验，50%处理概率
        >>> np.random.seed(42)
        >>> assignment = simple_randomization(1000, 0.5)
        >>> assignment[:10]
        array([0, 1, 0, 0, 0, 0, 1, 1, 1, 1])
        >>> np.mean(assignment)
        0.512  # 约51.2%进入处理组

        小样本可能不平衡
        >>> assignment = simple_randomization(20, 0.5)
        >>> np.sum(assignment)
        可能是8, 9, 10, 11, 12...不一定是10

        处理概率不等
        >>> assignment = simple_randomization(1000, 0.7)
        >>> np.mean(assignment)
        约0.70

    注意:
        1. 每次调用结果不同（随机性）
        2. 小样本时考虑使用分层随机
        3. 应检验随机化的平衡性
    """
    # TODO: 实现简单随机分配
    # 提示：
    # 1. 生成n_subjects个[0,1)均匀分布随机数
    # 2. 将小于treatment_probability的设为1，否则设为0
    # 可以使用：
    # np.random.random(n_subjects) < treatment_probability
    # 并转换为整数
    pass


def stratified_randomization(
    n_subjects: int,
    strata: np.ndarray,
    treatment_probability: float = 0.5
) -> np.ndarray:
    """
    分层随机分配。

    【理论背景】
    分层随机化（Stratified Randomization）在每个层（stratum）内分别进行随机分配。
    层通常按重要的协变量（如性别、地区、收入水平）定义。

    【目的】
    1. 确保每层内处理组和对照组比例平衡
    2. 提高估计精度
    3. 便于子群分析

    【方法】
    对每个层 j：
    在层 j 内独立进行简单随机化

    【优缺点】
    优点：
    - 保证层内平衡
    - 可以分层估计处理效应
    - 减少偶然的协变量不平衡

    缺点：
    - 需要事先知道分层变量
    - 层数过多可能导致某些层样本太小

    【发展研究中的常见分层变量】
    - 地区/村庄
    - 性别
    - 基线收入水平
    - 学校/诊所

    参数:
        n_subjects: 受试者数量
            - 例：1000
        strata: 层标识数组
            - 形状：(n_subjects,)
            - 例：np.array([0, 0, 1, 1, 0, 2, 2, ...])
            - 0=农村, 1=城镇, 2=城市
        treatment_probability: 处理概率（默认0.5）
            - 例：0.5

    返回:
        处理分配向量（1=处理组，0=对照组）

    示例:
        按地区分层
        >>> np.random.seed(42)
        >>> strata = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 5人农村，5人城市
        >>> assignment = stratified_randomization(10, strata, 0.5)

        检验层内平衡
        >>> assignment[strata == 0].sum()  # 农村处理人数
        约2-3（从5人中）
        >>> assignment[strata == 1].sum()  # 城市处理人数
        约2-3（从5人中）

        大样本示例
        >>> n = 1000
        >>> strata = np.random.choice([0, 1, 2], n, p=[0.5, 0.3, 0.2])
        >>> assignment = stratified_randomization(n, strata, 0.5)
        >>> for s in [0, 1, 2]:
        ...     print(f"层{s}: {np.mean(assignment[strata==s]):.2f}")
        每层处理比例应接近0.5

    注意:
        1. 分层变量应在基线测量
        2. 太多层可能适得其反
        3. 分析时应使用分层标准误
    """
    # TODO: 实现分层随机分配
    # 提示：
    # 1. 初始化分配向量
    # 2. 找出所有唯一的层
    # 3. 对每个层内的受试者分别进行简单随机化
    # 伪代码：
    # assignment = np.zeros(n_subjects, dtype=int)
    # for s in np.unique(strata):
    #     mask = (strata == s)
    #     n_in_stratum = np.sum(mask)
    #     assignment[mask] = (np.random.random(n_in_stratum) < treatment_probability).astype(int)
    pass


def required_sample_size(
    effect_size: float,
    baseline_mean: float,
    baseline_std: float,
    alpha: float = 0.05,
    power: float = 0.8,
    treatment_share: float = 0.5
) -> int:
    """
    计算所需样本量。

    【理论背景】
    功效分析（Power Analysis）确定检验假设所需的最小样本量。
    样本太小会导致无法检测到真实存在的效应（Type II错误）。

    【关键概念】
    - 效应大小（Effect Size）：处理效应的预期大小
    - 显著性水平（α）：Type I错误概率（通常0.05）
    - 检验功效（Power = 1-β）：检测到真实效应的概率（通常0.80）

    【样本量公式】
    对于比较两组均值的t检验：

    n = 2 × (z_α/2 + z_β)² × σ² / δ²

    其中：
    - z_α/2: 双侧显著性水平对应的z值（α=0.05时约1.96）
    - z_β: 功效对应的z值（power=0.80时约0.84）
    - σ: 标准差
    - δ: 预期效应大小

    考虑处理比例不等时：
    n = (z_α/2 + z_β)² × σ² × (1/p + 1/(1-p)) / δ²

    其中p是处理组比例

    【发展研究中的考虑】
    - 聚类设计需要更大样本（设计效应）
    - 损耗率需要额外考虑
    - 多重比较需要调整α

    参数:
        effect_size: 预期效应大小（绝对值）
            - 处理组和对照组均值差
            - 例：入学率从70%提高到80%，效应=0.10
        baseline_mean: 基线均值
            - 对照组预期均值
            - 例：0.70（70%入学率）
        baseline_std: 基线标准差
            - 结果变量的标准差
            - 例：0.46（二元变量标准差）
        alpha: 显著性水平（默认0.05）
            - Type I错误率
            - 0.05, 0.01, 0.10常用
        power: 检验功效（默认0.80）
            - 1 - Type II错误率
            - 0.80, 0.90常用
        treatment_share: 处理组比例（默认0.5）
            - 0.5最有效率
            - 可能因实际限制而不等

    返回:
        所需总样本量（整数）

    示例:
        评估CCT对入学率的影响
        基线入学率70%，预期提高10个百分点
        >>> required_sample_size(0.10, 0.70, 0.46, 0.05, 0.80, 0.5)
        334

        解释：需要约334人（167处理+167对照）

        小效应需要更大样本
        >>> required_sample_size(0.05, 0.70, 0.46, 0.05, 0.80, 0.5)
        约1300人

        更高功效需要更大样本
        >>> required_sample_size(0.10, 0.70, 0.46, 0.05, 0.90, 0.5)
        约450人

        处理组比例不等
        >>> required_sample_size(0.10, 0.70, 0.46, 0.05, 0.80, 0.7)
        约360人（比50-50分配需要更多）

    注意:
        1. 这是简化公式，实际设计可能更复杂
        2. 聚类随机需要考虑组内相关性
        3. 应预留损耗空间（如增加20%）
    """
    # TODO: 计算所需样本量
    # 提示：
    # 1. 获取z值（可以使用正态分布分位数）
    #    from scipy.stats import norm
    #    z_alpha = norm.ppf(1 - alpha/2)  # 双侧检验
    #    z_beta = norm.ppf(power)
    # 或使用近似值：alpha=0.05时z_alpha≈1.96，power=0.80时z_beta≈0.84
    #
    # 2. 应用公式
    #    n = (z_alpha + z_beta)² × σ² × (1/p + 1/(1-p)) / δ²
    #
    # 3. 向上取整
    pass


def minimum_detectable_effect(
    sample_size: int,
    baseline_std: float,
    alpha: float = 0.05,
    power: float = 0.8,
    treatment_share: float = 0.5
) -> float:
    """
    最小可检测效应（MDE）。

    【理论背景】
    MDE是给定样本量下能够检测到的最小效应大小。
    是样本量公式的逆运算。

    【公式推导】
    从样本量公式：
    n = (z_α/2 + z_β)² × σ² × (1/p + 1/(1-p)) / δ²

    解出 δ（效应）：
    δ = (z_α/2 + z_β) × σ × sqrt((1/p + 1/(1-p)) / n)

    【应用场景】
    1. 评估现有试验能否检测到有意义的效应
    2. 在样本量固定时评估试验可行性
    3. 与预期效应比较，判断是否值得进行试验

    【解读MDE】
    如果 MDE > 预期效应 → 样本量不足
    如果 MDE < 预期效应 → 有足够功效

    参数:
        sample_size: 总样本量
            - 处理组和对照组总和
            - 例：500
        baseline_std: 基线标准差
            - 例：0.46
        alpha: 显著性水平（默认0.05）
        power: 检验功效（默认0.80）
        treatment_share: 处理组比例（默认0.5）

    返回:
        最小可检测效应

    示例:
        评估现有样本能检测多大效应
        >>> minimum_detectable_effect(500, 0.46, 0.05, 0.80, 0.5)
        0.081

        解释：500人样本只能检测到8.1个百分点的入学率变化

        如果预期效应只有5个百分点
        >>> mde = minimum_detectable_effect(500, 0.46, 0.05, 0.80, 0.5)
        0.081 > 0.05
        # 样本量不足，可能错过真实效应！

        增加样本量
        >>> minimum_detectable_effect(1000, 0.46, 0.05, 0.80, 0.5)
        0.057  # 能检测到更小的效应

    注意:
        1. MDE是"刚好能检测到"的效应，实际效应应大于MDE
        2. 标准差估计很关键
        3. 聚类设计需要调整
    """
    # TODO: 计算最小可检测效应
    # 提示：
    # 使用z值近似：z_alpha ≈ 1.96（α=0.05），z_beta ≈ 0.84（power=0.80）
    # MDE = (z_alpha + z_beta) × σ × sqrt((1/p + 1/(1-p)) / n)
    pass


def intention_to_treat(
    y: np.ndarray,
    assignment: np.ndarray
) -> tuple[float, float]:
    """
    意向处理分析（ITT）。

    【理论背景】
    ITT分析按随机分配分组进行分析，而非按实际接受处理分组。
    即使有人没有实际接受处理（不服从），仍按分配分析。

    【为什么用ITT？】
    1. 保持随机化：随机分配保证两组可比，按实际接受分组破坏这一点
    2. 政策相关：反映实际政策效果（包括不服从的现实）
    3. 避免选择偏误：实际接受与否可能与结果相关

    【ITT估计量】
    ITT = E[Y | Z=1] - E[Y | Z=0]

    其中 Z 是分配（非实际接受）

    【ITT vs ATE】
    - ITT: 分配的效应（包括不服从）
    - ATE (Average Treatment Effect): 实际接受的效应
    - 如果有不服从，ITT < ATE

    【标准误计算】
    SE = sqrt(Var(Y|Z=1)/n₁ + Var(Y|Z=0)/n₀)

    参数:
        y: 结果变量数组
            - 形状：(n,)
            - 例：np.array([1, 0, 1, 0, 1, 0, 1, 1, ...])（入学=1）
        assignment: 随机分配数组
            - 形状：(n,)
            - 1=分配到处理组，0=分配到对照组
            - 注意：这是分配，不是实际接受

    返回:
        (ITT效应, 标准误)

    示例:
        完美服从情况
        >>> np.random.seed(42)
        >>> y = np.array([1, 1, 1, 0, 1, 0, 0, 0, 1, 0])
        >>> assignment = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        >>> intention_to_treat(y, assignment)
        (0.4, 0.28)

        计算：
        处理组均值：(1+1+1+0+1)/5 = 0.8
        对照组均值：(0+0+0+1+0)/5 = 0.2
        ITT = 0.8 - 0.2 = 0.6

        实际研究示例（模拟）
        >>> n = 1000
        >>> assignment = simple_randomization(n, 0.5)
        >>> # 处理效应 = 0.10，基线 = 0.70
        >>> y0 = np.random.binomial(1, 0.70, n)  # 对照组潜在结果
        >>> y1 = np.random.binomial(1, 0.80, n)  # 处理组潜在结果
        >>> y = assignment * y1 + (1 - assignment) * y0
        >>> itt, se = intention_to_treat(y, assignment)
        约 (0.10, 0.03)

    注意:
        1. ITT是政策评估的首选方法
        2. 如果关心"实际接受处理"的效应，需要TOT分析
        3. 应检验基线平衡
    """
    # TODO: 实现ITT分析
    # 提示：
    # 1. 计算处理组均值：y[assignment == 1].mean()
    # 2. 计算对照组均值：y[assignment == 0].mean()
    # 3. ITT = 处理组均值 - 对照组均值
    # 4. 计算标准误：
    #    var_t = np.var(y[assignment == 1], ddof=1)
    #    var_c = np.var(y[assignment == 0], ddof=1)
    #    n_t = np.sum(assignment == 1)
    #    n_c = np.sum(assignment == 0)
    #    se = np.sqrt(var_t/n_t + var_c/n_c)
    pass


def treatment_on_treated(
    y: np.ndarray,
    assignment: np.ndarray,
    takeup: np.ndarray
) -> tuple[float, float]:
    """
    处理组效应（TOT/LATE）。

    【理论背景】
    TOT（Treatment on the Treated）或LATE（Local Average Treatment Effect）
    估计的是实际接受处理者的效应。

    当存在不服从（non-compliance）时：
    - ITT低估了处理对接受者的效应
    - TOT使用分配作为工具变量（IV）

    【IV/2SLS方法】
    第一阶段：D = α + π×Z + ε  （D=实际接受，Z=分配）
    第二阶段：Y = β + τ×D̂ + u

    TOT = ITT / (服从率)
        = [E(Y|Z=1) - E(Y|Z=0)] / [E(D|Z=1) - E(D|Z=0)]

    【LATE的解读】
    LATE是"服从者"（Compliers）的效应：
    - 如果分配到处理就接受
    - 如果分配到对照就不接受

    不包括：
    - 总是接受者（Always-takers）
    - 从不接受者（Never-takers）

    【排他性假设】
    分配只通过实际接受影响结果

    参数:
        y: 结果变量数组
            - 形状：(n,)
        assignment: 随机分配数组
            - 形状：(n,)
            - 1=分配到处理组
        takeup: 实际接受处理数组
            - 形状：(n,)
            - 1=实际接受处理
            - 可能与分配不同（不服从）

    返回:
        (TOT效应, 标准误)

    示例:
        存在不服从的情况
        >>> y = np.array([1, 1, 0, 1, 1, 0, 0, 1, 0, 0])
        >>> assignment = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        >>> takeup = np.array([1, 1, 0, 1, 1, 0, 0, 1, 0, 0])  # 第3和第8人不服从
        >>> treatment_on_treated(y, assignment, takeup)

        计算：
        ITT = (处理分配组均值) - (对照分配组均值)
        服从率 = (处理分配组接受率) - (对照分配组接受率)
        TOT = ITT / 服从率

        高不服从率
        如果服从率只有50%，且ITT=0.10
        TOT = 0.10 / 0.50 = 0.20
        实际接受者的效应是ITT的两倍

    注意:
        1. TOT > ITT（当存在不服从时）
        2. TOT假设排他性（分配只通过接受影响结果）
        3. 标准误会更大（因为IV估计）
        4. 如果服从率接近0，TOT估计不稳定
    """
    # TODO: 实现TOT分析
    # 提示：
    # 1. 计算ITT：处理分配组均值 - 对照分配组均值
    # 2. 计算服从率：
    #    处理分配组接受率 - 对照分配组接受率
    #    = takeup[assignment==1].mean() - takeup[assignment==0].mean()
    # 3. TOT = ITT / 服从率
    # 4. 标准误可以使用bootstrap或渐近公式
    #    简化：SE_TOT ≈ SE_ITT / 服从率
    pass


def balance_test(
    covariates: np.ndarray,
    treatment: np.ndarray
) -> dict:
    """
    协变量平衡检验。

    【理论背景】
    平衡检验检查处理组和对照组在基线特征上是否平衡。
    如果随机化正确执行，两组应在所有协变量上（平均）相同。

    【为什么做平衡检验？】
    1. 验证随机化：检测随机化实施错误
    2. 展示可信度：向读者证明两组可比
    3. 识别需要控制的变量

    【检验方法】
    对每个协变量：
    - 计算两组均值差
    - 进行t检验
    - 报告p值

    联合检验：
    - F检验所有协变量的联合平衡
    - 单个变量可能偶然不平衡

    【注意】
    - 即使随机化正确，5%的变量预期在5%水平上"不平衡"
    - 应看整体pattern，而非单个变量
    - 事后控制"不平衡"变量有争议

    参数:
        covariates: 协变量矩阵
            - 形状：(n_subjects, n_covariates)
            - 例：年龄、性别、基线收入等
        treatment: 处理分配
            - 形状：(n_subjects,)
            - 0/1数组

    返回:
        字典包含：
        - 'means_diff': 均值差数组
        - 'p_values': 每个协变量的p值
        - 'joint_test': 联合F检验的p值

    示例:
        检验3个协变量的平衡
        >>> np.random.seed(42)
        >>> n = 200
        >>> treatment = simple_randomization(n, 0.5)
        >>> age = np.random.normal(35, 10, n)
        >>> income = np.random.normal(5000, 2000, n)
        >>> female = np.random.binomial(1, 0.5, n)
        >>> covariates = np.column_stack([age, income, female])
        >>> result = balance_test(covariates, treatment)
        >>> result
        {
            'means_diff': array([0.5, -150, 0.02]),  # 小差异
            'p_values': array([0.72, 0.58, 0.85]),   # 都不显著
            'joint_test': 0.65  # 联合检验不显著
        }

        不平衡的例子（随机化可能有问题）
        如果某个p值 < 0.05，应调查原因

    注意:
        1. 平衡检验不能"证明"随机化正确，只能检测明显问题
        2. 即使平衡，分析时也可以控制协变量以提高精度
        3. 应在事前（基线）数据上进行
    """
    # TODO: 实现平衡检验
    # 提示：
    # 1. 对每个协变量计算两组均值差
    # 2. 进行t检验（可以使用scipy.stats.ttest_ind）
    # 3. 联合检验可以用F检验（logistic回归treatment~covariates的似然比检验）
    #
    # 简化版本（不用scipy）：
    # means_diff = [cov[treatment==1].mean() - cov[treatment==0].mean() for each cov]
    # p_values: 使用t统计量近似（假设正态）
    pass


def attrition_analysis(
    baseline_n: int,
    endline_n: int,
    treatment: np.ndarray,
    attrited: np.ndarray
) -> dict:
    """
    样本损耗分析。

    【理论背景】
    样本损耗（Attrition）是纵向研究的常见问题。
    如果损耗与处理相关，会导致估计偏误。

    【损耗的类型】
    1. 随机损耗：与处理无关（仍可无偏估计，但精度降低）
    2. 差异性损耗：处理组和对照组损耗率不同（可能有偏）
    3. 选择性损耗：特定类型人群更可能损耗（可能有偏）

    【分析步骤】
    1. 计算总损耗率
    2. 检验差异性损耗（处理组 vs 对照组）
    3. 如果差异性损耗存在，进行敏感性分析

    【Lee边界】
    Lee (2009) 提出的边界估计：
    假设损耗由处理导致，通过截断数据得到效应的上下界

    如果处理组损耗更多：
    - 下界：假设损耗的是处理组中结果最好的人
    - 上界：假设损耗的是处理组中结果最差的人

    参数:
        baseline_n: 基线样本量
            - 研究开始时的样本
            - 例：1000
        endline_n: 终线样本量
            - 完成后续调查的样本
            - 例：850
        treatment: 处理分配（基线时）
            - 形状：(baseline_n,)
        attrited: 损耗指示
            - 形状：(baseline_n,)
            - 1=损耗，0=留存

    返回:
        字典包含：
        - 'attrition_rate': 总损耗率
        - 'differential_attrition': 差异损耗（处理组-对照组）
        - 'lee_bounds': Lee边界估计（如果适用）

    示例:
        低损耗
        >>> baseline_n = 1000
        >>> endline_n = 950
        >>> treatment = simple_randomization(1000, 0.5)
        >>> attrited = np.random.binomial(1, 0.05, 1000)  # 5%随机损耗
        >>> attrition_analysis(baseline_n, endline_n, treatment, attrited)
        {
            'attrition_rate': 0.05,
            'differential_attrition': 0.01,  # 接近0
            'lee_bounds': None  # 差异不显著，不需要
        }

        差异性损耗
        处理组损耗15%，对照组损耗5%
        >>> # 假设处理组损耗率更高
        >>> attrition_rate_t = 0.15
        >>> attrition_rate_c = 0.05
        >>> attrited = np.where(treatment == 1,
        ...     np.random.binomial(1, 0.15, 1000),
        ...     np.random.binomial(1, 0.05, 1000))
        >>> result = attrition_analysis(...)
        'differential_attrition': 0.10  # 需要关注！

    注意:
        1. 差异性损耗可能导致偏误
        2. 应分析损耗者的特征
        3. 严重损耗时结果可能不可信
        4. 设计时应最小化损耗
    """
    # TODO: 实现样本损耗分析
    # 提示：
    # 1. 总损耗率 = np.mean(attrited)
    # 2. 处理组损耗率 = attrited[treatment==1].mean()
    # 3. 对照组损耗率 = attrited[treatment==0].mean()
    # 4. 差异损耗 = 处理组损耗率 - 对照组损耗率
    # 5. Lee边界需要更复杂的计算（可选实现）
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
