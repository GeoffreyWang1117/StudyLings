# Vulkanlings 🌋

一个类似 rustlings 的 Vulkan 学习系统，通过渐进式填空练习帮助你掌握 Vulkan 图形编程。

## 项目简介

Vulkanlings 是一个交互式 Vulkan 学习工具，包含 20 个由浅入深的练习题和一个完整的最终项目。每个练习都是一个不完整的 C++ 程序，你需要填写缺失的代码使其正确编译和运行。

## 学习路径

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Vulkanlings 学习路径                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🟢 基础阶段 (00-06)                                                     │
│  ├── 00_intro          - Vulkan 概述与环境配置                           │
│  ├── 01_instance       - 创建 Vulkan 实例                                │
│  ├── 02_physical_device - 选择物理设备（GPU）                            │
│  ├── 03_logical_device  - 创建逻辑设备与队列                             │
│  ├── 04_surface         - 创建窗口表面                                   │
│  ├── 05_swapchain       - 配置交换链                                     │
│  └── 06_image_views     - 创建图像视图                                   │
│                                                                          │
│  🟡 中级阶段 (07-12)                                                     │
│  ├── 07_render_pass     - 配置渲染通道                                   │
│  ├── 08_pipeline        - 创建图形管线                                   │
│  ├── 09_framebuffers    - 创建帧缓冲                                     │
│  ├── 10_command_buffers - 命令缓冲与命令池                               │
│  ├── 11_sync            - 同步机制（信号量与栅栏）                        │
│  └── 12_triangle        - 🔺 渲染你的第一个三角形！                       │
│                                                                          │
│  🔴 高级阶段 (13-19)                                                     │
│  ├── 13_vertex_buffers  - 顶点缓冲与暂存缓冲                             │
│  ├── 14_index_buffers   - 索引缓冲                                       │
│  ├── 15_uniforms        - Uniform 缓冲对象                               │
│  ├── 16_textures        - 纹理映射与采样器                               │
│  ├── 17_depth           - 深度缓冲与测试                                 │
│  ├── 18_model_loading   - 加载 OBJ 模型                                  │
│  └── 19_lighting        - Blinn-Phong 光照                               │
│                                                                          │
│  🏆 最终项目                                                             │
│  └── Minimal Vulkan Renderer - 完整的轻量实时渲染引擎                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 环境要求

- **编译器**: GCC 9+ 或 Clang 10+ (支持 C++17)
- **Vulkan SDK**: 1.2.0+
- **GLFW**: 3.3+
- **GLM**: 0.9.9+
- **CMake**: 3.16+

### Ubuntu/Debian 安装

```bash
# 安装 Vulkan SDK
wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo apt-key add -
sudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-focal.list \
    https://packages.lunarg.com/vulkan/lunarg-vulkan-focal.list
sudo apt update
sudo apt install vulkan-sdk

# 安装依赖
sudo apt install libglfw3-dev libglm-dev cmake build-essential
```

### Arch Linux 安装

```bash
sudo pacman -S vulkan-devel glfw-x11 glm cmake
```

### macOS 安装

```bash
brew install vulkan-sdk glfw glm cmake
```

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/your-repo/Vulkan-Study.git
cd Vulkan-Study

# 构建项目
mkdir build && cd build
cmake ..
make

# 运行 vulkanlings
./vulkanlings

# 或运行特定练习
./vulkanlings run 01_instance
./vulkanlings verify 01_instance
```

## 使用方法

### 命令列表

```bash
vulkanlings list              # 列出所有练习
vulkanlings run <exercise>    # 运行指定练习
vulkanlings verify <exercise> # 验证练习是否正确
vulkanlings hint <exercise>   # 获取提示
vulkanlings watch             # 监视模式，自动检测文件变化
vulkanlings reset <exercise>  # 重置练习到初始状态
```

### 练习格式

每个练习文件包含 `// TODO:` 注释，标记需要填写的代码位置：

```cpp
// TODO: 创建 Vulkan 实例
// 提示: 使用 vkCreateInstance 函数
VkInstanceCreateInfo createInfo{};
createInfo.sType = /* ??? */;  // 填写正确的结构体类型
```

填写正确的代码后：

```cpp
VkInstanceCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
```

## 练习详解

### 第一阶段：Vulkan 基础 (00-06)

这个阶段学习 Vulkan 的基本概念和初始化流程：

| 练习 | 难度 | 描述 |
|------|------|------|
| 00_intro | ⭐ | 理解 Vulkan 架构，配置开发环境 |
| 01_instance | ⭐ | 创建 Vulkan 实例，启用验证层 |
| 02_physical_device | ⭐⭐ | 枚举和选择 GPU |
| 03_logical_device | ⭐⭐ | 创建逻辑设备和队列 |
| 04_surface | ⭐⭐ | 创建窗口表面 |
| 05_swapchain | ⭐⭐⭐ | 配置交换链 |
| 06_image_views | ⭐⭐ | 创建图像视图 |

### 第二阶段：渲染管线 (07-12)

学习 Vulkan 渲染管线的核心概念：

| 练习 | 难度 | 描述 |
|------|------|------|
| 07_render_pass | ⭐⭐⭐ | 配置渲染通道和附件 |
| 08_pipeline | ⭐⭐⭐⭐ | 创建图形管线 |
| 09_framebuffers | ⭐⭐ | 创建帧缓冲 |
| 10_command_buffers | ⭐⭐⭐ | 命令缓冲录制 |
| 11_sync | ⭐⭐⭐ | 同步原语 |
| 12_triangle | ⭐⭐⭐ | 渲染第一个三角形 |

### 第三阶段：高级技术 (13-19)

掌握实际渲染中需要的高级技术：

| 练习 | 难度 | 描述 |
|------|------|------|
| 13_vertex_buffers | ⭐⭐⭐ | 顶点数据管理 |
| 14_index_buffers | ⭐⭐⭐ | 索引绘制 |
| 15_uniforms | ⭐⭐⭐⭐ | 描述符和 Uniform 缓冲 |
| 16_textures | ⭐⭐⭐⭐ | 纹理加载与采样 |
| 17_depth | ⭐⭐⭐ | 深度测试 |
| 18_model_loading | ⭐⭐⭐⭐ | OBJ 模型加载 |
| 19_lighting | ⭐⭐⭐⭐⭐ | Blinn-Phong 光照模型 |

## 最终项目：Minimal Vulkan Renderer

完成所有练习后，你将实现一个完整的轻量渲染引擎：

```
final_project/minimal_renderer/
├── src/
│   ├── main.cpp              # 程序入口
│   ├── VulkanRenderer.cpp    # 渲染器核心
│   ├── Pipeline.cpp          # 管线管理
│   ├── Buffer.cpp            # 缓冲管理
│   ├── Texture.cpp           # 纹理管理
│   └── Model.cpp             # 模型加载
├── shaders/
│   ├── shader.vert           # 顶点着色器
│   ├── shader.frag           # 片段着色器
│   ├── blur.frag             # 高斯模糊
│   └── bloom.frag            # Bloom 效果
└── assets/
    └── models/               # 3D 模型
```

### 功能特性

- ✅ 完整的 Vulkan 渲染管线
- ✅ OBJ 模型加载
- ✅ 纹理映射
- ✅ Blinn-Phong 光照
- ✅ 后期处理（高斯模糊/Bloom）
- ✅ Vulkan Validation Layer 集成
- ✅ 性能监控

## 项目架构

```
┌──────────────────────────────────────────────────────────────────┐
│                     Minimal Vulkan Renderer                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐           │
│  │   Window    │    │   Input     │    │   Timer     │           │
│  │   (GLFW)    │    │   Handler   │    │   System    │           │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘           │
│         │                  │                  │                   │
│         └────────────────┬─┴──────────────────┘                   │
│                          ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                    VulkanRenderer                          │   │
│  │  ┌─────────────┬─────────────┬─────────────┬────────────┐ │   │
│  │  │  Instance   │   Device    │  Swapchain  │  Pipeline  │ │   │
│  │  └─────────────┴─────────────┴─────────────┴────────────┘ │   │
│  │  ┌─────────────┬─────────────┬─────────────┬────────────┐ │   │
│  │  │  Commands   │    Sync     │   Buffers   │  Textures  │ │   │
│  │  └─────────────┴─────────────┴─────────────┴────────────┘ │   │
│  └───────────────────────────────────────────────────────────┘   │
│                          │                                        │
│                          ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                    Render Loop                             │   │
│  │                                                            │   │
│  │  1. Acquire Image ──► 2. Record Commands ──► 3. Submit    │   │
│  │         │                     │                    │       │   │
│  │         ▼                     ▼                    ▼       │   │
│  │  ┌───────────┐         ┌───────────┐        ┌──────────┐  │   │
│  │  │ Semaphore │         │  Render   │        │  Queue   │  │   │
│  │  │  Signal   │         │   Pass    │        │  Submit  │  │   │
│  │  └───────────┘         └───────────┘        └──────────┘  │   │
│  │         │                                          │       │   │
│  │         └──────────────────────────────────────────┘       │   │
│  │                          │                                 │   │
│  │                          ▼                                 │   │
│  │                    4. Present Image                        │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## 许可证

MIT License

## 参考资料

- [Vulkan Tutorial](https://vulkan-tutorial.com/)
- [Vulkan Specification](https://www.khronos.org/registry/vulkan/specs/)
- [Vulkan Guide](https://vkguide.dev/)
- [Vulkan Samples](https://github.com/KhronosGroup/Vulkan-Samples)
