#!/usr/bin/env python3
from __future__ import annotations
import csv
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
REG = EXP / "REGISTRY.csv"
TPL = EXP / "templates"

def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s[:60] or "experiment"

def next_id():
    mx = 0
    if REG.exists():
        with REG.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                m = re.fullmatch(r"E-(\d+)", row.get("experiment_id", ""))
                if m:
                    mx = max(mx, int(m.group(1)))
    return f"E-{mx+1:04d}"

def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

if len(sys.argv) < 2:
    raise SystemExit('usage: new_experiment.py "experiment title"')

title = " ".join(sys.argv[1:]).strip()
eid = next_id()
folder = EXP / f"{eid}-{slugify(title)}"
folder.mkdir(parents=True)

stamp = datetime.now(timezone.utc).isoformat()
yaml_text = (TPL / "experiment.yaml").read_text(encoding="utf-8")
yaml_text = yaml_text.replace("experiment_id: E-0000", f"experiment_id: {eid}", 1)
yaml_text = yaml_text.replace('title: ""', f'title: "{title.replace(chr(34), chr(39))}"', 1)
yaml_text = yaml_text.replace('created_at: ""', f'created_at: "{stamp}"', 1)
yaml_text = yaml_text.replace('git_commit: ""', f'git_commit: "{git_commit()}"', 1)
(folder / "experiment.yaml").write_text(yaml_text, encoding="utf-8")

report = (TPL / "report.md").read_text(encoding="utf-8")
report = report.replace("Experiment E-0000 — Title", f"Experiment {eid} — {title}", 1)
(folder / "report.md").write_text(report, encoding="utf-8")
(folder / "metrics.json").write_text("{}\n", encoding="utf-8")
(folder / "runs").mkdir()

with REG.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        eid, title, "planned", stamp, "", "", "", git_commit(), "",
        str((folder / "experiment.yaml").relative_to(ROOT)), "", "", "",
        str((folder / "report.md").relative_to(ROOT))
    ])

print(folder)
