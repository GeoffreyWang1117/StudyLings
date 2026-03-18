# EXERCISE: iv1
# DIFFICULTY: ★★★★★
# TOPIC: 工具变量与内生性
#
# 说明：
# 工具变量（Instrumental Variables, IV）是计量经济学中解决内生性问题的核心方法。
# 内生性会导致OLS估计量有偏且不一致，而IV方法可以得到一致的因果效应估计。
#
# 【理论背景】
# 考虑线性回归模型：Y = β₀ + β₁X + ε
#
# OLS的关键假设：E[ε|X] = 0（外生性）
# 若该假设不成立，即Cov(X, ε) ≠ 0，则称X为内生变量。
#
# 【内生性的来源】
#
# 1. 遗漏变量偏误（Omitted Variable Bias）
#    - 真实模型：Y = β₀ + β₁X + β₂Z + ε
#    - 若遗漏Z，且Z与X相关，则X变为内生
#    - 例：教育回报率中遗漏能力变量
#    - 偏误方向：取决于Z与X、Y的相关方向
#
# 2. 测量误差（Measurement Error）
#    - 真实模型：Y = β₀ + β₁X* + ε
#    - 观测：X = X* + u（含测量误差）
#    - 导致经典衰减偏误（attenuation bias）
#    - 例：自报收入存在误差
#
# 3. 联立方程偏误（Simultaneity Bias）
#    - 供给与需求同时决定价格和数量
#    - Y影响X的同时，X也影响Y
#    - 例：价格与需求量的双向因果
#
# 4. 样本选择偏误（Sample Selection Bias）
#    - 样本非随机选择
#    - 选择过程与误差项相关
#    - 例：只观察到就业者的工资
#
# 【工具变量法的基本思想】
# 找到一个变量Z（工具变量），满足：
#
# 1. 相关性（Relevance）：Cov(Z, X) ≠ 0
#    - Z与内生变量X相关
#    - 可通过第一阶段回归检验
#
# 2. 外生性（Exogeneity）：Cov(Z, ε) = 0
#    - Z与误差项不相关
#    - Z仅通过X影响Y，无直接效应
#    - 无法直接检验（排除限制）
#
# 【两阶段最小二乘（2SLS）】
# 2SLS是IV估计的标准方法：
#
# 第一阶段（First Stage）：
#   X = π₀ + π₁Z + v
#   得到X的拟合值 X̂ = π̂₀ + π̂₁Z
#
# 第二阶段（Second Stage）：
#   Y = β₀ + β₁X̂ + ε
#   用X̂替代X进行回归
#
# 【2SLS的直觉】
# X̂ 是X中与Z相关的部分（外生变异）
# 去除了X中与ε相关的内生部分
# 第二阶段只使用X的外生变异来估计β₁
#
# 【弱工具变量问题】
# 当Z与X的相关性弱时（第一阶段F统计量小）：
# - 2SLS偏误可能比OLS更严重
# - 标准误估计不可靠
# - 经验法则：F > 10
# - Stock-Yogo临界值提供更精确的判断标准
#
# 【过度识别检验】
# 当工具变量数 > 内生变量数时（过度识别）：
# - 可以检验工具变量的外生性
# - Sargan/Hansen J检验
# - H₀：所有工具变量都外生
# - 若拒绝H₀，说明至少一个工具变量无效
#
# 【局部平均处理效应（LATE）】
# 当处理D是二元变量，工具变量Z也是二元时：
# IV估计的是LATE = E[Y₁ - Y₀ | Compliers]
#
# - Compliers：受Z影响改变处理状态的个体
# - Never-takers：无论Z如何都不接受处理
# - Always-takers：无论Z如何都接受处理
# - Defiers：Z=1时不处理，Z=0时处理（假设不存在）
#
# LATE与ATE（平均处理效应）可能不同！
#
# 任务：
# 1. 实现两阶段最小二乘估计
# 2. 检验工具变量的有效性（弱工具变量检验）
# 3. 实现过度识别检验
# 4. 理解LATE的解释
#
# HINT1: 弱工具变量导致严重偏误，检查第一阶段F统计量
# HINT2: 恰好识别时无法检验外生性，需要理论支持
# HINT3: IV估计的标准误通常大于OLS

import numpy as np


def first_stage_regression(z: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    IV第一阶段回归。

    【模型】
    X = π₀ + π₁Z₁ + π₂Z₂ + ... + v
    或矩阵形式：X = Zπ + v

    【OLS估计】
    π̂ = (Z'Z)⁻¹Z'X
    X̂ = Z(Z'Z)⁻¹Z'X = Pz × X

    其中 Pz = Z(Z'Z)⁻¹Z' 是投影矩阵

    【经济含义】
    第一阶段将内生变量X分解为两部分：
    - X̂：与工具变量Z相关的部分（外生变异）
    - v = X - X̂：与Z无关的部分（可能包含内生性）

    参数:
        z: 工具变量矩阵，形状 (n, k)
           应包含常数列（如果需要截距）
           k = 工具变量数量（含常数）
        x: 内生变量，形状 (n,) 或 (n, 1)

    返回:
        (系数估计π̂, 拟合值X̂)
        - π̂: 形状 (k,)
        - X̂: 形状 (n,)

    示例:
        >>> n = 1000
        >>> z = np.column_stack([np.ones(n), np.random.randn(n)])
        >>> x = z[:, 1] * 0.5 + np.random.randn(n)  # 相关性0.5
        >>> pi, x_fitted = first_stage_regression(z, x)
        >>> print(f"第一阶段系数: {pi}")

    注意:
        - 检查Z是否包含常数项
        - 检查Z的列数是否至少等于内生变量数（阶条件）
    """
    # TODO: 第一阶段回归
    # 步骤1: 计算 π̂ = (Z'Z)⁻¹Z'X
    #        使用 np.linalg.lstsq 或 np.linalg.solve
    # 步骤2: 计算 X̂ = Z @ π̂
    pass


def second_stage_regression(x_fitted: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    IV第二阶段回归。

    【模型】
    Y = β₀ + β₁X̂ + ε

    【OLS估计】
    β̂ = (X̂'X̂)⁻¹X̂'Y

    【注意事项】
    第二阶段直接用OLS得到的标准误是错误的！
    正确的标准误需要使用原始X而非X̂计算残差。

    正确的残差：ε̂ = Y - Xβ̂（用原始X）
    而非：Y - X̂β̂

    参数:
        x_fitted: 第一阶段拟合值X̂，形状 (n,) 或 (n, p)
                  应包含常数列
        y: 因变量，形状 (n,)

    返回:
        系数估计β̂，形状 (p,)

    示例:
        >>> beta = second_stage_regression(x_fitted_with_const, y)
        >>> print(f"IV估计: {beta}")

    重要:
        实际应用中，应使用完整的2SLS程序计算正确的标准误
    """
    # TODO: 第二阶段回归
    # 提示：β̂ = (X̂'X̂)⁻¹X̂'Y
    pass


def two_stage_least_squares(
    y: np.ndarray,
    x: np.ndarray,
    z: np.ndarray
) -> np.ndarray:
    """
    两阶段最小二乘估计（完整实现）。

    【算法步骤】
    1. 第一阶段：用Z回归X，得到X̂
    2. 第二阶段：用X̂回归Y，得到β̂

    【等价公式】
    2SLS估计量也可以写为：
    β̂_IV = (X'Pz X)⁻¹ X'Pz Y
    其中 Pz = Z(Z'Z)⁻¹Z'

    或者使用IV公式：
    β̂_IV = (Z'X)⁻¹ Z'Y（恰好识别时）

    【与OLS的对比】
    OLS: β̂_OLS = (X'X)⁻¹ X'Y
    IV:  β̂_IV  = (X'Pz X)⁻¹ X'Pz Y

    参数:
        y: 因变量，形状 (n,)
        x: 自变量矩阵，形状 (n, p)
           包含常数列和内生变量
        z: 工具变量矩阵，形状 (n, k)
           包含常数列和工具变量
           要求 k ≥ p（阶条件）

    返回:
        2SLS系数估计β̂，形状 (p,)

    示例:
        教育回报率，用父母教育作为工具变量
        >>> y = wage
        >>> x = np.column_stack([np.ones(n), education])
        >>> z = np.column_stack([np.ones(n), parent_education])
        >>> beta_iv = two_stage_least_squares(y, x, z)
        >>> print(f"教育回报率IV估计: {beta_iv[1]:.3f}")

    注意:
        - 确保z的列数 ≥ x的列数
        - 外生变量应同时出现在x和z中
    """
    # TODO: 2SLS估计
    # 方法1: 两步法
    #   步骤1: X̂ = Z(Z'Z)⁻¹Z'X
    #   步骤2: β̂ = (X̂'X̂)⁻¹X̂'Y
    #
    # 方法2: 一步法
    #   Pz = Z @ np.linalg.inv(Z.T @ Z) @ Z.T
    #   β̂ = np.linalg.inv(X.T @ Pz @ X) @ X.T @ Pz @ y
    pass


def first_stage_f_statistic(
    z: np.ndarray,
    x: np.ndarray,
    excluded_instruments: int
) -> float:
    """
    计算第一阶段F统计量。

    【检验目的】
    检验工具变量与内生变量的相关性强度。
    H₀：排除的工具变量系数全为零（弱工具变量）
    H₁：至少一个系数不为零

    【F统计量】
    F = [(R²_full - R²_reduced) / q] / [(1 - R²_full) / (n - k)]

    其中：
    - R²_full：完整模型（含排除工具变量）的R²
    - R²_reduced：受限模型（不含排除工具变量）的R²
    - q：排除的工具变量数量
    - k：完整模型的参数数量

    【经验法则】
    - F < 10：弱工具变量，IV估计可能严重偏误
    - F > 10：工具变量足够强
    - Stock-Yogo临界值提供更精确的判断

    【弱工具变量的后果】
    - 2SLS估计量有限样本偏误大
    - 偏误方向接近OLS
    - t统计量和置信区间不可靠

    参数:
        z: 工具变量矩阵（含常数和所有工具变量）
        x: 内生变量
        excluded_instruments: 排除的工具变量数量
                             （不包括常数和外生变量）

    返回:
        第一阶段F统计量

    示例:
        >>> z = np.column_stack([np.ones(n), z1, z2])  # 常数 + 2个工具变量
        >>> f_stat = first_stage_f_statistic(z, x, excluded_instruments=2)
        >>> print(f"第一阶段F统计量: {f_stat:.2f}")
        >>> if f_stat < 10:
        ...     print("警告：弱工具变量")

    参考:
        Stock & Yogo (2005) 提供了不同情况下的临界值表
    """
    # TODO: 计算F统计量
    # 步骤1: 进行完整的第一阶段回归，计算R²_full
    # 步骤2: 只用外生变量（不含排除的工具变量）回归，计算R²_reduced
    # 步骤3: 计算F统计量
    pass


def is_weak_instrument(f_statistic: float, threshold: float = 10) -> bool:
    """
    判断是否为弱工具变量。

    【Stock-Yogo检验】
    弱工具变量检验有两种形式：

    1. 相对偏误检验：
       检验IV相对偏误是否小于OLS偏误的某个比例
       临界值取决于工具变量数量和可接受的偏误比例

    2. 规模扭曲检验：
       检验名义5%的Wald检验实际规模是否接近5%
       临界值取决于工具变量数量和可接受的规模扭曲

    【经验法则】
    - 单一内生变量、单一工具变量：F > 10
    - 这是10%相对偏误的近似临界值
    - 更严格的标准可能要求F > 16.38

    参数:
        f_statistic: 第一阶段F统计量
        threshold: 判断阈值（默认10）

    返回:
        True表示弱工具变量（F < threshold）
        False表示工具变量足够强

    示例:
        >>> if is_weak_instrument(f_stat):
        ...     print("弱工具变量，考虑使用其他方法")
        ... else:
        ...     print("工具变量足够强，可以使用2SLS")

    备选方法:
        若工具变量弱，可考虑：
        - LIML（有限信息最大似然）
        - Fuller修正
        - 弱工具稳健推断（Anderson-Rubin检验）
    """
    # TODO: 判断弱工具变量
    # 提示：return f_statistic < threshold
    pass


def sargan_test(
    residuals: np.ndarray,
    z: np.ndarray,
    n_instruments: int,
    n_endogenous: int
) -> tuple[float, float]:
    """
    Sargan过度识别检验。

    【检验目的】
    当工具变量数 > 内生变量数（过度识别）时，
    检验所有工具变量是否都满足外生性假设。

    【检验原理】
    如果所有工具变量都外生，2SLS残差应与所有工具变量不相关。
    Sargan统计量检验这一条件：

    J = n × R²（用残差对Z回归的R²）

    H₀：Cov(Z, ε) = 0（所有工具变量外生）
    H₁：至少一个工具变量不外生

    在H₀下：J ~ χ²(q)
    其中 q = 工具变量数 - 内生变量数（过度识别的自由度）

    【检验结果解读】
    - 不拒绝H₀：不能否定所有IV外生（但不能证明外生）
    - 拒绝H₀：至少一个IV无效

    【局限性】
    - 若所有IV都与误差项以相同方式相关，检验无效
    - 不能告诉我们哪个IV有问题
    - 恰好识别时无法检验

    参数:
        residuals: 2SLS残差 ε̂ = Y - X @ β̂_IV
        z: 工具变量矩阵（含常数）
        n_instruments: 工具变量数量（不含常数）
        n_endogenous: 内生变量数量

    返回:
        (J统计量, p值)

    示例:
        >>> residuals = y - x @ beta_iv
        >>> j_stat, p_value = sargan_test(residuals, z, n_instruments=2, n_endogenous=1)
        >>> print(f"Sargan J统计量: {j_stat:.3f}, p值: {p_value:.3f}")
        >>> if p_value < 0.05:
        ...     print("拒绝H₀：存在无效工具变量")

    Hansen J检验:
        与Sargan检验类似，但在异方差下也有效
    """
    # TODO: Sargan检验
    # 步骤1: 用残差对Z回归：ε̂ = Zγ + u
    # 步骤2: 计算R²
    # 步骤3: J = n × R²
    # 步骤4: p值 = 1 - χ².cdf(J, df=n_instruments - n_endogenous)
    pass


def local_average_treatment_effect(
    y: np.ndarray,
    d: np.ndarray,
    z: np.ndarray
) -> float:
    """
    计算局部平均处理效应（LATE）。

    【LATE定义】
    当处理D和工具变量Z都是二元变量时：

    LATE = [E(Y|Z=1) - E(Y|Z=0)] / [E(D|Z=1) - E(D|Z=0)]
         = ITT / (第一阶段效应)

    其中ITT（Intent-to-Treat）= E(Y|Z=1) - E(Y|Z=0)

    【LATE的解释】
    LATE估计的是"顺从者"（Compliers）的平均处理效应：
    - 顺从者：当Z=1时接受处理，Z=0时不接受的人

    四种人群：
    - Always-takers：D(0)=D(1)=1
    - Never-takers：D(0)=D(1)=0
    - Compliers：D(0)=0, D(1)=1
    - Defiers：D(0)=1, D(1)=0（假设不存在，单调性假设）

    【LATE vs ATE】
    LATE只识别顺从者的效应，可能与：
    - ATE（平均处理效应）
    - ATT（处理组平均处理效应）
    - ATU（控制组平均处理效应）
    都不同！

    【经典例子】
    - 越战抽签与教育：Z=抽签号码，D=服役，Y=收入
    - 择校券：Z=券中签，D=上私校，Y=成绩
    - 法官随机分配：Z=严厉法官，D=入狱，Y=再犯

    参数:
        y: 结果变量，形状 (n,)
        d: 处理变量（0/1），形状 (n,)
        z: 工具变量（0/1），形状 (n,)

    返回:
        LATE估计

    示例:
        >>> # 随机鼓励设计
        >>> late = local_average_treatment_effect(y, d, z)
        >>> print(f"LATE = {late:.3f}")
        >>> # 这是对"因鼓励而接受处理"的人的处理效应

    注意:
        - 需要单调性假设（无defiers）
        - 需要排除限制（Z只通过D影响Y）
        - 需要独立性（Z与潜在结果独立）
    """
    # TODO: 计算LATE
    # 公式：LATE = [E(Y|Z=1) - E(Y|Z=0)] / [E(D|Z=1) - E(D|Z=0)]
    # 步骤1: 计算 E(Y|Z=1) 和 E(Y|Z=0)
    # 步骤2: 计算 E(D|Z=1) 和 E(D|Z=0)
    # 步骤3: LATE = 差值比
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
