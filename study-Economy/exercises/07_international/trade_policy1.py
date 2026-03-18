# EXERCISE: trade_policy1
# DIFFICULTY: ★★★☆☆
# TOPIC: 贸易政策分析（关税、配额）
#
# 说明：
# 贸易政策是政府干预国际贸易的各种措施，主要包括关税和非关税壁垒。
# 理解贸易政策的福利效应是国际经济学的核心内容。
#
# 【贸易政策工具】
#
# 1. 关税（Tariff）
#    - 从价税：按商品价值的百分比征收，如10%关税
#    - 从量税：按商品数量征收，如每吨100美元
#    - 混合税：从价与从量相结合
#
# 2. 非关税壁垒（Non-Tariff Barriers）
#    - 进口配额：限制进口数量
#    - 自愿出口限制（VER）：出口国"自愿"限制出口
#    - 进口许可证：政府审批进口
#    - 技术性壁垒：卫生、安全、环保标准
#    - 反倾销、反补贴措施
#
# 3. 出口政策
#    - 出口补贴：鼓励出口
#    - 出口禁令：限制战略物资出口
#
# 【关税的福利分析（局部均衡）】
#
# 假设小国开放经济，世界价格 P_w 固定
# 征收关税后，国内价格 P_d = P_w × (1 + t)
#
# 福利变化：
# ┌─────────────────────────────────────────────────────────┐
# │  主体        │    变化           │    原因              │
# ├─────────────────────────────────────────────────────────┤
# │ 消费者剩余   │    减少 ↓         │ 价格上升，消费减少   │
# │ 生产者剩余   │    增加 ↑         │ 价格上升，生产扩大   │
# │ 政府收入     │    增加 ↑         │ 关税收入             │
# │ 社会总福利   │    净损失 ↓       │ 无谓损失（两个三角） │
# └─────────────────────────────────────────────────────────┘
#
# 无谓损失来源：
# 1. 生产扭曲：高成本国内生产替代低成本进口
# 2. 消费扭曲：消费者减少高价值消费
#
# 【大国关税分析】
#
# 大国可以影响世界价格：
# - 征收关税 → 减少进口需求 → 世界价格下降
# - 贸易条件改善（进口价格下降）
# - 可能获得净福利收益
#
# 最优关税公式：
# t* = 1/ε
# 其中ε是外国出口供给弹性
#
# 外国供给弹性越低，最优关税越高
# （买方垄断力量越强）
#
# 【有效保护率】
#
# 名义关税可能低估或高估对产业的真实保护程度。
#
# 有效保护率（ERP）= (V' - V) / V
# 其中：V = 自由贸易下的增加值，V' = 关税下的增加值
#
# 公式：
# ERP = (t_o - a × t_i) / (1 - a)
#
# 其中：
# - t_o: 产出品关税
# - t_i: 投入品关税
# - a: 投入品占产出品价值的比例
#
# 重要结论：
# - 如果 t_o > a × t_i：ERP > t_o（有效保护高于名义保护）
# - 如果 t_o < a × t_i：ERP < t_o（有效保护低于名义保护）
# - 如果 t_i > t_o/a：ERP < 0（负保护！）
#
# 【配额与关税的比较】
#
# 相同点：都提高国内价格，保护国内生产者
#
# 不同点：
# ┌─────────────┬─────────────────┬─────────────────┐
# │   特征      │     关税        │     配额        │
# ├─────────────┼─────────────────┼─────────────────┤
# │ 收入归属    │ 政府            │ 配额持有者      │
# │ 需求变化时  │ 进口量自动调整  │ 价格变化        │
# │ 透明度      │ 高              │ 低              │
# │ 管理成本    │ 低              │ 高（寻租）      │
# └─────────────┴─────────────────┴─────────────────┘
#
# 配额租金 = (P_d - P_w) × 配额量
# 归谁取决于配额分配方式
#
# 任务：
# 1. 计算关税后的国内价格
# 2. 分析关税的福利效应（消费者/生产者剩余变化）
# 3. 理解最优关税理论
# 4. 计算有效保护率
#
# HINT1: 小国无法影响世界价格
# HINT2: 大国可通过关税改善贸易条件
# HINT3: 有效保护率考虑投入品关税的影响

import numpy as np


def domestic_price_with_tariff(
    world_price: float,
    tariff_rate: float
) -> float:
    """
    计算从价税后的国内价格。

    从价税（Ad Valorem Tariff）按商品价值的百分比征收。

    公式：
    P_d = P_w × (1 + t)

    其中：
    - P_d: 国内价格（含税）
    - P_w: 世界价格（CIF价格）
    - t: 从价税率

    经济学含义：
    - 关税提高了进口商品的国内售价
    - 消费者支付更高价格
    - 国内生产者获得价格保护

    参数:
        world_price: 世界价格（CIF，成本+保险+运费）
                     例如：P_w = 100美元/单位
        tariff_rate: 从价关税率
                     例如：t = 0.20表示20%关税

    返回:
        关税后国内价格

    示例:
        世界价格100美元，关税率20%
        >>> domestic_price_with_tariff(100, 0.20)
        120.0  # 国内价格120美元

    TODO提示：
    - P_d = P_w × (1 + t)
    """
    # TODO: 计算关税后国内价格
    # 提示：P_d = world_price × (1 + tariff_rate)
    pass


def import_quantity(
    domestic_demand: float,
    domestic_supply: float
) -> float:
    """
    计算进口量。

    进口量 = 国内需求 - 国内供给

    公式：
    M = D - S

    前提：国内需求 > 国内供给（否则不需要进口）

    在关税分析中：
    - 自由贸易时：较低世界价格 → 高需求，低供给 → 大量进口
    - 关税后：国内价格上升 → 需求下降，供给上升 → 进口减少

    参数:
        domestic_demand: 国内需求量D
                         例如：D = 100万单位
        domestic_supply: 国内供给量S
                         例如：S = 60万单位

    返回:
        进口量（正值表示进口，负值表示出口）

    示例:
        国内需求100万，国内供给60万
        >>> import_quantity(100, 60)
        40.0  # 进口40万单位

    TODO提示：
    - M = D - S
    """
    # TODO: 计算进口量
    # 提示：M = domestic_demand - domestic_supply
    pass


def consumer_surplus_change(
    price_old: float,
    price_new: float,
    quantity_old: float,
    quantity_new: float
) -> float:
    """
    计算消费者剩余变化（假设线性需求曲线）。

    消费者剩余是消费者愿意支付的价格与实际支付价格之差的总和。

    图形理解（需求曲线下方，价格线上方的面积）：

    价格 ↑
         │╲
         │ ╲  需求曲线
    P_new├───╲───────
         │    ╲     │
    P_old├─────╲────│
         │      ╲   │
         └──────────┴───→ 数量
               Q_new Q_old

    关税导致价格上升时：
    - 消费者剩余减少（梯形面积）

    近似公式（线性需求）：
    ΔCS = -½ × (Q_old + Q_new) × (P_new - P_old)

    注意：
    - 如果价格上升，ΔCS为负（消费者受损）
    - 如果价格下降，ΔCS为正（消费者受益）

    参数:
        price_old: 原价格（如自由贸易价格）
                   例如：P_old = 100
        price_new: 新价格（如关税后价格）
                   例如：P_new = 120
        quantity_old: 原消费量
                      例如：Q_old = 100万
        quantity_new: 新消费量
                      例如：Q_new = 80万

    返回:
        消费者剩余变化（负值表示减少）

    示例:
        价格从100升到120，数量从100万降到80万
        >>> consumer_surplus_change(100, 120, 100, 80)
        -1800.0  # 消费者剩余减少1800万

        计算：-0.5 × (100 + 80) × (120 - 100) = -1800

    TODO提示：
    - ΔCS = -0.5 × (Q_old + Q_new) × (P_new - P_old)
    """
    # TODO: 计算消费者剩余变化
    # 提示：ΔCS = -0.5 × (quantity_old + quantity_new) × (price_new - price_old)
    pass


def producer_surplus_change(
    price_old: float,
    price_new: float,
    quantity_old: float,
    quantity_new: float
) -> float:
    """
    计算生产者剩余变化（假设线性供给曲线）。

    生产者剩余是生产者实际获得的价格与愿意接受的最低价格之差的总和。

    图形理解（价格线下方，供给曲线上方的面积）：

    价格 ↑
         │        供给曲线
    P_new├─────────╱
         │       ╱│
    P_old├─────╱──│
         │   ╱    │
         │ ╱      │
         └────────┴───→ 数量
            S_old S_new

    关税导致价格上升时：
    - 生产者剩余增加（梯形面积）

    近似公式（线性供给）：
    ΔPS = ½ × (Q_old + Q_new) × (P_new - P_old)

    参数:
        price_old: 原价格
        price_new: 新价格
        quantity_old: 原供给量
        quantity_new: 新供给量

    返回:
        生产者剩余变化（正值表示增加）

    示例:
        价格从100升到120，供给从60万增到70万
        >>> producer_surplus_change(100, 120, 60, 70)
        1300.0  # 生产者剩余增加1300万

        计算：0.5 × (60 + 70) × (120 - 100) = 1300

    TODO提示：
    - ΔPS = 0.5 × (Q_old + Q_new) × (P_new - P_old)
    """
    # TODO: 计算生产者剩余变化
    # 提示：ΔPS = 0.5 × (quantity_old + quantity_new) × (price_new - price_old)
    pass


def tariff_revenue(
    tariff_rate: float,
    world_price: float,
    import_quantity: float
) -> float:
    """
    计算关税收入。

    关税收入是政府从进口商品征收的税收。

    公式：
    TR = t × P_w × M

    其中：
    - t: 关税率
    - P_w: 世界价格
    - M: 进口量

    图形上，关税收入是一个矩形：
    - 高度 = 关税（P_d - P_w = t × P_w）
    - 宽度 = 关税后的进口量

    参数:
        tariff_rate: 关税率
                     例如：t = 0.20
        world_price: 世界价格
                     例如：P_w = 100
        import_quantity: 关税后进口量
                         例如：M = 30万单位

    返回:
        关税收入

    示例:
        关税率20%，世界价格100，进口30万
        >>> tariff_revenue(0.20, 100, 30)
        600.0  # 关税收入600万

        计算：0.20 × 100 × 30 = 600

    TODO提示：
    - TR = tariff_rate × world_price × import_quantity
    """
    # TODO: 计算关税收入
    # 提示：TR = t × P_w × M
    pass


def deadweight_loss(
    price_change: float,
    production_change: float,
    consumption_change: float
) -> float:
    """
    计算关税的无谓损失（两个三角形之和）。

    无谓损失是社会净福利损失，代表经济效率的损失。

    关税导致两种扭曲：

    1. 生产扭曲三角形（左侧）
       - 高成本国内生产替代低成本进口
       - 面积 = ½ × |ΔP| × |ΔS|

    2. 消费扭曲三角形（右侧）
       - 消费者放弃高价值消费
       - 面积 = ½ × |ΔP| × |ΔD|

    总无谓损失：
    DWL = ½ × |ΔP| × (|ΔS| + |ΔD|)

    或写作：
    DWL = ½ × |ΔP| × |ΔM|（进口变化量）

    参数:
        price_change: 价格变化（通常为正，表示上升）
                      例如：ΔP = 20
        production_change: 国内生产变化（关税后增加）
                           例如：ΔS = 10万
        consumption_change: 消费变化（关税后减少，用绝对值）
                            例如：|ΔD| = 20万

    返回:
        无谓损失（正值）

    示例:
        价格上升20，生产增加10万，消费减少20万
        >>> deadweight_loss(20, 10, 20)
        300.0  # 无谓损失300万

        计算：0.5 × 20 × (10 + 20) = 300

    TODO提示：
    - DWL = 0.5 × |price_change| × (|production_change| + |consumption_change|)
    """
    # TODO: 计算无谓损失
    # 提示：DWL = 0.5 × |ΔP| × (|ΔS| + |ΔD|)
    pass


def optimal_tariff(
    foreign_export_elasticity: float
) -> float:
    """
    计算大国最优关税率。

    大国可以通过征收关税影响世界价格，
    从而改善贸易条件（降低进口价格）。

    最优关税理论：

    大国征收关税 → 减少进口需求 → 世界价格下降
    → 贸易条件改善 → 可能的净福利收益

    最优关税公式：
    t* = 1/ε

    其中：
    - t*: 最优关税率
    - ε: 外国出口供给弹性

    经济学直觉：
    - ε低（外国供给缺乏弹性）→ 关税更多转嫁给外国生产者
      → 最优关税较高
    - ε高（外国供给弹性大）→ 关税更多转嫁给国内消费者
      → 最优关税较低

    局限性：
    - 假设对方不报复（博弈论考虑时最优关税可能为0）
    - 以邻为壑政策可能引发贸易战
    - WTO规则限制关税使用

    参数:
        foreign_export_elasticity: 外国出口供给弹性
                                   例如：ε = 2.0

    返回:
        最优关税率

    示例:
        外国出口供给弹性为2
        >>> optimal_tariff(2.0)
        0.5  # 最优关税率50%

        外国出口供给弹性为5
        >>> optimal_tariff(5.0)
        0.2  # 最优关税率20%

    TODO提示：
    - t* = 1 / ε
    """
    # TODO: 计算最优关税
    # 提示：t* = 1 / foreign_export_elasticity
    pass


def effective_rate_of_protection(
    nominal_tariff_output: float,
    nominal_tariff_input: float,
    input_share: float
) -> float:
    """
    计算有效保护率（ERP）。

    有效保护率衡量关税对国内增加值的真实保护程度，
    考虑了产出品和投入品关税的综合影响。

    公式推导：

    自由贸易下：
    - 产出价格 = 1（标准化）
    - 增加值 V = 1 - a（a是投入品份额）

    征收关税后：
    - 产出价格 = 1 + t_o
    - 投入价格 = a × (1 + t_i)
    - 增加值 V' = (1 + t_o) - a(1 + t_i)

    有效保护率：
    ERP = (V' - V) / V
        = [(1 + t_o) - a(1 + t_i) - (1 - a)] / (1 - a)
        = (t_o - a × t_i) / (1 - a)

    重要情形：
    1. t_i = 0（投入品免税）：ERP = t_o / (1-a) > t_o
       有效保护率高于名义关税
    2. t_i = t_o（统一税率）：ERP = t_o
       有效保护率等于名义关税
    3. t_i > t_o/a：ERP < 0
       负保护！投入品关税过高损害国内生产者

    案例：
    汽车组装（名义关税25%，零部件进口份额70%，零部件关税15%）
    ERP = (0.25 - 0.7×0.15) / (1 - 0.7) = 0.145/0.3 = 48.3%
    有效保护率远高于名义关税！

    参数:
        nominal_tariff_output: 产出品名义关税
                               例如：t_o = 0.25（25%）
        nominal_tariff_input: 投入品名义关税
                              例如：t_i = 0.15（15%）
        input_share: 投入品占产出品价值的比例
                     例如：a = 0.7（70%）

    返回:
        有效保护率

    示例:
        产出关税25%，投入关税15%，投入份额70%
        >>> effective_rate_of_protection(0.25, 0.15, 0.7)
        0.483  # 有效保护率48.3%

    TODO提示：
    - ERP = (t_o - a × t_i) / (1 - a)
    """
    # TODO: 计算有效保护率
    # 提示：ERP = (nominal_tariff_output - input_share × nominal_tariff_input) / (1 - input_share)
    pass


def quota_equivalent_tariff(
    demand_elasticity: float,
    supply_elasticity: float,
    quota_quantity: float,
    free_trade_import: float
) -> float:
    """
    计算配额等价关税率。

    配额等价关税是指能够产生与配额相同进口量效果的关税率。

    理论背景：
    虽然配额和关税都限制进口，但它们不完全等价：
    - 关税下，进口量随价格自动调整
    - 配额下，进口量固定，价格根据供需调整

    计算方法：
    找到使进口量从自由贸易水平下降到配额水平的关税率。

    简化公式（假设线性供需）：
    进口变化率 ≈ (η_d + η_s) × 价格变化率

    其中：
    - η_d: 需求弹性（绝对值）
    - η_s: 供给弹性

    配额导致的进口减少比例：
    ΔM/M = (M_quota - M_free) / M_free

    所需价格上涨比例（即等价关税）：
    t ≈ -ΔM/M / (η_d + η_s)

    参数:
        demand_elasticity: 需求价格弹性（绝对值）
                           例如：η_d = 0.5
        supply_elasticity: 国内供给弹性
                           例如：η_s = 0.3
        quota_quantity: 配额允许的进口量
                        例如：30万单位
        free_trade_import: 自由贸易下的进口量
                           例如：50万单位

    返回:
        等价关税率

    示例:
        需求弹性0.5，供给弹性0.3，配额30万，自由贸易进口50万
        >>> quota_equivalent_tariff(0.5, 0.3, 30, 50)
        0.5  # 等价关税率50%

        计算：进口减少 (30-50)/50 = -0.4
              等价关税 ≈ 0.4 / (0.5 + 0.3) = 0.5

    TODO提示：
    - 计算进口减少比例：(quota - free_trade) / free_trade
    - 等价关税 ≈ -进口减少比例 / (需求弹性 + 供给弹性)
    """
    # TODO: 计算配额等价关税
    # 提示：
    # import_reduction = (quota_quantity - free_trade_import) / free_trade_import
    # equivalent_tariff = -import_reduction / (demand_elasticity + supply_elasticity)
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
