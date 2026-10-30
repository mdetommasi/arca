#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "context" / "session_archive"

def git(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception:
        return "unknown"

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT.mkdir(parents=True, exist_ok=True)

state = (ROOT / "context" / "STATE.md").read_text(encoding="utf-8")
nxt = (ROOT / "context" / "NEXT.md").read_text(encoding="utf-8")
branch = git(["branch", "--show-current"])
commit = git(["rev-parse", "HEAD"])
status = git(["status", "--short"])

content = f"""# Context checkpoint {stamp}

Branch: {branch}
Commit: {commit}

## Git status

```text
{status}
```

## STATE

{state}

## NEXT

{nxt}
"""
path = OUT / f"checkpoint-{stamp}.md"
path.write_text(content, encoding="utf-8")
print(path)
