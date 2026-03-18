"""
Exercise discovery, metadata parsing, and configuration for studylings projects.
"""

import enum
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class ValidationMode(enum.Enum):
    """How exercises are validated."""
    TEST_FILE = "test_file"           # External test files (study-Economy style)
    VERIFY_FUNC = "verify_func"       # Embedded verify() + markers (TodayPhysics style)
    COMPILE_AND_RUN = "compile_and_run"  # TODO/??? markers + cmake build (Vulkan-Study style)


@dataclass
class ProjectConfig:
    """Configuration for a studylings project."""
    name: str                          # e.g. "economlings"
    display_name: str                  # e.g. "Economlings - 经济学交互式学习系统"
    version: str
    validation_mode: ValidationMode
    exercises_dir: str = "exercises"   # relative to project root
    tests_dir: Optional[str] = None   # only for TEST_FILE mode
    solutions_dir: Optional[str] = None
    project_root: Optional[Path] = None
    chapters: dict = field(default_factory=dict)
    banner: str = ""
    file_extension: str = ".py"       # ".py" or ".cpp"
    build_command: Optional[str] = None  # for COMPILE_AND_RUN mode
    build_dir: Optional[str] = None     # for COMPILE_AND_RUN mode
    comment_prefix: str = "#"           # "#" for Python, "//" for C++
    todo_markers: list = field(default_factory=lambda: ["TODO:"])
    incomplete_markers: list = field(default_factory=lambda: ["I AM NOT DONE"])
    placeholder_markers: list = field(default_factory=lambda: [])  # e.g. ["/* ??? */"]
    run_timeout: int = 10              # seconds for execution timeout

    def get_exercises_path(self) -> Path:
        return self.project_root / self.exercises_dir

    def get_tests_path(self) -> Optional[Path]:
        if self.tests_dir:
            return self.project_root / self.tests_dir
        return None

    def get_progress_file(self) -> Path:
        return self.project_root / f".studylings_progress.json"


@dataclass
class Exercise:
    """Represents a single exercise."""
    name: str
    path: Path
    chapter: str
    difficulty: str = "★☆☆☆☆"
    topic: str = "Unknown"
    title: str = ""
    description: str = ""
    hints: list = field(default_factory=list)

    @classmethod
    def discover_all(cls, config: ProjectConfig) -> list["Exercise"]:
        """Discover all exercises for a project."""
        exercises = []
        exercises_path = config.get_exercises_path()
        if not exercises_path.exists():
            return exercises

        for chapter_dir in sorted(exercises_path.iterdir()):
            if not chapter_dir.is_dir() or chapter_dir.name.startswith("_"):
                continue
            chapter_name = chapter_dir.name

            if config.file_extension in (".cpp", ".cu", ".c"):
                # C/C++/CUDA exercises: each directory has a main file
                for main_name in [f"main{config.file_extension}", "main.cpp"]:
                    main_file = chapter_dir / main_name
                    if main_file.exists():
                        ex = cls._from_cpp_file(main_file, chapter_name, config)
                        exercises.append(ex)
                        break
                else:
                    # Try individual files in the chapter directory
                    found_files = False
                    for ex_file in sorted(chapter_dir.glob(f"*{config.file_extension}")):
                        if ex_file.name.startswith("_"):
                            continue
                        found_files = True
                        ex = cls._from_cpp_file(ex_file, chapter_name, config)
                        ex.name = ex_file.stem
                        exercises.append(ex)

                    # Try subdirectories (e.g., exercise-1/, exercise-2/)
                    if not found_files:
                        for sub_dir in sorted(chapter_dir.iterdir()):
                            if not sub_dir.is_dir() or sub_dir.name.startswith("_"):
                                continue
                            for ext in [config.file_extension, ".cpp", ".c"]:
                                sub_files = sorted(sub_dir.glob(f"*{ext}"))
                                if sub_files:
                                    ex = cls._from_cpp_file(sub_files[0], chapter_name, config)
                                    ex.name = f"{chapter_name}/{sub_dir.name}"
                                    exercises.append(ex)
                                    break
            else:
                # Python/TypeScript exercises: each file in the chapter dir
                for ex_file in sorted(chapter_dir.glob(f"*{config.file_extension}")):
                    if ex_file.name.startswith("_"):
                        continue
                    ex = cls._from_python_file(ex_file, chapter_name, config)
                    exercises.append(ex)

        return exercises

    @classmethod
    def _from_python_file(cls, filepath: Path, chapter: str, config: ProjectConfig) -> "Exercise":
        """Parse a Python/TypeScript exercise file for metadata."""
        ex = cls(name=filepath.stem, path=filepath, chapter=chapter)
        try:
            content = filepath.read_text(encoding="utf-8")[:3000]
        except Exception:
            return ex

        if config.file_extension == ".ts":
            # TypeScript: use comment-based metadata with // prefix
            ex._parse_comment_metadata(content, "//")
            # Also try docstring-style from JSDoc comments
            if ex.topic == "Unknown":
                ex._parse_docstring_metadata(content)
        elif config.validation_mode == ValidationMode.VERIFY_FUNC:
            # TodayPhysics style: metadata in docstring
            ex._parse_docstring_metadata(content)
        else:
            # study-Economy style: metadata in comments
            ex._parse_comment_metadata(content, config.comment_prefix)

        return ex

    @classmethod
    def _from_cpp_file(cls, filepath: Path, chapter: str, config: ProjectConfig) -> "Exercise":
        """Parse a C++ exercise file for metadata."""
        ex = cls(name=chapter, path=filepath, chapter=chapter)
        # Use chapter display name as default topic
        ex.topic = config.chapters.get(chapter, chapter)
        try:
            content = filepath.read_text(encoding="utf-8")[:3000]
        except Exception:
            return ex

        # Parse C++ block comment metadata
        ex._parse_cpp_metadata(content)
        return ex

    def _parse_comment_metadata(self, content: str, prefix: str = "#"):
        """Parse metadata from comment-style headers (study-Economy)."""
        match = re.search(rf"{re.escape(prefix)}\s*DIFFICULTY:\s*(.+)", content)
        if match:
            self.difficulty = match.group(1).strip()

        match = re.search(rf"{re.escape(prefix)}\s*TOPIC:\s*(.+)", content)
        if match:
            self.topic = match.group(1).strip()

        match = re.search(rf"{re.escape(prefix)}\s*EXERCISE:\s*(.+)", content)
        if match:
            self.title = match.group(1).strip()

        # Parse description
        lines = content.split("\n")
        desc_lines = []
        in_desc = False
        for line in lines:
            if "说明：" in line or "说明:" in line or "Description:" in line:
                in_desc = True
                continue
            if in_desc:
                if line.startswith(prefix):
                    desc_lines.append(line.lstrip(prefix).strip())
                elif line.strip() == "":
                    continue
                else:
                    break
        self.description = "\n".join(desc_lines)

        # Parse hints
        hint_matches = re.findall(rf"{re.escape(prefix)}\s*HINT(?:\d*):\s*(.+)", content)
        if hint_matches:
            self.hints = hint_matches

    def _parse_docstring_metadata(self, content: str):
        """Parse metadata from docstring (TodayPhysics style)."""
        lines = content.split("\n")
        in_docstring = False
        docstring_lines = []

        for line in lines:
            if '"""' in line or "'''" in line:
                if in_docstring:
                    break
                in_docstring = True
                continue
            if in_docstring:
                docstring_lines.append(line)

        self.description = "\n".join(docstring_lines)

        if docstring_lines:
            self.title = docstring_lines[0].strip()
            # Use the title as topic if no explicit TOPIC found
            if self.title:
                self.topic = self.title

        for line in docstring_lines:
            if "难度" in line or "Difficulty" in line:
                self.difficulty = line.split(":")[-1].strip()
            if "HINT:" in line or "提示:" in line:
                self.hints.append(line.split(":", 1)[-1].strip())

    def _parse_cpp_metadata(self, content: str):
        """Parse metadata from C++ block comments."""
        # Look for block comment header
        match = re.search(r"/\*\*(.*?)\*/", content, re.DOTALL)
        if match:
            block = match.group(1)
            lines = block.split("\n")
            # First meaningful line is title
            for line in lines:
                stripped = line.strip().lstrip("* ").strip()
                if stripped and "练习" in stripped:
                    self.title = stripped
                    break

        # Parse hints from HINT.md if present
        hint_file = self.path.parent / "HINT.md"
        if hint_file.exists():
            try:
                self.hints = [hint_file.read_text(encoding="utf-8")]
            except Exception:
                pass

    def is_complete(self, config: ProjectConfig, content: Optional[str] = None) -> bool:
        """Check if exercise is complete based on validation mode."""
        if config.validation_mode == ValidationMode.COMPILE_AND_RUN:
            # Check .completed file
            completed_file = self.path.parent / ".completed"
            return completed_file.exists()

        # For Python exercises, check file content for markers
        if content is None:
            try:
                content = self.path.read_text(encoding="utf-8")
            except Exception:
                return False

        if config.validation_mode == ValidationMode.VERIFY_FUNC:
            # Check for TODO and I AM NOT DONE markers using project's comment prefix
            prefix = config.comment_prefix
            for marker in config.todo_markers:
                if f"{prefix} {marker}" in content:
                    return False
            for marker in config.incomplete_markers:
                if f"{prefix} {marker}" in content:
                    return False
            # Also check for placeholder markers
            for marker in config.placeholder_markers:
                if marker in content:
                    return False
            return True

        # TEST_FILE mode: rely on progress tracking (JSON)
        return False  # Caller should check progress tracker

    def get_hint(self, level: int = 0) -> str:
        """Get hint at specified level."""
        if level < len(self.hints):
            return self.hints[level]
        return "没有更多提示了 No more hints available"


def find_exercise(name: str, config: ProjectConfig) -> Optional[Exercise]:
    """Find an exercise by name."""
    exercises = Exercise.discover_all(config)
    for ex in exercises:
        if ex.name == name or name in str(ex.path):
            return ex
    return None
