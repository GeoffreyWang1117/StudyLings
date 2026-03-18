"""
Utility functions for Economlings.
"""

import os
import re
from pathlib import Path
from typing import Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
EXERCISES_DIR = PROJECT_ROOT / "exercises"
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"
PROGRESS_FILE = PROJECT_ROOT / ".economlings_progress.json"


def get_exercise_dirs() -> list[Path]:
    """Get all exercise directories in order."""
    if not EXERCISES_DIR.exists():
        return []
    dirs = sorted([d for d in EXERCISES_DIR.iterdir() if d.is_dir()])
    return dirs


def get_all_exercises() -> list[dict]:
    """Get all exercises with their metadata."""
    exercises = []
    for chapter_dir in get_exercise_dirs():
        chapter_name = chapter_dir.name
        for exercise_file in sorted(chapter_dir.glob("*.py")):
            if exercise_file.name.startswith("_"):
                continue
            metadata = parse_exercise_metadata(exercise_file)
            exercises.append({
                "name": exercise_file.stem,
                "path": exercise_file,
                "chapter": chapter_name,
                **metadata
            })
    return exercises


def parse_exercise_metadata(filepath: Path) -> dict:
    """Parse exercise metadata from file header."""
    metadata = {
        "difficulty": "★☆☆☆☆",
        "topic": "Unknown",
        "description": "",
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(2000)  # Read first 2000 chars for metadata

        # Parse DIFFICULTY
        match = re.search(r"#\s*DIFFICULTY:\s*(.+)", content)
        if match:
            metadata["difficulty"] = match.group(1).strip()

        # Parse TOPIC
        match = re.search(r"#\s*TOPIC:\s*(.+)", content)
        if match:
            metadata["topic"] = match.group(1).strip()

        # Parse description (lines starting with # after TOPIC until empty line or code)
        lines = content.split("\n")
        desc_lines = []
        in_desc = False
        for line in lines:
            if "说明：" in line or "Description:" in line:
                in_desc = True
                continue
            if in_desc:
                if line.startswith("#"):
                    desc_lines.append(line.lstrip("#").strip())
                elif line.strip() == "":
                    continue
                else:
                    break
        metadata["description"] = "\n".join(desc_lines)

    except Exception:
        pass

    return metadata


def find_exercise(name: str) -> Optional[Path]:
    """Find an exercise by name."""
    for chapter_dir in get_exercise_dirs():
        exercise_path = chapter_dir / f"{name}.py"
        if exercise_path.exists():
            return exercise_path
    return None


def get_chapter_name(chapter_dir: str) -> str:
    """Get human-readable chapter name."""
    chapter_names = {
        "01_basics": "第1章：基础概念",
        "02_microeconomics": "第2章：微观经济学",
        "03_macroeconomics": "第3章：宏观经济学",
        "04_finance": "第4章：金融经济学",
        "05_econometrics": "第5章：计量经济学",
        "06_advanced": "第6章：高级模型",
        "07_international": "第7章：国际经济学",
        "08_public": "第8章：公共经济学",
        "09_behavioral": "第9章：行为经济学",
        "10_development": "第10章：发展经济学",
    }
    return chapter_names.get(chapter_dir, chapter_dir)


def check_cuda_available() -> bool:
    """Check if CUDA is available."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def format_difficulty(stars: str) -> str:
    """Format difficulty stars with color."""
    filled = stars.count("★")
    return f"[yellow]{'★' * filled}[/yellow][dim]{'☆' * (5 - filled)}[/dim]"
