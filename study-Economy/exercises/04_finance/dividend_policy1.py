# EXERCISE: dividend_policy1
# DIFFICULTY: ★★★☆☆
# TOPIC: 股利政策
#
# 说明：
# 股利政策（Dividend Policy）是公司金融的重要议题，研究企业如何在留存收益与
# 股利分配之间做出选择，以及这一选择如何影响企业价值和股东财富。
#
# 【理论背景】
# 股利（Dividend）是公司将盈利分配给股东的方式。
# 核心问题：股利政策是否影响企业价值？应该如何制定股利政策？
#
# 【MM股利无关论（Miller-Modigliani, 1961）】
# 在完美资本市场假设下：
# - 无税收
# - 无交易成本
# - 无信息不对称
# - 投资政策独立于股利政策
#
# 结论：股利政策不影响企业价值
# 原因：
# 1. 股东可以通过卖出股票"自制股利"
# 2. 企业价值由投资机会决定，而非利润分配方式
# 3. 支付股利减少再投资，但股价会相应下跌
#
# 然而，现实市场并非完美，股利政策确实具有重要影响。
#
# 【股利政策理论】
#
# 1. 信号理论（Signaling Theory）
#    - 股利传递公司前景信息
#    - 股利增加被视为利好信号（管理层对未来有信心）
#    - 股利削减被视为利空信号
#    - 解释：为什么公司维持稳定的股利政策
#
# 2. 代理理论（Agency Theory）
#    - 股利减少管理层控制的自由现金流
#    - 防止管理层过度投资或挥霍
#    - "鸟在手"效应：股东更偏好确定的股利
#    - 股利是一种公司治理机制
#
# 3. 税收偏好理论（Tax Preference Theory）
#    - 许多国家：资本利得税率 < 股利税率
#    - 资本利得可以延迟纳税
#    - 因此投资者可能偏好股票回购而非现金股利
#    - 税收客户效应：高税率投资者偏好低股利股票
#
# 4. 客户效应（Clientele Effect）
#    - 不同投资者有不同的股利偏好
#    - 养老基金可能偏好高股利（稳定现金流）
#    - 成长型投资者可能偏好低股利（再投资）
#    - 公司吸引匹配其股利政策的投资者群体
#
# 【股利形式】
# 1. 现金股利（Cash Dividend）：最常见形式
# 2. 股票股利（Stock Dividend）：以股票形式分配，不改变股东财富
# 3. 股票回购（Share Repurchase）：
#    - 公司在公开市场买回自己的股票
#    - 减少流通股数，提高EPS
#    - 税收上可能更优（资本利得vs股利）
#    - 信号效应：表示管理层认为股票被低估
# 4. 特别股利（Special Dividend）：一次性额外派发
#
# 【股利政策实践】
# 1. 稳定增长政策：每年稳定增加股利
# 2. 固定支付率政策：保持固定的股利支付率
# 3. 低正常股利加额外股利：基础股利加视情况的额外派发
# 4. 剩余股利政策：投资后剩余的利润用于派发股利
#
# 【重要指标】
# - 股利支付率 = 股利 / 净利润
# - 股利收益率 = 每股股利 / 股价
# - 留存比率 = 1 - 股利支付率
# - 可持续增长率 = ROE × 留存比率
#
# 任务：
# 1. 计算各种股利指标
# 2. 分析股利政策对股价的影响
# 3. 比较现金股利与股票回购
# 4. 理解可持续增长率
#
# HINT1: 回购在税收上可能更优（资本利得vs股利税率）
# HINT2: 股利信号效应很重要，削减股利通常导致股价大跌
# HINT3: 可持续增长率反映了内部融资能力

import numpy as np


def dividend_payout_ratio(dividends: float, net_income: float) -> float:
    """
    计算股利支付率。

    【公式】
    Payout Ratio = Dividends / Net Income
    股利支付率 = 股利总额 / 净利润

    【经济含义】
    - 衡量公司将多少利润分配给股东
    - 高支付率：成熟公司、增长机会有限
    - 低支付率：成长型公司、需要资金再投资
    - 0%：不派息（如早期的亚马逊、Alphabet）
    - >100%：派发超过当年利润（动用留存收益，不可持续）

    【行业差异】
    - 公用事业：通常60-80%（稳定现金流）
    - 科技行业：通常0-30%（高增长需求）
    - 银行业：通常30-50%（监管要求）
    - REITs：通常90%+（法定要求）

    参数:
        dividends: 股利总额（通常为年度总额）
        net_income: 净利润

    返回:
        股利支付率（0到1之间，可能>1）

    示例:
        净利润100亿，派发股利40亿
        >>> dividend_payout_ratio(40, 100)
        0.4  # 40%的利润用于分红

    注意:
        - 应使用普通股股利（不含优先股）
        - 净利润应为归属母公司股东的净利润
    """
    # TODO: 计算支付率
    # 提示：Payout Ratio = Dividends / Net Income
    pass


def dividend_yield(dividend_per_share: float, stock_price: float) -> float:
    """
    计算股利收益率。

    【公式】
    Yield = DPS / P
    股利收益率 = 每股股利 / 股价

    【经济含义】
    股利收益率表示投资者从股利中获得的回报率：
    - 高股利收益率：可能是价值股，或股价被低估，或公司成熟
    - 低股利收益率：可能是成长股，利润用于再投资
    - 异常高的收益率：可能预示股利削减风险

    【投资策略应用】
    - 股利收益率策略："狗股"策略（Dogs of the Dow）
    - 买入高股利收益率股票，期待价格回归
    - 收益型投资者偏好高且稳定的股利收益率

    参数:
        dividend_per_share: 每股股利（DPS，通常为年度）
        stock_price: 当前股价（P）

    返回:
        股利收益率

    示例:
        每股股利2元，股价50元
        >>> dividend_yield(2, 50)
        0.04  # 股利收益率4%

    对比:
        与债券收益率相比，股利还有增长潜力
        总回报 = 股利收益率 + 资本增值
    """
    # TODO: 计算收益率
    # 提示：Yield = DPS / P
    pass


def retention_ratio(payout_ratio: float) -> float:
    """
    计算留存比率（利润留存率）。

    【公式】
    Retention Ratio = 1 - Payout Ratio
    留存比率 = 1 - 股利支付率

    也可以直接计算：
    Retention Ratio = Retained Earnings / Net Income

    【经济含义】
    留存比率表示多少利润被保留用于再投资：
    - 高留存率：公司有好的投资机会，需要资金支持增长
    - 低留存率：公司增长放缓，将利润返还股东

    【与增长的关系】
    留存收益是内部融资的主要来源：
    可持续增长率 g = ROE × b
    其中 b 是留存比率

    参数:
        payout_ratio: 股利支付率

    返回:
        留存比率（b）

    示例:
        支付率40%
        >>> retention_ratio(0.4)
        0.6  # 60%的利润被留存

    注意:
        - 留存比率 + 支付率 = 1
        - 也称为"再投资比率"或"耕耘比率"（plowback ratio）
    """
    # TODO: 计算留存比率
    # 提示：Retention Ratio = 1 - Payout Ratio
    pass


def sustainable_growth_rate(roe: float, retention_ratio: float) -> float:
    """
    计算可持续增长率。

    【公式】
    g = ROE × b
    可持续增长率 = 股本回报率 × 留存比率

    【推导】
    假设公司保持恒定的债务权益比和股利政策：
    - 留存收益增加 = 净利润 × 留存比率
    - 权益增长率 = 留存收益增加 / 权益 = ROE × b
    - 保持恒定资本结构，资产也以相同速率增长
    - 因此，销售收入也以相同速率增长

    【经济含义】
    可持续增长率是在不改变资本结构、不发行新股的情况下，
    仅靠内部融资（留存收益）能够支持的最大增长率。

    【实践应用】
    - 如果实际增长 > 可持续增长：需要外部融资或改变财务政策
    - 如果实际增长 < 可持续增长：可能增加股利或回购股票
    - 用于财务规划和预测

    参数:
        roe: 股本回报率（Return on Equity）
        retention_ratio: 留存比率（b）

    返回:
        可持续增长率（g）

    示例:
        ROE = 15%，留存比率 = 60%
        >>> sustainable_growth_rate(0.15, 0.6)
        0.09  # 可持续增长率9%

    扩展:
        更完整的可持续增长率公式：
        g = (ROE × b) / [1 - (ROE × b)]
        当ROE×b较大时差异明显
    """
    # TODO: 计算可持续增长率
    # 提示：g = ROE × b
    pass


def stock_price_after_dividend(
    price_before: float,
    dividend: float
) -> float:
    """
    计算股利除权后的股价。

    【除权日机制】
    - 股权登记日：确定有权获得股利的股东
    - 除权日（Ex-dividend Date）：买入股票不再享有本次股利
    - 除权日股价理论上下跌股利金额

    【公式】
    P_ex = P_cum - D
    除权价 = 含权价 - 每股股利

    【MM股利无关论的体现】
    股东财富不变：
    - 除权前：持有价值 P_cum 的股票
    - 除权后：持有价值 P_ex 的股票 + 收到 D 的现金
    - 总财富：P_ex + D = P_cum

    【实际观察】
    - 实际除权日股价下跌往往小于股利金额
    - 可能原因：税收效应（股利税可能高于资本利得税）
    - "除权日效应"是市场异象研究的课题

    参数:
        price_before: 除权前股价（P_cum，含权价）
        dividend: 每股股利（D）

    返回:
        除权后股价（P_ex）

    示例:
        除权前股价52元，每股股利2元
        >>> stock_price_after_dividend(52, 2)
        50  # 除权后股价50元

    注意:
        股票股利和股票分割需要不同的计算方式
    """
    # TODO: 计算除权价
    # 提示：P_ex = P_cum - D
    pass


def shares_repurchased(repurchase_amount: float, stock_price: float) -> float:
    """
    计算股票回购股数。

    【股票回购机制】
    公司使用现金在公开市场购买自己的流通股：
    回购股数 = 回购金额 / 股价

    【回购方式】
    1. 公开市场回购：最常见，逐步买入
    2. 固定价格要约：以固定溢价一次性收购
    3. 荷兰式拍卖：股东竞价，公司选择最低价
    4. 定向回购：向特定股东购买

    【回购动机】
    1. 向市场传递股票被低估的信号
    2. 返还多余现金给股东（替代股利）
    3. 调整资本结构（增加杠杆）
    4. 抵消股权激励的稀释效应
    5. 阻止恶意收购

    参数:
        repurchase_amount: 回购金额（公司投入的现金）
        stock_price: 回购时的股价

    返回:
        回购股数

    示例:
        用10亿元回购，股价50元
        >>> shares_repurchased(10_0000_0000, 50)
        20000000  # 回购2000万股

    注意:
        - 实际回购价格可能略高于市价（流动性溢价）
        - 回购计划可能分批执行
    """
    # TODO: 计算回购股数
    # 提示：Shares = Amount / Price
    pass


def eps_after_repurchase(
    net_income: float,
    shares_outstanding: float,
    shares_repurchased: float
) -> float:
    """
    计算回购后的每股收益。

    【公式】
    EPS_after = Net Income / (Shares - Repurchased)
    回购后EPS = 净利润 / (总股数 - 回购股数)

    【EPS增厚效应】
    回购减少流通股数，如果净利润不变，EPS会上升。

    设回购前：EPS_0 = NI / N
    回购后：EPS_1 = NI / (N - R)

    EPS增长率 = R / (N - R)

    【注意事项】
    EPS增加不一定创造价值：
    - 回购使用了现金（减少了资产）
    - 股东持股比例上升，但公司总价值可能不变
    - 关键是回购价格是否低于内在价值

    【与股利的比较】
    - 回购：EPS上升，股价不变（理论上）
    - 股利：EPS不变，股价下跌（除权）
    - 两者对股东财富影响理论上相同（MM无关论）

    参数:
        net_income: 净利润
        shares_outstanding: 原流通股数
        shares_repurchased: 回购股数

    返回:
        回购后EPS

    示例:
        净利润10亿，原股数2亿股，回购0.2亿股
        >>> eps_after_repurchase(10, 2, 0.2)
        5.56  # EPS从5元升至5.56元

    对比:
        回购前EPS = 10/2 = 5元
        EPS增长约11%
    """
    # TODO: 计算回购后EPS
    # 提示：EPS = NI / (Shares - Repurchased)
    pass


def tax_advantage_of_repurchase(
    dividend_tax_rate: float,
    capital_gains_tax_rate: float,
    gain_percentage: float
) -> float:
    """
    计算回购相对于股利的税收优势。

    【税收比较】
    现金股利：
    - 全额按股利税率征税
    - 每1元股利，税后收到 (1 - t_d) 元

    股票回购：
    - 只有资本利得部分征税
    - 如果成本基础是 (1 - gain_percentage)
    - 每1元分配，税收 = gain_percentage × t_cg
    - 税后收到 1 - gain_percentage × t_cg

    【税收优势】
    税收节省 = (1 - gain_percentage × t_cg) - (1 - t_d)
             = t_d - gain_percentage × t_cg

    【其他税收考量】
    1. 资本利得可延迟纳税（时间价值）
    2. 继承时成本基础可提升（step-up in basis）
    3. 长期资本利得税率可能更低
    4. 某些投资者（如养老金）免税

    参数:
        dividend_tax_rate: 股利税率（t_d）
        capital_gains_tax_rate: 资本利得税率（t_cg）
        gain_percentage: 收益占投资的比例（如0.5表示50%是利得）

    返回:
        每1元分配的税收节省

    示例:
        股利税率20%，资本利得税率15%，增值比例50%
        >>> tax_advantage_of_repurchase(0.20, 0.15, 0.5)
        0.125  # 回购每1元节省0.125元税

    解释:
        股利：缴税0.20元
        回购：只有0.5元是利得，缴税0.5×0.15=0.075元
        节省：0.20 - 0.075 = 0.125元
    """
    # TODO: 计算税收优势
    # 提示：税收节省 = t_d - gain_percentage × t_cg
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
