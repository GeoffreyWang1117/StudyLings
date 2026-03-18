"""
混沌动力学 Chaos Dynamics
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解混沌系统的基本特征（确定性但不可预测）
  Understand basic characteristics of chaotic systems (deterministic but unpredictable)
- 掌握Lorenz系统的数值模拟和奇异吸引子
  Master numerical simulation of Lorenz system and strange attractors
- 计算李雅普诺夫指数作为混沌的定量判据
  Calculate Lyapunov exponent as quantitative measure of chaos
- 分析分岔现象和通往混沌的道路
  Analyze bifurcation phenomena and routes to chaos

================================================================================
物理背景 Physical Background
================================================================================
混沌是确定性系统中出现的复杂非周期行为。

1. 混沌的三个特征 Three Characteristics of Chaos:
   - 对初始条件的敏感依赖性（蝴蝶效应）
   - 长期行为不可预测
   - 轨道局限于有限区域（有界性）

2. Lorenz系统 Lorenz System:
   描述大气对流的简化模型：
   dx/dt = σ(y - x)        [热耗散]
   dy/dt = x(ρ - z) - y    [对流]
   dz/dt = xy - βz         [温度梯度]
   经典参数: σ = 10, ρ = 28, β = 8/3

3. 李雅普诺夫指数 Lyapunov Exponent:
   衡量相空间中相邻轨迹分离的速率
   δ(t) ~ δ₀·exp(λt)
   - λ > 0: 混沌（轨迹指数分离）
   - λ = 0: 周期运动或临界态
   - λ < 0: 吸引子（轨迹收敛）

4. 奇异吸引子 Strange Attractor:
   - 分形维数（非整数维）
   - 所有轨迹最终被吸引到此结构上
   - 具有自相似性

5. 分岔 Bifurcation:
   - 参数变化导致定性行为改变
   - 倍周期分岔是通往混沌的典型路径
   - 费根鲍姆常数: δ ≈ 4.669...

6. 庞加莱截面 Poincare Section:
   - 将连续动力学离散化
   - 揭示隐藏的周期性或混沌结构

HINT: 混沌系统对初始条件敏感（蝴蝶效应）
HINT: Lorenz方程: dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz
HINT: 李雅普诺夫指数 λ > 0 表示混沌
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 11.1: Lorenz系统
# Exercise 11.1: Lorenz System
# =============================================================================
# Lorenz系统是1963年Edward Lorenz在研究大气对流时发现的
# 这是第一个被发现的混沌系统，开启了混沌理论的研究

# Lorenz方程参数的物理意义
SIGMA = 10.0  # Prandtl数: 动量扩散与热扩散之比
RHO = 28.0    # Rayleigh数: 浮力与粘性力之比（控制对流强度）
BETA = 8.0/3  # 几何因子: 与对流单元的几何形状有关

def lorenz_derivatives(state, t, sigma=SIGMA, rho=RHO, beta=BETA):
    """
    Lorenz系统的微分方程 Lorenz System ODEs

    方程组的物理意义：
    dx/dt = σ(y - x)        流体速度与温度差的耦合
    dy/dt = x(ρ - z) - y    温度场的演化
    dz/dt = xy - βz         垂直温度梯度的变化

    参数 Parameters:
        state: [x, y, z] 系统状态
        t: 时间（方程本身与时间无关）
        sigma, rho, beta: Lorenz参数
    返回 Returns:
        [dx/dt, dy/dt, dz/dt]: 状态导数
    """
    x, y, z = state
    # TODO: 计算Lorenz方程的导数
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]


def simulate_lorenz(initial_state, t_span, dt=0.01, sigma=SIGMA, rho=RHO, beta=BETA):
    """
    模拟Lorenz系统 Simulate Lorenz System

    使用odeint数值积分求解Lorenz方程
    对于混沌系统，时间步长dt需要足够小以保持精度
    """
    t = np.arange(t_span[0], t_span[1], dt)
    solution = odeint(lorenz_derivatives, initial_state, t, args=(sigma, rho, beta))
    return t, solution


# =============================================================================
# 练习 11.2: 敏感依赖性（蝴蝶效应）
# Exercise 11.2: Sensitive Dependence on Initial Conditions
# =============================================================================
# "蝴蝶效应"是混沌系统最著名的特征
# 两个初始条件极其接近的轨迹会随时间指数级分离
# 这使得长期天气预报在原理上不可能精确

def butterfly_effect(state1, state2, t_span, dt=0.01):
    """
    演示蝴蝶效应 Demonstrate Butterfly Effect

    追踪两条初始条件略有不同的轨迹
    观察它们之间的距离如何随时间增长

    参数 Parameters:
        state1: 第一条轨迹的初始状态 [x, y, z]
        state2: 第二条轨迹的初始状态（与state1略有不同）
        t_span: 时间范围 [t_start, t_end]
        dt: 时间步长
    返回 Returns:
        t: 时间数组
        sol1, sol2: 两条轨迹
        distance: 轨迹间距离随时间的变化
    """
    t, sol1 = simulate_lorenz(state1, t_span, dt)
    _, sol2 = simulate_lorenz(state2, t_span, dt)

    # TODO: 计算两条轨迹之间的欧氏距离随时间的变化
    distance = np.sqrt(np.sum((sol1 - sol2)**2, axis=1))
    return t, sol1, sol2, distance


def divergence_rate(distance, t, t_start=5):
    """
    计算轨迹分离的指数增长率 Calculate Divergence Rate

    对于混沌系统: distance(t) ~ d₀·exp(λt)
    取对数: ln(d) = ln(d₀) + λt
    斜率λ即为李雅普诺夫指数的近似值

    参数 Parameters:
        distance: 轨迹间距离数组
        t: 时间数组
        t_start: 开始拟合的时间（跳过初始瞬态）
    返回 Returns:
        lambda_approx: 近似李雅普诺夫指数（正值表示混沌）
    """
    # 只取初始阶段（指数增长区域，饱和前）
    mask = (t >= t_start) & (t <= t_start + 10)
    t_fit = t[mask]
    d_fit = distance[mask]

    # TODO: 线性拟合 ln(d) vs t，斜率即为李雅普诺夫指数
    log_d = np.log(d_fit + 1e-10)  # 避免log(0)
    coeffs = np.polyfit(t_fit, log_d, 1)
    lambda_approx = coeffs[0]  # 斜率即为李雅普诺夫指数
    return lambda_approx


# =============================================================================
# 练习 11.3: 李雅普诺夫指数
# Exercise 11.3: Lyapunov Exponent
# =============================================================================
# 李雅普诺夫指数是混沌的定量判据
# 它度量相空间中相邻轨迹分离的平均速率
# Lorenz系统的最大李雅普诺夫指数约为 λ ≈ 0.9

def lyapunov_exponent_lorenz(initial_state, t_end=100, dt=0.01, delta=1e-8):
    """
    计算Lorenz系统的最大李雅普诺夫指数 Calculate Maximum Lyapunov Exponent

    使用重正化方法（Benettin算法）：
    1. 维护两条轨迹：主轨迹和扰动轨迹
    2. 周期性地测量分离并重新正规化
    3. 平均增长率即为李雅普诺夫指数

    λ = lim(t→∞) (1/t) Σ ln(d_i/δ)

    参数 Parameters:
        initial_state: 初始状态 [x, y, z]
        t_end: 总演化时间
        dt: 时间步长
        delta: 初始扰动大小
    返回 Returns:
        lambda_max: 最大李雅普诺夫指数 [1/s]
        （Lorenz系统典型值约为0.9）
    """
    state = np.array(initial_state, dtype=float)
    perturbed = state + np.array([delta, 0, 0])

    lyap_sum = 0
    n_steps = int(t_end / dt)
    renorm_interval = 10  # 每10步重正化一次
    n_renorm = 0

    for i in range(n_steps):
        # 同时演化主轨迹和扰动轨迹
        t_step = np.array([0, dt])
        state = odeint(lorenz_derivatives, state, t_step)[-1]
        perturbed = odeint(lorenz_derivatives, perturbed, t_step)[-1]

        if (i + 1) % renorm_interval == 0:
            # TODO: 计算分离距离并累加对数
            separation = perturbed - state
            distance = np.linalg.norm(separation)

            if distance > 0:
                lyap_sum += np.log(distance / delta)
                n_renorm += 1

                # 重正化：将扰动轨迹拉回到原轨迹附近（保持方向）
                perturbed = state + delta * separation / distance

    # TODO: 计算平均李雅普诺夫指数（除以总时间）
    lambda_max = lyap_sum / (n_renorm * renorm_interval * dt) if n_renorm > 0 else 0
    return lambda_max


# =============================================================================
# 练习 11.4: 分岔图
# Exercise 11.4: Bifurcation Diagram
# =============================================================================
def bifurcation_lorenz(rho_range, n_samples=100, t_transient=100, t_sample=50):
    """
    绘制Lorenz系统关于参数rho的分岔图
    """
    rho_values = []
    z_values = []

    for rho in rho_range:
        # 初始演化（跳过瞬态）
        t, sol = simulate_lorenz([1, 1, 1], (0, t_transient), sigma=SIGMA, rho=rho, beta=BETA)
        initial_state = sol[-1]

        # 采样
        t, sol = simulate_lorenz(initial_state, (0, t_sample), sigma=SIGMA, rho=rho, beta=BETA)

        # TODO: 记录局部极大值作为分岔图的点
        z = sol[:, 2]
        # 找局部极大值
        for i in range(1, len(z) - 1):
            if z[i] > z[i-1] and z[i] > z[i+1]:
                rho_values.append(rho)
                z_values.append(z[i])

    return np.array(rho_values), np.array(z_values)


# =============================================================================
# 练习 11.5: 逻辑斯蒂映射（Logistic Map）
# Exercise 11.5: Logistic Map
# =============================================================================
# 逻辑斯蒂映射是最简单的混沌系统之一
# 它是一个离散动力系统，展示了通往混沌的倍周期分岔路径
# 原为种群动力学模型: x表示种群占最大容量的比例

def logistic_map(x, r):
    """
    逻辑斯蒂映射 Logistic Map
    x_{n+1} = r·x_n·(1 - x_n)

    物理意义（种群模型）：
    - x_n: 第n代种群（归一化到0-1）
    - r: 增长率参数
    - (1-x): 环境承载能力的制约

    参数r的影响：
    - r < 1: 种群灭绝
    - 1 < r < 3: 稳定到固定点
    - 3 < r < 3.57: 周期性振荡（倍周期分岔）
    - r ≈ 3.57: 混沌开始
    - r = 4: 完全混沌
    """
    # TODO: 计算映射后的值
    return r * x * (1 - x)


def iterate_logistic(x0, r, n_iterations):
    """
    迭代逻辑斯蒂映射 Iterate Logistic Map

    从初始值x0开始，迭代n次
    返回完整的迭代序列
    """
    x = np.zeros(n_iterations + 1)
    x[0] = x0
    for i in range(n_iterations):
        x[i + 1] = logistic_map(x[i], r)
    return x


def bifurcation_logistic(r_range, x0=0.5, n_transient=200, n_sample=100):
    """
    逻辑斯蒂映射的分岔图 Bifurcation Diagram

    分岔图展示系统的长期行为如何随参数r变化：
    - 单点: 稳定到固定点
    - 2点: 周期2振荡
    - 4,8,16...点: 倍周期分岔
    - 连续带: 混沌区域
    - 白条: 周期窗口

    参数 Parameters:
        r_range: 参数r的取值范围
        x0: 初始值
        n_transient: 瞬态时间（跳过初始的非稳态行为）
        n_sample: 采样点数
    """
    r_values = []
    x_values = []

    for r in r_range:
        # 跳过瞬态，只记录稳态行为
        x = iterate_logistic(x0, r, n_transient + n_sample)

        # TODO: 记录跳过瞬态后的所有值
        for val in x[n_transient:]:
            r_values.append(r)
            x_values.append(val)

    return np.array(r_values), np.array(x_values)


def lyapunov_logistic(r, x0=0.5, n_iterations=1000):
    """
    计算逻辑斯蒂映射的李雅普诺夫指数 Lyapunov Exponent for Logistic Map

    对于一维映射: λ = lim (1/n) Σ ln|f'(x_i)|
    逻辑斯蒂映射的导数: f'(x) = r(1 - 2x)

    λ > 0: 混沌
    λ < 0: 周期吸引子
    λ = 0: 分岔点

    参数 Parameters:
        r: 映射参数
        x0: 初始值
        n_iterations: 迭代次数
    返回 Returns:
        李雅普诺夫指数
    """
    x = x0
    lyap_sum = 0

    for _ in range(n_iterations):
        # TODO: 累加ln|f'(x)|
        derivative = abs(r * (1 - 2 * x))
        if derivative > 0:
            lyap_sum += np.log(derivative)
        x = logistic_map(x, r)

    return lyap_sum / n_iterations


# =============================================================================
# 练习 11.6: 奇异吸引子
# Exercise 11.6: Strange Attractor
# =============================================================================
# Rossler系统是另一个经典的混沌系统
# 它的吸引子结构比Lorenz系统更简单，更易于分析
# 展示了简单的"折叠和拉伸"机制如何产生混沌

def rossler_derivatives(state, t, a=0.2, b=0.2, c=5.7):
    """
    Rossler系统方程 Rossler System Equations
    dx/dt = -y - z
    dy/dt = x + ay
    dz/dt = b + z(x - c)

    特点：
    - 只有一个非线性项 zx
    - 在xy平面形成近圆形轨道
    - z方向的"尖峰"产生混沌行为

    参数a, b, c控制系统行为：
    - 典型混沌参数: a=0.2, b=0.2, c=5.7
    """
    x, y, z = state
    # TODO: 计算Rossler方程的导数
    dx_dt = -y - z
    dy_dt = x + a * y
    dz_dt = b + z * (x - c)
    return [dx_dt, dy_dt, dz_dt]


def simulate_rossler(initial_state, t_span, dt=0.01, a=0.2, b=0.2, c=5.7):
    """
    模拟Rossler系统 Simulate Rossler System

    Rossler吸引子在xy平面呈现扁平的螺旋结构
    z方向的脉冲产生"混合"效应
    """
    t = np.arange(t_span[0], t_span[1], dt)
    solution = odeint(rossler_derivatives, initial_state, t, args=(a, b, c))
    return t, solution


# =============================================================================
# 练习 11.7: 庞加莱截面
# Exercise 11.7: Poincare Section
# =============================================================================
# 庞加莱截面是研究动力系统的重要工具
# 它将连续流化为离散映射，降低系统维度
# 周期轨道在截面上表现为有限点集，混沌则表现为分形结构

def poincare_section(trajectory, plane_coord=2, plane_value=None, direction='positive'):
    """
    计算庞加莱截面 Calculate Poincare Section

    原理：选择一个超平面（如z=常数），
    记录轨迹每次穿越该平面时的位置

    参数 Parameters:
        trajectory: (N, 3) 轨迹数组
        plane_coord: 截面法向坐标轴 (0=x, 1=y, 2=z)
        plane_value: 截面位置，默认为该坐标的平均值
        direction: 穿越方向 'positive'(从小到大) 或 'negative'
    返回 Returns:
        截面上的点集 (M, 3) 数组

    应用：
    - 周期轨道: 有限点集
    - 准周期轨道: 封闭曲线
    - 混沌轨道: 分形点集
    """
    if plane_value is None:
        plane_value = np.mean(trajectory[:, plane_coord])

    points = []
    coord = trajectory[:, plane_coord]

    # TODO: 找到轨迹穿越截面的所有点
    for i in range(1, len(coord)):
        if direction == 'positive':
            # 从负到正穿越（沿正方向穿过）
            if coord[i-1] < plane_value and coord[i] >= plane_value:
                # 线性插值找到精确穿越点
                alpha = (plane_value - coord[i-1]) / (coord[i] - coord[i-1])
                point = trajectory[i-1] + alpha * (trajectory[i] - trajectory[i-1])
                points.append(point)
        else:
            # 从正到负穿越（沿负方向穿过）
            if coord[i-1] > plane_value and coord[i] <= plane_value:
                alpha = (plane_value - coord[i-1]) / (coord[i] - coord[i-1])
                point = trajectory[i-1] + alpha * (trajectory[i] - trajectory[i-1])
                points.append(point)

    return np.array(points) if points else np.array([]).reshape(0, 3)


# =============================================================================
# 可视化
# =============================================================================
def plot_chaos():
    fig = plt.figure(figsize=(16, 12))

    # 1. Lorenz吸引子
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    t, sol = simulate_lorenz([1, 1, 1], (0, 50), dt=0.01)
    ax1.plot(sol[:, 0], sol[:, 1], sol[:, 2], 'b-', linewidth=0.5, alpha=0.8)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax1.set_title('Lorenz吸引子 Lorenz Attractor')

    # 2. 蝴蝶效应
    ax2 = fig.add_subplot(2, 3, 2)
    state1 = [1, 1, 1]
    state2 = [1.001, 1, 1]  # 微小差异
    t, sol1, sol2, distance = butterfly_effect(state1, state2, (0, 30))
    ax2.semilogy(t, distance, 'r-', linewidth=1)
    ax2.set_xlabel('t')
    ax2.set_ylabel('Distance (log scale)')
    ax2.set_title('蝴蝶效应 Butterfly Effect')
    ax2.grid(True, alpha=0.3)

    # 3. 逻辑斯蒂映射分岔图
    ax3 = fig.add_subplot(2, 3, 3)
    r_range = np.linspace(2.5, 4.0, 500)
    r_vals, x_vals = bifurcation_logistic(r_range, n_transient=300, n_sample=100)
    ax3.plot(r_vals, x_vals, 'k,', markersize=0.5)
    ax3.set_xlabel('r')
    ax3.set_ylabel('x')
    ax3.set_title('逻辑斯蒂映射分岔图')
    ax3.set_xlim(2.5, 4.0)

    # 4. 李雅普诺夫指数
    ax4 = fig.add_subplot(2, 3, 4)
    r_range_lyap = np.linspace(2.5, 4.0, 200)
    lyap = [lyapunov_logistic(r) for r in r_range_lyap]
    ax4.plot(r_range_lyap, lyap, 'b-', linewidth=1)
    ax4.axhline(y=0, color='r', linestyle='--')
    ax4.set_xlabel('r')
    ax4.set_ylabel('Lyapunov Exponent')
    ax4.set_title('逻辑斯蒂映射李雅普诺夫指数')
    ax4.grid(True, alpha=0.3)

    # 5. Rossler吸引子
    ax5 = fig.add_subplot(2, 3, 5, projection='3d')
    t, sol = simulate_rossler([1, 1, 1], (0, 200), dt=0.01)
    ax5.plot(sol[:, 0], sol[:, 1], sol[:, 2], 'g-', linewidth=0.3, alpha=0.7)
    ax5.set_xlabel('x')
    ax5.set_ylabel('y')
    ax5.set_zlabel('z')
    ax5.set_title('Rossler吸引子 Rossler Attractor')

    # 6. 庞加莱截面
    ax6 = fig.add_subplot(2, 3, 6)
    poincare = poincare_section(sol, plane_coord=2, plane_value=1.0)
    if len(poincare) > 0:
        ax6.plot(poincare[:, 0], poincare[:, 1], 'b.', markersize=1)
    ax6.set_xlabel('x')
    ax6.set_ylabel('y')
    ax6.set_title('庞加莱截面 (z=1)')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('chaos_dynamics.png', dpi=150)
    print("图像已保存为 chaos_dynamics.png")
    plt.show()


def verify():
    all_passed = True

    # Check 11.1 - Lorenz系统
    t, sol = simulate_lorenz([1, 1, 1], (0, 10))
    if sol.shape[0] < 100:
        print("❌ 11.1 Lorenz系统模拟失败")
        all_passed = False
    else:
        print("✓ 11.1 Lorenz系统模拟正确")

    # Check 11.2 - 蝴蝶效应
    state1, state2 = [1, 1, 1], [1.001, 1, 1]
    t, sol1, sol2, distance = butterfly_effect(state1, state2, (0, 20))
    if distance[-1] < 1:  # 轨迹应该显著分离
        print("❌ 11.2 蝴蝶效应计算错误")
        all_passed = False
    else:
        print(f"✓ 11.2 蝴蝶效应正确 (最终距离: {distance[-1]:.2f})")

    # Check 11.3 - 李雅普诺夫指数
    lambda_max = lyapunov_exponent_lorenz([1, 1, 1], t_end=50)
    # Lorenz系统的最大李雅普诺夫指数约为0.9
    if lambda_max < 0.5 or lambda_max > 1.5:
        print(f"❌ 11.3 李雅普诺夫指数计算可能有误 (λ = {lambda_max:.3f})")
        all_passed = False
    else:
        print(f"✓ 11.3 李雅普诺夫指数正确 (λ_max ≈ {lambda_max:.3f})")

    # Check 11.5 - 逻辑斯蒂映射
    x = iterate_logistic(0.5, 3.5, 100)
    if not (0 < x[-1] < 1):
        print("❌ 11.5 逻辑斯蒂映射错误")
        all_passed = False
    else:
        print("✓ 11.5 逻辑斯蒂映射正确")

    # Check Lyapunov for logistic map at r=4 (should be positive)
    lyap_4 = lyapunov_logistic(4.0)
    if lyap_4 < 0:
        print("❌ 11.5 逻辑斯蒂映射李雅普诺夫指数错误")
        all_passed = False
    else:
        print(f"✓ 11.5 逻辑斯蒂映射李雅普诺夫指数正确 (r=4: λ = {lyap_4:.3f})")

    # Check 11.6 - Rossler系统
    t, sol = simulate_rossler([1, 1, 1], (0, 50))
    if sol.shape[0] < 100:
        print("❌ 11.6 Rossler系统模拟失败")
        all_passed = False
    else:
        print("✓ 11.6 Rossler系统模拟正确")

    # Check 11.7 - 庞加莱截面
    t, sol = simulate_rossler([1, 1, 1], (0, 200))
    poincare = poincare_section(sol, plane_coord=2, plane_value=1.0)
    if len(poincare) < 10:
        print("❌ 11.7 庞加莱截面计算错误")
        all_passed = False
    else:
        print(f"✓ 11.7 庞加莱截面正确 ({len(poincare)}个穿越点)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_chaos()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("混沌动力学 Chaos Dynamics")
    print("=" * 50)
    verify()
