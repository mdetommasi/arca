---
name: arca-resume
description: Resume an ARCA research project after a break, model switch, compaction, or new session. Read the canonical research state, verify Git and experiment references, then report the precise next action without changing files or launching jobs.
---

# ARCA Resume

## Purpose
Reconstruct a reliable, concise snapshot of the active ARCA research project. Treat Git-backed project records as canonical; CortexDB recall (if available) is only a lead to verify.

## Procedure
1. Locate the repository root containing `AGENTS.md` and `context/STATE.md`. If missing, report the issue; do not invent paths.
2. Run `python3 -m arca_cli status --json` from the project root. It returns canonical STATE/NEXT text, the research objective, next action, Git metadata, and experiment counts. Read `AGENTS.md`, relevant sections of `research/CHARTER.md`, and, when needed, `context/MAP.md`. Keep context loading selective.
3. Inspect the returned Git snapshot and, when relevant, `git log -5 --oneline`. Note uncommitted work and branch/commit mismatches with STATE. If the CLI is unavailable in an older project, read STATE/NEXT and run the Git checks directly. The CLI does not inspect a scheduler or verify that recorded jobs are running.
4. Follow relevant references to the active plan (`research/plans/active/`), experiment report and `experiments/REGISTRY.csv`. Inspect the latest pertinent `research/LAB_NOTEBOOK.md` entry and only those findings/decisions/contradictions required by the task.
5. Verify that paths and experiment/artifact identifiers mentioned in the current work exist. Where an artifact is remote or inaccessible, explicitly say it was not verified. Do not infer a result from an old chat or memory recall.
6. Report, briefly: research objective; latest **verified** findings with source IDs; active experiment/status; important blockers and inconsistencies; any running job that is explicitly evidenced (otherwise unknown); and one concrete next action, including whether approval is required.

## Non-negotiable rules
- **Read-only.** Do not edit files, start/stop processes, launch GPU jobs, change Git state or perform network-dependent actions without explicit user direction.
- Distinguish measured facts, interpretations, hypotheses, and pending validations.
- Do not claim an experiment, checkpoint or background process exists unless verified.
- End by asking the researcher whether to proceed with the suggested action, rather than executing it.
