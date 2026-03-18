"""
Project-specific configuration for Algolings (Traditional-Important-Algorithms).
Uses the Python exercise track (exercises/ directory with .py files).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="algolings",
    display_name="Algolings - 经典算法交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises_py",
    project_root=Path(__file__).parent.parent,
    chapters={
        "01_gc_and_memory": "01 GC与内存管理",
        "02_memory_models": "02 内存模型",
        "03_concurrency": "03 并发算法",
        "04_os_algorithms": "04 操作系统算法",
        "05_compiler": "05 编译器算法",
        "06_distributed_systems": "06 分布式系统",
        "07_cryptography": "07 密码学",
        "08_database": "08 数据库算法",
        "09_rate_limiting": "09 限流算法",
        "10_string_algorithms": "10 字符串算法",
        "11_stream_processing": "11 流处理",
        "12_graph_algorithms": "12 图算法",
        "13_data_structures": "13 数据结构",
        "14_ml_fundamentals": "14 机器学习基础",
    },
    banner=r"""
     █████╗ ██╗      ██████╗  ██████╗ ██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔══██╗██║     ██╔════╝ ██╔═══██╗██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ███████║██║     ██║  ███╗██║   ██║██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██╔══██║██║     ██║   ██║██║   ██║██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

              经典算法交互式学习系统 v1.0.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
