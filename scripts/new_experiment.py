#!/usr/bin/env python3
"""Compatibility entry point; prefer `arca experiment new`."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arca_cli.core import ArcaError, new_experiment


def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: new_experiment.py "experiment title"')
    try:
        print(new_experiment(ROOT, " ".join(sys.argv[1:]))["path"])
    except (ArcaError, OSError, UnicodeError) as exc:
        raise SystemExit(f"ARCA: {exc}") from exc


if __name__ == "__main__":
    main()
