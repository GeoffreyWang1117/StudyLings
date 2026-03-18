# EXERCISE: did1
# DIFFICULTY: ★★★★☆
# TOPIC: 双重差分法
#
# 说明：
# 双重差分法（Difference-in-Differences, DID）是政策评估和因果推断的核心方法，
# 通过比较处理组和对照组在政策前后的变化来识别因果效应。
#
# 【理论背景】
# 评估政策效应的根本问题是"反事实"无法观测：
# - 我们能观测到接受政策的个体在政策后的结果
# - 但无法观测"如果没有政策，同一个体会怎样"
#
# DID的基本思想：
# 用对照组的变化来近似处理组的反事实变化
#
# 【DID的基本设定】
# 两组（处理组T、对照组C）× 两期（政策前、政策后）
#
# 四个均值：
# - Ȳ_T,pre：处理组政策前均值
# - Ȳ_T,post：处理组政策后均值
# - Ȳ_C,pre：对照组政策前均值
# - Ȳ_C,post：对照组政策后均值
#
# 【DID估计量】
# β_DID = (Ȳ_T,post - Ȳ_T,pre) - (Ȳ_C,post - Ȳ_C,pre)
#       = ΔȲ_T - ΔȲ_C
#
# 分解：
# - 第一个差分（Ȳ_T,post - Ȳ_T,pre）：处理组的前后变化
# - 第二个差分：减去对照组的前后变化
# - 剔除了"时间效应"（两组共同的趋势）
#
# 【回归形式】
# Y_it = α + β₁ × Treat_i + β₂ × Post_t + β₃ × (Treat_i × Post_t) + ε_it
#
# 其中：
# - Treat_i：处理组指示变量（处理组=1，对照组=0）
# - Post_t：政策后时期指示变量（政策后=1，政策前=0）
# - β₃：DID估计量，即处理效应
#
# 系数解释：
# - α：对照组政策前均值
# - α + β₁：处理组政策前均值（β₁ = 组间差异）
# - α + β₂：对照组政策后均值（β₂ = 时间效应）
# - α + β₁ + β₂ + β₃：处理组政策后均值
#
# 【关键识别假设】
#
# 平行趋势假设（Parallel Trends）：
# 在没有政策干预的情况下，处理组和对照组的结果变量
# 会沿着相同的趋势变化。
#
# 数学表示：
# E[Y₀,post - Y₀,pre | Treat=1] = E[Y₀,post - Y₀,pre | Treat=0]
#
# 若该假设不成立，DID估计量将有偏。
#
# 【平行趋势检验】
# 虽然无法直接检验（反事实），但可以：
# 1. 检验政策前的趋势是否平行（事件研究法）
# 2. 安慰剂检验：在没有政策的时期检验是否有"效应"
# 3. 图形化展示：绘制两组的趋势图
#
# 【事件研究法（Event Study）】
# 估计相对于政策时点各期的效应：
# Y_it = α + Σ_k β_k × (Treat_i × 1{t=k}) + γ_t + δ_i + ε_it
#
# - 政策前各期的β_k应接近零（平行趋势）
# - 政策后各期的β_k显示动态效应
# - 通常选择政策前一期（k=-1）作为参照期
#
# 【扩展】
#
# 1. 多期DID（面板数据）：
#    Y_it = α_i + γ_t + β × D_it + ε_it
#    - α_i：个体固定效应
#    - γ_t：时间固定效应
#    - D_it：处理指示变量
#
# 2. 交错DID（Staggered DID）：
#    不同单位在不同时点接受处理
#    标准DID可能产生"负权重"问题
#    新方法：Callaway & Sant'Anna, Sun & Abraham
#
# 3. 带协变量的DID：
#    Y_it = α + β₁Treat + β₂Post + β₃(Treat×Post) + X'γ + ε
#
# 任务：
# 1. 实现基本DID估计
# 2. 实现回归形式的DID
# 3. 检验平行趋势
# 4. 计算反事实结果
#
# HINT1: 平行趋势可用政策前数据进行"预趋势检验"
# HINT2: 标准误需要聚类调整（cluster at the treatment level）
# HINT3: 事件研究图是展示结果的有效方式

import numpy as np


def did_simple(
    y_treat_pre: float,
    y_treat_post: float,
    y_control_pre: float,
    y_control_post: float
) -> float:
    """
    简单DID估计量（四个均值的计算）。

    【公式】
    β_DID = (Ȳ_T,post - Ȳ_T,pre) - (Ȳ_C,post - Ȳ_C,pre)

    【等价表达】
    也可以写成：
    β_DID = (Ȳ_T,post - Ȳ_C,post) - (Ȳ_T,pre - Ȳ_C,pre)
    即：政策后的组间差异 - 政策前的组间差异

    【图形理解】
    在Y-时间图上：
    - 处理组从点(pre, Ȳ_T,pre)移动到(post, Ȳ_T,post)
    - 对照组从点(pre, Ȳ_C,pre)移动到(post, Ȳ_C,post)
    - DID测量处理组相对于对照组趋势的额外变化

    参数:
        y_treat_pre: 处理组政策前均值（Ȳ_T,pre）
        y_treat_post: 处理组政策后均值（Ȳ_T,post）
        y_control_pre: 对照组政策前均值（Ȳ_C,pre）
        y_control_post: 对照组政策后均值（Ȳ_C,post）

    返回:
        DID估计量（β_DID）

    示例:
        最低工资对就业的影响
        - 处理组（提高最低工资的州）：就业率从5.0%变为4.8%
        - 对照组（未提高的州）：就业率从5.2%变为5.1%
        >>> did_simple(5.0, 4.8, 5.2, 5.1)
        -0.1  # 最低工资导致就业率额外下降0.1个百分点

    解读:
        处理组下降了0.2个百分点（5.0→4.8）
        对照组下降了0.1个百分点（5.2→5.1）
        处理效应 = -0.2 - (-0.1) = -0.1
    """
    # TODO: 计算DID
    # 提示：β = (Ȳ_T,post - Ȳ_T,pre) - (Ȳ_C,post - Ȳ_C,pre)
    pass


def did_regression(
    y: np.ndarray,
    treat: np.ndarray,
    post: np.ndarray
) -> dict:
    """
    DID回归估计。

    【回归模型】
    Y = α + β₁ × Treat + β₂ × Post + β₃ × (Treat × Post) + ε

    【矩阵形式】
    Y = Xβ + ε
    其中X = [1, Treat, Post, Treat×Post]

    【系数解释】
    - α：E[Y | Treat=0, Post=0] = 对照组政策前均值
    - β₁：E[Y | Treat=1, Post=0] - E[Y | Treat=0, Post=0] = 组间初始差异
    - β₂：E[Y | Treat=0, Post=1] - E[Y | Treat=0, Post=0] = 时间效应
    - β₃：DID估计量 = 处理效应

    【为什么用回归】
    - 便于添加控制变量
    - 便于计算标准误
    - 便于进行假设检验
    - 与面板数据固定效应的联系

    参数:
        y: 结果变量，形状 (n,)
        treat: 处理组指示变量（0/1），形状 (n,)
        post: 政策后指示变量（0/1），形状 (n,)

    返回:
        包含各系数的字典：
        {
            'alpha': α（截距，对照组政策前均值）,
            'beta_treat': β₁（组间差异）,
            'beta_post': β₂（时间效应）,
            'beta_did': β₃（DID估计量）
        }

    示例:
        >>> y = np.array([...])  # 结果变量
        >>> treat = np.array([1,1,1,0,0,0,1,1,1,0,0,0])  # 前6个政策前，后6个政策后
        >>> post = np.array([0,0,0,0,0,0,1,1,1,1,1,1])
        >>> results = did_regression(y, treat, post)
        >>> print(f"处理效应: {results['beta_did']:.3f}")

    注意:
        返回的标准误可能需要聚类调整
    """
    # TODO: DID回归
    # 步骤1: 构建设计矩阵 X = [1, treat, post, treat*post]
    # 步骤2: OLS估计 β = (X'X)⁻¹X'Y
    # 步骤3: 提取各系数
    pass


def parallel_trends_test(
    y_treat_pre: np.ndarray,
    y_control_pre: np.ndarray,
    periods: np.ndarray
) -> tuple[float, float]:
    """
    平行趋势检验。

    【检验思想】
    在政策实施前，比较处理组和对照组的趋势。
    如果趋势平行，两组的斜率差异应该接近零。

    【回归模型】
    对政策前数据：
    Y = α + β₁ × Treat + β₂ × t + β₃ × (Treat × t) + ε

    β₃ 是处理组和对照组斜率的差异。
    H₀：β₃ = 0（平行趋势）
    H₁：β₃ ≠ 0

    【检验的局限性】
    - 只能检验"事前"趋势，不能保证"事后"反事实趋势
    - 统计功效可能不足
    - 不拒绝H₀不等于接受平行趋势

    参数:
        y_treat_pre: 处理组政策前数据（按时间排列的均值或个体数据）
        y_control_pre: 对照组政策前数据
        periods: 时间指示（如[-3, -2, -1]表示政策前3期）

    返回:
        (趋势差异系数β₃, p值)

    示例:
        >>> # 政策前5期的数据
        >>> y_treat = np.array([10.1, 10.5, 10.8, 11.2, 11.5])
        >>> y_control = np.array([9.0, 9.4, 9.7, 10.1, 10.4])
        >>> periods = np.array([-5, -4, -3, -2, -1])
        >>> diff, pval = parallel_trends_test(y_treat, y_control, periods)
        >>> if pval > 0.05:
        ...     print("不能拒绝平行趋势假设")

    可视化建议:
        绘制两组的趋势图，直观判断是否平行
    """
    # TODO: 平行趋势检验
    # 步骤1: 合并两组数据，创建Treat指示变量
    # 步骤2: 回归 Y ~ Treat + t + Treat*t
    # 步骤3: 检验Treat*t的系数是否显著
    pass


def event_study_coefficients(
    y: np.ndarray,
    treat: np.ndarray,
    time_to_treatment: np.ndarray,
    reference_period: int = -1
) -> dict:
    """
    事件研究法系数估计。

    【模型】
    Y_it = α + Σ_{k≠ref} β_k × (Treat_i × 1{t=k}) + γ_t + δ_i + ε_it

    省略参照期（通常k=-1）以避免多重共线性。

    【解释】
    - β_k (k < 0)：政策前各期的"预处理效应"
      应该接近0，否则违反平行趋势
    - β_k (k ≥ 0)：政策后各期的动态处理效应
      β_0是即期效应，β_1是滞后1期效应...

    【图形展示】
    事件研究图：
    - 横轴：相对于政策的时间（k）
    - 纵轴：系数估计值及置信区间
    - 政策前系数应在0附近
    - 政策后系数显示效应的动态演变

    参数:
        y: 结果变量，形状 (n,)
        treat: 处理组指示变量（0/1），形状 (n,)
        time_to_treatment: 相对于处理的时间，形状 (n,)
                          如-2表示处理前2期，0表示处理当期，1表示处理后1期
        reference_period: 参照期（默认-1，即处理前1期）

    返回:
        字典 {period: coefficient}
        如 {-3: 0.02, -2: -0.01, 0: 0.15, 1: 0.18, 2: 0.20}

    示例:
        >>> coefs = event_study_coefficients(y, treat, time_to_treat, reference_period=-1)
        >>> # 绘制事件研究图
        >>> import matplotlib.pyplot as plt
        >>> plt.plot(coefs.keys(), coefs.values())
        >>> plt.axvline(x=-0.5, color='r', linestyle='--')  # 政策时点
        >>> plt.axhline(y=0, color='k', linestyle='-')

    应用:
        - 检验预趋势（政策前系数）
        - 展示动态效应
        - 判断效应的持续性
    """
    # TODO: 事件研究
    # 步骤1: 为每个时期（除参照期外）创建指示变量
    # 步骤2: 创建交互项 Treat × 时期指示
    # 步骤3: 回归估计各期系数
    # 步骤4: 返回系数字典
    pass


def att_did(
    y_treat_pre: np.ndarray,
    y_treat_post: np.ndarray,
    y_control_pre: np.ndarray,
    y_control_post: np.ndarray
) -> float:
    """
    计算处理组平均处理效应（ATT）。

    【ATT的定义】
    ATT = E[Y₁ - Y₀ | D=1]
        = E[Y₁ | D=1] - E[Y₀ | D=1]

    其中：
    - Y₁：接受处理时的潜在结果
    - Y₀：不接受处理时的潜在结果（反事实）
    - D=1：处理组

    【DID如何估计ATT】
    E[Y₁ | D=1, Post=1] = Ȳ_T,post（可观测）
    E[Y₀ | D=1, Post=1] = ?（反事实，不可观测）

    在平行趋势假设下：
    E[Y₀ | D=1, Post=1] - E[Y₀ | D=1, Post=0]
    = E[Y₀ | D=0, Post=1] - E[Y₀ | D=0, Post=0]

    因此：
    E[Y₀ | D=1, Post=1] = Ȳ_T,pre + (Ȳ_C,post - Ȳ_C,pre)

    ATT = Ȳ_T,post - [Ȳ_T,pre + (Ȳ_C,post - Ȳ_C,pre)]
        = (Ȳ_T,post - Ȳ_T,pre) - (Ȳ_C,post - Ȳ_C,pre)
        = DID估计量

    参数:
        y_treat_pre: 处理组政策前数据（个体水平），形状 (n_t_pre,)
        y_treat_post: 处理组政策后数据，形状 (n_t_post,)
        y_control_pre: 对照组政策前数据，形状 (n_c_pre,)
        y_control_post: 对照组政策后数据，形状 (n_c_post,)

    返回:
        ATT估计

    示例:
        >>> att = att_did(y_t_pre, y_t_post, y_c_pre, y_c_post)
        >>> print(f"处理组平均处理效应: {att:.3f}")

    注意:
        DID估计的是ATT，不是ATE
        除非处理效应是同质的
    """
    # TODO: 计算ATT
    # 提示：计算四个均值，然后用DID公式
    pass


def counterfactual_outcome(
    y_treat_pre: float,
    y_control_pre: float,
    y_control_post: float
) -> float:
    """
    计算反事实结果。

    【反事实的定义】
    反事实结果是：如果处理组没有接受处理，
    在政策后他们的预期结果是什么？

    【计算方法】
    在平行趋势假设下：
    Y⁰_T,post = Y_T,pre + (Y_C,post - Y_C,pre)
              = Y_T,pre + ΔY_C

    即：处理组的初始水平 + 对照组的变化

    【图形理解】
    在Y-时间图上：
    - 从处理组政策前的点出发
    - 沿着与对照组相同的斜率延伸
    - 到达的点就是反事实结果

    【处理效应】
    处理效应 = 实际结果 - 反事实结果
            = Y_T,post - Y⁰_T,post

    参数:
        y_treat_pre: 处理组政策前均值
        y_control_pre: 对照组政策前均值
        y_control_post: 对照组政策后均值

    返回:
        处理组的反事实结果（如果没有接受处理的预期结果）

    示例:
        处理组政策前收入5万，对照组从4.5万涨到4.8万
        >>> counterfactual = counterfactual_outcome(5.0, 4.5, 4.8)
        5.3  # 如果没有政策，处理组预期收入5.3万

        如果处理组实际收入是5.5万
        处理效应 = 5.5 - 5.3 = 0.2万

    应用:
        - 政策效果评估
        - 损失计算
        - 情景分析
    """
    # TODO: 计算反事实
    # 公式：Y⁰_T,post = Y_T,pre + (Y_C,post - Y_C,pre)
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
