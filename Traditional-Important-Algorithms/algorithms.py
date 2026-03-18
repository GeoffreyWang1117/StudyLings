#!/usr/bin/env python3
"""
Traditional Important Algorithms - Python Exercise Runner

Interactive CLI for running algorithm exercises in Python.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple
import toml
from dataclasses import dataclass

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

@dataclass
class Exercise:
    name: str
    path: str
    mode: str
    hint: str

def colored(text: str, color: str) -> str:
    """Return colored text."""
    return f"{color}{text}{Colors.END}"

def bold(text: str) -> str:
    """Return bold text."""
    return f"{Colors.BOLD}{text}{Colors.END}"

def load_exercises() -> List[Exercise]:
    """Load exercise information from info.toml."""
    try:
        with open('info.toml', 'r') as f:
            data = toml.load(f)
            exercises = []
            for ex in data['exercises']:
                # Convert Rust path to Python path
                py_path = ex['path'].replace('exercises/', 'exercises_py/').replace('.rs', '.py')
                exercises.append(Exercise(
                    name=ex['name'],
                    path=py_path,
                    mode=ex['mode'],
                    hint=ex['hint']
                ))
            return exercises
    except FileNotFoundError:
        print(colored(bold("ERROR:"), Colors.RED), "info.toml not found")
        sys.exit(1)
    except Exception as e:
        print(colored(bold("ERROR:"), Colors.RED), f"Failed to load exercises: {e}")
        sys.exit(1)

def get_exercise_status(exercise: Exercise) -> str:
    """Get the status of an exercise."""
    path = Path(exercise.path)

    if not path.exists():
        return "missing"

    try:
        with open(path, 'r') as f:
            content = f.read()
            if "# I AM NOT DONE" in content:
                return "pending"

            # Try to run the tests
            result = subprocess.run(
                [sys.executable, str(path)],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                return "done"
            else:
                return "failed"
    except subprocess.TimeoutExpired:
        return "failed"
    except Exception:
        return "failed"

def verify_exercise(exercise: Exercise) -> bool:
    """Verify an exercise by running its tests."""
    print(colored(bold("INFO:"), Colors.BLUE), f"Verifying {exercise.name}...")

    path = Path(exercise.path)
    if not path.exists():
        print(colored(bold("ERROR:"), Colors.RED), f"Exercise file not found: {exercise.path}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(path), '-v'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(colored(bold("SUCCESS:"), Colors.GREEN), f"{exercise.name} passed all tests!")
            return True
        else:
            print(colored(bold("FAILED:"), Colors.RED), f"{exercise.name} failed tests")
            print("\nOutput:")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            print(f"\n{colored(bold('HINT:'), Colors.YELLOW)} Run 'python3 algorithms.py hint {exercise.name}' to see the hint")
            return False
    except subprocess.TimeoutExpired:
        print(colored(bold("ERROR:"), Colors.RED), "Test execution timed out")
        return False
    except Exception as e:
        print(colored(bold("ERROR:"), Colors.RED), f"Failed to verify: {e}")
        return False

def watch_exercise(exercise: Exercise):
    """Watch an exercise and re-run tests on changes."""
    print(colored(bold("INFO:"), Colors.BLUE), f"Watching {exercise.name}. Press Ctrl+C to exit.")
    print(colored(bold("INFO:"), Colors.BLUE), "Modify the file and save to trigger verification.\n")

    path = Path(exercise.path)
    last_mtime = path.stat().st_mtime if path.exists() else 0

    try:
        while True:
            time.sleep(2)
            if path.exists():
                current_mtime = path.stat().st_mtime
                if current_mtime != last_mtime:
                    last_mtime = current_mtime
                    print("\n" + "="*50)
                    if verify_exercise(exercise):
                        print(f"\n{colored(bold('SUCCESS:'), Colors.GREEN)} {exercise.name} is complete!")
                        break
                    print("="*50 + "\n")
    except KeyboardInterrupt:
        print(f"\n{colored(bold('INFO:'), Colors.BLUE)} Stopped watching.")

def run_all_exercises(exercises: List[Exercise]):
    """Run all exercises and show progress."""
    print(colored(bold("INFO:"), Colors.BLUE), "Running all exercises...\n")

    passed = 0
    failed = 0
    pending = 0
    missing = 0

    for i, exercise in enumerate(exercises, 1):
        status = get_exercise_status(exercise)

        if status == "done":
            passed += 1
            print(f"  {colored('✓', Colors.GREEN)} {exercise.name}")
        elif status == "pending":
            pending += 1
            print(f"  {colored('○', Colors.YELLOW)} {exercise.name} (pending)")
        elif status == "failed":
            failed += 1
            print(f"  {colored('✗', Colors.RED)} {exercise.name} (failed)")
        else:
            missing += 1
            print(f"  {colored('?', Colors.YELLOW)} {exercise.name} (missing)")

        # Show progress
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(exercises)}")

    print(f"\n{bold('Summary:')}")
    print(f"  {colored('✓', Colors.GREEN)} Passed: {passed}")
    print(f"  {colored('✗', Colors.RED)} Failed: {failed}")
    print(f"  {colored('○', Colors.YELLOW)} Pending: {pending}")
    if missing > 0:
        print(f"  {colored('?', Colors.YELLOW)} Missing: {missing}")

    if passed == len(exercises):
        print(f"\n{colored(bold('SUCCESS:'), Colors.GREEN)} All exercises complete! 🎉")

def show_hint(exercise: Exercise):
    """Show hint for an exercise."""
    print(colored(bold(f"HINT for {exercise.name}:"), Colors.YELLOW))
    print(f"\n{exercise.hint}")

def list_exercises(exercises: List[Exercise]):
    """List all exercises grouped by category."""
    print(colored(bold("Available Exercises:\n"), Colors.GREEN))

    categories = [
        ("01_gc_and_memory", "🧩 Garbage Collection and Memory Management"),
        ("02_memory_models", "🧩 Memory Models and Safety Mechanisms"),
        ("03_concurrency", "🧩 Concurrency and Scheduling"),
        ("04_os_algorithms", "🧩 Operating System Algorithms"),
        ("05_compiler", "🧩 Compiler and Runtime Mechanisms"),
        ("06_distributed_systems", "🧩 Network and Distributed Systems"),
        ("07_cryptography", "🔐 Cryptography and Security"),
        ("08_database", "💾 Database and Storage"),
        ("09_rate_limiting", "🚦 Rate Limiting and Fault Tolerance"),
        ("10_string_algorithms", "📝 String and Text Processing"),
        ("11_stream_processing", "🌊 Stream Processing"),
        ("12_graph_algorithms", "🕸️ Graph Algorithms"),
        ("13_data_structures", "🌳 Data Structures"),
        ("14_ml_fundamentals", "🤖 Machine Learning Fundamentals"),
    ]

    for category_path, category_name in categories:
        print(colored(bold(category_name), Colors.CYAN))

        category_exercises = [ex for ex in exercises if category_path in ex.path]
        for exercise in category_exercises:
            status = get_exercise_status(exercise)

            if status == "done":
                icon = colored("✓", Colors.GREEN)
            elif status == "pending":
                icon = colored("○", Colors.YELLOW)
            elif status == "failed":
                icon = colored("✗", Colors.RED)
            else:
                icon = colored("?", Colors.YELLOW)

            print(f"  {icon} {exercise.name} - {exercise.path}")

        print()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Interactive exercises for traditional and important algorithms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 algorithms.py list                    # List all exercises
  python3 algorithms.py verify gc01_reference_counting
  python3 algorithms.py watch gc01_reference_counting
  python3 algorithms.py hint gc01_reference_counting
  python3 algorithms.py run                     # Run all exercises
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List command
    subparsers.add_parser('list', help='List all exercises')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a specific exercise')
    verify_parser.add_argument('name', help='Exercise name')

    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Watch an exercise and re-run on changes')
    watch_parser.add_argument('name', help='Exercise name')

    # Hint command
    hint_parser = subparsers.add_parser('hint', help='Show a hint for an exercise')
    hint_parser.add_argument('name', help='Exercise name')

    # Run command
    subparsers.add_parser('run', help='Run all exercises')

    args = parser.parse_args()

    if not args.command:
        print(colored(bold("Welcome to Traditional Important Algorithms!"), Colors.GREEN))
        print(f"\nUse {colored('python3 algorithms.py --help', Colors.YELLOW)} to see available commands.")
        print(f"Use {colored('python3 algorithms.py list', Colors.YELLOW)} to list all exercises.")
        print(f"Use {colored('python3 algorithms.py verify <name>', Colors.YELLOW)} to verify an exercise.")
        return

    exercises = load_exercises()

    if args.command == 'list':
        list_exercises(exercises)
    elif args.command == 'verify':
        exercise = next((ex for ex in exercises if ex.name == args.name), None)
        if not exercise:
            print(colored(bold("ERROR:"), Colors.RED), f"Exercise '{args.name}' not found")
            return
        verify_exercise(exercise)
    elif args.command == 'watch':
        exercise = next((ex for ex in exercises if ex.name == args.name), None)
        if not exercise:
            print(colored(bold("ERROR:"), Colors.RED), f"Exercise '{args.name}' not found")
            return
        watch_exercise(exercise)
    elif args.command == 'hint':
        exercise = next((ex for ex in exercises if ex.name == args.name), None)
        if not exercise:
            print(colored(bold("ERROR:"), Colors.RED), f"Exercise '{args.name}' not found")
            return
        show_hint(exercise)
    elif args.command == 'run':
        run_all_exercises(exercises)

if __name__ == '__main__':
    main()
