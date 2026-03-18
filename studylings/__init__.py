"""
Studylings - A shared framework for rustlings-style educational projects.
"""

__version__ = "0.1.0"

from .exercise import Exercise, ValidationMode, ProjectConfig

__all__ = ["Exercise", "ValidationMode", "ProjectConfig", "__version__"]
