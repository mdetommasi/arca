# Research Lab Notebook

Append-only. Ogni sessione significativa aggiunge una voce.

---

## YYYY-MM-DD HH:MM — Session title

Agent/model:
Branch:
Commit:
Active question/hypothesis:
Active experiment:

### Intent

...

### Actions

- ...

### Observations

- FACT:
- FACT:

### Interpretations

- INTERPRETATION:

### Failures / dead ends

- ...

### Decisions

- RDR-...

### Files/artifacts produced

- ...

### Next

- ...

---

## 2026-10-30 — Unified CLI implementation (framework maintenance)

Agent: Codex
Branch: main
Base commit: eb8b0cf
Scientific question/experiment: not applicable; no ML run.

### Intent and implementation

- DECISION: prioritize one user interface before the other harness proposals.
- Implemented the standard-library `arca_cli` core, checkout launcher, and
  optional installable `arca` command. Commands: init, status, check,
  experiment new, checkpoint; JSON output and explicit project selection.
- Legacy scripts call the same implementation. Added the `arca` skill and
  thin Claude adapters; documented commands in `docs/CLI.md` and the README.
- Initialization preserves existing notes and preflights target sections.
  New experiment records preserve title/CSV encoding and Git dirty/unknown
  provenance. Checkpoint filenames include microseconds and use exclusive creation.

### Verification

- FACT: 21 isolated unittest integration tests passed, including initialization
  conflicts/idempotency, read-only operations, project discovery, JSON output,
  reordered registries, ID reuse protection, real Git provenance, and legacy helpers.
- FACT: a regular package installation exposed the console command and passed
  structural validation in a temporary virtual environment, without fetching dependencies.
- FACT: editable installation also exposed the console command and passed strict
  validation. A disposable copy of the current template passed init/status/check.
- FACT: changed Codex and Claude skill files passed skill structural validation.
- No claim of scientific validity or scheduler/process monitoring is made by these checks.

### Handoff

- Research objective and queue remain initializable template sections.
- Framework context is recorded in STATE/NEXT; completed plan:
  `research/plans/completed/PLAN-001-unified-cli.md`.
- Next: run `./arca status --full` for a user review of the interface.

## 2026-10-30 — Documentation and publication preparation

- User requested updated README/documentation and commit/push of the unified CLI.
- Clarified extension chat skill invocation (`/arca` in Claude Code, `$arca`
  in Codex), direct terminal commands, optional installation, and Remote SSH.
- SOURCE CLAIM: official Codex/Claude documentation supports the described
  invocation and discovery mechanisms; references and access date are in
  `docs/CLI.md`. Interactive extension behavior was not tested locally.
- FACT: regenerated the Quick Start PDF as four pages and inspected all pages;
  the editable HTML source is now tracked alongside the PDF.
- FACT: all 21 CLI integration tests and strict structural validation passed
  again during this documentation update.
- DECISION: publish the CLI implementation, agent adapters, documentation,
  tests, and continuity records together. Git HEAD/upstream records the
  resulting publication revision.
