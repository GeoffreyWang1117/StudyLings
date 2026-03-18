# EXERCISE: exchange_rate1
# DIFFICULTY: ★★★☆☆
# TOPIC: 汇率决定理论
#
# 说明：
# 汇率是一国货币相对于另一国货币的价格，是开放经济宏观经济学的核心变量。
#
# 【汇率标价法】
# - 直接标价法：1单位外币 = X单位本币（中国采用）
#   如：1美元 = 7.2人民币
# - 间接标价法：1单位本币 = X单位外币（英美采用）
#   如：1英镑 = 1.25美元
#
# 【汇率决定理论】
#
# 1. 购买力平价（PPP）
#    基于一价定律：同一商品在不同国家应有相同价格
#    绝对PPP：E = P / P*（名义汇率 = 价格水平之比）
#    相对PPP：ΔE/E = π - π*（汇率变化 = 通胀差）
#
# 2. 利率平价（IRP）
#    无套利条件下，国内外投资收益应相等
#    抛补利率平价（CIP）：F/S = (1+i)/(1+i*)
#    非抛补利率平价（UIP）：E[S']/S = (1+i)/(1+i*)
#
# 3. 货币模型
#    E = (M/M*) × (Y*/Y)^η × exp(φ(i-i*))
#
# 【实际汇率】
# RER = E × P* / P
# 衡量国际竞争力，RER上升（实际贬值）提高出口竞争力
#
# 任务：
# 1. 计算PPP汇率
# 2. 验证利率平价
# 3. 分析汇率变动
#
# HINT1: PPP长期成立，短期偏离大
# HINT2: CIP几乎完美成立，UIP常被违反
# HINT3: 实际汇率反映相对购买力

import numpy as np


def purchasing_power_parity(
    price_home: float,
    price_foreign: float
) -> float:
    """
    绝对购买力平价。

    基于一价定律：相同商品在不同国家应有相同价格
    P = E × P*（本国价格 = 汇率 × 外国价格）

    解得PPP汇率：E = P / P*

    参数:
        price_home: 国内价格水平（或价格指数）
        price_foreign: 国外价格水平（或价格指数）

    返回:
        PPP汇率（直接标价法：1外币=X本币）

    示例:
        巨无霸在中国卖24元，在美国卖4美元
        >>> purchasing_power_parity(24, 4)
        6.0  # PPP汇率：1美元=6人民币

    注意:
        实际汇率常偏离PPP，尤其短期内
        原因：贸易壁垒、运输成本、非贸易品、价格粘性
    """
    # TODO: 计算绝对PPP汇率
    # 提示：E = P / P*
    pass


def relative_ppp(
    inflation_home: float,
    inflation_foreign: float,
    initial_rate: float
) -> float:
    """
    相对购买力平价。

    相对PPP关注汇率变化而非汇率水平：
    ΔE/E ≈ π - π*（汇率变化率 ≈ 通胀差）

    推导：
    E₁/E₀ = (P₁/P₀) / (P*₁/P*₀)
    E₁ = E₀ × (1+π) / (1+π*)

    含义：高通胀国货币趋于贬值

    参数:
        inflation_home: 国内通胀率（如0.05表示5%）
        inflation_foreign: 国外通胀率
        initial_rate: 初始汇率

    返回:
        预期未来汇率

    示例:
        中国通胀3%，美国通胀2%，当前汇率7.0
        >>> relative_ppp(0.03, 0.02, 7.0)
        7.069  # 人民币预期小幅贬值
    """
    # TODO: 计算相对PPP汇率
    # 提示：E₁ = E₀ × (1+π) / (1+π*)
    pass


def real_exchange_rate(
    nominal_rate: float,
    price_home: float,
    price_foreign: float
) -> float:
    """
    计算实际汇率。

    实际汇率衡量以外国商品表示的本国商品的相对价格：
    RER = E × P* / P

    其中：
    - E: 名义汇率（直接标价）
    - P: 国内价格水平
    - P*: 国外价格水平

    解读：
    - RER > 1：本国商品相对便宜，有竞争力
    - RER < 1：本国商品相对昂贵，缺乏竞争力
    - RER上升（实际贬值）：提高出口竞争力

    参数:
        nominal_rate: 名义汇率
        price_home: 国内价格水平
        price_foreign: 国外价格水平

    返回:
        实际汇率

    示例:
        名义汇率7.0，中国CPI=110，美国CPI=105
        >>> real_exchange_rate(7.0, 110, 105)
        6.68  # 实际汇率低于名义汇率
    """
    # TODO: 计算实际汇率
    # 提示：RER = E × P* / P
    pass


def covered_interest_parity(
    spot_rate: float,
    interest_home: float,
    interest_foreign: float
) -> float:
    """
    抛补利率平价（CIP）求远期汇率。

    抛补利率平价条件：
    在远期市场锁定汇率后，国内外投资应无套利机会

    公式推导：
    1单位外币投资外国：(1 + i*)
    1单位外币换成本币投资国内，再换回外币：(1/S) × (1 + i) × F
    无套利均衡：(1 + i*) = (1/S) × (1 + i) × F

    整理得：F/S = (1 + i) / (1 + i*)

    远期升水（F>S）当 i > i*

    参数:
        spot_rate: 即期汇率S（直接标价）
        interest_home: 国内利率
        interest_foreign: 国外利率

    返回:
        远期汇率F

    示例:
        即期7.0，国内利率4%，国外利率2%
        >>> covered_interest_parity(7.0, 0.04, 0.02)
        7.137  # 远期升水，本币预期贬值

    注意:
        CIP在成熟金融市场几乎完美成立
        偏离CIP意味着套利机会
    """
    # TODO: 计算远期汇率
    # 提示：F = S × (1 + i) / (1 + i*)
    pass


def forward_premium(
    spot_rate: float,
    forward_rate: float,
    days: int = 360
) -> float:
    """
    计算远期升贴水（年化）。

    远期升水：F > S，外币远期价格高于即期
    远期贴水：F < S，外币远期价格低于即期

    年化升贴水率 = (F - S) / S × (360 / days) × 100%

    参数:
        spot_rate: 即期汇率
        forward_rate: 远期汇率
        days: 远期天数（默认360天=1年）

    返回:
        年化升贴水率（正为升水，负为贴水）

    示例:
        即期7.0，90天远期7.05
        >>> forward_premium(7.0, 7.05, 90)
        0.0286  # 年化升水约2.86%
    """
    # TODO: 计算远期升贴水
    # 提示：(F - S) / S × (360 / days)
    pass


def uncovered_interest_parity(
    spot_rate: float,
    interest_home: float,
    interest_foreign: float
) -> float:
    """
    非抛补利率平价（UIP）求预期汇率。

    UIP条件（风险中性假设下）：
    投资者对不同货币资产的预期收益应相等

    E[S'] / S = (1 + i) / (1 + i*)

    与CIP的区别：
    - CIP使用远期汇率（无风险）
    - UIP使用预期即期汇率（有风险）

    参数:
        spot_rate: 即期汇率
        interest_home: 国内利率
        interest_foreign: 国外利率

    返回:
        预期未来即期汇率

    注意:
        UIP经常被违反（"远期溢价之谜"）
        高利率货币往往升值而非贬值
    """
    # TODO: 计算UIP预期汇率
    # 提示：E[S'] = S × (1 + i) / (1 + i*)
    pass


def monetary_model_exchange_rate(
    money_home: float,
    money_foreign: float,
    income_home: float,
    income_foreign: float,
    interest_home: float,
    interest_foreign: float,
    income_elasticity: float = 1.0,
    interest_elasticity: float = 0.5
) -> float:
    """
    货币模型汇率。

    货币模型将汇率视为两国相对货币供求的结果。

    基于货币数量论：
    M/P = L(Y, i)（实际货币需求）

    结合PPP：E = P/P*

    得到：E = (M/M*) × (Y*/Y)^η × exp(φ(i - i*))

    含义：
    - 货币供给增加 → 本币贬值
    - 收入增加 → 本币升值（货币需求增加）
    - 利率上升 → 本币贬值（货币需求减少）

    参数:
        money_home, money_foreign: 货币供给
        income_home, income_foreign: 实际收入
        interest_home, interest_foreign: 利率
        income_elasticity: 货币需求的收入弹性（通常约1）
        interest_elasticity: 货币需求的利率半弹性

    返回:
        均衡汇率
    """
    # TODO: 计算货币模型汇率
    # 提示：E = (M/M*) × (Y*/Y)^η × exp(φ(i - i*))
    pass


def effective_exchange_rate(
    bilateral_rates: np.ndarray,
    trade_weights: np.ndarray,
    base_rates: np.ndarray = None
) -> float:
    """
    计算名义有效汇率指数（NEER）。

    有效汇率是对多个贸易伙伴汇率的加权平均，
    权重通常基于贸易份额。

    计算公式（几何平均）：
    NEER = Π (Eᵢ / E₀ᵢ)^wᵢ

    其中：
    - Eᵢ: 与第i国的双边汇率
    - E₀ᵢ: 基期双边汇率
    - wᵢ: 第i国的贸易权重

    参数:
        bilateral_rates: 当前双边汇率数组
        trade_weights: 贸易权重（和为1）
        base_rates: 基期汇率（默认为1，即计算变化率）

    返回:
        有效汇率指数

    示例:
        与美国汇率7.0（权重0.3），与欧洲7.5（权重0.4），与日本0.05（权重0.3）
    """
    # TODO: 计算有效汇率
    # 提示：使用几何加权平均
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
