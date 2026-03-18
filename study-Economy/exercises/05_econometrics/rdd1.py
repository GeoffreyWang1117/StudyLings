# EXERCISE: rdd1
# DIFFICULTY: ★★★★★
# TOPIC: 断点回归设计
#
# 说明：
# 断点回归设计（Regression Discontinuity Design, RDD）是一种准实验方法，
# 利用处理分配规则中的断点来识别因果效应。RDD被认为是最接近随机实验的
# 观察性研究方法。
#
# 【理论背景】
# 在许多现实场景中，是否接受处理取决于某个变量是否超过某个阈值：
# - 考试分数超过及格线获得奖学金
# - 收入低于贫困线获得补贴
# - 年龄达到65岁获得养老金
# - 选举中票数过半当选
#
# 【基本设定】
# - 运行变量（Running Variable）X：决定处理分配的连续变量
# - 阈值（Cutoff）c：处理分配的临界点
# - 处理（Treatment）D：是否接受处理
#
# 对于精确断点（Sharp RDD）：
# D = 1{X ≥ c}（当X超过阈值时，必然接受处理）
#
# 【识别策略】
# 核心思想：在断点附近，处理的分配近似随机
#
# 因为：
# 1. 刚好在阈值以上和刚好在阈值以下的个体应该非常相似
# 2. 如果运行变量不可精确操纵，个体无法确保自己落在哪一侧
# 3. 因此，阈值附近的处理分配是"局部随机"的
#
# 【处理效应的估计】
# τ = lim_{x↓c} E[Y|X=x] - lim_{x↑c} E[Y|X=x]
#   = E[Y|X=c⁺] - E[Y|X=c⁻]
#
# 即：断点处结果变量的跳跃
#
# 【估计方法】
#
# 1. 局部线性回归（Local Linear Regression）
#    在断点附近拟合两条直线：
#    - 阈值左侧：Y = α₀ + β₀(X - c) + ε，对于 X < c
#    - 阈值右侧：Y = α₁ + β₁(X - c) + ε，对于 X ≥ c
#    处理效应：τ = α₁ - α₀
#
# 2. 多项式回归
#    在断点两侧拟合高阶多项式
#    但可能导致过拟合，现在不推荐
#
# 【带宽选择】
# 带宽（Bandwidth）h决定使用断点附近多大范围的数据：
# - 带宽太小：方差大（样本少）
# - 带宽太大：偏误大（远离断点的观测可能不可比）
#
# 最优带宽权衡偏误和方差：
# - Imbens-Kalyanaraman (IK) 带宽
# - Calonico-Cattaneo-Titiunik (CCT) 带宽
#
# 【精确断点 vs 模糊断点】
#
# 精确断点（Sharp RDD）：
# D = 1{X ≥ c}
# 处理完全由运行变量决定
#
# 模糊断点（Fuzzy RDD）：
# P(D=1|X=c⁺) - P(D=1|X=c⁻) < 1
# 超过阈值只改变处理的概率，不是确定性的
# 类似于IV，用断点作为处理的工具变量
# τ_fuzzy = [E(Y|X=c⁺) - E(Y|X=c⁻)] / [E(D|X=c⁺) - E(D|X=c⁻)]
#
# 【识别假设】
#
# 1. 运行变量不可精确操纵
#    个体不能精确控制自己落在阈值哪一侧
#    可用McCrary检验（运行变量在断点处密度是否跳跃）
#
# 2. 其他因素在断点处连续
#    除了处理，其他协变量在断点处应该是连续的
#    否则无法排除混杂
#
# 【有效性检验】
#
# 1. McCrary密度检验
#    检验运行变量的密度在断点处是否有跳跃
#    有跳跃说明存在操纵
#
# 2. 协变量平衡检验
#    检验预处理协变量在断点处是否连续
#
# 3. 安慰剂断点检验
#    在没有真正断点的位置估计"效应"
#    应该为零
#
# 任务：
# 1. 实现精确断点回归估计
# 2. 实现局部线性回归
# 3. 理解带宽选择
# 4. 实现模糊断点回归
#
# HINT1: 带宽选择影响偏误-方差权衡
# HINT2: McCrary检验用于检测操纵行为
# HINT3: 局部线性回归优于多项式回归

import numpy as np


def sharp_rdd_estimate(
    y: np.ndarray,
    x: np.ndarray,
    cutoff: float,
    bandwidth: float
) -> float:
    """
    精确断点回归估计。

    【估计策略】
    使用局部线性回归，在断点两侧分别拟合直线。

    左侧（x < c）：Y = α_L + β_L(X - c) + ε
    右侧（x ≥ c）：Y = α_R + β_R(X - c) + ε

    处理效应：τ = α_R - α_L

    【为什么用 (X - c) 而不是 X】
    将X中心化到断点：
    - 截距 α_L 和 α_R 分别是断点处的拟合值
    - 处理效应直接是两个截距的差
    - 便于解释

    【带宽的作用】
    只使用 |X - c| ≤ h 范围内的观测
    - 这些观测更接近断点
    - 更好地近似断点处的局部效应

    参数:
        y: 结果变量，形状 (n,)
        x: 运行变量，形状 (n,)
        cutoff: 阈值（c）
        bandwidth: 带宽（h），只使用|X-c| ≤ h的观测

    返回:
        处理效应估计（τ）

    示例:
        奖学金对成绩的影响，60分为阈值
        >>> tau = sharp_rdd_estimate(grades, scores, cutoff=60, bandwidth=10)
        >>> print(f"奖学金的处理效应: {tau:.2f}")

    注意:
        - 确保带宽内两侧都有足够的观测
        - 可考虑使用核加权
    """
    # TODO: Sharp RDD
    # 步骤1: 筛选带宽内的观测 |x - cutoff| ≤ bandwidth
    # 步骤2: 分别对断点左右两侧进行线性回归
    # 步骤3: 计算处理效应 = 右侧截距 - 左侧截距
    pass


def local_linear_regression(
    y: np.ndarray,
    x: np.ndarray,
    x0: float,
    bandwidth: float,
    kernel: str = "triangular"
) -> float:
    """
    局部线性回归在某点的估计值。

    【核加权局部回归】
    不同于普通回归给所有观测相同权重，
    局部线性回归根据观测到估计点x0的距离给予不同权重。

    加权最小二乘：
    min Σ K((x_i - x0)/h) × (y_i - α - β(x_i - x0))²

    其中K是核函数，h是带宽。

    【常用核函数】
    1. 均匀核：K(u) = 0.5 × 1{|u| ≤ 1}
    2. 三角核：K(u) = (1 - |u|) × 1{|u| ≤ 1}
    3. Epanechnikov核：K(u) = 0.75(1-u²) × 1{|u| ≤ 1}

    三角核在RDD中最常用，因为边界偏误较小。

    参数:
        y: 因变量，形状 (n,)
        x: 自变量，形状 (n,)
        x0: 估计点
        bandwidth: 带宽
        kernel: 核函数类型（"triangular", "uniform", "epanechnikov"）

    返回:
        x0点的拟合值（局部线性回归的截距）

    示例:
        估计x=60处的E[Y|X=60]
        >>> y_hat = local_linear_regression(y, x, x0=60, bandwidth=5)

    在RDD中的应用:
        分别计算断点左右两侧的局部回归值
        τ = local_linear_regression(..., x0=c, from_right)
          - local_linear_regression(..., x0=c, from_left)
    """
    # TODO: 局部线性回归
    # 步骤1: 计算标准化距离 u = (x - x0) / bandwidth
    # 步骤2: 计算核权重 w = kernel(u)
    # 步骤3: 加权最小二乘回归
    # 步骤4: 返回截距（x0处的拟合值）
    pass


def triangular_kernel(u: float) -> float:
    """
    三角核函数。

    【公式】
    K(u) = (1 - |u|) × 1{|u| ≤ 1}

    【特点】
    - 在u=0处权重最大（值为1）
    - 权重随距离线性递减
    - |u|>1时权重为0
    - 积分为1（归一化核）

    【为什么用三角核】
    - 边界偏误小
    - 在RDD中广泛使用
    - 简单直观

    参数:
        u: 标准化距离（(x - x0) / bandwidth）

    返回:
        核权重（0到1之间）

    示例:
        >>> triangular_kernel(0)     # 1.0 （中心点权重最大）
        >>> triangular_kernel(0.5)   # 0.5
        >>> triangular_kernel(1.0)   # 0.0 （边界权重为0）
        >>> triangular_kernel(1.5)   # 0.0 （超出范围）
    """
    # TODO: 三角核
    # K(u) = (1 - |u|) if |u| ≤ 1 else 0
    pass


def optimal_bandwidth_ik(
    y: np.ndarray,
    x: np.ndarray,
    cutoff: float
) -> float:
    """
    Imbens-Kalyanaraman最优带宽选择（简化版）。

    【最优带宽的权衡】
    - 小带宽：低偏误（更局部），高方差（样本少）
    - 大带宽：高偏误（远离断点），低方差（样本多）

    最优带宽最小化均方误差（MSE）= 偏误² + 方差

    【IK带宽公式（简化）】
    h_opt = C × n^(-1/5) × σ / f(c)

    其中：
    - n：样本量
    - σ：结果变量的标准差
    - f(c)：运行变量在断点处的密度

    【实践中的带宽选择】
    1. 数据驱动方法（IK, CCT）
    2. 敏感性分析（尝试不同带宽）
    3. 报告多个带宽的结果

    参数:
        y: 结果变量
        x: 运行变量
        cutoff: 阈值

    返回:
        最优带宽

    示例:
        >>> h_opt = optimal_bandwidth_ik(y, x, cutoff=60)
        >>> print(f"最优带宽: {h_opt:.2f}")
        >>> tau = sharp_rdd_estimate(y, x, cutoff=60, bandwidth=h_opt)

    注意:
        完整的IK公式较复杂，这里是简化版本
        实际应用推荐使用rdrobust等包
    """
    # TODO: 带宽选择
    # 简化实现：使用经验公式
    # h = 1.84 × std(X) × n^(-1/5)
    # 或者使用Silverman法则的变体
    pass


def fuzzy_rdd_estimate(
    y: np.ndarray,
    d: np.ndarray,
    x: np.ndarray,
    cutoff: float,
    bandwidth: float
) -> float:
    """
    模糊断点回归估计。

    【模糊断点的情况】
    超过阈值不是必然接受处理，而是增加接受处理的概率。
    例如：
    - 超过分数线"有资格"申请奖学金，但不是所有人都申请
    - 达到补贴标准，但需要自己申请

    【估计策略】
    类似于工具变量法，用断点作为处理的工具：
    - 第一阶段：断点对处理的影响
    - 简化式：断点对结果的影响
    - 处理效应 = 简化式 / 第一阶段

    τ_fuzzy = [E(Y|X=c⁺) - E(Y|X=c⁻)] / [E(D|X=c⁺) - E(D|X=c⁻)]

    【LATE解释】
    模糊RDD估计的是局部平均处理效应（LATE）：
    对那些"因为超过阈值而改变处理状态"的人的效应

    参数:
        y: 结果变量
        d: 处理变量（0/1，不再是X≥c决定）
        x: 运行变量
        cutoff: 阈值
        bandwidth: 带宽

    返回:
        LATE估计

    示例:
        奖学金资格（60分以上）与实际获得奖学金
        >>> tau = fuzzy_rdd_estimate(grades, scholarship, scores, 60, 10)
        >>> print(f"奖学金的LATE: {tau:.2f}")

    对比精确断点:
        精确断点：E(D|X=c⁺) - E(D|X=c⁻) = 1
        模糊断点：E(D|X=c⁺) - E(D|X=c⁻) < 1
    """
    # TODO: Fuzzy RDD
    # 步骤1: 估计断点处Y的跳跃（简化式效应）
    #        用sharp_rdd_estimate(y, x, cutoff, bandwidth)
    # 步骤2: 估计断点处D的跳跃（第一阶段效应）
    #        用sharp_rdd_estimate(d, x, cutoff, bandwidth)
    # 步骤3: τ = Y的跳跃 / D的跳跃
    pass


def mccrary_test(x: np.ndarray, cutoff: float) -> tuple[float, float]:
    """
    McCrary密度检验。

    【检验目的】
    检验运行变量在断点处的密度是否有跳跃。
    如果有跳跃，说明存在操纵行为。

    【操纵的例子】
    - 学生知道60分是奖学金分数线，老师可能把59分改成60分
    - 这会导致60分附近的密度异常高
    - 密度跳跃说明处理分配不再是"局部随机"的

    【检验方法】
    1. 估计断点左右两侧的密度函数
    2. 比较断点处的密度是否有跳跃
    3. 检验跳跃是否显著

    H₀：断点处密度连续（无操纵）
    H₁：断点处密度不连续（存在操纵）

    参数:
        x: 运行变量
        cutoff: 阈值

    返回:
        (密度跳跃估计, p值)

    示例:
        >>> jump, pval = mccrary_test(scores, cutoff=60)
        >>> if pval < 0.05:
        ...     print("警告：可能存在操纵，RDD假设可能被违反")

    可视化建议:
        绘制运行变量的直方图，观察断点处是否有异常
    """
    # TODO: McCrary检验
    # 简化实现:
    # 步骤1: 分别估计断点左右的密度（用直方图或核密度估计）
    # 步骤2: 计算断点处的密度跳跃
    # 步骤3: 检验跳跃是否显著
    pass


def placebo_cutoff_test(
    y: np.ndarray,
    x: np.ndarray,
    true_cutoff: float,
    placebo_cutoffs: list[float],
    bandwidth: float
) -> list[float]:
    """
    安慰剂断点检验。

    【检验思想】
    在没有真正断点的位置估计"处理效应"，
    如果RDD有效，这些安慰剂效应应该接近零。

    【检验方法】
    1. 在真正阈值的一侧选择多个"假阈值"
    2. 在每个假阈值处估计"效应"
    3. 这些效应应该不显著地不同于零

    【常见做法】
    - 只使用真阈值一侧的数据（避免真效应的污染）
    - 选择多个假阈值（如真阈值附近的中位数、四分位数）
    - 报告假阈值处效应的分布

    参数:
        y: 结果变量
        x: 运行变量
        true_cutoff: 真实阈值
        placebo_cutoffs: 安慰剂阈值列表
        bandwidth: 带宽

    返回:
        安慰剂效应估计列表

    示例:
        真阈值60分，在40分、50分、70分、80分处检验
        >>> placebos = [40, 50, 70, 80]
        >>> effects = placebo_cutoff_test(y, x, 60, placebos, 10)
        >>> print(f"安慰剂效应: {effects}")
        # 应该都接近0

    解释:
        如果安慰剂效应显著不为零，可能说明：
        1. 存在未观测的混杂因素
        2. 运行变量与结果有非线性关系
        3. RDD模型设定不当
    """
    # TODO: 安慰剂检验
    # 对每个placebo_cutoff:
    #   1. 只使用真阈值一侧的数据
    #   2. 估计该点的"效应"
    # 返回所有安慰剂效应
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
