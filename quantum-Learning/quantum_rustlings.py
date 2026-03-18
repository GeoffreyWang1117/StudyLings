#!/usr/bin/env python3
"""
Quantum Rustlings - 量子编程学习系统
类似 rustlings 的交互式量子计算学习工具
"""

import os
import sys
import subprocess
import toml
from pathlib import Path
from typing import List, Dict
import argparse


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class QuantumRustlings:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.info_file = self.root_dir / "info.toml"
        self.progress_file = self.root_dir / ".progress"
        self.exercises = self.load_exercises()
        self.progress = self.load_progress()

    def load_exercises(self) -> List[Dict]:
        """加载练习题配置"""
        if not self.info_file.exists():
            print(f"{Colors.RED}错误: 找不到 info.toml 文件{Colors.END}")
            sys.exit(1)

        data = toml.load(self.info_file)
        return data.get('exercises', [])

    def load_progress(self) -> set:
        """加载学习进度"""
        if not self.progress_file.exists():
            return set()

        with open(self.progress_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())

    def save_progress(self):
        """保存学习进度"""
        with open(self.progress_file, 'w') as f:
            for name in sorted(self.progress):
                f.write(f"{name}\n")

    def run_exercise(self, exercise: Dict) -> bool:
        """运行单个练习"""
        exercise_path = self.root_dir / exercise['path']

        if not exercise_path.exists():
            print(f"{Colors.RED}错误: 找不到文件 {exercise_path}{Colors.END}")
            return False

        # 运行测试
        result = subprocess.run(
            [sys.executable, str(exercise_path)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ {exercise['name']} 通过！{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ {exercise['name']} 失败{Colors.END}")
            if result.stdout:
                print(f"\n{Colors.YELLOW}输出:{Colors.END}")
                print(result.stdout)
            if result.stderr:
                print(f"\n{Colors.RED}错误:{Colors.END}")
                print(result.stderr)
            return False

    def show_hint(self, exercise: Dict):
        """显示提示"""
        print(f"\n{Colors.CYAN}💡 提示:{Colors.END}")
        print(exercise.get('hint', '暂无提示'))
        print()

    def list_exercises(self):
        """列出所有练习"""
        print(f"\n{Colors.BOLD}Quantum Rustlings - 练习列表{Colors.END}\n")

        current_section = None
        for i, ex in enumerate(self.exercises, 1):
            # 检测章节变化
            section = ex['path'].split('/')[1]
            if section != current_section:
                current_section = section
                print(f"\n{Colors.BOLD}{Colors.BLUE}━━━ {section.upper()} ━━━{Colors.END}")

            status = f"{Colors.GREEN}✓{Colors.END}" if ex['name'] in self.progress else f"{Colors.YELLOW}○{Colors.END}"
            print(f"{status} {i:2d}. {ex['name']}")

        completed = len(self.progress)
        total = len(self.exercises)
        percentage = (completed / total * 100) if total > 0 else 0

        print(f"\n{Colors.BOLD}进度: {completed}/{total} ({percentage:.1f}%){Colors.END}")
        print()

    def get_next_exercise(self) -> Dict:
        """获取下一个未完成的练习"""
        for ex in self.exercises:
            if ex['name'] not in self.progress:
                return ex
        return None

    def watch_mode(self):
        """监视模式：自动运行下一个练习"""
        print(f"{Colors.BOLD}🚀 Quantum Rustlings - 开始学习！{Colors.END}\n")

        while True:
            next_ex = self.get_next_exercise()

            if not next_ex:
                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 恭喜！你已完成所有练习！{Colors.END}")
                print(f"{Colors.CYAN}你已经掌握了从基础到前沿的量子编程知识！{Colors.END}\n")
                break

            print(f"{Colors.BOLD}当前练习: {next_ex['name']}{Colors.END}")
            print(f"文件: {next_ex['path']}\n")

            if self.run_exercise(next_ex):
                self.progress.add(next_ex['name'])
                self.save_progress()
                print()
            else:
                self.show_hint(next_ex)
                print(f"{Colors.YELLOW}修改文件后，再次运行以继续...{Colors.END}")
                print(f"或使用 {Colors.BOLD}python quantum_rustlings.py hint{Colors.END} 查看提示\n")
                break

    def verify_all(self):
        """验证所有练习"""
        print(f"{Colors.BOLD}验证所有练习...{Colors.END}\n")

        passed = 0
        failed = 0

        for ex in self.exercises:
            if self.run_exercise(ex):
                passed += 1
            else:
                failed += 1

        print(f"\n{Colors.BOLD}结果: {Colors.GREEN}{passed} 通过{Colors.END}, {Colors.RED}{failed} 失败{Colors.END}\n")

    def reset_progress(self):
        """重置进度"""
        if self.progress_file.exists():
            self.progress_file.unlink()
        self.progress = set()
        print(f"{Colors.GREEN}进度已重置{Colors.END}")


def main():
    parser = argparse.ArgumentParser(description='Quantum Rustlings - 量子编程学习系统')
    parser.add_argument('command', nargs='?', default='watch',
                       choices=['watch', 'verify', 'list', 'reset', 'hint'],
                       help='命令: watch(默认) | verify | list | reset | hint')
    parser.add_argument('--exercise', '-e', help='指定练习名称')

    args = parser.parse_args()

    qr = QuantumRustlings()

    if args.command == 'watch':
        qr.watch_mode()
    elif args.command == 'verify':
        qr.verify_all()
    elif args.command == 'list':
        qr.list_exercises()
    elif args.command == 'reset':
        qr.reset_progress()
    elif args.command == 'hint':
        if args.exercise:
            ex = next((e for e in qr.exercises if e['name'] == args.exercise), None)
            if ex:
                qr.show_hint(ex)
            else:
                print(f"{Colors.RED}找不到练习: {args.exercise}{Colors.END}")
        else:
            next_ex = qr.get_next_exercise()
            if next_ex:
                qr.show_hint(next_ex)
            else:
                print(f"{Colors.GREEN}所有练习已完成！{Colors.END}")


if __name__ == '__main__':
    main()
