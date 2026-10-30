# Current Research State

> Documento mutabile e ad alta densità informativa. Mantenerlo idealmente entro 100-150 righe.

Last updated: 2026-10-30 (template maintenance)
Git branch: main
Git commit: eb8b0cf (implementation base; use Git HEAD for the current revision)
Active plan: none; see `research/plans/completed/PLAN-001-unified-cli.md`.

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

- Working pipeline: shared ARCA CLI (`./arca`, `python3 -m arca_cli`, optional installed `arca`).
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

- CLI operations: `init`, `status`, `check`, `experiment new`, `checkpoint`.
- Agent interface: `$arca` in Codex or `/arca` in Claude; canonical workflow in `.agents/skills/arca/SKILL.md`.
- Existing helper scripts delegate to `arca_cli/`; retain that directory when updating an older project.
- FACT: 21 isolated integration tests passed; regular and editable package installations were verified in a temporary environment.
- FACT: a disposable copy of the current template passed initialization, status, and strict structural validation.
- FACT: canonical and Claude skill files passed their structural validation.
- FACT: README, CLI/skills/compatibility docs, and the four-page illustrated PDF cover extension-chat invocation, terminal use, and Remote SSH; invocation syntax checked against official docs on 2026-10-30.
- Editable PDF source: `docs/ARCA_Quick_Start_User_Guide.html`; regeneration instructions in `docs/CLI.md`.
- Initialization fills only the objective and next-action template sections; other research facts need user input.
- Checkpoint snapshots existing notes. The agent updates notes first; no scheduler or scientific correctness is checked by the CLI.
- No ML experiments or GPU jobs were launched for this implementation.
- Usage and verification commands: `docs/CLI.md`; framework next action: `context/NEXT.md` / Template maintenance.
