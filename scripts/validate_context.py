#!/usr/bin/env python3
"""Compatibility entry point for the context-only structural check."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arca_cli.cli import print_check
from arca_cli.core import ArcaError, validate


def main():
    try:
        result = validate(ROOT, context_only=True)
        print_check(result, context_only=True)
        return int(bool(result["errors"]))
    except (ArcaError, OSError, UnicodeError) as exc:
        print(f"ARCA: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
