# ARCA Agent Contract · v2.0

Cross-agent rules for Codex, Claude Code and collaborators. Read only relevant material.

## Orientamento

- Read `research/CHARTER.md` to understand scientific goals or scope.
- Read `context/STATE.md` and `context/NEXT.md` when resuming long-running work, switching agents or changing scientific direction.
- Follow `context/MAP.md` to locate detailed evidence; do **not** load every file on every task.
- If a task spans sessions, maintain an active plan in `research/plans/active/`; skip this for trivial edits.

## Epistemic discipline

- Distinguish measured FACT, external SOURCE CLAIM, HYPOTHESIS, INTERPRETATION and DECISION.
- Every publishable quantitative claim must resolve to `paper/CLAIMS.md` -> finding `F-###` -> experiment `E-####` -> metrics/config/commit/dataset/artifacts.
- Preserve informative negative experiments and contradictions. Do not silently upgrade uncertain findings to facts.
- An automatically recalled memory is a **lead**: verify against repository records before relying on it.

## Experimental workflow

- For a substantive ML experiment, create an experiment ID and record the baseline, intended test, config, data fingerprint, split, seed policy, metrics and environment.
- Store raw artifacts outside Git when large; register URI, hash and provenance in `artifacts/manifest.jsonl`.
- After completion, update the experiment report/registry, relevant findings and manuscript claim links.
- Verify code changes with tests appropriate to their risk. For scientific claims include no-leakage and baseline/comparability checks.

## Continuity

- Before long breaks, model handoffs, manual compaction or session completion, update `STATE.md`/`NEXT.md` and add an entry to `research/LAB_NOTEBOOK.md` when meaningful.
- Make `NEXT.md` specify one exact, executable next action.
- Keep handoff compact; archive large transcripts separately.

## Memory and skills

- CortexDB is optional (`memory/CORTEXDB.md`); Git-tracked files remain canonical. Never insert secrets, private data, or unsupported claims into automatic memory.
- Skills are opt-in, task-scoped procedures in `.agents/skills/` or `.claude/skills/` (`docs/SKILLS.md`). Do not activate every skill by default.
- Avoid duplicating Feynman or platform-native procedures unless repeated local needs justify it.

## Done

A substantive task is done when the requested implementation/analysis is verified, links to evidence are current, and ongoing work can be resumed from the repository. Do not impose the full experiment workflow on trivial maintenance.
