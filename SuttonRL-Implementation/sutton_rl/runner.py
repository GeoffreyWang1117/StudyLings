"""
Main runner for Sutton RL exercises - Rustlings-style interface
"""
import argparse
import importlib.util
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict
import traceback

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = RED = YELLOW = CYAN = MAGENTA = BLUE = ""
    class Style:
        RESET_ALL = BRIGHT = ""

from sutton_rl.checker import ExerciseChecker
from sutton_rl.exercise_info import EXERCISE_LIST


class SuttonRLRunner:
    """Main runner for exercises"""

    def __init__(self, exercises_dir: Optional[Path] = None):
        if exercises_dir is None:
            self.exercises_dir = Path(__file__).parent.parent / "exercises"
        else:
            self.exercises_dir = Path(exercises_dir)

        self.checker = ExerciseChecker()

    def list_exercises(self):
        """List all available exercises"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}Sutton RL Exercises - 强化学习算法练习")
        print(f"{Fore.CYAN}{'='*70}\n")

        current_chapter = None
        for idx, exercise in enumerate(EXERCISE_LIST, 1):
            if exercise['chapter'] != current_chapter:
                current_chapter = exercise['chapter']
                print(f"\n{Fore.YELLOW}{Style.BRIGHT}{exercise['chapter_name']}")
                print(f"{Fore.YELLOW}{'-'*60}")

            status = "✓" if self._check_if_completed(exercise['id']) else "○"
            color = Fore.GREEN if status == "✓" else Fore.WHITE

            print(f"{color}{idx:2d}. [{status}] {exercise['id']:25s} - {exercise['name']}")

        print(f"\n{Fore.CYAN}总共 {len(EXERCISE_LIST)} 个练习")
        print(f"{Fore.CYAN}运行: python -m sutton_rl run <exercise_id>")
        print()

    def run_exercise(self, exercise_id: str, verbose: bool = True) -> bool:
        """Run a specific exercise"""
        exercise = self._find_exercise(exercise_id)
        if not exercise:
            print(f"{Fore.RED}错误: 找不到练习 '{exercise_id}'")
            print(f"{Fore.YELLOW}提示: 使用 'python -m sutton_rl list' 查看所有练习")
            return False

        exercise_path = self.exercises_dir / exercise['path']

        if not exercise_path.exists():
            print(f"{Fore.RED}错误: 练习文件不存在: {exercise_path}")
            return False

        if verbose:
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.CYAN}运行练习: {exercise['name']}")
            print(f"{Fore.CYAN}{'='*70}\n")
            print(f"{Fore.YELLOW}章节: {exercise['chapter_name']}")
            print(f"{Fore.YELLOW}文件: {exercise['path']}\n")

        # Check if exercise has TODO markers
        if self._has_incomplete_todos(exercise_path):
            print(f"{Fore.YELLOW}⚠️  发现未完成的 TODO 标记")
            print(f"{Fore.YELLOW}请填写代码中的 TODO 部分后再运行\n")
            return False

        # Load and run the exercise
        try:
            spec = importlib.util.spec_from_file_location(exercise['id'], exercise_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[exercise['id']] = module
            spec.loader.exec_module(module)

            # Run the test function
            test_func_name = exercise.get('test_func', 'test')
            if hasattr(module, test_func_name):
                test_func = getattr(module, test_func_name)
                result = test_func()

                # Check result
                if self.checker.check_result(exercise['id'], result):
                    print(f"\n{Fore.GREEN}{'='*70}")
                    print(f"{Fore.GREEN}✓ 练习通过！")
                    print(f"{Fore.GREEN}{'='*70}\n")

                    if 'learning_points' in exercise:
                        print(f"{Fore.CYAN}📚 学习要点:")
                        for point in exercise['learning_points']:
                            print(f"{Fore.CYAN}  • {point}")
                        print()

                    return True
                else:
                    print(f"\n{Fore.RED}{'='*70}")
                    print(f"{Fore.RED}✗ 练习未通过")
                    print(f"{Fore.RED}{'='*70}\n")
                    print(f"{Fore.YELLOW}结果未达到预期标准")
                    print(f"{Fore.YELLOW}提示: 使用 'python -m sutton_rl hint {exercise_id}' 获取帮助\n")
                    return False
            else:
                print(f"{Fore.RED}错误: 找不到测试函数 '{test_func_name}'")
                return False

        except Exception as e:
            print(f"\n{Fore.RED}{'='*70}")
            print(f"{Fore.RED}✗ 运行出错")
            print(f"{Fore.RED}{'='*70}\n")
            print(f"{Fore.RED}错误信息:")
            print(f"{Fore.RED}{str(e)}\n")

            if verbose:
                print(f"{Fore.YELLOW}详细错误信息:")
                traceback.print_exc()
                print()

            return False

    def watch_mode(self):
        """Watch mode - automatically run exercises when files change"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}Watch Mode - 监控模式")
        print(f"{Fore.CYAN}{'='*70}\n")
        print(f"{Fore.YELLOW}正在监控 exercises/ 目录...")
        print(f"{Fore.YELLOW}修改文件后自动运行测试")
        print(f"{Fore.YELLOW}按 Ctrl+C 退出\n")

        file_mtimes = {}

        try:
            while True:
                for exercise in EXERCISE_LIST:
                    exercise_path = self.exercises_dir / exercise['path']
                    if not exercise_path.exists():
                        continue

                    current_mtime = exercise_path.stat().st_mtime

                    if exercise_path not in file_mtimes:
                        file_mtimes[exercise_path] = current_mtime
                        continue

                    if current_mtime > file_mtimes[exercise_path]:
                        file_mtimes[exercise_path] = current_mtime
                        print(f"\n{Fore.MAGENTA}检测到文件变化: {exercise['path']}")
                        self.run_exercise(exercise['id'])

                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}退出监控模式")

    def verify_all(self):
        """Verify all exercises"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}验证所有练习")
        print(f"{Fore.CYAN}{'='*70}\n")

        passed = 0
        failed = 0
        incomplete = 0

        for exercise in EXERCISE_LIST:
            exercise_path = self.exercises_dir / exercise['path']

            if not exercise_path.exists():
                print(f"{Fore.RED}[缺失] {exercise['id']}")
                failed += 1
                continue

            if self._has_incomplete_todos(exercise_path):
                print(f"{Fore.YELLOW}[未完成] {exercise['id']}")
                incomplete += 1
                continue

            result = self.run_exercise(exercise['id'], verbose=False)

            if result:
                print(f"{Fore.GREEN}[✓] {exercise['id']}")
                passed += 1
            else:
                print(f"{Fore.RED}[✗] {exercise['id']}")
                failed += 1

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}通过: {passed}")
        print(f"{Fore.YELLOW}未完成: {incomplete}")
        print(f"{Fore.RED}失败: {failed}")
        print(f"{Fore.CYAN}总计: {len(EXERCISE_LIST)}")
        print(f"{Fore.CYAN}{'='*70}\n")

    def show_hint(self, exercise_id: str):
        """Show hint for an exercise"""
        exercise = self._find_exercise(exercise_id)
        if not exercise:
            print(f"{Fore.RED}错误: 找不到练习 '{exercise_id}'")
            return

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}提示: {exercise['name']}")
        print(f"{Fore.CYAN}{'='*70}\n")

        if 'hints' in exercise:
            for idx, hint in enumerate(exercise['hints'], 1):
                print(f"{Fore.YELLOW}{idx}. {hint}")
            print()
        else:
            print(f"{Fore.YELLOW}该练习暂无提示")
            print(f"{Fore.YELLOW}请参考 Sutton & Barto 书中的相关章节\n")

        if 'reference' in exercise:
            print(f"{Fore.CYAN}参考: {exercise['reference']}\n")

    def _find_exercise(self, exercise_id: str) -> Optional[Dict]:
        """Find exercise by ID"""
        for exercise in EXERCISE_LIST:
            if exercise['id'] == exercise_id or exercise['id'].endswith(exercise_id):
                return exercise
        return None

    def _check_if_completed(self, exercise_id: str) -> bool:
        """Check if exercise is completed"""
        # Simple check - could be enhanced with persistent storage
        return False

    def _has_incomplete_todos(self, exercise_path: Path) -> bool:
        """Check if exercise has incomplete TODO markers"""
        try:
            content = exercise_path.read_text(encoding='utf-8')
            # Check for TODO: or TODO markers
            return '# TODO:' in content or '# TODO' in content or 'pass  # TODO' in content
        except:
            return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Sutton RL Implementation - Interactive Learning Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m sutton_rl list                    列出所有练习
  python -m sutton_rl run ch02_ex01          运行特定练习
  python -m sutton_rl watch                   监控模式
  python -m sutton_rl verify                  验证所有练习
  python -m sutton_rl hint ch02_ex01         显示提示
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # List command
    subparsers.add_parser('list', help='列出所有练习')

    # Run command
    run_parser = subparsers.add_parser('run', help='运行特定练习')
    run_parser.add_argument('exercise', help='练习 ID')
    run_parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')

    # Watch command
    subparsers.add_parser('watch', help='监控模式（自动运行）')

    # Verify command
    subparsers.add_parser('verify', help='验证所有练习')

    # Hint command
    hint_parser = subparsers.add_parser('hint', help='显示提示')
    hint_parser.add_argument('exercise', help='练习 ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    runner = SuttonRLRunner()

    if args.command == 'list':
        runner.list_exercises()
    elif args.command == 'run':
        runner.run_exercise(args.exercise, verbose=args.verbose)
    elif args.command == 'watch':
        runner.watch_mode()
    elif args.command == 'verify':
        runner.verify_all()
    elif args.command == 'hint':
        runner.show_hint(args.exercise)


if __name__ == '__main__':
    main()
