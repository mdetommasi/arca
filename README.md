# ARCA — Agentic Research Context Architecture

**Version 2.0**

ARCA is a repository harness for machine-learning research that lasts across people, models, and sessions. It keeps the objective, hypotheses, experiments, negative results, decisions, and paper claims together, with provenance that can be checked from the files and from Git.

A coding agent (Claude Code, Codex, or a specialist agent) reads only the context that the current task needs. When the chat is compacted, the model changes, or work resumes after a pause, the scientific state stays in the repository.

## What it does

- **Defines the problem.** `research/CHARTER.md` records the objective, questions, scope, and success criteria.
- **Keeps a restartable state.** `context/STATE.md` and `context/NEXT.md` record where the work stands and the next executable action.
- **Separates fact, hypothesis, and interpretation.** Questions, hypotheses, findings, contradictions, and decisions stay distinct under `research/`.
- **Records every experiment.** Each run has an ID, a baseline, config, data fingerprint, split, seed, metrics, and commit.
- **Ties the paper to the evidence.** A publishable claim points to a finding, an experiment, and the artifacts.
- **Keeps negative results.** Refutations and failures stay visible, so later work starts from what has already been tried.
- **Works on its own.** CortexDB, if you enable it, is a semantic recall index. Versioned registries, metrics, and claims remain the source of truth.

## Principle

**Git-versioned files = source of truth. CortexDB = optional memory, semantic index, and knowledge graph.**

CortexDB does not replace the experiment registry, metrics, dataset fingerprints, decisions, findings, or paper claims.

## First run (no dependencies)

```bash
python3 scripts/arca_check.py
python3 scripts/new_experiment.py "initial baseline"
python3 scripts/session_checkpoint.py
```

Fill in `research/CHARTER.md`, `context/STATE.md`, and `context/NEXT.md`. Open VS Code at the repository root and work as usual with Claude Code or Codex.

## Where to look

| What | Where |
|---|---|
| Shared, lightweight instructions | `AGENTS.md` |
| Claude Code instructions | `CLAUDE.md` |
| State and next actions | `context/STATE.md`, `context/NEXT.md` |
| Hypotheses, results, decisions | `research/` |
| Experiments, config, provenance | `experiments/`, `data/`, `artifacts/` |
| Claims and manuscript | `paper/` |
| Optional CortexDB memory | `memory/CORTEXDB.md` |
| Optional skills | `.agents/skills/`, `.claude/skills/` |
| Full operating guide | `docs/GUIDELINES_v2.md` |
| Current agent compatibility | `docs/AGENT_COMPATIBILITY.md` |

## Installing CortexDB (only if you want it)

Follow `memory/CORTEXDB.md` for installation, per-project isolation, permissions, privacy, and diagnostics. **Using ARCA does not install or enable any backend automatically.**

## Creating a skill (only when you need one)

```bash
python3 scripts/new_skill.py "experimental-audit" "Use when validating a completed ML experiment against its recorded metrics and provenance."
```

The generator writes a `SKILL.md` for Codex and a minimal delegate for Claude Code. See `docs/SKILLS.md`.

## Safety boundaries

- Keep secrets, restricted datasets, and unauthorized private notes out of automatic memory.
- Move data to shared servers only with authorization, a token, and secure transport.
- Treat automatically recalled memory as a lead, and check it against the repository before using it as scientific evidence.
- Keep the system fully usable with CortexDB turned off.

## References

- [CortexDB (correct repo: liliang-cn/cortexdb)](https://github.com/liliang-cn/cortexdb)
- [Codex: guidance on skills and AGENTS.md, September 2026](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Codex skill locations](https://learn.chatgpt.com/docs/build-skills)
- [Claude Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
