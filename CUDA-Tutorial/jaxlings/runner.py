"""Exercise runner and progress tracker."""

import json
from pathlib import Path
from typing import List, Optional
from .exercise import Exercise, ExerciseResult
from .config import Config


class ProgressTracker:
    """Tracks user progress through exercises."""

    def __init__(self, progress_file: Path = None):
        if progress_file is None:
            progress_file = Path.home() / ".jaxlings_progress.json"

        self.progress_file = progress_file
        self.completed: List[str] = []
        self._load_progress()

    def _load_progress(self):
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.completed = data.get("completed", [])
            except Exception:
                self.completed = []

    def _save_progress(self):
        """Save progress to file."""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump({"completed": self.completed}, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")

    def mark_completed(self, exercise_name: str):
        """Mark an exercise as completed."""
        if exercise_name not in self.completed:
            self.completed.append(exercise_name)
            self._save_progress()

    def is_completed(self, exercise_name: str) -> bool:
        """Check if an exercise is completed."""
        return exercise_name in self.completed

    def reset(self):
        """Reset all progress."""
        self.completed = []
        self._save_progress()

    def get_next_pending(self, exercises: List[Exercise]) -> Optional[Exercise]:
        """Get the next pending exercise."""
        for exercise in exercises:
            if not self.is_completed(exercise.name):
                return exercise
        return None


class Runner:
    """Runs exercises and manages the learning flow."""

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.progress = ProgressTracker()

    def run_exercise(self, exercise: Exercise, verbose: bool = True) -> ExerciseResult:
        """Run a single exercise."""
        if verbose:
            print(f"\n{'='*60}")
            print(f"Running: {exercise.name}")
            print(f"Path: {exercise.path}")
            print(f"{'='*60}\n")

        result = exercise.check()

        if result.passed:
            self.progress.mark_completed(exercise.name)
            if verbose:
                print(f"\n✓ Exercise {exercise.name} passed!")
        else:
            if verbose:
                print(f"\n✗ Exercise {exercise.name} failed!")
                if result.error:
                    print(f"Error: {result.error}")
                if result.output:
                    print(f"\nOutput:\n{result.output}")

        return result

    def run_all(self) -> bool:
        """Run all exercises."""
        exercises = self.config.get_all_exercises()
        total = len(exercises)
        passed = 0

        for exercise in exercises:
            result = self.run_exercise(exercise, verbose=False)
            if result.passed:
                passed += 1
                print(f"✓ {exercise.name}")
            else:
                print(f"✗ {exercise.name}")

        print(f"\nResults: {passed}/{total} exercises passed")
        return passed == total

    def run_next(self) -> Optional[ExerciseResult]:
        """Run the next pending exercise."""
        exercise = self.progress.get_next_pending(self.config.get_all_exercises())

        if exercise is None:
            print("\n🎉 Congratulations! You've completed all exercises!")
            return None

        return self.run_exercise(exercise)

    def show_hint(self, exercise_name: str):
        """Show hint for an exercise."""
        try:
            exercise = self.config.get_exercise(exercise_name)
            print(f"\n💡 Hint for {exercise_name}:")
            print(f"{exercise.get_hint()}\n")
        except ValueError as e:
            print(f"Error: {e}")

    def list_exercises(self):
        """List all exercises with their status."""
        exercises = self.config.get_all_exercises()

        print("\nJAXlings Exercises:")
        print("=" * 60)

        for i, exercise in enumerate(exercises, 1):
            status = "✓" if self.progress.is_completed(exercise.name) else "○"
            print(f"{i:2d}. {status} {exercise.name}")

        completed = len([e for e in exercises if self.progress.is_completed(e.name)])
        print(f"\nProgress: {completed}/{len(exercises)} completed")

    def reset_progress(self):
        """Reset all progress."""
        self.progress.reset()
        print("Progress reset successfully!")
