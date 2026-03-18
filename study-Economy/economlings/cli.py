"""
Command-line interface for Economlings.
Delegates to the studylings framework.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .config import config
from studylings.cli import main as _main, create_cli


def main():
    """Main entry point."""
    _main(config)


cli = create_cli(config)

if __name__ == "__main__":
    main()
