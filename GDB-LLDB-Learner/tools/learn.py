#!/usr/bin/env python3
"""
GDB/LLDB 交互式学习工具
帮助用户导航和学习各个级别的内容
"""

import os
import sys
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print("=" * 60)

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def get_project_root():
    """获取项目根目录"""
    current = Path(__file__).resolve().parent.parent
    return current

def list_levels():
    """列出所有级别"""
    levels = {
        1: ("调试器入门", "启动、退出、查看代码"),
        2: ("断点管理", "设置、删除、条件断点"),
        3: ("程序执行控制", "step、next、finish"),
        4: ("变量检查与修改", "打印、修改变量"),
        5: ("调用栈分析", "backtrace、frame"),
        6: ("多线程调试", "线程切换、线程断点"),
        7: ("内存和数据结构", "内存检查、数组、指针"),
        8: ("Core Dump 分析", "分析崩溃程序"),
        9: ("高级调试技巧", "优化代码、远程调试")
    }

    print_header("GDB & LLDB 学习路径")

    for level, (name, desc) in levels.items():
        print(f"\n{Colors.BOLD}Level {level}: {name}{Colors.END}")
        print(f"  {desc}")

    print("\n" + "=" * 60)
    print("\n使用方法:")
    print(f"  python3 tools/learn.py start <level>  # 开始某个级别")
    print(f"  python3 tools/learn.py list           # 列出所有级别")
    print()

def start_level(level):
    """开始某个级别的学习"""
    root = get_project_root()
    level_dir = root / "exercises" / f"level-{level:02d}-*"

    # 查找级别目录
    import glob
    matches = glob.glob(str(level_dir))

    if not matches:
        print_warning(f"Level {level} 不存在或尚未实现")
        return

    level_path = Path(matches[0])
    readme_path = level_path / "README.md"

    print_header(f"Level {level}: {level_path.name.split('-', 2)[2]}")

    # 读取 README
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取学习目标部分
        if "## 学习目标" in content:
            start = content.find("## 学习目标")
            end = content.find("##", start + 10)
            if end == -1:
                end = len(content)
            print(content[start:end].strip())

    # 列出练习
    exercises = sorted(level_path.glob("exercise-*"))

    if exercises:
        print_header("可用练习")
        for i, ex in enumerate(exercises, 1):
            problem_md = ex / "problem.md"
            if problem_md.exists():
                # 读取练习标题
                with open(problem_md, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.replace('#', '').strip()
                print(f"\n{Colors.BOLD}{i}. {title}{Colors.END}")
                print(f"   目录: {ex.relative_to(root)}")
            else:
                print(f"\n{i}. Exercise {i}")
                print(f"   目录: {ex.relative_to(root)}")

    print("\n" + "=" * 60)
    print_info("开始练习:")
    print(f"  1. cd {exercises[0].relative_to(root) if exercises else level_path}")
    print(f"  2. 阅读 problem.md")
    print(f"  3. make")
    print(f"  4. gdb ./program 或 lldb ./program")
    print()

    # 提供快捷方式
    if exercises:
        print_info("快捷命令:")
        print(f"  cd {exercises[0].relative_to(root)} && cat problem.md")
        print()

def show_cheatsheet():
    """显示命令速查表"""
    print_header("常用命令速查表")

    commands = [
        ("启动/退出", "gdb program", "lldb program"),
        ("", "quit", "quit"),
        ("运行", "run", "run"),
        ("断点", "break main", "b main"),
        ("", "break file.c:10", "b file.c:10"),
        ("执行", "step", "step"),
        ("", "next", "next"),
        ("", "continue", "continue"),
        ("变量", "print var", "p var"),
        ("", "info locals", "fr v"),
        ("调用栈", "backtrace", "bt"),
        ("", "frame 2", "f 2"),
        ("线程", "info threads", "thread list"),
        ("", "thread 2", "t 2"),
    ]

    print(f"\n{Colors.BOLD}{'功能':<12} {'GDB':<20} {'LLDB':<20}{Colors.END}")
    print("-" * 60)

    for cmd in commands:
        category, gdb, lldb = cmd
        if category:
            print(f"{Colors.YELLOW}{category:<12}{Colors.END} {gdb:<20} {lldb:<20}")
        else:
            print(f"{'':12} {gdb:<20} {lldb:<20}")

    print("\n" + "=" * 60)
    print_info("完整命令对照表: docs/gdb-lldb-commands.md")
    print()

def show_menu():
    """显示主菜单"""
    print_header("GDB & LLDB 交互式学习工具")

    options = [
        "1. 查看所有级别",
        "2. 开始学习特定级别",
        "3. 查看命令速查表",
        "4. 查看学习进度",
        "5. 退出"
    ]

    for opt in options:
        print(f"  {opt}")

    print("\n" + "=" * 60)

    choice = input("请选择 (1-5): ").strip()

    if choice == "1":
        list_levels()
        input("\n按回车继续...")
        show_menu()
    elif choice == "2":
        level = input("请输入级别编号 (1-9): ").strip()
        try:
            start_level(int(level))
        except ValueError:
            print_warning("无效的级别编号")
        input("\n按回车继续...")
        show_menu()
    elif choice == "3":
        show_cheatsheet()
        input("\n按回车继续...")
        show_menu()
    elif choice == "4":
        os.system("python3 tools/progress.py")
        input("\n按回车继续...")
        show_menu()
    elif choice == "5":
        print_success("祝学习愉快！")
        sys.exit(0)
    else:
        print_warning("无效的选择")
        show_menu()

def main():
    if len(sys.argv) < 2:
        # 交互模式
        show_menu()
    else:
        command = sys.argv[1]

        if command == "list":
            list_levels()
        elif command == "start" and len(sys.argv) >= 3:
            try:
                level = int(sys.argv[2])
                start_level(level)
            except ValueError:
                print_warning("无效的级别编号")
        elif command == "cheatsheet":
            show_cheatsheet()
        else:
            print("用法:")
            print("  python3 tools/learn.py              # 交互模式")
            print("  python3 tools/learn.py list         # 列出所有级别")
            print("  python3 tools/learn.py start <N>    # 开始 Level N")
            print("  python3 tools/learn.py cheatsheet   # 显示命令速查表")

if __name__ == "__main__":
    main()
