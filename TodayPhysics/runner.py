#!/usr/bin/env python3
"""
Physics Rustlings - An interactive physics learning tool through programming
Inspired by Rustlings, designed for physics education from classical mechanics to quantum physics
"""

import os
import sys
import importlib.util
import traceback
from pathlib import Path
from typing import Optional, List, Tuple
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

console = Console()

EXERCISES_DIR = Path(__file__).parent / "exercises"
SOLUTIONS_DIR = Path(__file__).parent / "solutions"

# Exercise metadata
CHAPTERS = {
    "01_classical_mechanics": "经典力学 Classical Mechanics",
    "02_oscillations_waves": "振动与波 Oscillations & Waves",
    "03_electromagnetism": "电磁学 Electromagnetism",
    "04_thermodynamics": "热力学与统计物理 Thermodynamics & Statistical Physics",
    "05_special_relativity": "狭义相对论 Special Relativity",
    "06_general_relativity": "广义相对论 General Relativity",
    "07_quantum_mechanics": "量子力学 Quantum Mechanics",
    "08_advanced_quantum": "高等量子力学 Advanced Quantum Mechanics",
}


class Exercise:
    """Represents a single exercise"""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem
        self.chapter = path.parent.name
        self.content = path.read_text(encoding='utf-8')
        self._parse_metadata()

    def _parse_metadata(self):
        """Extract metadata from exercise file"""
        lines = self.content.split('\n')
        self.title = ""
        self.difficulty = "★"
        self.hints = []
        self.description = ""

        in_docstring = False
        docstring_lines = []

        for line in lines:
            if '"""' in line or "'''" in line:
                if in_docstring:
                    break
                in_docstring = True
                continue
            if in_docstring:
                docstring_lines.append(line)

        self.description = '\n'.join(docstring_lines)

        # Extract title from first line of docstring
        if docstring_lines:
            self.title = docstring_lines[0].strip()

        # Check for difficulty marker
        for line in docstring_lines:
            if '难度' in line or 'Difficulty' in line:
                self.difficulty = line.split(':')[-1].strip()
            if 'HINT:' in line or '提示:' in line:
                self.hints.append(line.split(':', 1)[-1].strip())

    def is_complete(self) -> bool:
        """Check if exercise has no TODO markers"""
        return '# TODO:' not in self.content and '# I AM NOT DONE' not in self.content

    def run(self) -> Tuple[bool, str, Optional[str]]:
        """Run the exercise and return (success, output, error)"""
        try:
            spec = importlib.util.spec_from_file_location(self.name, self.path)
            module = importlib.util.module_from_spec(spec)

            # Capture stdout
            import io
            from contextlib import redirect_stdout, redirect_stderr

            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                spec.loader.exec_module(module)

                # Run verify function if exists
                if hasattr(module, 'verify'):
                    result = module.verify()
                    if result is False:
                        return False, stdout_capture.getvalue(), "验证失败 Verification failed"

            return True, stdout_capture.getvalue(), None

        except Exception as e:
            return False, "", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

    def get_hint(self, level: int = 0) -> str:
        """Get hint at specified level"""
        if level < len(self.hints):
            return self.hints[level]
        return "没有更多提示了 No more hints available"


class ExerciseWatcher(FileSystemEventHandler):
    """Watch for file changes and auto-run exercises"""

    def __init__(self, exercise: Exercise, callback):
        self.exercise = exercise
        self.callback = callback
        self.last_modified = 0

    def on_modified(self, event):
        if event.src_path == str(self.exercise.path):
            # Debounce
            current_time = time.time()
            if current_time - self.last_modified > 0.5:
                self.last_modified = current_time
                self.callback()


def get_all_exercises() -> List[Exercise]:
    """Get all exercises in order"""
    exercises = []
    for chapter_dir in sorted(EXERCISES_DIR.iterdir()):
        if chapter_dir.is_dir() and not chapter_dir.name.startswith('_'):
            for ex_file in sorted(chapter_dir.glob('*.py')):
                if not ex_file.name.startswith('_'):
                    exercises.append(Exercise(ex_file))
    return exercises


def get_next_exercise(exercises: List[Exercise]) -> Optional[Exercise]:
    """Get the next incomplete exercise"""
    for ex in exercises:
        if not ex.is_complete():
            return ex
    return None


def display_exercise(exercise: Exercise):
    """Display exercise information"""
    console.clear()

    chapter_name = CHAPTERS.get(exercise.chapter, exercise.chapter)

    console.print(Panel(
        f"[bold cyan]{exercise.title}[/bold cyan]\n"
        f"章节: {chapter_name}\n"
        f"难度: {exercise.difficulty}",
        title="📚 Physics Rustlings",
        border_style="blue"
    ))

    console.print("\n[bold]文件路径:[/bold]", str(exercise.path))
    console.print("\n[bold yellow]说明:[/bold yellow]")
    console.print(Markdown(exercise.description))

    console.print("\n" + "="*60 + "\n")


def run_exercise(exercise: Exercise):
    """Run and display exercise results"""
    console.print("[bold]运行中...[/bold]\n")

    success, output, error = exercise.run()

    if output:
        console.print(Panel(output, title="输出 Output", border_style="green"))

    if success:
        console.print("\n[bold green]✓ 练习完成！Exercise completed![/bold green]")
        if exercise.is_complete():
            console.print("[cyan]运行 'physics-rustlings next' 继续下一个练习[/cyan]")
        else:
            console.print("[yellow]请移除 '# I AM NOT DONE' 标记以继续[/yellow]")
    else:
        console.print(f"\n[bold red]✗ 出错了 Error occurred[/bold red]")
        if error:
            console.print(Panel(error, title="错误信息", border_style="red"))
        console.print("\n[yellow]提示: 运行 'physics-rustlings hint' 获取帮助[/yellow]")


@click.group()
def cli():
    """Physics Rustlings - 通过编程学习物理学"""
    pass


@cli.command()
def list():
    """列出所有练习 List all exercises"""
    exercises = get_all_exercises()

    table = Table(title="📚 Physics Rustlings 练习列表")
    table.add_column("章节", style="cyan")
    table.add_column("练习", style="white")
    table.add_column("难度", style="yellow")
    table.add_column("状态", style="green")

    current_chapter = ""
    for ex in exercises:
        chapter_name = CHAPTERS.get(ex.chapter, ex.chapter)
        if ex.chapter != current_chapter:
            current_chapter = ex.chapter
            display_chapter = chapter_name
        else:
            display_chapter = ""

        status = "✓ 完成" if ex.is_complete() else "○ 未完成"
        status_style = "green" if ex.is_complete() else "yellow"

        table.add_row(
            display_chapter,
            ex.name,
            ex.difficulty,
            f"[{status_style}]{status}[/{status_style}]"
        )

    console.print(table)

    completed = sum(1 for ex in exercises if ex.is_complete())
    console.print(f"\n进度: {completed}/{len(exercises)} 已完成")


@cli.command()
@click.argument('name', required=False)
def run(name: Optional[str]):
    """运行指定练习 Run a specific exercise"""
    exercises = get_all_exercises()

    if name:
        # Find exercise by name
        exercise = None
        for ex in exercises:
            if ex.name == name or name in str(ex.path):
                exercise = ex
                break
        if not exercise:
            console.print(f"[red]找不到练习: {name}[/red]")
            return
    else:
        exercise = get_next_exercise(exercises)
        if not exercise:
            console.print("[green]🎉 恭喜！所有练习已完成！[/green]")
            return

    display_exercise(exercise)
    run_exercise(exercise)


@cli.command()
def next():
    """运行下一个未完成的练习 Run next incomplete exercise"""
    exercises = get_all_exercises()
    exercise = get_next_exercise(exercises)

    if not exercise:
        console.print("[green]🎉 恭喜！所有练习已完成！[/green]")
        return

    display_exercise(exercise)
    run_exercise(exercise)


@cli.command()
@click.argument('name', required=False)
def watch(name: Optional[str]):
    """监视文件变化并自动运行 Watch for changes and auto-run"""
    exercises = get_all_exercises()

    if name:
        exercise = None
        for ex in exercises:
            if ex.name == name or name in str(ex.path):
                exercise = ex
                break
        if not exercise:
            console.print(f"[red]找不到练习: {name}[/red]")
            return
    else:
        exercise = get_next_exercise(exercises)
        if not exercise:
            console.print("[green]🎉 恭喜！所有练习已完成！[/green]")
            return

    def on_change():
        # Reload exercise
        nonlocal exercise
        exercise = Exercise(exercise.path)
        display_exercise(exercise)
        run_exercise(exercise)

    display_exercise(exercise)
    run_exercise(exercise)

    console.print("\n[cyan]👀 监视模式已启动，保存文件后自动运行...[/cyan]")
    console.print("[dim]按 Ctrl+C 退出[/dim]\n")

    event_handler = ExerciseWatcher(exercise, on_change)
    observer = Observer()
    observer.schedule(event_handler, str(exercise.path.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@cli.command()
@click.argument('name', required=False)
@click.option('--level', '-l', default=0, help='Hint level (0-indexed)')
def hint(name: Optional[str], level: int):
    """获取练习提示 Get hints for an exercise"""
    exercises = get_all_exercises()

    if name:
        exercise = None
        for ex in exercises:
            if ex.name == name or name in str(ex.path):
                exercise = ex
                break
        if not exercise:
            console.print(f"[red]找不到练习: {name}[/red]")
            return
    else:
        exercise = get_next_exercise(exercises)
        if not exercise:
            console.print("[green]所有练习已完成！[/green]")
            return

    hint_text = exercise.get_hint(level)
    console.print(Panel(
        hint_text,
        title=f"💡 提示 Hint (Level {level + 1})",
        border_style="yellow"
    ))

    if level + 1 < len(exercise.hints):
        console.print(f"[dim]还有更多提示，使用 --level {level + 1} 查看[/dim]")


@cli.command()
def verify():
    """验证所有练习 Verify all exercises"""
    exercises = get_all_exercises()

    console.print("[bold]验证所有练习...[/bold]\n")

    passed = 0
    failed = 0

    for ex in exercises:
        success, _, error = ex.run()
        status = "[green]✓[/green]" if success else "[red]✗[/red]"
        console.print(f"{status} {ex.chapter}/{ex.name}")

        if success:
            passed += 1
        else:
            failed += 1

    console.print(f"\n结果: {passed} 通过, {failed} 失败")


@cli.command()
def progress():
    """显示学习进度 Show learning progress"""
    exercises = get_all_exercises()

    console.print(Panel("[bold]📊 学习进度 Learning Progress[/bold]", border_style="blue"))

    chapter_stats = {}
    for ex in exercises:
        if ex.chapter not in chapter_stats:
            chapter_stats[ex.chapter] = {"total": 0, "completed": 0}
        chapter_stats[ex.chapter]["total"] += 1
        if ex.is_complete():
            chapter_stats[ex.chapter]["completed"] += 1

    for chapter, stats in chapter_stats.items():
        chapter_name = CHAPTERS.get(chapter, chapter)
        pct = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        bar_width = 30
        filled = int(bar_width * pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        console.print(f"\n[cyan]{chapter_name}[/cyan]")
        console.print(f"[green]{bar}[/green] {stats['completed']}/{stats['total']} ({pct:.0f}%)")

    total = len(exercises)
    completed = sum(1 for ex in exercises if ex.is_complete())
    overall_pct = (completed / total * 100) if total > 0 else 0

    console.print(f"\n[bold]总进度: {completed}/{total} ({overall_pct:.1f}%)[/bold]")


if __name__ == "__main__":
    cli()
