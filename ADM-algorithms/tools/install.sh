#!/bin/bash
# ADM Judge 安装脚本

set -e  # 遇到错误立即退出

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      ADM Judge - 安装脚本                                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 检测操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🔍 检测到操作系统: $MACHINE"
echo ""

# 检查依赖
echo "📦 检查依赖..."

# 检查 g++
if ! command -v g++ &> /dev/null; then
    echo "❌ 错误: 未找到 g++ 编译器"
    echo "   请安装 g++ (建议版本 7.0 或更高)"
    if [ "$MACHINE" == "Linux" ]; then
        echo "   Ubuntu/Debian: sudo apt-get install g++"
        echo "   Fedora/RHEL:   sudo dnf install gcc-c++"
    elif [ "$MACHINE" == "Mac" ]; then
        echo "   macOS: xcode-select --install"
    fi
    exit 1
fi

GCC_VERSION=$(g++ --version | head -n1)
echo "✓ 找到 g++: $GCC_VERSION"

# 检查 CMake
if ! command -v cmake &> /dev/null; then
    echo "❌ 错误: 未找到 CMake"
    echo "   请安装 CMake 3.15 或更高版本"
    if [ "$MACHINE" == "Linux" ]; then
        echo "   Ubuntu/Debian: sudo apt-get install cmake"
        echo "   Fedora/RHEL:   sudo dnf install cmake"
    elif [ "$MACHINE" == "Mac" ]; then
        echo "   macOS: brew install cmake"
    fi
    exit 1
fi

CMAKE_VERSION=$(cmake --version | head -n1)
echo "✓ 找到 CMake: $CMAKE_VERSION"

echo ""
echo "✅ 所有依赖检查完成！"
echo ""

# 构建项目
echo "🔨 开始构建 ADM Judge..."
echo ""

# 创建 build 目录
if [ -d "build" ]; then
    echo "⚠️  build 目录已存在，删除旧的构建..."
    rm -rf build
fi

mkdir build
cd build

# 运行 CMake
echo "⚙️  配置项目..."
cmake .. || {
    echo "❌ CMake 配置失败"
    exit 1
}

echo ""
echo "🔧 编译项目..."
make || {
    echo "❌ 编译失败"
    exit 1
}

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装成功！                                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 ADM Judge 已成功构建！"
echo ""
echo "📍 可执行文件位置: $(pwd)/adm-judge"
echo ""
echo "🚀 快速开始:"
echo "   cd build"
echo "   ./adm-judge"
echo ""
echo "💡 更多信息请查看: ../QUICKSTART.md"
echo ""
