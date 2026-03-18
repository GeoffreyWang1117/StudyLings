# EXERCISE: indifference1
# DIFFICULTY: ★★★☆☆
# TOPIC: 无差异曲线
#
# 说明：
# 无差异曲线 (Indifference Curve) 是给消费者带来相同效用水平的所有商品组合的轨迹。
#
# 对于柯布-道格拉斯效用 U(x,y) = x^α * y^β：
# 给定效用水平 U̅，无差异曲线方程为：
# y = (U̅ / x^α)^(1/β)
#
# 无差异曲线的性质：
# 1. 向右下方倾斜（负斜率）
# 2. 凸向原点
# 3. 不相交
# 4. 离原点越远效用越高
#
# 任务：
# 1. 给定效用水平，计算无差异曲线上的点
# 2. 验证无差异曲线的凸性
# 3. 计算无差异曲线的斜率
#
# HINT1: 无差异曲线斜率 = -MRS
# HINT2: 凸向原点意味着斜率的绝对值随x增加而减小

import numpy as np


def indifference_curve_y(x: float, utility: float, alpha: float, beta: float) -> float:
    """
    给定x，计算无差异曲线上对应的y值。

    对于 U(x,y) = x^α * y^β = U̅
    y = (U̅ / x^α)^(1/β)

    参数:
        x: 商品X的数量
        utility: 目标效用水平 U̅
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        商品Y的数量
    """
    # TODO: 计算无差异曲线上的y值
    pass


def indifference_curve_slope(x: float, y: float, alpha: float, beta: float) -> float:
    """
    计算无差异曲线在点(x,y)处的斜率。

    斜率 = dy/dx = -MRS = -(α/β) * (y/x)

    参数:
        x: 商品X的数量
        y: 商品Y的数量
        alpha: 商品X的指数
        beta: 商品Y的指数

    返回:
        无差异曲线的斜率（负值）
    """
    # TODO: 计算无差异曲线斜率
    pass


def is_convex_to_origin(x_values: list[float], y_values: list[float]) -> bool:
    """
    检验无差异曲线是否凸向原点。

    凸向原点：随着x增加，斜率的绝对值减小（斜率从负变得更接近0）

    参数:
        x_values: x坐标序列（递增）
        y_values: 对应的y坐标序列

    返回:
        如果凸向原点返回 True
    """
    # TODO: 检验凸向原点
    # 提示：计算相邻点之间的斜率，检验斜率是否递增（从大负数到小负数）
    pass


def generate_indifference_curve(
    utility: float,
    alpha: float,
    beta: float,
    x_min: float,
    x_max: float,
    n_points: int = 50
) -> tuple[np.ndarray, np.ndarray]:
    """
    生成无差异曲线的点。

    参数:
        utility: 效用水平
        alpha, beta: 效用函数参数
        x_min, x_max: x的范围
        n_points: 点的数量

    返回:
        (x数组, y数组)
    """
    # TODO: 生成无差异曲线
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
