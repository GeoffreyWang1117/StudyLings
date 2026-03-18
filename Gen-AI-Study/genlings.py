#!/usr/bin/env python3
"""
Genlings - 生成式AI算法填空练习
类似 Rustlings 的交互式学习工具
"""

import os
import sys
import json
import subprocess
import argparse
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum

# ANSI 颜色码
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class ExerciseStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class Exercise:
    name: str
    path: str
    category: str
    difficulty: int  # 1-5
    description: str
    hint: str

def color_print(text: str, color: str = Colors.WHITE, bold: bool = False):
    """打印彩色文本"""
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Colors.RESET}")

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗ ███████╗███╗   ██╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗  ║
    ║  ██╔════╝ ██╔════╝████╗  ██║██║     ██║████╗  ██║██╔════╝ ██╔════╝  ║
    ║  ██║  ███╗█████╗  ██╔██╗ ██║██║     ██║██╔██╗ ██║██║  ███╗███████╗  ║
    ║  ██║   ██║██╔══╝  ██║╚██╗██║██║     ██║██║╚██╗██║██║   ██║╚════██║  ║
    ║  ╚██████╔╝███████╗██║ ╚████║███████╗██║██║ ╚████║╚██████╔╝███████║  ║
    ║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝  ║
    ║                                                               ║
    ║           生成式AI算法填空练习 - 从基础到前沿                    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    color_print(banner, Colors.CYAN, bold=True)

def load_exercises(base_path: Path) -> list[Exercise]:
    """加载所有练习配置"""
    exercises = []
    config_path = base_path / "exercises.json"

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for ex in config['exercises']:
                exercises.append(Exercise(**ex))

    return exercises

def get_progress(base_path: Path) -> dict:
    """获取学习进度"""
    progress_path = base_path / ".genlings_progress.json"
    if progress_path.exists():
        with open(progress_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "current": None}

def save_progress(base_path: Path, progress: dict):
    """保存学习进度"""
    progress_path = base_path / ".genlings_progress.json"
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def check_exercise(exercise: Exercise, base_path: Path) -> tuple[bool, str]:
    """检查练习是否通过"""
    exercise_path = base_path / exercise.path

    if not exercise_path.exists():
        return False, f"练习文件不存在: {exercise.path}"

    # 检查是否还有 TODO 标记
    with open(exercise_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "# TODO:" in content or "# todo:" in content:
            return False, "练习中还有未完成的 TODO 标记"
        if "___" in content:
            return False, "练习中还有未填写的空白 (___)"

    # 尝试运行练习
    try:
        result = subprocess.run(
            [sys.executable, str(exercise_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(base_path)
        )

        if result.returncode == 0:
            return True, "练习通过!"
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, f"运行错误:\n{error_msg}"

    except subprocess.TimeoutExpired:
        return False, "运行超时 (60秒)"
    except Exception as e:
        return False, f"执行错误: {str(e)}"

def run_exercise(exercise: Exercise, base_path: Path):
    """运行单个练习"""
    color_print(f"\n{'='*60}", Colors.CYAN)
    color_print(f"练习: {exercise.name}", Colors.GREEN, bold=True)
    color_print(f"分类: {exercise.category} | 难度: {'★' * exercise.difficulty}{'☆' * (5-exercise.difficulty)}", Colors.YELLOW)
    color_print(f"{'='*60}", Colors.CYAN)
    color_print(f"\n{exercise.description}\n", Colors.WHITE)

    # 显示练习文件内容
    exercise_path = base_path / exercise.path
    if exercise_path.exists():
        color_print(f"文件: {exercise.path}", Colors.BLUE)
        color_print("-" * 40, Colors.BLUE)
        with open(exercise_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 高亮 TODO 和 ___
            for i, line in enumerate(content.split('\n'), 1):
                if 'TODO' in line or '___' in line:
                    color_print(f"{i:4d} | {line}", Colors.YELLOW)
                else:
                    print(f"{i:4d} | {line}")
        color_print("-" * 40, Colors.BLUE)

    # 检查练习
    passed, message = check_exercise(exercise, base_path)

    if passed:
        color_print(f"\n✓ {message}", Colors.GREEN, bold=True)
        return True
    else:
        color_print(f"\n✗ {message}", Colors.RED)
        color_print(f"\n💡 提示: {exercise.hint}", Colors.MAGENTA)
        return False

def watch_mode(exercises: list[Exercise], base_path: Path, progress: dict):
    """监视模式 - 自动检测文件变化"""
    color_print("\n👀 进入监视模式 - 保存文件后自动检查", Colors.CYAN, bold=True)
    color_print("按 Ctrl+C 退出\n", Colors.YELLOW)

    # 找到当前练习
    current_idx = 0
    if progress.get('current'):
        for i, ex in enumerate(exercises):
            if ex.name == progress['current']:
                current_idx = i
                break

    last_modified = {}

    try:
        while current_idx < len(exercises):
            exercise = exercises[current_idx]
            exercise_path = base_path / exercise.path

            if not exercise_path.exists():
                color_print(f"等待创建文件: {exercise.path}", Colors.YELLOW)
                time.sleep(1)
                continue

            current_mtime = exercise_path.stat().st_mtime

            if exercise.name not in last_modified or last_modified[exercise.name] != current_mtime:
                last_modified[exercise.name] = current_mtime

                # 清屏
                os.system('clear' if os.name != 'nt' else 'cls')
                print_banner()

                passed = run_exercise(exercise, base_path)

                if passed:
                    progress['completed'].append(exercise.name)
                    current_idx += 1
                    if current_idx < len(exercises):
                        progress['current'] = exercises[current_idx].name
                        color_print(f"\n🎉 进入下一个练习: {exercises[current_idx].name}", Colors.GREEN, bold=True)
                    else:
                        color_print("\n🏆 恭喜! 你已完成所有练习!", Colors.GREEN, bold=True)
                    save_progress(base_path, progress)
                else:
                    progress['current'] = exercise.name
                    save_progress(base_path, progress)

            time.sleep(0.5)

    except KeyboardInterrupt:
        color_print("\n\n退出监视模式", Colors.YELLOW)
        save_progress(base_path, progress)

def list_exercises(exercises: list[Exercise], progress: dict):
    """列出所有练习"""
    color_print("\n📚 练习列表\n", Colors.CYAN, bold=True)

    categories = {}
    for ex in exercises:
        if ex.category not in categories:
            categories[ex.category] = []
        categories[ex.category].append(ex)

    for category, exs in categories.items():
        color_print(f"\n【{category}】", Colors.BLUE, bold=True)
        for ex in exs:
            status = "✓" if ex.name in progress.get('completed', []) else " "
            current = "→" if ex.name == progress.get('current') else " "
            difficulty = '★' * ex.difficulty + '☆' * (5 - ex.difficulty)
            color = Colors.GREEN if status == "✓" else (Colors.YELLOW if current == "→" else Colors.WHITE)
            color_print(f"  [{status}]{current} {ex.name:<40} {difficulty}", color)

def show_hint(exercise_name: str, exercises: list[Exercise]):
    """显示练习提示"""
    for ex in exercises:
        if ex.name == exercise_name:
            color_print(f"\n💡 提示 - {ex.name}", Colors.MAGENTA, bold=True)
            color_print(f"\n{ex.hint}\n", Colors.WHITE)
            return
    color_print(f"未找到练习: {exercise_name}", Colors.RED)

def reset_progress(base_path: Path):
    """重置进度"""
    progress_path = base_path / ".genlings_progress.json"
    if progress_path.exists():
        progress_path.unlink()
    color_print("✓ 进度已重置", Colors.GREEN)

def main():
    parser = argparse.ArgumentParser(
        description="Genlings - 生成式AI算法填空练习",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # watch 命令
    watch_parser = subparsers.add_parser('watch', help='监视模式 - 自动检测文件变化')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有练习')

    # run 命令
    run_parser = subparsers.add_parser('run', help='运行指定练习')
    run_parser.add_argument('name', help='练习名称')

    # hint 命令
    hint_parser = subparsers.add_parser('hint', help='显示练习提示')
    hint_parser.add_argument('name', help='练习名称')

    # verify 命令
    verify_parser = subparsers.add_parser('verify', help='验证当前练习')

    # reset 命令
    reset_parser = subparsers.add_parser('reset', help='重置学习进度')

    args = parser.parse_args()

    # 获取基础路径
    base_path = Path(__file__).parent

    # 加载练习和进度
    exercises = load_exercises(base_path)
    progress = get_progress(base_path)

    if not exercises:
        color_print("错误: 未找到练习配置文件 exercises.json", Colors.RED)
        sys.exit(1)

    # 设置初始当前练习
    if not progress.get('current') and exercises:
        progress['current'] = exercises[0].name
        save_progress(base_path, progress)

    if args.command == 'watch':
        print_banner()
        watch_mode(exercises, base_path, progress)

    elif args.command == 'list':
        print_banner()
        list_exercises(exercises, progress)

    elif args.command == 'run':
        print_banner()
        for ex in exercises:
            if ex.name == args.name:
                run_exercise(ex, base_path)
                break
        else:
            color_print(f"未找到练习: {args.name}", Colors.RED)

    elif args.command == 'hint':
        show_hint(args.name, exercises)

    elif args.command == 'verify':
        print_banner()
        current = progress.get('current')
        if current:
            for ex in exercises:
                if ex.name == current:
                    passed = run_exercise(ex, base_path)
                    if passed:
                        # 更新进度到下一个
                        idx = exercises.index(ex)
                        if idx + 1 < len(exercises):
                            progress['current'] = exercises[idx + 1].name
                        progress['completed'].append(ex.name)
                        save_progress(base_path, progress)
                    break
        else:
            color_print("没有当前练习", Colors.YELLOW)

    elif args.command == 'reset':
        reset_progress(base_path)

    else:
        print_banner()
        color_print("\n使用方法:", Colors.CYAN)
        color_print("  python genlings.py watch   - 开始练习 (监视模式)", Colors.WHITE)
        color_print("  python genlings.py list    - 查看所有练习", Colors.WHITE)
        color_print("  python genlings.py verify  - 验证当前练习", Colors.WHITE)
        color_print("  python genlings.py hint <name> - 获取提示", Colors.WHITE)
        color_print("  python genlings.py reset   - 重置进度", Colors.WHITE)
        color_print("\n快速开始: python genlings.py watch\n", Colors.GREEN, bold=True)

if __name__ == "__main__":
    main()
