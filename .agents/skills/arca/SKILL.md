---
name: arca
description: Initialize an existing ARCA research project, install optional CortexDB/Feynman integrations, inspect state, prepare an experiment, check structure, or checkpoint a session through the shared CLI.
---

# ARCA project interface

Use the shared CLI for repository operations. Run `python3 arca` from
the project root, or use an installed `arca --root PATH` command. Read
`docs/CLI.md` when command options or initialization behavior matter.

## Select the requested operation

- **Initialize:** inspect `AGENTS.md`, the charter, STATE, and NEXT. Establish
  the research objective and exact next action with the user, using facts
  already supplied. Run `python3 arca init --objective "..."
  --next-action "..." --json`. Review the changed sections and complete only
  the scientific details the user has supplied. If initialization reports
  existing content, preserve it and inspect the conflicting section.
- **Optional integrations:** when requested during init, append
  `--with cortexdb feynman --scope project` (or only the requested integration).
  Honor an explicit `--scope user` or `--agents claude` / `--agents codex`.
  Default to project scope and both hosts; plain init installs nothing extra.
  For an existing project, use `python3 arca integrations install cortexdb
  feynman --scope project --json` without reinitializing research notes.
  Use `--dry-run` for a requested preview and `integrations status --scope
  project --json` to inspect files. Read `docs/INTEGRATIONS.md` for locations,
  conflict recovery, and the Feynman skills-edition boundary. Installation
  requires network access; user scope applies to all projects. On success,
  report that the user should reopen the agent session and handle its normal
  MCP trust prompt, then use `/feynman lit ...` / `$feynman lit ...` or the
  `cortexdb` skill. Do not report MCP connectivity from the file-status check.
- **Status or resume:** run `python3 arca status --json`. For a full
  research handoff, follow `.agents/skills/arca-resume/SKILL.md`. Job counts
  and experiment labels are recorded state; the CLI does not query a scheduler.
- **Prepare an experiment:** run `python3 arca experiment new "title"
  --json`, then complete the relevant protocol with the known baseline,
  data, metrics, seeds, and constraints. Allocation creates starter files.
- **Check:** run `python3 arca check --json` and report errors and
  warnings. Structural validation does not certify a scientific conclusion.
- **Checkpoint:** follow `.agents/skills/arca-checkpoint/SKILL.md` to update
  the canonical notes before creating the snapshot.

Report the operation, changed paths or observed state, verification, and any
missing input. The CLI does not run training or make Git commits.
