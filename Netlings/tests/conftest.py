import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # suite root → studylings

from studylings.probe import *  # noqa: E402,F401,F403  (provides the `exe` fixture)
