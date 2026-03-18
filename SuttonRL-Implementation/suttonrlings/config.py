"""
Project-specific configuration for SuttonRLings (SuttonRL-Implementation).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="suttonrlings",
    display_name="Sutton RL - 强化学习交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    solutions_dir="solutions",
    project_root=Path(__file__).parent.parent,
    chapters={
        "ch02_bandits": "Ch02 多臂老虎机",
        "ch04_dp": "Ch04 动态规划",
        "ch05_mc": "Ch05 蒙特卡洛方法",
        "ch06_td": "Ch06 时序差分",
        "ch07_nstep": "Ch07 n步方法",
        "ch08_planning": "Ch08 规划与学习",
        "ch09_approximation": "Ch09 函数近似",
        "ch10_control": "Ch10 策略控制",
        "ch11_offpolicy": "Ch11 Off-Policy 方法",
        "ch12_eligibility": "Ch12 资格迹",
        "ch13_policy_gradient": "Ch13 策略梯度",
        "ch14_advanced": "Ch14 高级方法",
        "ch15_exploration": "Ch15 探索策略",
        "ch16_modelbased": "Ch16 基于模型方法",
        "ch17_multiagent": "Ch17 多智能体",
        "ch18_hierarchical": "Ch18 分层强化学习",
        "ch19_imitation": "Ch19 模仿学习",
        "ch20_inverse_rl": "Ch20 逆强化学习",
        "ch21_offline_rl": "Ch21 离线强化学习",
        "ch22_rlhf": "Ch22 RLHF",
    },
    banner=r"""
    ███████╗██╗   ██╗████████╗████████╗ ██████╗ ███╗   ██╗    ██████╗ ██╗
    ██╔════╝██║   ██║╚══██╔══╝╚══██╔══╝██╔═══██╗████╗  ██║    ██╔══██╗██║
    ███████╗██║   ██║   ██║      ██║   ██║   ██║██╔██╗ ██║    ██████╔╝██║
    ╚════██║██║   ██║   ██║      ██║   ██║   ██║██║╚██╗██║    ██╔══██╗██║
    ███████║╚██████╔╝   ██║      ██║   ╚██████╔╝██║ ╚████║    ██║  ██║███████╗
    ╚══════╝ ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝╚══════╝

              强化学习交互式学习系统 v1.0.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
