"""
Rich terminal output helpers for studylings projects.
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress as RichProgress, TextColumn
from rich.table import Table

from .exercise import Exercise, ProjectConfig

console = Console()


def print_banner(config: ProjectConfig):
    """Print the project welcome banner."""
    if config.banner:
        console.print(config.banner, style="cyan")
    else:
        console.print(
            Panel(
                f"[bold]{config.display_name}[/bold]\nv{config.version}",
                border_style="cyan",
            )
        )


def show_status(config: ProjectConfig, progress, get_next_fn):
    """Show current progress and next exercise."""
    stats = progress.get_stats()

    console.print("\n[bold]学习进度[/bold]")
    with RichProgress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as prog:
        prog.add_task(
            f"已完成 {stats['completed']}/{stats['total']} 个练习",
            total=stats["total"],
            completed=stats["completed"],
        )

    next_ex = get_next_fn()
    if next_ex:
        console.print(
            Panel(
                f"[bold]{next_ex.name}[/bold]\n"
                f"主题: {next_ex.topic}\n"
                f"难度: {next_ex.difficulty}\n"
                f"章节: {config.chapters.get(next_ex.chapter, next_ex.chapter)}\n\n"
                f"文件路径: [cyan]{next_ex.path}[/cyan]\n\n"
                f"运行命令: [green]python -m {config.name} run {next_ex.name}[/green]",
                title="下一个练习",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                "[green]恭喜！你已完成所有练习！[/green]",
                title="完成",
                border_style="green",
            )
        )

    console.print(f"\n[dim]使用 'python -m {config.name} --help' 查看所有命令[/dim]")


def show_exercise_list(exercises: list, config: ProjectConfig, progress, chapter_filter: str = None):
    """Display exercises grouped by chapter."""
    if not exercises:
        console.print("[yellow]没有找到练习文件[/yellow]")
        return

    chapters = {}
    for ex in exercises:
        ch = ex.chapter
        if chapter_filter and chapter_filter not in ch:
            continue
        if ch not in chapters:
            chapters[ch] = []
        chapters[ch].append(ex)

    for ch_name, ch_exercises in sorted(chapters.items()):
        display_name = config.chapters.get(ch_name, ch_name)
        console.print(f"\n[bold]{display_name}[/bold]")

        table = Table(show_header=True, header_style="bold")
        table.add_column("状态", width=4)
        table.add_column("名称", width=25)
        table.add_column("主题", width=30)
        table.add_column("难度", width=10)

        for ex in ch_exercises:
            is_done = progress.is_complete(ex.name)
            status = "[green]✓[/green]" if is_done else "[dim]○[/dim]"
            table.add_row(status, ex.name, ex.topic, ex.difficulty)

        console.print(table)


def show_progress_detail(config: ProjectConfig, progress):
    """Display detailed chapter-by-chapter progress."""
    stats = progress.get_stats()

    console.print("\n[bold]学习进度统计[/bold]\n")
    console.print(f"总进度: {stats['completed']}/{stats['total']} ({stats['percentage']:.1f}%)")

    console.print("\n[bold]各章节进度:[/bold]")
    for ch_name, ch_stats in sorted(stats["chapters"].items()):
        pct = (ch_stats["completed"] / ch_stats["total"] * 100) if ch_stats["total"] > 0 else 0
        bar_len = 20
        filled = int(bar_len * ch_stats["completed"] / ch_stats["total"]) if ch_stats["total"] > 0 else 0
        bar = "█" * filled + "░" * (bar_len - filled)

        display_name = config.chapters.get(ch_name, ch_name)
        console.print(
            f"  {display_name}: "
            f"[green]{bar}[/green] "
            f"{ch_stats['completed']}/{ch_stats['total']} ({pct:.0f}%)"
        )

    if stats["started_at"]:
        console.print(f"\n开始时间: {stats['started_at'][:19]}")
    if stats["last_activity"]:
        console.print(f"最后活动: {stats['last_activity'][:19]}")


def show_check_result(result, exercise_name: str, config: ProjectConfig):
    """Display a check result with Rich formatting."""
    if result.success:
        console.print(
            Panel(
                f"[green]恭喜！练习 '{exercise_name}' 完成！[/green]\n"
                f"运行 [bold]python -m {config.name}[/bold] 继续下一个练习",
                title="成功",
                border_style="green",
            )
        )
        if result.details:
            console.print(result.details)
    else:
        console.print(
            Panel(
                f"[red]✗ {result.message}[/red]" + (f"\n{result.details}" if result.details else ""),
                title="失败",
                border_style="red",
            )
        )


def show_hint(exercise: Exercise, level: int = 0):
    """Display hints for an exercise."""
    hint_text = exercise.get_hint(level)
    console.print(
        Panel(
            hint_text,
            title=f"提示: {exercise.name} (Level {level + 1})",
            border_style="yellow",
        )
    )
    if level + 1 < len(exercise.hints):
        console.print(f"[dim]还有更多提示，使用 --level {level + 1} 查看[/dim]")
