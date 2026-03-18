# 安装指南

本文档介绍如何在不同操作系统上安装 GDB 和 LLDB。

## Linux

### Ubuntu/Debian

```bash
# 安装 GDB
sudo apt-get update
sudo apt-get install gdb

# 安装 LLDB
sudo apt-get install lldb

# 安装开发工具
sudo apt-get install build-essential

# 验证安装
gdb --version
lldb --version
gcc --version
```

### Fedora/RHEL/CentOS

```bash
# 安装 GDB
sudo dnf install gdb

# 安装 LLDB
sudo dnf install lldb

# 安装开发工具
sudo dnf groupinstall "Development Tools"

# 验证安装
gdb --version
lldb --version
```

### Arch Linux

```bash
# 安装 GDB
sudo pacman -S gdb

# 安装 LLDB
sudo pacman -S lldb

# 安装开发工具
sudo pacman -S base-devel

# 验证安装
gdb --version
lldb --version
```

## macOS

### 使用 Homebrew

```bash
# 安装 Homebrew (如果还没有)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 GDB
brew install gdb

# LLDB 已经随 Xcode Command Line Tools 安装
xcode-select --install

# 验证安装
gdb --version
lldb --version
```

### GDB 代码签名（macOS 特殊要求）

在 macOS 上，GDB 需要代码签名才能调试程序。请参考：
https://sourceware.org/gdb/wiki/PermissionsDarwin

或者直接使用 LLDB，它是 macOS 的默认调试器。

## Windows

### 使用 WSL (推荐)

1. 安装 WSL2:
```powershell
wsl --install
```

2. 在 WSL 中安装 GDB/LLDB（参考 Linux 部分）

### 使用 MinGW-w64

1. 下载并安装 MinGW-w64: https://www.mingw-w64.org/

2. GDB 会随 MinGW-w64 一起安装

3. 将 MinGW-w64 的 bin 目录添加到 PATH

### 使用 MSYS2

```bash
# 安装 MSYS2: https://www.msys2.org/

# 在 MSYS2 终端中：
pacman -S mingw-w64-x86_64-gdb
pacman -S mingw-w64-x86_64-lldb
```

## 验证安装

运行以下命令验证安装是否成功：

```bash
# 检查 GDB
gdb --version
# 应该显示类似: GNU gdb (GDB) 12.1

# 检查 LLDB
lldb --version
# 应该显示类似: lldb version 14.0.0

# 检查 GCC
gcc --version
# 应该显示类似: gcc (GCC) 11.3.0

# 测试基本功能
echo 'int main(){return 0;}' > test.c
gcc -g test.c -o test
gdb ./test
# 应该能成功启动 GDB
```

## 配置调试器

### GDB 配置文件 (~/.gdbinit)

```bash
# 创建 GDB 配置文件
cat > ~/.gdbinit << 'EOF'
# 启用历史记录
set history save on
set history size 10000
set history filename ~/.gdb_history

# 美化输出
set print pretty on
set print array on
set print array-indexes on

# Intel 汇编语法（如果你喜欢）
set disassembly-flavor intel

# 启动时不显示版权信息
set startup-quietly on
EOF
```

### LLDB 配置文件 (~/.lldbinit)

```bash
# 创建 LLDB 配置文件
cat > ~/.lldbinit << 'EOF'
# 设置历史记录
settings set target.process.thread.step-avoid-regexp ^std::

# Intel 汇编语法
settings set target.x86-disassembly-flavor intel

# 常用别名
command alias bfl breakpoint set -f %1 -l %2
command alias rd register read
command alias wr register write
EOF
```

## Python 支持

GDB 和 LLDB 都支持 Python 脚本。

### 检查 Python 支持

```bash
# GDB
gdb -ex 'python print("GDB Python works!")' -ex quit

# LLDB
lldb -o 'script print("LLDB Python works!")' -o quit
```

### 安装 Python (如果需要)

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# 验证
python3 --version
```

## 常见问题

### GDB: "ptrace: Operation not permitted"

这通常发生在 Linux 上。解决方法：

```bash
# 临时解决
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope

# 永久解决
sudo sh -c 'echo "kernel.yama.ptrace_scope = 0" >> /etc/sysctl.d/10-ptrace.conf'
```

### macOS: "Unable to find Mach task port"

需要为 GDB 签名（参考上面的代码签名部分），或者使用 LLDB 代替。

### Windows: 找不到调试符号

确保：
1. 使用 `-g` 选项编译
2. 可执行文件和源代码在同一目录
3. 使用正确的调试器版本（匹配编译器）

## 额外工具（可选）

这些工具可以增强调试体验：

```bash
# Valgrind - 内存调试
sudo apt-get install valgrind

# GDB Dashboard - GDB 增强界面
wget -P ~ https://git.io/.gdbinit

# cgdb - GDB 的 curses 界面
sudo apt-get install cgdb
```

## 下一步

安装完成后，继续阅读 [快速开始](../README.md#快速开始) 开始学习！
