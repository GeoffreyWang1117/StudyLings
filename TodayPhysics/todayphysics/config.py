"""
Project-specific configuration for TodayPhysics.
"""

from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="todayphysics",
    display_name="Physics Rustlings - 通过编程学习物理学",
    version="1.0.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    solutions_dir="solutions",
    project_root=Path(__file__).parent.parent,
    chapters={
        "01_classical_mechanics": "经典力学 Classical Mechanics",
        "02_oscillations_waves": "振动与波 Oscillations & Waves",
        "03_electromagnetism": "电磁学 Electromagnetism",
        "04_thermodynamics": "热力学与统计物理 Thermodynamics & Statistical Physics",
        "05_special_relativity": "狭义相对论 Special Relativity",
        "06_general_relativity": "广义相对论 General Relativity",
        "07_quantum_mechanics": "量子力学 Quantum Mechanics",
        "08_advanced_quantum": "高等量子力学 Advanced Quantum Mechanics",
    },
    banner="""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ██████╗ ██╗  ██╗██╗   ██╗███████╗██╗ ██████╗███████╗    ║
    ║   ██╔══██╗██║  ██║╚██╗ ██╔╝██╔════╝██║██╔════╝██╔════╝    ║
    ║   ██████╔╝███████║ ╚████╔╝ ███████╗██║██║     ███████╗    ║
    ║   ██╔═══╝ ██╔══██║  ╚██╔╝  ╚════██║██║██║     ╚════██║    ║
    ║   ██║     ██║  ██║   ██║   ███████║██║╚██████╗███████║    ║
    ║   ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝ ╚═════╝╚══════╝    ║
    ║                                                            ║
    ║          通过编程学习物理学 v1.0.0                          ║
    ╚════════════════════════════════════════════════════════════╝
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
)
