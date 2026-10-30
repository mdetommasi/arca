---
name: arca-checkpoint
description: Prepare a reliable ARCA session handoff before ending work, switching between Claude Code and Codex, or compacting context. Update canonical STATE/NEXT and the research notebook as appropriate, then run the repository checkpoint script and report its path.
---

# ARCA Checkpoint

## Purpose
Create an actionable, evidence-aware handoff. `scripts/session_checkpoint.py` only **copies existing** STATE/NEXT plus Git metadata; it does not summarize the session or update source documents. Update the canonical records first.

## Procedure
1. Locate the ARCA repository root; read `AGENTS.md`, `context/STATE.md`, `context/NEXT.md`, and relevant active experiment/plan records. Inspect `git status --short --branch` and `git diff` for changes. Never infer that a modification was successfully tested merely because it appears in Git.
2. Reconstruct **what actually changed** in this session: implemented or edited files, completed verification, measured experimental outputs, failures, unfinished jobs and outstanding decisions. Distinguish verified facts from interpretations and open questions.
3. Update `context/STATE.md` with the current research/technical state, relevant experiment IDs, locations of verifiable outputs, blockers and manuscript impacts. Keep it compact; preserve rather than overwrite unrelated work.
4. Update `context/NEXT.md` with a small prioritized queue and **one precise executable next step**, including required approvals (especially substantial GPU jobs). State uncertainty and missing evidence.
5. Append a dated entry to `research/LAB_NOTEBOOK.md` for meaningful scientific work. Update `experiments/REGISTRY.csv`, experiment reports, `research/FINDINGS.md`, decisions/contradictions, artifact manifest or paper claims **only when the observed evidence calls for it**; never fabricate metrics, hashes or successful runs.
6. Verify the two context files are readable and consistent with relevant Git and experiment records. If available, run `python3 scripts/validate_context.py` and report warnings; do not automatically "fix" scientific disagreements.
7. Run `python3 scripts/session_checkpoint.py` from the repository root. Capture and report the generated path and current Git status. If the script is missing or fails, report the problem and provide the exact manual handoff files instead.
8. End with a concise handoff summary: updated files, checkpoint path, verified outcomes, unresolved issues and the next action.

## Safety and limits
- Do not create a Git commit, push, delete or rewrite history without explicit permission.
- Do not start, cancel, or resume GPU jobs. Document running jobs only if their status was actually inspected.
- Do not assume that transcript archiving or automatic CortexDB synchronization happened.
- If an automatic lifecycle hook invokes this skill without enough context or permission, do not make speculative edits; instead report what needs to be captured.
