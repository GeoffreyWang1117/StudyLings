"""
Exercise runner for Economlings.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .progress import Progress
from .utils import EXERCISES_DIR, find_exercise, get_all_exercises


class ExerciseRunner:
    """Run and manage exercises."""

    def __init__(self):
        self.progress = Progress()

    def run_exercise(self, exercise_path: Path, verbose: bool = True) -> bool:
        """Run a single exercise and check it."""
        result = subprocess.run(
            [sys.executable, str(exercise_path)],
            capture_output=not verbose,
            text=True
        )
        return result.returncode == 0

    def run_by_name(self, name: str, verbose: bool = True) -> bool:
        """Run an exercise by name."""
        path = find_exercise(name)
        if path is None:
            print(f"找不到练习: {name}")
            return False
        return self.run_exercise(path, verbose)

    def get_next_exercise(self) -> Optional[dict]:
        """Get the next uncompleted exercise."""
        exercises = get_all_exercises()
        for ex in exercises:
            if not self.progress.is_complete(ex["name"]):
                return ex
        return None

    def list_exercises(self) -> list[dict]:
        """List all exercises with their status."""
        exercises = get_all_exercises()
        for ex in exercises:
            ex["completed"] = self.progress.is_complete(ex["name"])
        return exercises


class WatchHandler(FileSystemEventHandler):
    """Handle file changes for watch mode."""

    def __init__(self, runner: ExerciseRunner, console):
        self.runner = runner
        self.console = console
        self.last_run = 0
        self.debounce_seconds = 1

    def on_modified(self, event):
        if event.is_directory:
            return

        if not event.src_path.endswith(".py"):
            return

        # Debounce
        now = time.time()
        if now - self.last_run < self.debounce_seconds:
            return
        self.last_run = now

        path = Path(event.src_path)
        if EXERCISES_DIR in path.parents or path.parent == EXERCISES_DIR:
            self.console.clear()
            self.console.print(f"\n[cyan]检测到文件变化: {path.name}[/cyan]\n")
            self.runner.run_exercise(path)


def watch_exercises(console) -> None:
    """Watch for exercise file changes and auto-run."""
    runner = ExerciseRunner()
    handler = WatchHandler(runner, console)
    observer = Observer()
    observer.schedule(handler, str(EXERCISES_DIR), recursive=True)
    observer.start()

    console.print("[green]监视模式已启动[/green]")
    console.print(f"正在监视: {EXERCISES_DIR}")
    console.print("按 Ctrl+C 退出\n")

    # Run current exercise initially
    next_ex = runner.get_next_exercise()
    if next_ex:
        console.print(f"当前练习: [bold]{next_ex['name']}[/bold]")
        console.print(f"文件: {next_ex['path']}\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
