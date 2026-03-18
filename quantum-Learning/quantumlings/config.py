"""
Project-specific configuration for Quantumlings (quantum-Learning).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="quantumlings",
    display_name="Quantum Rustlings - 通过编程学习量子计算",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    solutions_dir="solutions",
    project_root=Path(__file__).parent.parent,
    chapters={
        "intro": "入门 Introduction",
        "entanglement": "量子纠缠 Entanglement",
        "algorithms": "量子算法 Algorithms",
        "error_correction": "量子纠错 Error Correction",
        "variational": "变分算法 Variational",
        "nisq": "NISQ 应用 NISQ Applications",
        "frontiers": "前沿研究 Frontiers",
        "advanced": "高级主题 Advanced",
    },
    banner=r"""
     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗
    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║
    ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
    ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝

              通过编程学习量子计算 v1.0.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
