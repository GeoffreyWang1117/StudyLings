# EXERCISE: general_equilibrium1
# DIFFICULTY: ★★★★★
# TOPIC: 一般均衡理论
#
# ============================================================================
# 理论背景
# ============================================================================
#
# 一般均衡理论（General Equilibrium Theory）是微观经济学的巅峰之作，
# 研究所有市场同时达到均衡的状态。该理论由Leon Walras在19世纪奠基，
# 后由Kenneth Arrow和Gerard Debreu在1950年代严格化，他们因此获得诺贝尔奖。
#
# 【与局部均衡的区别】
# - 局部均衡（Partial Equilibrium）：分析单个市场，假设其他市场不变
#   例：只分析苹果市场的供需
# - 一般均衡（General Equilibrium）：同时分析所有市场的相互作用
#   例：苹果价格影响橙子需求，进而影响橙子价格...
#
# ============================================================================
# 纯交换经济（Pure Exchange Economy）
# ============================================================================
#
# 【2×2模型设定】
# - 2个消费者：A和B
# - 2种商品：X和Y
# - 无生产，只有交换
# - 消费者有初始禀赋和效用函数
#
# 【瓦尔拉斯均衡（Walrasian Equilibrium）】
# 定义：价格向量 p* 和配置 (x*, y*) 使得：
# 1. 每个消费者在预算约束下最大化效用
# 2. 所有市场出清（需求 = 供给）
#
# 形式化：
# - 预算约束：px × xᵢ + py × yᵢ ≤ px × ωᵢx + py × ωᵢy
# - 效用最大化：max U(x, y) s.t. 预算约束
# - 市场出清：Σxᵢ = Σωᵢx，Σyᵢ = Σωᵢy
#
# 【瓦尔拉斯法则（Walras' Law）】
# 在任何价格下，所有市场的超额需求价值之和为零：
# Σ pⱼ × EDⱼ = 0
#
# 推论：如果 n-1 个市场出清，第 n 个市场也必然出清。
# 因此只需找到使 n-1 个市场出清的价格。
#
# ============================================================================
# 福利经济学基本定理
# ============================================================================
#
# 【帕累托效率（Pareto Efficiency）】
# 配置是帕累托有效的，如果不存在另一配置使某人更好而无人更差。
#
# 【第一福利定理（First Welfare Theorem）】
# 竞争均衡是帕累托有效的。
# - 意义：市场机制（看不见的手）导致有效配置
# - 条件：完全竞争、无外部性、完全信息
#
# 【第二福利定理（Second Welfare Theorem）】
# 任何帕累托有效配置都可以通过竞争均衡实现（适当再分配后）。
# - 意义：效率与公平可以分离
# - 通过一次性转移支付实现公平，然后让市场实现效率
#
# ============================================================================
# 埃奇沃斯框图（Edgeworth Box）
# ============================================================================
#
# 2×2纯交换经济的图形表示：
#
#          Y轴(A)
#            ↑
#      B原点 ·────────────────────────→ X轴(B)
#            │                        │
#            │     契约曲线           │
#            │        ╱              │
#            │      ╱                │
#            │    ·← 均衡点           │
#            │   /                   │
#            │  /  初始禀赋点         │
#            │ ·                      │
#            │───────────────────────·
#            A原点                   → X轴(A)
#
# 【框图要素】
# - A从左下角看，B从右上角看
# - 框的大小 = 总禀赋
# - 每点代表一种配置
# - 无差异曲线可以画在框内
#
# 【契约曲线（Contract Curve）】
# 所有帕累托有效配置的集合
# 特征：两人无差异曲线相切，MRS_A = MRS_B
#
# ============================================================================
# 任务
# ============================================================================
# 1. 求解瓦尔拉斯均衡：找到均衡价格和配置
# 2. 验证福利定理：检验均衡是否帕累托有效
# 3. 绘制埃奇沃斯框图：可视化契约曲线和均衡
#
# HINT1: 使用瓦尔拉斯法则简化计算，只需一个市场出清
# HINT2: MRS相等是帕累托有效的必要条件
# HINT3: 对于柯布-道格拉斯效用，有解析解

import numpy as np


def demand_cobb_douglas(
    price_x: float,
    price_y: float,
    income: float,
    alpha: float
) -> tuple[float, float]:
    """
    柯布-道格拉斯效用下的需求函数。

    【效用函数】
    U(x, y) = x^α × y^(1-α)

    特性：
    - 齐次函数：U(tx, ty) = t × U(x, y)
    - 边际效用递减
    - 无差异曲线凸向原点

    【预算约束最大化】
    max x^α × y^(1-α)  s.t.  px×x + py×y = m

    构造拉格朗日函数：
    L = x^α × y^(1-α) - λ(px×x + py×y - m)

    一阶条件：
    ∂L/∂x = α × x^(α-1) × y^(1-α) - λpx = 0
    ∂L/∂y = (1-α) × x^α × y^(-α) - λpy = 0
    ∂L/∂λ = -(px×x + py×y - m) = 0

    【MRS = 价格比】
    从前两个条件：
    MRS = MUx/MUy = (α/(1-α)) × (y/x) = px/py

    【需求函数推导】
    将MRS条件代入预算约束：
    px×x + py×y = m
    px×x + px×x×(1-α)/α = m
    px×x/α = m

    解得：
    x* = α × m / px
    y* = (1-α) × m / py

    【柯布-道格拉斯的性质】
    - 花费份额恒定：px×x/m = α，py×y/m = 1-α
    - 无替代效应（单位弹性）
    - 收入效应完全决定需求变化

    参数:
        price_x: 商品X的价格 px
        price_y: 商品Y的价格 py
        income: 收入（或禀赋价值）m = px×ωx + py×ωy
        alpha: 效用函数参数 α∈(0,1)
               α越大，对X的偏好越强

    返回:
        (x需求量, y需求量) 元组

    示例:
        # α=0.5，均等偏好
        >>> demand_cobb_douglas(2, 4, 100, 0.5)
        (25.0, 12.5)  # x=0.5×100/2=25, y=0.5×100/4=12.5

        # α=0.75，偏好X
        >>> demand_cobb_douglas(2, 4, 100, 0.75)
        (37.5, 6.25)  # 更多支出在X上

        # 验证预算约束
        >>> px, py = 2, 4
        >>> x, y = demand_cobb_douglas(px, py, 100, 0.5)
        >>> px*x + py*y
        100.0  # 恰好花完收入

    注意:
        - 需求只依赖于收入和自身价格
        - 价格变化时，花费份额保持不变
    """
    # TODO: 计算需求
    # 提示：
    # x* = alpha × income / price_x
    # y* = (1-alpha) × income / price_y
    pass


def walrasian_equilibrium_2x2(
    endowment_a: tuple[float, float],
    endowment_b: tuple[float, float],
    alpha_a: float,
    alpha_b: float
) -> dict:
    """
    求解2×2纯交换经济的瓦尔拉斯均衡。

    【模型设定】
    - 消费者A：初始禀赋 (ωax, ωay)，效用 U_A = x^αa × y^(1-αa)
    - 消费者B：初始禀赋 (ωbx, ωby)，效用 U_B = x^αb × y^(1-αb)
    - 总禀赋：(Ωx, Ωy) = (ωax+ωbx, ωay+ωby)

    【均衡条件】
    1. A的需求：xₐ = αa×mₐ/px，yₐ = (1-αa)×mₐ/py
       其中 mₐ = px×ωax + py×ωay
    2. B的需求：类似
    3. 市场出清：xₐ + xb = Ωx

    【求解步骤】
    标准化：令 px = 1（X为计价商品），只求 py/px = p

    A的收入：mₐ = ωax + p×ωay
    A对X的需求：xₐ = αa×(ωax + p×ωay)

    B的收入：mb = ωbx + p×ωby
    B对X的需求：xb = αb×(ωbx + p×ωby)

    市场出清：xₐ + xb = Ωx

    αa×(ωax + p×ωay) + αb×(ωbx + p×ωby) = ωax + ωbx

    解出 p*：
    p* = [ωax + ωbx - αa×ωax - αb×ωbx] / [αa×ωay + αb×ωby]
       = [(1-αa)×ωax + (1-αb)×ωbx] / [αa×ωay + αb×ωby]

    参数:
        endowment_a: 消费者A的初始禀赋 (ωax, ωay)
        endowment_b: 消费者B的初始禀赋 (ωbx, ωby)
        alpha_a: A的效用参数 αa
        alpha_b: B的效用参数 αb

    返回:
        {
            'price_ratio': 均衡价格比 py/px,
            'allocation_a': A的均衡配置 (xa, ya),
            'allocation_b': B的均衡配置 (xb, yb)
        }

    示例:
        # 对称情况
        >>> walrasian_equilibrium_2x2((1, 0), (0, 1), 0.5, 0.5)
        {'price_ratio': 1.0, 'allocation_a': (0.5, 0.5), 'allocation_b': (0.5, 0.5)}
        # 各持有一种商品，均等偏好，均衡时各半分

        # 非对称偏好
        >>> walrasian_equilibrium_2x2((1, 0), (0, 1), 0.75, 0.25)
        {'price_ratio': 1.0, 'allocation_a': (0.75, 0.25), 'allocation_b': (0.25, 0.75)}
        # A更爱X，B更爱Y，通过交换各取所需

    注意:
        - 标准化 px=1，价格比即 py 的值
        - 瓦尔拉斯法则保证Y市场也出清
    """
    # TODO: 求解均衡
    # 步骤：
    # 1. 计算总禀赋
    # 2. 解出均衡价格比 p*
    # 3. 计算各消费者的均衡需求
    # 4. 返回结果字典
    pass


def is_pareto_efficient(
    allocation_a: tuple[float, float],
    allocation_b: tuple[float, float],
    alpha_a: float,
    alpha_b: float
) -> bool:
    """
    检验配置是否帕累托有效。

    【帕累托有效条件】
    在纯交换经济中，帕累托有效要求：
    MRS_A = MRS_B（两人的边际替代率相等）

    【直觉解释】
    如果 MRS_A ≠ MRS_B，说明存在帕累托改进的交易空间。
    例如：如果 MRS_A > MRS_B，A愿意用更多Y换X，B愿意用更多X换Y
    双方可以通过交易共同获益。

    当 MRS_A = MRS_B 时，无法再通过交易使双方都获益。

    【柯布-道格拉斯的MRS】
    对于 U = x^α × y^(1-α)：
    MRS = MUx/MUy = (α/(1-α)) × (y/x)

    帕累托有效条件：
    (αa/(1-αa)) × (ya/xa) = (αb/(1-αb)) × (yb/xb)

    参数:
        allocation_a: A的配置 (xa, ya)
        allocation_b: B的配置 (xb, yb)
        alpha_a: A的效用参数
        alpha_b: B的效用参数

    返回:
        True 如果配置是帕累托有效的，False 否则

    示例:
        # 瓦尔拉斯均衡配置是帕累托有效的（第一福利定理）
        >>> is_pareto_efficient((0.5, 0.5), (0.5, 0.5), 0.5, 0.5)
        True

        # 初始禀赋通常不是帕累托有效的
        >>> is_pareto_efficient((1, 0), (0, 1), 0.5, 0.5)
        False  # MRS_A = inf, MRS_B = 0

    注意:
        - 使用数值比较时需要容忍误差
        - 边界情况（x=0或y=0）需要特殊处理
    """
    # TODO: 检验帕累托效率
    # 步骤：
    # 1. 计算 MRS_A = (alpha_a/(1-alpha_a)) × (ya/xa)
    # 2. 计算 MRS_B = (alpha_b/(1-alpha_b)) × (yb/xb)
    # 3. 比较是否相等（允许数值误差）
    pass


def marginal_rate_of_substitution_cd(
    x: float,
    y: float,
    alpha: float
) -> float:
    """
    计算柯布-道格拉斯效用的边际替代率。

    【MRS定义】
    边际替代率（Marginal Rate of Substitution）是无差异曲线的斜率（绝对值），
    表示保持效用不变时，愿意用多少Y换取1单位X。

    MRS = - dy/dx |_{U=const} = MUx / MUy

    【推导】
    对于 U = x^α × y^(1-α)：

    MUx = ∂U/∂x = α × x^(α-1) × y^(1-α)
    MUy = ∂U/∂y = (1-α) × x^α × y^(-α)

    MRS = MUx / MUy
        = [α × x^(α-1) × y^(1-α)] / [(1-α) × x^α × y^(-α)]
        = [α / (1-α)] × [y / x]

    【经济学含义】
    - MRS随x增加而减少（边际替代率递减）
    - MRS随y增加而增加
    - α越大，MRS越大（越愿意用Y换X）

    参数:
        x: X的消费量（必须 > 0）
        y: Y的消费量（必须 > 0）
        alpha: 效用函数参数 α∈(0,1)

    返回:
        边际替代率 MRS = (α/(1-α)) × (y/x)

    示例:
        # 均等偏好，均等消费
        >>> marginal_rate_of_substitution_cd(1, 1, 0.5)
        1.0  # MRS = 1，愿意1:1交换

        # x多y少
        >>> marginal_rate_of_substitution_cd(2, 1, 0.5)
        0.5  # MRS < 1，X相对充足，不太愿意用Y换X

        # x少y多
        >>> marginal_rate_of_substitution_cd(1, 2, 0.5)
        2.0  # MRS > 1，X相对稀缺，愿意用更多Y换X

    注意:
        - x=0或y=0时，MRS为无穷大或零
        - MRS是正数（取绝对值）
    """
    # TODO: 计算MRS
    # 提示：MRS = (alpha / (1-alpha)) × (y / x)
    pass


def contract_curve_point(
    total_x: float,
    total_y: float,
    alpha_a: float,
    alpha_b: float,
    x_a: float
) -> float:
    """
    给定A的x消费量，计算契约曲线上A的y消费量。

    【契约曲线定义】
    契约曲线（Contract Curve）是埃奇沃斯框图中所有帕累托有效配置的集合。

    【帕累托有效条件】
    MRS_A = MRS_B

    设 A 的配置为 (xa, ya)，B 的配置为 (Ωx-xa, Ωy-ya)

    MRS_A = (αa/(1-αa)) × (ya/xa)
    MRS_B = (αb/(1-αb)) × ((Ωy-ya)/(Ωx-xa))

    令 MRS_A = MRS_B 并解出 ya：

    (αa/(1-αa)) × (ya/xa) = (αb/(1-αb)) × ((Ωy-ya)/(Ωx-xa))

    设 ka = αa/(1-αa)，kb = αb/(1-αb)

    ka × ya × (Ωx-xa) = kb × xa × (Ωy-ya)
    ka × ya × (Ωx-xa) + kb × xa × ya = kb × xa × Ωy
    ya × [ka(Ωx-xa) + kb×xa] = kb × xa × Ωy

    ya = kb × xa × Ωy / [ka(Ωx-xa) + kb×xa]

    参数:
        total_x: 总禀赋 Ωx
        total_y: 总禀赋 Ωy
        alpha_a: A的效用参数 αa
        alpha_b: B的效用参数 αb
        x_a: A的x消费量 xa

    返回:
        契约曲线上对应的 ya

    示例:
        # 对称情况，契约曲线是对角线
        >>> contract_curve_point(2, 2, 0.5, 0.5, 1)
        1.0  # 中点在对角线上

        >>> contract_curve_point(2, 2, 0.5, 0.5, 0.5)
        0.5  # 另一点

        # 非对称情况
        >>> contract_curve_point(2, 2, 0.75, 0.25, 1)
        0.5  # 契约曲线不是对角线

    注意:
        - 契约曲线从A的原点(0,0)延伸到B的原点(Ωx,Ωy)
        - xa应在[0, Ωx]范围内
    """
    # TODO: 计算契约曲线点
    # 步骤：
    # 1. 计算 ka = alpha_a / (1-alpha_a)
    # 2. 计算 kb = alpha_b / (1-alpha_b)
    # 3. 应用公式 ya = kb × xa × Ωy / [ka(Ωx-xa) + kb×xa]
    pass


def excess_demand(
    price_ratio: float,
    endowment_a: tuple[float, float],
    endowment_b: tuple[float, float],
    alpha_a: float,
    alpha_b: float
) -> float:
    """
    计算商品X的超额需求。

    【超额需求定义】
    超额需求 = 总需求 - 总供给
    ED_X(p) = x_a(p) + x_b(p) - (ωax + ωbx)

    【性质】
    - ED(p*) = 0 当且仅当 p* 是均衡价格
    - 瓦尔拉斯法则：p×ED_X + ED_Y = 0
    - 因此 ED_Y(p*) = 0 自动满足

    【计算步骤】
    令 px = 1，py = price_ratio = p

    A的收入：mₐ = ωax + p×ωay
    A对X的需求：xₐ = αa×mₐ = αa×(ωax + p×ωay)

    B的收入：mb = ωbx + p×ωby
    B对X的需求：xb = αb×mb = αb×(ωbx + p×ωby)

    超额需求：
    ED_X = xₐ + xb - (ωax + ωbx)
         = αa×(ωax + p×ωay) + αb×(ωbx + p×ωby) - ωax - ωbx

    参数:
        price_ratio: 价格比 py/px（标准化 px=1）
        endowment_a: A的初始禀赋 (ωax, ωay)
        endowment_b: B的初始禀赋 (ωbx, ωby)
        alpha_a: A的效用参数
        alpha_b: B的效用参数

    返回:
        商品X的超额需求（正为超额需求，负为超额供给）

    示例:
        # 均衡价格下超额需求为0
        >>> excess_demand(1.0, (1, 0), (0, 1), 0.5, 0.5)
        0.0  # p=1是均衡价格

        # 价格过低，需求过大
        >>> excess_demand(0.5, (1, 0), (0, 1), 0.5, 0.5)
        0.25  # 超额需求 > 0

        # 价格过高，需求不足
        >>> excess_demand(2.0, (1, 0), (0, 1), 0.5, 0.5)
        -0.167  # 超额需求 < 0（超额供给）

    注意:
        - 可以用数值方法（如二分法）找到使 ED=0 的价格
        - 超额需求函数通常是价格的递减函数
    """
    # TODO: 计算超额需求
    # 步骤：
    # 1. 计算A的收入和X需求
    # 2. 计算B的收入和X需求
    # 3. 计算总需求 - 总供给
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
