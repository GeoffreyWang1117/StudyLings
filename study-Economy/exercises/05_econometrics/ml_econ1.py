# EXERCISE: ml_econ1
# DIFFICULTY: ★★★★★
# TOPIC: 机器学习与因果推断
#
# 说明：
# 机器学习（Machine Learning, ML）与计量经济学的融合是当前研究的前沿领域。
# ML方法为处理高维数据、变量选择、非线性关系提供了强大工具，
# 但在因果推断中需要特殊的适配。
#
# 【机器学习 vs 传统计量经济学】
#
# 目标的差异：
# - 机器学习：预测（Prediction），最小化样本外误差
# - 计量经济学：因果推断（Causal Inference），估计因果效应
#
# 方法论差异：
# - ML：正则化、交叉验证、模型集成
# - 计量：无偏估计、假设检验、结构模型
#
# 核心权衡：
# - ML：偏误-方差权衡（允许一些偏误来降低方差）
# - 计量：希望得到无偏或一致估计
#
# 【LASSO回归（Least Absolute Shrinkage and Selection Operator）】
#
# LASSO目标函数：
# L(β) = (1/2n)||Y - Xβ||² + λ||β||₁
#
# 其中：
# - (1/2n)||Y - Xβ||²：OLS损失函数
# - λ||β||₁ = λΣ|β_j|：L1正则化惩罚
# - λ：正则化参数（调节惩罚强度）
#
# LASSO的特性：
# 1. 变量选择：可以将某些系数精确地缩减到0
# 2. 防止过拟合：通过惩罚限制模型复杂度
# 3. 处理高维数据：p > n 的情况也适用
#
# LASSO的局限：
# - 估计有偏（正则化引入偏误）
# - 用于因果推断需要特殊处理
#
# 【双机器学习（Double/Debiased Machine Learning, DML）】
#
# Chernozhukov et al. (2018) 提出的框架。
#
# 基本思想：
# 通过"残差化"来分离控制变量的影响，使ML方法可用于因果推断。
#
# 模型设定：
# Y = D × θ + g(X) + ε     （结果方程）
# D = m(X) + v             （处理方程）
#
# 其中：
# - θ：感兴趣的因果效应
# - g(X)：控制变量对Y的影响（允许非线性）
# - m(X)：控制变量对D的影响
#
# DML步骤（Partial Linear Model）：
# 1. 用ML方法预测Y，得到残差 Ỹ = Y - Ê[Y|X]
# 2. 用ML方法预测D，得到残差 D̃ = D - Ê[D|X]
# 3. 回归 Ỹ ~ D̃ 得到 θ̂
#
# 为什么有效：
# - 去除了X对Y和D的混杂影响
# - 残差 D̃ 是D中与X无关的部分（外生变异）
# - 类似于FWL定理的思想
#
# 【样本分割（Sample Splitting）】
#
# DML的关键技术：交叉拟合（Cross-Fitting）
#
# 问题：如果用全样本训练ML模型再用同样本预测，会有过拟合偏误。
#
# 解决：将样本分成K折
# - 用K-1折训练ML模型
# - 用剩余1折预测
# - 轮换直到所有样本都有预测值
#
# 【因果森林（Causal Forest）】
#
# Wager & Athey (2018) 提出。
#
# 目的：估计异质性处理效应 τ(x) = E[Y(1) - Y(0)|X=x]
#
# 方法：
# - 修改随机森林的分裂准则
# - 最大化子节点间处理效应的差异
# - 提供有效的置信区间
#
# 【机器学习在计量中的其他应用】
#
# 1. 变量选择（LASSO）
# 2. 异质性处理效应（因果森林）
# 3. 倾向得分估计（ML提升精度）
# 4. 合成控制法（ML优化权重）
# 5. 反事实预测（深度学习）
#
# 任务：
# 1. 理解并实现LASSO目标函数
# 2. 实现软阈值算子
# 3. 理解双机器学习框架
# 4. 实现交叉验证模型选择
#
# HINT1: 正则化参数需要通过交叉验证选择
# HINT2: DML需要样本分割避免过拟合偏误
# HINT3: LASSO估计有偏，不能直接用于推断

import numpy as np


def lasso_objective(
    beta: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    lambda_: float
) -> float:
    """
    LASSO目标函数。

    【公式】
    L(β) = (1/2n)||Y - Xβ||² + λ||β||₁
         = (1/2n) Σ(y_i - x_i'β)² + λ Σ|β_j|

    【分解】
    - 损失项：(1/2n)||Y - Xβ||²（OLS损失的一半，除以n）
    - 惩罚项：λ||β||₁（系数绝对值之和）

    【为什么用L1惩罚】
    L1惩罚（||β||₁）vs L2惩罚（||β||²）：
    - L1在原点不可微，有"角"
    - 优化路径会先到达坐标轴
    - 导致某些系数精确为0（稀疏性）
    - L2只会把系数缩小，不会变成0

    参数:
        beta: 系数向量，形状 (p,)
        x: 自变量矩阵，形状 (n, p)
        y: 因变量，形状 (n,)
        lambda_: 正则化参数（λ > 0）

    返回:
        目标函数值

    示例:
        >>> n, p = 100, 10
        >>> x = np.random.randn(n, p)
        >>> beta_true = np.array([1, 0, 2, 0, 0, 0, 0, 0, 0, 0])
        >>> y = x @ beta_true + np.random.randn(n) * 0.5
        >>> beta = np.zeros(p)
        >>> loss = lasso_objective(beta, x, y, lambda_=0.1)

    用途:
        评估LASSO优化的收敛性
    """
    # TODO: LASSO目标函数
    # 步骤1: 计算残差 r = y - x @ beta
    # 步骤2: 计算OLS损失 = (1/2n) * ||r||²
    # 步骤3: 计算L1惩罚 = λ * Σ|β_j|
    # 步骤4: 返回 损失 + 惩罚
    pass


def soft_threshold(z: float, lambda_: float) -> float:
    """
    软阈值算子（Soft Thresholding Operator）。

    【公式】
    S(z, λ) = sign(z) × max(|z| - λ, 0)

    等价于：
    S(z, λ) = z - λ     if z > λ
            = 0         if |z| ≤ λ
            = z + λ     if z < -λ

    【在LASSO中的作用】
    软阈值是LASSO优化的核心操作。
    坐标下降法中，每次更新一个系数时：
    β_j ← S(z_j, λ) / (norm of j-th column)

    【硬阈值 vs 软阈值】
    硬阈值：直接把小于λ的值置0，其他不变
    软阈值：把小于λ的值置0，其他向0方向收缩λ

    软阈值更平滑，是L1正则化的解。

    参数:
        z: 输入值
        lambda_: 阈值参数

    返回:
        软阈值结果

    示例:
        >>> soft_threshold(3.0, 1.0)   # 2.0（向0收缩1）
        >>> soft_threshold(0.5, 1.0)   # 0.0（绝对值小于阈值）
        >>> soft_threshold(-2.0, 1.0)  # -1.0（向0收缩1）
    """
    # TODO: 软阈值
    # if z > lambda_: return z - lambda_
    # elif z < -lambda_: return z + lambda_
    # else: return 0
    pass


def coordinate_descent_lasso(
    x: np.ndarray,
    y: np.ndarray,
    lambda_: float,
    max_iter: int = 1000,
    tol: float = 1e-6
) -> np.ndarray:
    """
    坐标下降法求解LASSO。

    【算法思想】
    不同时优化所有参数，而是每次只优化一个参数。
    循环遍历所有参数，直到收敛。

    【LASSO的坐标下降】
    对于第j个系数，固定其他系数，优化：
    min (1/2n)||y - X_{-j}β_{-j} - X_j β_j||² + λ|β_j|

    一阶条件（subgradient）：
    0 ∈ -(1/n)X_j'(y - Xβ) + [-λ, λ]  当 β_j = 0
    0 = -(1/n)X_j'(y - Xβ) + λ×sign(β_j)  当 β_j ≠ 0

    解：
    β_j = S(z_j, λ) / (||X_j||²/n)
    其中 z_j = (1/n)X_j'(y - X_{-j}β_{-j})

    参数:
        x: 自变量矩阵，形状 (n, p)
           假设已标准化（每列均值0，范数1）
        y: 因变量，形状 (n,)
        lambda_: 正则化参数
        max_iter: 最大迭代次数
        tol: 收敛容差

    返回:
        系数估计β̂，形状 (p,)

    示例:
        >>> # 生成稀疏数据
        >>> n, p = 200, 50
        >>> x = np.random.randn(n, p)
        >>> beta_true = np.zeros(p)
        >>> beta_true[:5] = [1, -2, 3, -1, 0.5]
        >>> y = x @ beta_true + np.random.randn(n) * 0.5
        >>>
        >>> beta_lasso = coordinate_descent_lasso(x, y, lambda_=0.1)
        >>> print(f"非零系数数量: {np.sum(beta_lasso != 0)}")

    收敛条件:
        当所有系数的变化都小于tol时停止
    """
    # TODO: 坐标下降
    # 初始化 beta = 0
    # for iteration in range(max_iter):
    #     beta_old = beta.copy()
    #     for j in range(p):
    #         # 计算部分残差
    #         r_j = y - x @ beta + x[:, j] * beta[j]
    #         # 计算z_j
    #         z_j = x[:, j].T @ r_j / n
    #         # 软阈值更新
    #         beta[j] = soft_threshold(z_j, lambda_) / (||x[:, j]||²/n)
    #     # 检查收敛
    #     if max(|beta - beta_old|) < tol:
    #         break
    pass


def cross_validation_mse(
    x: np.ndarray,
    y: np.ndarray,
    lambda_: float,
    n_folds: int = 5
) -> float:
    """
    交叉验证计算MSE。

    【交叉验证的目的】
    评估模型的泛化能力（样本外预测误差）。
    用于选择最优的正则化参数λ。

    【K折交叉验证步骤】
    1. 将数据随机分成K份
    2. 依次用K-1份训练，1份验证
    3. 计算K次验证误差的平均

    【选择λ】
    对于一系列λ值，计算各自的CV-MSE。
    选择使CV-MSE最小的λ（或最简单的在1个标准误内的λ）。

    参数:
        x: 自变量矩阵
        y: 因变量
        lambda_: 正则化参数
        n_folds: 折数（默认5）

    返回:
        交叉验证MSE

    示例:
        >>> lambdas = np.logspace(-3, 1, 20)
        >>> cv_errors = [cross_validation_mse(x, y, lam) for lam in lambdas]
        >>> best_lambda = lambdas[np.argmin(cv_errors)]
        >>> print(f"最优λ: {best_lambda:.4f}")

    注意:
        - 需要随机打乱数据（或使用分层抽样）
        - K通常取5或10
    """
    # TODO: 交叉验证
    # 步骤1: 将数据分成n_folds份
    # 步骤2: 对于每一折:
    #        - 在训练集上拟合LASSO
    #        - 在验证集上计算MSE
    # 步骤3: 返回平均MSE
    pass


def double_ml_ate(
    y: np.ndarray,
    d: np.ndarray,
    x: np.ndarray,
    ml_method: str = "lasso"
) -> float:
    """
    双机器学习估计平均处理效应。

    【Partial Linear Model】
    Y = D × θ + g(X) + ε
    D = m(X) + v

    其中θ是我们感兴趣的因果效应。

    【朴素方法的问题】
    如果直接用Y ~ D + X回归：
    - 高维X时，OLS不适用
    - 用ML预测Y然后用残差回归，会有正则化偏误

    【DML方法】
    关键：用样本分割避免过拟合偏误

    步骤（2折交叉拟合）：
    1. 将样本分成两半：I₁ 和 I₂

    对于 I₁ 的估计：
    2. 在 I₂ 上用ML训练：Ê[Y|X] 和 Ê[D|X]
    3. 在 I₁ 上计算残差：Ỹ = Y - Ê[Y|X], D̃ = D - Ê[D|X]
    4. 在 I₁ 上回归：Ỹ ~ D̃

    对于 I₂ 做同样的事（用 I₁ 训练）

    5. 合并两部分的估计

    【为什么需要样本分割】
    - 避免"自己预测自己"的过拟合偏误
    - 使ML预测误差与估计θ的误差独立
    - Neyman正交性保证根号n一致性

    参数:
        y: 结果变量，形状 (n,)
        d: 处理变量（0/1或连续），形状 (n,)
        x: 控制变量，形状 (n, p)
        ml_method: ML方法（"lasso", "rf"等）

    返回:
        ATE估计（θ̂）

    示例:
        >>> # 模拟数据
        >>> n, p = 1000, 20
        >>> x = np.random.randn(n, p)
        >>> d = (x[:, 0] + np.random.randn(n) > 0).astype(float)
        >>> y = d * 2 + x[:, 0] + x[:, 1]**2 + np.random.randn(n)
        >>>
        >>> theta = double_ml_ate(y, d, x)
        >>> print(f"DML估计的ATE: {theta:.3f}")  # 应接近2

    参考:
        Chernozhukov et al. (2018) "Double/Debiased Machine Learning"
    """
    # TODO: DML估计
    # 步骤1: 样本分割（2折）
    # 步骤2: 第一折
    #        - 在第二半样本训练ML模型预测Y和D
    #        - 在第一半样本计算残差
    # 步骤3: 第二折类似
    # 步骤4: 合并残差，回归 Ỹ ~ D̃
    pass


def sample_splitting(
    n: int,
    n_folds: int = 2
) -> list[tuple[np.ndarray, np.ndarray]]:
    """
    样本分割用于DML。

    【样本分割的目的】
    将样本分成K份（通常K=2），用于交叉拟合：
    - 用K-1份训练ML模型
    - 用第K份进行预测和估计

    【输出格式】
    返回列表，每个元素是(训练索引, 估计索引)元组

    参数:
        n: 样本量
        n_folds: 折数（默认2）

    返回:
        [(训练索引, 估计索引), ...]

    示例:
        >>> n = 100
        >>> folds = sample_splitting(n, n_folds=2)
        >>> train_idx, est_idx = folds[0]
        >>> print(f"训练集大小: {len(train_idx)}, 估计集大小: {len(est_idx)}")
        # 应该各约50个

    应用:
        在DML中，对每个fold：
        - 用train_idx的数据训练ML模型
        - 对est_idx的数据做预测
        - 在est_idx上计算θ的贡献
    """
    # TODO: 样本分割
    # 步骤1: 随机打乱索引
    # 步骤2: 分成n_folds份
    # 步骤3: 生成(训练, 估计)索引对
    pass


def bic_model_selection(
    x: np.ndarray,
    y: np.ndarray,
    lambda_values: np.ndarray
) -> float:
    """
    BIC选择正则化参数。

    【BIC（贝叶斯信息准则）】
    BIC = n × ln(MSE) + k × ln(n)

    其中：
    - MSE：均方误差
    - k：非零系数数量（模型复杂度）
    - n：样本量

    【BIC vs 交叉验证】
    - BIC：有理论依据（一致的模型选择）
    - CV：更稳定，广泛使用
    - BIC倾向于选择更简单的模型

    【LASSO中的BIC】
    对于每个λ：
    1. 拟合LASSO得到β̂
    2. 计算MSE = ||Y - Xβ̂||² / n
    3. 计算k = Σ(β̂_j ≠ 0)
    4. BIC = n × ln(MSE) + k × ln(n)

    选择BIC最小的λ。

    参数:
        x: 自变量矩阵
        y: 因变量
        lambda_values: 候选λ值数组

    返回:
        最优λ

    示例:
        >>> lambdas = np.logspace(-3, 1, 50)
        >>> best_lambda = bic_model_selection(x, y, lambdas)
        >>> print(f"BIC选择的λ: {best_lambda:.4f}")

    扩展:
        也可以用AIC（k的惩罚是2而非ln(n)）
        AIC倾向于选择更复杂的模型
    """
    # TODO: BIC选择
    # 对每个lambda:
    #   1. 拟合LASSO
    #   2. 计算BIC
    # 返回BIC最小的lambda
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
