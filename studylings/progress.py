"""
Unified JSON-based progress tracking for studylings projects.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .exercise import Exercise, ProjectConfig, ValidationMode


class Progress:
    """Track user progress through exercises."""

    FORMAT_VERSION = 1

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.progress_file = config.get_progress_file()
        self.data = self._load()

    def _load(self) -> dict:
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Migrate from old format if needed
                data = self._migrate(data)
                return data
            except (json.JSONDecodeError, IOError):
                pass
        return self._new_data()

    def _new_data(self) -> dict:
        now = datetime.now().isoformat()
        return {
            "format_version": self.FORMAT_VERSION,
            "project": self.config.name,
            "completed": {},
            "started_at": now,
            "last_activity": now,
        }

    def _migrate(self, data: dict) -> dict:
        """Migrate from old progress formats to the unified format."""
        if "format_version" in data:
            return data

        # Old study-Economy format: {"completed": ["name1", ...], ...}
        if isinstance(data.get("completed"), list):
            now = datetime.now().isoformat()
            completed_dict = {}
            for name in data["completed"]:
                completed_dict[name] = now
            return {
                "format_version": self.FORMAT_VERSION,
                "project": self.config.name,
                "completed": completed_dict,
                "started_at": data.get("started_at", now),
                "last_activity": data.get("last_activity", now),
            }

        return data

    def _save(self):
        """Save progress to file."""
        self.data["last_activity"] = datetime.now().isoformat()
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def mark_complete(self, exercise_name: str):
        """Mark an exercise as completed."""
        if exercise_name not in self.data["completed"]:
            self.data["completed"][exercise_name] = datetime.now().isoformat()
            self._save()

    def is_complete(self, exercise_name: str) -> bool:
        """Check if an exercise is completed."""
        if self.config.validation_mode == ValidationMode.VERIFY_FUNC:
            # For verify_func mode, also check file markers
            exercises = Exercise.discover_all(self.config)
            for ex in exercises:
                if ex.name == exercise_name:
                    return ex.is_complete(self.config)
            return False

        if self.config.validation_mode == ValidationMode.COMPILE_AND_RUN:
            # For compile_and_run, check .completed file
            exercises_path = self.config.get_exercises_path()
            completed_file = exercises_path / exercise_name / ".completed"
            return completed_file.exists()

        # TEST_FILE mode: use JSON tracker
        return exercise_name in self.data["completed"]

    def get_current(self) -> Optional[str]:
        """Get the first incomplete exercise name."""
        exercises = Exercise.discover_all(self.config)
        for ex in exercises:
            if not self.is_complete(ex.name):
                return ex.name
        return None

    def get_stats(self) -> dict:
        """Get progress statistics."""
        exercises = Exercise.discover_all(self.config)
        total = len(exercises)
        completed_count = 0

        chapter_stats = {}
        for ex in exercises:
            chapter = ex.chapter
            if chapter not in chapter_stats:
                chapter_stats[chapter] = {"total": 0, "completed": 0}
            chapter_stats[chapter]["total"] += 1
            if self.is_complete(ex.name):
                chapter_stats[chapter]["completed"] += 1
                completed_count += 1

        return {
            "total": total,
            "completed": completed_count,
            "percentage": (completed_count / total * 100) if total > 0 else 0,
            "chapters": chapter_stats,
            "started_at": self.data.get("started_at"),
            "last_activity": self.data.get("last_activity"),
        }

    def reset(self, exercise_name: Optional[str] = None):
        """Reset progress for an exercise or all exercises."""
        if exercise_name:
            self.data["completed"].pop(exercise_name, None)
            # Also remove .completed file for compile_and_run mode
            if self.config.validation_mode == ValidationMode.COMPILE_AND_RUN:
                completed_file = self.config.get_exercises_path() / exercise_name / ".completed"
                if completed_file.exists():
                    completed_file.unlink()
        else:
            self.data["completed"] = {}
            # Remove all .completed files for compile_and_run mode
            if self.config.validation_mode == ValidationMode.COMPILE_AND_RUN:
                for d in self.config.get_exercises_path().iterdir():
                    cf = d / ".completed"
                    if cf.exists():
                        cf.unlink()
        self._save()

    def get_completed_exercises(self) -> list:
        """Get list of completed exercise names."""
        return list(self.data["completed"].keys())
