# EXERCISE: fiscal_sustainability1
# DIFFICULTY: ★★★★☆
# TOPIC: 财政可持续性
#
# ============================================================================
#                        财政可持续性 (Fiscal Sustainability)
# ============================================================================
#
# 一、理论背景与重要性
# ============================================================================
# 财政可持续性是宏观经济政策的核心问题之一，关系到：
# - 政府能否长期履行其支出承诺
# - 主权债务危机的风险评估
# - 财政政策的代际公平
# - 宏观经济稳定
#
# 历史案例：
# - 2010年欧洲主权债务危机（希腊、葡萄牙、爱尔兰等）
# - 1990年代日本的债务累积
# - 2001年阿根廷债务违约
# - 1980年代拉美债务危机
#
# 二、核心概念
# ============================================================================
#
# 1. 政府预算约束
# ----------------------------
# 单期预算约束：
# G_t + r_t B_{t-1} = T_t + (B_t - B_{t-1})
#
# 其中：
# - G_t: 政府支出（不含利息）
# - r_t: 利率
# - B_t: 政府债务存量
# - T_t: 税收收入
#
# 基本余额（Primary Balance）：
# PB_t = T_t - G_t
# - PB > 0: 基本盈余
# - PB < 0: 基本赤字
#
# 总赤字：
# Deficit_t = G_t + r_t B_{t-1} - T_t = -PB_t + r_t B_{t-1}
#
# 2. 债务动态方程
# ----------------------------
# 将变量表示为GDP的比例（小写字母）：
# d_t = B_t / Y_t （债务率）
# pb_t = PB_t / Y_t （基本余额率）
#
# 推导：
# B_t = (1 + r_t) B_{t-1} - PB_t
# 两边除以 Y_t：
# d_t = (1 + r_t) / (1 + g_t) × d_{t-1} - pb_t
#
# 其中 g_t = (Y_t - Y_{t-1}) / Y_{t-1} 是GDP增长率
#
# 近似形式（当r和g较小时）：
# Δd_t ≈ (r_t - g_t) d_{t-1} - pb_t
#
# 关键洞察：
# - 如果 r < g：即使有基本赤字，债务率也可能下降
# - 如果 r > g：需要基本盈余来稳定债务率
# - (r - g) 被称为"利率-增长率差"，是财政可持续性的关键
#
# 3. 稳态债务率
# ----------------------------
# 在稳态（Δd = 0）时：
# 0 = (r - g) d* - pb
# d* = pb / (g - r)
#
# 条件：
# - 当 g > r 且 pb > 0 时：正的稳态债务率
# - 当 g > r 且 pb < 0 时：负的稳态债务率（净资产）
# - 当 g < r 时：需要 pb > 0 才能有正的稳态债务率
#
# 4. 跨期预算约束（No-Ponzi Condition）
# ----------------------------
# 政府不能永远通过借新债还旧债（庞氏骗局）。
#
# 数学表达：
# lim_{T→∞} B_T / ∏(1+r_s) = 0
#
# 这意味着债务的现值最终必须为零。
#
# 等价条件：
# B_0 = Σ_{t=1}^{∞} PB_t / ∏_{s=1}^{t}(1+r_s)
#
# 即：当前债务 = 未来基本盈余的现值
#
# 5. 财政缺口 (Fiscal Gap)
# ----------------------------
# 定义：使跨期预算约束成立所需的即时永久性财政调整
#
# 财政缺口 = 所需基本余额 - 当前基本余额
#
# 如果财政缺口为正，意味着：
# - 需要增加税收，或
# - 需要削减支出，或
# - 两者的组合
#
# 6. 财政空间 (Fiscal Space)
# ----------------------------
# 定义：政府在不危及财政可持续性的前提下，可以增加的额外支出或债务
#
# 简单定义：
# 财政空间 = 债务上限 - 当前债务率
#
# 更复杂的定义考虑：
# - 债务容忍度（debt intolerance）
# - 市场信心
# - 历史违约记录
# - 制度质量
#
# 7. 债务分解
# ----------------------------
# 债务率变化可以分解为几个组成部分：
#
# Δd = (r - g)d - pb + SFA
#
# 其中：
# - 利息贡献：r × d（利息支付推高债务）
# - 增长贡献：-g × d（经济增长稀释债务）
# - 基本余额贡献：-pb（盈余降低债务，赤字增加债务）
# - 存量-流量调整（SFA）：会计调整、估值变化等
#
# 8. 代际核算 (Generational Accounting)
# ----------------------------
# 由 Alan Auerbach 和 Laurence Kotlikoff 提出。
#
# 核心思想：
# 分析财政政策在不同代际之间的负担分配
#
# 代际不平衡：
# 如果当前政策持续，未来世代需要承担更多负担来维持财政可持续性
#
# 计算：
# 未来代的净税收负担 vs 当前代的净税收负担
#
# 三、财政规则
# ============================================================================
# 许多国家采用财政规则来确保可持续性：
#
# 1. 赤字规则
#    - 欧盟《稳定与增长公约》：赤字不超过GDP的3%
#    - 美国：债务上限（需国会批准提高）
#
# 2. 债务规则
#    - 欧盟：债务不超过GDP的60%
#    - 德国"债务刹车"（Schuldenbremse）
#
# 3. 支出规则
#    - 限制支出增长率
#    - 与GDP增长挂钩
#
# 4. 黄金规则
#    - 只允许为资本支出借债
#    - 经常性支出必须由税收覆盖
#
# 四、模型假设与局限
# ============================================================================
# 1. 利率和增长率假设为外生且恒定（实际上会变化）
# 2. 忽略了债务结构（期限、货币等）
# 3. 未考虑隐性债务（养老金承诺、医疗保障等）
# 4. 未考虑或有负债（金融部门担保等）
# 5. 政治经济因素被忽略
#
# 五、学习目标
# ============================================================================
# 1. 理解债务动态的基本方程
# 2. 掌握财政可持续性的判断标准
# 3. 计算财政缺口和财政空间
# 4. 理解代际公平问题
# 5. 分析财政规则的作用
#
# ============================================================================

import numpy as np


def debt_dynamics(
    initial_debt_ratio: float,
    interest_rate: float,
    growth_rate: float,
    primary_balance_ratio: float,
    years: int
) -> np.ndarray:
    """
    模拟债务动态，计算债务率的时间路径。

    基本原理：
    ----------
    政府债务的动态演变遵循债务动态方程。给定初始债务率和财政政策参数，
    可以模拟未来债务率的变化轨迹。

    债务动态方程：
    ----------
    精确形式：
    d_{t+1} = (1 + r) / (1 + g) × d_t - pb

    其中：
    - d_t: t期的债务/GDP比率
    - r: 名义利率
    - g: 名义GDP增长率
    - pb: 基本余额/GDP（盈余为正，赤字为负）

    推导过程：
    从 B_{t+1} = (1 + r) B_t - PB × Y_t
    两边除以 Y_{t+1} = (1 + g) Y_t：
    d_{t+1} = (1 + r) / (1 + g) × d_t - pb

    近似形式（当r, g较小时）：
    Δd ≈ (r - g) d_t - pb

    关键参数 (r - g)：
    - r - g > 0: 利率超过增长率，债务自我膨胀
    - r - g < 0: 增长率超过利率，债务自我收缩
    - r - g = 0: 债务率变化仅取决于基本余额

    参数详解：
    ----------
    initial_debt_ratio : float
        初始债务/GDP比率（t=0时的值）
        示例：0.6 表示债务为GDP的60%

    interest_rate : float
        名义利率（年化）
        示例：0.05 表示5%的年利率

    growth_rate : float
        名义GDP增长率（年化）
        示例：0.03 表示3%的年增长率

    primary_balance_ratio : float
        基本余额/GDP比率
        - 正值表示基本盈余（收入>支出）
        - 负值表示基本赤字（支出>收入）
        示例：0.02 表示2%GDP的基本盈余
              -0.03 表示3%GDP的基本赤字

    years : int
        模拟年数
        示例：10 表示模拟10年

    返回值：
    ----------
    np.ndarray : 债务/GDP比率的时间序列
        - 长度为 years + 1（包含初始值）
        - path[0] = initial_debt_ratio
        - path[t] = t期末的债务率

    数值示例：
    ----------
    例1：利率高于增长率，无基本盈余
    >>> debt_dynamics(0.6, 0.05, 0.02, 0.0, 5)
    array([0.6, 0.618, 0.636, 0.655, 0.674, 0.694])
    # 债务率持续上升（r > g 且 pb = 0）
    # 乘数 = (1.05/1.02) = 1.0294

    例2：利率高于增长率，有基本盈余
    >>> debt_dynamics(0.6, 0.05, 0.02, 0.02, 5)
    array([0.6, 0.598, 0.596, 0.594, 0.592, 0.590])
    # 基本盈余抵消了利息支付，债务率缓慢下降

    例3：利率低于增长率（日本情况的近似）
    >>> debt_dynamics(1.5, 0.01, 0.02, -0.03, 5)
    array([1.5, 1.455, 1.411, 1.368, 1.326, 1.285])
    # 即使有基本赤字，由于 g > r，债务率仍在下降

    例4：债务爆炸性增长
    >>> debt_dynamics(0.6, 0.08, 0.02, -0.02, 10)
    # 高利率 + 赤字 = 债务快速膨胀

    政策含义：
    ----------
    1. 降低利率（货币政策）可以减轻债务负担
    2. 提高经济增长是最"无痛"的债务化解方式
    3. 基本盈余是财政调整的核心工具
    4. 观察债务轨迹可以判断政策是否可持续

    TODO提示：
    ----------
    1. 创建存储债务路径的数组
       path = np.zeros(years + 1)
       path[0] = initial_debt_ratio

    2. 计算增长调整后的利率因子
       growth_factor = (1 + interest_rate) / (1 + growth_rate)

    3. 迭代计算每年的债务率
       for t in range(years):
           path[t + 1] = growth_factor * path[t] - primary_balance_ratio

    4. 返回债务路径
    """
    # TODO: 债务动态
    pass


def required_primary_balance(
    current_debt_ratio: float,
    target_debt_ratio: float,
    interest_rate: float,
    growth_rate: float,
    years: int
) -> float:
    """
    计算在给定年限内达到目标债务率所需的基本余额。

    基本原理：
    ----------
    给定当前债务率和目标债务率，以及调整期限，可以计算出
    需要保持多大的基本余额才能实现目标。

    这是政策制定的关键工具：告诉决策者需要多大的财政调整。

    数学推导：
    ----------
    设增长调整后的利率因子为 α = (1+r)/(1+g)

    债务动态：d_{t+1} = α × d_t - pb

    迭代求解：
    d_1 = α × d_0 - pb
    d_2 = α × d_1 - pb = α² × d_0 - pb(1 + α)
    ...
    d_n = α^n × d_0 - pb × (α^{n-1} + α^{n-2} + ... + 1)
        = α^n × d_0 - pb × (α^n - 1)/(α - 1)   （当α ≠ 1时）

    求解pb：
    target = α^n × current - pb × (α^n - 1)/(α - 1)

    pb = (α^n × current - target) × (α - 1) / (α^n - 1)

    特殊情况：
    - 当 r = g 时，α = 1，债务变化 = n × pb
      pb = (current - target) / n

    参数详解：
    ----------
    current_debt_ratio : float
        当前债务/GDP比率
        示例：0.8 表示当前债务为GDP的80%

    target_debt_ratio : float
        目标债务/GDP比率
        示例：0.6 表示目标是将债务降至GDP的60%

    interest_rate : float
        名义利率
        示例：0.04 表示4%

    growth_rate : float
        GDP增长率
        示例：0.03 表示3%

    years : int
        调整年限
        示例：10 表示10年内达到目标

    返回值：
    ----------
    float : 所需的基本余额/GDP比率
        - 正值表示需要基本盈余
        - 负值表示可以有基本赤字（但仍能达到目标）

    数值示例：
    ----------
    例1：降低债务率
    >>> required_primary_balance(0.8, 0.6, 0.04, 0.03, 10)
    0.027
    # 需要约2.7%GDP的基本盈余才能在10年内将债务从80%降至60%

    例2：稳定债务率
    >>> required_primary_balance(0.6, 0.6, 0.05, 0.02, 10)
    0.017
    # 需要约1.7%GDP的基本盈余来稳定60%的债务率

    例3：利率低于增长率时增加债务
    >>> required_primary_balance(0.6, 0.8, 0.02, 0.04, 10)
    -0.025
    # 可以有2.5%GDP的基本赤字，债务仍会增至80%

    例4：快速削减债务
    >>> required_primary_balance(1.0, 0.6, 0.03, 0.02, 5)
    0.087
    # 需要8.7%GDP的基本盈余——这是非常激进的财政紧缩

    政策应用：
    ----------
    - 欧盟委员会使用类似方法评估成员国的财政调整需求
    - IMF在援助计划中使用此方法设定财政目标
    - 各国财政部用于中期财政规划

    TODO提示：
    ----------
    1. 计算增长调整后的利率因子
       alpha = (1 + interest_rate) / (1 + growth_rate)

    2. 处理特殊情况 r ≈ g
       if abs(alpha - 1) < 1e-10:
           # 当 r = g 时
           return (current_debt_ratio - target_debt_ratio) / years

    3. 计算所需的基本余额
       alpha_n = alpha ** years
       pb = (alpha_n * current_debt_ratio - target_debt_ratio) * \
            (alpha - 1) / (alpha_n - 1)

    4. 返回结果
    """
    # TODO: 所需基本余额
    pass


def steady_state_debt(
    primary_balance_ratio: float,
    interest_rate: float,
    growth_rate: float
) -> float:
    """
    计算给定政策参数下的稳态债务率。

    基本原理：
    ----------
    稳态是指债务率不再变化的状态（Δd = 0）。
    给定基本余额和利率-增长率差，可以计算出长期均衡的债务水平。

    数学推导：
    ----------
    在稳态：d_{t+1} = d_t = d*

    代入债务动态方程：
    d* = (1+r)/(1+g) × d* - pb

    整理：
    d* [1 - (1+r)/(1+g)] = -pb
    d* [(1+g-1-r)/(1+g)] = -pb
    d* (g-r)/(1+g) = -pb

    解得：
    d* = -pb × (1+g) / (g-r)
       = pb × (1+g) / (r-g)

    近似形式（当r, g较小时）：
    d* ≈ pb / (r - g)  或  d* ≈ -pb / (g - r)

    稳定性分析：
    ----------
    - 当 r < g 时：稳态是稳定的
      - 如果 pb > 0（盈余）：d* > 0（正债务）
      - 如果 pb < 0（赤字）：d* < 0（净资产）

    - 当 r > g 时：稳态是不稳定的
      - 任何偏离都会导致债务发散
      - 只有 pb > (r-g)d 才能阻止发散

    参数详解：
    ----------
    primary_balance_ratio : float
        基本余额/GDP比率
        - 正值：基本盈余
        - 负值：基本赤字
        示例：0.02 表示2%GDP的盈余

    interest_rate : float
        名义利率
        示例：0.04 表示4%

    growth_rate : float
        GDP增长率
        示例：0.05 表示5%

    返回值：
    ----------
    float : 稳态债务/GDP比率
        - 当 r = g 时返回 np.inf 或 -np.inf（无有限稳态）
        - 当 g > r 且 pb > 0 时：返回正值
        - 当 g > r 且 pb < 0 时：返回负值（净资产）

    数值示例：
    ----------
    例1：增长率高于利率，有基本盈余
    >>> steady_state_debt(0.02, 0.03, 0.05)
    1.03
    # 稳态债务率约为103%GDP
    # d* = 0.02 × 1.05 / (0.03 - 0.05) = 0.021 / (-0.02) ≈ -1.05
    # 但使用近似公式：d* = 0.02 / (0.05 - 0.03) = 1.0

    例2：增长率高于利率，有基本赤字
    >>> steady_state_debt(-0.02, 0.03, 0.05)
    -1.03
    # 稳态是负债务率（政府净资产）
    # 这是理论上的结果，实际中很少见

    例3：利率高于增长率
    >>> steady_state_debt(0.02, 0.05, 0.03)
    1.03
    # 虽然数学上存在稳态，但这是不稳定的
    # 任何偏离都会导致债务发散

    例4：利率等于增长率
    >>> steady_state_debt(0.02, 0.04, 0.04)
    inf  # 或 -inf，取决于pb的符号
    # 没有有限的稳态

    TODO提示：
    ----------
    1. 检查 r = g 的情况（无有限稳态）
       if abs(interest_rate - growth_rate) < 1e-10:
           if primary_balance_ratio >= 0:
               return np.inf
           else:
               return -np.inf

    2. 使用精确公式计算稳态债务
       d_star = primary_balance_ratio * (1 + growth_rate) / \
                (interest_rate - growth_rate)

    或使用近似公式：
       d_star = primary_balance_ratio / (interest_rate - growth_rate)

    3. 返回结果
    """
    # TODO: 稳态债务
    pass


def is_debt_sustainable(
    debt_ratio: float,
    interest_rate: float,
    growth_rate: float,
    primary_balance_ratio: float
) -> bool:
    """
    判断当前财政政策下债务是否可持续。

    基本原理：
    ----------
    财政可持续性有多种定义，本函数采用最基本的定义：
    债务率不会无限增长（即收敛或稳定在有限值）。

    判断标准：
    ----------
    1. 如果 g > r（增长率高于利率）：
       债务总是可持续的，因为稳态是稳定的
       任何初始债务最终都会收敛到稳态

    2. 如果 g < r（利率高于增长率）：
       需要足够大的基本盈余来抵消利息
       可持续条件：pb ≥ (r - g) × d
       即：基本盈余 ≥ 利率-增长率差 × 债务率

    3. 如果 g = r：
       - pb > 0：债务逐渐下降，可持续
       - pb ≤ 0：债务稳定或上升

    经济直觉：
    ----------
    - 利息使债务自动增长（速度为r）
    - 经济增长使债务率自动下降（速度为g）
    - 净效果取决于 r - g
    - 基本盈余是主动偿还债务
    - 只有当主动偿还+被动稀释 ≥ 利息时，债务才能稳定

    参数详解：
    ----------
    debt_ratio : float
        当前债务/GDP比率
        示例：0.6 表示60%

    interest_rate : float
        名义利率
        示例：0.05 表示5%

    growth_rate : float
        GDP增长率
        示例：0.03 表示3%

    primary_balance_ratio : float
        基本余额/GDP比率
        示例：0.01 表示1%GDP的盈余

    返回值：
    ----------
    bool : 债务是否可持续
        - True: 债务可持续（不会无限增长）
        - False: 债务不可持续（将无限增长）

    数值示例：
    ----------
    例1：增长率高于利率
    >>> is_debt_sustainable(0.8, 0.03, 0.05, -0.02)
    True
    # 即使有2%的基本赤字，由于 g > r，债务仍可持续

    例2：利率高于增长率，盈余不足
    >>> is_debt_sustainable(0.6, 0.05, 0.02, 0.01)
    False
    # 需要的盈余：(0.05-0.02) × 0.6 = 0.018 = 1.8%
    # 实际盈余：1%，不足以稳定债务

    例3：利率高于增长率，盈余充足
    >>> is_debt_sustainable(0.6, 0.05, 0.02, 0.02)
    True
    # 需要的盈余：1.8%，实际盈余：2%，足够

    例4：高债务率需要更大盈余
    >>> is_debt_sustainable(1.5, 0.05, 0.02, 0.03)
    False
    # 需要的盈余：(0.05-0.02) × 1.5 = 4.5%
    # 实际盈余：3%，不足

    政策含义：
    ----------
    1. 高债务国家需要更大的财政调整
    2. 降低利率可以缓解财政压力
    3. 提高增长率是最有利的改善途径
    4. 低增长高债务国家面临最大挑战

    TODO提示：
    ----------
    1. 如果增长率高于利率，总是可持续
       if growth_rate > interest_rate:
           return True

    2. 如果增长率等于利率
       if abs(growth_rate - interest_rate) < 1e-10:
           return primary_balance_ratio >= 0

    3. 如果利率高于增长率，检查盈余是否足够
       required_pb = (interest_rate - growth_rate) * debt_ratio
       return primary_balance_ratio >= required_pb
    """
    # TODO: 可持续判断
    pass


def fiscal_gap(
    debt_ratio: float,
    interest_rate: float,
    growth_rate: float,
    current_primary_balance: float,
    target_debt_ratio: float = None
) -> float:
    """
    计算财政缺口：使债务可持续所需的财政调整。

    基本原理：
    ----------
    财政缺口衡量的是当前财政政策与可持续财政政策之间的差距。
    它告诉决策者需要多大的财政调整（增税或减支）。

    定义：
    ----------
    财政缺口 = 所需基本余额 - 当前基本余额

    所需基本余额的计算：
    - 如果要稳定债务率在当前水平：pb_required = (r - g) × d
    - 如果要稳定在目标水平：需要更复杂的计算

    解释：
    ----------
    - 财政缺口 > 0：需要增加盈余（增税或减支）
    - 财政缺口 < 0：可以增加赤字（有财政空间）
    - 财政缺口 = 0：当前政策恰好可持续

    参数详解：
    ----------
    debt_ratio : float
        当前债务/GDP比率
        示例：0.8

    interest_rate : float
        名义利率
        示例：0.05

    growth_rate : float
        GDP增长率
        示例：0.03

    current_primary_balance : float
        当前基本余额/GDP比率
        示例：-0.02（2%的基本赤字）

    target_debt_ratio : float, optional
        目标债务率，默认为当前债务率（稳定当前水平）
        示例：0.6

    返回值：
    ----------
    float : 财政缺口/GDP比率
        - 正值：需要财政紧缩
        - 负值：有财政扩张空间

    数值示例：
    ----------
    例1：稳定当前债务率
    >>> fiscal_gap(0.8, 0.05, 0.03, -0.01)
    0.026
    # 所需盈余：(0.05-0.03) × 0.8 = 0.016 = 1.6%
    # 当前余额：-1%（赤字）
    # 财政缺口：1.6% - (-1%) = 2.6%
    # 需要2.6%GDP的财政调整

    例2：当前政策可持续
    >>> fiscal_gap(0.6, 0.04, 0.03, 0.01)
    -0.004
    # 所需盈余：(0.04-0.03) × 0.6 = 0.006 = 0.6%
    # 当前盈余：1%
    # 财政缺口：0.6% - 1% = -0.4%
    # 有财政空间

    例3：增长率高于利率
    >>> fiscal_gap(0.6, 0.02, 0.04, 0.0)
    0.012
    # 所需盈余：(0.02-0.04) × 0.6 = -0.012 = -1.2%（可以有赤字）
    # 当前余额：0
    # 财政缺口：-1.2% - 0 = -1.2%
    # 但考虑到是负数，说明有空间

    例4：向目标债务率调整
    >>> fiscal_gap(0.8, 0.05, 0.03, -0.01, target_debt_ratio=0.6)
    # 需要更大的盈余来同时偿还债务

    政策应用：
    ----------
    - IMF和世界银行使用财政缺口评估各国财政状况
    - 欧盟委员会的"可持续性报告"使用类似概念
    - 用于设计财政调整计划

    TODO提示：
    ----------
    1. 确定目标债务率
       if target_debt_ratio is None:
           target_debt_ratio = debt_ratio

    2. 计算稳定目标债务率所需的基本余额
       # 简化版本：只考虑稳定在目标水平
       required_pb = (interest_rate - growth_rate) * target_debt_ratio

    3. 计算财政缺口
       gap = required_pb - current_primary_balance

    4. 返回财政缺口
    """
    # TODO: 财政缺口
    pass


def fiscal_space(
    current_debt_ratio: float,
    debt_limit: float,
    interest_rate: float,
    growth_rate: float
) -> float:
    """
    计算财政空间：可以增加的额外债务。

    基本原理：
    ----------
    财政空间是指政府在不危及财政可持续性的前提下，
    可以承担的额外债务或支出。

    简单定义：
    财政空间 = 债务上限 - 当前债务率

    更复杂的定义考虑：
    - 动态路径（不仅是静态差异）
    - 利率对债务水平的敏感性
    - 市场信心和风险溢价
    - 制度因素

    债务上限的来源：
    ----------
    1. 法定上限（如欧盟的60%规则）
    2. 市场容忍度（历史经验表明的临界点）
    3. 财政反应函数（政府调整财政的意愿和能力）

    研究表明：
    - 发达国家的债务容忍度较高（可能超过100%）
    - 新兴市场的债务容忍度较低（可能40-60%）
    - 有违约历史的国家容忍度更低

    参数详解：
    ----------
    current_debt_ratio : float
        当前债务/GDP比率
        示例：0.5

    debt_limit : float
        债务上限/GDP比率
        示例：0.8（80%作为安全上限）

    interest_rate : float
        名义利率（用于调整考虑）
        示例：0.04

    growth_rate : float
        GDP增长率（用于调整考虑）
        示例：0.03

    返回值：
    ----------
    float : 财政空间（可增加的债务/GDP比率）
        - 正值：有空间增加债务
        - 负值：已超过上限，需要削减债务
        - 零：恰好在上限

    数值示例：
    ----------
    例1：基本计算
    >>> fiscal_space(0.5, 0.8, 0.04, 0.03)
    0.3
    # 简单差异：80% - 50% = 30%
    # 有30%GDP的财政空间

    例2：接近上限
    >>> fiscal_space(0.75, 0.8, 0.04, 0.03)
    0.05
    # 只有5%GDP的空间，需要谨慎

    例3：已超过上限
    >>> fiscal_space(0.9, 0.8, 0.04, 0.03)
    -0.1
    # 负的财政空间，需要削减债务

    例4：考虑增长率的调整
    # 高增长率可能意味着更大的实际财政空间
    # 因为未来GDP更高，债务更容易稀释

    政策应用：
    ----------
    1. 财政刺激政策的空间评估
    2. 危机应对能力的评估
    3. 主权信用评级的考量因素
    4. 财政规则的设计

    扩展考虑：
    ----------
    更精细的财政空间计算可以考虑：
    - 利率对债务的弹性（债务增加可能导致利率上升）
    - 财政乘数（支出增加对GDP的影响）
    - 政策可信度（影响市场预期）

    TODO提示：
    ----------
    1. 基本财政空间计算
       basic_space = debt_limit - current_debt_ratio

    2. 可选：考虑利率和增长率的调整
       # 如果 r > g，实际空间可能更小
       # 如果 g > r，实际空间可能更大
       # adjustment = some_function(interest_rate, growth_rate)

    3. 返回财政空间
       return basic_space

    简化版本直接返回差值：
       return debt_limit - current_debt_ratio
    """
    # TODO: 财政空间
    pass


def debt_decomposition(
    debt_change: float,
    interest_rate: float,
    growth_rate: float,
    initial_debt: float,
    primary_balance: float,
    stock_flow_adjustment: float
) -> dict:
    """
    将债务率变化分解为各组成部分。

    基本原理：
    ----------
    债务率的变化可以分解为几个驱动因素，这有助于理解
    债务变化的原因，并指导政策制定。

    分解公式：
    ----------
    Δd = (r - g)d - pb + SFA

    展开为：
    Δd = r×d - g×d - pb + SFA

    各组成部分：
    1. 利息贡献 (Interest Effect): r × d
       - 利息支付增加债务
       - 利率越高、债务越高，贡献越大

    2. 增长贡献 (Growth Effect): -g × d
       - 经济增长稀释债务
       - 增长率越高，贡献越负（减少债务率）

    3. 基本余额贡献 (Primary Balance Effect): -pb
       - 盈余减少债务率，赤字增加
       - 这是政府可以直接控制的部分

    4. 存量-流量调整 (Stock-Flow Adjustment, SFA):
       - 会计调整（如资产出售）
       - 汇率变动对外币债务的影响
       - 或有负债的实现
       - 其他未反映在赤字中的债务变化

    参数详解：
    ----------
    debt_change : float
        债务率的实际变化（Δd = d_t - d_{t-1}）
        示例：0.05 表示债务率增加5个百分点

    interest_rate : float
        名义利率
        示例：0.04

    growth_rate : float
        名义GDP增长率
        示例：0.02

    initial_debt : float
        期初债务率（d_{t-1}）
        示例：0.6

    primary_balance : float
        基本余额/GDP（正为盈余）
        示例：0.01

    stock_flow_adjustment : float
        存量-流量调整
        示例：0.01

    返回值：
    ----------
    dict : 债务变化的分解
        {
            'interest': 利息贡献 (r × d),
            'growth': 增长贡献 (-g × d),
            'primary': 基本余额贡献 (-pb),
            'sfa': 存量-流量调整
        }

    数值示例：
    ----------
    例1：标准分解
    >>> debt_decomposition(0.05, 0.04, 0.02, 0.6, 0.01, 0.02)
    {
        'interest': 0.024,   # 0.04 × 0.6 = 2.4%
        'growth': -0.012,    # -0.02 × 0.6 = -1.2%
        'primary': -0.01,    # -0.01 = -1%
        'sfa': 0.02          # 2%
    }
    # 验证：0.024 - 0.012 - 0.01 + 0.02 = 0.022
    # 注意：分解之和应等于 (r-g)d - pb + SFA
    # 实际债务变化可能略有不同（因为公式是近似的）

    例2：高增长率抵消利息
    >>> debt_decomposition(0.02, 0.03, 0.05, 0.8, -0.02, 0.0)
    {
        'interest': 0.024,   # 0.03 × 0.8 = 2.4%
        'growth': -0.04,     # -0.05 × 0.8 = -4%
        'primary': 0.02,     # -(-0.02) = 2%
        'sfa': 0.0
    }
    # 增长贡献(-4%)抵消了利息(2.4%)和赤字(2%)

    例3：债务危机期间
    >>> debt_decomposition(0.15, 0.08, -0.02, 1.0, 0.02, 0.05)
    {
        'interest': 0.08,    # 8%
        'growth': 0.02,      # GDP负增长，增加债务率
        'primary': -0.02,    # -2%（有盈余）
        'sfa': 0.05          # 5%（或有负债实现等）
    }

    政策应用：
    ----------
    1. 识别债务增长的主要驱动因素
    2. 评估政策有效性（基本余额贡献）
    3. 理解外部因素的影响（利率、增长）
    4. 发现数据问题（大的SFA可能表示隐性债务）

    TODO提示：
    ----------
    1. 计算各组成部分
       interest_contribution = interest_rate * initial_debt
       growth_contribution = -growth_rate * initial_debt
       primary_contribution = -primary_balance
       sfa_contribution = stock_flow_adjustment

    2. 返回分解结果
       return {
           'interest': interest_contribution,
           'growth': growth_contribution,
           'primary': primary_contribution,
           'sfa': sfa_contribution
       }

    注意：分解之和应该近似等于实际债务变化
    sum ≈ debt_change（可能有小的舍入差异）
    """
    # TODO: 债务分解
    pass


def generational_accounting(
    current_spending: float,
    future_spending_growth: float,
    tax_revenue: float,
    discount_rate: float,
    years: int
) -> float:
    """
    代际核算：计算代际间的财政负担分配。

    基本原理：
    ----------
    代际核算（Generational Accounting）由 Auerbach, Gokhale, 和 Kotlikoff
    在1990年代提出，用于分析财政政策的代际影响。

    核心问题：
    如果当前财政政策持续，未来世代需要承担多少额外负担？

    计算方法：
    ----------
    1. 计算政府跨期预算约束的现值

    2. 当前代的净税收负担：
       他们支付的税收 - 他们获得的福利

    3. 未来代的净税收负担：
       满足跨期预算约束所需的额外负担

    4. 代际不平衡 = 未来代净负担 - 当前代净负担

    简化模型：
    ----------
    本函数计算一个简化的代际不平衡指标：
    未来支出的现值 - 未来收入的现值

    如果这个值为正，说明存在代际不平衡，
    未来世代需要承担更多负担（更高税收或更低福利）。

    参数详解：
    ----------
    current_spending : float
        当前政府支出（作为初始值）
        示例：1000（10亿单位）

    future_spending_growth : float
        未来支出的年增长率
        示例：0.03 表示每年增长3%（如医疗、养老支出）

    tax_revenue : float
        当前税收收入（假设保持不变或按某比例增长）
        示例：900

    discount_rate : float
        折现率（时间偏好 + 风险调整）
        示例：0.05

    years : int
        分析期限（通常是75年或无穷期）
        示例：50

    返回值：
    ----------
    float : 代际不平衡（正值表示未来代负担更重）
        = 未来支出现值 - 未来收入现值

    数值示例：
    ----------
    例1：支出增长快于折现率
    >>> generational_accounting(100, 0.04, 95, 0.03, 30)
    # 支出增长(4%) > 折现率(3%)，代际不平衡会很大
    # 未来支出的现值会非常高

    例2：支出增长慢于折现率
    >>> generational_accounting(100, 0.02, 95, 0.05, 30)
    # 支出增长(2%) < 折现率(5%)
    # 代际不平衡较小

    例3：收支平衡
    >>> generational_accounting(100, 0.02, 100, 0.02, 30)
    0.0
    # 如果收入也以相同速度增长，可能平衡

    例4：人口老龄化情景
    # 老龄化导致养老金和医疗支出快速增长
    # 而劳动力减少导致税基萎缩
    # 代际不平衡会很大

    政策含义：
    ----------
    1. 大的代际不平衡意味着需要改革
       - 削减未来福利承诺
       - 增加当前储蓄
       - 提高未来税率

    2. 养老金和医疗改革的必要性
       - 延迟退休年龄
       - 从现收现付转向基金制
       - 控制医疗成本

    3. 财政透明度
       - 显示隐性负债
       - 揭示政策的真实成本

    局限性：
    ----------
    1. 对参数（折现率、增长率）非常敏感
    2. 难以准确预测未来几十年的变化
    3. 不考虑政策的内生反应
    4. 忽略代际间的转移支付可能带来的效用

    TODO提示：
    ----------
    1. 计算未来支出的现值
       spending_pv = 0
       for t in range(1, years + 1):
           future_spending = current_spending * (1 + future_spending_growth) ** t
           discounted = future_spending / (1 + discount_rate) ** t
           spending_pv += discounted

    2. 计算未来收入的现值（简化：假设收入不变）
       revenue_pv = sum(tax_revenue / (1 + discount_rate) ** t
                       for t in range(1, years + 1))

    3. 计算代际不平衡
       imbalance = spending_pv - revenue_pv

    4. 返回结果

    或者使用等比级数公式简化计算：
    如果增长率和折现率固定，可以用公式直接计算现值
    """
    # TODO: 代际核算
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
