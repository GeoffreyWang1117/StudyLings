"""Command-line interface for JAXlings."""

import sys
import argparse
from pathlib import Path
from .config import Config
from .runner import Runner
from .watcher import watch_mode


def main():
    """Main entry point for JAXlings CLI."""
    parser = argparse.ArgumentParser(
        description="JAXlings - Interactive JAX learning exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jaxlings verify          Run the next pending exercise
  jaxlings watch           Watch mode - auto-run on file changes
  jaxlings run intro01     Run a specific exercise
  jaxlings list            List all exercises
  jaxlings hint intro01    Show hint for an exercise
  jaxlings reset           Reset all progress
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="verify",
        choices=["verify", "watch", "run", "list", "hint", "reset", "test"],
        help="Command to execute"
    )

    parser.add_argument(
        "exercise",
        nargs="?",
        help="Exercise name (for 'run' and 'hint' commands)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    try:
        runner = Runner()

        if args.command == "verify":
            result = runner.run_next()
            if result is None:
                sys.exit(0)
            sys.exit(0 if result.passed else 1)

        elif args.command == "watch":
            print("Starting watch mode... (Press Ctrl+C to exit)")
            watch_mode(runner)

        elif args.command == "run":
            if not args.exercise:
                print("Error: Exercise name required for 'run' command")
                sys.exit(1)

            try:
                exercise = runner.config.get_exercise(args.exercise)
                result = runner.run_exercise(exercise)
                sys.exit(0 if result.passed else 1)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

        elif args.command == "list":
            runner.list_exercises()

        elif args.command == "hint":
            if not args.exercise:
                # Show hint for next pending exercise
                exercise = runner.progress.get_next_pending(
                    runner.config.get_all_exercises()
                )
                if exercise:
                    runner.show_hint(exercise.name)
                else:
                    print("No pending exercises!")
            else:
                runner.show_hint(args.exercise)

        elif args.command == "reset":
            confirm = input("Reset all progress? (y/N): ")
            if confirm.lower() == 'y':
                runner.reset_progress()

        elif args.command == "test":
            # Run all exercises (for testing)
            success = runner.run_all()
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
