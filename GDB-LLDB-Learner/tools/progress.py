#!/usr/bin/env python3
"""
GDB/LLDB 学习进度追踪工具
"""

import os
import json
import sys
from pathlib import Path

PROGRESS_FILE = os.path.expanduser("~/.gdb_lldb_learner_progress.json")

def load_progress():
    """加载学习进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    """保存学习进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def mark_complete(level, exercise):
    """标记练习为完成"""
    progress = load_progress()
    key = f"level-{level:02d}-exercise-{exercise}"
    progress[key] = {
        "completed": True,
        "timestamp": str(Path(PROGRESS_FILE).stat().st_mtime if os.path.exists(PROGRESS_FILE) else 0)
    }
    save_progress(progress)
    print(f"✓ 已标记 Level {level} Exercise {exercise} 为完成")

def show_progress():
    """显示学习进度"""
    progress = load_progress()

    levels = {
        1: "调试器入门",
        2: "断点管理",
        3: "程序执行控制",
        4: "变量检查与修改",
        5: "调用栈分析",
        6: "多线程调试",
        7: "内存和数据结构",
        8: "Core Dump 分析",
        9: "高级调试技巧"
    }

    print("\n" + "="*60)
    print("GDB/LLDB 学习进度")
    print("="*60)

    total_exercises = 27  # 9 levels × 3 exercises
    completed = len(progress)

    print(f"\n总体进度: {completed}/{total_exercises} ({completed*100//total_exercises}%)")
    print("\n各级别进度:")
    print("-"*60)

    for level in range(1, 10):
        level_name = levels.get(level, f"Level {level}")
        exercises_completed = sum(1 for key in progress if key.startswith(f"level-{level:02d}"))
        status = "✓" if exercises_completed == 3 else "○"
        progress_bar = "█" * exercises_completed + "░" * (3 - exercises_completed)
        print(f"{status} Level {level}: {level_name:20s} [{progress_bar}] {exercises_completed}/3")

    print("="*60)
    print("\n提示: 使用 'python3 tools/progress.py mark <level> <exercise>' 标记完成")
    print("      例如: python3 tools/progress.py mark 1 1\n")

def reset_progress():
    """重置学习进度"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("✓ 学习进度已重置")
    else:
        print("没有找到进度记录")

def main():
    if len(sys.argv) < 2:
        show_progress()
        return

    command = sys.argv[1]

    if command == "mark" and len(sys.argv) >= 4:
        level = int(sys.argv[2])
        exercise = int(sys.argv[3])
        mark_complete(level, exercise)
        show_progress()
    elif command == "show":
        show_progress()
    elif command == "reset":
        reset_progress()
    else:
        print("用法:")
        print("  python3 tools/progress.py              # 显示进度")
        print("  python3 tools/progress.py show         # 显示进度")
        print("  python3 tools/progress.py mark <level> <exercise>  # 标记完成")
        print("  python3 tools/progress.py reset        # 重置进度")

if __name__ == "__main__":
    main()
