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

## 2026-11-02 — Keep CLI packaging products out of the project root

- FACT: root-level `build/` and `arca_research_cli.egg-info/` were ignored
  packaging products left by the earlier setuptools installation tests.
- Moved those two directories recoverably into ignored
  `.local/packaging-archive.GpfTyu/`. Kept the CLI source and scientific
  artifact registry in their canonical locations.
- DECISION: use Hatchling for packaging, keep local distribution output under
  `.local/dist/`, and expose `make package` for a wheel build to that location.
- FACT: a wheel install and an editable install in a disposable virtual
  environment exposed a working `arca` entry point without recreating either
  root-level directory. All 21 CLI integration tests and strict structural
  validation passed. The source distribution was also generated under `.local/dist/`.
- No ML experiment, scientific claim, or artifact manifest was changed.
- Packaging changes remain local; next: review the packaging diff.

## 2026-11-02 — Group the CLI implementation with repository tools

- User prefers a lean top-level folder structure and proposed `scripts/` for
  the CLI when technically appropriate.
- DECISION: move the implementation into `scripts/arca_cli/`, leave the small
  root `arca` launcher, and reserve `src/` for research implementations.
- Updated helper imports, package selection, Make targets, test fixtures,
  canonical skills, README, CLI documentation, and the illustrated guide.
- Source execution is `./arca`, `python3 arca`, or
  `python3 -m scripts.arca_cli`. The installed command remains `arca` and the
  installed import name remains `arca_cli`. Older editable copies need one reinstall.
- FACT: all 21 CLI integration tests passed, including module execution,
  nested-directory use, and legacy helpers. Three changed canonical skills
  passed structural validation. The regenerated PDF has four pages.
- FACT: an older editable installation was reinstalled and resolved the new
  source path; the wheel installation resolved site-packages and passed the
  strict project check. A wheel was also rebuilt successfully from the sdist.
- Only stale bytecode remained in the old root directory after moving sources;
  archived it recoverably at `.local/packaging-archive.GpfTyu/old-cli-import-cache/`.
- Changes remain local; no scientific results, dataset records, or artifacts
  were changed. Next: `python3 arca status --full`.

## 2026-11-02 — Publish packaging cleanup and CLI source relocation

- User explicitly requested commit and push of the completed local changes.
- Reviewed the changed paths and reran strict structural validation and the
  whitespace check successfully. The earlier 21 tests and packaging checks
  remain applicable; no implementation changes followed them.
- Publication revision and upstream alignment are recorded by Git.
