#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

def file_hash(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def dir_hash(path: Path):
    h = hashlib.sha256()
    files = sorted(p for p in path.rglob("*") if p.is_file())
    for p in files:
        rel = p.relative_to(path).as_posix().encode()
        h.update(rel)
        h.update(b"\0")
        h.update(file_hash(p).encode())
        h.update(b"\0")
    return h.hexdigest()

if len(sys.argv) != 2:
    raise SystemExit("usage: fingerprint.py PATH")
p = Path(sys.argv[1])
if not p.exists():
    raise SystemExit(f"not found: {p}")
print(dir_hash(p) if p.is_dir() else file_hash(p))
