"""
Project-specific configuration for Asynclings (Asynchronous-Programming-Learning).
TypeScript exercises with subprocess-based validation.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="asynclings",
    display_name="Asynclings - 异步编程交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    solutions_dir="solutions",
    project_root=Path(__file__).parent.parent,
    chapters={
        "01_basics": "01 异步基础",
        "02_promises": "02 Promise",
        "03_async_await": "03 Async/Await",
        "04_error_handling": "04 错误处理",
        "05_concurrent": "05 并发模式",
        "06_advanced": "06 高级模式",
        "07_applications": "07 实际应用",
    },
    banner=r"""
     █████╗ ███████╗██╗   ██╗███╗   ██╗ ██████╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔══██╗██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ███████║███████╗ ╚████╔╝ ██╔██╗ ██║██║     ██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██╔══██║╚════██║  ╚██╔╝  ██║╚██╗██║██║     ██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██║  ██║███████║   ██║   ██║ ╚████║╚██████╗███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

            异步编程交互式学习系统 v1.0.0
    """,
    file_extension=".ts",
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
