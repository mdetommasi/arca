#!/usr/bin/env python3
"""Compatibility entry point; prefer `arca checkpoint`."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arca_cli.core import ArcaError, checkpoint


def main():
    try:
        print(checkpoint(ROOT)["path"])
    except (ArcaError, OSError, UnicodeError) as exc:
        raise SystemExit(f"ARCA: {exc}") from exc


if __name__ == "__main__":
    main()
