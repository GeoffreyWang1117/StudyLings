"""
Project-specific configuration for Unixlings (APUE, modern edition).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

_project_root = Path(__file__).parent.parent

config = ProjectConfig(
    name="unixlings",
    display_name="Unixlings - APUE 现代版：文件/进程/信号/线程",
    version="0.1.0",
    validation_mode=ValidationMode.BUILD_AND_PROBE,
    exercises_dir="exercises",
    tests_dir="tests",
    solutions_dir="solutions",
    hints_dir="hints",
    project_root=_project_root,
    chapters={
        "00_c_prep": "A00 系统编程 C 预备",
        "01_file_io": "A01 文件 I/O (APUE 3-4)",
        "02_process": "A02 进程控制 (APUE 7-9)",
        "03_signals": "A03 信号 (APUE 10)",
        "04_threads": "A04 线程 (APUE 11-12)",
    },
    banner=r"""
    ██╗   ██╗███╗   ██╗██╗██╗  ██╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██║   ██║████╗  ██║██║╚██╗██╔╝██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██║   ██║██╔██╗ ██║██║ ╚███╔╝ ██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║   ██║██║╚██╗██║██║ ██╔██╗ ██║     ██║██║╚██╗██║██║   ██║╚════██║
    ╚██████╔╝██║ ╚████║██║██╔╝ ██╗███████╗██║██║ ╚████║╚██████╔╝███████║
     ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

        APUE 现代版 · C23 · CMake · Sanitizers · strace
    """,
    file_extension=".c",
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
    run_timeout=10,
)
