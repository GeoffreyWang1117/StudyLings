"""
File watching with watchdog for studylings projects.
"""

import time
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .exercise import ProjectConfig


class ExerciseWatchHandler(FileSystemEventHandler):
    """Handle file changes for watch mode."""

    def __init__(self, callback: Callable, file_extension: str = ".py", debounce: float = 1.0):
        self.callback = callback
        self.file_extension = file_extension
        self.last_run = 0.0
        self.debounce = debounce

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(self.file_extension):
            return

        now = time.time()
        if now - self.last_run < self.debounce:
            return
        self.last_run = now

        self.callback(Path(event.src_path))


def watch_exercises(config: ProjectConfig, callback: Callable, specific_path: Path = None):
    """Watch for exercise file changes and trigger callback.

    Args:
        config: Project configuration.
        callback: Called with the changed file path.
        specific_path: If set, only watch this specific directory.
    """
    watch_path = specific_path or config.get_exercises_path()
    handler = ExerciseWatchHandler(
        callback=callback,
        file_extension=config.file_extension,
        debounce=0.5 if config.file_extension == ".cpp" else 1.0,
    )
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
