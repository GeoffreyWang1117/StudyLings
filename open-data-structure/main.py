#!/usr/bin/env python3
"""
ODS-Python: Open Data Structures Learning System
Inspired by Rustlings - Learn data structures through interactive exercises
"""

import sys
import os
import argparse
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import toml
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class Exercise:
    """Represents a single exercise"""
    def __init__(self, name: str, path: str, mode: str, hint: str):
        self.name = name
        self.path = path
        self.mode = mode
        self.hint = hint
        self.completed = False

    def run(self) -> bool:
        """Run the exercise tests"""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", self.path, "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}⏱  Test timed out after 30 seconds")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Error running test: {e}")
            return False

    def show_hint(self):
        """Display the hint for this exercise"""
        print(f"\n{Fore.CYAN}💡 Hint for {self.name}:")
        print(f"{Fore.YELLOW}{self.hint}")


class ODSPython:
    """Main application class"""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.config_file = self.root_dir / "info.toml"
        self.progress_file = self.root_dir / ".ods_progress.json"
        self.exercises: List[Exercise] = []
        self.current_index = 0

        self.load_config()
        self.load_progress()

    def load_config(self):
        """Load exercises from info.toml"""
        if not self.config_file.exists():
            print(f"{Fore.RED}❌ Configuration file not found: {self.config_file}")
            sys.exit(1)

        config = toml.load(self.config_file)

        for ex_data in config.get("exercises", []):
            exercise = Exercise(
                name=ex_data["name"],
                path=str(self.root_dir / ex_data["path"]),
                mode=ex_data["mode"],
                hint=ex_data["hint"]
            )
            self.exercises.append(exercise)

        if not self.exercises:
            print(f"{Fore.RED}❌ No exercises found in configuration")
            sys.exit(1)

    def load_progress(self):
        """Load user progress from JSON file"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    completed = set(data.get("completed", []))

                    for ex in self.exercises:
                        if ex.name in completed:
                            ex.completed = True

                    self.current_index = data.get("current_index", 0)
            except Exception as e:
                print(f"{Fore.YELLOW}⚠  Could not load progress: {e}")

    def save_progress(self):
        """Save user progress to JSON file"""
        data = {
            "completed": [ex.name for ex in self.exercises if ex.completed],
            "current_index": self.current_index
        }

        try:
            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"{Fore.YELLOW}⚠  Could not save progress: {e}")

    def print_banner(self):
        """Print welcome banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   {Fore.GREEN}🐍 ODS-Python: Open Data Structures Learning System{Fore.CYAN}   ║
║                                                           ║
║   {Fore.YELLOW}Learn data structures through hands-on exercises{Fore.CYAN}       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def print_progress(self):
        """Display overall progress"""
        completed = sum(1 for ex in self.exercises if ex.completed)
        total = len(self.exercises)
        percentage = (completed / total) * 100 if total > 0 else 0

        progress_bar_width = 40
        filled = int(progress_bar_width * completed / total)
        bar = "█" * filled + "░" * (progress_bar_width - filled)

        print(f"\n{Fore.CYAN}Progress: {Fore.GREEN}{completed}/{total} {Fore.CYAN}exercises completed")
        print(f"{Fore.CYAN}[{Fore.GREEN}{bar}{Fore.CYAN}] {percentage:.1f}%\n")

    def get_current_exercise(self) -> Optional[Exercise]:
        """Get the current exercise to work on"""
        for i, ex in enumerate(self.exercises):
            if not ex.completed:
                self.current_index = i
                return ex
        return None

    def run_exercise(self, exercise: Exercise):
        """Run a specific exercise"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📝 Exercise: {Fore.GREEN}{exercise.name}")
        print(f"{Fore.CYAN}📁 File: {Fore.WHITE}{exercise.path}")
        print(f"{Fore.CYAN}{'='*60}\n")

        if not Path(exercise.path).exists():
            print(f"{Fore.RED}❌ Exercise file not found: {exercise.path}")
            print(f"{Fore.YELLOW}💡 This exercise hasn't been created yet.")
            return False

        print(f"{Fore.CYAN}🔧 Running tests...\n")

        success = exercise.run()

        if success:
            print(f"\n{Fore.GREEN}✅ Success! All tests passed!")
            exercise.completed = True
            self.save_progress()

            # Check if there are more exercises
            next_ex = self.get_current_exercise()
            if next_ex:
                print(f"\n{Fore.CYAN}➡️  Next exercise: {Fore.GREEN}{next_ex.name}")
                print(f"{Fore.YELLOW}Run 'python main.py' to continue")
            else:
                print(f"\n{Fore.GREEN}🎉 Congratulations! You've completed all exercises!")
                self.print_progress()
        else:
            print(f"\n{Fore.RED}❌ Tests failed. Keep trying!")
            print(f"{Fore.YELLOW}💡 Use 'python main.py hint' for a hint")
            print(f"{Fore.CYAN}📖 Review the exercise file: {exercise.path}")

        return success

    def cmd_run(self, exercise_name: Optional[str] = None):
        """Run command: execute current or specified exercise"""
        if exercise_name:
            # Run specific exercise
            exercise = next((ex for ex in self.exercises if ex.name == exercise_name), None)
            if not exercise:
                print(f"{Fore.RED}❌ Exercise not found: {exercise_name}")
                return
        else:
            # Run current exercise
            exercise = self.get_current_exercise()
            if not exercise:
                print(f"{Fore.GREEN}🎉 All exercises completed!")
                self.print_progress()
                return

        self.run_exercise(exercise)

    def cmd_watch(self):
        """Watch mode: auto-run tests on file changes"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class ExerciseHandler(FileSystemEventHandler):
                def __init__(self, ods):
                    self.ods = ods

                def on_modified(self, event):
                    if event.src_path.endswith('.py') and '/exercises/' in event.src_path:
                        print(f"\n{Fore.CYAN}🔄 File changed: {event.src_path}")
                        exercise = self.ods.get_current_exercise()
                        if exercise and event.src_path == exercise.path:
                            self.ods.run_exercise(exercise)

            print(f"{Fore.CYAN}👀 Watch mode enabled. Edit your exercises and save to auto-run tests.")
            print(f"{Fore.YELLOW}Press Ctrl+C to exit.\n")

            event_handler = ExerciseHandler(self)
            observer = Observer()
            observer.schedule(event_handler, str(self.root_dir / "exercises"), recursive=True)
            observer.start()

            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print(f"\n{Fore.YELLOW}👋 Watch mode stopped.")

            observer.join()

        except ImportError:
            print(f"{Fore.RED}❌ Watch mode requires 'watchdog' package")
            print(f"{Fore.YELLOW}Install it with: pip install watchdog")

    def cmd_verify(self):
        """Verify all completed exercises"""
        print(f"{Fore.CYAN}🔍 Verifying all completed exercises...\n")

        failed = []
        for ex in self.exercises:
            if ex.completed:
                print(f"{Fore.CYAN}Checking {ex.name}... ", end="")
                if ex.run():
                    print(f"{Fore.GREEN}✅")
                else:
                    print(f"{Fore.RED}❌")
                    failed.append(ex.name)

        if failed:
            print(f"\n{Fore.RED}❌ {len(failed)} exercise(s) failed:")
            for name in failed:
                print(f"  - {name}")
        else:
            print(f"\n{Fore.GREEN}✅ All completed exercises verified!")

    def cmd_hint(self):
        """Show hint for current exercise"""
        exercise = self.get_current_exercise()
        if exercise:
            exercise.show_hint()
        else:
            print(f"{Fore.GREEN}🎉 All exercises completed! No hints needed.")

    def cmd_list(self):
        """List all exercises"""
        print(f"\n{Fore.CYAN}📚 Available exercises:\n")

        for i, ex in enumerate(self.exercises, 1):
            status = f"{Fore.GREEN}✅" if ex.completed else f"{Fore.YELLOW}⏳"
            current = f"{Fore.CYAN}→ " if ex == self.get_current_exercise() else "  "
            print(f"{current}{status} {i:2d}. {ex.name}")

        print()
        self.print_progress()

    def cmd_reset(self):
        """Reset progress"""
        confirm = input(f"{Fore.YELLOW}⚠️  Reset all progress? (yes/no): ")
        if confirm.lower() == 'yes':
            if self.progress_file.exists():
                self.progress_file.unlink()
            print(f"{Fore.GREEN}✅ Progress reset!")
            self.current_index = 0
            for ex in self.exercises:
                ex.completed = False
        else:
            print(f"{Fore.CYAN}Reset cancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="ODS-Python: Interactive Data Structures Learning System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run current exercise
  python main.py watch        # Watch mode (auto-run on save)
  python main.py run arrays01 # Run specific exercise
  python main.py list         # List all exercises
  python main.py hint         # Get a hint
  python main.py verify       # Verify all completed exercises
        """
    )

    parser.add_argument(
        'command',
        nargs='?',
        default='run',
        choices=['run', 'watch', 'verify', 'hint', 'list', 'reset'],
        help='Command to execute'
    )

    parser.add_argument(
        'exercise',
        nargs='?',
        help='Specific exercise to run'
    )

    args = parser.parse_args()

    ods = ODSPython()
    ods.print_banner()

    if args.command == 'run':
        ods.cmd_run(args.exercise)
    elif args.command == 'watch':
        ods.cmd_watch()
    elif args.command == 'verify':
        ods.cmd_verify()
    elif args.command == 'hint':
        ods.cmd_hint()
    elif args.command == 'list':
        ods.cmd_list()
    elif args.command == 'reset':
        ods.cmd_reset()


if __name__ == "__main__":
    main()
