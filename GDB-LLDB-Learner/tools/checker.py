#!/usr/bin/env python3
"""
通用练习验证工具
检查程序是否正确编译和运行
"""

import os
import sys
import subprocess
from pathlib import Path

def check_compilation(source_file, executable):
    """检查程序是否能正确编译"""
    print(f"[1/3] 检查编译...")

    if not os.path.exists(source_file):
        print(f"  ✗ 源文件不存在: {source_file}")
        return False

    # 尝试编译
    try:
        result = subprocess.run(
            ["gcc", "-g", "-Wall", "-Wextra", source_file, "-o", executable],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"  ✗ 编译失败:")
            print(result.stderr)
            return False

        print(f"  ✓ 编译成功")
        return True

    except subprocess.TimeoutExpired:
        print(f"  ✗ 编译超时")
        return False
    except FileNotFoundError:
        print(f"  ✗ gcc 未找到，请确保已安装 GCC")
        return False

def check_executable(executable):
    """检查可执行文件是否存在且包含调试信息"""
    print(f"[2/3] 检查可执行文件...")

    if not os.path.exists(executable):
        print(f"  ✗ 可执行文件不存在: {executable}")
        return False

    # 检查是否包含调试信息
    try:
        result = subprocess.run(
            ["file", executable],
            capture_output=True,
            text=True
        )

        if "not stripped" in result.stdout or "with debug" in result.stdout:
            print(f"  ✓ 可执行文件包含调试信息")
            return True
        else:
            print(f"  ⚠ 警告: 可执行文件可能不包含调试信息")
            print(f"     请使用 -g 选项编译")
            return True  # 仍然允许继续

    except FileNotFoundError:
        print(f"  ⚠ 无法检查调试信息（file 命令未找到）")
        return True

def check_run(executable, expected_exit_code=0):
    """检查程序是否能正常运行"""
    print(f"[3/3] 检查运行...")

    try:
        result = subprocess.run(
            [f"./{executable}"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == expected_exit_code:
            print(f"  ✓ 程序正常运行（退出码: {result.returncode}）")
            return True
        else:
            print(f"  ⚠ 程序退出码: {result.returncode} (期望: {expected_exit_code})")
            return True  # 某些练习的程序可能故意有错误

    except subprocess.TimeoutExpired:
        print(f"  ✗ 程序运行超时")
        return False

def main():
    if len(sys.argv) < 3:
        print("用法: python3 checker.py <source_file> <executable>")
        print("示例: python3 checker.py hello.c hello")
        sys.exit(1)

    source_file = sys.argv[1]
    executable = sys.argv[2]

    print("\n" + "="*60)
    print("GDB/LLDB 练习验证工具")
    print("="*60 + "\n")

    checks = [
        check_compilation(source_file, executable),
        check_executable(executable),
        check_run(executable)
    ]

    print("\n" + "="*60)
    if all(checks):
        print("✓ 所有检查通过！")
        print("="*60)
        print("\n你可以继续进行调试练习了。")
        print(f"运行: gdb ./{executable}")
        print(f"或:   lldb ./{executable}\n")
        sys.exit(0)
    else:
        print("✗ 部分检查未通过")
        print("="*60)
        print("\n请修复上述问题后再试。\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
