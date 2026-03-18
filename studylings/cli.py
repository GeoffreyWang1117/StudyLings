"""
Unified Click CLI for studylings projects.
Provides: list, run, next, verify, watch, hint, progress, reset, solution
"""

import subprocess
import sys

import click

from .checker import get_checker
from .exercise import Exercise, ProjectConfig, ValidationMode, find_exercise
from .progress import Progress
from .ui import (
    console,
    print_banner,
    show_check_result,
    show_exercise_list,
    show_hint,
    show_progress_detail,
    show_status,
)
from .watcher import watch_exercises


def create_cli(config: ProjectConfig) -> click.Group:
    """Create a Click CLI group configured for a specific project."""

    @click.group(invoke_without_command=True)
    @click.pass_context
    @click.option("--version", "-v", is_flag=True, help="显示版本信息")
    def cli(ctx, version):
        if version:
            console.print(f"{config.display_name} v{config.version}")
            return

        if ctx.invoked_subcommand is None:
            print_banner(config)
            progress = Progress(config)
            exercises = Exercise.discover_all(config)

            def get_next():
                for ex in exercises:
                    if not progress.is_complete(ex.name):
                        return ex
                return None

            show_status(config, progress, get_next)

    cli.help = config.display_name

    @cli.command("list")
    @click.option("--chapter", "-c", help="只显示指定章节")
    def list_exercises(chapter):
        """列出所有练习"""
        exercises = Exercise.discover_all(config)
        progress = Progress(config)
        show_exercise_list(exercises, config, progress, chapter)

    @cli.command()
    @click.argument("exercise_name", required=False)
    def run(exercise_name):
        """运行指定练习"""
        if exercise_name:
            ex = find_exercise(exercise_name, config)
            if ex is None:
                console.print(f"[red]找不到练习: {exercise_name}[/red]")
                console.print(f"\n使用 [green]python -m {config.name} list[/green] 查看所有练习")
                sys.exit(1)
        else:
            # Run next incomplete
            exercises = Exercise.discover_all(config)
            progress = Progress(config)
            ex = None
            for e in exercises:
                if not progress.is_complete(e.name):
                    ex = e
                    break
            if ex is None:
                console.print("[green]恭喜！所有练习已完成！[/green]")
                return

        console.print(f"\n[cyan]运行练习: {ex.name}[/cyan]\n")
        _run_and_check(ex, config)

    @cli.command()
    def next():
        """运行下一个未完成的练习"""
        exercises = Exercise.discover_all(config)
        progress = Progress(config)
        for ex in exercises:
            if not progress.is_complete(ex.name):
                console.print(f"\n[cyan]运行练习: {ex.name}[/cyan]\n")
                _run_and_check(ex, config)
                return
        console.print("[green]恭喜！所有练习已完成！[/green]")

    @cli.command()
    @click.argument("exercise_name", required=False)
    def verify(exercise_name):
        """验证练习"""
        exercises = Exercise.discover_all(config)

        if exercise_name:
            ex = find_exercise(exercise_name, config)
            if ex is None:
                console.print(f"[red]找不到练习: {exercise_name}[/red]")
                sys.exit(1)
            exercises = [ex]

        console.print("[bold]验证练习...[/bold]\n")
        passed = 0
        failed = 0

        for ex in exercises:
            checker = get_checker(ex, config)
            result = checker.check(verbose=False)
            status = "[green]✓[/green]" if result else "[red]✗[/red]"
            console.print(f"{status} {ex.chapter}/{ex.name}")

            if result:
                passed += 1
                progress = Progress(config)
                progress.mark_complete(ex.name)
            else:
                failed += 1

        console.print(f"\n结果: {passed} 通过, {failed} 失败")

    @cli.command()
    @click.argument("exercise_name", required=False)
    def watch(exercise_name):
        """监视模式 - 自动检测文件变化并运行"""
        if exercise_name:
            ex = find_exercise(exercise_name, config)
            if ex is None:
                console.print(f"[red]找不到练习: {exercise_name}[/red]")
                sys.exit(1)
            watch_path = ex.path.parent
        else:
            watch_path = None

        console.print("[green]监视模式已启动[/green]")
        console.print(f"正在监视: {watch_path or config.get_exercises_path()}")
        console.print("按 Ctrl+C 退出\n")

        # Show current exercise
        _show_current_exercise(config)

        def on_change(changed_path):
            console.clear()
            console.print(f"\n[cyan]检测到文件变化: {changed_path.name}[/cyan]\n")

            # Find the exercise that matches this file
            matched_ex = None
            for ex in Exercise.discover_all(config):
                if ex.path == changed_path or changed_path.is_relative_to(ex.path.parent):
                    matched_ex = ex
                    break

            if matched_ex is None:
                # Fallback: run current incomplete exercise
                prog = Progress(config)
                for ex in Exercise.discover_all(config):
                    if not prog.is_complete(ex.name):
                        matched_ex = ex
                        break

            if matched_ex is None:
                console.print("[green]恭喜！所有练习已完成！[/green]")
                return

            passed = _run_and_check(matched_ex, config)

            if passed:
                # Auto-advance: show next incomplete exercise
                prog = Progress(config)
                next_ex = None
                for ex in Exercise.discover_all(config):
                    if not prog.is_complete(ex.name):
                        next_ex = ex
                        break

                if next_ex is None:
                    stats = prog.get_stats()
                    console.print(f"\n[bold green]🎉 恭喜！你已完成全部 {stats['total']} 个练习！[/bold green]")
                else:
                    console.print(f"\n[cyan]{'─' * 50}[/cyan]")
                    console.print(f"[bold]下一个练习: {next_ex.name}[/bold]")
                    console.print(f"文件: [cyan]{next_ex.path}[/cyan]")
                    if next_ex.topic and next_ex.topic != "Unknown":
                        console.print(f"主题: {next_ex.topic}")
                    console.print(f"\n[dim]编辑上述文件，保存后自动运行[/dim]")

        watch_exercises(config, on_change, specific_path=watch_path)

    @cli.command()
    @click.argument("exercise_name")
    @click.option("--level", "-l", default=0, help="提示级别 (从0开始)")
    def hint(exercise_name, level):
        """获取练习提示"""
        ex = find_exercise(exercise_name, config)
        if ex is None:
            console.print(f"[red]找不到练习: {exercise_name}[/red]")
            sys.exit(1)
        show_hint(ex, level)

    @cli.command()
    def progress():
        """显示学习进度"""
        prog = Progress(config)
        show_progress_detail(config, prog)

    @cli.command()
    @click.argument("exercise_name", required=False)
    @click.option("--all", "-a", "reset_all", is_flag=True, help="重置所有进度")
    def reset(exercise_name, reset_all):
        """重置练习进度"""
        prog = Progress(config)

        if reset_all:
            if click.confirm("确定要重置所有进度吗？"):
                prog.reset()
                console.print("[green]已重置所有进度[/green]")
        elif exercise_name:
            ex = find_exercise(exercise_name, config)
            if ex is None:
                console.print(f"[red]找不到练习: {exercise_name}[/red]")
                sys.exit(1)
            prog.reset(exercise_name)
            console.print(f"[green]已重置练习: {exercise_name}[/green]")
        else:
            console.print("[yellow]请指定练习名称或使用 --all 重置所有进度[/yellow]")

    @cli.command()
    @click.argument("exercise_name")
    def solution(exercise_name):
        """查看练习参考答案"""
        ex = find_exercise(exercise_name, config)
        if ex is None:
            console.print(f"[red]找不到练习: {exercise_name}[/red]")
            sys.exit(1)

        solutions_path = config.project_root / (config.solutions_dir or "solutions")
        if not solutions_path.exists():
            console.print("[yellow]此项目没有参考答案目录[/yellow]")
            return

        # Try common patterns for solution files
        candidates = [
            solutions_path / ex.chapter / ex.path.name,           # solutions/ch01/ex01.py
            solutions_path / ex.chapter / f"{ex.name}{config.file_extension}",
            solutions_path / f"{ex.name}{config.file_extension}", # solutions/ex01.py
            solutions_path / ex.path.name,
        ]
        # For C++ exercises with sub-dirs
        if config.file_extension in (".cpp", ".cu", ".c"):
            candidates.extend([
                solutions_path / ex.chapter / "main.cpp",
                solutions_path / ex.chapter / f"main{config.file_extension}",
            ])

        solution_file = None
        for c in candidates:
            if c.exists():
                solution_file = c
                break

        if solution_file is None:
            console.print(f"[yellow]找不到 '{exercise_name}' 的参考答案[/yellow]")
            console.print(f"[dim]已搜索: {solutions_path}[/dim]")
            return

        from rich.syntax import Syntax
        content = solution_file.read_text(encoding="utf-8")
        lang_map = {".py": "python", ".cpp": "cpp", ".cu": "cpp",
                     ".c": "c", ".ts": "typescript", ".rs": "rust"}
        lang = lang_map.get(config.file_extension, "text")
        console.print(f"\n[bold]参考答案: {exercise_name}[/bold]")
        console.print(f"[dim]文件: {solution_file}[/dim]\n")
        console.print(Syntax(content, lang, theme="monokai", line_numbers=True))

    return cli


def _show_current_exercise(config: ProjectConfig):
    """Show the current incomplete exercise info."""
    progress = Progress(config)
    for ex in Exercise.discover_all(config):
        if not progress.is_complete(ex.name):
            console.print(f"当前练习: [bold]{ex.name}[/bold]")
            console.print(f"文件: {ex.path}\n")
            return
    console.print("[green]所有练习已完成！[/green]\n")


def _run_and_check(exercise: Exercise, config: ProjectConfig) -> bool:
    """Run an exercise and display results. Returns True if exercise passed."""
    passed = False

    if config.validation_mode == ValidationMode.TEST_FILE:
        # Run as subprocess (exercise calls checker itself)
        result = subprocess.run(
            [sys.executable, str(exercise.path)],
            text=True,
        )
        if result.returncode == 0:
            passed = True
            progress = Progress(config)
            progress.mark_complete(exercise.name)

    elif config.validation_mode == ValidationMode.VERIFY_FUNC:
        checker = get_checker(exercise, config)
        result = checker.check(verbose=True)
        if result.details:
            console.print(result.details)
        if result.success:
            console.print("\n[bold green]✓ 练习完成！Exercise completed![/bold green]")
            if exercise.is_complete(config):
                # Exercise markers removed — record progress
                passed = True
                progress = Progress(config)
                progress.mark_complete(exercise.name)
            else:
                marker = config.comment_prefix + " I AM NOT DONE"
                console.print(f"[yellow]请移除 '{marker}' 标记以继续[/yellow]")
        else:
            console.print(f"\n[bold red]✗ 出错了 Error occurred[/bold red]")
            if result.message:
                console.print(f"[red]{result.message}[/red]")

    elif config.validation_mode == ValidationMode.COMPILE_AND_RUN:
        checker = get_checker(exercise, config)
        result = checker.check(verbose=True)
        show_check_result(result, exercise.name, config)
        if result.success:
            passed = True
            # CompileAndRunChecker already creates .completed, also write JSON
            progress = Progress(config)
            progress.mark_complete(exercise.name)

    return passed


def main(config: ProjectConfig):
    """Entry point for a studylings project."""
    cli = create_cli(config)
    cli()
