#!/usr/bin/env python3
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

required = [
    "AGENTS.md",
    "CLAUDE.md",
    "research/CHARTER.md",
    "context/STATE.md",
    "context/NEXT.md",
    "research/LAB_NOTEBOOK.md",
    "research/FINDINGS.md",
    "research/CONTRADICTIONS.md",
    "experiments/REGISTRY.csv",
    "artifacts/manifest.jsonl",
    "paper/CLAIMS.md",
]

for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

registry = ROOT / "experiments" / "REGISTRY.csv"
known_experiments = set()
if registry.exists():
    with registry.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            eid = row.get("experiment_id", "").strip()
            if eid:
                known_experiments.add(eid)
                report = row.get("report_path", "").strip()
                config = row.get("config_path", "").strip()
                if report and not (ROOT / report).exists():
                    errors.append(f"{eid}: missing report {report}")
                if config and not (ROOT / config).exists():
                    errors.append(f"{eid}: missing config {config}")

claims = ROOT / "paper" / "CLAIMS.md"
if claims.exists():
    text = claims.read_text(encoding="utf-8")
    refs = set(re.findall(r"\bE-\d{4}\b", text))
    for ref in refs:
        if ref not in known_experiments and ref != "E-0001":
            warnings.append(f"paper claim references experiment not in registry: {ref}")

state = ROOT / "context" / "STATE.md"
if state.exists() and len(state.read_text(encoding="utf-8").splitlines()) > 180:
    warnings.append("context/STATE.md is >180 lines; consider compacting it")

if errors:
    print("ERRORS")
    for x in errors:
        print(" -", x)
if warnings:
    print("WARNINGS")
    for x in warnings:
        print(" -", x)
if not errors and not warnings:
    print("context validation: OK")

sys.exit(1 if errors else 0)
