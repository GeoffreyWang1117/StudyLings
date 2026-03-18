"""
Project-specific configuration for ADMlings (ADM-algorithms).
"""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

_project_root = Path(__file__).parent.parent

_build_dir = None
for candidate in ["build", "cmake-build-debug"]:
    candidate_path = _project_root / candidate
    if candidate_path.exists():
        _build_dir = str(candidate_path)
        break
_build_dir = os.environ.get("ADMLINGS_BUILD_DIR", _build_dir)

config = ProjectConfig(
    name="admlings",
    display_name="ADM Algorithms - 算法设计手册交互式学习",
    version="1.0.0",
    validation_mode=ValidationMode.COMPILE_AND_RUN,
    exercises_dir="exercises",
    project_root=_project_root,
    chapters={
        "01_analysis": "01 算法分析",
        "02_data_structures": "02 数据结构",
        "03_sorting": "03 排序",
        "04_graph_traversal": "04 图遍历",
        "05_weighted_graphs": "05 加权图",
        "06_combinatorial": "06 组合搜索",
        "07_dynamic_programming": "07 动态规划",
        "08_greedy": "08 贪心算法",
        "09_strings": "09 字符串算法",
        "10_geometry": "10 计算几何",
        "11_np_complete": "11 NP完全问题",
        "12_divide_conquer": "12 分治法",
        "13_randomized": "13 随机算法",
        "14_advanced_graphs": "14 高级图算法",
        "15_number_theory": "15 数论",
    },
    banner=r"""
     █████╗ ██████╗ ███╗   ███╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔══██╗██╔══██╗████╗ ████║██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ███████║██║  ██║██╔████╔██║██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██╔══██║██║  ██║██║╚██╔╝██║██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██║  ██║██████╔╝██║ ╚═╝ ██║███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

           算法设计手册交互式学习 v1.0.0
    """,
    file_extension=".cpp",
    build_dir=_build_dir,
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
    placeholder_markers=["/* ??? */"],
)
