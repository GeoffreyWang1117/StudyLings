"""
Project-specific configuration for Vulkanlings.
"""

import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

_project_root = Path(__file__).parent.parent

# Try to find build directory
_build_dir = None
for candidate in ["build", "cmake-build-debug", "cmake-build-release"]:
    candidate_path = _project_root / candidate
    if candidate_path.exists():
        _build_dir = str(candidate_path)
        break

# Allow override via environment variable
_build_dir = os.environ.get("VULKANLINGS_BUILD_DIR", _build_dir)

config = ProjectConfig(
    name="vulkanlings",
    display_name="Vulkanlings - Vulkan 交互式学习系统",
    version="1.0.0",
    validation_mode=ValidationMode.COMPILE_AND_RUN,
    exercises_dir="exercises",
    project_root=_project_root,
    chapters={
        "00_intro": "Vulkan 概述与环境配置",
        "01_instance": "创建 Vulkan 实例",
        "02_physical_device": "选择物理设备",
        "03_logical_device": "创建逻辑设备与队列",
        "04_surface": "创建窗口表面",
        "05_swapchain": "配置交换链",
        "06_image_views": "创建图像视图",
        "07_render_pass": "配置渲染通道",
        "08_pipeline": "创建图形管线",
        "09_framebuffers": "创建帧缓冲",
        "10_command_buffers": "命令缓冲与命令池",
        "11_sync": "同步机制",
        "12_triangle": "渲染三角形",
        "13_vertex_buffers": "顶点缓冲",
        "14_index_buffers": "索引缓冲",
        "15_uniforms": "Uniform 缓冲对象",
        "16_textures": "纹理映射",
        "17_depth": "深度缓冲",
        "18_model_loading": "模型加载",
        "19_lighting": "Blinn-Phong 光照",
    },
    banner="""
     __      __    _ _                  _ _
     \\ \\    / /   | | |                | (_)
      \\ \\  / /   _| | | ____ _ _ __   | |_ _ __   __ _ ___
       \\ \\/ / | | | | |/ / _` | '_ \\  | | | '_ \\ / _` / __|
        \\  /| |_| | |   < (_| | | | | | | | | | | (_| \\__ \\
         \\/  \\__,_|_|_|\\_\\__,_|_| |_| |_|_|_| |_|\\__, |___/
                                                  __/ |
                                                 |___/

              Vulkan 交互式学习系统 v1.0.0
    """,
    file_extension=".cpp",
    build_command="make",
    build_dir=_build_dir,
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=[],
    placeholder_markers=["/* ??? */"],
    run_timeout=10,
)
