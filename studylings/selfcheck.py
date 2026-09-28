"""
Maintainer self-check for BUILD_AND_PROBE projects.

    python -m studylings.selfcheck Unixlings [name ...]

For every exercise it verifies two things:
  1. the reference solution (preset "solutions") builds and passes its probe;
  2. the unmodified exercise (preset "dev") does NOT pass — otherwise there is nothing to learn.
"""

import argparse
import importlib
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .checker import BuildAndProbeChecker
from .exercise import Exercise


def load_config(project_dir: Path):
    sys.path.insert(0, str(project_dir))
    for pkg in project_dir.iterdir():
        if (pkg / "config.py").exists():
            return importlib.import_module(f"{pkg.name}.config").config
    raise SystemExit(f"{project_dir} 下找不到 <package>/config.py")


def check_one(ex, config):
    sol = BuildAndProbeChecker(ex, config, preset="solutions")
    r = sol.build()
    if r:
        r = sol.probe()
    solution_ok = bool(r)
    solution_msg = "" if r else f"{r.message}\n{r.details}"

    dev = BuildAndProbeChecker(ex, config, preset="dev")
    d = dev.build()
    if d:
        d = dev.probe()
    exercise_fails = not d
    return ex, solution_ok, solution_msg, exercise_fails, d.message


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("names", nargs="*")
    ap.add_argument("-j", "--jobs", type=int, default=1)
    args = ap.parse_args()

    config = load_config(Path(args.project).resolve())
    exercises = Exercise.discover_all(config)
    if args.names:
        exercises = [e for e in exercises if e.name in args.names]

    # Configure both trees once up front so parallel builds don't race on configure
    for preset in ("solutions", "dev"):
        BuildAndProbeChecker(exercises[0], config, preset=preset).build()

    bad = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for ex, sol_ok, sol_msg, ex_fails, ex_msg in pool.map(lambda e: check_one(e, config), exercises):
            status = ("OK " if sol_ok else "SOL") + ("" if ex_fails else " EX-PASSES")
            print(f"[{status:>13}] {ex.chapter}/{ex.name}  (exercise: {ex_msg})", flush=True)
            if not sol_ok:
                print("    " + sol_msg.replace("\n", "\n    "))
            if not sol_ok or not ex_fails:
                bad += 1
    print(f"\n{len(exercises) - bad}/{len(exercises)} exercises healthy")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
