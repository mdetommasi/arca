"""Repository operations shared by the CLI and legacy helper scripts.

Operations receive an explicit project root. Importing this module never
modifies files, changes Git state, or starts external services.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class ArcaError(Exception):
    """An actionable user-facing repository error."""


CONTEXT_FILES = (
    "AGENTS.md", "CLAUDE.md", "research/CHARTER.md", "context/STATE.md",
    "context/NEXT.md", "research/LAB_NOTEBOOK.md", "research/FINDINGS.md",
    "research/CONTRADICTIONS.md", "experiments/REGISTRY.csv",
    "artifacts/manifest.jsonl", "paper/CLAIMS.md",
)
CHECK_FILES = CONTEXT_FILES + (
    "framework.yaml", "memory/CORTEXDB.md", "docs/GUIDELINES_v2.md",
    ".agents/skills/research-evidence-audit/SKILL.md",
    ".claude/skills/research-evidence-audit/SKILL.md",
)
PLACEHOLDERS = {
    "objective": "Quale risultato scientifico/tecnico vuoi ottenere?",
    "state": "Descrivi l'obiettivo immediato e il suo legame con `research/CHARTER.md`.",
    "next": "1. [ ] ...",
}


def find_root(explicit=None, start=None):
    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        if not root.is_dir():
            raise ArcaError(f"Project directory does not exist: {root}")
        return root
    current = Path(start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "framework.yaml").is_file():
            return candidate
    raise ArcaError(
        "No ARCA project found. Open a folder containing the ARCA template, "
        "or select it with --root PATH. See docs/CLI.md for setup."
    )


def read_text(root, relative):
    path = root / relative
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ArcaError(f"Cannot read {relative}: {exc}") from exc


def git_output(root, *args):
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(root), *args],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.rstrip("\r\n") if result.returncode == 0 else None


def git_snapshot(root):
    location = git_output(root, "rev-parse", "--show-toplevel")
    if location is None:
        return {"available": False, "root": None, "branch": None,
                "commit": None, "dirty": None, "status": None}
    status = git_output(root, "status", "--short")
    return {
        "available": True,
        "root": location,
        "branch": git_output(root, "branch", "--show-current"),
        "commit": git_output(root, "rev-parse", "HEAD"),
        "dirty": bool(status) if status is not None else None,
        "status": status,
    }


def read_registry(root):
    path = root / "experiments/REGISTRY.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "experiment_id" not in reader.fieldnames:
                raise ArcaError("experiments/REGISTRY.csv has no experiment_id column.")
            if len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ArcaError("experiments/REGISTRY.csv contains duplicate columns.")
            rows = list(reader)
            if any(None in row for row in rows):
                raise ArcaError("experiments/REGISTRY.csv contains extra CSV fields.")
            return reader.fieldnames, rows
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ArcaError(f"Cannot read experiments/REGISTRY.csv: {exc}") from exc


def experiment_rows(root):
    return read_registry(root)[1]


def validate(root, context_only=False):
    errors, warnings = [], []
    for relative in CONTEXT_FILES if context_only else CHECK_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing: {relative}")
    known = set()
    registry = root / "experiments/REGISTRY.csv"
    if registry.is_file():
        try:
            for row in experiment_rows(root):
                eid = (row.get("experiment_id") or "").strip()
                if not eid:
                    continue
                known.add(eid)
                for key in ("report_path", "config_path"):
                    relative = (row.get(key) or "").strip()
                    if relative and not (root / relative).is_file():
                        errors.append(f"{eid}: missing {key}: {relative}")
        except ArcaError as exc:
            errors.append(str(exc))
    claims = root / "paper/CLAIMS.md"
    if claims.is_file():
        for ref in sorted(set(re.findall(r"\bE-\d{4}\b", read_text(root, "paper/CLAIMS.md")))):
            if ref not in known:
                warnings.append(f"Paper claim references experiment not in registry: {ref}")
    state = root / "context/STATE.md"
    if state.is_file() and len(read_text(root, "context/STATE.md").splitlines()) > 180:
        warnings.append("context/STATE.md is >180 lines; consider compacting it")
    return {"root": str(root), "ok": not errors, "errors": errors,
            "warnings": warnings, "scope": "structure and selected references"}


def section_span(text, heading):
    match = re.search(r"^## " + re.escape(heading) + r"[ \t]*\r?$", text, re.MULTILINE)
    if not match:
        raise ArcaError(f"Missing section: ## {heading}")
    following = re.search(r"^## ", text[match.end():], re.MULTILINE)
    end = match.end() + following.start() if following else len(text)
    return match.end(), end


def section(text, heading):
    start, end = section_span(text, heading)
    return text[start:end].strip()


def configured_value(value, placeholder):
    return value if value and value not in (placeholder, "...") else None


def initialization_values(root):
    # Read and inspect all targets before prompting or writing anything.
    targets = (
        ("research/CHARTER.md", "Research objective", "objective"),
        ("context/STATE.md", "Current objective", "state"),
        ("context/NEXT.md", "Now", "next"),
    )
    values = {}
    for relative, heading, key in targets:
        content = section(read_text(root, relative), heading)
        values[key] = configured_value(content, PLACEHOLDERS[key])
    return values


def initialize(root, objective, next_action):
    objective, next_action = objective.strip(), next_action.strip()
    if not objective or not next_action:
        raise ArcaError("Both a research objective and a concrete next action are required.")
    if "\n" in objective or "\n" in next_action or "\r" in objective + next_action:
        raise ArcaError("Use a single line for the objective and for the next action.")
    targets = (
        ("research/CHARTER.md", "Research objective", "objective", objective),
        ("context/STATE.md", "Current objective", "state", objective),
        ("context/NEXT.md", "Now", "next", f"1. [ ] {next_action}"),
    )
    updates = []
    for relative, heading, key, replacement in targets:
        text = read_text(root, relative)
        start, end = section_span(text, heading)
        old = text[start:end].strip()
        if old == replacement:
            continue
        if configured_value(old, PLACEHOLDERS[key]) is not None:
            raise ArcaError(
                f"{relative}: ## {heading} already contains project notes. "
                "Initialization preserves existing content; review this section with your agent."
            )
        updated = text[:start] + "\n\n" + replacement + "\n\n" + text[end:]
        if relative.startswith("context/"):
            stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            updated = re.sub(r"^Last updated: .*", f"Last updated: {stamp}", updated,
                             count=1, flags=re.MULTILINE)
        updates.append((relative, updated))
    for relative, content in updates:
        (root / relative).write_text(content, encoding="utf-8")
    return {"root": str(root), "updated": [item[0] for item in updates],
            "objective": objective, "next_action": next_action,
            "note": "Review questions, datasets, metrics, and compute constraints with your agent."}


def status(root):
    state = read_text(root, "context/STATE.md")
    next_text = read_text(root, "context/NEXT.md")
    objective = section(read_text(root, "research/CHARTER.md"), "Research objective")
    next_section = section(next_text, "Now")
    actions = re.findall(r"^\s*(?:\d+[.)]|[-*])\s+\[ \]\s+(.+)$", next_section, re.MULTILINE)
    next_action = next((a.strip() for a in actions if a.strip() != "..."), None)
    rows = experiment_rows(root)
    counts = {}
    for row in rows:
        value = (row.get("status") or "unknown").strip() or "unknown"
        counts[value] = counts.get(value, 0) + 1
    warnings = []
    if configured_value(objective, PLACEHOLDERS["objective"]) is None:
        objective = None
        warnings.append("Research objective is still a template; run arca init.")
    if next_action is None:
        warnings.append("No concrete unchecked action is recorded under NEXT.md / Now.")
    git = git_snapshot(root)
    if not git["available"]:
        warnings.append("Git metadata is unavailable.")
    elif git["commit"] is None:
        warnings.append("No Git commit is available yet.")
    return {
        "root": str(root), "objective": objective, "next_action": next_action,
        "git": git, "experiments": {"total": len(rows), "by_status": counts},
        "state": state, "next": next_text, "warnings": warnings,
        "job_status": "unknown (recorded context only; no scheduler queried)",
    }


def slugify(title):
    return re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower()).strip("-")[:60] or "experiment"


def new_experiment(root, title):
    title = title.strip()
    if not title:
        raise ArcaError("Experiment title cannot be empty.")
    if "\n" in title or "\r" in title:
        raise ArcaError("Use a single line for the experiment title.")
    fields, rows = read_registry(root)
    ids = [int(match.group(1)) for row in rows
           if (match := re.fullmatch(r"E-(\d+)", row.get("experiment_id") or ""))]
    eid = f"E-{max(ids, default=0) + 1:04d}"
    folder = root / "experiments" / f"{eid}-{slugify(title)}"
    if any((root / "experiments").glob(f"{eid}-*")):
        raise ArcaError(f"An experiment folder already uses {eid}; review the registry before allocating another ID.")
    config = read_text(root, "experiments/templates/experiment.yaml")
    report = read_text(root, "experiments/templates/report.md")
    stamp = datetime.now(timezone.utc).isoformat()
    git = git_snapshot(root)
    commit = git["commit"] or ""
    row = {
        "experiment_id": eid, "title": title, "status": "planned", "date": stamp,
        "parent_experiment": "", "question_ids": "", "hypothesis_ids": "",
        "git_commit": commit, "dataset_ids": "",
        "config_path": (folder / "experiment.yaml").relative_to(root).as_posix(),
        "primary_metric": "", "primary_value": "", "decision": "",
        "report_path": (folder / "report.md").relative_to(root).as_posix(),
    }
    missing = sorted(set(row) - set(fields))
    if missing:
        raise ArcaError("Experiment registry is missing columns: " + ", ".join(missing))
    for old, new in (
        ("experiment_id: E-0000", f"experiment_id: {eid}"),
        ('title: ""', "title: " + json.dumps(title, ensure_ascii=False)),
        ('created_at: ""', f'created_at: "{stamp}"'),
        ('git_commit: ""', f'git_commit: "{commit}"'),
        ("git_dirty: false", "git_dirty: " + str(git["dirty"]).lower()
         if git["dirty"] is not None else "git_dirty: null"),
    ):
        if old not in config:
            raise ArcaError(f"Experiment template is missing expected field: {old}")
        config = config.replace(old, new, 1)
    if "Experiment E-0000 — Title" not in report:
        raise ArcaError("Experiment report template is missing its title placeholder.")
    report = report.replace("Experiment E-0000 — Title", f"Experiment {eid} — {title}", 1)
    folder.mkdir()
    (folder / "experiment.yaml").write_text(config, encoding="utf-8")
    (folder / "report.md").write_text(report, encoding="utf-8")
    (folder / "metrics.json").write_text("{}\n", encoding="utf-8")
    (folder / "runs").mkdir()
    with (root / "experiments/REGISTRY.csv").open("a", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=fields).writerow(row)
    return {"root": str(root), "experiment_id": eid, "path": str(folder),
            "status": "planned", "note": "Starter files created. Complete the protocol before running training."}


def checkpoint(root):
    state, next_text = read_text(root, "context/STATE.md"), read_text(root, "context/NEXT.md")
    git = git_snapshot(root)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory = root / "context/session_archive"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"checkpoint-{stamp}.md"
    content = (
        f"# Context checkpoint {stamp}\n\n"
        f"Branch: {git['branch'] or 'unknown'}\nCommit: {git['commit'] or 'unknown'}\n\n"
        f"## Git status\n\n```text\n{git['status'] if git['status'] is not None else 'unknown'}\n```\n\n"
        f"## STATE\n\n{state}\n\n## NEXT\n\n{next_text}\n"
    )
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content.rstrip("\n") + "\n")
    return {"root": str(root), "path": str(path),
            "note": "Snapshot of existing STATE/NEXT. Their content has not been updated by this command."}
