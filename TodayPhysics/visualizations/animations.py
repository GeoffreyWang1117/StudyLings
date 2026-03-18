"""
Physics Animations - 物理动画
Animation utilities for physics simulations
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from typing import Callable, Tuple, List, Optional


class PhysicsAnimation:
    """Base class for physics animations"""

    def __init__(self, fig: plt.Figure, ax: plt.Axes, interval: int = 50):
        self.fig = fig
        self.ax = ax
        self.interval = interval
        self.animation = None

    def animate(self, frames: int) -> FuncAnimation:
        """Override this method in subclasses"""
        raise NotImplementedError

    def save(self, filename: str, fps: int = 30):
        """Save animation to file"""
        if self.animation:
            self.animation.save(filename, fps=fps)
            print(f"Animation saved to {filename}")

    def show(self):
        """Display the animation"""
        plt.show()


class PendulumAnimation(PhysicsAnimation):
    """Animate a simple pendulum"""

    def __init__(self, L: float, theta: np.ndarray, interval: int = 50):
        fig, ax = plt.subplots(figsize=(6, 6))
        super().__init__(fig, ax, interval)

        self.L = L
        self.theta = theta

        # Set up plot
        ax.set_xlim(-L * 1.2, L * 1.2)
        ax.set_ylim(-L * 1.2, L * 0.2)
        ax.set_aspect('equal')
        ax.set_title('Simple Pendulum 单摆')

        # Create objects
        self.line, = ax.plot([], [], 'k-', linewidth=2)
        self.bob = Circle((0, 0), L * 0.05, fc='blue', ec='black')
        ax.add_patch(self.bob)
        ax.plot(0, 0, 'ko', markersize=10)  # Pivot

    def animate(self, frames: int = None) -> FuncAnimation:
        if frames is None:
            frames = len(self.theta)

        def init():
            self.line.set_data([], [])
            self.bob.center = (0, -self.L)
            return self.line, self.bob

        def update(frame):
            x = self.L * np.sin(self.theta[frame])
            y = -self.L * np.cos(self.theta[frame])
            self.line.set_data([0, x], [0, y])
            self.bob.center = (x, y)
            return self.line, self.bob

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=True
        )
        return self.animation


class SpringMassAnimation(PhysicsAnimation):
    """Animate a spring-mass system"""

    def __init__(self, x: np.ndarray, x_eq: float = 0, interval: int = 50):
        fig, ax = plt.subplots(figsize=(10, 4))
        super().__init__(fig, ax, interval)

        self.x = x
        self.x_eq = x_eq

        # Set up plot
        x_range = max(abs(x.max()), abs(x.min())) + 0.5
        ax.set_xlim(-1, x_range + 1)
        ax.set_ylim(-0.5, 0.5)
        ax.set_aspect('equal')
        ax.axvline(x=x_eq, color='gray', linestyle='--', alpha=0.5)
        ax.set_title('Spring-Mass System 弹簧振子')

        # Wall
        ax.fill_betweenx([-0.3, 0.3], -1, -0.8, color='gray', hatch='///')

        # Create objects
        self.spring, = ax.plot([], [], 'b-', linewidth=2)
        self.mass = Rectangle((0, -0.15), 0.3, 0.3, fc='red', ec='black')
        ax.add_patch(self.mass)

    def _draw_spring(self, x_end: float, n_coils: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Generate spring coordinates"""
        x_start = -0.8
        n_points = n_coils * 4 + 2
        xs = np.linspace(x_start, x_end, n_points)
        ys = np.zeros(n_points)

        for i in range(1, n_points - 1):
            if i % 4 == 1:
                ys[i] = 0.1
            elif i % 4 == 3:
                ys[i] = -0.1

        return xs, ys

    def animate(self, frames: int = None) -> FuncAnimation:
        if frames is None:
            frames = len(self.x)

        def init():
            xs, ys = self._draw_spring(self.x[0])
            self.spring.set_data(xs, ys)
            self.mass.set_x(self.x[0])
            return self.spring, self.mass

        def update(frame):
            xs, ys = self._draw_spring(self.x[frame])
            self.spring.set_data(xs, ys)
            self.mass.set_x(self.x[frame])
            return self.spring, self.mass

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=True
        )
        return self.animation


class WaveAnimation(PhysicsAnimation):
    """Animate a traveling or standing wave"""

    def __init__(self, x: np.ndarray, wave_func: Callable,
                 t_max: float, dt: float = 0.05, interval: int = 50):
        fig, ax = plt.subplots(figsize=(10, 4))
        super().__init__(fig, ax, interval)

        self.x = x
        self.wave_func = wave_func
        self.t_values = np.arange(0, t_max, dt)

        # Set up plot
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Wave Animation 波动动画')
        ax.grid(True, alpha=0.3)

        self.line, = ax.plot([], [], 'b-', linewidth=2)

    def animate(self, frames: int = None) -> FuncAnimation:
        if frames is None:
            frames = len(self.t_values)

        def init():
            self.line.set_data([], [])
            return self.line,

        def update(frame):
            t = self.t_values[frame]
            y = self.wave_func(self.x, t)
            self.line.set_data(self.x, y)
            return self.line,

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=True
        )
        return self.animation


class OrbitAnimation(PhysicsAnimation):
    """Animate orbital motion"""

    def __init__(self, x: np.ndarray, y: np.ndarray,
                 central_body_radius: float = 0.1, interval: int = 50):
        fig, ax = plt.subplots(figsize=(8, 8))
        super().__init__(fig, ax, interval)

        self.x = x
        self.y = y

        # Set up plot
        max_r = max(max(abs(x)), max(abs(y))) * 1.1
        ax.set_xlim(-max_r, max_r)
        ax.set_ylim(-max_r, max_r)
        ax.set_aspect('equal')
        ax.set_title('Orbital Motion 轨道运动')
        ax.grid(True, alpha=0.3)

        # Central body
        central = Circle((0, 0), central_body_radius, fc='yellow', ec='orange')
        ax.add_patch(central)

        # Orbiting body and trail
        self.orbit_trail, = ax.plot([], [], 'b-', linewidth=0.5, alpha=0.5)
        self.orbit_body = Circle((x[0], y[0]), central_body_radius * 0.3,
                                  fc='blue', ec='black')
        ax.add_patch(self.orbit_body)

    def animate(self, frames: int = None, trail_length: int = 100) -> FuncAnimation:
        if frames is None:
            frames = len(self.x)

        def init():
            self.orbit_trail.set_data([], [])
            self.orbit_body.center = (self.x[0], self.y[0])
            return self.orbit_trail, self.orbit_body

        def update(frame):
            start = max(0, frame - trail_length)
            self.orbit_trail.set_data(self.x[start:frame], self.y[start:frame])
            self.orbit_body.center = (self.x[frame], self.y[frame])
            return self.orbit_trail, self.orbit_body

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=True
        )
        return self.animation


class ParticleBoxAnimation(PhysicsAnimation):
    """Animate particles in a box (ideal gas visualization)"""

    def __init__(self, positions: np.ndarray, box_size: float = 1.0,
                 interval: int = 50):
        """
        positions: array of shape (n_frames, n_particles, 2)
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        super().__init__(fig, ax, interval)

        self.positions = positions
        self.box_size = box_size
        self.n_particles = positions.shape[1]

        # Set up plot
        ax.set_xlim(-0.1, box_size + 0.1)
        ax.set_ylim(-0.1, box_size + 0.1)
        ax.set_aspect('equal')
        ax.set_title('Particles in a Box 理想气体')

        # Draw box
        box = Rectangle((0, 0), box_size, box_size,
                         fill=False, ec='black', linewidth=2)
        ax.add_patch(box)

        # Create particles
        self.particles, = ax.plot([], [], 'bo', markersize=5)

    def animate(self, frames: int = None) -> FuncAnimation:
        if frames is None:
            frames = len(self.positions)

        def init():
            self.particles.set_data([], [])
            return self.particles,

        def update(frame):
            pos = self.positions[frame]
            self.particles.set_data(pos[:, 0], pos[:, 1])
            return self.particles,

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=True
        )
        return self.animation


class QuantumWavePacketAnimation(PhysicsAnimation):
    """Animate a quantum wave packet evolution"""

    def __init__(self, x: np.ndarray, psi_t: np.ndarray,
                 V: np.ndarray = None, interval: int = 50):
        """
        psi_t: array of shape (n_frames, n_x) - wavefunction at each time
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        super().__init__(fig, ax, interval)

        self.x = x
        self.psi_t = psi_t
        self.V = V

        # Set up plot
        ax.set_xlim(x.min(), x.max())
        prob_max = np.max(np.abs(psi_t)**2)
        ax.set_ylim(-0.1, prob_max * 1.2)
        ax.set_xlabel('x')
        ax.set_ylabel('|ψ|²')
        ax.set_title('Quantum Wave Packet 量子波包')

        # Plot potential if provided
        if V is not None:
            ax2 = ax.twinx()
            ax2.plot(x, V, 'r--', alpha=0.5, label='V(x)')
            ax2.set_ylabel('V(x)', color='r')

        self.prob_line, = ax.plot([], [], 'b-', linewidth=2)
        self.prob_fill = ax.fill_between([], [], alpha=0.3, color='blue')

    def animate(self, frames: int = None) -> FuncAnimation:
        if frames is None:
            frames = len(self.psi_t)

        def init():
            self.prob_line.set_data([], [])
            return self.prob_line,

        def update(frame):
            prob = np.abs(self.psi_t[frame])**2
            self.prob_line.set_data(self.x, prob)

            # Update fill (need to remove and recreate)
            for coll in self.ax.collections:
                coll.remove()
            self.ax.fill_between(self.x, prob, alpha=0.3, color='blue')

            return self.prob_line,

        self.animation = FuncAnimation(
            self.fig, update, frames=frames,
            init_func=init, interval=self.interval, blit=False
        )
        return self.animation


def animate_double_pendulum(theta1: np.ndarray, theta2: np.ndarray,
                            L1: float, L2: float,
                            interval: int = 50) -> FuncAnimation:
    """Create animation for double pendulum"""
    fig, ax = plt.subplots(figsize=(8, 8))

    L_total = L1 + L2
    ax.set_xlim(-L_total * 1.2, L_total * 1.2)
    ax.set_ylim(-L_total * 1.2, L_total * 0.2)
    ax.set_aspect('equal')
    ax.set_title('Double Pendulum 双摆')

    line, = ax.plot([], [], 'k-', linewidth=2)
    bob1 = Circle((0, 0), L_total * 0.03, fc='blue', ec='black')
    bob2 = Circle((0, 0), L_total * 0.03, fc='red', ec='black')
    ax.add_patch(bob1)
    ax.add_patch(bob2)
    ax.plot(0, 0, 'ko', markersize=10)

    trail, = ax.plot([], [], 'r-', linewidth=0.5, alpha=0.5)
    trail_x, trail_y = [], []

    def init():
        line.set_data([], [])
        bob1.center = (0, 0)
        bob2.center = (0, 0)
        trail.set_data([], [])
        return line, bob1, bob2, trail

    def update(frame):
        x1 = L1 * np.sin(theta1[frame])
        y1 = -L1 * np.cos(theta1[frame])
        x2 = x1 + L2 * np.sin(theta2[frame])
        y2 = y1 - L2 * np.cos(theta2[frame])

        line.set_data([0, x1, x2], [0, y1, y2])
        bob1.center = (x1, y1)
        bob2.center = (x2, y2)

        trail_x.append(x2)
        trail_y.append(y2)
        if len(trail_x) > 500:
            trail_x.pop(0)
            trail_y.pop(0)
        trail.set_data(trail_x, trail_y)

        return line, bob1, bob2, trail

    return FuncAnimation(fig, update, frames=len(theta1),
                         init_func=init, interval=interval, blit=True)
