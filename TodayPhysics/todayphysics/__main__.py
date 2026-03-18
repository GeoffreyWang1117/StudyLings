"""
Entry point for running todayphysics as a module.
Usage: python -m todayphysics
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .config import config
from studylings.cli import main

if __name__ == "__main__":
    main(config)
else:
    def _main():
        main(config)
