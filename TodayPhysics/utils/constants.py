"""
Physical Constants - 物理常数
All values in SI units unless otherwise specified
"""

import numpy as np

# Fundamental Constants 基本常数
c = 299792458  # Speed of light 光速 [m/s]
h = 6.62607015e-34  # Planck constant 普朗克常数 [J·s]
hbar = h / (2 * np.pi)  # Reduced Planck constant 约化普朗克常数 [J·s]
G = 6.67430e-11  # Gravitational constant 万有引力常数 [m³/(kg·s²)]
e = 1.602176634e-19  # Elementary charge 元电荷 [C]
k_B = 1.380649e-23  # Boltzmann constant 玻尔兹曼常数 [J/K]
N_A = 6.02214076e23  # Avogadro constant 阿伏伽德罗常数 [mol⁻¹]
R = 8.314462618  # Gas constant 气体常数 [J/(mol·K)]

# Electromagnetic Constants 电磁常数
epsilon_0 = 8.8541878128e-12  # Vacuum permittivity 真空介电常数 [F/m]
mu_0 = 1.25663706212e-6  # Vacuum permeability 真空磁导率 [H/m]
k_e = 1 / (4 * np.pi * epsilon_0)  # Coulomb constant 库仑常数 [N·m²/C²]

# Particle Masses 粒子质量
m_e = 9.1093837015e-31  # Electron mass 电子质量 [kg]
m_p = 1.67262192369e-27  # Proton mass 质子质量 [kg]
m_n = 1.67492749804e-27  # Neutron mass 中子质量 [kg]

# Atomic Constants 原子常数
a_0 = 5.29177210903e-11  # Bohr radius 玻尔半径 [m]
alpha = 7.2973525693e-3  # Fine structure constant 精细结构常数 [dimensionless]
R_inf = 10973731.568160  # Rydberg constant 里德伯常数 [m⁻¹]
E_h = 4.3597447222071e-18  # Hartree energy 哈特里能量 [J]

# Astronomical Constants 天文常数
M_sun = 1.989e30  # Solar mass 太阳质量 [kg]
M_earth = 5.972e24  # Earth mass 地球质量 [kg]
R_earth = 6.371e6  # Earth radius 地球半径 [m]
AU = 1.496e11  # Astronomical unit 天文单位 [m]
ly = 9.461e15  # Light year 光年 [m]
pc = 3.086e16  # Parsec 秒差距 [m]

# Conversion Factors 单位换算
eV = 1.602176634e-19  # Electron volt 电子伏特 [J]
keV = 1e3 * eV
MeV = 1e6 * eV
GeV = 1e9 * eV
angstrom = 1e-10  # Angstrom 埃 [m]


def print_constants():
    """Print all constants with descriptions"""
    constants_info = [
        ("c", c, "Speed of light 光速", "m/s"),
        ("h", h, "Planck constant 普朗克常数", "J·s"),
        ("ħ", hbar, "Reduced Planck constant 约化普朗克常数", "J·s"),
        ("G", G, "Gravitational constant 万有引力常数", "m³/(kg·s²)"),
        ("e", e, "Elementary charge 元电荷", "C"),
        ("k_B", k_B, "Boltzmann constant 玻尔兹曼常数", "J/K"),
        ("m_e", m_e, "Electron mass 电子质量", "kg"),
        ("m_p", m_p, "Proton mass 质子质量", "kg"),
        ("ε₀", epsilon_0, "Vacuum permittivity 真空介电常数", "F/m"),
        ("μ₀", mu_0, "Vacuum permeability 真空磁导率", "H/m"),
    ]

    print("Physical Constants 物理常数")
    print("=" * 60)
    for symbol, value, name, unit in constants_info:
        print(f"{symbol:4s} = {value:.6e} {unit:15s} | {name}")


if __name__ == "__main__":
    print_constants()
