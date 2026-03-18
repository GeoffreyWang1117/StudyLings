"""File watcher for automatic exercise re-running."""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .runner import Runner


class ExerciseHandler(FileSystemEventHandler):
    """Handles file system events for exercise files."""

    def __init__(self, runner: Runner):
        self.runner = runner
        self.last_run = 0
        self.debounce_seconds = 1

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Only watch Python files in exercises directory
        if not event.src_path.endswith('.py'):
            return

        if 'exercises' not in event.src_path:
            return

        # Debounce rapid file changes
        current_time = time.time()
        if current_time - self.last_run < self.debounce_seconds:
            return

        self.last_run = current_time

        # Find and run the modified exercise
        path = Path(event.src_path)
        for exercise in self.runner.config.get_all_exercises():
            if path.samefile(exercise.path):
                print(f"\n{'='*60}")
                print(f"File changed: {path.name}")
                print(f"{'='*60}")
                self.runner.run_exercise(exercise)
                break


def watch_mode(runner: Runner):
    """Start watch mode for automatic exercise re-running."""
    event_handler = ExerciseHandler(runner)
    observer = Observer()

    # Watch the exercises directory
    exercises_dir = Path("exercises")
    if not exercises_dir.exists():
        print(f"Error: {exercises_dir} directory not found")
        return

    observer.schedule(event_handler, str(exercises_dir), recursive=True)
    observer.start()

    print(f"Watching {exercises_dir} for changes...")
    print("Modify any exercise file to trigger automatic checking.")
    print("Press Ctrl+C to exit.\n")

    # Run the next pending exercise initially
    runner.run_next()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping watch mode...")

    observer.join()
