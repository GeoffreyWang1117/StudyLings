"""
Studylings integration config for JAXlings (CUDA-Tutorial).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="jaxlings",
    display_name="JAXlings - JAX 交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    project_root=Path(__file__).parent.parent,
    chapters={
        "01_intro": "01 JAX 入门",
        "02_arrays": "02 数组操作",
        "03_transformations": "03 JAX 变换",
        "04_neural_networks": "04 神经网络基础",
        "05_advanced": "05 高级特性",
        "06_random": "06 随机数",
        "07_pytrees": "07 PyTrees",
        "08_control_flow": "08 控制流",
        "09_parallel": "09 并行计算",
        "10_deep_learning": "10 深度学习",
    },
    banner=r"""
         ██╗ █████╗ ██╗  ██╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
         ██║██╔══██╗╚██╗██╔╝██║     ██║████╗  ██║██╔════╝ ██╔════╝
         ██║███████║ ╚███╔╝ ██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██   ██║██╔══██║ ██╔██╗ ██║     ██║██║╚██╗██║██║   ██║╚════██║
    ╚█████╔╝██║  ██║██╔╝ ██╗███████╗██║██║ ╚████║╚██████╔╝███████║
     ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

                JAX 交互式学习系统 v1.0.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
