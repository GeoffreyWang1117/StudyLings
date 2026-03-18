"""
Studylings Suite Dashboard
Usage: cd rustlings-suite && python -m studylings
Shows aggregate progress across all projects.
"""

import importlib
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .exercise import Exercise

console = Console()

# Registry of all known projects: (directory_name, module_name)
PROJECTS = [
    ("study-Economy", "economlings"),
    ("TodayPhysics", "todayphysics"),
    ("Vulkan-Study", "vulkanlings"),
    ("Gen-AI-Study", "genailings"),
    ("quantum-Learning", "quantumlings"),
    ("Cuda-CPP-Study", "cudalings"),
    ("CUDA-Tutorial", "jaxlings"),
    ("GDB-LLDB-Learner", "debuglings"),
    ("SuttonRL-Implementation", "suttonrlings"),
    ("multi-processor-programming-study", "mplings"),
    ("open-data-structure", "odslings"),
    ("ADM-algorithms", "admlings"),
    ("Traditional-Important-Algorithms", "algolings"),
    ("Asynchronous-Programming-Learning", "asynclings"),
]


def load_project_config(suite_root: Path, dir_name: str, module_name: str):
    """Try to load a project's studylings config."""
    project_path = suite_root / dir_name
    if not project_path.exists():
        return None

    # Add project to sys.path so its package can be imported
    if str(project_path) not in sys.path:
        sys.path.insert(0, str(project_path))

    try:
        # Try common config module paths
        for config_module_name in [
            f"{module_name}.config",
            f"{module_name}.studylings_config",
        ]:
            try:
                mod = importlib.import_module(config_module_name)
                if hasattr(mod, "config"):
                    return mod.config
            except (ImportError, ModuleNotFoundError):
                continue
    except Exception:
        pass
    return None


def dashboard():
    """Show aggregate progress dashboard."""
    suite_root = Path(__file__).parent.parent

    console.print(Panel(
        "[bold cyan]Studylings Suite Dashboard[/bold cyan]\n"
        "全部自学项目进度总览",
        border_style="cyan",
    ))

    table = Table(show_header=True, header_style="bold")
    table.add_column("项目", width=22)
    table.add_column("名称", width=28)
    table.add_column("进度", width=28)
    table.add_column("完成", justify="right", width=8)
    table.add_column("总数", justify="right", width=6)

    grand_total = 0
    grand_completed = 0
    loaded = 0

    from .progress import Progress

    for dir_name, module_name in PROJECTS:
        cfg = load_project_config(suite_root, dir_name, module_name)
        if cfg is None:
            table.add_row(
                module_name,
                f"[dim]{dir_name}[/dim]",
                "[dim]未加载[/dim]",
                "-",
                "-",
            )
            continue

        loaded += 1
        try:
            progress = Progress(cfg)
            stats = progress.get_stats()
            total = stats["total"]
            completed = stats["completed"]
            pct = stats["percentage"]

            grand_total += total
            grand_completed += completed

            bar_len = 20
            filled = int(bar_len * completed / total) if total > 0 else 0
            bar = "█" * filled + "░" * (bar_len - filled)

            if pct >= 100:
                status_style = "green"
            elif pct > 0:
                status_style = "yellow"
            else:
                status_style = "dim"

            table.add_row(
                module_name,
                cfg.display_name[:28],
                f"[{status_style}]{bar}[/{status_style}] {pct:.0f}%",
                str(completed),
                str(total),
            )
        except Exception as e:
            table.add_row(
                module_name,
                f"[dim]{dir_name}[/dim]",
                f"[red]错误: {e}[/red]",
                "-",
                "-",
            )

    console.print(table)

    # Grand total
    grand_pct = (grand_completed / grand_total * 100) if grand_total > 0 else 0
    bar_len = 40
    filled = int(bar_len * grand_completed / grand_total) if grand_total > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)

    console.print(f"\n[bold]总计: {loaded} 个项目, {grand_total} 个练习[/bold]")
    console.print(f"[green]{bar}[/green] {grand_completed}/{grand_total} ({grand_pct:.1f}%)")

    if grand_completed >= grand_total and grand_total > 0:
        console.print("\n[bold green]🎉 恭喜！你已完成全部项目的全部练习！[/bold green]")
    else:
        console.print(f"\n[dim]在各项目目录中运行 python -m <项目名> 开始学习[/dim]")


if __name__ == "__main__":
    dashboard()
