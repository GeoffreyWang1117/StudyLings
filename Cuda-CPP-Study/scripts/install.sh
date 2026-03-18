#!/bin/bash

# CUDAlings 安装脚本

set -e

echo "=================================="
echo "CUDAlings 安装脚本"
echo "=================================="

# 检查 CUDA
echo ""
echo "检查 CUDA 安装..."
if command -v nvcc &> /dev/null; then
    CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | cut -d',' -f1)
    echo "✓ 找到 CUDA $CUDA_VERSION"
else
    echo "✗ 未找到 CUDA"
    echo ""
    echo "请先安装 CUDA Toolkit:"
    echo "https://developer.nvidia.com/cuda-downloads"
    exit 1
fi

# 检查 CMake
echo ""
echo "检查 CMake..."
if command -v cmake &> /dev/null; then
    CMAKE_VERSION=$(cmake --version | head -n1 | awk '{print $3}')
    echo "✓ 找到 CMake $CMAKE_VERSION"
else
    echo "✗ 未找到 CMake"
    echo "正在安装 CMake..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y cmake
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cmake
    else
        echo "请手动安装 CMake: https://cmake.org/download/"
        exit 1
    fi
fi

# 创建构建目录
echo ""
echo "创建构建目录..."
mkdir -p build
cd build

# 配置
echo ""
echo "配置项目..."
cmake ..

# 编译
echo ""
echo "编译..."
make -j$(nproc)

# 测试
echo ""
echo "测试安装..."
if [ -f "./cudalings" ]; then
    echo "✓ cudalings 编译成功"
else
    echo "✗ 编译失败"
    exit 1
fi

# 安装 (可选)
echo ""
read -p "是否安装到系统路径? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo make install
    echo "✓ 已安装到系统路径"
    echo "现在可以在任何地方运行 'cudalings'"
else
    echo "跳过系统安装"
    echo "运行 './build/cudalings' 来使用"
fi

echo ""
echo "=================================="
echo "安装完成！"
echo "=================================="
echo ""
echo "快速开始:"
echo "  cd build"
echo "  ./cudalings list    # 查看所有练习"
echo "  ./cudalings run     # 开始学习"
echo "  ./cudalings watch   # 监视模式"
echo ""
echo "查看文档: docs/GETTING_STARTED.md"
echo ""
echo "祝学习愉快！ 🚀"
