"""
Project-specific configuration for Economlings.
"""

from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="economlings",
    display_name="Economlings - 经济学交互式学习系统",
    version="0.1.0",
    validation_mode=ValidationMode.TEST_FILE,
    exercises_dir="exercises",
    tests_dir="tests",
    solutions_dir="solutions",
    project_root=Path(__file__).parent.parent,
    chapters={
        "01_basics": "第1章：基础概念",
        "02_microeconomics": "第2章：微观经济学",
        "03_macroeconomics": "第3章：宏观经济学",
        "04_finance": "第4章：金融经济学",
        "05_econometrics": "第5章：计量经济学",
        "06_advanced": "第6章：高级模型",
        "07_international": "第7章：国际经济学",
        "08_public": "第8章：公共经济学",
        "09_behavioral": "第9章：行为经济学",
        "10_development": "第10章：发展经济学",
    },
    banner="""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███████╗ ██████╗ ██████╗ ███╗   ██╗ ██████╗            ║
    ║   ██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔═══██╗           ║
    ║   █████╗  ██║     ██║   ██║██╔██╗ ██║██║   ██║           ║
    ║   ██╔══╝  ██║     ██║   ██║██║╚██╗██║██║   ██║           ║
    ║   ███████╗╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝           ║
    ║   ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝            ║
    ║                                                           ║
    ║   ███╗   ███╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗      ║
    ║   ████╗ ████║██║     ██║████╗  ██║██╔════╝ ██╔════╝      ║
    ║   ██╔████╔██║██║     ██║██╔██╗ ██║██║  ███╗███████╗      ║
    ║   ██║╚██╔╝██║██║     ██║██║╚██╗██║██║   ██║╚════██║      ║
    ║   ██║ ╚═╝ ██║███████╗██║██║ ╚████║╚██████╔╝███████║      ║
    ║   ╚═╝     ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝      ║
    ║                                                           ║
    ║           经济学交互式学习系统 v0.1.0                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """,
)
