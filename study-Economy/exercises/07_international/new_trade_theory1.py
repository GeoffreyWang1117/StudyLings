# EXERCISE: new_trade_theory1
# DIFFICULTY: ★★★★☆
# TOPIC: 新贸易理论（规模经济、产业内贸易）
#
# 说明：
# 新贸易理论（New Trade Theory）由保罗·克鲁格曼（Paul Krugman）
# 在1979年开创，他因此获得2008年诺贝尔经济学奖。
#
# 【传统贸易理论的局限】
#
# 李嘉图和赫克歇尔-俄林模型基于以下假设：
# - 完全竞争
# - 规模报酬不变
# - 同质产品
#
# 这些模型预测：
# - 贸易基于比较优势
# - 贸易发生在不同产业之间（产业间贸易）
# - 要素禀赋差异越大，贸易越多
#
# 但现实中观察到：
# - 大量贸易发生在相似国家之间（如美国和欧洲）
# - 同一产业内存在双向贸易（如德国和法国互相出口汽车）
# - 发达国家之间贸易量最大
#
# 【新贸易理论的核心要素】
#
# 1. 规模报酬递增（Increasing Returns to Scale）
#    - 生产规模扩大 → 平均成本下降
#    - 来源：固定成本分摊、专业化分工、学习效应
#
# 2. 不完全竞争（Imperfect Competition）
#    - 规模经济导致市场集中
#    - 垄断竞争：产品差异化 + 自由进入
#
# 3. 产品差异化（Product Differentiation）
#    - 同类产品有不同品牌、款式、特性
#    - 消费者偏好多样性
#
# 【克鲁格曼模型】
#
# 基本设定：
# - 垄断竞争市场
# - 规模经济（固定成本 + 恒定边际成本）
# - 消费者爱好多样性（CES效用函数）
#
# 成本结构：
# TC = F + c × Q（总成本 = 固定成本 + 边际成本 × 产量）
# AC = F/Q + c（平均成本递减）
#
# 垄断竞争定价：
# P = MC × ε/(ε-1)（价格 = 边际成本 × 加成）
#
# 贸易利得来源：
# 1. 规模经济效应：更大市场 → 更大生产规模 → 更低成本
# 2. 多样性效应：更多产品种类 → 更高消费者效用
#
# 【产业内贸易指数（Grubel-Lloyd Index）】
#
# GL = 1 - |X - M| / (X + M)
#
# 其中：X = 出口，M = 进口
#
# 解读：
# - GL = 0：纯产业间贸易（只出口或只进口）
# - GL = 1：纯产业内贸易（出口 = 进口）
#
# 发达国家之间GL指数通常很高（0.6-0.8）
#
# 【本地市场效应（Home Market Effect）】
#
# 克鲁格曼的重要发现：
# 在规模经济和贸易成本存在时，
# 需求较大的国家在该产业的生产份额将超过其需求份额。
#
# 例如：
# - A国占全球汽车需求的60%
# - A国可能占全球汽车生产的70%以上
# - 因为在A国生产可以节省运输成本
#
# 这解释了产业集聚现象。
#
# 【引力模型（Gravity Model）】
#
# 贸易量与经济规模成正比，与距离成反比：
# Trade_ij = G × (GDP_i × GDP_j) / Distance^β
#
# 这个简单模型对实际贸易有惊人的解释力（R² > 0.7）
#
# 任务：
# 1. 理解规模经济与贸易的关系
# 2. 计算产业内贸易指数
# 3. 分析多样性收益
# 4. 运用引力模型
#
# HINT1: 规模经济使贸易利得超越比较优势
# HINT2: 产业内贸易指数衡量同类产品双向贸易
# HINT3: 引力模型解释双边贸易量

import numpy as np


def average_cost_with_scale_economies(
    fixed_cost: float,
    marginal_cost: float,
    quantity: float
) -> float:
    """
    计算规模经济下的平均成本。

    规模经济的核心：产量增加，平均成本下降。

    成本结构：
    总成本：TC = F + c × Q
    平均成本：AC = TC/Q = F/Q + c

    其中：
    - F: 固定成本（研发、设备、厂房）
    - c: 边际成本（每单位可变成本）
    - Q: 产量

    AC曲线特征：
    - Q很小时：AC很高（固定成本分摊少）
    - Q增加时：AC下降（固定成本被稀释）
    - Q→∞时：AC→c（接近边际成本）

    规模经济的来源：
    1. 固定成本分摊
    2. 专业化分工
    3. 大规模采购议价
    4. 学习曲线效应

    参数:
        fixed_cost: 固定成本F
                    例如：F = 100万（研发投入）
        marginal_cost: 边际成本c
                       例如：c = 10（每单位生产成本）
        quantity: 产量Q
                  例如：Q = 10万单位

    返回:
        平均成本

    示例:
        固定成本100万，边际成本10，产量10万
        >>> average_cost_with_scale_economies(100, 10, 10)
        20.0  # 平均成本20（100/10 + 10）

        产量增加到50万
        >>> average_cost_with_scale_economies(100, 10, 50)
        12.0  # 平均成本降至12（100/50 + 10）

    TODO提示：
    - AC = F/Q + c
    """
    # TODO: 计算平均成本
    # 提示：AC = fixed_cost / quantity + marginal_cost
    pass


def monopolistic_competition_price(
    marginal_cost: float,
    elasticity: float
) -> float:
    """
    计算垄断竞争定价。

    垄断竞争企业面临向下倾斜的需求曲线，
    通过最大化利润来定价。

    利润最大化条件：MR = MC

    需求弹性与边际收益的关系：
    MR = P × (1 - 1/ε)

    代入MR = MC：
    P × (1 - 1/ε) = MC
    P = MC × ε/(ε-1)

    加成定价公式：
    P = MC × (1 + m)
    其中 m = 1/(ε-1) 是加成率

    弹性与加成的关系：
    - ε大（需求弹性高）→ 加成小 → 价格接近MC
    - ε小（需求弹性低）→ 加成大 → 价格远高于MC

    参数:
        marginal_cost: 边际成本
                       例如：MC = 10
        elasticity: 需求弹性（绝对值，>1）
                    例如：ε = 4

    返回:
        均衡价格

    示例:
        边际成本10，需求弹性4
        >>> monopolistic_competition_price(10, 4)
        13.33  # 价格 = 10 × 4/(4-1) = 13.33

        边际成本10，需求弹性2
        >>> monopolistic_competition_price(10, 2)
        20.0  # 价格 = 10 × 2/(2-1) = 20

    TODO提示：
    - P = MC × ε / (ε - 1)
    """
    # TODO: 计算垄断竞争价格
    # 提示：P = marginal_cost × elasticity / (elasticity - 1)
    pass


def number_of_varieties(
    market_size: float,
    fixed_cost: float,
    demand_per_variety: float
) -> int:
    """
    计算均衡下的产品种类数。

    在垄断竞争市场中，企业自由进入直到利润为零。

    零利润条件：
    总收入 = 总成本
    P × Q = F + c × Q

    由于P > c（有加成），每个企业都有正的销售量Q。
    但自由进入确保经济利润为零。

    均衡产品种类数取决于：
    - 市场规模L（消费者数量或总支出）
    - 固定成本F（进入门槛）
    - 每种产品的需求

    简化公式：
    n ≈ L / (F/利润率 + 每品种运营支出)

    更直观的理解：
    市场越大，支持的品种越多
    固定成本越高，品种越少

    参数:
        market_size: 市场规模（总消费支出）
                     例如：L = 1000万
        fixed_cost: 每个企业的固定成本
                    例如：F = 100万
        demand_per_variety: 每种产品的均衡需求量
                            例如：q = 10万单位

    返回:
        产品种类数（整数）

    示例:
        市场1000万，固定成本100万，每品种需求10万
        >>> number_of_varieties(1000, 100, 10)
        10  # 约10种产品

    TODO提示：
    - 简化计算：n = market_size / (fixed_cost + marginal_cost × demand_per_variety)
    - 这里进一步简化：n ≈ market_size / (fixed_cost / profit_rate)
    - 假设零利润均衡，可用 n = int(market_size / fixed_cost) 作为近似
    """
    # TODO: 计算产品种类数
    # 提示：简化为 n = market_size / (fixed_cost × 某个系数)
    # 或者 n = int(market_size / (fixed_cost + demand_per_variety × marginal_cost))
    pass


def grubel_lloyd_index(
    exports: float,
    imports: float
) -> float:
    """
    计算Grubel-Lloyd产业内贸易指数。

    GL指数是衡量产业内贸易程度的标准指标，
    由Herb Grubel和Peter Lloyd于1975年提出。

    公式：
    GL = 1 - |X - M| / (X + M)
       = (X + M - |X - M|) / (X + M)
       = 2 × min(X, M) / (X + M)

    解读：
    - GL = 0：纯产业间贸易
      例如：只出口咖啡，只进口汽车
    - GL = 1：纯产业内贸易
      例如：出口德国汽车，进口日本汽车，金额相等

    经验规律：
    - 发达国家之间：GL通常为0.5-0.8
    - 发展中国家与发达国家之间：GL通常为0.2-0.4
    - 初级产品部门：GL通常很低

    参数:
        exports: 该产业出口额
                 例如：X = 80亿美元
        imports: 该产业进口额
                 例如：M = 60亿美元

    返回:
        GL指数（0到1之间）

    示例:
        出口80亿，进口60亿
        >>> grubel_lloyd_index(80, 60)
        0.857  # 1 - |80-60|/(80+60) = 1 - 20/140 = 0.857

        出口100亿，进口0（纯出口）
        >>> grubel_lloyd_index(100, 0)
        0.0  # 纯产业间贸易

        出口50亿，进口50亿
        >>> grubel_lloyd_index(50, 50)
        1.0  # 纯产业内贸易

    TODO提示：
    - GL = 1 - |X - M| / (X + M)
    - 注意处理分母为0的情况
    """
    # TODO: 计算GL指数
    # 提示：GL = 1 - abs(exports - imports) / (exports + imports)
    pass


def aggregate_gl_index(
    exports: np.ndarray,
    imports: np.ndarray
) -> float:
    """
    计算加权平均Grubel-Lloyd指数。

    当分析多个产业时，需要计算加总的GL指数。

    加权公式：
    GL_总 = Σ wᵢ × GLᵢ

    其中权重：
    wᵢ = (Xᵢ + Mᵢ) / Σ(X + M)

    即按各产业贸易额占比加权。

    替代计算方式：
    GL_总 = 1 - Σ|Xᵢ - Mᵢ| / Σ(Xᵢ + Mᵢ)

    这两种方法结果相同。

    参数:
        exports: 各产业出口额数组
                 例如：[80, 50, 30]（三个产业）
        imports: 各产业进口额数组
                 例如：[60, 55, 10]

    返回:
        加总GL指数

    示例:
        三个产业：出口[80,50,30]，进口[60,55,10]
        >>> aggregate_gl_index(np.array([80,50,30]), np.array([60,55,10]))
        0.824  # 加权平均GL指数

    TODO提示：
    - GL = 1 - sum(|X - M|) / sum(X + M)
    """
    # TODO: 计算加总GL指数
    # 提示：GL = 1 - np.sum(np.abs(exports - imports)) / np.sum(exports + imports)
    pass


def variety_gain(
    initial_varieties: int,
    final_varieties: int,
    sigma: float
) -> float:
    """
    计算多样性增加的福利收益。

    在克鲁格曼模型中，消费者效用来自多样性。

    CES效用函数：
    U = (Σ cᵢ^ρ)^(1/ρ)

    其中：
    - ρ = (σ-1)/σ（σ是替代弹性）
    - σ > 1：产品之间可替代但不完全替代

    多样性增加的福利等价：
    如果产品种类从n₀增加到n₁，
    等价于收入增加的比例为：

    收入等价增长 = (n₁/n₀)^(1/(σ-1)) - 1

    直觉：
    - σ大（产品高度可替代）→ 多样性价值低
    - σ小（产品差异大）→ 多样性价值高

    参数:
        initial_varieties: 初始产品种类数n₀
                           例如：n₀ = 10
        final_varieties: 最终产品种类数n₁
                         例如：n₁ = 20
        sigma: 替代弹性σ
               例如：σ = 4

    返回:
        等价收入增长比例

    示例:
        种类从10增加到20，替代弹性4
        >>> variety_gain(10, 20, 4)
        0.26  # 等价于收入增加26%

        计算：(20/10)^(1/(4-1)) - 1 = 2^(1/3) - 1 ≈ 0.26

    TODO提示：
    - gain = (n₁/n₀)^(1/(σ-1)) - 1
    """
    # TODO: 计算多样性收益
    # 提示：gain = (final_varieties / initial_varieties) ** (1 / (sigma - 1)) - 1
    pass


def home_market_effect(
    home_share_demand: float,
    transport_cost: float,
    elasticity: float
) -> float:
    """
    计算本地市场效应。

    本地市场效应（Home Market Effect）是新贸易理论的重要发现：
    需求份额较大的国家，将获得超比例的生产份额。

    机制：
    - 规模经济 → 生产集中有利
    - 贸易成本 → 靠近大市场有利
    - 结果 → 大市场吸引更多生产

    简化模型：
    本国生产份额 = f(本国需求份额, 贸易成本, 替代弹性)

    当贸易成本存在且σ > 1时：
    生产份额 > 需求份额（对于需求大的国家）

    公式（Krugman简化版）：
    生产份额 ≈ 需求份额 + 放大因子 × (需求份额 - 0.5)

    放大因子与(σ, τ)有关，τ是贸易成本

    参数:
        home_share_demand: 本国需求份额（0到1）
                           例如：0.6（本国占全球需求60%）
        transport_cost: 运输成本（冰山成本形式，>1）
                        例如：1.2（20%的货物在运输中"融化"）
        elasticity: 替代弹性σ
                    例如：σ = 4

    返回:
        本国生产份额（0到1）

    示例:
        本国需求60%，运输成本20%，替代弹性4
        >>> home_market_effect(0.6, 1.2, 4)
        0.68  # 本国生产份额68%（超过需求份额）

    TODO提示：
    - 简化公式：生产份额 ≈ 需求份额 + k × (需求份额 - 0.5)
    - 其中 k 与运输成本和替代弹性有关
    - k ≈ (τ^(1-σ) - 1) / (τ^(1-σ) + 1)
    """
    # TODO: 计算本地市场效应
    # 提示：
    # phi = transport_cost ** (1 - elasticity)
    # k = (1 - phi) / (1 + phi)  # 放大因子
    # production_share = home_share_demand + k * (home_share_demand - 0.5)
    pass


def gravity_equation(
    gdp_i: float,
    gdp_j: float,
    distance: float,
    gravity_constant: float = 1.0,
    distance_elasticity: float = -1.0
) -> float:
    """
    引力模型预测双边贸易量。

    引力模型是国际贸易实证研究中最成功的模型之一。

    基本形式：
    Trade_ij = G × (GDP_i × GDP_j) / Distance^β

    或取对数：
    ln(Trade) = ln(G) + α₁ln(GDP_i) + α₂ln(GDP_j) + βln(Distance)

    经验规律：
    - GDP系数通常接近1
    - 距离弹性通常在-0.7到-1.5之间
    - R²通常超过0.7

    理论基础：
    - Anderson & van Wincoop (2003) 提供微观基础
    - 可从CES效用函数和冰山贸易成本推导

    控制变量（扩展模型）：
    - 共同语言（+）
    - 殖民关系（+）
    - 区域贸易协定（+）
    - 共同边界（+）

    参数:
        gdp_i: i国GDP
               例如：GDP_美国 = 25万亿美元
        gdp_j: j国GDP
               例如：GDP_中国 = 18万亿美元
        distance: 两国距离（通常是首都或经济中心距离）
                  例如：11000公里
        gravity_constant: 引力常数G
                          例如：G = 1.0（可根据数据校准）
        distance_elasticity: 距离弹性β（通常为负）
                             例如：β = -1.0

    返回:
        预测贸易量

    示例:
        美国GDP 25万亿，中国GDP 18万亿，距离11000公里
        >>> gravity_equation(25, 18, 11000, 1.0, -1.0)
        0.041  # 预测贸易量（需要根据单位调整）

        计算：1.0 × (25 × 18) / 11000^1 = 450/11000 ≈ 0.041

    TODO提示：
    - Trade = G × (GDP_i × GDP_j) / Distance^|β|
    - 或 Trade = G × (GDP_i × GDP_j) × Distance^β（β为负）
    """
    # TODO: 计算引力模型贸易量
    # 提示：Trade = gravity_constant × (gdp_i × gdp_j) × (distance ** distance_elasticity)
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
