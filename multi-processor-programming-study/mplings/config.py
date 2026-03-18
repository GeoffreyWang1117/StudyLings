"""
Project-specific configuration for MPlings (multi-processor-programming-study).
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
_build_dir = os.environ.get("MPLINGS_BUILD_DIR", _build_dir)

config = ProjectConfig(
    name="mplings",
    display_name="MPlings - 多处理器编程交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.COMPILE_AND_RUN,
    exercises_dir="exercises/cpp",
    project_root=_project_root,
    chapters={
        "01_basics": "01 并发基础",
        "02_mutual_exclusion": "02 互斥",
        "03_concurrent_objects": "03 并发对象",
        "04_foundations": "04 理论基础",
        "05_synchronization": "05 同步原语",
        "06_consensus": "06 共识",
        "07_spin_locks": "07 自旋锁",
        "08_monitors": "08 管程",
        "09_linked_lists": "09 并发链表",
        "10_queues": "10 并发队列",
        "11_stacks": "11 并发栈",
    },
    banner=r"""
    ███╗   ███╗██████╗ ██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ████╗ ████║██╔══██╗██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██╔████╔██║██████╔╝██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║╚██╔╝██║██╔═══╝ ██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██║ ╚═╝ ██║██║     ███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

         多处理器编程交互式学习系统 v1.0.0
    """,
    file_extension=".cpp",
    build_dir=_build_dir,
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
