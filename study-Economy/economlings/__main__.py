"""
Entry point for running economlings as a module.
Usage: python -m economlings
"""

from .config import config

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings.cli import main

if __name__ == "__main__":
    main(config)
else:
    # When imported as a module (e.g. from .cli import main), provide the entry
    def _main():
        main(config)
