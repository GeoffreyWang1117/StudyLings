"""
Physics Visualization Tools - 物理可视化工具
Plotting utilities for physics simulations and data
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from typing import List, Tuple, Optional, Callable
import warnings

# Set up matplotlib for better physics plots
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


def setup_2d_axes(title: str = "", xlabel: str = "x", ylabel: str = "y",
                  equal_aspect: bool = False) -> Tuple[plt.Figure, plt.Axes]:
    """Set up a 2D plot with standard physics styling"""
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if equal_aspect:
        ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    return fig, ax


def setup_3d_axes(title: str = "", xlabel: str = "x", ylabel: str = "y",
                  zlabel: str = "z") -> Tuple[plt.Figure, Axes3D]:
    """Set up a 3D plot with standard physics styling"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    return fig, ax


# =============================================================================
# Vector Visualization 向量可视化
# =============================================================================

def draw_vector(ax: plt.Axes, origin: np.ndarray, vector: np.ndarray,
                color: str = 'blue', label: str = None, width: float = 0.02):
    """Draw a vector arrow on 2D axes"""
    ax.quiver(origin[0], origin[1], vector[0], vector[1],
              angles='xy', scale_units='xy', scale=1,
              color=color, width=width, label=label)


def draw_vector_3d(ax: Axes3D, origin: np.ndarray, vector: np.ndarray,
                   color: str = 'blue', label: str = None):
    """Draw a vector arrow on 3D axes"""
    ax.quiver(origin[0], origin[1], origin[2],
              vector[0], vector[1], vector[2],
              color=color, label=label, arrow_length_ratio=0.1)


def plot_vector_field_2d(ax: plt.Axes, X: np.ndarray, Y: np.ndarray,
                         U: np.ndarray, V: np.ndarray,
                         title: str = "Vector Field", density: int = 1):
    """Plot a 2D vector field"""
    # Subsample for clarity
    ax.quiver(X[::density, ::density], Y[::density, ::density],
              U[::density, ::density], V[::density, ::density])
    ax.set_title(title)
    ax.set_aspect('equal')


def plot_streamlines(ax: plt.Axes, X: np.ndarray, Y: np.ndarray,
                     U: np.ndarray, V: np.ndarray,
                     title: str = "Streamlines", density: float = 1.5):
    """Plot streamlines of a vector field"""
    ax.streamplot(X, Y, U, V, density=density, color=np.sqrt(U**2 + V**2),
                  cmap='viridis')
    ax.set_title(title)
    ax.set_aspect('equal')


# =============================================================================
# Trajectory Visualization 轨迹可视化
# =============================================================================

def plot_trajectory_2d(ax: plt.Axes, x: np.ndarray, y: np.ndarray,
                       title: str = "Trajectory", show_start_end: bool = True):
    """Plot a 2D trajectory"""
    ax.plot(x, y, 'b-', linewidth=1.5, label='Trajectory')
    if show_start_end:
        ax.plot(x[0], y[0], 'go', markersize=10, label='Start')
        ax.plot(x[-1], y[-1], 'ro', markersize=10, label='End')
    ax.set_title(title)
    ax.legend()


def plot_trajectory_3d(ax: Axes3D, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                       title: str = "3D Trajectory", show_start_end: bool = True):
    """Plot a 3D trajectory"""
    ax.plot(x, y, z, 'b-', linewidth=1.5, label='Trajectory')
    if show_start_end:
        ax.scatter(x[0], y[0], z[0], c='g', s=100, label='Start')
        ax.scatter(x[-1], y[-1], z[-1], c='r', s=100, label='End')
    ax.set_title(title)
    ax.legend()


def plot_phase_space(ax: plt.Axes, q: np.ndarray, p: np.ndarray,
                     title: str = "Phase Space", xlabel: str = "q",
                     ylabel: str = "p"):
    """Plot phase space trajectory"""
    ax.plot(q, p, 'b-', linewidth=0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)


def plot_phase_portrait(ax: plt.Axes, trajectories: List[Tuple[np.ndarray, np.ndarray]],
                        title: str = "Phase Portrait"):
    """Plot multiple phase space trajectories"""
    colors = plt.cm.viridis(np.linspace(0, 1, len(trajectories)))
    for i, (q, p) in enumerate(trajectories):
        ax.plot(q, p, color=colors[i], linewidth=0.5)
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.set_title(title)


# =============================================================================
# Energy Diagrams 能量图
# =============================================================================

def plot_potential_energy(ax: plt.Axes, x: np.ndarray, V: np.ndarray,
                          E_levels: List[float] = None,
                          title: str = "Potential Energy"):
    """Plot potential energy curve with optional energy levels"""
    ax.plot(x, V, 'b-', linewidth=2, label='V(x)')
    ax.fill_between(x, V, alpha=0.3)

    if E_levels:
        for i, E in enumerate(E_levels):
            ax.axhline(y=E, color=f'C{i+1}', linestyle='--',
                       label=f'E = {E:.2f}')

    ax.set_xlabel('x')
    ax.set_ylabel('V(x)')
    ax.set_title(title)
    ax.legend()


def plot_energy_diagram(ax: plt.Axes, t: np.ndarray, KE: np.ndarray,
                        PE: np.ndarray, title: str = "Energy vs Time"):
    """Plot kinetic, potential, and total energy"""
    TE = KE + PE
    ax.plot(t, KE, 'r-', label='Kinetic Energy')
    ax.plot(t, PE, 'b-', label='Potential Energy')
    ax.plot(t, TE, 'k--', label='Total Energy')
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.set_title(title)
    ax.legend()


# =============================================================================
# Quantum Mechanics Visualization 量子力学可视化
# =============================================================================

def plot_wavefunction(ax: plt.Axes, x: np.ndarray, psi: np.ndarray,
                      title: str = "Wavefunction", show_probability: bool = True):
    """Plot wavefunction and optionally probability density"""
    ax.plot(x, np.real(psi), 'b-', label='Re(ψ)', linewidth=1.5)
    ax.plot(x, np.imag(psi), 'r-', label='Im(ψ)', linewidth=1.5)

    if show_probability:
        prob = np.abs(psi)**2
        ax.fill_between(x, prob, alpha=0.3, color='purple', label='|ψ|²')

    ax.set_xlabel('x')
    ax.set_ylabel('ψ(x)')
    ax.set_title(title)
    ax.legend()


def plot_probability_density(ax: plt.Axes, x: np.ndarray, psi: np.ndarray,
                             V: np.ndarray = None, title: str = "Probability Density"):
    """Plot probability density with optional potential"""
    prob = np.abs(psi)**2
    ax.fill_between(x, prob, alpha=0.6, color='blue', label='|ψ|²')
    ax.plot(x, prob, 'b-', linewidth=1)

    if V is not None:
        ax2 = ax.twinx()
        ax2.plot(x, V, 'r--', label='V(x)')
        ax2.set_ylabel('V(x)', color='r')

    ax.set_xlabel('x')
    ax.set_ylabel('|ψ|²')
    ax.set_title(title)


def plot_bloch_sphere(ax: Axes3D, theta: float, phi: float,
                      title: str = "Bloch Sphere"):
    """Plot a state on the Bloch sphere"""
    # Draw sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x, y, z, alpha=0.2, color='gray')

    # Draw axes
    ax.quiver(0, 0, 0, 1.3, 0, 0, color='r', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.3, 0, color='g', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.3, color='b', arrow_length_ratio=0.1)

    # Plot state vector
    sx = np.sin(theta) * np.cos(phi)
    sy = np.sin(theta) * np.sin(phi)
    sz = np.cos(theta)
    ax.quiver(0, 0, 0, sx, sy, sz, color='purple',
              arrow_length_ratio=0.1, linewidth=2)
    ax.scatter([sx], [sy], [sz], color='purple', s=50)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)


# =============================================================================
# Field Visualization 场可视化
# =============================================================================

def plot_scalar_field(ax: plt.Axes, X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
                      title: str = "Scalar Field", cmap: str = 'viridis'):
    """Plot a 2D scalar field as a heatmap"""
    c = ax.pcolormesh(X, Y, Z, cmap=cmap, shading='auto')
    plt.colorbar(c, ax=ax)
    ax.set_title(title)
    ax.set_aspect('equal')


def plot_equipotential_lines(ax: plt.Axes, X: np.ndarray, Y: np.ndarray,
                             V: np.ndarray, levels: int = 20,
                             title: str = "Equipotential Lines"):
    """Plot equipotential contour lines"""
    cs = ax.contour(X, Y, V, levels=levels, cmap='RdYlBu')
    ax.clabel(cs, inline=True, fontsize=8)
    ax.set_title(title)
    ax.set_aspect('equal')


def plot_electric_field_lines(ax: plt.Axes, charges: List[Tuple[float, float, float]],
                              xlim: Tuple[float, float] = (-5, 5),
                              ylim: Tuple[float, float] = (-5, 5),
                              title: str = "Electric Field Lines"):
    """
    Plot electric field lines for point charges
    charges: list of (x, y, q) tuples
    """
    x = np.linspace(xlim[0], xlim[1], 50)
    y = np.linspace(ylim[0], ylim[1], 50)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for cx, cy, q in charges:
        dx = X - cx
        dy = Y - cy
        r = np.sqrt(dx**2 + dy**2)
        r = np.maximum(r, 0.1)  # Avoid division by zero
        Ex += q * dx / r**3
        Ey += q * dy / r**3

    ax.streamplot(X, Y, Ex, Ey, density=1.5, color='blue')

    # Draw charges
    for cx, cy, q in charges:
        color = 'red' if q > 0 else 'blue'
        marker = '+' if q > 0 else '_'
        ax.plot(cx, cy, marker, markersize=15, color=color, markeredgewidth=3)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title)
    ax.set_aspect('equal')


# =============================================================================
# Spacetime Diagrams 时空图
# =============================================================================

def plot_spacetime_diagram(ax: plt.Axes, worldlines: List[Tuple[np.ndarray, np.ndarray]],
                           labels: List[str] = None,
                           show_light_cone: bool = True,
                           title: str = "Spacetime Diagram"):
    """
    Plot a spacetime diagram (Minkowski diagram)
    worldlines: list of (t, x) arrays
    """
    if show_light_cone:
        t_max = max(max(t) for t, x in worldlines)
        t = np.linspace(0, t_max, 100)
        ax.plot(t, t, 'y--', alpha=0.5, label='Light cone')
        ax.plot(t, -t, 'y--', alpha=0.5)
        ax.fill_between(t, -t, t, alpha=0.1, color='yellow')

    colors = plt.cm.tab10(np.linspace(0, 1, len(worldlines)))
    for i, (t, x) in enumerate(worldlines):
        label = labels[i] if labels else f'Object {i+1}'
        ax.plot(t, x, color=colors[i], linewidth=2, label=label)

    ax.set_xlabel('t (ct)')
    ax.set_ylabel('x')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)


# =============================================================================
# Animation Helpers 动画辅助
# =============================================================================

def create_trajectory_animation(fig: plt.Figure, ax: plt.Axes,
                                x: np.ndarray, y: np.ndarray,
                                interval: int = 50,
                                trail_length: int = 50) -> FuncAnimation:
    """Create an animation of a 2D trajectory"""
    line, = ax.plot([], [], 'b-', linewidth=1)
    point, = ax.plot([], [], 'ro', markersize=8)

    ax.set_xlim(x.min() - 0.1, x.max() + 0.1)
    ax.set_ylim(y.min() - 0.1, y.max() + 0.1)

    def init():
        line.set_data([], [])
        point.set_data([], [])
        return line, point

    def update(frame):
        start = max(0, frame - trail_length)
        line.set_data(x[start:frame], y[start:frame])
        point.set_data([x[frame]], [y[frame]])
        return line, point

    return FuncAnimation(fig, update, frames=len(x),
                         init_func=init, interval=interval, blit=True)


def show_plot():
    """Display all current plots"""
    plt.tight_layout()
    plt.show()


def save_plot(filename: str, dpi: int = 150):
    """Save current figure"""
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"Plot saved to {filename}")
