#!/usr/bin/env python3
"""Optional hook helper for Claude Code (and adaptable to compatible hook runtimes).

session-start:
  prints a compact project resume to stdout so it is injected in context.

pre-compact:
  copies the raw transcript, when available, into context/session_archive.
  This is only an insurance archive; structured repo memory remains canonical.
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def read_stdin_json():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}

def safe_read(path: Path, max_chars: int = 12000) -> str:
    if not path.exists():
        return f"[missing: {path.relative_to(ROOT)}]"
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[:max_chars]

def git(cmd):
    try:
        return subprocess.check_output(["git", *cmd], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as e:
        return f"[git unavailable: {e}]"

def session_start():
    parts = [
        "# Persistent project context",
        "## Git",
        git(["status", "--short", "--branch"]),
        "\nRecent commits:",
        git(["log", "-5", "--oneline"]),
        "\n## STATE.md",
        safe_read(ROOT / "context" / "STATE.md", 2600),
        "\n## NEXT.md",
        safe_read(ROOT / "context" / "NEXT.md", 1500),
        "\nInstruction: treat repository files as canonical persistent memory."
    ]
    print("\n".join(parts))

def pre_compact(payload):
    transcript = payload.get("transcript_path")
    if not transcript:
        return
    src = Path(transcript).expanduser()
    if not src.exists():
        return
    out_dir = ROOT / "context" / "session_archive"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    session_id = payload.get("session_id", "unknown")
    dst = out_dir / f"transcript-{stamp}-{session_id}.jsonl"
    shutil.copy2(src, dst)

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: agent_hook.py [session-start|pre-compact]")
    mode = sys.argv[1]
    payload = read_stdin_json()
    if mode == "session-start":
        session_start()
    elif mode == "pre-compact":
        pre_compact(payload)
    else:
        raise SystemExit(f"unknown mode: {mode}")

if __name__ == "__main__":
    main()
