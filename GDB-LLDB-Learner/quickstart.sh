#!/bin/bash

# GDB/LLDB Learner 快速开始脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${CYAN}${1}${NC}"
    echo "============================================================"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# 检查依赖
check_dependencies() {
    print_header "检查依赖..."

    local missing=()

    # 检查 GCC
    if ! command -v gcc &> /dev/null; then
        missing+=("gcc")
    else
        print_success "GCC 已安装: $(gcc --version | head -n1)"
    fi

    # 检查 GDB
    if ! command -v gdb &> /dev/null; then
        print_warning "GDB 未安装"
        missing+=("gdb")
    else
        print_success "GDB 已安装: $(gdb --version | head -n1)"
    fi

    # 检查 LLDB
    if ! command -v lldb &> /dev/null; then
        print_warning "LLDB 未安装"
        missing+=("lldb")
    else
        print_success "LLDB 已安装: $(lldb --version | head -n1)"
    fi

    # 检查 Python3
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    else
        print_success "Python3 已安装: $(python3 --version)"
    fi

    if [ ${#missing[@]} -ne 0 ]; then
        print_error "缺少依赖: ${missing[*]}"
        echo ""
        echo "请安装缺少的依赖:"
        echo ""
        echo "Ubuntu/Debian:"
        echo "  sudo apt-get install gcc gdb lldb python3"
        echo ""
        echo "macOS:"
        echo "  brew install gcc gdb"
        echo "  xcode-select --install  # LLDB 随 Xcode 安装"
        echo ""
        echo "Fedora:"
        echo "  sudo dnf install gcc gdb lldb python3"
        echo ""
        return 1
    fi

    return 0
}

# 测试编译
test_compile() {
    print_header "测试编译功能..."

    # 创建临时测试文件
    local temp_dir=$(mktemp -d)
    local test_file="$temp_dir/test.c"

    cat > "$test_file" << 'EOF'
#include <stdio.h>
int main() {
    printf("Hello, Debugger!\n");
    return 0;
}
EOF

    if gcc -g "$test_file" -o "$temp_dir/test" 2>/dev/null; then
        print_success "编译测试通过"
        rm -rf "$temp_dir"
        return 0
    else
        print_error "编译测试失败"
        rm -rf "$temp_dir"
        return 1
    fi
}

# 显示快速开始指南
show_guide() {
    print_header "快速开始指南"

    cat << 'EOF'

欢迎来到 GDB & LLDB 学习系统！

📚 学习路径:
  Level 1-3: 基础调试命令（推荐新手从这里开始）
  Level 4-6: 中级调试技巧
  Level 7-9: 高级调试场景

🚀 开始学习:

  方式一：交互式工具
    python3 tools/learn.py

  方式二：直接开始 Level 1
    cd exercises/level-01-basics/exercise-1
    cat problem.md
    make
    gdb ./hello

  方式三：查看所有级别
    python3 tools/learn.py list

📖 有用的资源:
  - 命令对照表: docs/gdb-lldb-commands.md
  - 安装指南: docs/installation.md
  - 最佳实践: docs/best-practices.md

🔧 工具:
  - 进度追踪: python3 tools/progress.py
  - 验证工具: python3 tools/checker.py <source> <executable>
  - 学习助手: python3 tools/learn.py

💡 小贴士:
  1. 按顺序学习，打好基础
  2. 每个命令都要亲自尝试
  3. 对比学习 GDB 和 LLDB
  4. 记录笔记和常用命令
  5. 将学到的技能应用到实际项目

EOF

    print_success "环境准备就绪！"
    echo ""
    print_info "现在你可以开始学习了。建议从 Level 1 开始："
    echo ""
    echo "  cd exercises/level-01-basics/exercise-1"
    echo "  cat problem.md"
    echo ""
}

# 主函数
main() {
    cat << 'EOF'
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        GDB & LLDB 调试器学习系统                         ║
║        快速开始向导                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF

    if ! check_dependencies; then
        echo ""
        print_error "请先安装必需的依赖，然后重新运行此脚本"
        exit 1
    fi

    if ! test_compile; then
        echo ""
        print_error "编译测试失败，请检查开发环境"
        exit 1
    fi

    show_guide

    # 询问是否立即开始
    echo ""
    read -p "是否立即启动交互式学习工具？(y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 tools/learn.py
    else
        print_info "你随时可以运行 'python3 tools/learn.py' 启动学习工具"
    fi
}

main
