# EXERCISE: risk_management1
# DIFFICULTY: ★★★★☆
# TOPIC: 风险管理与衍生品
#
# 说明：
# 风险管理（Risk Management）是现代金融机构的核心职能，涉及风险的识别、
# 度量、监控和对冲。本模块聚焦于市场风险度量和衍生品对冲策略。
#
# 【理论背景】
# 金融风险的主要类型：
# 1. 市场风险：资产价格变动导致的损失（本模块重点）
# 2. 信用风险：交易对手违约风险
# 3. 流动性风险：无法以合理价格交易的风险
# 4. 操作风险：内部流程、人员或系统故障
#
# 【在险价值（Value at Risk, VaR）】
# VaR是最广泛使用的市场风险度量指标。
#
# 定义：在给定置信水平（如95%或99%）下，
#       一定持有期内（如1天或10天），
#       资产组合可能遭受的最大损失。
#
# 数学表示：P(Loss > VaR) = 1 - α
# 其中α是置信水平（如0.95表示95%）
#
# VaR的计算方法：
# 1. 参数法（方差-协方差法）：
#    假设收益率服从正态分布
#    VaR = -V × (μ + σ × z_α)
#    其中z_α是标准正态分布的分位数
#
# 2. 历史模拟法：
#    使用历史收益率分布
#    VaR = 历史收益率的(1-α)分位数 × 组合价值
#
# 3. 蒙特卡洛模拟法：
#    模拟大量可能的价格路径
#    从模拟分布中计算VaR
#
# VaR的局限性：
# - 不满足次可加性（非一致性风险度量）
# - 不捕捉尾部风险（VaR以外的损失大小）
# - 对分布假设敏感
#
# 【期望损失（Expected Shortfall, ES）】
# 也称条件VaR（CVaR）或尾部VaR（TVaR）。
#
# 定义：ES = E[Loss | Loss > VaR]
# 即：在损失超过VaR的条件下，损失的期望值。
#
# ES克服了VaR的一些缺陷：
# - 满足次可加性（一致性风险度量）
# - 考虑尾部损失的严重程度
# - 更适合厚尾分布
#
# 【希腊字母（Greeks）】
# 希腊字母描述期权价格对各风险因子的敏感度。
#
# Delta (Δ)：期权价格对标的资产价格的一阶导数
#   Δ = ∂V/∂S
#   看涨期权：0 < Δ < 1，看跌期权：-1 < Δ < 0
#   深度实值期权Δ接近±1，深度虚值期权Δ接近0
#
# Gamma (Γ)：Delta对标的资产价格的导数（二阶导数）
#   Γ = ∂²V/∂S² = ∂Δ/∂S
#   平值期权Gamma最大
#   多头期权Gamma为正，空头为负
#
# Vega (ν)：期权价格对波动率的敏感度
#   ν = ∂V/∂σ
#   期权多头Vega为正
#   平值期权Vega最大
#
# Theta (Θ)：期权价格对时间的敏感度（时间衰减）
#   Θ = ∂V/∂t
#   期权多头Theta通常为负（时间价值衰减）
#
# Rho (ρ)：期权价格对无风险利率的敏感度
#   ρ = ∂V/∂r
#
# 【对冲策略】
#
# 1. Delta对冲：
#    持有-Δ单位标的资产以抵消期权的Delta
#    使组合Delta为零（Delta中性）
#    需要动态调整（因为Delta会变化）
#
# 2. Delta-Gamma对冲：
#    同时实现Delta和Gamma中性
#    需要两种对冲工具
#    减少调仓频率
#
# 3. 久期对冲：
#    用于债券组合
#    通过久期匹配对冲利率风险
#
# 任务：
# 1. 计算参数法和历史模拟法VaR
# 2. 计算期望损失ES
# 3. 实现Delta和Gamma对冲
# 4. 理解久期对冲
#
# HINT1: VaR低估尾部风险，ES更为保守
# HINT2: 动态对冲需要频繁调整，有交易成本
# HINT3: Gamma对冲需要额外的期权头寸

import numpy as np
from scipy import stats


def parametric_var(
    portfolio_value: float,
    mean_return: float,
    std_return: float,
    confidence: float = 0.95,
    holding_period: int = 1
) -> float:
    """
    参数法（方差-协方差法）计算VaR。

    【公式推导】
    假设收益率 r ~ N(μ, σ²)

    对于t天持有期：
    收益率均值 = μ × t
    收益率标准差 = σ × √t（波动率的平方根法则）

    VaR是使得P(Loss > VaR) = 1 - α的损失值

    由于 r ~ N(μ×t, σ²×t)，
    损失 L = -V × r

    VaR_α = -V × (μ×t + σ×√t × z_{1-α})

    其中z_{1-α}是标准正态分布的(1-α)分位数
    例如：95%置信水平，z = -1.645
          99%置信水平，z = -2.326

    注意：VaR是正数表示损失

    【参数法的优缺点】
    优点：
    - 计算简单快速
    - 可分解到各风险因子
    - 不需要大量历史数据

    缺点：
    - 假设正态分布（忽略厚尾）
    - 对非线性资产（期权）不准确
    - 低估极端事件

    参数:
        portfolio_value: 组合价值（V）
        mean_return: 日均收益率（μ，如0.001表示0.1%）
        std_return: 日收益率标准差（σ，日波动率）
        confidence: 置信水平（α，默认95%）
        holding_period: 持有期（天数，默认1天）

    返回:
        VaR（正数表示损失）

    示例:
        组合价值1亿，日均收益0.05%，日波动率2%，95%置信度，1天
        >>> parametric_var(100_000_000, 0.0005, 0.02, 0.95, 1)
        3239500  # 1天95% VaR约324万

    解释:
        z_0.05 = -1.645
        VaR = -1亿 × (0.0005 + 0.02 × (-1.645)) = 324万
    """
    # TODO: 计算参数VaR
    # 步骤1: 计算t天的均值 μ_t = μ × t
    # 步骤2: 计算t天的标准差 σ_t = σ × √t
    # 步骤3: 计算正态分布分位数 z = norm.ppf(1 - confidence)
    # 步骤4: VaR = -V × (μ_t + σ_t × z)
    pass


def historical_var(
    returns: np.ndarray,
    portfolio_value: float,
    confidence: float = 0.95
) -> float:
    """
    历史模拟法计算VaR。

    【方法原理】
    使用历史收益率的经验分布来估计VaR：
    1. 收集历史收益率数据
    2. 对收益率从小到大排序
    3. 找到(1-α)分位数对应的收益率
    4. VaR = -该分位数收益率 × 组合价值

    【优缺点】
    优点：
    - 不需要分布假设
    - 自动捕捉厚尾和偏度
    - 直观易理解

    缺点：
    - 依赖历史数据的代表性
    - 假设历史会重演
    - 对数据量要求高
    - 对极端事件估计不稳定

    【实践考量】
    - 通常需要250-500天历史数据
    - 可考虑加权（近期数据权重更高）
    - 需要定期滚动更新

    参数:
        returns: 历史收益率数组（如过去500天的日收益率）
        portfolio_value: 当前组合价值
        confidence: 置信水平（默认95%）

    返回:
        VaR（正数表示损失）

    示例:
        500天历史数据，组合价值1亿，95%置信度
        假设5%分位数收益率为-3%
        >>> returns = np.random.randn(500) * 0.02  # 模拟数据
        >>> historical_var(returns, 100_000_000, 0.95)
        约300万  # 取决于具体数据

    注意:
        返回的是损失（正数），所以要对收益率取负
    """
    # TODO: 计算历史VaR
    # 步骤1: 计算(1-confidence)分位数对应的收益率
    #        使用 np.percentile(returns, (1-confidence)*100)
    # 步骤2: VaR = -分位数收益率 × 组合价值
    pass


def expected_shortfall(
    returns: np.ndarray,
    portfolio_value: float,
    confidence: float = 0.95
) -> float:
    """
    计算期望损失（Expected Shortfall，也称CVaR）。

    【定义】
    ES = E[Loss | Loss > VaR]
    即：在损失超过VaR的条件下，损失的期望值

    【计算方法】
    1. 找到VaR对应的分位数
    2. 计算所有超过该分位数的损失的平均值

    对于历史模拟法：
    ES = -mean(收益率 | 收益率 < VaR分位数) × 组合价值

    【ES vs VaR】
    - ES ≥ VaR（总是更保守）
    - ES是一致性风险度量（满足次可加性）
    - ES考虑尾部损失的严重程度
    - Basel III要求使用ES替代VaR

    【数学性质】
    对于正态分布：
    ES = σ × φ(z_α) / (1-α) - μ
    其中φ是标准正态密度函数

    参数:
        returns: 历史收益率数组
        portfolio_value: 组合价值
        confidence: 置信水平（默认95%）

    返回:
        ES（正数表示损失）

    示例:
        假设最差5%的收益率平均为-4%
        >>> returns = np.random.randn(500) * 0.02
        >>> expected_shortfall(returns, 100_000_000, 0.95)
        约400万  # ES通常大于VaR

    应用:
        - 资本充足率计算
        - 压力测试
        - 风险预算
    """
    # TODO: 计算ES
    # 步骤1: 计算VaR对应的分位数收益率
    # 步骤2: 筛选出低于该分位数的所有收益率
    # 步骤3: ES = -这些收益率的平均值 × 组合价值
    pass


def delta_hedge_ratio(delta: float, shares_per_option: int = 100) -> float:
    """
    计算Delta对冲比率。

    【Delta对冲原理】
    期权价格变化 ≈ Δ × 标的价格变化

    为了对冲期权头寸：
    - 卖出看涨期权：买入 Δ × 合约乘数 股股票
    - 买入看涨期权：卖出 Δ × 合约乘数 股股票

    对冲后，标的价格小幅变动时，组合价值不变。

    【公式】
    对冲股数 = -Δ × 合约乘数

    负号因为：
    - 期权多头需要反向股票头寸
    - 卖出期权（Δ为正）需要买入股票

    【实践应用】
    - 期权做市商保持Delta中性
    - 动态对冲：随标的价格变化调整
    - 对冲成本：频繁调仓的交易成本

    参数:
        delta: 期权的Delta值
               看涨期权：0 < Δ < 1
               看跌期权：-1 < Δ < 0
        shares_per_option: 每份期权对应的股数（合约乘数，如100股）

    返回:
        每份期权需要的对冲股数（正数买入，负数卖出）

    示例:
        卖出1份看涨期权，Δ=0.6，合约乘数100
        >>> delta_hedge_ratio(0.6, 100)
        -60  # 需要卖出60股来对冲

        买入1份看跌期权，Δ=-0.4，合约乘数100
        >>> delta_hedge_ratio(-0.4, 100)
        40  # 需要买入40股来对冲

    注意:
        - 返回的是做空期权时需要的对冲头寸
        - 实际应用中还需考虑Gamma风险
    """
    # TODO: 计算对冲比率
    # 提示：对冲股数 = -Delta × 合约乘数
    pass


def portfolio_delta(
    option_deltas: np.ndarray,
    option_positions: np.ndarray,
    stock_position: float
) -> float:
    """
    计算组合Delta。

    【组合Delta】
    组合的Delta是各头寸Delta的加权和：
    Portfolio Δ = Σ(期权头寸ᵢ × Δᵢ × 合约乘数) + 股票头寸

    股票的Delta = 1（每股）

    【Delta中性】
    当组合Delta = 0时，称为Delta中性：
    - 标的价格小幅变动对组合价值影响很小
    - 做市商和对冲基金常用策略

    参数:
        option_deltas: 各期权的Delta值数组
        option_positions: 各期权头寸数组（正数多头，负数空头）
                         假设已包含合约乘数的影响
        stock_position: 股票头寸（股数，正数多头）

    返回:
        组合总Delta

    示例:
        持有：100份看涨期权(Δ=0.5)，-50份看涨期权(Δ=0.7)，200股股票
        >>> option_deltas = np.array([0.5, 0.7])
        >>> option_positions = np.array([100, -50])  # 假设乘数已计入
        >>> portfolio_delta(option_deltas, option_positions, 200)
        215  # 组合Delta = 100×0.5 + (-50)×0.7 + 200 = 215

    应用:
        - 判断组合的方向性风险敞口
        - 计算需要多少股票来实现Delta中性
    """
    # TODO: 计算组合Delta
    # 提示：Σ(position × delta) + stock_position
    pass


def gamma_neutral_hedge(
    current_gamma: float,
    hedge_option_gamma: float
) -> float:
    """
    计算达到Gamma中性所需的期权数量。

    【Gamma风险】
    Delta会随标的价格变化，这种变化由Gamma描述：
    ΔΔ = Γ × ΔS

    高Gamma意味着：
    - Delta变化快，需要频繁调整对冲
    - 大幅价格变动时对冲失效

    【Gamma对冲】
    股票Gamma = 0，所以只能用期权对冲Gamma。

    设需要n份对冲期权：
    当前Gamma + n × 对冲期权Gamma = 0
    n = -当前Gamma / 对冲期权Gamma

    【实践步骤】
    1. 用期权实现Gamma中性
    2. 再用股票调整Delta到中性
    3. 因为加入期权改变了Delta

    参数:
        current_gamma: 当前组合的Gamma
        hedge_option_gamma: 用于对冲的期权的Gamma

    返回:
        所需期权数量（正数买入，负数卖出）

    示例:
        当前组合Gamma = 500，对冲期权Gamma = 2
        >>> gamma_neutral_hedge(500, 2)
        -250  # 需要卖出250份期权

    注意:
        - Gamma对冲后还需调整Delta
        - 平值期权Gamma最大，最适合对冲
    """
    # TODO: 计算Gamma对冲
    # 提示：n = -current_gamma / hedge_option_gamma
    pass


def duration_hedge(
    bond_value: float,
    bond_duration: float,
    hedge_duration: float,
    hedge_price: float
) -> float:
    """
    计算久期对冲所需的头寸。

    【久期（Duration）】
    久期衡量债券价格对利率变化的敏感度：
    ΔP/P ≈ -D × Δy

    其中：
    - P = 债券价格
    - D = 修正久期
    - Δy = 收益率变化

    【久期对冲原理】
    通过调整组合久期来对冲利率风险。

    设：
    - V_B = 债券组合价值，D_B = 组合久期
    - V_H = 对冲工具头寸，D_H = 对冲工具久期

    久期匹配条件：
    V_B × D_B + V_H × D_H = 0

    解得：
    V_H = -(V_B × D_B) / D_H

    【常用对冲工具】
    - 国债期货
    - 利率互换
    - 久期匹配的债券

    参数:
        bond_value: 债券组合价值
        bond_duration: 债券组合久期（修正久期）
        hedge_duration: 对冲工具久期
        hedge_price: 对冲工具单位价格

    返回:
        对冲头寸（合约数量，正数多头，负数空头）

    示例:
        债券组合1000万，久期5年；用久期10的期货对冲，期货价100
        >>> duration_hedge(10_000_000, 5, 10, 100)
        -5000  # 需要卖出5000份期货合约

    验证:
        对冲价值 = -5000 × 100 = -50万（名义价值）
        实际上期货名义价值通常为价格×乘数
    """
    # TODO: 计算久期对冲
    # 步骤1: 计算需要的对冲价值 V_H = -(V_B × D_B) / D_H
    # 步骤2: 计算合约数量 = V_H / hedge_price
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
