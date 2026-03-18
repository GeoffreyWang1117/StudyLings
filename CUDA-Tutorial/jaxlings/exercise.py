"""Exercise management and execution."""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExerciseResult:
    """Result of running an exercise."""
    passed: bool
    output: str
    error: Optional[str] = None


class Exercise:
    """Represents a single JAX exercise."""

    def __init__(self, name: str, path: str, mode: str, hint: str):
        self.name = name
        self.path = Path(path)
        self.mode = mode
        self.hint = hint

    def check(self) -> ExerciseResult:
        """Run the exercise and check if it passes."""
        if not self.path.exists():
            return ExerciseResult(
                passed=False,
                output="",
                error=f"Exercise file not found: {self.path}"
            )

        if self.mode == "test":
            return self._run_pytest()
        else:
            return self._run_compile()

    def _run_pytest(self) -> ExerciseResult:
        """Run pytest on the exercise file."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(self.path), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=30
            )

            passed = result.returncode == 0
            output = result.stdout + result.stderr

            return ExerciseResult(
                passed=passed,
                output=output,
                error=None if passed else "Tests failed"
            )
        except subprocess.TimeoutExpired:
            return ExerciseResult(
                passed=False,
                output="",
                error="Exercise timed out (30s limit)"
            )
        except Exception as e:
            return ExerciseResult(
                passed=False,
                output="",
                error=f"Error running exercise: {str(e)}"
            )

    def _run_compile(self) -> ExerciseResult:
        """Check if the exercise compiles without errors."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(self.path)],
                capture_output=True,
                text=True,
                timeout=10
            )

            passed = result.returncode == 0

            return ExerciseResult(
                passed=passed,
                output=result.stdout,
                error=None if passed else result.stderr
            )
        except Exception as e:
            return ExerciseResult(
                passed=False,
                output="",
                error=f"Error compiling exercise: {str(e)}"
            )

    def get_hint(self) -> str:
        """Get the hint for this exercise."""
        return self.hint

    def __repr__(self) -> str:
        return f"Exercise(name='{self.name}', path='{self.path}')"
