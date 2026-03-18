"""
Physics Helper Functions - 物理辅助函数
Common utilities for physics calculations and simulations
"""

import numpy as np
from typing import Tuple, Callable, List, Optional
from .constants import *


# =============================================================================
# Vector Operations 向量运算
# =============================================================================

def magnitude(v: np.ndarray) -> float:
    """Calculate vector magnitude 计算向量模长"""
    return np.linalg.norm(v)


def unit_vector(v: np.ndarray) -> np.ndarray:
    """Return unit vector 返回单位向量"""
    mag = magnitude(v)
    if mag == 0:
        return v
    return v / mag


def angle_between(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculate angle between two vectors (radians) 计算两向量夹角"""
    cos_angle = np.dot(v1, v2) / (magnitude(v1) * magnitude(v2))
    return np.arccos(np.clip(cos_angle, -1, 1))


def cross_2d(v1: np.ndarray, v2: np.ndarray) -> float:
    """2D cross product (returns scalar) 二维叉积"""
    return v1[0] * v2[1] - v1[1] * v2[0]


# =============================================================================
# Numerical Integration 数值积分
# =============================================================================

def euler_step(y: np.ndarray, dydt: Callable, dt: float, t: float) -> np.ndarray:
    """
    Euler method single step 欧拉法单步
    y: current state
    dydt: derivative function dydt(y, t)
    dt: time step
    t: current time
    """
    return y + dt * dydt(y, t)


def rk4_step(y: np.ndarray, dydt: Callable, dt: float, t: float) -> np.ndarray:
    """
    4th order Runge-Kutta single step 四阶龙格库塔单步
    y: current state
    dydt: derivative function dydt(y, t)
    dt: time step
    t: current time
    """
    k1 = dydt(y, t)
    k2 = dydt(y + 0.5 * dt * k1, t + 0.5 * dt)
    k3 = dydt(y + 0.5 * dt * k2, t + 0.5 * dt)
    k4 = dydt(y + dt * k3, t + dt)
    return y + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)


def integrate_ode(dydt: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                  dt: float = 0.01, method: str = 'rk4') -> Tuple[np.ndarray, np.ndarray]:
    """
    Integrate ODE system 积分常微分方程组

    Parameters:
        dydt: derivative function dydt(y, t)
        y0: initial conditions
        t_span: (t_start, t_end)
        dt: time step
        method: 'euler' or 'rk4'

    Returns:
        t_array, y_array
    """
    t_start, t_end = t_span
    t_array = np.arange(t_start, t_end + dt, dt)
    y_array = np.zeros((len(t_array), len(y0)))
    y_array[0] = y0

    step_func = rk4_step if method == 'rk4' else euler_step

    for i in range(1, len(t_array)):
        y_array[i] = step_func(y_array[i-1], dydt, dt, t_array[i-1])

    return t_array, y_array


# =============================================================================
# Coordinate Transformations 坐标变换
# =============================================================================

def cartesian_to_polar(x: float, y: float) -> Tuple[float, float]:
    """Convert Cartesian to polar coordinates 笛卡尔坐标转极坐标"""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta


def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
    """Convert polar to Cartesian coordinates 极坐标转笛卡尔坐标"""
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def cartesian_to_spherical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """Convert Cartesian to spherical coordinates 笛卡尔坐标转球坐标"""
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r) if r != 0 else 0  # polar angle
    phi = np.arctan2(y, x)  # azimuthal angle
    return r, theta, phi


def spherical_to_cartesian(r: float, theta: float, phi: float) -> Tuple[float, float, float]:
    """Convert spherical to Cartesian coordinates 球坐标转笛卡尔坐标"""
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


# =============================================================================
# Special Relativity 狭义相对论
# =============================================================================

def lorentz_factor(v: float) -> float:
    """Calculate Lorentz factor γ 计算洛伦兹因子"""
    beta = v / c
    if abs(beta) >= 1:
        raise ValueError("Velocity must be less than speed of light")
    return 1 / np.sqrt(1 - beta**2)


def time_dilation(t0: float, v: float) -> float:
    """Calculate dilated time 计算时间膨胀"""
    gamma = lorentz_factor(v)
    return gamma * t0


def length_contraction(L0: float, v: float) -> float:
    """Calculate contracted length 计算长度收缩"""
    gamma = lorentz_factor(v)
    return L0 / gamma


def relativistic_momentum(m: float, v: float) -> float:
    """Calculate relativistic momentum 计算相对论动量"""
    gamma = lorentz_factor(v)
    return gamma * m * v


def relativistic_energy(m: float, v: float) -> float:
    """Calculate relativistic total energy 计算相对论总能量"""
    gamma = lorentz_factor(v)
    return gamma * m * c**2


def rest_energy(m: float) -> float:
    """Calculate rest energy E = mc² 计算静止能量"""
    return m * c**2


# =============================================================================
# Quantum Mechanics 量子力学
# =============================================================================

def de_broglie_wavelength(p: float) -> float:
    """Calculate de Broglie wavelength λ = h/p 计算德布罗意波长"""
    return h / p


def photon_energy(frequency: float) -> float:
    """Calculate photon energy E = hf 计算光子能量"""
    return h * frequency


def photon_momentum(frequency: float) -> float:
    """Calculate photon momentum p = hf/c 计算光子动量"""
    return h * frequency / c


def uncertainty_position_momentum(delta_x: float) -> float:
    """Minimum momentum uncertainty from position uncertainty 由位置不确定度求动量不确定度下限"""
    return hbar / (2 * delta_x)


def bohr_energy(n: int, Z: int = 1) -> float:
    """Calculate hydrogen-like atom energy level 计算类氢原子能级
    n: principal quantum number
    Z: atomic number
    """
    return -13.6 * Z**2 / n**2 * eV


def bohr_radius_n(n: int, Z: int = 1) -> float:
    """Calculate Bohr radius for level n 计算第n能级玻尔半径"""
    return n**2 * a_0 / Z


# =============================================================================
# Statistical Mechanics 统计力学
# =============================================================================

def maxwell_boltzmann_speed(v: np.ndarray, m: float, T: float) -> np.ndarray:
    """Maxwell-Boltzmann speed distribution 麦克斯韦-玻尔兹曼速率分布"""
    factor = (m / (2 * np.pi * k_B * T))**1.5
    return 4 * np.pi * factor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))


def fermi_dirac(E: np.ndarray, mu: float, T: float) -> np.ndarray:
    """Fermi-Dirac distribution 费米-狄拉克分布"""
    if T == 0:
        return np.where(E < mu, 1.0, 0.0)
    return 1 / (np.exp((E - mu) / (k_B * T)) + 1)


def bose_einstein(E: np.ndarray, mu: float, T: float) -> np.ndarray:
    """Bose-Einstein distribution 玻色-爱因斯坦分布"""
    if T == 0:
        raise ValueError("T must be > 0 for Bose-Einstein distribution")
    return 1 / (np.exp((E - mu) / (k_B * T)) - 1)


def planck_distribution(nu: np.ndarray, T: float) -> np.ndarray:
    """Planck's black body radiation distribution 普朗克黑体辐射分布"""
    return (8 * np.pi * h * nu**3 / c**3) / (np.exp(h * nu / (k_B * T)) - 1)


# =============================================================================
# Wave Functions 波函数
# =============================================================================

def gaussian_wave_packet(x: np.ndarray, x0: float, sigma: float, k0: float) -> np.ndarray:
    """
    Gaussian wave packet 高斯波包
    ψ(x) = (2πσ²)^(-1/4) * exp(-(x-x0)²/(4σ²)) * exp(ik0*x)
    """
    norm = (2 * np.pi * sigma**2)**(-0.25)
    envelope = np.exp(-(x - x0)**2 / (4 * sigma**2))
    phase = np.exp(1j * k0 * x)
    return norm * envelope * phase


def normalize_wavefunction(psi: np.ndarray, dx: float) -> np.ndarray:
    """Normalize a wavefunction 归一化波函数"""
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi / norm


def expectation_value(psi: np.ndarray, operator: np.ndarray, dx: float) -> complex:
    """Calculate expectation value <ψ|O|ψ> 计算期望值"""
    return np.sum(np.conj(psi) * operator @ psi) * dx


def probability_density(psi: np.ndarray) -> np.ndarray:
    """Calculate probability density |ψ|² 计算概率密度"""
    return np.abs(psi)**2
