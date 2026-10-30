# ARCA v2 Context Architecture

Layer 0 — `AGENTS.md`, `CLAUDE.md`: lean instructions and pointers, not historical dumps.

Layer 1 — `context/STATE.md`, `context/NEXT.md`: current/restart state, short and maintained on significant transitions.

Layer 2 — `research/` and `research/literature/`: scientific knowledge, negative results, questions, hypotheses, decisions and sourced literature.

Layer 3 — `experiments/`, `configs/`, `data/`, `artifacts/`: immutable evidence paths, run/protocol provenance.

Layer 4 — `paper/`: claims tied to evidence, figures and current manuscript status.

Layer 5 (optional) — `memory/` + external CortexDB backend: semantic recall, graph traversal and navigation. Recover and **verify** canonical references before making scientific claims.

Layer 6 (on-demand) — `.agents/skills/` (Codex) + `.claude/skills/` (Claude thin adapters): one focused workflow per specialist skill. Do not inject them in every session.

**Default:** all layers other than CortexDB work entirely without external services. Avoid duplicate hook reinjection when CortexDB auto-recall is enabled.
