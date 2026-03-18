# EXERCISE: public_choice1
# DIFFICULTY: ★★★★☆
# TOPIC: 公共选择理论
#
# ============================================================================
#                            公共选择理论 (Public Choice Theory)
# ============================================================================
#
# 一、理论背景与发展
# ============================================================================
# 公共选择理论是用经济学方法研究政治决策过程的学科，主要创始人包括：
# - James Buchanan（布坎南）：1986年诺贝尔经济学奖得主，强调宪政经济学
# - Gordon Tullock（图洛克）：寻租理论的奠基人
# - Kenneth Arrow（阿罗）：1972年诺贝尔奖，提出不可能定理
# - Anthony Downs（唐斯）：《民主的经济理论》，理性选民模型
# - William Niskanen（尼斯卡宁）：官僚行为理论
#
# 核心假设（方法论个人主义）：
# 1. 理性人假设：政治参与者（选民、政治家、官僚）都是追求自身利益最大化的理性人
# 2. 交换范式：政治过程可以视为一种交换过程，类似于市场交易
# 3. 规则重要性：制度规则决定了政治博弈的结果
#
# 二、核心概念与理论
# ============================================================================
#
# 1. 投票理论 (Voting Theory)
# ----------------------------
# (1) 多数票规则 (Majority Rule)
#     - 简单多数：获得超过半数选票即当选
#     - 绝对多数：获得超过某个阈值（如2/3）选票
#     - 相对多数：获得最多选票即当选（不要求过半）
#
# (2) 孔多塞获胜者 (Condorcet Winner)
#     定义：在所有两两对决中都能获胜的候选人
#     例如：有A、B、C三个候选人，如果A vs B中A获胜，A vs C中A也获胜，
#          则A是孔多塞获胜者
#     特点：孔多塞获胜者不一定存在（可能出现循环）
#
# (3) 投票悖论 (Voting Paradox / Condorcet Paradox)
#     当存在三个或以上选项时，多数票规则可能产生循环：
#     例如：三个选民对A、B、C的偏好为
#           选民1: A > B > C
#           选民2: B > C > A
#           选民3: C > A > B
#     结果：A vs B: A获胜(2:1)
#           B vs C: B获胜(2:1)
#           C vs A: C获胜(2:1)
#     形成循环：A > B > C > A，无稳定均衡
#
# (4) 阿罗不可能定理 (Arrow's Impossibility Theorem)
#     不存在满足以下条件的社会选择规则：
#     - 非独裁性：没有人的偏好总是决定社会偏好
#     - 帕累托效率：如果所有人都偏好A胜过B，社会也应偏好A胜过B
#     - 独立性：对A和B的社会排序只依赖于个人对A和B的排序
#     - 传递性：社会偏好应满足传递性（A>B且B>C则A>C）
#     - 无限制域：适用于所有可能的个人偏好组合
#
# 2. 中位选民定理 (Median Voter Theorem)
# ----------------------------
# 前提条件：
# - 单峰偏好 (Single-peaked preferences)：每个选民有一个最偏好的点，
#   偏离该点效用单调下降
# - 一维政策空间：政策可以排列在一条线上
# - 两党竞争：两个候选人/政党在政策空间上选择位置
#
# 定理内容：
# 在满足上述条件下，均衡政策是中位选民的理想点
#
# 数学表达：
# 设选民理想点为 x₁ ≤ x₂ ≤ ... ≤ xₙ
# 中位选民的理想点 x_median = x_{(n+1)/2}（n为奇数时）
#                         = (x_{n/2} + x_{n/2+1})/2（n为偶数时）
#
# 直觉解释：
# 任何偏离中位点的政策都会被更接近中位点的政策击败，
# 因为中位选民加上同侧的选民构成多数
#
# 例如：5个选民的理想点为 [1, 3, 5, 7, 9]
#       中位选民理想点 = 5
#       政策5将在与任何其他政策的对决中获胜
#
# 3. 单峰偏好 (Single-peaked Preferences)
# ----------------------------
# 定义：选民的效用函数在政策空间上只有一个峰值
#
# 数学表达：
# 对于选民i，其效用函数u_i(x)满足：
# 存在理想点x*，使得对于所有x₁ < x₂ ≤ x* 或 x* ≤ x₂ < x₁
# 有 u_i(x₂) > u_i(x₁)
#
# 例如：效用函数 u(x) = -(x - x*)² 是单峰的
#
# 单峰偏好的重要性：
# - 保证中位选民定理成立
# - 避免投票循环
# - 确保稳定的政治均衡
#
# 非单峰偏好的例子：
# 某选民对教育支出的偏好可能是：高支出 > 低支出 > 中等支出
# （要么公立教育好，要么干脆让私立学校发展）
#
# 4. 寻租理论 (Rent-Seeking Theory)
# ----------------------------
# 定义：个人或组织花费资源去获取政府创造的特权或租金，
#       而不是通过生产性活动创造价值
#
# 寻租的例子：
# - 游说政府获取垄断许可
# - 争取贸易保护（关税、配额）
# - 争取政府补贴
# - 争取政府合同
#
# 寻租的社会成本：
# (1) 直接寻租支出：用于游说、贿赂、公关的资源
# (2) 防租支出：反对寻租的资源（如消费者团体的游说）
# (3) 资源错配：租金导致的生产扭曲
# (4) 寻租竞争的扭曲：优秀人才从事非生产性活动
#
# 图洛克的"社会成本"观点：
# 完全竞争的寻租会耗散全部租金价值
# 即：寻租支出总和 → 租金价值
#
# 5. 图洛克寻租博弈 (Tullock Rent-Seeking Game)
# ----------------------------
# 博弈设定：
# - n个参与者竞争价值为V的租金
# - 参与者i投入努力e_i
# - 获胜概率（比赛成功函数）：p_i = e_i / Σe_j
#
# 期望收益：
# E[π_i] = p_i × V - e_i = (e_i / Σe_j) × V - e_i
#
# 纳什均衡：
# 对称均衡中：e* = V(n-1)/n²
# 总寻租支出：n × e* = V(n-1)/n
# 当n→∞时，总支出→V（完全耗散）
#
# 6. 官僚行为理论 (Bureaucratic Behavior)
# ----------------------------
# 尼斯卡宁模型 (Niskanen Model)：
# 假设官僚追求预算最大化（而非社会福利最大化）
#
# 设定：
# - 需求函数：P(Q) = a - bQ（公众对公共服务的边际支付意愿）
# - 成本函数：TC(Q) = cQ（边际成本恒定为c）
# - 政治家只观察到总收益和总成本
#
# 官僚的策略：
# 选择产出Q使得总收益 = 总成本
# 即：∫₀^Q P(q)dq = TC(Q)
#     aQ - bQ²/2 = cQ
#     Q* = 2(a-c)/b（预算最大化产出）
#
# 效率产出（边际收益=边际成本）：
# a - bQ = c
# Q_eff = (a-c)/b
#
# 结论：官僚产出是效率产出的两倍，存在过度供给
#
# 7. 滚木立法 (Log-rolling)
# ----------------------------
# 定义：立法者之间的投票交易，互相支持对方的法案
#
# 机制：
# - 项目A只对立法者甲有利，项目B只对立法者乙有利
# - 单独投票，两个项目都无法通过（各只有1票支持）
# - 通过交易：甲支持B，乙支持A，两个项目都能通过
#
# 效率分析：
# - 可能提高效率：如果项目总收益超过总成本
# - 可能降低效率：如果少数人受益但成本由全体分摊
#
# 例如：
# 项目成本100万，由100人平均分摊（每人1万）
# 项目收益30万，归5个人（每人6万）
# 净收益：-70万（无效率）
# 但5个受益者每人净获益5万，愿意游说
# 每个纳税人只损失1万，缺乏反对动力（理性无知）
#
# 三、模型假设与局限
# ============================================================================
# 1. 理性选民假设可能过强（许多选民不完全理性或信息不完全）
# 2. 政治企业家的作用被忽视（领袖可以改变偏好和议程）
# 3. 意识形态和价值观的影响被低估
# 4. 制度细节很重要（不同的投票规则产生不同结果）
# 5. 实验和实证研究对某些预测提出质疑
#
# 四、学习目标
# ============================================================================
# 1. 理解投票规则的性质和局限性
# 2. 掌握中位选民定理及其应用条件
# 3. 理解寻租的社会成本
# 4. 分析官僚行为和政府失灵
# 5. 理解政治市场与经济市场的异同
#
# ============================================================================

import numpy as np


def majority_winner(
    preferences: np.ndarray
) -> int:
    """
    多数票规则的获胜者。

    基本原理：
    ----------
    多数票规则是最常见的集体决策规则。在两两对决中，获得超过半数选票的
    选项获胜。但当有三个或以上选项时，可能出现循环（孔多塞悖论）。

    偏好矩阵表示：
    ----------
    preferences[i, j] = k 表示选民i把选项k排在第j位
    例如：preferences[0] = [2, 0, 1] 表示选民0的偏好为：选项2 > 选项0 > 选项1

    算法（简单多数，第一轮）：
    ----------
    统计每个选项获得的第一名票数，获得最多第一名的选项获胜
    如果存在平局或循环，返回-1

    参数详解：
    ----------
    preferences : np.ndarray
        偏好矩阵，形状为 (n_voters, n_alternatives)
        - n_voters: 选民数量
        - n_alternatives: 候选方案数量
        - preferences[i, j] = k: 选民i的第j偏好是选项k（j从0开始，0是最偏好）

        示例：3个选民，3个选项
        preferences = np.array([
            [0, 1, 2],  # 选民0: 0 > 1 > 2
            [1, 2, 0],  # 选民1: 1 > 2 > 0
            [0, 2, 1]   # 选民2: 0 > 2 > 1
        ])

    返回值：
    ----------
    int : 获胜方案的编号
        - 返回获得最多第一名票数的选项编号
        - 如果存在平局，返回 -1

    数值示例：
    ----------
    例1：明确获胜者
    >>> preferences = np.array([
    ...     [0, 1, 2],  # 选民0首选0
    ...     [0, 2, 1],  # 选民1首选0
    ...     [1, 0, 2]   # 选民2首选1
    ... ])
    >>> majority_winner(preferences)
    0  # 选项0获得2票第一名，选项1获得1票

    例2：平局
    >>> preferences = np.array([
    ...     [0, 1, 2],  # 选民0首选0
    ...     [1, 0, 2],  # 选民1首选1
    ...     [2, 0, 1],  # 选民2首选2
    ...     [0, 2, 1]   # 选民3首选0
    ... ])
    >>> majority_winner(preferences)
    0  # 选项0获得2票，选项1获得1票，选项2获得1票

    TODO提示：
    ----------
    1. 获取选民数量n_voters和选项数量n_alternatives
       n_voters, n_alternatives = preferences.shape

    2. 统计每个选项获得的第一名票数
       first_choices = preferences[:, 0]  # 每个选民的第一选择
       使用 np.bincount 或循环统计每个选项的票数

    3. 找出票数最多的选项
       winner = np.argmax(vote_counts)

    4. 检查是否有平局（多个选项获得相同最高票数）
       max_votes = vote_counts[winner]
       if np.sum(vote_counts == max_votes) > 1:
           return -1

    5. 返回获胜者编号
    """
    # TODO: 多数票获胜者
    pass


def condorcet_winner(
    preferences: np.ndarray
) -> int:
    """
    孔多塞获胜者（在所有两两对决中都能获胜的选项）。

    基本原理：
    ----------
    孔多塞获胜者是指在所有成对比较中都能获得多数支持的选项。
    如果存在，孔多塞获胜者被认为是"真正的"多数偏好。

    数学定义：
    ----------
    选项x是孔多塞获胜者，当且仅当：
    对于所有其他选项y，在x vs y的对决中，偏好x胜过y的选民超过半数

    形式化：∀y≠x, |{i: x >_i y}| > n/2
    其中 >_i 表示选民i的偏好关系

    判断方法：
    ----------
    1. 对每对选项(x, y)，统计偏好x胜过y的选民数
    2. 构建"获胜矩阵"W，W[x,y] = 1 如果x击败y，否则为0
    3. 如果某选项x的W[x,:]全为1（除了W[x,x]），则x是孔多塞获胜者

    参数详解：
    ----------
    preferences : np.ndarray
        偏好矩阵，形状为 (n_voters, n_alternatives)
        preferences[i, j] = k: 选民i的第j偏好是选项k

        在偏好排序中，位置靠前的选项更被偏好：
        如果 preferences[i] = [2, 0, 1]
        则选民i的偏好为：2 > 0 > 1

    返回值：
    ----------
    int : 孔多塞获胜者的编号
        - 如果存在孔多塞获胜者，返回其编号
        - 如果不存在（存在循环），返回 -1

    数值示例：
    ----------
    例1：存在孔多塞获胜者
    >>> preferences = np.array([
    ...     [0, 1, 2],  # 0 > 1 > 2
    ...     [0, 2, 1],  # 0 > 2 > 1
    ...     [1, 0, 2]   # 1 > 0 > 2
    ... ])
    >>> condorcet_winner(preferences)
    0
    # 验证：0 vs 1: 选民0和1偏好0，选民2偏好1 → 0获胜(2:1)
    #       0 vs 2: 选民0、1、2都偏好0胜过2 → 0获胜(3:0)
    #       所以0是孔多塞获胜者

    例2：不存在孔多塞获胜者（投票悖论）
    >>> preferences = np.array([
    ...     [0, 1, 2],  # 0 > 1 > 2
    ...     [1, 2, 0],  # 1 > 2 > 0
    ...     [2, 0, 1]   # 2 > 0 > 1
    ... ])
    >>> condorcet_winner(preferences)
    -1
    # 验证：0 vs 1: 选民0、2偏好0 → 0获胜
    #       1 vs 2: 选民0、1偏好1 → 1获胜
    #       2 vs 0: 选民1、2偏好2 → 2获胜
    #       循环：0 > 1 > 2 > 0

    TODO提示：
    ----------
    1. 获取选民数和选项数
       n_voters, n_alternatives = preferences.shape

    2. 创建函数判断选民i是否偏好x胜过y
       def prefers(voter_pref, x, y):
           # 在偏好列表中，位置靠前表示更偏好
           x_pos = np.where(voter_pref == x)[0][0]
           y_pos = np.where(voter_pref == y)[0][0]
           return x_pos < y_pos

    3. 对每个候选获胜者x，检查它是否击败所有其他选项
       for x in range(n_alternatives):
           is_condorcet = True
           for y in range(n_alternatives):
               if x == y:
                   continue
               # 统计偏好x胜过y的选民数
               votes_for_x = sum(prefers(preferences[i], x, y)
                                for i in range(n_voters))
               if votes_for_x <= n_voters / 2:
                   is_condorcet = False
                   break
           if is_condorcet:
               return x

    4. 如果没有找到，返回-1
    """
    # TODO: 孔多塞获胜者
    pass


def median_voter_outcome(
    voter_preferences: np.ndarray
) -> float:
    """
    中位选民定理：在单峰偏好下，均衡政策是中位选民的理想点。

    基本原理：
    ----------
    中位选民定理（Median Voter Theorem）由 Duncan Black 和 Anthony Downs 提出。
    在满足特定条件下，政治竞争的均衡结果将是中位选民的偏好。

    前提条件：
    ----------
    1. 单峰偏好：每个选民有唯一的理想点，偏离理想点效用下降
    2. 一维政策空间：政策可以在一条线上排序（如左右政治光谱）
    3. 两党竞争：两个候选人在政策空间上选择位置
    4. 选民投票给更接近自己理想点的候选人

    数学推导：
    ----------
    设n个选民的理想点为 x₁ ≤ x₂ ≤ ... ≤ xₙ

    中位数定义：
    - n为奇数时：x_median = x_{(n+1)/2}
    - n为偶数时：x_median = (x_{n/2} + x_{n/2+1}) / 2
      （任何在这个区间内的政策都是均衡）

    证明（两党竞争）：
    假设两个候选人A和B选择位置p_A和p_B，p_A < p_B
    - 所有理想点 < (p_A + p_B)/2 的选民投票给A
    - 所有理想点 > (p_A + p_B)/2 的选民投票给B

    如果p_A ≠ x_median，A可以通过向中位数移动获得更多选票
    因此，纳什均衡是 p_A = p_B = x_median

    参数详解：
    ----------
    voter_preferences : np.ndarray
        选民的理想点数组，一维数组
        - 每个元素表示一个选民在政策空间上的理想位置
        - 值越小表示越"左"，值越大表示越"右"

        示例：voter_preferences = np.array([1, 3, 5, 7, 9])
        表示5个选民的理想点分别为1, 3, 5, 7, 9

    返回值：
    ----------
    float : 均衡政策（中位选民的理想点）
        - 选民数为奇数时，返回中间那个选民的理想点
        - 选民数为偶数时，返回中间两个理想点的平均值

    数值示例：
    ----------
    例1：奇数个选民
    >>> voter_preferences = np.array([2, 4, 6, 8, 10])
    >>> median_voter_outcome(voter_preferences)
    6.0
    # 5个选民，中位数是第3个（排序后），即6

    例2：偶数个选民
    >>> voter_preferences = np.array([1, 3, 7, 9])
    >>> median_voter_outcome(voter_preferences)
    5.0
    # 4个选民，中位数是第2和第3个的平均：(3+7)/2 = 5

    例3：未排序的输入
    >>> voter_preferences = np.array([9, 1, 5, 3, 7])
    >>> median_voter_outcome(voter_preferences)
    5.0
    # 排序后 [1, 3, 5, 7, 9]，中位数是5

    例4：政治光谱应用
    >>> # 0=极左，100=极右
    >>> voter_preferences = np.array([20, 35, 45, 55, 60, 70, 80])
    >>> median_voter_outcome(voter_preferences)
    55.0
    # 两党都会向55这个位置靠拢

    TODO提示：
    ----------
    1. 使用 np.median() 函数直接计算中位数
       median = np.median(voter_preferences)
       return float(median)

    或者手动实现：
    2. 对选民偏好进行排序
       sorted_prefs = np.sort(voter_preferences)

    3. 计算中位数
       n = len(sorted_prefs)
       if n % 2 == 1:
           # 奇数个选民
           median = sorted_prefs[n // 2]
       else:
           # 偶数个选民
           median = (sorted_prefs[n//2 - 1] + sorted_prefs[n//2]) / 2

    4. 返回中位数
    """
    # TODO: 中位选民
    pass


def is_single_peaked(
    preferences: np.ndarray,
    policy_space: np.ndarray
) -> bool:
    """
    检验所有选民的偏好是否都是单峰的。

    基本原理：
    ----------
    单峰偏好（Single-peaked Preferences）是中位选民定理的关键前提。
    如果偏好是单峰的，多数投票规则将产生稳定的均衡。

    数学定义：
    ----------
    选民i的偏好是单峰的，当且仅当：
    存在理想点 x* ∈ X（政策空间），使得
    对于所有 x₁, x₂ ∈ X：
    如果 x₁ < x₂ ≤ x* 或 x* ≤ x₂ < x₁，则 u_i(x₂) > u_i(x₁)

    直观理解：
    从理想点向任一方向移动，效用单调下降，不会出现"先降后升"的情况

    检验方法：
    ----------
    1. 找到每个选民的理想点（效用最高的政策）
    2. 检查从理想点向左移动，效用是否单调下降
    3. 检查从理想点向右移动，效用是否单调下降
    4. 如果所有选民都满足，则偏好是单峰的

    参数详解：
    ----------
    preferences : np.ndarray
        效用函数值矩阵，形状为 (n_voters, n_policies)
        preferences[i, j] 表示选民i对政策j的效用值

        示例：3个选民，5个政策
        preferences = np.array([
            [1, 3, 5, 4, 2],  # 选民0的效用，理想点在政策2（效用5）
            [5, 4, 3, 2, 1],  # 选民1的效用，理想点在政策0（效用5）
            [1, 2, 3, 4, 5]   # 选民2的效用，理想点在政策4（效用5）
        ])

    policy_space : np.ndarray
        政策空间，一维数组，表示政策的位置（已排序）
        示例：policy_space = np.array([0, 1, 2, 3, 4])

    返回值：
    ----------
    bool : 是否所有选民的偏好都是单峰的
        - True: 所有选民的偏好都是单峰的
        - False: 至少有一个选民的偏好不是单峰的

    数值示例：
    ----------
    例1：单峰偏好
    >>> policy_space = np.array([0, 1, 2, 3, 4])
    >>> preferences = np.array([
    ...     [1, 3, 5, 4, 2],  # 峰在2
    ...     [5, 4, 3, 2, 1],  # 峰在0
    ...     [1, 2, 3, 4, 5]   # 峰在4
    ... ])
    >>> is_single_peaked(preferences, policy_space)
    True

    例2：非单峰偏好
    >>> policy_space = np.array([0, 1, 2, 3, 4])
    >>> preferences = np.array([
    ...     [5, 2, 3, 2, 5],  # 两个峰：在0和4
    ...     [1, 2, 3, 4, 5]   # 单峰
    ... ])
    >>> is_single_peaked(preferences, policy_space)
    False
    # 选民0的偏好有两个峰值（0和4都是局部最大）

    例3：教育支出的非单峰偏好
    # 有人偏好：高支出 > 低支出 > 中等支出
    # （要么公立教育好，要么让私立发展）
    >>> policy_space = np.array([0, 50, 100])  # 支出水平
    >>> preferences = np.array([
    ...     [4, 2, 5],  # 非单峰：100 > 0 > 50
    ... ])
    >>> is_single_peaked(preferences, policy_space)
    False

    TODO提示：
    ----------
    1. 遍历每个选民的效用函数
       for voter_utility in preferences:

    2. 找到该选民的理想点（效用最大的位置）
       peak_idx = np.argmax(voter_utility)

    3. 检查从理想点向左是否单调递减
       for j in range(peak_idx - 1, -1, -1):
           if voter_utility[j] > voter_utility[j + 1]:
               return False  # 左边不是单调递减

    4. 检查从理想点向右是否单调递减
       for j in range(peak_idx + 1, len(voter_utility)):
           if voter_utility[j] > voter_utility[j - 1]:
               return False  # 右边不是单调递减

    5. 如果所有选民都通过检验，返回True
    """
    # TODO: 单峰检验
    pass


def rent_seeking_loss(
    rent_value: float,
    n_seekers: int,
    expenditure_per_seeker: float
) -> float:
    """
    计算寻租活动造成的社会损失。

    基本原理：
    ----------
    寻租（Rent-seeking）是指个人或组织花费资源去获取由政府创造的特权或租金，
    而不是通过生产性活动创造价值。这是一种非生产性的再分配活动。

    寻租的例子：
    - 游说政府获取垄断许可
    - 争取贸易保护（关税、配额）
    - 争取政府补贴或税收优惠
    - 竞争政府合同

    社会损失的组成：
    ----------
    1. 直接寻租支出：用于游说、公关、法律费用等
       = n_seekers × expenditure_per_seeker

    2. 资源错配损失：租金本身导致的效率损失
       - 垄断导致的无谓损失
       - 保护导致的贸易扭曲
       - 补贴导致的过度生产

    3. 寻租竞争的扭曲：
       - 优秀人才从事非生产性活动
       - 创业精神被引向寻租而非创新

    数学表达：
    ----------
    简化模型中，社会损失 = 总寻租支出 + 租金价值的一部分
    total_loss = n_seekers × expenditure_per_seeker + α × rent_value

    其中α表示资源错配系数（简化模型中可取0或固定值）

    图洛克的完全耗散理论：
    在完全竞争的寻租中，均衡时总寻租支出趋近于租金价值
    即：Σe_i → V（租金被完全耗散）

    参数详解：
    ----------
    rent_value : float
        租金的价值（如垄断利润、补贴金额等）
        示例：1000000（一百万的垄断利润）

    n_seekers : int
        寻租者的数量
        示例：5（5家公司竞争一个垄断许可）

    expenditure_per_seeker : float
        每个寻租者的支出（游说、公关费用等）
        示例：150000（每家公司花费15万游说）

    返回值：
    ----------
    float : 社会总损失
        = 总寻租支出（n_seekers × expenditure_per_seeker）
        这里采用最简单的模型，只考虑直接寻租支出

    数值示例：
    ----------
    例1：基本计算
    >>> rent_seeking_loss(1000000, 5, 150000)
    750000.0
    # 5家公司各花费15万游说，总损失 = 5 × 150000 = 750000

    例2：完全耗散情况
    >>> rent_seeking_loss(1000000, 10, 100000)
    1000000.0
    # 10家公司各花费10万，总损失 = 10 × 100000 = 1000000
    # 租金被完全耗散

    例3：部分耗散
    >>> rent_seeking_loss(500000, 3, 100000)
    300000.0
    # 3家公司各花费10万，总损失 = 300000
    # 耗散率 = 300000 / 500000 = 60%

    政策含义：
    ----------
    1. 减少政府创造的租金机会可以减少寻租损失
    2. 增加寻租竞争者反而可能增加社会损失
    3. 透明的规则和自动化审批可以减少寻租空间

    TODO提示：
    ----------
    1. 计算总寻租支出
       total_expenditure = n_seekers * expenditure_per_seeker

    2. 返回社会损失（最简单模型只考虑直接支出）
       return total_expenditure

    扩展：如果要考虑资源错配损失，可以加上租金的一部分
       # return total_expenditure + misallocation_factor * rent_value
    """
    # TODO: 寻租损失
    pass


def tullock_lottery(
    efforts: np.ndarray,
    prize: float
) -> np.ndarray:
    """
    图洛克寻租博弈：计算各参与者的期望收益。

    基本原理：
    ----------
    图洛克竞赛（Tullock Contest）是分析寻租行为的经典模型。
    参与者通过投入努力（资源）来竞争一个固定的奖金（租金）。

    博弈设定：
    ----------
    - n个参与者竞争价值为V的租金
    - 参与者i投入努力e_i（成本）
    - 获胜是概率性的，不是确定性的

    比赛成功函数（Contest Success Function）：
    ----------
    参与者i的获胜概率：
    p_i = e_i^r / Σ(e_j^r)

    其中r是"比赛敏感度"参数：
    - r = 1：标准图洛克竞赛（线性）
    - r < 1：努力的边际效果递减
    - r > 1：努力的边际效果递增
    - r → ∞：全胜者拍卖（努力最多者确定获胜）

    本函数使用 r = 1 的标准情况：
    p_i = e_i / Σe_j

    期望收益：
    ----------
    E[π_i] = p_i × V - e_i
           = (e_i / Σe_j) × V - e_i

    纳什均衡分析：
    ----------
    在对称均衡中，每个参与者选择相同的努力水平e*
    一阶条件：∂E[π_i]/∂e_i = 0

    解得：e* = V(n-1)/n²

    均衡特性：
    - 总寻租支出：n × e* = V(n-1)/n
    - 当n→∞时，总支出→V（完全耗散）
    - 每个参与者的期望利润：V/n - e* = V/n²

    参数详解：
    ----------
    efforts : np.ndarray
        各参与者的努力投入，一维数组
        efforts[i] 表示参与者i投入的资源（成本）

        示例：efforts = np.array([100, 150, 200])
        表示3个参与者分别投入100, 150, 200

    prize : float
        奖金（租金）的价值
        示例：prize = 1000

    返回值：
    ----------
    np.ndarray : 各参与者的期望收益数组
        expected_payoff[i] = p_i × prize - efforts[i]

    数值示例：
    ----------
    例1：两个参与者
    >>> efforts = np.array([100, 100])
    >>> prize = 500
    >>> tullock_lottery(efforts, prize)
    array([150., 150.])
    # p_0 = 100/200 = 0.5, E[π_0] = 0.5 × 500 - 100 = 150
    # p_1 = 100/200 = 0.5, E[π_1] = 0.5 × 500 - 100 = 150

    例2：不对称努力
    >>> efforts = np.array([100, 200, 100])
    >>> prize = 800
    >>> tullock_lottery(efforts, prize)
    array([100., 200., 100.])
    # 总努力 = 400
    # p_0 = 100/400 = 0.25, E[π_0] = 0.25 × 800 - 100 = 100
    # p_1 = 200/400 = 0.50, E[π_1] = 0.50 × 800 - 200 = 200
    # p_2 = 100/400 = 0.25, E[π_2] = 0.25 × 800 - 100 = 100

    例3：验证纳什均衡
    >>> # 3个参与者，奖金900，均衡努力 = 900×(3-1)/9 = 200
    >>> efforts = np.array([200, 200, 200])
    >>> prize = 900
    >>> tullock_lottery(efforts, prize)
    array([100., 100., 100.])
    # 每人期望收益 = 900/9 = 100

    例4：边界情况（零努力）
    >>> efforts = np.array([0, 100, 0])
    >>> prize = 500
    >>> tullock_lottery(efforts, prize)
    array([  0., 400.,   0.])
    # 只有参与者1投入努力，获胜概率100%

    TODO提示：
    ----------
    1. 计算总努力
       total_effort = np.sum(efforts)

    2. 处理边界情况（总努力为0）
       if total_effort == 0:
           # 没人投入努力，平分奖金，成本为0
           return np.full(len(efforts), prize / len(efforts))

    3. 计算每个参与者的获胜概率
       probabilities = efforts / total_effort

    4. 计算期望收益
       expected_payoffs = probabilities * prize - efforts

    5. 返回期望收益数组
    """
    # TODO: 图洛克博弈
    pass


def bureaucrat_budget(
    demand_intercept: float,
    demand_slope: float,
    marginal_cost: float
) -> float:
    """
    尼斯卡宁官僚预算最大化模型。

    基本原理：
    ----------
    William Niskanen的官僚行为理论假设官僚追求预算最大化，
    而不是社会福利最大化或成本最小化。

    为什么官僚追求预算最大化？
    - 更大的预算意味着更多的权力和声望
    - 更多的下属和办公室
    - 更高的薪资和晋升机会
    - 更多的资源可供支配

    模型设定：
    ----------
    1. 需求函数（公众的边际支付意愿）：
       P(Q) = a - bQ
       其中 a = demand_intercept, b = demand_slope

    2. 成本函数（假设边际成本恒定）：
       TC(Q) = cQ
       MC(Q) = c = marginal_cost

    3. 信息不对称：
       - 政治家只观察到总收益和总成本
       - 官僚知道真实的成本函数
       - 官僚可以策略性地选择产出水平

    官僚的目标：
    ----------
    最大化预算，同时确保预算能够通过
    条件：总收益 ≥ 总成本（否则政治家不会批准）

    总收益（消费者剩余 + 支付）= 需求曲线下的面积：
    TR(Q) = ∫₀^Q P(q)dq = ∫₀^Q (a - bq)dq = aQ - bQ²/2

    最优策略：选择Q使得 TR(Q) = TC(Q)
    aQ - bQ²/2 = cQ
    aQ - cQ = bQ²/2
    (a - c)Q = bQ²/2
    Q* = 2(a - c) / b

    效率比较：
    ----------
    社会最优产出（边际收益 = 边际成本）：
    a - bQ = c
    Q_eff = (a - c) / b

    官僚产出 vs 效率产出：
    Q* / Q_eff = [2(a-c)/b] / [(a-c)/b] = 2

    结论：官僚的预算最大化产出是社会最优产出的两倍！

    参数详解：
    ----------
    demand_intercept : float (a)
        需求函数的截距，表示Q=0时的边际支付意愿
        即第一单位公共服务的最高价值
        示例：a = 100 表示第一单位价值100

    demand_slope : float (b)
        需求函数的斜率（绝对值），表示需求下降的速度
        示例：b = 2 表示每增加一单位产出，边际价值下降2

    marginal_cost : float (c)
        提供公共服务的边际成本（假设恒定）
        示例：c = 20 表示每单位成本为20

    返回值：
    ----------
    float : 预算最大化产出 Q*
        Q* = 2(a - c) / b

    数值示例：
    ----------
    例1：基本计算
    >>> bureaucrat_budget(100, 2, 20)
    80.0
    # a=100, b=2, c=20
    # Q* = 2(100-20)/2 = 2×80/2 = 80
    # 效率产出 Q_eff = (100-20)/2 = 40
    # 过度供给：80 vs 40

    例2：高边际成本
    >>> bureaucrat_budget(100, 2, 60)
    40.0
    # Q* = 2(100-60)/2 = 40
    # 效率产出 Q_eff = 20

    例3：验证预算约束
    # Q* = 80 时：
    # TR = 100×80 - 2×80²/2 = 8000 - 6400 = 1600
    # TC = 20×80 = 1600
    # TR = TC，预算约束恰好满足

    图形理解：
    ----------
    价格
    |
    a |\
      | \  需求曲线 P = a - bQ
      |  \
    c |...\.........  MC = c
      |    \        |
      |_____\________|___ 数量
            Q_eff   Q*

    效率产出：需求曲线与MC相交
    官僚产出：使得三角形面积（TR）等于矩形面积（TC）

    TODO提示：
    ----------
    1. 计算预算最大化产出
       Q_star = 2 * (demand_intercept - marginal_cost) / demand_slope

    2. 确保产出非负
       return max(0, Q_star)

    或者直接返回：
       return 2 * (demand_intercept - marginal_cost) / demand_slope
    """
    # TODO: 官僚预算
    pass


def log_rolling(
    project_benefits: np.ndarray,
    project_costs: np.ndarray,
    n_voters: int
) -> list[int]:
    """
    滚木立法（互投赞成票）分析。

    基本原理：
    ----------
    滚木立法（Log-rolling）是立法者之间的投票交易：
    "我支持你的法案，你支持我的法案"

    这种做法可能导致社会无效率的项目获得通过，
    因为少数人获益的项目可以通过交易获得多数支持。

    机制分析：
    ----------
    考虑3个立法者A、B、C，代表3个选区

    项目1：只对选区A有利
    - 收益：A得60，B得0，C得0（总收益60）
    - 成本：90，平均分摊（每人30）
    - 净效益：-30（社会无效率）
    - 单独投票：1票赞成，2票反对 → 不通过

    项目2：只对选区B有利
    - 收益：A得0，B得60，C得0（总收益60）
    - 成本：90，平均分摊
    - 单独投票：不通过

    滚木交易：A和B达成协议
    - A投票支持项目2
    - B投票支持项目1
    - 两个项目都以2:1通过！

    结果分析：
    - A的净收益：60 - 30 - 30 = 0
    - B的净收益：60 - 30 - 30 = 0
    - C的净收益：-30 - 30 = -60
    - 社会净收益：0 + 0 - 60 = -60

    C是"被剥削的多数"！

    判断标准：
    ----------
    本函数采用简化标准：如果一个项目对任何选民的净收益为正，
    就假设它可以通过滚木交易获得通过。

    更复杂的分析需要考虑：
    - 具体的交易形成过程
    - 稳定的联盟结构
    - 重复博弈和声誉

    参数详解：
    ----------
    project_benefits : np.ndarray
        收益矩阵，形状为 (n_projects, n_voters)
        project_benefits[j, i] 表示项目j对选民i的收益

        示例：
        project_benefits = np.array([
            [60, 0, 0],   # 项目0：只有选民0受益
            [0, 60, 0],   # 项目1：只有选民1受益
            [30, 30, 30]  # 项目2：所有人受益
        ])

    project_costs : np.ndarray
        各项目的总成本，一维数组
        成本假设由所有选民平均分摊

        示例：project_costs = np.array([90, 90, 60])

    n_voters : int
        选民/立法者数量
        示例：n_voters = 3

    返回值：
    ----------
    list[int] : 可能通过滚木立法获得通过的项目编号列表

    判断逻辑：
    对于每个项目j：
    1. 计算每个选民的净收益 = 收益 - (总成本 / n_voters)
    2. 如果存在至少一个选民的净收益 > 0，该项目可能通过
    （因为受益者有动力进行交易）

    数值示例：
    ----------
    例1：基本滚木案例
    >>> project_benefits = np.array([
    ...     [60, 0, 0],   # 项目0
    ...     [0, 60, 0],   # 项目1
    ... ])
    >>> project_costs = np.array([90, 90])
    >>> n_voters = 3
    >>> log_rolling(project_benefits, project_costs, n_voters)
    [0, 1]
    # 项目0：选民0净收益 = 60 - 30 = 30 > 0，可能通过
    # 项目1：选民1净收益 = 60 - 30 = 30 > 0，可能通过

    例2：有社会效率的项目
    >>> project_benefits = np.array([
    ...     [40, 40, 40]  # 每人收益40
    ... ])
    >>> project_costs = np.array([90])  # 总成本90，每人30
    >>> n_voters = 3
    >>> log_rolling(project_benefits, project_costs, n_voters)
    [0]
    # 每人净收益 = 40 - 30 = 10 > 0，会通过（且社会有效）

    例3：无人受益的项目
    >>> project_benefits = np.array([
    ...     [20, 20, 20]  # 每人收益20
    ... ])
    >>> project_costs = np.array([90])  # 每人成本30
    >>> n_voters = 3
    >>> log_rolling(project_benefits, project_costs, n_voters)
    []
    # 每人净收益 = 20 - 30 = -10 < 0，不会通过

    例4：混合情况
    >>> project_benefits = np.array([
    ...     [100, 0, 0],  # 项目0：集中收益
    ...     [20, 20, 20], # 项目1：分散收益但总收益低
    ...     [50, 50, 50]  # 项目2：分散收益且总收益高
    ... ])
    >>> project_costs = np.array([90, 90, 120])
    >>> n_voters = 3
    >>> log_rolling(project_benefits, project_costs, n_voters)
    [0, 2]
    # 项目0：选民0净收益 = 100 - 30 = 70 > 0
    # 项目1：每人净收益 = 20 - 30 = -10 < 0，无人受益
    # 项目2：每人净收益 = 50 - 40 = 10 > 0

    政策含义：
    ----------
    1. 集中收益、分散成本的项目更容易通过（即使社会无效）
    2. 分散收益、集中成本的项目难以通过（即使社会有效）
    3. 这解释了为什么农业补贴、贸易保护等政策难以废除

    TODO提示：
    ----------
    1. 初始化通过项目列表
       passed_projects = []

    2. 计算每人分摊的成本
       cost_per_voter = project_costs / n_voters

    3. 遍历每个项目
       for j, benefits in enumerate(project_benefits):
           # 计算每个选民的净收益
           net_benefits = benefits - cost_per_voter[j]

           # 如果存在正净收益的选民，项目可能通过
           if np.any(net_benefits > 0):
               passed_projects.append(j)

    4. 返回通过的项目列表
    """
    # TODO: 滚木立法
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
