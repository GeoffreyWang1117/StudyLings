# EXERCISE: comparative_advantage1
# DIFFICULTY: ★★☆☆☆
# TOPIC: 比较优势理论
#
# 说明：
# 比较优势是国际贸易理论的基石，由大卫·李嘉图于1817年提出。
#
# 【核心思想】
# 即使一国在所有商品生产上都处于绝对劣势，仍然可以通过专业化生产
# 其相对效率较高（机会成本较低）的商品并进行贸易来获益。
#
# 【李嘉图模型假设】
# - 两个国家（本国与外国）
# - 两种商品（X和Y）
# - 一种生产要素（劳动）
# - 劳动在国内完全流动，国际间不流动
# - 规模报酬不变
# - 完全竞争市场
#
# 【关键概念】
# 1. 绝对优势：生产某商品所需劳动更少
# 2. 比较优势：生产某商品的机会成本更低
# 3. 机会成本：生产一单位X需要放弃的Y产量
#    OC_X = L_X / L_Y（单位X的劳动需求 / 单位Y的劳动需求）
#
# 【贸易利得来源】
# - 专业化提高生产效率
# - 扩大消费可能性边界
# - 贸易后消费点可在生产可能性边界之外
#
# 【数学推导】
# 设本国生产X需要a_LX单位劳动，生产Y需要a_LY单位劳动
# 本国X的机会成本：a_LX / a_LY
# 外国X的机会成本：a*_LX / a*_LY
# 若 a_LX/a_LY < a*_LX/a*_LY，则本国在X上有比较优势
#
# 任务：
# 1. 计算机会成本
# 2. 确定比较优势
# 3. 计算贸易利得
#
# HINT1: 机会成本 = 该商品的劳动需求 / 另一商品的劳动需求
# HINT2: 比较优势由相对效率决定，而非绝对效率
# HINT3: 贸易价格介于两国机会成本之间

import numpy as np


def opportunity_cost(
    labor_x: float,
    labor_y: float
) -> float:
    """
    计算生产X的机会成本（以Y为单位）。

    机会成本反映资源的替代用途价值。生产一单位X需要放弃多少Y？

    公式推导：
    - 生产1单位X需要 labor_x 单位劳动
    - 这些劳动如果用于生产Y，可生产 labor_x / labor_y 单位Y
    - 因此，X的机会成本 = labor_x / labor_y

    参数:
        labor_x: 生产一单位X所需劳动（如：2小时/单位X）
        labor_y: 生产一单位Y所需劳动（如：1小时/单位Y）

    返回:
        X的机会成本（以Y为单位）

    示例:
        >>> opportunity_cost(2, 1)  # 生产1单位X需放弃2单位Y
        2.0
    """
    # TODO: 计算机会成本
    # 提示：OC_X = L_X / L_Y
    pass


def has_comparative_advantage(
    labor_x_home: float,
    labor_y_home: float,
    labor_x_foreign: float,
    labor_y_foreign: float
) -> str:
    """
    判断本国在哪种商品上具有比较优势。

    比较优势判断规则：
    - 计算本国X的机会成本：OC_X_home = labor_x_home / labor_y_home
    - 计算外国X的机会成本：OC_X_foreign = labor_x_foreign / labor_y_foreign
    - 若 OC_X_home < OC_X_foreign，本国在X上有比较优势
    - 若 OC_X_home > OC_X_foreign，本国在Y上有比较优势
    - 若相等，则无比较优势

    参数:
        labor_x_home: 本国生产一单位X的劳动需求
        labor_y_home: 本国生产一单位Y的劳动需求
        labor_x_foreign: 外国生产一单位X的劳动需求
        labor_y_foreign: 外国生产一单位Y的劳动需求

    返回:
        "X"（本国在X上有比较优势）
        "Y"（本国在Y上有比较优势）
        "none"（无比较优势，机会成本相等）

    示例:
        本国：2小时/X，1小时/Y → OC_X = 2
        外国：6小时/X，2小时/Y → OC_X = 3
        本国X的机会成本更低，在X上有比较优势
    """
    # TODO: 判断比较优势
    # 提示：比较两国X的机会成本
    pass


def autarky_production(
    labor_endowment: float,
    labor_x: float,
    labor_y: float,
    preference_share_x: float = 0.5
) -> tuple[float, float]:
    """
    封闭经济（自给自足）下的生产与消费。

    假设消费者具有Cobb-Douglas效用函数：U = X^α × Y^(1-α)
    在封闭经济中，生产=消费

    预算约束（用劳动表示）：
    labor_x × X + labor_y × Y = labor_endowment

    最优消费满足：
    α × 支出 用于购买X
    (1-α) × 支出 用于购买Y

    参数:
        labor_endowment: 劳动禀赋总量（如：100小时）
        labor_x: 生产一单位X的劳动需求
        labor_y: 生产一单位Y的劳动需求
        preference_share_x: X在效用函数中的份额α（默认0.5）

    返回:
        (X的产量/消费量, Y的产量/消费量)

    示例:
        >>> autarky_production(100, 2, 1, 0.5)
        (25.0, 50.0)  # 50小时生产X得25单位，50小时生产Y得50单位
    """
    # TODO: 封闭经济生产
    # 提示：根据偏好份额分配劳动时间
    pass


def trade_equilibrium_price(
    oc_home: float,
    oc_foreign: float
) -> tuple[float, float]:
    """
    计算贸易均衡价格的范围。

    贸易价格（X相对于Y的价格）必须介于两国机会成本之间，
    否则至少有一国不会参与贸易。

    原理：
    - 若价格 < min(OC_home, OC_foreign)：两国都不生产X
    - 若价格 > max(OC_home, OC_foreign)：两国都生产X
    - 只有价格在两者之间，才有专业化和贸易

    参数:
        oc_home: 本国X的机会成本
        oc_foreign: 外国X的机会成本

    返回:
        (价格下界, 价格上界)
        价格p满足：下界 < p < 上界

    示例:
        >>> trade_equilibrium_price(2, 3)
        (2, 3)  # 贸易价格在2到3之间
    """
    # TODO: 均衡价格范围
    # 提示：取两个机会成本的最小值和最大值
    pass


def specialization_pattern(
    oc_home: float,
    oc_foreign: float
) -> tuple[str, str]:
    """
    确定两国的专业化模式。

    专业化原则：每个国家应专业化生产其具有比较优势的商品
    - 机会成本低的国家专业化生产该商品
    - 机会成本高的国家专业化生产另一商品

    参数:
        oc_home: 本国X的机会成本
        oc_foreign: 外国X的机会成本

    返回:
        (本国专业化商品, 外国专业化商品)

    示例:
        >>> specialization_pattern(2, 3)
        ("X", "Y")  # 本国专业化X（机会成本低），外国专业化Y
    """
    # TODO: 专业化模式
    # 提示：机会成本低者生产X
    pass


def gains_from_trade(
    autarky_utility: float,
    trade_utility: float
) -> float:
    """
    计算贸易利得（效用增加的百分比）。

    贸易利得是指相对于自给自足状态，参与国际贸易后
    福利水平的提高程度。

    参数:
        autarky_utility: 封闭经济时的效用水平
        trade_utility: 贸易后的效用水平

    返回:
        贸易利得百分比：(U_trade - U_autarky) / U_autarky × 100

    示例:
        >>> gains_from_trade(100, 120)
        20.0  # 效用提高了20%
    """
    # TODO: 贸易利得
    # 提示：计算百分比变化
    pass


def production_possibility_frontier(
    labor_endowment: float,
    labor_x: float,
    labor_y: float,
    x_values: np.ndarray
) -> np.ndarray:
    """
    计算生产可能性边界（PPF）。

    PPF表示在给定资源约束下，所有可能的产出组合。

    约束条件：L_X × X + L_Y × Y ≤ L（总劳动）
    在PPF上：L_X × X + L_Y × Y = L

    解得：Y = (L - L_X × X) / L_Y

    PPF的斜率 = -L_X / L_Y = -机会成本
    PPF是一条直线（因为规模报酬不变）

    参数:
        labor_endowment: 劳动禀赋总量
        labor_x: 生产一单位X的劳动需求
        labor_y: 生产一单位Y的劳动需求
        x_values: X产量的数组（用于计算对应的Y值）

    返回:
        对应的Y产量数组

    注意:
        - 若计算得Y<0，说明该X产量不可行
        - X的最大产量 = labor_endowment / labor_x
    """
    # TODO: 计算PPF
    # 提示：Y = (L - L_X × X) / L_Y
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
