#!/usr/bin/env python3
"""Compatibility entry point; prefer `arca check`."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arca_cli.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["--root", str(ROOT), "check", *sys.argv[1:]]))
