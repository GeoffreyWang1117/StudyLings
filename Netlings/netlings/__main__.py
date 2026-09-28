from .config import config  # also puts the suite root on sys.path

from studylings.cli import main

if __name__ == "__main__":
    main(config)
