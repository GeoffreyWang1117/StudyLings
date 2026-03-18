"""
Project-specific configuration for Genlings (Gen-AI-Study).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

config = ProjectConfig(
    name="genailings",
    display_name="Genlings - 生成式AI算法交互式学习系统",
    version="0.1.0",
    validation_mode=ValidationMode.VERIFY_FUNC,
    exercises_dir="exercises",
    project_root=Path(__file__).parent.parent,
    chapters={
        "00_basics": "00 基础知识",
        "01_text": "01 文本生成基础",
        "02_attention": "02 注意力机制",
        "03_transformer": "03 Transformer",
        "04_gpt": "04 GPT",
        "05_image": "05 图像生成基础",
        "06_vae": "06 VAE",
        "07_gan": "07 GAN",
        "08_diffusion": "08 Diffusion",
        "09_multimodal": "09 多模态基础",
        "10_clip": "10 CLIP",
        "11_stable_diffusion": "11 Stable Diffusion",
        "12_llm_advanced": "12 LLM 进阶",
    },
    banner=r"""
     ██████╗ ███████╗███╗   ██╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ██╔════╝ ██╔════╝████╗  ██║██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██║  ███╗█████╗  ██╔██╗ ██║██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║   ██║██╔══╝  ██║╚██╗██║██║     ██║██║╚██╗██║██║   ██║╚════██║
    ╚██████╔╝███████╗██║ ╚████║███████╗██║██║ ╚████║╚██████╔╝███████║
     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

                生成式AI算法交互式学习系统 v0.1.0
    """,
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
    placeholder_markers=["___"],
)
