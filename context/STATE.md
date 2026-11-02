# Current Research State

> Documento mutabile e ad alta densità informativa. Mantenerlo idealmente entro 100-150 righe.

Last updated: 2026-11-02 (template maintenance)
Git branch: main
Git commit: 615cebb (feature base; use Git HEAD and working tree for current changes)
Active plan: none; see `research/plans/completed/PLAN-002-integrations.md`.

This repository remains a reusable research template. Research objective and
experiment fields below are intentionally uninitialized for `arca init`.

## Current objective

Descrivi l'obiettivo immediato e il suo legame con `research/CHARTER.md`.

## Current scientific state

- Supported findings:
- Refuted hypotheses:
- Leading hypotheses:
- Important unresolved contradictions:

## Current technical state

- Working pipeline: shared ARCA CLI (`./arca`, `python3 arca`, optional installed `arca`).
- Current model/config:
- Current dataset/version:
- Best verified result:
- Known broken/fragile areas:

## Current experiment

Experiment ID:
Status:
Command/job:
Artifact locations:
Expected next observation:

## Paper/report impact

Claim IDs affected:
Figures/tables affected:
Sections requiring update:

## Blockers

- ...

## Critical reminders for the next agent

- CLI operations: `init`, `status`, `check`, `experiment new`, `checkpoint`, `integrations install/status`.
- Agent interface: `$arca` in Codex or `/arca` in Claude; canonical workflow in `.agents/skills/arca/SKILL.md`.
- Existing helper scripts delegate to `scripts/arca_cli/`; retain that directory and `scripts/__init__.py` when updating an older project.
- FACT: 46 isolated tests passed, including all 21 original CLI tests and 25 integration-installer tests.
- FACT: a disposable copy of the current template passed initialization, status, and strict structural validation.
- FACT (2026-11-02): Hatchling wheel and editable installations passed in a temporary environment without recreating root-level build/ or egg-info directories; all 21 CLI tests passed.
- Packaging output: `.local/dist/` via `make package`. Old build/ and arca_research_cli.egg-info/ were moved recoverably to ignored `.local/packaging-archive.GpfTyu/`.
- FACT (2026-11-02): CLI source moved to `scripts/arca_cli/`; launcher, source module, legacy helpers, all 21 tests, wheel/editable installs, and sdist-to-wheel build passed. No root-level CLI package directory remains.
- Source invocation: `./arca` or `python3 arca` (module form: `python3 -m scripts.arca_cli`). Reinstall older editable copies once; installed command/import name stay `arca`/`arca_cli`.
- FACT: canonical and Claude skill files passed their structural validation.
- FACT: README, CLI/skills/compatibility docs, and the five-page illustrated PDF cover chat, terminal, Remote SSH, and optional integration setup; host integration docs checked on 2026-11-02.
- Editable PDF source: `docs/ARCA_Quick_Start_User_Guide.html`; regeneration instructions in `docs/CLI.md`.
- Initialization fills only the objective and next-action template sections; other research facts need user input.
- Optional setup: `init --with cortexdb feynman --scope project|user`; existing projects use `integrations install`. Both hosts are selected by default; plain init remains offline.
- CortexDB 2.142.0: pinned binary and local MCP config, one DB per scope, no automatic hooks. Feynman 0.5.61: original prompts/roles with an ARCA host adapter, not the standalone Pi runtime.
- FACT: real downloads, MCP handshake (115 tools), and cross-process memory save/recall passed on macOS ARM64 in a disposable project. Claude Code recognized the server; Codex UI/model workflows were not exercised.
- FACT: installed-wheel init with both integrations, status, repeat installation, and all four generated host skills passed verification. Live user profiles were not changed.
- Integration implementation and docs are complete and verified; see `docs/INTEGRATIONS.md` and completed PLAN-002. Publication requested on 2026-11-02; Git HEAD/upstream records the revision.
- Checkpoint snapshots existing notes. The agent updates notes first; no scheduler or scientific correctness is checked by the CLI.
- No ML experiments or GPU jobs were launched for this implementation.
- Usage and verification commands: `docs/CLI.md`; framework next action: `context/NEXT.md` / Template maintenance.
