# EXERCISE: behavioral_finance1
# DIFFICULTY: ★★★★☆
# TOPIC: 行为金融学
#
# 说明：
# 行为金融学（Behavioral Finance）研究心理因素如何影响金融决策和市场价格。
# 它挑战了传统金融学的理性人假设，为解释市场异象提供了新视角。
#
# 【理论背景】
# 传统金融学假设：
# - 投资者完全理性
# - 市场有效
# - 价格反映所有信息
#
# 行为金融学发现：
# - 投资者存在系统性认知偏差
# - 这些偏差影响资产价格
# - 某些市场"异象"可以用行为因素解释
#
# 【认知偏差（Cognitive Biases）】
#
# 1. 过度自信（Overconfidence）
#    - 高估自己的知识和预测能力
#    - 表现：过度交易、低估风险、过窄的置信区间
#    - 后果：交易成本侵蚀收益
#
# 2. 损失厌恶（Loss Aversion）
#    - 损失带来的痛苦大于等额收益带来的快乐
#    - 典型值：λ ≈ 2.25（损失的权重是收益的2.25倍）
#    - 后果：过久持有亏损股票，过早卖出盈利股票
#
# 3. 锚定效应（Anchoring）
#    - 过度依赖初始信息或参考点
#    - 示例：购买价成为参考点，影响卖出决策
#    - 后果：对新信息反应不足
#
# 4. 可得性偏差（Availability Bias）
#    - 依赖容易想到的信息
#    - 示例：高估最近发生事件的概率
#    - 后果：追逐热门股票
#
# 5. 代表性偏差（Representativeness Bias）
#    - 根据相似性而非概率判断
#    - 示例：认为好公司就是好投资
#    - 后果：忽视基础概率
#
# 6. 框架效应（Framing Effect）
#    - 决策受问题呈现方式影响
#    - 示例：同一结果用"存活率"vs"死亡率"描述
#    - 后果：决策不一致
#
# 【前景理论（Prospect Theory）】
# 由Daniel Kahneman和Amos Tversky于1979年提出（诺贝尔经济学奖2002）。
#
# 与期望效用理论的区别：
# 1. 参考点依赖：评估的是相对于参考点的得失，而非最终财富
# 2. 损失厌恶：损失的负效用大于等额收益的正效用
# 3. 敏感度递减：对得失的敏感度随幅度增加而减小
# 4. 概率加权：高估小概率事件，低估大概率事件
#
# 价值函数：
#   v(x) = x^α           if x ≥ 0 (收益区域)
#        = -λ(-x)^β      if x < 0 (损失区域)
#
# 典型参数值（Kahneman & Tversky, 1992）：
# - α = β = 0.88（敏感度递减）
# - λ = 2.25（损失厌恶）
#
# 概率加权函数（Prelec, 1998）：
#   w(p) = exp(-(-ln(p))^γ)
# - γ ≈ 0.61
# - 高估小概率，低估大概率
# - 解释：为什么人们买彩票又买保险
#
# 【市场异象（Market Anomalies）】
#
# 1. 动量效应（Momentum）
#    - 过去表现好的股票继续表现好
#    - 与有效市场假说矛盾
#    - 可能解释：反应不足、羊群效应
#
# 2. 过度反应（Overreaction）
#    - 对新闻过度反应，随后反转
#    - 表现：输家组合跑赢赢家组合
#
# 3. 处置效应（Disposition Effect）
#    - 过早卖出盈利股票，过久持有亏损股票
#    - 源于损失厌恶和心理账户
#
# 4. 股票溢价之谜（Equity Premium Puzzle）
#    - 股票历史收益率远高于债券
#    - 传统效用理论难以解释
#    - 前景理论可部分解释（损失厌恶）
#
# 任务：
# 1. 理解并实现前景理论价值函数
# 2. 实现概率加权函数
# 3. 计算行为偏差的影响
# 4. 分析动量策略
#
# HINT1: λ ≈ 2.25 是经验估计的损失厌恶系数
# HINT2: 框架效应导致同一问题的不同答案
# HINT3: 动量策略在许多市场都有效

import numpy as np


def prospect_theory_value(
    outcome: float,
    alpha: float = 0.88,
    beta: float = 0.88,
    lambda_: float = 2.25
) -> float:
    """
    前景理论价值函数。

    【公式】
    v(x) = x^α           if x ≥ 0 (收益)
         = -λ(-x)^β      if x < 0 (损失)

    【参数解释】
    - α (alpha): 收益区域的风险态度
      α < 1 表示收益区域风险厌恶（凹函数）
      边际价值递减

    - β (beta): 损失区域的风险态度
      β < 1 表示损失区域风险寻求（凸函数）
      边际损失递减

    - λ (lambda): 损失厌恶系数
      λ > 1 表示损失的痛苦大于等额收益的快乐
      典型值约2.25，即损失100元的痛苦 ≈ 收益225元的快乐

    【与期望效用理论的对比】
    期望效用理论：U(W)，对最终财富水平的效用
    前景理论：v(x)，对相对于参考点的得失的价值

    参数:
        outcome: 结果（相对于参考点的得失）
                 正数表示收益，负数表示损失
        alpha: 收益区域曲率参数（默认0.88）
        beta: 损失区域曲率参数（默认0.88）
        lambda_: 损失厌恶系数（默认2.25）

    返回:
        主观价值

    示例:
        收益100元的主观价值
        >>> prospect_theory_value(100)
        57.54  # 100^0.88 ≈ 57.54

        损失100元的主观价值
        >>> prospect_theory_value(-100)
        -129.47  # -2.25 × 100^0.88 ≈ -129.47

    观察:
        损失100元的负价值绝对值是收益100元的正价值的约2.25倍
        体现了损失厌恶
    """
    # TODO: 计算前景理论价值
    # 提示：
    # if outcome >= 0:
    #     return outcome ** alpha
    # else:
    #     return -lambda_ * ((-outcome) ** beta)
    pass


def probability_weighting(
    prob: float,
    gamma: float = 0.61
) -> float:
    """
    Prelec概率加权函数。

    【公式】
    w(p) = exp(-(-ln(p))^γ)

    【函数特征】
    - 当 γ < 1：
      - 高估小概率：w(p) > p for small p
      - 低估大概率：w(p) < p for large p
      - 确定性效应：w(0) = 0, w(1) = 1
      - 在中间概率交叉：存在某个p*使得w(p*) = p*

    【解释】
    - 人们对小概率事件过于敏感（买彩票心理）
    - 对大概率事件不够敏感（忽视几乎确定的事件）
    - 在极端概率附近敏感度突变

    【应用】
    解释保险购买行为：
    - 小概率灾难事件的概率被高估
    - 即使期望损失小，也愿意购买保险

    解释彩票购买行为：
    - 中奖的小概率被高估
    - 即使期望收益为负，也愿意购买彩票

    参数:
        prob: 客观概率（0到1之间）
        gamma: 加权参数（默认0.61，来自实验估计）

    返回:
        主观概率权重

    示例:
        1%概率的主观权重
        >>> probability_weighting(0.01)
        0.065  # 远大于0.01，高估小概率

        99%概率的主观权重
        >>> probability_weighting(0.99)
        0.91  # 小于0.99，低估大概率

    注意:
        - prob必须在(0, 1)开区间内（ln(0)和ln(1)边界问题）
        - 实际应用中需处理边界情况
    """
    # TODO: 计算概率权重
    # 提示：w(p) = exp(-(-ln(p))^γ)
    # 注意处理边界情况：p = 0 或 p = 1
    pass


def certainty_equivalent_prospect(
    gain: float,
    loss: float,
    prob_gain: float,
    alpha: float = 0.88,
    beta: float = 0.88,
    lambda_: float = 2.25,
    gamma: float = 0.61
) -> float:
    """
    前景理论下的确定性等价。

    【问题设定】
    一个赌博有两种结果：
    - 以概率 p 获得收益 G
    - 以概率 (1-p) 遭受损失 L

    确定性等价（CE）是使决策者无差异的确定收益：
    v(CE) = w(p) × v(G) + w(1-p) × v(-L)

    【前景理论下的计算步骤】
    1. 计算收益的主观价值 v(G)
    2. 计算损失的主观价值 v(-L)
    3. 计算概率权重 w(p) 和 w(1-p)
    4. 计算加权主观期望值
    5. 反推确定性等价

    【与期望值的对比】
    期望值 = p × G - (1-p) × L
    确定性等价通常不等于期望值，
    反映了风险态度和概率扭曲

    参数:
        gain: 可能的收益（正数）
        loss: 可能的损失（正数，函数内部处理为负）
        prob_gain: 获得收益的概率
        alpha, beta, lambda_, gamma: 前景理论参数

    返回:
        确定性等价

    示例:
        有50%概率赢100元，50%概率输100元
        期望值 = 0，但确定性等价为负（因为损失厌恶）
        >>> certainty_equivalent_prospect(100, 100, 0.5)
        -15.5  # 大约，取决于参数

    应用:
        - 解释风险溢价
        - 设计激励机制
        - 理解保险需求
    """
    # TODO: 计算确定性等价
    # 步骤1: 计算v(gain)和v(-loss)
    # 步骤2: 计算w(prob_gain)和w(1-prob_gain)
    # 步骤3: 计算加权期望值 = w(p)*v(G) + w(1-p)*v(-L)
    # 步骤4: 从v(CE) = 加权期望值 反推CE（需要考虑正负）
    pass


def overconfidence_bias(
    actual_accuracy: float,
    perceived_accuracy: float
) -> float:
    """
    计算过度自信程度。

    【过度自信的定义】
    过度自信 = 主观准确率 - 客观准确率

    【过度自信的表现形式】
    1. 校准不足（Miscalibration）：
       - 对预测的置信度过高
       - 90%置信区间只包含50%的结果

    2. 优于平均效应（Better-than-average）：
       - 80%的司机认为自己驾驶技术高于平均
       - 在投资者中同样普遍

    3. 控制错觉（Illusion of Control）：
       - 高估自己对结果的控制能力
       - 例如：亲自选号vs随机号码

    【对投资的影响】
    - 过度交易：高估自己的选股能力
    - 分散不足：对少数股票过于自信
    - 低估风险：置信区间过窄

    参数:
        actual_accuracy: 实际准确率（如预测的实际命中率）
        perceived_accuracy: 自认为的准确率

    返回:
        过度自信程度（正数表示过度自信，负数表示不自信）

    示例:
        投资者认为选股准确率80%，实际只有50%
        >>> overconfidence_bias(0.50, 0.80)
        0.30  # 过度自信30个百分点

    研究发现:
        - 专业投资者也存在过度自信
        - 男性通常比女性更过度自信
        - 过度自信随经验积累可能减少或加剧
    """
    # TODO: 计算过度自信
    # 提示：过度自信 = 主观准确率 - 客观准确率
    pass


def disposition_effect(
    gain_holding_period: float,
    loss_holding_period: float
) -> float:
    """
    计算处置效应强度。

    【处置效应定义】
    投资者倾向于：
    - 过早卖出盈利股票（锁定收益）
    - 过久持有亏损股票（不愿确认损失）

    处置效应强度 = 损失持有期 / 收益持有期

    【理论解释】
    1. 前景理论：
       - 收益区域风险厌恶（想锁定收益）
       - 损失区域风险寻求（赌一把可能回本）

    2. 心理账户：
       - 每只股票是独立的心理账户
       - 不愿"关闭"亏损账户

    3. 后悔规避：
       - 卖出后股票上涨会后悔
       - 亏损只是"浮亏"不算真正损失

    【实证研究】
    Odean (1998) 发现：
    - 投资者卖出盈利股票的概率是亏损股票的1.5倍
    - 被卖出的股票后续表现反而更好

    参数:
        gain_holding_period: 盈利股票平均持有期（天/月）
        loss_holding_period: 亏损股票平均持有期

    返回:
        处置效应比率
        > 1 表示存在处置效应
        = 1 表示无偏
        < 1 表示反向处置效应

    示例:
        盈利股票平均持有60天，亏损股票平均持有120天
        >>> disposition_effect(60, 120)
        2.0  # 亏损股票持有期是盈利股票的2倍

    应用:
        - 评估投资者行为偏差
        - 设计交易提醒系统
        - 投资者教育
    """
    # TODO: 计算处置效应
    # 提示：处置效应 = loss_holding_period / gain_holding_period
    pass


def mental_accounting_value(
    outcomes: list[float],
    segregate_gains: bool = True,
    integrate_losses: bool = True
) -> float:
    """
    心理账户下的总价值。

    【心理账户理论】
    Richard Thaler的心理账户理论指出，人们会将金钱划分到不同的
    "心理账户"中，违反了资金的可替代性原则。

    【享乐编辑（Hedonic Editing）】
    根据前景理论，为最大化主观感受：
    1. 分别体验收益（Segregate gains）：
       v(100) + v(100) > v(200)
       因为价值函数边际递减

    2. 合并体验损失（Integrate losses）：
       v(-200) > v(-100) + v(-100)
       因为损失函数也边际递减

    3. 小收益与大损失合并（Integration of smaller gain with larger loss）：
       v(-100 + 10) > v(-100) + v(10)
       小收益可以"安慰"大损失

    4. 小损失与大收益分开（Segregation of small loss from large gain）：
       v(100) + v(-10) > v(100 - 10)
       小损失不要玷污大收益

    参数:
        outcomes: 结果列表（多个收益或损失）
        segregate_gains: 是否分别计算收益（默认True）
        integrate_losses: 是否合并损失（默认True）

    返回:
        根据心理账户规则计算的总主观价值

    示例:
        两个收益100和50，一个损失80
        >>> mental_accounting_value([100, 50, -80])
        根据规则：分开计算收益，合并损失

    注意:
        此函数使用默认的前景理论参数
    """
    # TODO: 计算心理账户价值
    # 步骤1: 将outcomes分为收益和损失
    # 步骤2: 根据segregate_gains决定收益的处理方式
    # 步骤3: 根据integrate_losses决定损失的处理方式
    # 步骤4: 计算总价值
    pass


def momentum_return(
    past_returns: np.ndarray,
    formation_period: int,
    holding_period: int
) -> float:
    """
    计算动量策略收益。

    【动量效应】
    Jegadeesh和Titman (1993) 发现：
    - 过去3-12个月表现好的股票继续表现好
    - 动量策略：买入赢家，卖出输家
    - 年化超额收益约12%

    【策略设计】
    1. 形成期（Formation Period）：
       根据过去收益排名股票

    2. 持有期（Holding Period）：
       买入赢家组合，卖出输家组合

    典型策略：12-1（12个月形成期，跳过最近1个月，持有1个月）

    【行为解释】
    1. 反应不足：投资者对信息反应缓慢
    2. 确认偏差：寻找支持已有观点的信息
    3. 羊群效应：跟随他人行为

    参数:
        past_returns: 历史收益率数组（按时间顺序）
        formation_period: 形成期长度（月数）
        holding_period: 持有期长度（月数，用于计算后续收益）

    返回:
        动量信号（形成期累计收益率）

    示例:
        过去24个月收益率，形成期12个月
        >>> past_returns = np.random.randn(24) * 0.05
        >>> momentum_return(past_returns, 12, 1)
        0.15  # 过去12个月累计收益15%，正动量

    应用:
        - 构建动量因子
        - 识别赢家/输家股票
        - 量化投资策略
    """
    # TODO: 计算动量收益
    # 步骤1: 取最近formation_period个月的收益率
    # 步骤2: 计算累计收益率（可用(1+r).prod() - 1）
    # 或简单地计算总和
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
