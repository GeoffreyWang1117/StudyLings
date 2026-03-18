"""
Progress tracking for Economlings.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .utils import PROGRESS_FILE, get_all_exercises


class Progress:
    """Track user progress through exercises."""

    def __init__(self):
        self.progress_file = PROGRESS_FILE
        self.data = self._load()

    def _load(self) -> dict:
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "completed": [],
            "current": None,
            "started_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
        }

    def _save(self):
        """Save progress to file."""
        self.data["last_activity"] = datetime.now().isoformat()
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def mark_complete(self, exercise_name: str):
        """Mark an exercise as completed."""
        if exercise_name not in self.data["completed"]:
            self.data["completed"].append(exercise_name)
            self._save()

    def is_complete(self, exercise_name: str) -> bool:
        """Check if an exercise is completed."""
        return exercise_name in self.data["completed"]

    def get_current(self) -> Optional[str]:
        """Get the current exercise (first incomplete one)."""
        exercises = get_all_exercises()
        for ex in exercises:
            if ex["name"] not in self.data["completed"]:
                return ex["name"]
        return None

    def set_current(self, exercise_name: str):
        """Set the current exercise."""
        self.data["current"] = exercise_name
        self._save()

    def get_stats(self) -> dict:
        """Get progress statistics."""
        exercises = get_all_exercises()
        total = len(exercises)
        completed = len(self.data["completed"])

        # Count by chapter
        chapter_stats = {}
        for ex in exercises:
            chapter = ex["chapter"]
            if chapter not in chapter_stats:
                chapter_stats[chapter] = {"total": 0, "completed": 0}
            chapter_stats[chapter]["total"] += 1
            if ex["name"] in self.data["completed"]:
                chapter_stats[chapter]["completed"] += 1

        return {
            "total": total,
            "completed": completed,
            "percentage": (completed / total * 100) if total > 0 else 0,
            "chapters": chapter_stats,
            "started_at": self.data.get("started_at"),
            "last_activity": self.data.get("last_activity"),
        }

    def reset(self, exercise_name: Optional[str] = None):
        """Reset progress for an exercise or all exercises."""
        if exercise_name:
            if exercise_name in self.data["completed"]:
                self.data["completed"].remove(exercise_name)
        else:
            self.data["completed"] = []
            self.data["current"] = None
        self._save()

    def get_completed_exercises(self) -> list[str]:
        """Get list of completed exercise names."""
        return self.data["completed"].copy()
