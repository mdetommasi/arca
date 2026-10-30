# PLAN-001 — Unified ARCA CLI

Status: completed
Created: 2026-10-30
Completed: 2026-10-30
Owner: Codex

## Goal

Provide one local interface for project initialization, status, structural
checks, experiment scaffolding, and checkpoints. Share the implementation
between the CLI, legacy scripts, and agent workflows.

## Success criteria

- [x] `./arca` and `python3 -m arca_cli` work without third-party dependencies.
- [x] An optional package installation exposes the `arca` console command.
- [x] Commands discover the project from the working directory or `--root`.
- [x] Initialization fills only empty/template objective and next-action sections.
- [x] Read-only commands preserve files and Git state; JSON output supports agents.
- [x] Legacy helper scripts retain their existing invocation and output conventions.
- [x] Documentation, skills, and automated integration tests cover the interface.

## Scope

Initialization configures an existing ARCA scaffold; template distribution,
scheduler integration, scientific evaluation, and evidence-graph expansion
remain separate work. No GPU jobs or external services are required.

## Plan

1. [x] Inspect current scripts, templates, and agent workflows.
2. [x] Implement a shared Python core, CLI, and compatibility wrappers.
3. [x] Add meaningful integration tests using isolated temporary projects.
4. [x] Update documentation and skills; record verification and handoff.

## Verification

Use standard-library unittest integration tests, CLI smoke checks, legacy
script checks, and an isolated package installation. Exercise preservation of
existing records, non-root invocation, JSON output, failure codes, experiment
registration, and repeated checkpoints.

## Decisions

- Keep Python standard library as the only runtime dependency.
- Keep initialization distinct from copying or merging the repository template.
- A checkpoint snapshots existing notes; the agent still supplies their content.

## Verification and handoff

- 21 unittest integration tests passed; regular and editable console-command
  installation and Codex/Claude skill structural validation succeeded.
- A disposable copy of the current template passed init/status/check, including
  the framework maintenance notes retained in STATE/NEXT.
- `docs/CLI.md` documents setup, commands, JSON, limitations, and compatibility.
- Canonical STATE/NEXT retain their scientific template sections while recording
  the framework maintenance handoff. No scientific findings were fabricated.
- The user requested publication with the updated README and documentation on
  2026-10-30. Read Git HEAD/upstream for the publication revision. Next executable
  action: `./arca status --full`.
