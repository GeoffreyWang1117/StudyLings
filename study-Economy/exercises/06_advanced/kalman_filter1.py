# EXERCISE: kalman_filter1
# DIFFICULTY: ★★★★★
# TOPIC: 卡尔曼滤波与状态空间模型
#
# 说明：
# 卡尔曼滤波（Kalman Filter）是估计动态系统状态的最优方法，
# 广泛应用于信号处理、导航、控制系统以及经济学中的时间序列分析。
#
# 【理论背景】
# 许多经济变量是不可直接观测的（潜在变量），例如：
# - 潜在GDP（Potential GDP）
# - 自然利率（Natural Rate of Interest）
# - 通胀预期（Inflation Expectations）
# - 资本存量（Capital Stock）
#
# 状态空间模型提供了处理这些问题的统一框架。
#
# 【状态空间模型（State Space Model）】
#
# 模型由两个方程组成：
#
# 1. 状态方程（State/Transition Equation）：
#    x_t = F × x_{t-1} + w_t
#    描述状态如何随时间演变
#
# 2. 观测方程（Observation/Measurement Equation）：
#    y_t = H × x_t + v_t
#    描述观测值与状态的关系
#
# 其中：
# - x_t：状态向量（n_state × 1），不可直接观测
# - y_t：观测向量（n_obs × 1），可直接观测
# - F：状态转移矩阵（n_state × n_state）
# - H：观测矩阵（n_obs × n_state）
# - w_t ~ N(0, Q)：过程噪声（状态扰动）
# - v_t ~ N(0, R)：观测噪声（测量误差）
#
# 【卡尔曼滤波的目标】
# 给定观测值 y_1, y_2, ..., y_t，
# 估计状态 x_t 及其不确定性。
#
# 三种估计问题：
# 1. 滤波（Filtering）：估计 x_{t|t}（用y_1,...,y_t估计x_t）
# 2. 预测（Prediction）：估计 x_{t+h|t}（预测未来状态）
# 3. 平滑（Smoothing）：估计 x_{t|T}（用全样本估计历史状态）
#
# 【卡尔曼滤波算法】
#
# 初始化：x_{0|0}（初始状态估计），P_{0|0}（初始协方差）
#
# 对于每个时期 t = 1, 2, ..., T：
#
# ===== 预测步骤（Prediction/Time Update）=====
# 状态预测：
#   x̂_{t|t-1} = F × x̂_{t-1|t-1}
#
# 协方差预测：
#   P_{t|t-1} = F × P_{t-1|t-1} × F' + Q
#
# ===== 更新步骤（Update/Measurement Update）=====
# 预测残差（Innovation）：
#   ν_t = y_t - H × x̂_{t|t-1}
#
# 残差协方差：
#   S_t = H × P_{t|t-1} × H' + R
#
# 卡尔曼增益：
#   K_t = P_{t|t-1} × H' × S_t^{-1}
#
# 状态更新：
#   x̂_{t|t} = x̂_{t|t-1} + K_t × ν_t
#
# 协方差更新：
#   P_{t|t} = (I - K_t × H) × P_{t|t-1}
#
# 【卡尔曼增益的直觉】
# K_t 在模型预测和新观测之间做加权平均：
# - 如果 R 大（观测噪声大）：K 小，更相信模型预测
# - 如果 Q 大（状态波动大）：K 大，更相信新观测
# - K = P_{t|t-1}H'(HP_{t|t-1}H'+R)^{-1}
#
# 【卡尔曼平滑器（Kalman Smoother）】
# 使用未来信息改进历史状态估计。
#
# 后向递推（Rauch-Tung-Striebel Smoother）：
# J_t = P_{t|t} × F' × P_{t+1|t}^{-1}
# x̂_{t|T} = x̂_{t|t} + J_t × (x̂_{t+1|T} - x̂_{t+1|t})
# P_{t|T} = P_{t|t} + J_t × (P_{t+1|T} - P_{t+1|t}) × J_t'
#
# 【经济学应用】
#
# 1. 估计潜在产出（Potential Output）
#    状态：[趋势, 增长率]
#    观测：实际GDP
#
# 2. 估计自然利率（r*）
#    Laubach-Williams模型
#
# 3. 提取共同因子（Factor Models）
#    从多个序列提取共同趋势
#
# 4. 动态因子模型（Dynamic Factor Model）
#    结合横截面和时间序列信息
#
# 5. DSGE模型估计
#    线性化DSGE模型是状态空间形式
#
# 任务：
# 1. 实现卡尔曼滤波的预测和更新步骤
# 2. 实现完整的卡尔曼滤波算法
# 3. 实现卡尔曼平滑器
# 4. 估计潜在产出
#
# HINT1: 矩阵运算注意维度匹配
# HINT2: 数值稳定性很重要（使用正定性保证的更新公式）
# HINT3: 参数估计可用最大似然法

import numpy as np


def kalman_predict(
    x: np.ndarray,
    p: np.ndarray,
    f: np.ndarray,
    q: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    卡尔曼滤波预测步骤（Time Update）。

    【公式】
    状态预测：x̂_{t|t-1} = F × x̂_{t-1|t-1}
    协方差预测：P_{t|t-1} = F × P_{t-1|t-1} × F' + Q

    【直觉】
    - 状态预测：根据状态方程向前推进
    - 协方差增加：预测增加不确定性（加上过程噪声Q）

    参数:
        x: 当前状态估计 x̂_{t-1|t-1}，形状 (n_state,)
        p: 当前协方差矩阵 P_{t-1|t-1}，形状 (n_state, n_state)
        f: 状态转移矩阵 F，形状 (n_state, n_state)
        q: 过程噪声协方差 Q，形状 (n_state, n_state)

    返回:
        (预测状态 x̂_{t|t-1}, 预测协方差 P_{t|t-1})

    示例:
        >>> # 简单随机游走模型
        >>> x = np.array([100.0])  # 当前估计
        >>> p = np.array([[1.0]])  # 当前不确定性
        >>> f = np.array([[1.0]])  # 状态转移（随机游走）
        >>> q = np.array([[0.1]])  # 过程噪声
        >>> x_pred, p_pred = kalman_predict(x, p, f, q)
        >>> print(f"预测状态: {x_pred}, 预测方差: {p_pred}")
    """
    # TODO: 预测步骤
    # x_pred = F @ x
    # p_pred = F @ p @ F.T + q
    pass


def kalman_update(
    x_pred: np.ndarray,
    p_pred: np.ndarray,
    y: np.ndarray,
    h: np.ndarray,
    r: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    卡尔曼滤波更新步骤（Measurement Update）。

    【公式】
    残差：ν = y - H × x̂_{t|t-1}
    残差协方差：S = H × P_{t|t-1} × H' + R
    卡尔曼增益：K = P_{t|t-1} × H' × S^{-1}
    状态更新：x̂_{t|t} = x̂_{t|t-1} + K × ν
    协方差更新：P_{t|t} = (I - K × H) × P_{t|t-1}

    【直觉】
    - 残差ν：观测与预测的差异（"惊喜"）
    - 卡尔曼增益K：分配给新观测的权重
    - 协方差减少：新观测减少不确定性

    【数值稳定性】
    可用Joseph形式更新协方差：
    P = (I - KH)P(I - KH)' + KRK'
    保证正定性

    参数:
        x_pred: 预测状态 x̂_{t|t-1}
        p_pred: 预测协方差 P_{t|t-1}
        y: 观测值 y_t
        h: 观测矩阵 H
        r: 观测噪声协方差 R

    返回:
        (更新状态 x̂_{t|t}, 更新协方差 P_{t|t}, 卡尔曼增益 K)

    示例:
        >>> y = np.array([101.5])  # 观测到101.5
        >>> h = np.array([[1.0]])  # 直接观测状态
        >>> r = np.array([[0.5]])  # 观测噪声
        >>> x_upd, p_upd, k = kalman_update(x_pred, p_pred, y, h, r)
    """
    # TODO: 更新步骤
    # 步骤1: 计算残差 ν = y - H @ x_pred
    # 步骤2: 计算残差协方差 S = H @ p_pred @ H.T + r
    # 步骤3: 计算卡尔曼增益 K = p_pred @ H.T @ np.linalg.inv(S)
    # 步骤4: 更新状态 x = x_pred + K @ ν
    # 步骤5: 更新协方差 p = (I - K @ H) @ p_pred
    pass


def kalman_filter(
    observations: np.ndarray,
    f: np.ndarray,
    h: np.ndarray,
    q: np.ndarray,
    r: np.ndarray,
    x0: np.ndarray,
    p0: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    完整卡尔曼滤波。

    【算法流程】
    for t = 1, 2, ..., T:
        1. 预测：(x_pred, p_pred) = predict(x_{t-1}, p_{t-1})
        2. 更新：(x_t, p_t) = update(x_pred, p_pred, y_t)
        3. 存储：filtered_states[t] = x_t

    【初始化】
    - 精确初始化：已知初始状态的分布
    - 扩散初始化：初始协方差很大（无信息先验）

    参数:
        observations: 观测序列，形状 (T, n_obs)
        f: 状态转移矩阵
        h: 观测矩阵
        q: 过程噪声协方差
        r: 观测噪声协方差
        x0: 初始状态估计
        p0: 初始协方差

    返回:
        (滤波状态序列, 滤波协方差序列)
        - 状态序列：形状 (T, n_state)
        - 协方差序列：形状 (T, n_state, n_state)

    示例:
        >>> # 局部水平模型（Local Level Model）
        >>> T = 100
        >>> f = np.array([[1.0]])  # 随机游走
        >>> h = np.array([[1.0]])  # 直接观测
        >>> q = np.array([[0.1]])  # 状态噪声
        >>> r = np.array([[1.0]])  # 观测噪声
        >>> x0 = np.array([0.0])
        >>> p0 = np.array([[10.0]])
        >>>
        >>> filtered_states, filtered_covs = kalman_filter(y, f, h, q, r, x0, p0)

    处理缺失值:
        如果某时期观测缺失，可跳过更新步骤，只做预测
    """
    # TODO: 完整滤波
    # 初始化存储数组
    # for t in range(T):
    #     预测步骤
    #     更新步骤
    #     存储结果
    pass


def kalman_smoother(
    filtered_states: np.ndarray,
    filtered_covs: np.ndarray,
    f: np.ndarray
) -> np.ndarray:
    """
    卡尔曼平滑器（后向递推）。

    【平滑的目的】
    利用全样本信息（包括未来观测）来改进历史状态估计。

    【Rauch-Tung-Striebel Smoother】
    从最后一期 T 向前递推：

    J_t = P_{t|t} × F' × P_{t+1|t}^{-1}
    x̂_{t|T} = x̂_{t|t} + J_t × (x̂_{t+1|T} - x̂_{t+1|t})
    P_{t|T} = P_{t|t} + J_t × (P_{t+1|T} - P_{t+1|t}) × J_t'

    【滤波 vs 平滑】
    - 滤波：实时估计，只用过去信息
    - 平滑：事后分析，用全部信息
    - 平滑估计更精确，协方差更小

    参数:
        filtered_states: 滤波状态，形状 (T, n_state)
        filtered_covs: 滤波协方差，形状 (T, n_state, n_state)
        f: 状态转移矩阵

    返回:
        平滑状态序列，形状 (T, n_state)

    示例:
        >>> smoothed = kalman_smoother(filtered_states, filtered_covs, f)
        >>> # smoothed比filtered更平滑，波动更小

    应用:
        - 估计潜在GDP时，平滑器给出更可靠的历史估计
        - 参数估计时，用平滑状态计算似然
    """
    # TODO: 平滑器
    # smoothed[-1] = filtered[-1]  # 最后一期相同
    # for t in range(T-2, -1, -1):  # 从T-2到0后向递推
    #     P_pred = f @ filtered_covs[t] @ f.T + q
    #     J = filtered_covs[t] @ f.T @ inv(P_pred)
    #     smoothed[t] = filtered[t] + J @ (smoothed[t+1] - f @ filtered[t])
    pass


def log_likelihood(
    observations: np.ndarray,
    f: np.ndarray,
    h: np.ndarray,
    q: np.ndarray,
    r: np.ndarray,
    x0: np.ndarray,
    p0: np.ndarray
) -> float:
    """
    计算状态空间模型的对数似然。

    【似然函数】
    用于参数估计（最大似然估计）。

    对数似然 = Σ log p(y_t | y_{1:t-1})

    其中 p(y_t | y_{1:t-1}) 是预测密度，
    在卡尔曼滤波中，预测残差服从：
    ν_t ~ N(0, S_t)

    因此：
    log p(y_t | y_{1:t-1}) = -0.5 × (n_obs × log(2π) + log|S_t| + ν_t' S_t^{-1} ν_t)

    【参数估计】
    可以对模型参数（如Q、R中的元素）求导，
    找到最大化对数似然的参数值。

    参数:
        observations: 观测序列
        f, h, q, r: 模型参数矩阵
        x0, p0: 初始条件

    返回:
        对数似然值

    示例:
        >>> ll = log_likelihood(y, f, h, q, r, x0, p0)
        >>> print(f"对数似然: {ll:.2f}")
        >>>
        >>> # 参数估计
        >>> from scipy.optimize import minimize
        >>> def neg_ll(params):
        ...     q = np.array([[params[0]]])
        ...     r = np.array([[params[1]]])
        ...     return -log_likelihood(y, f, h, q, r, x0, p0)
        >>> result = minimize(neg_ll, [0.1, 1.0])

    注意:
        - 需要在卡尔曼滤波过程中累积似然
        - 注意数值稳定性（使用log行列式）
    """
    # TODO: 计算对数似然
    # ll = 0
    # for t in range(T):
    #     预测步骤
    #     计算残差和残差协方差
    #     ll += -0.5 * (log|S| + ν' S^{-1} ν + n_obs*log(2π))
    #     更新步骤
    # return ll
    pass


def estimate_potential_output(
    gdp: np.ndarray,
    signal_to_noise: float = 0.1
) -> np.ndarray:
    """
    使用卡尔曼滤波估计潜在产出。

    【模型设定（局部线性趋势模型）】
    状态向量 x_t = [τ_t, g_t]'
    - τ_t：趋势水平
    - g_t：趋势增长率

    状态方程：
    τ_t = τ_{t-1} + g_{t-1} + w_{τ,t}
    g_t = g_{t-1} + w_{g,t}

    观测方程：
    y_t = τ_t + ε_t

    其中：
    - y_t：观测GDP（对数）
    - ε_t：周期/噪声成分

    【信噪比】
    信噪比 = Var(趋势冲击) / Var(观测噪声)
    - 信噪比小：趋势平滑
    - 信噪比大：趋势波动大

    HP滤波是此模型的特例（信噪比 = 1/1600）

    参数:
        gdp: GDP序列（建议取对数），形状 (T,)
        signal_to_noise: 信噪比（默认0.1）

    返回:
        潜在产出估计，形状 (T,)

    示例:
        >>> gdp_log = np.log(gdp_real)
        >>> potential = estimate_potential_output(gdp_log)
        >>> output_gap = gdp_log - potential  # 产出缺口

    对比HP滤波:
        HP滤波：signal_to_noise = 1/1600（季度数据）
        卡尔曼滤波更灵活，可以估计参数
    """
    # TODO: 估计潜在产出
    # 步骤1: 设定状态空间模型
    #        F = [[1, 1], [0, 1]]
    #        H = [[1, 0]]
    #        Q = [[q_tau, 0], [0, q_g]]
    #        R = [[r]]
    # 步骤2: 根据signal_to_noise设定Q和R
    # 步骤3: 运行卡尔曼滤波（或平滑器）
    # 步骤4: 提取趋势成分
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
