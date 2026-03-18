"""
Economlings - Interactive Economics Learning System
An interactive learning system for economics, similar to Rustlings.
"""

__version__ = "0.1.0"
__author__ = "Economlings Team"

# Keep backward compatibility for exercise files that import check()
from .checker import check

__all__ = ["check", "__version__"]
