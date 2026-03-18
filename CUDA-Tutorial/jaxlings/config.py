"""Configuration management for JAXlings."""

import toml
from pathlib import Path
from typing import List, Dict, Any
from .exercise import Exercise


class Config:
    """Manages JAXlings configuration."""

    def __init__(self, config_path: Path = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "exercises.toml"

        self.config_path = config_path
        self.exercises: List[Exercise] = []
        self._load_config()

    def _load_config(self):
        """Load configuration from TOML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        data = toml.load(self.config_path)

        for ex_data in data.get("exercises", []):
            exercise = Exercise(
                name=ex_data["name"],
                path=ex_data["path"],
                mode=ex_data.get("mode", "test"),
                hint=ex_data.get("hint", "No hint available.")
            )
            self.exercises.append(exercise)

    def get_exercise(self, name: str) -> Exercise:
        """Get an exercise by name."""
        for exercise in self.exercises:
            if exercise.name == name:
                return exercise
        raise ValueError(f"Exercise not found: {name}")

    def get_all_exercises(self) -> List[Exercise]:
        """Get all exercises."""
        return self.exercises

    def get_next_exercise(self, current: str = None) -> Exercise:
        """Get the next pending exercise."""
        if current is None:
            return self.exercises[0] if self.exercises else None

        for i, ex in enumerate(self.exercises):
            if ex.name == current and i + 1 < len(self.exercises):
                return self.exercises[i + 1]

        return None
