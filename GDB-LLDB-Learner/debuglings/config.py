"""
Project-specific configuration for Debuglings (GDB-LLDB-Learner).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

_project_root = Path(__file__).parent.parent

config = ProjectConfig(
    name="debuglings",
    display_name="Debuglings - GDB/LLDB 调试技术交互式学习",
    version="1.0.0",
    validation_mode=ValidationMode.COMPILE_AND_RUN,
    exercises_dir="exercises",
    project_root=_project_root,
    chapters={
        "level-01-basics": "Level 01 基础调试",
        "level-02-breakpoints": "Level 02 断点",
        "level-03-execution": "Level 03 执行控制",
        "level-04-variables": "Level 04 变量检查",
        "level-05-callstack": "Level 05 调用栈",
        "level-06-threads": "Level 06 多线程调试",
        "level-07-memory": "Level 07 内存调试",
        "level-08-coredump": "Level 08 Core Dump",
        "level-09-advanced": "Level 09 高级技巧",
        "level-10-datastructures": "Level 10 数据结构",
        "level-11-pointers": "Level 11 指针调试",
        "level-12-memory-layout": "Level 12 内存布局",
        "level-13-linker": "Level 13 链接器",
    },
    banner=r"""
    ██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗ ██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝ ██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

           GDB/LLDB 调试技术交互式学习 v1.0.0
    """,
    file_extension=".c",
    comment_prefix="//",
    todo_markers=["TODO:", "FIXME:"],
    incomplete_markers=["I AM NOT DONE"],
)
