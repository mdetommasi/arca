---
name: arca
description: Initialize an existing ARCA research project, inspect its state, prepare an experiment, check its structure, or checkpoint a session through the shared local CLI.
---

# ARCA project interface

Use the shared CLI for repository operations. Run `python3 -m arca_cli` from
the project root, or use an installed `arca --root PATH` command. Read
`docs/CLI.md` when command options or initialization behavior matter.

## Select the requested operation

- **Initialize:** inspect `AGENTS.md`, the charter, STATE, and NEXT. Establish
  the research objective and exact next action with the user, using facts
  already supplied. Run `python3 -m arca_cli init --objective "..."
  --next-action "..." --json`. Review the changed sections and complete only
  the scientific details the user has supplied. If initialization reports
  existing content, preserve it and inspect the conflicting section.
- **Status or resume:** run `python3 -m arca_cli status --json`. For a full
  research handoff, follow `.agents/skills/arca-resume/SKILL.md`. Job counts
  and experiment labels are recorded state; the CLI does not query a scheduler.
- **Prepare an experiment:** run `python3 -m arca_cli experiment new "title"
  --json`, then complete the relevant protocol with the known baseline,
  data, metrics, seeds, and constraints. Allocation creates starter files.
- **Check:** run `python3 -m arca_cli check --json` and report errors and
  warnings. Structural validation does not certify a scientific conclusion.
- **Checkpoint:** follow `.agents/skills/arca-checkpoint/SKILL.md` to update
  the canonical notes before creating the snapshot.

Report the operation, changed paths or observed state, verification, and any
missing input. The CLI does not run training or make Git commits.
