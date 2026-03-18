"""
Project-specific configuration for ODSlings (open-data-structure).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="odslings",
    display_name="ODS Rustlings - 数据结构交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    project_root=Path(__file__).parent.parent,
    chapters={
        "00_intro": "00 入门",
        "01_arrays": "01 数组",
        "02_lists": "02 链表",
        "03_stacks_queues": "03 栈与队列",
        "04_hash_tables": "04 哈希表",
        "05_trees": "05 树",
        "06_heaps": "06 堆",
        "07_graphs": "07 图",
        "08_sorting": "08 排序",
        "09_advanced": "09 高级结构",
        "10_advanced_structures": "10 高级数据结构",
        "11_specialized_structures": "11 特殊数据结构",
    },
    banner=r"""
     ██████╗ ██████╗ ███████╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔═══██╗██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██║   ██║██║  ██║███████╗██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║   ██║██║  ██║╚════██║██║     ██║██║╚██╗██║██║   ██║╚════██║
    ╚██████╔╝██████╔╝███████║███████╗██║██║ ╚████║╚██████╔╝███████║
     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

           数据结构交互式学习系统 v1.0.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
